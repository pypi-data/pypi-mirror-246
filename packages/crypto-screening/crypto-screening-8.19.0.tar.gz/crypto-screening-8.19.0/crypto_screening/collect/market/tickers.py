# tickers.py

from abc import ABCMeta
import datetime as dt
from typing import Iterable, ClassVar

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from crypto_screening.dataset import BIDS, ASKS

from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.collect.market.state import (
    MarketState, assets_market_values, SymbolsMarketState,
    is_symbol_in_assets_market_values, symbols_market_values,
    is_symbol_in_symbols_market_values, merge_symbols_market_states_data,
    assets_to_symbols_data, assets_market_state_data,
    symbol_to_assets_data, symbols_market_state_data,
    merge_assets_market_states_data, AssetsMarketState
)

__all__ = [
    "symbols_tickers_market_state",
    "merge_assets_tickers_market_states",
    "merge_symbols_tickers_market_states",
    "assets_tickers_market_state",
    "AssetsTickersMarketState",
    "SymbolsTickersMarketState",
    "symbols_to_assets_tickers_market_state",
    "assets_to_symbols_tickers_market_state",
    "TICKERS_ATTRIBUTES"
]

AssetsPrices = dict[str, dict[str, dict[str, list[tuple[dt.datetime, float]]]]]
SymbolsPrices = dict[str, dict[str, list[tuple[dt.datetime, float]]]]

TICKERS_ATTRIBUTES = {
    "bids": BIDS,
    "asks": ASKS
}

@define(repr=False)
@represent
class TickersMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **MarketState.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks"])

    ATTRIBUTES: ClassVar[dict[str, str]] = TICKERS_ATTRIBUTES

AssetsMarketData = dict[str, dict[str, dict[str, list[tuple[dt.datetime, dict[str, float]]]]]]
AssetsMarketDatasets = dict[str, dict[str, dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsTickersMarketState(TickersMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - bids:
        The bids values of the assets.

    - asks:
        The asks values of the assets.

    >>> from crypto_screening.collect.market.tickers import assets_tickers_market_state
    >>>
    >>> state = assets_tickers_market_state(...)
    """

    bids: AssetsPrices
    asks: AssetsPrices

    def bid(
            self, exchange: str, symbol: str, separator: str = None
    ) -> list[tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.bids,
            separator=separator, provider=self
        )

    def ask(
            self, exchange: str, symbol: str, separator: str = None
    ) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.asks,
            separator=separator, provider=self
        )

    def in_bids_prices(
            self,
            exchange: str,
            symbol: str,
            separator: str = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.bids
        )

    def in_asks_prices(
            self,
            exchange: str,
            symbol: str,
            separator: str = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, data=self.asks
        )

SymbolsMarketData = dict[str, dict[str, list[tuple[dt.datetime, dict[str, float]]]]]
SymbolsMarketDatasets = dict[str, dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsTickersMarketState(TickersMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - bids:
        The bids values of the assets.

    - asks:
        The asks values of the assets.

    >>> from crypto_screening.collect.market.tickers import symbols_tickers_market_state
    >>>
    >>> state = symbols_tickers_market_state(...)
    """

    bids: SymbolsPrices
    asks: SymbolsPrices

    def bid(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.bids, provider=self
        )

    def ask(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.asks, provider=self
        )

    def in_bids_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.bids
        )

    def in_asks_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.asks
        )

def assets_tickers_market_state(
        screeners: Iterable[BaseScreener] = None,
        separator: str = None,
        length: int = None,
        adjust: bool = True
) -> AssetsTickersMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsTickersMarketState(
        screeners=screeners,
        **assets_market_state_data(
            columns=TickersMarketState.ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )

def symbols_tickers_market_state(
        screeners: Iterable[BaseScreener] = None,
        length: int = None,
        adjust: bool = True
) -> SymbolsTickersMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsTickersMarketState(
        screeners=screeners,
        **symbols_market_state_data(
            columns=TickersMarketState.ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )

def merge_symbols_tickers_market_states(
        states: Iterable[SymbolsTickersMarketState], sort: bool = True
) -> SymbolsTickersMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)

    return SymbolsTickersMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={
                name: {} for name in TickersMarketState.ATTRIBUTES
            }, sort=sort
        )
    )

def merge_assets_tickers_market_states(
        states: Iterable[AssetsTickersMarketState], sort: bool = True
) -> AssetsTickersMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)

    return AssetsTickersMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={
                name: {} for name in TickersMarketState.ATTRIBUTES
            }, sort=sort
        )
    )

def assets_to_symbols_tickers_market_state(
        state: AssetsTickersMarketState, separator: str = None
) -> SymbolsTickersMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsTickersMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in TickersMarketState.ATTRIBUTES
        }
    )

def symbols_to_assets_tickers_market_state(
        state: SymbolsTickersMarketState, separator: str = None
) -> AssetsTickersMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsTickersMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in TickersMarketState.ATTRIBUTES
        }
    )
