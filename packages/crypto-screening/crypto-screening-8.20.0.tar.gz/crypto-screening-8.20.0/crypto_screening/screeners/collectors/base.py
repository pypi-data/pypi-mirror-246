# base.py

import warnings
import threading
import datetime as dt
import time
from typing import Iterable, Any

from market_break.dataset import index_to_datetime

from crypto_screening.screeners.container import ScreenersContainer
from crypto_screening.screeners.base import BaseScreener, BaseMarketScreener
from crypto_screening.screeners.recorder import insert_screeners_data
from crypto_screening.screeners.combined import CATEGORIES_MAP, OHLCVCategory

__all__ = [
    "ScreenersDataCollector"
]

Data = list[tuple[str | float | dt.datetime, dict[str, str | float | bool | None]]]
TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

class ScreenersDataCollector(BaseMarketScreener, ScreenersContainer):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - screeners:
        The screener object to control and fill with data.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - screeners:
        The screener object to control and fill with data.
    """

    ADJUSTABLE = True

    def __init__(
            self,
            screeners: Iterable[BaseScreener] = None,
            location: str = None,
            cancel: TimeDuration = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, screeners=screeners
        )

        self._handling_processes: list[threading.Thread] = []
        self._awaiting: list[dict[str, Any]] = []

        self.exceptions: list[tuple[Exception, Any]] = []

        self._handling = False

    @property
    def handling(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._handling

    @property
    def adjustable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.ADJUSTABLE

    def exception(self, exception: Exception, data: Any) -> bool:
        """
        Records and handles the exception.

        :param data: The data from the exchange.
        :param exception: The exception object.

        :return: The validation value.
        """

        self.exceptions.append((exception, data))

        if self.adjustable:
            warnings.warn(f"{type(exception)}: {str(exception)}.\ndata: {data}")

            return False

        else:
            raise exception

    def collect(self, data: dict[str, Any], create: bool = False) -> None:
        """
        Collects the data for the handler.

        :param data: The data to collect.
        :param create: The value to create new screeners and add them to the collection.
        """

        if self.handling:
            self._awaiting.append(data)

        else:
            self.handle(**data, create=create)

    def handle(
            self,
            name: str,
            exchange: str,
            symbol: str,
            interval: str,
            data: Data,
            create: bool = False
    ) -> None:
        """
        Handles the data received from the connection.

        :param data: The data to handle.
        :param name: The name of the data.
        :param exchange: The exchange of the screener.
        :param symbol: The symbol of the screener.
        :param interval: The interval of the screener.
        :param create: The value to create new screeners and add them to the collection.
        """

        screeners = []

        for base in BaseScreener.SCREENER_NAME_TYPE_MATCHES[name]:
            found_screeners = self.find_screeners(
                base=base, exchange=exchange,
                symbol=symbol, interval=interval
            )

            if create and not found_screeners and name in CATEGORIES_MAP:
                new_screener = CATEGORIES_MAP[name].screener(
                    exchange=exchange, symbol=symbol,
                    **(
                        dict(interval=interval)
                        if CATEGORIES_MAP[name] is OHLCVCategory else
                        dict()
                    )
                )

                found_screeners.append(new_screener)

                self.add([new_screener])

            screeners.extend(found_screeners)

        for index, row in data:
            insert_screeners_data(
                data=row, index=index_to_datetime(index),
                screeners=screeners
            )

    def handling_loop(self) -> None:
        """Handles the requests."""

        self._handling = True

        while self.handling:
            try:
                data = self._awaiting.pop(0)

            except IndexError:
                time.sleep(0.001)

                continue

            self.handle(**data)

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

    def stop(self) -> None:
        """Stops the screening process."""

        super().stop()

        self.stop_handling()

    def run(
            self,
            handlers: int = None,
            screen: bool = True,
            save: bool = True,
            block: bool = False,
            update: bool = True,
            wait: TimeDestination = False,
            timeout: TimeDestination = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param handlers: The amount of handlers to create.
        :param screen: The value to start the screening.
        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param update: The value to update the screeners.
        :param timeout: The valur to add a start_timeout to the process.
        """

        if handlers is None:
            handlers = 0

        if handlers:
            self._handling = True

        for _ in range(handlers):
            self.start_handling()

        super().run(
            screen=screen, save=save, block=block,
            update=update, wait=wait, timeout=timeout
        )
