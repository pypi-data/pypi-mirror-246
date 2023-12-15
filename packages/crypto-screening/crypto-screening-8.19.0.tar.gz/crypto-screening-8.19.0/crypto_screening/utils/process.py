# process.py

from typing import Iterable

__all__ = [
    "find_string_value",
    "upper_string_values",
    "lower_string_values",
    "mutual_string_values",
    "string_in_values"
]

def find_string_value(value: str, values: Iterable[str]) -> str:
    """
    Finds the exchange in the exchanges.

    :param value: The name of the exchange.
    :param values: The exchanges to search in.

    :return: The valid exchange name.
    """

    if value in values:
        return value

    if value.lower() in values:
        return value.lower()

    if value.upper() in values:
        return value.upper()

    for valid in values:
        if value.lower() == valid.lower():
            return valid

    return value

def string_in_values(value: str, values: Iterable[str]) -> bool:
    """
    Finds the exchange in the exchanges.

    :param value: The name of the exchange.
    :param values: The exchanges to search in.

    :return: The valid exchange name.
    """

    return find_string_value(value=value, values=values) in values

def upper_string_values(values: Iterable[str]) -> list[str]:
    """
    Converts all string values to upper case.

    :param values: The values to convert.

    :return: The converted values.
    """

    return [value.upper() for value in values]

def lower_string_values(values: Iterable[str]) -> list[str]:
    """
    Converts all string values to upper case.

    :param values: The values to convert.

    :return: The converted values.
    """

    return [value.lower() for value in values]

def mutual_string_values(
        data: dict[str, Iterable[str]],
        minimum: int = None,
        maximum: int = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param data: The exchanges' data.
    :param minimum: The minimum amount of counts for a value.
    :param maximum: The maximum amount of counts for a value.

    :return: The data of the exchanges.
    """

    if minimum is None:
        minimum = 2

    if maximum is None:
        maximum = len(data) * max(len(list(values)) for values in data.values()) + 1

    values = {}

    for key in data:
        for value in data[key]:
            values[value] = values.setdefault(value, 0) + 1

    return {
        key: {
            value for value in data[key]
            if minimum <= values.get(value, 0) <= maximum
        } for key in data
    }
