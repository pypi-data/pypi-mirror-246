# trades.py

import datetime as dt
from typing import Iterable, Callable

import pandas as pd

from cryptofeed.types import Trade
from cryptofeed.defines import TRADES

from crypto_screening.symbols import adjust_symbol
from crypto_screening.dataset import create_dataset, AMOUNT, PRICE, SIDE
from crypto_screening.screeners.callbacks import BaseCallback
from crypto_screening.screeners.screener import TradesScreener
from crypto_screening.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler, record
)

__all__ = [
    "TradesMarketScreener",
    "TradesMarketRecorder",
    "TradesScreener",
    "trades_market_screener",
    "create_trades_market_dataset",
    "record_trades",
    "create_trades_screeners"
]

TimeDuration = float | dt.timedelta

def create_trades_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(columns=TradesMarketRecorder.COLUMNS)

async def record_trades(
        screeners: Iterable[TradesScreener],
        data: Trade,
        timestamp: float,
        insert: bool = True,
        callbacks: Iterable[BaseCallback] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param screeners: The screeners.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param insert: The value to insert data into the datasets.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    new_data = {
        AMOUNT: float(data.amount),
        PRICE: float(data.price),
        SIDE: data.side
    }

    exchange = data.exchange.lower()
    symbol = adjust_symbol(symbol=data.symbol)

    return await record(
        screeners=screeners, data=new_data,
        insert=insert, callbacks=callbacks, key=TradesScreener.NAME,
        timestamp=timestamp, exchange=exchange, symbol=symbol
    )

RecorderParameters = dict[str, Iterable[str] | dict[str, Callable]]

class TradesMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.screeners.trades import TradesMarketRecorder
    >>>
    >>> recorder = TradesMarketRecorder(...)
    """

    COLUMNS = TradesScreener.COLUMNS

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[TRADES],
            callbacks={TRADES: self.record},
            max_depth=1
        )

    async def process(self, data: Trade, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.

        :return: The validation value.
        """

        exchange = data.exchange.lower()
        symbol = adjust_symbol(symbol=data.symbol)

        screeners = self.find_trades_screeners(exchange=exchange, symbol=symbol)

        return await record_trades(
            screeners=screeners, data=data, timestamp=timestamp,
            callbacks=self.callbacks, insert=self.insert
        )

class TradesMarketScreener(MarketScreener):
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

    >>> from crypto_screening.screeners.trades import trades_market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = trades_market_screener(data=structure)
    >>> screener.run()
    """

    screeners: list[TradesScreener]
    recorder: TradesMarketRecorder

    COLUMNS = TradesMarketRecorder.COLUMNS

    def __init__(
            self,
            recorder: TradesMarketRecorder,
            screeners: Iterable[TradesScreener] = None,
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

def create_trades_screeners(
        data: dict[str, Iterable[str]],
        location: str = None,
        memory: int = None,
        cancel: TimeDuration = None,
        delay: TimeDuration = None
) -> list[TradesScreener]:
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
                TradesScreener(
                    symbol=symbol, exchange=exchange, delay=delay,
                    location=location, cancel=cancel, memory=memory
                )
            )

    return screeners

def trades_market_screener(
        data: dict[str, Iterable[str]],
        cancel: TimeDuration = None,
        delay: TimeDuration = None,
        refresh: TimeDuration | bool = None,
        location: str = None,
        limited: bool = None,
        amount: int = None,
        memory: int = None,
        insert: bool = None,
        handler: MarketHandler = None,
        recorder: TradesMarketRecorder = None,
        callbacks: Iterable[BaseCallback] = None
) -> TradesMarketScreener:
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

    screeners = create_trades_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay, memory=memory
    )

    return TradesMarketScreener(
        recorder=recorder or TradesMarketRecorder(
            screeners=screeners, callbacks=callbacks, insert=insert
        ), screeners=screeners, insert=insert,
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )
