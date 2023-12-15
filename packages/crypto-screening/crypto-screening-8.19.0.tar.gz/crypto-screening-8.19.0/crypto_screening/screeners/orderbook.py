# orderbook.py

import datetime as dt
from typing import Iterable, Callable

import pandas as pd

from cryptofeed.types import OrderBook
from cryptofeed.defines import L2_BOOK

from market_break.dataset import (
    BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME, create_dataset
)

from crypto_screening.symbols import adjust_symbol
from crypto_screening.screeners.screener import OrderbookScreener
from crypto_screening.screeners.callbacks import BaseCallback
from crypto_screening.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler, record
)

__all__ = [
    "OrderbookMarketScreener",
    "OrderbookMarketRecorder",
    "OrderbookScreener",
    "orderbook_market_screener",
    "create_orderbook_market_dataset",
    "record_orderbook",
    "create_orderbook_screeners"
]

TimeDuration = float | dt.timedelta

def create_orderbook_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(columns=OrderbookMarketRecorder.COLUMNS)

async def record_orderbook(
        screeners: Iterable[OrderbookScreener],
        data: OrderBook,
        timestamp: float,
        insert: bool = True,
        callbacks: Iterable[BaseCallback] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param screeners: The market structure.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param insert: The value to insert data into the datasets.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    try:
        bids = data.book.bids.to_list()
        asks = data.book.asks.to_list()

        new_data = {
            BIDS: float(bids[0][0]),
            ASKS: float(asks[0][0]),
            BIDS_VOLUME: float(bids[0][1]),
            ASKS_VOLUME: float(asks[0][1])
        }

    except IndexError:
        return False

    exchange = data.exchange.lower()
    symbol = adjust_symbol(symbol=data.symbol)

    return await record(
        screeners=screeners, data=new_data,
        insert=insert, callbacks=callbacks, key=OrderbookScreener.NAME,
        timestamp=timestamp, exchange=exchange, symbol=symbol
    )

RecorderParameters = dict[str, Iterable[str] | dict[str, Callable]]

class OrderbookMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.screeners.orderbook import OrderbookMarketRecorder
    >>>
    >>> recorder = OrderbookMarketRecorder(...)
    """

    COLUMNS = OrderbookScreener.COLUMNS

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

        screeners = self.find_orderbook_screeners(exchange=exchange, symbol=symbol)

        return await record_orderbook(
            screeners=screeners, data=data, timestamp=timestamp,
            callbacks=self.callbacks, insert=self.insert
        )

class OrderbookMarketScreener(MarketScreener):
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

    >>> from crypto_screening.screeners.orderbook import orderbook_market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = orderbook_market_screener(data=structure)
    >>> screener.run()
    """

    screeners: list[OrderbookScreener]
    recorder: OrderbookMarketRecorder

    COLUMNS = OrderbookMarketRecorder.COLUMNS

    def __init__(
            self,
            recorder: OrderbookMarketRecorder,
            screeners: Iterable[OrderbookScreener] = None,
            location: str = None,
            cancel: TimeDuration = None,
            delay: TimeDuration = None,
            refresh: TimeDuration | bool = None,
            handler: MarketHandler = None,
            limited: bool = None,
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

def create_orderbook_screeners(
        data: dict[str, Iterable[str]],
        location: str = None,
        memory: int = None,
        cancel: MarketHandler = None,
        delay: MarketHandler = None
) -> list[OrderbookScreener]:
    """
    Defines the class attributes.

    :param data: The data for the screeners.
    :param location: The saving location for the data.
    :param cancel: The time to cancel the waiting.
    :param delay: The delay for the process.
    :param memory: The memory limitation of the market dataset.
    """

    screeners = []

    for exchange, symbols in data.items():
        for symbol in symbols:
            screeners.append(
                OrderbookScreener(
                    symbol=symbol, exchange=exchange, delay=delay,
                    location=location, cancel=cancel, memory=memory
                )
            )

    return screeners

def orderbook_market_screener(
        data: dict[str, Iterable[str]],
        cancel: MarketHandler = None,
        delay: MarketHandler = None,
        refresh: MarketHandler | bool = None,
        location: str = None,
        limited: bool = None,
        amount: int = None,
        memory: int = None,
        insert: bool = None,
        handler: MarketHandler = None,
        recorder: OrderbookMarketRecorder = None,
        callbacks: Iterable[BaseCallback] = None
) -> OrderbookMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
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

    :return: The market screener object.
    """

    screeners = create_orderbook_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay, memory=memory
    )

    return OrderbookMarketScreener(
        recorder=recorder or OrderbookMarketRecorder(
            screeners=screeners, callbacks=callbacks, insert=insert
        ), screeners=screeners, insert=insert,
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )
