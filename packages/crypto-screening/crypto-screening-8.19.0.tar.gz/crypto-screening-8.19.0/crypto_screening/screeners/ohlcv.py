# ohlcv.py

import datetime as dt
from typing import Iterable, Callable, Any

import pandas as pd

from cryptofeed.types import OrderBook
from cryptofeed.defines import L2_BOOK

from market_break.interval import interval_total_time
from market_break.dataset import bid_ask_to_ohlcv, create_dataset

from crypto_screening.symbols import adjust_symbol
from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.screeners.screener import OHLCVScreener
from crypto_screening.screeners.callbacks.base import (
    BaseCallback, execute_callbacks
)
from crypto_screening.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler,
    limit_screener_dataset, insert_screeners_data
)
from crypto_screening.screeners.orderbook import (
    OrderbookScreener, record_orderbook, create_orderbook_screeners
)

__all__ = [
    "OHLCVMarketScreener",
    "OHLCVMarketRecorder",
    "OHLCVScreener",
    "ohlcv_market_screener",
    "create_ohlcv_market_dataset",
    "create_ohlcv_screeners",
    "merge_screeners"
]

Indexes = dict[str, dict[str, dict[str, int]]]
TimeDuration = float | dt.timedelta

def create_ohlcv_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(columns=OHLCVMarketRecorder.COLUMNS)

async def record_ohlcv(
        screeners: Iterable[OHLCVScreener],
        indexes: Indexes,
        data: OrderBook,
        timestamp: float,
        orderbook_screeners: Iterable[OrderbookScreener] = None,
        insert: bool = True,
        callbacks: Iterable[BaseCallback] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param screeners: The OHLCV screeners.
    :param orderbook_screeners: The orderbook screeners.
    :param indexes: The indexes of the OHLCV market.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param insert: The value to insert data into the datasets.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    if orderbook_screeners is None:
        orderbook_screeners: list[OrderbookScreener] = [
            screener for screener in screeners
            if isinstance(screener, OrderbookScreener)
        ]

    if not orderbook_screeners:
        return False

    if not await record_orderbook(
        screeners=orderbook_screeners, callbacks=callbacks,
        data=data, timestamp=timestamp
    ):
        return False

    exchange = data.exchange.lower()
    symbol = adjust_symbol(symbol=data.symbol)

    ohlcv_screeners: dict[str, list[OHLCVScreener]] = {}
    ohlcv_datasets: dict[str, pd.DataFrame] = {}

    for screener in screeners:
        (
            ohlcv_screeners.
            setdefault(screener.interval, []).
            append(screener)
        )

    if not ohlcv_screeners:
        return False

    spread = orderbook_screeners[0].market

    if len(spread) == 0:
        return False

    for interval, screeners in ohlcv_screeners.items():
        dataset_index = (
            indexes.
            setdefault(exchange, {}).
            setdefault(symbol, {}).
            setdefault(interval, 0)
        )

        if len(spread.index) <= dataset_index:
            continue

        span: dt.timedelta = spread.index[-1] - spread.index[dataset_index]

        if (dataset_index == 0) or (span >= interval_total_time(interval)):
            ohlcv_datasets[interval] = bid_ask_to_ohlcv(
                dataset=spread.iloc[dataset_index:], interval=interval
            )

    for interval, ohlcv in ohlcv_datasets.items():
        data: list[tuple[float, dict[str, Any]]] = []

        if insert:
            for screener in ohlcv_screeners[interval]:
                for index, row in ohlcv.iterrows():
                    index: dt.datetime

                    row_data = row.to_dict()

                    insert_screeners_data(
                        screeners=ohlcv_screeners[interval],
                        data=row_data, index=index, limit=False
                    )

                    data.append((index.timestamp(), row_data))

                limit_screener_dataset(screener)

        indexes[exchange][symbol][interval] = len(spread)

        await execute_callbacks(
            callbacks=callbacks, key=OHLCVScreener.NAME,
            timestamp=timestamp, data=data,
            exchange=exchange, symbol=symbol, interval=interval
        )

    return True

RecorderParameters = dict[str, Iterable[str] | dict[str, Callable]]

class OHLCVMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.screeners.ohlcv import OHLCVMarketRecorder
    >>>
    >>> recorder = OHLCVMarketRecorder(...)
    """

    COLUMNS = OHLCVScreener.COLUMNS

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            callbacks: Iterable[BaseCallback] = None,
            insert: bool = None
    ) -> None:
        """
        Defines the class attributes.

        :param screeners: The screener objects.
        :param callbacks: The callbacks for the service.
        :param insert: The value to insert data into the market datasets.
        """

        super().__init__(
            screeners=screeners, callbacks=callbacks, insert=insert
        )

        self._indexes: Indexes = {}

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[L2_BOOK],
            callbacks={L2_BOOK: self.record},
            max_depth=1
        )

    async def process(self, data: OrderBook, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        exchange = data.exchange.lower()
        symbol = adjust_symbol(symbol=data.symbol)

        orderbook_screeners = self.find_orderbook_screeners(exchange=exchange, symbol=symbol)
        ohlcv_screeners = self.find_ohlcv_screeners(exchange=exchange, symbol=symbol)

        return await record_ohlcv(
            screeners=ohlcv_screeners, orderbook_screeners=orderbook_screeners,
            data=data, timestamp=timestamp, indexes=self._indexes,
            callbacks=self.callbacks, insert=self.insert
        )

class OHLCVMarketScreener(MarketScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - screeners:
        The screeners to connect to the market screener.

    - intervals:
        The structure to set a specific interval to the dataset
        of each symbol in each exchange, matching the market data.

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

    >>> from crypto_screening.screeners.ohlcv import ohlcv_market_screener
    >>>
    >>> structure = {'1m': {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}}
    >>>
    >>> screener = ohlcv_market_screener(data=structure)
    >>> screener.run()
    """

    screeners: list[OrderbookScreener | OHLCVScreener]

    COLUMNS = OHLCVMarketRecorder.COLUMNS

    def __init__(
            self,
            recorder: OHLCVMarketRecorder,
            screeners: Iterable[OHLCVScreener | OrderbookScreener] = None,
            location: str = None,
            cancel: TimeDuration = None,
            delay: TimeDuration = None,
            refresh: TimeDuration | bool = None,
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
            location=location, cancel=cancel, amount=amount,
            delay=delay, recorder=recorder, insert=insert, refresh=refresh,
            screeners=screeners, handler=handler, limited=limited
        )

    def merge_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        merge_screeners(
            orderbook_screeners=self.orderbook_screeners,
            ohlcv_screeners=self.ohlcv_screeners
        )

def merge_screeners(
        orderbook_screeners: Iterable[OrderbookScreener],
        ohlcv_screeners: Iterable[OHLCVScreener]
) -> None:
    """
    Connects the screeners to the recording object.

    :param orderbook_screeners: The orderbook screeners.
    :param ohlcv_screeners: The OHLCV screeners.
    """

    for ohlcv_screener in ohlcv_screeners:
        for orderbook_screener in orderbook_screeners:
            if (
                (ohlcv_screener.exchange == orderbook_screener.exchange) and
                (ohlcv_screener.symbol == orderbook_screener.symbol)
            ):
                ohlcv_screener.orderbook_market = orderbook_screener.market

def create_ohlcv_screeners(
        data: dict[str, Iterable[str] | dict[str, Iterable[str]]],
        location: str = None,
        memory: int = None,
        cancel: TimeDuration = None,
        delay: TimeDuration = None,
        intervals: Iterable[str] = None
) -> list[OHLCVScreener]:
    """
    Defines the class attributes.

    :param data: The data for the screeners.
    :param location: The saving location for the data.
    :param cancel: The time to cancel the waiting.
    :param delay: The delay for the process.
    :param memory: The memory limitation of the market dataset.
    :param intervals: The intervals to create.
    """

    screeners = []

    for exchange, symbols in data.items():
        if intervals and (not isinstance(symbols, dict)):
            symbols = {symbol: intervals for symbol in symbols}

        if isinstance(symbols, dict):
            for symbol, intervals in symbols.items():
                for interval in intervals:
                    screeners.append(
                        OHLCVScreener(
                            symbol=symbol, exchange=exchange,
                            delay=delay, location=location,
                            cancel=cancel, interval=interval,
                            memory=memory
                        )
                    )

        else:
            for symbol in symbols:
                screeners.append(
                    OHLCVScreener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel, memory=memory
                    )
                )

    return screeners

def ohlcv_market_screener(
        data: dict[str, Iterable[str] | dict[str | Iterable[str]]],
        screeners: Iterable[OrderbookScreener] = None,
        intervals: Iterable[str] = None,
        cancel: TimeDuration = None,
        delay: TimeDuration = None,
        refresh: TimeDuration | bool = None,
        location: str = None,
        limited: bool = None,
        amount: int = None,
        memory: int = None,
        insert: bool = None,
        handler: MarketHandler = None,
        recorder: OHLCVMarketRecorder = None,
        callbacks: Iterable[BaseCallback] = None
) -> OHLCVMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param screeners: The base screeners.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param callbacks: The callbacks for the service.
    :param insert: The value to insert data into the market datasets.
    :param memory: The memory limitation of the market dataset.
    :param intervals: The intervals to create.

    :return: The market screener object.
    """

    orderbook_screeners = (screeners or []) or create_orderbook_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay, memory=memory
    )

    ohlcv_screeners = create_ohlcv_screeners(
        data=data, location=location, cancel=cancel,
        delay=delay, intervals=intervals
    )

    screeners = []
    screeners.extend(orderbook_screeners)
    screeners.extend(ohlcv_screeners)

    market = OHLCVMarketScreener(
        recorder=recorder or OHLCVMarketRecorder(
            screeners=screeners, callbacks=callbacks, insert=insert
        ), screeners=screeners, insert=insert,
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )
    market.merge_screeners()

    return market
