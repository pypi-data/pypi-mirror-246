from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import sleep
from typing import Iterable, Iterator, Optional, Sequence, TypeVar

import grpc
from numerous.grpc import spm_pb2, spm_pb2_grpc

from numerous.sdk.models.input import (
    InputSource,
    InputVariable,
    InputVariableScenarioSource,
)
from numerous.sdk.models.job import Job
from numerous.sdk.models.time_setup import RunMode

INPUT_READER_DEFAULT_BUFFER_SIZE = 10000
nan = float("nan")


class ReadRetryExhausted(Exception):
    """Raised when reading has been retried too many times."""


class DataListWrapper:
    """A helper class that wraps and chains data lists."""

    def __init__(
        self,
        data_lists: list[spm_pb2.DataList],
        repeat_offset: float,
        previous: Optional["DataListWrapper"] = None,
    ) -> None:
        self._index = next(
            (
                list(block.values)
                for data_list in data_lists
                for block in data_list.data
                if block.tag == "_index"
            )
        )
        self._repeat_offset = repeat_offset
        self._previous = previous
        self.min_key = min(self._index)
        self.max_key = max(self._index)
        self.last_key_step = self._find_last_key_step()

        self._values = {
            block.tag: list(block.values)
            for data_list in data_lists
            for block in data_list.data
            if block.tag != "_index"
        }
        self._reference_count = 0

    def _find_last_key_step(self) -> Optional[float]:
        if not self._index:
            if self._previous is not None:
                return self._previous.last_key_step
            else:
                return None

        if len(self._index) > 1:
            return self._index[-1] - self._index[-2]

        if self._previous is None:
            return None
        if last_index := self._previous.last_index():
            return self._index[-1] - last_index
        else:
            return None

    def last_index(self) -> Optional[float]:
        if self._index:
            return self._index[-1]
        elif self._previous:
            return self.last_index()
        else:
            return None

    def remove_previous(self) -> None:
        self._previous = None

    def last_value(self, tag: str) -> float:
        return self._values[tag][-1]

    def is_after(self, key: float) -> bool:
        upper_boundary = self.max_key + self._repeat_offset
        return key >= upper_boundary

    def is_before(self, key: float) -> bool:
        lower_boundary = self.min_key + self._repeat_offset
        return key < lower_boundary

    def read_tag(self, tag: str, key: float) -> float:
        offset_cancelled_key = key - self._repeat_offset
        previous_value: Optional[float] = None
        for value_key, value in zip(self._index, self._values[tag]):
            if offset_cancelled_key >= value_key:
                previous_value = value
                continue
            elif previous_value is None:
                raise KeyError(
                    f"Key {key!r} outside lower bound of data list, and no previous "
                    "value."
                )
            else:
                return previous_value
        raise RuntimeError("Could not read tag with no data.")


class InputStream(ABC):
    @abstractmethod
    def read_variables(self, key: datetime) -> dict[str, float]:
        ...


class ContinuousInputStream(InputStream):
    def __init__(
        self,
        spm_stub: spm_pb2_grpc.SPMStub,
        job_start_time: datetime,
        input_source: InputSource,
        input_variables: Iterable[InputVariable],
    ) -> None:
        raise NotImplementedError()

    def read_variables(self, key: datetime) -> dict[str, float]:
        raise NotImplementedError()


class DurationInputStream(InputStream):
    """A helper class that reads data from a specific input source."""

    def __init__(
        self,
        spm_stub: spm_pb2_grpc.SPMStub,
        job_start_time: datetime,
        job_end_time: datetime,
        input_source: InputSource,
        input_variables: Iterable[InputVariable],
        repeat_spacing: Optional[float] = None,
    ) -> None:
        self._spm_stub = spm_stub
        self._job_start_time = job_start_time
        self._job_end_time = job_end_time
        self._input_source = input_source
        self._input_variables = self._filter_input_variables(input_variables)
        self._maximum_input_variable_offset = max(
            input_variable.offset for input_variable in self._input_variables
        )
        self._repeat_spacing = repeat_spacing
        self._repeat_start_index: Optional[float] = None
        self._repeat_offset = 0.0
        self._stream: Optional[Iterator[spm_pb2.DataList]] = None
        self._data_lists: list[DataListWrapper] = []

    def _filter_input_variables(
        self,
        input_variables: Iterable[InputVariable],
    ) -> list[InputVariable]:
        return [
            input_variable
            for input_variable in input_variables
            if isinstance(input_variable.source, InputVariableScenarioSource)
            and input_variable.source.source == self._input_source
        ]

    def read_variables(self, key: datetime) -> dict[str, float]:
        return {
            ".".join(var.path): self._read_variable(var, var.source, key)
            for var in self._input_variables
        }

    def _read_variable(
        self,
        variable: InputVariable,
        source: InputVariableScenarioSource,
        key: datetime,
    ) -> float:
        if not isinstance(variable.source, InputVariableScenarioSource):
            raise ValueError()

        base_key = variable.job_time_to_base_time(key)
        previous_data_list: Optional[DataListWrapper] = None
        out_of_scope_data_lists: list[DataListWrapper] = []
        for data_list in self._data_lists:
            if data_list.is_after(base_key):
                self._collect_out_of_scope_data_list(
                    variable, out_of_scope_data_lists, previous_data_list, data_list
                )
                previous_data_list = data_list
            elif data_list.is_before(base_key):
                if not previous_data_list:
                    return nan
                previous_value = previous_data_list.last_value(variable.source.tag)
                variable.value = previous_value
                return previous_value
            else:
                current_value = data_list.read_tag(variable.source.tag, base_key)
                variable.value = current_value
                return current_value

        self._data_lists.append(self._get_next_data_list(key))
        for out_of_scope_data_list in out_of_scope_data_lists:
            self._data_lists.remove(out_of_scope_data_list)
        return self._read_variable(variable, source, key)

    def _collect_out_of_scope_data_list(
        self,
        variable: InputVariable,
        out_of_scope_data_lists: list[DataListWrapper],
        old_previous_data_list: Optional[DataListWrapper],
        new_previous_data_list: DataListWrapper,
    ):
        if variable.offset != self._maximum_input_variable_offset:
            return

        if old_previous_data_list is None:
            return

        out_of_scope_data_lists.append(old_previous_data_list)
        new_previous_data_list.remove_previous()

    def _get_next_data_list(self, key: datetime) -> DataListWrapper:
        data_lists = self._get_next_complete_data_lists(key)
        if data_lists:
            previous = self._data_lists[-1] if self._data_lists else None
            next_data_list = DataListWrapper(
                data_lists,
                self._repeat_offset,
                previous=previous,
            )
            if self._repeat_start_index is None:
                self._repeat_start_index = next_data_list.min_key
            return next_data_list
        else:
            if self._data_lists:
                last_data_list = self._data_lists[-1]
                self._repeat_offset += last_data_list.max_key
                self._repeat_offset -= self._repeat_start_index or 0.0
                if self._repeat_spacing is None:
                    if last_data_list.last_key_step is not None:
                        self._repeat_offset += last_data_list.last_key_step
                    else:
                        self._repeat_offset = 1.0
                else:
                    self._repeat_offset += self._repeat_spacing
            self._stream = self._create_stream(None)
            next_data_list = self._get_next_data_list(key)
            self._repeat_start_index = next_data_list.min_key
            return next_data_list

    def _get_next_complete_data_lists(self, key: datetime) -> list[spm_pb2.DataList]:
        if self._stream is None:
            self._stream = self._create_stream(key)

        data_lists: list[spm_pb2.DataList] = []
        while True:
            data_list = _next_grpc_retry(self._stream)
            if data_list and data_list.data:
                data_lists.append(data_list)

            if data_list is None or data_list.block_complete or data_list.row_complete:
                break

        return data_lists

    def _create_stream(self, key: Optional[datetime]) -> Iterator[spm_pb2.DataList]:
        is_closed: bool = self._spm_stub.GetDataSetClosed(
            request=spm_pb2.Scenario(
                project=self._input_source.project_id,
                scenario=self._input_source.scenario_id,
            )
        ).is_closed
        maximum_variable_offset = max(
            variable.offset for variable in self._input_variables
        )
        tags = [input_variable.source.tag for input_variable in self._input_variables]

        if key is None:
            start_time = 0.0
        else:
            start_time = (
                key.timestamp() - self._input_source.offset - maximum_variable_offset
            )

        end_time = self._job_end_time.timestamp() - self._input_source.offset
        request = spm_pb2.ReadScenario(
            scenario=self._input_source.scenario_id,
            project=self._input_source.project_id,
            tags=tags,
            start=start_time,
            end=end_time,
            time_range=True,
            listen=not is_closed,
        )

        return self._read_data_with_retry(request)

    def _read_data_with_retry(
        self,
        request: spm_pb2.ReadScenario,
        max_attempts: int = 5,
    ) -> Iterator[spm_pb2.DataList]:
        for attempt in range(max_attempts):
            try:
                return iter(self._spm_stub.ReadData(request=request))
            except grpc.RpcError:
                sleep(2**attempt)
        raise ReadRetryExhausted()


class InputReader(Iterable[tuple[datetime, dict[str, float]]]):
    """Reads input data according to the time setup of the current job.

    The input reader is meant to be used to iterate over the input data
    of the current job, taking into account the alignment of input sources,
    and input variables.

    During iteration the `value` attribute of :class:`InputVariable` objects in the
    scenario will be updated.
    """

    _streams: Sequence[InputStream]

    def __init__(
        self,
        spm_stub: spm_pb2_grpc.SPMStub,
        input_sources: list[InputSource],
        input_variables: list[InputVariable],
        job: Job,
        step: float = 1.0,
        repeat_spacing: Optional[float] = None,
    ) -> None:
        self._spm_stub = spm_stub
        self._input_sources = input_sources
        self._input_variables = input_variables
        self._start = job.time_setup.start
        self._end = job.time_setup.end
        self._next_key = self._start
        self._step = step
        self._repeat_spacing = repeat_spacing
        if job.time_setup.run_mode == RunMode.DURATION:
            self._streams = self._open_duration_streams()
        elif job.time_setup.run_mode == RunMode.CONTINUOUS:
            self._streams = self._open_continuous_streams()
        else:
            raise RuntimeError(
                f"Job {job.name!r} has invalid run mode {job.time_setup.run_mode!r}"
            )

    def _open_duration_streams(self) -> list[DurationInputStream]:
        return [
            DurationInputStream(
                self._spm_stub,
                self._start,
                self._end,
                input_source,
                self._input_variables,
                self._repeat_spacing,
            )
            for input_source in self._input_sources
        ]

    def _open_continuous_streams(self) -> list[ContinuousInputStream]:
        return [
            ContinuousInputStream(
                self._spm_stub, self._start, input_source, self._input_variables
            )
            for input_source in self._input_sources
        ]

    def __iter__(self) -> "InputReader":
        return self

    def __next__(self) -> tuple[datetime, dict[str, float]]:
        this_key = self._next_key
        if self._end is not None and this_key > self._end:
            raise StopIteration()

        self._next_key += timedelta(seconds=self._step)
        row_data = {
            variable_key: value
            for stream in self._streams
            for variable_key, value in stream.read_variables(this_key).items()
        }
        return (this_key, row_data)


T = TypeVar("T")


def _next_grpc_retry(iterator: Iterator[T], max_attempts: int = 5) -> Optional[T]:
    for attempt in range(max_attempts):
        try:
            return next(iterator, None)
        except grpc.RpcError:
            sleep(2**attempt)
    raise ReadRetryExhausted()
