# symbols.py

import warnings
from typing import Iterable, Any, ClassVar, Self

from attrs import define

from represent import Modifiers

from multithreading import Caller, multi_threaded_call

from crypto_screening.utils.process import (
    find_string_value, upper_string_values,
    mutual_string_values, string_in_values
)
from crypto_screening.exchanges import (
    EXCHANGES, EXCHANGE_NAMES, BUILTIN_EXCHANGES_SYMBOLS
)
from crypto_screening.symbols import (
    symbol_to_parts, adjust_symbol, Separator, Pair
)
from crypto_screening.validate import validate_exchange
from crypto_screening.collect.foundation.exchanges import exchanges_data

__all__ = [
    "exchanges_symbols",
    "mutual_exchanges_symbols",
    "include_symbols",
    "exclude_symbols",
    "exchange_symbols",
    "all_exchange_symbols",
    "matching_symbol_pair",
    "matching_symbol_pairs",
    "MarketSymbolSignature",
    "matching_symbol_signatures",
    "include_exchanges_symbols",
    "exclude_exchanges_symbols",
    "all_exchanges_symbols",
    "select_exchanges_symbols"
]

def include_symbols(
        symbols: Iterable[str],
        separator: str = None,
        adjust: bool = True,
        bases: Iterable[str] = None,
        quotes: Iterable[str] = None,
        included: Iterable[str] = None
) -> set[str]:
    """
    Removes all symbols with not matching base or quote.

    :param symbols: The symbols to filter.
    :param separator: The separator for the symbols.
    :param bases: The bases to include.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes to include.
    :param included: The symbols to include.

    :return: The filtered symbols.
    """

    saved = set()

    quotes = upper_string_values(quotes or [])
    bases = upper_string_values(bases or [])
    included = upper_string_values(included or [])

    for symbol in symbols:
        if symbol in included:
            saved.add(symbol)

            continue

        try:
            symbol = adjust_symbol(symbol=symbol, separator=separator)

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e

        if symbol in included:
            saved.add(symbol)

            continue

        base, quote = symbol_to_parts(
            symbol=symbol, separator=separator
        )

        if (
            string_in_values(value=base, values=bases) or
            string_in_values(value=quote, values=quotes)
        ):
            saved.add(symbol)

    return saved

def exclude_symbols(
        symbols: Iterable[str],
        separator: str = None,
        adjust: bool = True,
        bases: Iterable[str] = None,
        quotes: Iterable[str] = None,
        excluded: Iterable[str] = None
) -> set[str]:
    """
    Removes all symbols with the matching base or quote.

    :param symbols: The symbols to filter.
    :param separator: The separator for the symbols.
    :param bases: The bases to exclude.
    :param quotes: The quotes to exclude.
    :param adjust: The value to adjust the invalid exchanges.
    :param excluded: The symbols to exclude.

    :return: The filtered symbols.
    """

    saved = set()

    quotes = upper_string_values(quotes or [])
    bases = upper_string_values(bases or [])
    excluded = upper_string_values(excluded or [])

    for symbol in symbols:
        if symbol in excluded:
            continue

        try:
            symbol = adjust_symbol(symbol=symbol, separator=separator)

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e

        if symbol in excluded:
            continue

        base, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if (
            string_in_values(value=base, values=bases) or
            string_in_values(value=quote, values=quotes)
        ):
            continue

        saved.add(symbol)

    return set(saved)

def include_exchanges_symbols(
        data: dict[str, Iterable[str]],
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None
) -> dict[str, set[str]]:
    """
    Removes all symbols with not matching base or quote.

    :param data: The data to filter.
    :param bases: The bases to include.
    :param quotes: The quotes to include.
    :param included: The symbols to include.

    :return: The filtered symbols.
    """

    if all(value is None for value in (bases, quotes, included)):
        return {exchange: set(symbols) for exchange, symbols in data.items()}

    if not isinstance(quotes, dict):
        saved_quotes = quotes
        quotes = {exchange: saved_quotes for exchange in data}

    if not isinstance(bases, dict):
        saved_bases = bases
        bases = {exchange: saved_bases for exchange in data}

    if not isinstance(included, dict):
        saved_included = included
        included = {exchange: saved_included for exchange in data}

    return {
        exchange: saved for exchange, symbols in data.items()
        if (
            saved := include_symbols(
                symbols=symbols,
                bases=bases.get(exchange, None),
                quotes=quotes.get(exchange, None),
                included=included.get(exchange, None)
            )
        )
    }

def exclude_exchanges_symbols(
        data: dict[str, Iterable[str]],
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None
) -> dict[str, set[str]]:
    """
    Removes all symbols with the matching base or quote.

    :param data: The data to filter.
    :param bases: The bases to exclude.
    :param quotes: The quotes to exclude.
    :param excluded: The symbols to exclude.

    :return: The filtered symbols.
    """

    if all(value is None for value in (bases, quotes, excluded)):
        return {exchange: set(symbols) for exchange, symbols in data.items()}

    if not isinstance(quotes, dict):
        saved_quotes = quotes
        quotes = {exchange: saved_quotes for exchange in data}

    if not isinstance(bases, dict):
        saved_bases = bases
        bases = {exchange: saved_bases for exchange in data}

    if not isinstance(excluded, dict):
        saved_excluded = excluded
        excluded = {exchange: saved_excluded for exchange in data}

    return {
        exchange: saved for exchange, symbols in data.items()
        if (
            saved := exclude_symbols(
                symbols=symbols,
                bases=bases.get(exchange, None),
                quotes=quotes.get(exchange, None),
                excluded=excluded.get(exchange, None)
            )
        )
    }

def all_exchange_symbols(
        exchange: str,
        separator: str = None,
        adjust: bool = True,
        test: bool = False
) -> set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param test: Include test assets.

    :return: The data of the exchanges.
    """

    validate_exchange(exchange=exchange, exchanges=EXCHANGE_NAMES)

    try:
        found_symbols: Iterable[str] = EXCHANGES[
            find_string_value(value=exchange, values=EXCHANGES)
        ].symbols()

    except Exception as e:
        error_message = (
            f"Cannot fetch symbols of '{exchange}' exchange: {str(e)}."
        )

        if not adjust:
            raise RuntimeError(error_message)

        else:
            warnings.warn(error_message)

            return set()

    symbols = set()

    if separator is None:
        separator = Separator.value

    for symbol in found_symbols:
        try:
            symbol = adjust_symbol(symbol=symbol, separator=separator)

            if symbol.count(separator) != 1:
                raise ValueError(
                    f"Invalid symbol structure: {symbol}. "
                    f"Symbol must contain only one separator."
                )

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e

        base, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if (not test) and base.startswith("TEST") and quote.startswith("TEST"):
            continue

        symbols.add(symbol)

    return symbols

def all_exchanges_symbols(
        exchanges: Iterable[str],
        separator: str = None,
        adjust: bool = True,
        test: bool = False
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param test: Include test assets.

    :return: The data of the exchanges.
    """

    results = multi_threaded_call(
        [
            Caller(
                target=all_exchange_symbols, kwargs=dict(
                    exchange=exchange, separator=separator,
                    adjust=adjust, test=test
                ), identifier=exchange
            ) for exchange in exchanges
        ]
    )

    return {
        exchange: results.result(exchange).returns
        for exchange in exchanges
    }

def exchange_symbols(
        exchange: str = None,
        separator: str = None,
        adjust: bool = True,
        bases: Iterable[str] = None,
        quotes: Iterable[str] = None,
        included: Iterable[str] = None,
        excluded: Iterable[str] = None
) -> set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param quotes: The quotes of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param bases: The bases of the asset pairs.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    symbols = (
        symbols if all(value is None for value in (included, bases, quotes)) else
        include_symbols(
            symbols=symbols, included=included,
            bases=bases, quotes=quotes, separator=separator
        )
    )

    return symbols if excluded is None else exclude_symbols(
        symbols=symbols, excluded=excluded, separator=separator, adjust=adjust
    )

def exchanges_symbols(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return exchanges_data(
        collector=exchange_symbols,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator, included=included, bases=bases
    )

def select_exchanges_symbols(
        exchanges: Iterable[str] = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None,
        data: dict[str, Iterable[str]] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param data: The exchanges.
    :param exchanges: The exchange names to keep.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    if data is None:
        data = BUILTIN_EXCHANGES_SYMBOLS

    if exchanges is not None:
        data = {
            exchange: symbols for exchange, symbols in data.items()
            if exchange in exchanges
        }

    if bases is not None:
        data = include_exchanges_symbols(
            data=data, bases=bases
        )

    if quotes is not None:
        data = include_exchanges_symbols(
            data=data, quotes=quotes
        )

    if excluded is not None:
        data = exclude_exchanges_symbols(
            data=data, excluded=excluded
        )

    if included is not None:
        data = exclude_exchanges_symbols(
            data=data, excluded=included
        )

    return data

def mutual_exchanges_symbols(
        exchanges: Iterable[str] = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None,
        data: dict[str, Iterable[str]] = None,
        separator: str = None,
        adjust: bool = True
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return mutual_string_values(
        data=data or exchanges_symbols(
            exchanges=exchanges, quotes=quotes, excluded=excluded,
            adjust=adjust, separator=separator, included=included, bases=bases
        )
    )

AssetMatches = Iterable[Iterable[str]]

def matching_symbol_pair(
        symbol1: str,
        symbol2: str, /, *,
        matches: AssetMatches = None,
        separator: str = None
) -> bool:
    """
    Checks if the symbols are valid with the matching currencies.

    :param symbol1: The first ticker.
    :param symbol2: The second ticker.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    symbol1 = adjust_symbol(symbol=symbol1, separator=separator)
    symbol2 = adjust_symbol(symbol=symbol2, separator=separator)

    if symbol1 == symbol2:
        return True

    asset1, currency1 = symbol_to_parts(symbol=symbol1, separator=separator)
    asset2, currency2 = symbol_to_parts(symbol=symbol2, separator=separator)

    if asset1 != asset2:
        return False

    matches = matches or ()

    return any(
        (currency1 in match) and (currency2 in match)
        for match in matches
    )

ExchangeSymbolPairs = set[tuple[tuple[str, str], tuple[str, str]]]
ExchangesAssetMatches = dict[Iterable[str], AssetMatches] | AssetMatches

def matching_symbol_pairs(
        data: dict[str, Iterable[str]],
        matches: ExchangesAssetMatches = None,
        separator: str = None
) -> ExchangeSymbolPairs:
    """
    Checks if the symbols are valid with the matching currencies.

    :param data: The symbols.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    pairs = set()
    exchange_symbol_pairs = []

    for exchange, symbols in data.items():
        exchange_symbol_pairs.extend(
            [(exchange, symbol) for symbol in symbols]
        )

    for exchange1, symbol1 in exchange_symbol_pairs:
        for exchange2, symbol2 in exchange_symbol_pairs:
            if exchange1 == exchange2:
                continue

            match1 = ((exchange1, symbol1), (exchange2, symbol2))
            match2 = ((exchange2, symbol2), (exchange1, symbol1))

            if (match1 in pairs) or (match2 in pairs):
                continue

            exchanges_matches = (
                matches if not isinstance(matches, dict) else
                [*matches.get(exchange1, []), *matches.get(exchange2, [])]
            )

            if (
                (exchange1 != exchange2) and
                matching_symbol_pair(
                    symbol1, symbol2,
                    matches=exchanges_matches or None,
                    separator=separator
                )
            ):
                pairs.add(match1)
                pairs.add(match2)

    return pairs

@define(slots=False, init=False, repr=False, eq=False, unsafe_hash=True)
class MarketSymbolSignature(Pair):
    """A class to represent the data for the execution of a trade."""

    __slots__ = "_exchange",

    __modifiers__ = Modifiers(**Pair.__modifiers__)
    __modifiers__.properties.append('exchange')

    EXCHANGE: ClassVar[str] = 'exchange'

    def __init__(
            self,
            exchange: str,
            base: str,
            quote: str,
            separator: str = None
    ) -> None:
        """
        Defines the class attributes.

        :param exchange: The exchange name.
        :param base: The base asset.
        :param quote: The quote asset.
        :param separator: The symbol separator.
        """

        super().__init__(base=base, quote=quote, separator=separator)

        self._exchange = exchange

    def __eq__(self, other: Any) -> bool:
        """
        Checks if the signatures are equal.

        :param other: The signature to compare.

        :return: The equality value.
        """

        if type(other) is not type(self):
            return NotImplemented

        other: MarketSymbolSignature

        return (self is other) or (
            (self.exchange == other.exchange) and
            (self.base == other.base) and
            (self.quote == other.quote)
        )

    @property
    def exchange(self) -> str:
        """
        Returns the property value.

        :return: The exchange name.
        """

        return self._exchange

    @classmethod
    def load(cls, data: dict[str, str]) -> Self:
        """
        Creates a pair of assets from the data.

        :param data: The pair data.

        :return: The pair object.
        """

        return cls(
            exchange=data[cls.EXCHANGE],
            base=data[cls.BASE],
            quote=data[cls.QUOTE],
            separator=data.get(cls.SEPARATOR, None)
        )

    def json(self) -> dict[str, str]:
        """
        Converts the data into a json format.

        :return: The chain of assets.
        """

        return {
            self.EXCHANGE: self.exchange,
            **super().json()
        }

def matching_symbol_signatures(
        pairs: ExchangeSymbolPairs = None,
        data: dict[str, Iterable[str]] = None,
        matches: ExchangesAssetMatches = None,
        separator: str = None
) -> set[tuple[MarketSymbolSignature, MarketSymbolSignature]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param data: The data for the pairs.
    :param pairs: The pairs' data.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    if (data is None) and (pairs is None):
        raise ValueError(
            f"One of 'pairs' and 'data' parameters must be given, "
            f"when 'pairs' is superior to 'data'."
        )

    elif (not pairs) and (not data):
        return set()

    new_pairs = []

    pairs = pairs or matching_symbol_pairs(
        data=data, matches=matches, separator=separator
    )

    for (exchange1, symbol1), (exchange2, symbol2) in pairs:
        asset1, currency1 = symbol_to_parts(symbol1)
        asset2, currency2 = symbol_to_parts(symbol2)

        new_pairs.append(
            (
                MarketSymbolSignature(
                    base=asset1, quote=currency1,
                    exchange=exchange1
                ),
                MarketSymbolSignature(
                    base=asset2, quote=currency2,
                    exchange=exchange2
                )
            )
        )

    return set(new_pairs)
