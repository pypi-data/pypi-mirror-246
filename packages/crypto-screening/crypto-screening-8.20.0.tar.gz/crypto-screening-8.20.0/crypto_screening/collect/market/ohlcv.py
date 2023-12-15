# ohlcv.py

from abc import ABCMeta
import datetime as dt
from typing import Iterable, ClassVar

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from market_break.dataset import OPEN, HIGH, LOW, CLOSE, VOLUME

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
    "symbols_ohlcv_market_state",
    "merge_assets_ohlcv_market_states",
    "merge_symbols_ohlcv_market_states",
    "assets_ohlcv_market_state",
    "AssetsOHLCVMarketState",
    "SymbolsOHLCVMarketState",
    "symbols_to_assets_ohlcv_market_state",
    "assets_to_symbols_ohlcv_market_state",
    "OHLCV_ATTRIBUTES"
]

AssetsPrices = dict[str, dict[str, dict[str, list[tuple[dt.datetime, float]]]]]
SymbolsPrices = dict[str, dict[str, list[tuple[dt.datetime, float]]]]

OHLCV_ATTRIBUTES = {
    "opens": OPEN,
    "highs": HIGH,
    "lows": LOW,
    "closes": CLOSE,
    "volumes": VOLUME
}

@define(repr=False)
@represent
class OHLCVMarketState(MarketState, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    __modifiers__: ClassVar[Modifiers] = Modifiers(**MarketState.__modifiers__)
    __modifiers__.excluded.extend(["open", "high", "low", "close", "volume"])

    ATTRIBUTES: ClassVar[dict[str, str]] = OHLCV_ATTRIBUTES

AssetsMarketData = dict[str, dict[str, dict[str, list[tuple[dt.datetime, dict[str, float]]]]]]
AssetsMarketDatasets = dict[str, dict[str, dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsOHLCVMarketState(OHLCVMarketState, AssetsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - opens:
        The open price values of the symbol.

    - high:
        The open price values of the symbol.

    - low:
        The low price values of the symbol.

    - close:
        The close price values of the symbol.

    - volume:
        The volume price values of the symbol.

    >>> from crypto_screening.collect.market.ohlcv import assets_ohlcv_market_state
    >>>
    >>> state = assets_ohlcv_market_state(...)
    """

    opens: AssetsPrices
    highs: AssetsPrices
    lows: AssetsPrices
    closes: AssetsPrices
    volumes: AssetsPrices

    def open(
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
            exchange=exchange, symbol=symbol, data=self.opens,
            separator=separator, provider=self
        )

    def high(
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
            exchange=exchange, symbol=symbol, data=self.highs,
            separator=separator, provider=self
        )

    def low(
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
            exchange=exchange, symbol=symbol, data=self.lows,
            separator=separator, provider=self
        )

    def close(
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
            exchange=exchange, symbol=symbol, data=self.closes,
            separator=separator, provider=self
        )

    def volume(
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
            exchange=exchange, symbol=symbol, data=self.closes,
            separator=separator, provider=self
        )

    def in_open_prices(
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
            separator=separator, data=self.opens
        )

    def in_high_prices(
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
            separator=separator, data=self.highs
        )

    def in_low_prices(
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
            separator=separator, data=self.lows
        )

    def in_close_prices(
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
            separator=separator, data=self.closes
        )

    def in_volume_prices(
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
            separator=separator, data=self.volumes
        )

SymbolsMarketData = dict[str, dict[str, list[tuple[dt.datetime, dict[str, float]]]]]
SymbolsMarketDatasets = dict[str, dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsOHLCVMarketState(OHLCVMarketState, SymbolsMarketState):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - opens:
        The open price values of the symbol.

    - high:
        The open price values of the symbol.

    - low:
        The low price values of the symbol.

    - close:
        The close price values of the symbol.

    - volume:
        The volume price values of the symbol.

    >>> from crypto_screening.collect.market.ohlcv import symbols_ohlcv_market_state
    >>>
    >>> state = symbols_ohlcv_market_state(...)
    """

    opens: SymbolsPrices
    highs: SymbolsPrices
    lows: SymbolsPrices
    closes: SymbolsPrices
    volumes: SymbolsPrices

    def open(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.opens, provider=self
        )

    def high(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.highs, provider=self
        )

    def low(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.lows, provider=self
        )

    def close(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.closes, provider=self
        )

    def volume(self, exchange: str, symbol: str) -> list[tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            data=self.volumes, provider=self
        )

    def in_open_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.opens
        )

    def in_high_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.highs
        )

    def in_low_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.lows
        )

    def in_close_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The in_asks_volume_prices value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.closes
        )

    def in_volume_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The in_asks_volume_prices value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, data=self.volumes
        )

def assets_ohlcv_market_state(
        screeners: Iterable[BaseScreener] = None,
        separator: str = None,
        length: int = None,
        adjust: bool = True
) -> AssetsOHLCVMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsOHLCVMarketState(
        screeners=screeners,
        **assets_market_state_data(
            columns=OHLCVMarketState.ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )

def symbols_ohlcv_market_state(
        screeners: Iterable[BaseScreener] = None,
        length: int = None,
        adjust: bool = True
) -> SymbolsOHLCVMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsOHLCVMarketState(
        screeners=screeners,
        **symbols_market_state_data(
            columns=OHLCVMarketState.ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )

def merge_symbols_ohlcv_market_states(
        states: Iterable[SymbolsOHLCVMarketState], sort: bool = True
) -> SymbolsOHLCVMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)

    return SymbolsOHLCVMarketState(
        screeners=screeners,
        **merge_symbols_market_states_data(
            states, data={
                name: {} for name in OHLCVMarketState.ATTRIBUTES
            }, sort=sort
        )
    )

def merge_assets_ohlcv_market_states(
        states: Iterable[AssetsOHLCVMarketState], sort: bool = True
) -> AssetsOHLCVMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = set()

    for state in states:
        screeners.update(state.screeners)

    return AssetsOHLCVMarketState(
        screeners=screeners,
        **merge_assets_market_states_data(
            states, data={
                name: {} for name in OHLCVMarketState.ATTRIBUTES
            }, sort=sort
        )
    )

def assets_to_symbols_ohlcv_market_state(
        state: AssetsOHLCVMarketState, separator: str = None
) -> SymbolsOHLCVMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsOHLCVMarketState(
        **{
            name: assets_to_symbols_data(
                data=getattr(state, name), separator=separator
            ) for name in OHLCVMarketState.ATTRIBUTES
        }
    )

def symbols_to_assets_ohlcv_market_state(
        state: SymbolsOHLCVMarketState, separator: str = None
) -> AssetsOHLCVMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsOHLCVMarketState(
        **{
            name: symbol_to_assets_data(
                data=getattr(state, name), separator=separator
            ) for name in OHLCVMarketState.ATTRIBUTES
        }
    )
