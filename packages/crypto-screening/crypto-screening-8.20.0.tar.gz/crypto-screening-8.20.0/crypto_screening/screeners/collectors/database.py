# database.py

import datetime as dt
from typing import Iterable

from sqlalchemy import Engine
from sqlalchemy.orm.session import Session

from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.screeners.database import (
    extract_database_table_parts, extract_database_table_record,
    create_engine, extract_database_table_names, screeners_tables_names
)
from crypto_screening.screeners.collectors.base import ScreenersDataCollector

__all__ = [
    "DatabaseScreenersDataCollector"
]

Data = list[tuple[str | float | dt.datetime, dict[str, str | float | bool | None]]]
TimeDuration = float | dt.timedelta

class DatabaseScreenersDataCollector(ScreenersDataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - screeners:
        The screener object to control and fill with data.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - screeners:
        The screener object to control and fill with data.

    - database:
        The path to the database.

    - engine:
        The engine object for the database.
    """

    def __init__(
            self,
            database: str,
            engine: Engine = None,
            tables: Iterable[str] = None,
            screeners: Iterable[BaseScreener] = None,
            location: str = None,
            cancel: TimeDuration = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param database: The path to the database.
        :param engine: The engine for the database.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(
            screeners=screeners, location=location,
            cancel=cancel, delay=delay
        )

        self.database = database

        self.engine = engine or create_engine(self.database)

        if isinstance(self.engine, Engine):
            self._connected = True

        self._session: Session | None = None

        if not tables:
            all_tables = extract_database_table_names(self.engine)

        else:
            all_tables = ()

        self.tables = extract_database_table_parts(
            tables or [
                table for table in
                screeners_tables_names(self.screeners).values()
                if table in all_tables
            ]
        )

        self.failed_tables: dict[str, list[Exception]] = {}

    def screening_loop(self) -> None:
        """Runs the process of the price screening."""

        self._screening = True

        while self.screening:
            for table, (name, exchange, symbol, interval) in self.tables.items():
                try:
                    dataset = extract_database_table_record(
                        table=table, engine=self.engine, length=1
                    )

                    # noinspection PyTypeChecker
                    data: Data = list(
                        (index, row.to_dict())
                        for index, row in dataset.iterrows()
                    )

                    self.collect(
                        dict(
                            data=data, name=name, exchange=exchange,
                            symbol=symbol, interval=interval
                        )
                    )

                except Exception as e:
                    self.failed_tables.setdefault(table, []).append(e)

                    self.exception(exception=e, data=(name, exchange, symbol, interval))
