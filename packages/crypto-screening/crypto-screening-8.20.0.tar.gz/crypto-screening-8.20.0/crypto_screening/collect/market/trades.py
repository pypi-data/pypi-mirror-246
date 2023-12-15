# trades.py

from abc import ABCMeta
import datetime as dt
from typing import Iterable, ClassVar

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from crypto_screening.dataset import PRICE, AMOUNT, SIDE

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
    "symbols_trades_market_state",
    "merge_assets_trades_market_states",
    "merge_symbols_trades_market_states",
    "assets_trades_market_state",
    "AssetsTradesMarketState",
    "SymbolsTradesMarketState",
    "symbols_to_assets_trades_market_state",
    "assets_to_symbols_trades_market_state",
    "TRADES_ATTRIBUTES"
]

AssetsPrices = dict[str, dict[str, dict[str, list[tuple[dt.datetime, float]]]]]
SymbolsPrices = dict[str, dict[str, list[tuple[dt.datetime, float]]]]
AssetsSides = dict[str, dict[str, dict[str, list[tuple[dt.datetime, str]]]]]
SymbolsSides = dict[str, dict[str, list[tuple[dt.datetime, str]]]]

TRADES_ATTRIBUTES = {
    "amounts": AMOUNT,
    "prices": PRICE,
    "sides": SIDE
}

@define(repr=False)
@represent
class TradesMarketState(MarketState, metaclass=ABCMeta):
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
    __modifiers__.excluded.extend(["amounts", "values", "sides"])

    ATTRIBUTES: ClassVar[dict[str, str]] = TRADES_ATTRIBUTES

AssetsMarketData = dict[str, dict[str, dict[str, list[tuple[dt.datetime, dict[str, float]]]]]]
AssetsMarketDatasets = dict[str, dict[str, dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsTradesMarketState(TradesMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - amounts:
        The volume of the base asset of each trade.

    - price:
        The price of the base asset in the trade.

    - side:
        The side on the trade.

    >>> from crypto_screening.collect.market.trades import assets_trades_market_state
    >>>
    >>> state = assets_trades_market_state(...)
    """

    amounts: AssetsPrices
    prices: AssetsPrices
    sides: AssetsSides

    def amount(
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
            exchange=exchange, symbol=symbol, data=self.amounts,
            separator=separator, provider=self
        )

    def price(
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
            exchange=exchange, symbol=symbol, data=self.prices,
            separator=separator, provider=self
        )

    def side(
            self, exchange: str, symbol: str, separator: str = None
    ) -> list[tuple[dt.datetime, str]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, data=self.sides,
            separator=separator, provider=self
        )

    def in_amounts_prices(
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
            separator=separator, data=self.amounts
        )

    def in_prices_prices(
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
            separator=separator, data=self.prices
        )

    def in_sides_prices(
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
            separator=separator, data=self.sides
        )

SymbolsMarketData = dict[str, dict[str, list[tuple[dt.datetime, dict[str, float]]]]]
SymbolsMarketDatasets = dict[str, dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsTradesMarketState(TradesMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - amounts:
        The volume of the base asset of each trade.

    - price:
        The price of the base asset in the trade.

    - side:
        The side on the trade.

    >>> from crypto_screening.collect.market.trades import symbols_trades_market_state
    >>>
    >>> state = symbols_trades_market_state(...)
    """

    amounts: SymbolsPrices
    prices: SymbolsPrices
    sides: SymbolsSides

    def amount(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.amounts,
            provider=self
        )

    def price(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.prices,
            provider=self
        )

    def side(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, str]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.sides, provider=self
        )

    def in_amounts_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.amounts
        )

    def in_prices_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.prices
        )

    def in_sides_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.sides
        )

def assets_trades_market_state(
        screeners: Iterable[BaseScreener] = None,
        separator: str = None,
        length: int = None,
        adjust: bool = True
) -> AssetsTradesMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsTradesMarketState(
        screeners=screeners,
        **assets_market_state_data(
            columns=TradesMarketState.ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )

def symbols_trades_market_state(
        screeners: Iterable[BaseScreener] = None,
        length: int = None,
        adjust: bool = True
) -> SymbolsTradesMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsTradesMarketState(
        screeners=screeners,
        **symbols_market_state_data(
            columns=TradesMarketState.ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )

def merge_symbols_trades_market_states(
        states: Iterable[SymbolsTradesMarketState], sort: bool = True
) -> SymbolsTradesMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)

    return SymbolsTradesMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={
                name: {} for name in TradesMarketState.ATTRIBUTES
            }, sort=sort
        )
    )

def merge_assets_trades_market_states(
        states: Iterable[AssetsTradesMarketState], sort: bool = True
) -> AssetsTradesMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)

    return AssetsTradesMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={
                name: {} for name in TradesMarketState.ATTRIBUTES
            }, sort=sort
        )
    )

def assets_to_symbols_trades_market_state(
        state: AssetsTradesMarketState, separator: str = None
) -> SymbolsTradesMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsTradesMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in TradesMarketState.ATTRIBUTES
        }
    )

def symbols_to_assets_trades_market_state(
        state: SymbolsTradesMarketState, separator: str = None
) -> AssetsTradesMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsTradesMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in TradesMarketState.ATTRIBUTES
        }
    )
