# market.py

from typing import Iterable

from crypto_screening.collect.screeners import exchanges_symbols_screeners
from crypto_screening.collect.market.orderbook import (
    assets_orderbook_market_state, symbols_orderbook_market_state,
    SymbolsOrderbookMarketState, AssetsOrderbookMarketState
)
from crypto_screening.collect.market.ohlcv import (
    assets_ohlcv_market_state, symbols_ohlcv_market_state,
    SymbolsOHLCVMarketState, AssetsOHLCVMarketState
)
from crypto_screening.collect.market.tickers import (
    assets_tickers_market_state, symbols_tickers_market_state,
    SymbolsTickersMarketState, AssetsTickersMarketState
)
from crypto_screening.collect.market.trades import (
    assets_trades_market_state, symbols_trades_market_state,
    SymbolsTradesMarketState, AssetsTradesMarketState
)
from crypto_screening.screeners.container import (
    FrozenScreenersContainer, ScreenersContainer
)

__all__ = [
    "FrozenScreenersMarket",
    "ScreenersMarket"
]

ExchangesData = dict[str, Iterable[str]] | Iterable[str]

class FrozenScreenersMarket(FrozenScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> from crypto_screening.screeners.market import FrozenScreenersMarket
    >>> from crypto_screening.screeners import BaseScreener
    >>>
    >>> market = FrozenScreenersMarket(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> market.find_screener(exchange="binance", symbol="BTC/USDT"))
    """

    def assets_orderbook_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> AssetsOrderbookMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.orderbook_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_orderbook_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )

    def symbols_orderbook_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> SymbolsOrderbookMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.orderbook_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_orderbook_market_state(
            screeners=screeners, length=length, adjust=adjust
        )

    def assets_ohlcv_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> AssetsOHLCVMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.ohlcv_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_ohlcv_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )

    def symbols_ohlcv_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> SymbolsOHLCVMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.ohlcv_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_ohlcv_market_state(
            screeners=screeners, length=length, adjust=adjust
        )

    def assets_trades_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> AssetsTradesMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.trades_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_trades_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )

    def symbols_trades_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> SymbolsTradesMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.trades_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_trades_market_state(
            screeners=screeners, length=length, adjust=adjust
        )

    def assets_orders_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> AssetsTickersMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.tickers_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_tickers_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )

    def symbols_orders_market_state(
            self,
            exchanges: Iterable[str] = None,
            separator: str = None,
            length: int = None,
            adjust: bool = True,
            bases: ExchangesData = None,
            quotes: ExchangesData = None,
            included: ExchangesData = None,
            excluded: ExchangesData = None
    ) -> SymbolsTickersMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.tickers_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_tickers_market_state(
            screeners=screeners, length=length, adjust=adjust
        )

class ScreenersMarket(ScreenersContainer, FrozenScreenersMarket):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> from crypto_screening.screeners.market import ScreenersMarket
    >>> from crypto_screening.screeners import BaseScreener
    >>>
    >>> market = ScreenersMarket(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> market.find_screener(exchange="binance", symbol="BTC/USDT"))
    """
