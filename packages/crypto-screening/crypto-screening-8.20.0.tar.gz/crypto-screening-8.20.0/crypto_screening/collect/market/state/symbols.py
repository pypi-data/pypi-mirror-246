# symbols.py

from abc import ABCMeta
import datetime as dt
from typing import Iterable, Any, TypeVar

from attrs import define

from represent import represent

import numpy as np
import pandas as pd

from market_break.dataset import create_dataset, index_to_datetime

from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.symbols import symbol_to_parts
from crypto_screening.collect.screeners import find_screeners
from crypto_screening.collect.market.state.base import (
    is_exchange_in_market_data, get_last_value, MarketState,
    dataset_to_data_rows, add_data_to_screeners, adjusted_dataset_length,
    minimum_common_dataset_length, screener_dataset, set_screener_dataset,
    add_data_to_symbols_screeners, data_from_dataset,
    adjusted_screener_dataset_length, sort_data
)

__all__ = [
    "symbols_market_values",
    "symbols_market_value",
    "validate_symbols_market_state_values_symbol",
    "is_exchange_in_market_data",
    "is_symbol_in_symbols_market_values",
    "symbol_to_assets_data",
    "symbols_to_assets_market_datasets",
    "symbols_screeners",
    "symbols_market_datasets_to_screeners",
    "add_symbols_market_data_to_screeners",
    "symbols_to_assets_market_data",
    "merge_symbols_market_data",
    "dataset_to_data_rows",
    "symbols_datasets_to_symbols_data",
    "screeners_to_symbols_data",
    "MarketState",
    "symbols_market_data",
    "symbols_market_state_data",
    "merge_symbols_market_states_data",
    "symbols_to_assets_screeners",
    "SymbolsMarketState",
    "add_data_to_symbols_screeners",
    "add_data_to_screeners",
    "adjusted_dataset_length",
    "sort_symbols_market_data",
    "set_screener_dataset",
    "screener_dataset",
    "get_last_value",
    "minimum_common_dataset_length",
    "symbols_market_datasets",
    "screeners_to_symbols_datasets"
]

_V = TypeVar("_V")

Data = list[tuple[dt.datetime, _V]]
SymbolData = Data
SymbolsData = dict[str, dict[str, SymbolData]]

def is_symbol_in_symbols_market_values(
        exchange: str,
        symbol: str,
        data: SymbolsData
) -> bool:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param data: The price data to process.

    :return: The validation value.
    """

    if not is_exchange_in_market_data(exchange=exchange, values=data):
        return False

    if symbol not in data[exchange]:
        return False

    return not np.isnan(data[exchange][symbol])

def validate_symbols_market_state_values_symbol(
        exchange: str,
        symbol: str,
        data: SymbolsData,
        provider: Any = None
) -> None:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param data: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    if exchange not in data:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the values of"
            f"{f' of {repr(provider)}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(data.keys())}"
        )

    if symbol not in data[exchange]:
        raise ValueError(
            f"symbol '{symbol}' is not found in '{exchange}' values of"
            f"{f' of {repr(provider)}' if provider is not None else ''}. "
            f"Found symbols for '{exchange}' values are: "
            f"{', '.join(data[exchange].keys())}"
        )

def symbols_market_values(
        exchange: str,
        symbol: str,
        data: SymbolsData,
        provider: Any = None
) -> list[tuple[dt.datetime, _V]]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param data: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_values_symbol(
        exchange=exchange, symbol=symbol,
        data=data, provider=provider
    )

    return data[exchange][symbol]

def symbols_market_value(
        exchange: str,
        symbol: str,
        data: SymbolsData,
        provider: Any = None
) -> tuple[dt.datetime, _V]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param data: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    values = symbols_market_values(
        symbol=symbol, data=data,
        exchange=exchange, provider=provider
    )

    return get_last_value(values)

SymbolsMarketData = dict[str, dict[str, list[tuple[dt.datetime, dict[str, _V]]]]]

def symbols_datasets_to_symbols_data(
        datasets: dict[str, dict[str, pd.DataFrame]]
) -> SymbolsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param datasets: The datasets to convert.

    :return: The new data.
    """

    return {
        exchange: {
            symbol: dataset_to_data_rows(dataset=dataset)
            for symbol, dataset in symbols.items()
        } for exchange, symbols in datasets.items()
    }

def screeners_to_symbols_datasets(
        screeners: Iterable[BaseScreener]
) -> dict[str, dict[str, pd.DataFrame]]:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.

    :return: The new data.
    """

    results: dict[str, dict[str, pd.DataFrame]] = {}

    for screener in screeners:
        (
            results.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, screener.market)
        )

    return results

def screeners_to_symbols_data(screeners: Iterable[BaseScreener]) -> SymbolsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.

    :return: The new data.
    """

    return symbols_datasets_to_symbols_data(
        screeners_to_symbols_datasets(screeners=screeners)
    )

def sort_symbols_market_data(data: SymbolsMarketData) -> None:
    """
    Sorts the data of the market.

    :param data: The data to sort.
    """

    for exchange, symbols in data.items():
        for symbol_data in symbols.values():
            sort_data(data=symbol_data)

def merge_symbols_market_data(
        *data: SymbolsMarketData, sort: bool = True
) -> SymbolsMarketData:
    """
    Concatenates the states of the market.

    :param data: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    new_data: SymbolsMarketData = {}

    for data_packet in data:
        for exchange, symbols in data_packet.items():
            for symbol, prices in symbols.items():
                (
                    new_data.setdefault(exchange, {}).
                    setdefault(symbol, []).
                    extend(prices)
                )

    if sort:
        sort_symbols_market_data(data=new_data)

    return new_data

AssetsMarketDatasets = dict[str, dict[str, dict[str, pd.DataFrame]]]
SymbolsMarketDatasets = dict[str, dict[str, pd.DataFrame]]

def symbols_to_assets_market_datasets(
        datasets: SymbolsMarketDatasets, separator: bool = None
) -> AssetsMarketDatasets:
    """
    Converts the datasets structure from symbols to assets.

    :param datasets: The datasets to convert.
    :param separator: The separator for the symbols.

    :return: The result structure.
    """

    assets_datasets: AssetsMarketDatasets = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)
            (
                assets_datasets.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, dataset)
            )

    return assets_datasets

AssetData = Data
AssetsData = dict[str, dict[str, dict[str, list[tuple[dt.datetime, _V]]]]]

def symbol_to_assets_data(
        data: SymbolsData, separator: str = None
) -> AssetsData:
    """
    Converts a symbols market values into an assets market values.

    :param data: The source values.
    :param separator: The separator for the symbols.

    :return: The result values.
    """

    assets_prices: AssetsData = {}

    for exchange, symbols in data.items():
        for symbol, symbol_data in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)

            (
                assets_prices.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, []).
                extend(symbol_data)
            )

    return assets_prices

AssetsMarketData = dict[str, dict[str, dict[str, list[tuple[dt.datetime, dict[str, _V]]]]]]

def symbols_to_assets_market_data(
        data: SymbolsMarketData,
        separator: str = None
) -> AssetsMarketData:
    """
    Converts the structure of the market data from assets to symbols.

    :param data: The data to convert.
    :param separator: The separator for the symbols.

    :return: The data in the new structure
    """

    assets_data: AssetsMarketData = {}

    for exchange, symbols in data.items():
        for symbol, symbol_data in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)

            (
                assets_data.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, symbol_data)
            )

    return assets_data

_S = TypeVar("_S")

SymbolsScreeners = dict[str, dict[str, _S]]

def symbols_market_datasets_to_screeners(
        datasets: SymbolsMarketDatasets,
        adjust: bool = True,
        base: type[_S] = None,
        screeners: Iterable[_S] = None
) -> SymbolsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param adjust: The value to adjust the data.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []

    screener_base = base or BaseScreener

    new_screeners: SymbolsScreeners = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            found_screeners = (
                find_screeners(screeners, exchange=exchange, symbol=symbol) or
                [screener_base(symbol=symbol, exchange=exchange)]
            )

            for screener in found_screeners:
                set_screener_dataset(
                    screener=screener, dataset=dataset, adjust=adjust
                )

                (
                    new_screeners.setdefault(exchange, {}).
                    setdefault(symbol, screener)
                )

    return new_screeners

AssetsScreeners = dict[str, dict[str, dict[str, _S]]]

def symbols_to_assets_screeners(
        screeners: SymbolsScreeners, separator: str = None
) -> AssetsScreeners:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.
    :param separator: The separator for the symbols.

    :return: The screeners' collection.
    """

    data: AssetsScreeners = {}

    for exchange, symbols in screeners.items():
        for symbol, screener in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)
            (
                data.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, screener)
            )

    return data

def symbols_screeners(screeners: SymbolsScreeners) -> list[BaseScreener | _S]:
    """
    Collects the screeners from the symbols screeners structure.

    :param screeners: The screeners structure.

    :return: The screeners' collection.
    """

    screeners_collection = []

    for exchange, symbols in screeners.items():
        for symbol, screener in symbols.items():
            screeners_collection.append(screener)

    return screeners_collection

def add_symbols_market_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: SymbolsMarketData,
        adjust: bool = True,
        force: bool = False
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    :param force: The value to force the data into the screeners.
    """

    for exchange, symbols in data.items():
        for symbol, rows in symbols.items():
            add_data_to_symbols_screeners(
                symbol=symbol, exchange=exchange,
                screeners=screeners, data=rows,
                force=force, adjust=adjust
            )

def symbols_market_data(
        columns: dict[str, str],
        data: dict[str, SymbolsData] = None,
        sort: bool = True
) -> SymbolsMarketData:
    """
    Returns the structured data of the state.

    :param data: The values for the data collection.
    :param columns: The columns for the data.
    :param sort: The value to sort the data.

    :return: The data of the state.
    """

    datasets: dict[str, dict[str, dict[dt.datetime, dict[str, _V]]]] = {}

    for name, column in columns.items():
        for exchange, symbols in data[name].items():
            for symbol, symbol_data in symbols.items():
                for index, value in symbol_data:
                    (
                        datasets.
                        setdefault(exchange, {}).
                        setdefault(symbol, {}).
                        setdefault(index_to_datetime(index), {}).
                        setdefault(column, value)
                    )

    new_datasets: SymbolsMarketData = {}

    for exchange, symbols in datasets.items():
        for symbol, symbol_data in symbols.copy().items():
            symbol_data = list(symbol_data.items())
            new_datasets.setdefault(exchange, {})[symbol] = symbol_data

            if sort:
                sort_data(data=symbol_data)

    return new_datasets

def symbols_market_datasets(
        columns: dict[str, str],
        data: dict[str, SymbolsData] = None,
        sort: bool = True
) -> SymbolsMarketDatasets:
    """
    Returns the structured data of the state.

    :param data: The values for the data collection.
    :param columns: The columns for the data.
    :param sort: The value to sort the data.

    :return: The data of the state.
    """

    datasets: SymbolsMarketDatasets = {}

    data = symbols_market_data(columns=columns, data=data, sort=sort)

    for exchange, symbols in data.items():
        for symbol, rows in symbols.items():
            dataset = create_dataset(columns=columns)

            for index, row in rows:
                dataset.loc[index] = row

    return datasets

def symbols_market_state_data(
        columns: dict[str, str],
        data: dict[str, SymbolsData] = None,
        screeners: Iterable[BaseScreener] = None,
        length: int = None,
        adjust: bool = True
) -> dict[str, SymbolsData]:
    """
    Fetches the values and relations between the assets.

    :param data: The values for the data collection.
    :param columns: The columns for the data.
    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    data = data or {name: {} for name in columns}

    if (length is None) and (not adjust):
        length = minimum_common_dataset_length(
            columns=columns, screeners=screeners
        )

    for screener in screeners:
        market = screener_dataset(columns=columns, screener=screener)

        length = adjusted_screener_dataset_length(
            screener=screener, dataset=market,
            adjust=adjust, length=length
        )

        for name, column in columns.items():
            attribute_data = data_from_dataset(
                dataset=market, column=column,
                adjust=adjust, length=length
            )

            (
                data[name].
                setdefault(screener.exchange, {}).
                setdefault(screener.symbol, attribute_data)
            )

    return data

def merge_symbols_market_states_data(
        states: Iterable[MarketState],
        data: dict[str, SymbolsData],
        sort: bool = True
) -> dict[str, SymbolsData]:
    """
    Concatenates the states of the market.

    :param data: The values for the data collection.
    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    for state in states:
        for name in data:
            for exchange, symbols in getattr(state, name).items():
                for symbol, symbol_data in symbols.items():
                    (
                        data[name].
                        setdefault(exchange, {}).
                        setdefault(symbol, []).
                        extend(symbol_data)
                    )

    if sort:
        for attribute_data in data.values():
            sort_symbols_market_data(data=attribute_data)

    return data

@define(repr=False)
@represent
class SymbolsMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This class is a base class for containers of structured market data,
    with symbols structure.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    def data(self) -> SymbolsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        return symbols_market_data(
            columns=self.ATTRIBUTES,
            data={name: getattr(self, name) for name in self.ATTRIBUTES}
        )

    def datasets(self) -> SymbolsMarketDatasets:
        """
        Rebuilds the dataset from the market state.

        :return: The dataset of the state data.
        """

        return symbols_market_datasets(
            columns=self.ATTRIBUTES,
            data={name: getattr(self, name) for name in self.ATTRIBUTES}
        )
