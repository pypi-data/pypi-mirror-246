# database.py

import datetime as dt
from typing import Any

from sqlalchemy.orm.session import Session

from crypto_screening.screeners.database import (
    create_engine, parts_to_database_table_name, DATATYPES,
    extract_database_table_names, create_engine_session, Engine,
    insert_database_record_rows
)
from crypto_screening.screeners.callbacks.base import BaseCallback

__all__ = [
    "DatabaseCallback"
]

TimeDuration = float | dt.timedelta

class DatabaseCallback(BaseCallback):
    """A class to represent a callback."""

    CONNECTABLE: bool = True

    DATATYPES = DATATYPES

    def __init__(
            self,
            database: str,
            engine: Engine = None,
            key: Any = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param database: The path to the database.
        :param engine: The engine for the database.
        :param key: The key od the data.
        :param delay: The delay in handling.
        """

        super().__init__(key=key, delay=delay)

        self.database = database

        self.engine = engine

        if isinstance(self.engine, Engine):
            self._connected = True

        self._session: Session | None = None

        self.tables: dict[tuple[str, str, str, str | None], str] = {}
        self.table_names: set[str] | None = None

    async def handle(
            self,
            data: dict[str, Any],
            timestamp: float,
            key: Any = None
    ) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        key, exchange, symbol, interval = (
            key or self.key, data[self.EXCHANGE],
            data[self.SYMBOL], data.get(self.INTERVAL, None)
        )

        table = None

        if (key, exchange, symbol, interval) not in self.tables:
            table = parts_to_database_table_name(
                name=key, exchange=exchange,
                symbol=symbol, interval=interval
            )

            self.tables[(key, exchange, symbol, interval)] = table

        insert_database_record_rows(
            engine=self.engine, session=self._session,
            tables=self.table_names, data=data[self.DATA],
            exchange=exchange, symbol=symbol, create=True,
            name=key, interval=interval, commit=True
        )

        if table is not None:
            self.table_names.add(table)

        if data[self.DATA]:
            return True

        else:
            return False

    async def start(self) -> None:
        """Connects to the socket service."""

        self.engine = self.engine or create_engine(self.database)

        self.table_names = (
            self.table_names or
            extract_database_table_names(engine=self.engine)
        )

        self._session = (
            self._session or
            create_engine_session(engine=self.engine)
        )
