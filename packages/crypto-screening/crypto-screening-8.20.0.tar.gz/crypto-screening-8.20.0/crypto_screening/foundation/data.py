# data.py

import warnings
import datetime as dt
import time
from abc import ABCMeta, abstractmethod
import threading
from itertools import chain
from typing import Any

from looperator import Operator

from represent import represent

from crypto_screening.foundation.state import WaitingState

__all__ = [
    "DataCollector"
]

TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

def extract_attributes(data: Any, /) -> dict[str, Any]:
    """
    Gets all attributes of an object.

    :param data: The object.

    :return: The attributes of the object.
    """

    return {
        **(data.__dict__ if hasattr(data, '__dict__') else {}),
        **(
            {
                key: getattr(data, key)
                for key in chain.from_iterable(
                    getattr(cls, '__slots__', [])
                    for cls in type(data).__mro__
                ) if hasattr(data, key)
            } if hasattr(data, '__slots__') else {}
        )
    }

@represent
class DataCollector(metaclass=ABCMeta):
    """A class to represent an abstract parent class of data collectors."""

    LOCATION = "datasets"

    DELAY = 0
    CANCEL = 0

    __slots__ = (
        "location", "delay", "cancel", "_screening",
        "_blocking", "_saving", "_updating", "_screening_process",
        "_timeout_process", "_saving_process", "_updating_process"
    )

    def __init__(
            self,
            location: bool = None,
            cancel: TimeDestination = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        if delay is None:
            delay = self.DELAY

        if cancel is None:
            cancel = self.CANCEL

        self.cancel = cancel
        self.delay = delay

        self.location = location or self.LOCATION

        self._screening = False
        self._blocking = False
        self._saving = False
        self._updating = False

        self._timeout_process = Operator(termination=self.stop, loop=False)

        self._screening_process: threading.Thread | None = None
        self._saving_process: threading.Thread | None = None
        self._updating_process: threading.Thread | None = None

    def __getstate__(self) -> dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = extract_attributes(self)

        for key, value in data.items():
            if isinstance(value, threading.Thread):
                data[key] = None

        return data

    @property
    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._blocking

    @property
    def screening(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._screening

    @property
    def saving(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._saving

    @property
    def updating(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._updating

    @property
    def timeout(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._timeout_process.timeout

    def screening_loop(self) -> None:
        """Runs the process of the price screening."""

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

    def update_loop(self) -> None:
        """Updates the state of the screeners."""

    def timeout_loop(self, duration: TimeDestination) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        self._timeout_process.timeout_loop(duration=duration)

    @abstractmethod
    def await_initialization(
            self,
            stop: bool | int = False,
            delay: TimeDuration = None,
            cancel: TimeDestination = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

    @abstractmethod
    def await_update(
            self,
            stop: bool | int = False,
            delay: TimeDuration = None,
            cancel: TimeDestination = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

    def start_blocking(self) -> None:
        """Starts the blocking process."""

        if self.blocking:
            warnings.warn(
                f"Blocking process of "
                f"{repr(self)} is already running."
            )

            return

        self._blocking = True

        while self.blocking:
            time.sleep(0.005)

    def start_screening(self) -> None:
        """Starts the screening process."""

        if self.screening:
            warnings.warn(
                f"Screening process of "
                f"{repr(self)} is already running."
            )

            return

        self._screening = True

        self._screening_process = threading.Thread(
            target=self.screening_loop
        )

        self._screening_process.start()

    def start_saving(self) -> None:
        """Starts the saving process."""

        if self.saving:
            warnings.warn(
                f"Saving process of "
                f"{repr(self)} is already running."
            )

            return

        self._saving = True

        self._saving_process = threading.Thread(
            target=self.saving_loop
        )

        self._saving_process.start()

    def start_updating(self) -> None:
        """Starts the updating process."""

        if self.updating:
            warnings.warn(
                f"Updating process of "
                f"{repr(self)} is already running."
            )

            return

        self._updating = True

        self._updating_process = threading.Thread(
            target=self.update_loop
        )

        self._updating_process.start()

    def start_waiting(self, wait: bool | TimeDestination) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()

        if wait is True:
            self.await_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)

    def start_timeout(self, duration: TimeDestination) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        self._timeout_process.start_timeout(duration=duration)

    def pause_timeout(self) -> None:
        """Pauses the timeout process."""

        self._timeout_process.pause()

    def unpause_timeout(self) -> None:
        """Pauses the timeout process."""

        self._timeout_process.unpause()

    def run(
            self,
            screen: bool = True,
            save: bool = True,
            block: bool = False,
            update: bool = True,
            wait: bool | TimeDestination = False,
            timeout: TimeDestination = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param screen: The value to start the screening.
        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param update: The value to update the screeners.
        :param timeout: The valur to add a start_timeout to the process.
        """

        if screen:
            self.start_screening()

        if save:
            self.start_saving()

        if update:
            self.start_updating()

        if timeout:
            self.start_timeout(timeout)

        if wait:
            self.start_waiting(wait)

        if block:
            self.start_blocking()

    def stop_screening(self) -> None:
        """Stops the screening process."""

        if self.screening:
            self._screening = False

        if (
            isinstance(self._screening_process, threading.Thread) and
            self._screening_process.is_alive()
        ):
            self._screening_process = None

    def stop_saving(self) -> None:
        """Stops the screening process."""

        if self.saving:
            self._saving = False
        if (
            isinstance(self._saving_process, threading.Thread) and
            self._saving_process.is_alive()
        ):
            self._saving_process = None

    def stop_updating(self) -> None:
        """Stops the screening process."""

        if self.updating:
            self._updating = False
        if (
            isinstance(self._updating_process, threading.Thread) and
            self._updating_process.is_alive()
        ):
            self._updating_process = None

    def stop_timeout(self) -> None:
        """Stops the screening process."""

        self._timeout_process.stop_timeout()

    def stop_blocking(self) -> None:
        """Stops the screening process."""

        if self.blocking:
            self._blocking = False

    def stop(self) -> None:
        """Stops the screening process."""

        self.stop_screening()
        self.stop_saving()
        self.stop_blocking()
        self.stop_updating()
        self.stop_timeout()
