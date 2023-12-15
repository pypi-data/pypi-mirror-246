import signal
import threading
from typing import Any, Callable, Optional

from numerous.sdk.connect.job_state import JobState
from numerous.sdk.connect.subscription import Subscription


class CommandHandler:
    def __init__(
        self, subscription: Subscription, state_getter: Callable[[], JobState]
    ):
        self._subscription = subscription
        self._state_getter = state_getter
        self._thread = threading.Thread(target=self._handler, daemon=True)
        self._thread.start()
        self._hibernation_callback: Optional[Callable[[], Any]] = None
        self.hibernating: bool = False

    def _handler(self):
        for message in self._subscription:
            command = message.message["command"]
            if command == "terminate":
                signal.raise_signal(signal.SIGTERM)
                return
            elif command == "hibernate":
                self.hibernating = True
                if self._hibernation_callback is not None:
                    self._hibernation_callback()
                self._state_getter().commit()
                signal.raise_signal(signal.SIGTERM)

    def close(self) -> None:
        self._thread.join()
