# dataset.py

import pandas as pd

from market_break.dataset import (
    create_dataset, OHLC_COLUMNS, OPEN, LOW, HIGH, create_dataset,
    ORDERBOOK_COLUMNS, bid_ask_to_ohlcv, VOLUME, CLOSE,
    OHLCV_COLUMNS, BIDS_VOLUME, ASKS_VOLUME, BIDS, ASKS,
)

__all__ = [
    "TRADES_COLUMNS",
    "PRICE",
    "SIDE",
    "BUY",
    "SELL",
    "TICKERS_COLUMNS",
    "ORDERBOOK_COLUMNS",
    "AMOUNT",
    "bid_ask_to_tickers",
    "trades_to_tickers",
    "trades_to_bid_ask",
    "bid_ask_to_ohlcv",
    "OHLC_COLUMNS",
    "OHLCV_COLUMNS",
    "OPEN",
    "HIGH",
    "LOW",
    "CLOSE",
    "VOLUME",
    "BIDS_VOLUME",
    "ASKS_VOLUME",
    "BIDS",
    "ASKS",
    "create_dataset"
]

AMOUNT = "Amount"
PRICE = "Price"
SIDE = "Side"
BUY = 'buy'
SELL = 'sell'

TRADES_COLUMNS = (AMOUNT, PRICE, SIDE)
TICKERS_COLUMNS = (BIDS, ASKS)

def bid_ask_to_tickers(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the BID/ASK spread dataset into a tickers' dataset.

    :param dataset: The source data.

    :return: The returned dataset.
    """

    if not all(column in TICKERS_COLUMNS for column in dataset.columns):
        raise ValueError(
            f"Dataset has to contain all columns: "
            f"{', '.join(TICKERS_COLUMNS)}, "
            f"but found only: {', '.join(dataset.columns)}"
        )

    return dataset.copy()[list(TICKERS_COLUMNS)]

def trades_to_bid_ask(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the trades spread dataset into a BID/ASK dataset.

    :param dataset: The source data.

    :return: The returned dataset.
    """

    if not all(column in TRADES_COLUMNS for column in dataset.columns):
        raise ValueError(
            f"Dataset has to contain all columns: "
            f"{', '.join(TRADES_COLUMNS)}, "
            f"but found only: {', '.join(dataset.columns)}"
        )

    bid = None
    ask = None
    bid_volume = None
    ask_volume = None

    results = create_dataset(ORDERBOOK_COLUMNS)

    for index, data in dataset.iterrows():
        if data[SIDE] == BUY:
            ask = data[PRICE]
            ask_volume = data[AMOUNT]

        elif data[SIDE] == SELL:
            bid = data[PRICE]
            bid_volume = data[AMOUNT]

        else:
            continue

        if None in (bid, ask, bid_volume, ask_volume):
            continue

        results[index] = {
            BIDS: bid, ASKS: ask,
            BIDS_VOLUME: bid_volume, ASKS_VOLUME: ask_volume
        }

    return results

def trades_to_tickers(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the trades spread dataset into a tickers' dataset.

    :param dataset: The source data.

    :return: The returned dataset.
    """

    return bid_ask_to_tickers(trades_to_bid_ask(dataset))
