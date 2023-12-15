# base.py

import time
import asyncio
import threading
import datetime as dt
import warnings
from typing import Any, Iterable, Awaitable, Callable, Optional, Self

__all__ = [
    "BaseCallback",
    "callback_data",
    "execute_callbacks",
    "Callback"
]

CallbackData = list[tuple[float, dict[str, str | bool | float | None]]]
TimeDuration = float | dt.timedelta

def callback_data(
        data: CallbackData,
        name: str,
        exchange: str,
        symbol: str,
        interval: str = None
) -> dict[str, str | CallbackData]:
    """
    Wraps the data for the callback.

    :param data: The data to wrap.
    :param name: The name of the data.
    :param exchange: The source exchange of the data.
    :param symbol: The symbol of the data.
    :param interval: The interval of the data.

    :return: The wrapped data.
    """

    return {
        BaseCallback.NAME: name,
        BaseCallback.DATA: data,
        BaseCallback.EXCHANGE: exchange,
        BaseCallback.SYMBOL: symbol,
        BaseCallback.INTERVAL: interval
    }

class BaseCallback:
    """A class to represent a callback."""

    DATA_KEY = None
    CONNECTABLE = False
    ADJUSTABLE = True

    NAME = "name"
    DATA = 'data'
    EXCHANGE = 'exchange'
    SYMBOL = 'symbol'
    INTERVAL = 'interval'

    DELAY = 0.001

    def __init__(self, key: Any = None, delay: TimeDuration = None) -> None:
        """
        Defines the class attributes.

        :param key: The key od the data.
        :param delay: The delay in handling.
        """

        if key is None:
            key = self.DATA_KEY

        if delay is None:
            delay = self.DELAY

        self.key = key
        self.delay = delay

        self.awaiting: list[dict[str, Any]] = []
        self.exceptions: list[tuple[Exception, Any]] = []

        self._handling_processes: list[threading.Thread] = []

        self._connected = False
        self._handling = False
        self._running = True

    @property
    def handling(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._handling

    @property
    def running(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return (
            self._running and
            ((self.connected and self.connectable) or (not self.connectable))
        )

    @property
    def connected(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self._connected

    @property
    def connectable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.CONNECTABLE

    @property
    def adjustable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.ADJUSTABLE

    async def start(self) -> None:
        """Connects to the socket service."""

    async def connect(self) -> None:
        """Connects to the socket service."""

        if self.connected:
            warnings.warn(f"{repr(self)} callback is already connected.")

            return

        try:
            await self.start()

            self._connected = True
            self._running = True

        except Exception as e:
            if self.adjustable:
                warnings.warn(f"{type(e)}: {str(e)}")

            else:
                raise e

    async def prepare(self) -> None:
        """Connects to the socket service."""

        if self.connectable and (not self.connected):
            await self.connect()

    def handling_loop(self) -> None:
        """Handles the requests."""

        self._handling = True

        while self.handling:
            try:
                self.awaiting.append(self.awaiting.pop(0))

            except IndexError:
                delay = self.delay

                if isinstance(delay, dt.timedelta):
                    delay = delay.total_seconds()

                time.sleep(delay)

    def start_handling(self) -> None:
        """Starts the screening process."""

        handling_process = threading.Thread(
            target=lambda: self.handling_loop()
        )

        self._handling_processes.append(handling_process)

        handling_process.start()

    def stop_handling(self) -> None:
        """Stops the handling process."""

        if self.handling:
            self._handling = False

            self._handling_processes.clear()

    def enable(self) -> None:
        """Stops the handling process."""

        self._running = True

    def disable(self) -> None:
        """Stops the handling process."""

        self._running = False

    def stop_running(self) -> None:
        """Stops the screening process."""

        self.disable()

    def stop(self) -> None:
        """Stops the screening process."""

        self.stop_handling()
        self.stop_running()

    async def handle(self, data: Any, timestamp: float, key: Any = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

    async def exception(self, exception: Exception, data: Any) -> bool:
        """
        Records and handles the exception.

        :param data: The data from the exchange.
        :param exception: The exception object.

        :return: The validation value.
        """

        self.exceptions.append((exception, data))

        if self.adjustable:
            warnings.warn(f"{type(exception)}: {str(exception)}")

            return False

        else:
            raise exception

    async def _handle(self, **kwargs: Any) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param kwargs: Any keyword arguments.

        :return: The validation value.
        """

        try:
            return await self.handle(**kwargs)

        except Exception as e:
            return await self.exception(exception=e, data=kwargs)

    async def record(self, data: Any, timestamp: float, key: Any = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        await self.prepare()

        if (self.connectable and (not self.connected)) or (not self.running):
            return False

        return await self._handle(data=data, timestamp=timestamp, key=key)

    def run(self, handlers: int = None) -> None:
        """
        Runs the process of the price screening.

        :param handlers: The amount of handlers to create.
        """

        if handlers is None:
            handlers = 1

        if handlers:
            self._handling = True

        for _ in range(handlers):
            self.start_handling()

async def execute_callbacks(
        callbacks: Iterable[BaseCallback],
        key: str,
        timestamp: float,
        data: CallbackData,
        exchange: str,
        symbol: str,
        interval: str = None
) -> None:
    """
    Wraps the data for the callback.

    :param callbacks: The callbacks to execute.
    :param key: The call type key.
    :param timestamp: The timestamp of the source data.
    :param data: The data to wrap.
    :param exchange: The source exchange of the data.
    :param symbol: The symbol of the data.
    :param interval: The interval of the data.

    :return: The wrapped data.
    """

    payload = callback_data(
        data=data, exchange=exchange, name=key,
        symbol=symbol, interval=interval
    )

    await asyncio.gather(
        *(
            callback.record(payload, timestamp, key=key)
            for callback in callbacks or []
        )
    )

class Callback(BaseCallback):

    def __init__(
            self,
            handler: Callable[[Any, float, Optional[Any]], Any | Awaitable[Any]],
            starter: Callable[[Self], Any] = None,
            key: Any = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param key: The key od the data.
        :param delay: The delay in handling.
        """

        super().__init__(key=key, delay=delay)

        self.handler = handler
        self.starter = starter

    async def start(self) -> None:
        """Connects to the socket service."""

        if self.starter:
            if asyncio.iscoroutinefunction(self.handler):
                await self.starter(self)

            else:
                self.starter(self)

    async def handle(self, data: Any, timestamp: float, key: Any = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        if asyncio.iscoroutinefunction(self.handler):
            await self.handler(data, timestamp, key)

        else:
            self.handler(data, timestamp, key)

        return True
