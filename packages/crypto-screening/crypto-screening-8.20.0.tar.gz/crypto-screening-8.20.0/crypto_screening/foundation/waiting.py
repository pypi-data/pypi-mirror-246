# waiting.py

import datetime as dt
import time
from typing import Iterable, Callable, TypeVar

from crypto_screening.foundation.data import DataCollector
from crypto_screening.foundation.state import WaitingState
from crypto_screening.foundation.protocols import (
    BaseScreenerProtocol, BaseMarketScreenerProtocol
)

__all__ = [
    "base_await_update",
    "base_await_initialization",
    "base_await_dynamic_update",
    "base_await_dynamic_initialization",
    "Condition"
]

_BS = TypeVar("_BS", BaseScreenerProtocol, BaseMarketScreenerProtocol, DataCollector)

Gatherer = Callable[[Iterable[_BS]], Iterable[_BS]]
TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

class Condition:
    """A class to represent the value of a condition."""

    VALUE = True

    def __init__(self, value: bool = None) -> None:
        """
        Defines the value of the object.

        :param value: The value of the condition.
        """

        if value is None:
            value = self.VALUE

        self.value = value

def base_await_dynamic_initialization(
        screeners: Iterable[_BS],
        stop: bool = None,
        delay: TimeDuration = None,
        cancel: TimeDestination = None,
        condition: Condition = None,
        gatherer: Gatherer = None
) -> WaitingState[_BS]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    if gatherer is None:
        gatherer = list

    if cancel is None:
        cancel = 0

    if delay is None:
        delay = 0

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()

    start = dt.datetime.now()
    count = 0
    canceled = False

    while screeners:
        if (condition is not None) and (not condition.value):
            break

        s = time.time()

        gathered_screeners = gatherer(screeners)

        if all(
            len(screener.market) > 0
            for screener in gathered_screeners
        ):
            break

        if (
            isinstance(cancel, dt.timedelta) and
            (canceled := ((dt.datetime.now() - start) > cancel))
        ):
            break

        count += 1

        e = time.time()

        if isinstance(delay, (int, float)):
            time.sleep(max([delay - (e - s), 0]))

    if stop:
        for screener in screeners:
            screener.stop()

    return WaitingState[_BS](
        screeners=screeners, delay=delay,
        count=count, end=dt.datetime.now(), start=start,
        cancel=cancel, canceled=canceled
    )

def base_await_initialization(
        *screeners: _BS,
        stop: bool = None,
        delay: TimeDuration = None,
        cancel: TimeDestination = None,
        condition: Condition = None,
        gatherer: Gatherer = None
) -> WaitingState[_BS]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    return base_await_dynamic_initialization(
        screeners, delay=delay, stop=stop, condition=condition,
        cancel=cancel, gatherer=gatherer
    )

def base_await_dynamic_update(
        screeners: Iterable[_BS],
        stop: bool = None,
        delay: TimeDuration = None,
        cancel: TimeDestination = None,
        condition: Condition = None,
        gatherer: Gatherer = None
) -> WaitingState[_BS]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    if cancel is None:
        cancel = 0

    if delay is None:
        delay = 0

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()

    start = dt.datetime.now()
    count = 0
    canceled = False

    wait = base_await_dynamic_initialization(
        screeners, delay=delay, cancel=cancel,
        stop=stop, condition=condition
    )

    if not screeners:
        return wait

    while screeners:
        if (condition is not None) and (not condition.value):
            break

        s = time.time()

        checked_screeners = gatherer(screeners)

        indexes = {
            screener: len(screener.market)
            for screener in checked_screeners
        }

        if (
            isinstance(cancel, dt.timedelta) and
            (canceled := ((dt.datetime.now() - start) > cancel))
        ):
            break

        e = time.time()

        if isinstance(delay, (int, float)):
            time.sleep(max([delay - (e - s), 0]))

        count += 1

        new_indexes = {
            screener: len(screener.market)
            for screener in checked_screeners
        }

        if indexes == new_indexes:
            break

    if stop:
        for screener in screeners:
            screener.stop()

    return WaitingState[_BS](
        screeners=screeners, delay=delay,
        count=count, end=dt.datetime.now(), start=start,
        cancel=cancel, canceled=canceled
    )

def base_await_update(
        *screeners: _BS,
        stop: bool = None,
        delay: TimeDuration = None,
        cancel: TimeDestination = None,
        condition: Condition = None,
        gatherer: Gatherer = None
) -> WaitingState[_BS]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.
    :param condition: The condition to control the waiting outside the function.

    :returns: The total delay.
    """

    return base_await_dynamic_update(
        screeners, delay=delay, stop=stop, condition=condition,
        cancel=cancel, gatherer=gatherer
    )
