# recorder.py

import warnings
import threading
import time
from abc import ABCMeta, abstractmethod
import datetime as dt
from typing import Iterable, Any
from functools import partial
import asyncio

from represent import Modifiers, represent

from cryptofeed import FeedHandler
from cryptofeed.feed import Feed

from market_break.dataset import new_dataset_index

from crypto_screening.utils.process import find_string_value
from crypto_screening.exchanges import EXCHANGES, EXCHANGE_NAMES
from crypto_screening.symbols import adjust_symbol
from crypto_screening.screeners.base import (
    BaseMarketScreener, BaseScreener
)
from crypto_screening.screeners.market import ScreenersMarket
from crypto_screening.screeners.callbacks.base import (
    BaseCallback, execute_callbacks
)

__all__ = [
    "MarketHandler",
    "ExchangeFeed",
    "FEED_GROUP_SIZE",
    "add_feeds",
    "MarketScreener",
    "MarketRecorder",
    "insert_screeners_data",
    "record",
    "limit_screener_dataset"
]

class MarketHandler(FeedHandler):
    """A class to handle the market data feed."""

    def __init__(self) -> None:
        """Defines the class attributes."""

        super().__init__(
            config={'uvloop': False, 'log': {'disabled': True}}
        )

class ExchangeFeed(Feed):
    """A class to represent an exchange feed object."""

    handler: MarketHandler = None

    running: bool = False

    def stop(self) -> None:
        """Stops the process."""

        self.running = False

        Feed.stop(self)

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        Create tasks for exchange interfaces and backends.

        :param loop: The event loop for the process.
        """

        self.running = True

        Feed.start(self, loop=loop)

FEED_GROUP_SIZE = 20

def add_feeds(
        handler: MarketHandler,
        data: dict[str, Iterable[str]],
        fixed: bool = False,
        amount: int = FEED_GROUP_SIZE,
        parameters: dict[str, dict[str, Any]] | dict[str, Any] = None
) -> None:
    """
    Adds the symbols to the handler for each exchange.

    :param handler: The handler object.
    :param data: The data of the exchanges and symbols to add.
    :param parameters: The parameters for the exchanges.
    :param fixed: The value for fixed parameters to all exchanges.
    :param amount: The maximum amount of symbols for each feed.
    """

    base_parameters = None

    if not fixed:
        parameters = parameters or {}

    else:
        base_parameters = parameters or {}
        parameters = {}

    for exchange, symbols in data.items():
        saved_exchange = exchange

        exchange = find_string_value(value=exchange, values=EXCHANGE_NAMES)

        symbols = [adjust_symbol(symbol, separator='-') for symbol in symbols]

        if fixed:
            parameters.setdefault(saved_exchange, base_parameters)

        EXCHANGES[exchange]: type[ExchangeFeed]

        groups = []

        for i in range(0, int(len(symbols) / amount) + len(symbols) % amount, amount):
            groups.append(symbols[i:])

        for symbols_packet in groups:
            exchange_parameters = (
                parameters[saved_exchange]
                if (
                    (saved_exchange in parameters) and
                    isinstance(parameters[saved_exchange], dict) and
                    all(isinstance(key, str) for key in parameters)
                ) else {}
            )

            feed = EXCHANGES[exchange](
                symbols=symbols_packet, **exchange_parameters
            )

            feed.start = partial(ExchangeFeed.start, feed)
            feed.stop = partial(ExchangeFeed.stop, feed)
            feed.handler = handler
            feed.running = False

            handler.add_feed(feed)

@represent
class MarketRecorder(ScreenersMarket, metaclass=ABCMeta):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.screeners.recorder import MarketRecorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = MarketRecorder(data=market)
    """

    INSERT = True

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            callbacks: Iterable[BaseCallback] = None,
            insert: bool = None
    ) -> None:
        """
        Defines the class attributes.

        :param screeners: The screeners to record.
        :param callbacks: The callbacks for the service.
        :param insert: The value to insert data into the market datasets.
        """

        super().__init__(screeners=screeners)

        if insert is None:
            insert = self.INSERT

        self.callbacks = callbacks or []

        self.insert = insert

        self._disabled = False

    @property
    def disabled(self) -> bool:
        """Returns the value for the recorder to run."""

        return self._disabled

    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

    def disable(self) -> None:
        """Stops the recorder."""

        self._disabled = True

    def enable(self) -> None:
        """Starts the recorder."""

        self._disabled = False

    def disable_insert(self) -> None:
        """Disables saving data to screeners."""

        self.insert = False

    def enable_insert(self) -> None:
        """Enables saving data to screeners."""

        self.insert = True

    async def process(self, data: Any, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

    async def record(self, data: Any, timestamp: float):
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        if not self.disabled:
            await self.process(data=data, timestamp=timestamp)

class MarketScreener(BaseMarketScreener, ScreenersMarket):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - handler:
        The handler object to handle the data feed.

    - recorder:
        The recorder object to record the data of the market from the feed.

    - screeners:
        The screener object to control and fill with data.

    - refresh:
        The duration of time between each refresh. 0 means no refresh.

    - amount:
        The amount of symbols for each symbols group for an exchange.

    - limited:
        The value to limit the running screeners to active exchanges.
    """

    __modifiers__ = Modifiers()
    __modifiers__.excluded.append('handler')

    screeners: list[BaseScreener]
    recorder: MarketRecorder

    DELAY = 1
    AMOUNT = FEED_GROUP_SIZE

    INSERT = MarketRecorder.INSERT

    REFRESH = dt.timedelta(minutes=10)

    def __init__(
            self,
            recorder: MarketRecorder,
            screeners: Iterable[BaseScreener] = None,
            location: str = None,
            cancel: float | dt.timedelta = None,
            delay: float | dt.timedelta = None,
            refresh: float | dt.timedelta | bool = None,
            limited: bool = None,
            handler: MarketHandler = None,
            amount: int = None,
            insert: bool = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        :param insert: The value to insert data into the market datasets.
        """

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, screeners=screeners
        )

        if refresh is True:
            refresh = self.REFRESH

        if insert is None:
            insert = self.INSERT

        self._insert = insert

        self.recorder = recorder
        self.handler = handler or MarketHandler()
        self.limited = limited or False
        self.amount = amount or self.AMOUNT
        self.refresh = refresh

        self.loop: asyncio.AbstractEventLoop | None = None

        self._feeds_parameters: dict[str, Any] | None = None
        self._run_parameters: dict[str, Any] | None = None

    @property
    def insert(self) -> bool:
        """
        Returns the value to insert data into the datasets of the screeners.

        :return: The boolean flag.
        """

        return self._insert

    @insert.setter
    def insert(self, value: bool) -> None:
        """
        Returns the value to insert data into the datasets of the screeners.

        :param value: The boolean flag.
        """

        self.recorder.insert = value

        self._insert = value

    def update_screeners(self) -> None:
        """Updates the records of the object."""

        super().update_screeners()

        self.recorder.update_screeners()

    def add_feeds(
            self,
            data: dict[str, Iterable[str]] = None,
            fixed: bool = True,
            amount: int = None,
            parameters: dict[str, dict[str, Any]] | dict[str, Any] = None
    ) -> None:
        """
        Adds the symbols to the handler for each exchange.

        :param data: The data of the exchanges and symbols to add.
        :param parameters: The parameters for the exchanges.
        :param fixed: The value for fixed parameters to all exchanges.
        :param amount: The maximum amount of symbols for each feed.
        """

        if data is None:
            data = self.structure()

        self._feeds_parameters = dict(
            data=data, fixed=fixed, parameters=parameters, amount=amount
        )

        feed_params = self.recorder.parameters()
        feed_params.update(parameters or {})

        add_feeds(
            self.handler, data=data, fixed=fixed,
            parameters=feed_params, amount=amount or self.amount
        )

    def refresh_feeds(self) -> None:
        """Refreshes the feed objects."""

        if self._feeds_parameters is None:
            warnings.warn(
                "Cannot refresh feeds as there was "
                "no feeds initialization to repeat."
            )

            return

        self.handler.feeds.clear()

        self.add_feeds(**self._feeds_parameters)

    def rerun(self) -> None:
        """Refreshes the process."""

        if self._run_parameters is None:
            warnings.warn(
                "Cannot rerun as there was "
                "no initial process to repeat."
            )

            return

        self.stop()
        self.refresh_feeds()
        self.run(**self._run_parameters)

    def screening_loop(
            self,
            start: bool = True,
            loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if loop is None:
            loop = asyncio.new_event_loop()

        self.loop = loop

        asyncio.set_event_loop(loop)

        self._screening = True

        for screener in self.screeners:
            screener._screening = True

        if self._feeds_parameters is None:
            self.add_feeds()

        try:
            self.handler.run(
                start_loop=start and (not loop.is_running()),
                install_signal_handlers=False
            )

        except AttributeError:
            pass

    def update_loop(self) -> None:
        """Updates the state of the screeners."""

        self._updating = True

        refresh = self.refresh

        if isinstance(refresh, dt.timedelta):
            refresh = refresh.total_seconds()

        start = time.time()

        while self.updating:
            s = time.time()

            if self.screening:
                self.update()

                current = time.time()

                if refresh and ((current - start) >= refresh):
                    self.rerun()

                    start = current

            time.sleep(max([self.delay - (time.time() - s), 0]))

    def update(self) -> None:
        """Updates the state of the screeners."""

        for screener in self.screeners:
            for feed in self.handler.feeds:
                feed: ExchangeFeed

                if (
                    self.limited and
                    (screener.exchange.lower() == feed.id.lower()) and
                    (not feed.running)
                ):
                    screener.stop()

    def stop_screening(self) -> None:
        """Stops the screening process."""

        if not isinstance(self.loop, asyncio.AbstractEventLoop):
            return

        super().stop_screening()

        self.loop: asyncio.AbstractEventLoop

        for task in asyncio.all_tasks(self.loop):
            task.cancel()

        self.loop.stop()

        while self.loop.is_running():
            time.sleep(0.001)

        try:
            self.loop.close()

        except (AttributeError, RuntimeError):
            pass

        self.loop = None

        self.handler.running = False

    def start_screening(
            self,
            start: bool = True,
            loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """
        Starts the screening process.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if self.screening:
            warnings.warn(f"Timeout screening of {self} is already running.")

            return

        self._screening_process = threading.Thread(
            target=lambda: self.screening_loop(loop=loop, start=start)
        )

        self._screening_process.start()

    def run(
            self,
            save: bool = True,
            block: bool = False,
            update: bool = True,
            screen: bool = True,
            loop: asyncio.AbstractEventLoop = None,
            wait: bool | float | dt.timedelta | dt.datetime = False,
            timeout: float | dt.timedelta | dt.datetime = None
    ) -> None:
        """
        Runs the program.

        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        :param update: The value to update the screeners.
        :param screen: The value to start the loop.
        :param loop: The event loop.

        :return: The start_timeout process.
        """

        self._run_parameters = dict(
            save=save, block=block, update=update, screen=screen,
            loop=loop, wait=wait, timeout=timeout,
        )

        super().run(
            screen=False, block=False, wait=wait,
            timeout=timeout, update=update, save=save
        )

        if not block:
            self.start_screening(loop=loop, start=screen)

        else:
            self.screening_loop(loop=loop, start=screen)

def limit_screener_dataset(screener: BaseScreener, memory: int = None) -> None:
    """
    Limits the memory of the dataset in the screener.

    :param screener: The screener to limit its dataset.
    :param memory: The size of the dataset.
    """

    memory = memory or screener.memory

    if (memory is not None) and (len(screener.market) > memory):
        screener.market.drop(
            index=list(screener.market.index[:len(screener.market) - memory]),
            inplace=True
        )

def insert_screeners_data(
        data: dict[str, str | float | int | bool],
        index: dt.datetime,
        screeners: Iterable[BaseScreener],
        limit: bool = True
) -> bool:
    """
    Inserts the data into the datasets of the screeners, for the given index.

    :param data: The data to insert in a new row by the index.
    :param index: The index for the new data row.
    :param screeners: The screeners to update with the new data.
    :param limit: The value to limit the market memory.

    :return: The value of inserting data into at least one screener.
    """

    valid = False

    for screener in screeners:
        if new_dataset_index(index=index, dataset=screener.market):
            valid = True

            screener.market.loc[index] = data

            if limit and screener.memory:
                limit_screener_dataset(screener)

    return valid

async def record(
        screeners: Iterable[BaseScreener],
        callbacks: Iterable[BaseCallback],
        key: str,
        timestamp: float,
        data: dict[str, str | float | int | bool],
        exchange: str,
        symbol: str,
        insert: bool = True,
        interval: str = None
) -> bool:
    """
    Wraps the data for the callback.

    :param screeners: The market structure.
    :param callbacks: The callbacks to execute.
    :param key: The call type key.
    :param timestamp: The timestamp of the source data.
    :param data: The data to wrap.
    :param exchange: The source exchange of the data.
    :param symbol: The symbol of the data.
    :param insert: The value to insert data into the datasets.
    :param interval: The interval of the data.
    """

    valid = (
        (not insert) or insert_screeners_data(
            data=data, index=dt.datetime.fromtimestamp(timestamp),
            screeners=screeners
        )
    )

    if valid:
        await execute_callbacks(
            callbacks=callbacks, key=key, interval=interval,
            timestamp=timestamp, data=[(timestamp, data)],
            exchange=exchange, symbol=symbol
        )

    return valid
