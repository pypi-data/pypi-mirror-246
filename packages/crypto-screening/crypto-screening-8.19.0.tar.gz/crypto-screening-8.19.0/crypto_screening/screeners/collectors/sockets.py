# sockets.py

import time
import json
import warnings
import asyncio
import datetime as dt
from typing import Iterable

from socketsio import find_available_port

from crypto_screening.screeners.callbacks import SocketCallback, BaseCallback
from crypto_screening.foundation.screener import BaseScreener
from crypto_screening.screeners.collectors.base import ScreenersDataCollector

__all__ = [
    "SocketScreenersDataCollector",
    "SocketCallback"
]

TimeDuration = float | dt.timedelta

class SocketScreenersDataCollector(ScreenersDataCollector):
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

    - address:
        The host for the socket connection.

    - port:
        The port for the socket connection.
    """

    BUFFER = SocketCallback.BUFFER

    def __init__(
            self,
            address: str = None,
            port: int = None,
            buffer: int = None,
            screeners: Iterable[BaseScreener] = None,
            location: str = None,
            cancel: TimeDuration = None,
            delay: TimeDuration = None
    ) -> None:
        """
        Defines the class attributes.

        :param address: The address for the socket.
        :param port: The port for the socket.
        :param buffer: The buffer size.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(
            screeners=screeners, location=location,
            cancel=cancel, delay=delay
        )

        if address is None:
            address = "127.0.0.1"

        if port is None:
            port = find_available_port(address)

        self.address = address
        self.port = port
        self.buffer = buffer or self.BUFFER

        self.loop: asyncio.AbstractEventLoop | None = None

        self._data: list[str] = []

        self.chunks: dict[str, list[tuple[int, str]]] = {}
        self.fail_record: dict[str, list[tuple[str, Exception]]] = {}

    async def receive(
            self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """
        Receives the data from the senders.

        :param reader: The data reader.
        :param writer: The data writer.
        """

        data = (await reader.read(self.buffer)).decode()

        try:
            payloads = json.loads(f"[{', '.join(data.split('}{'))}]")

            complete = False

            for payload in payloads:
                if payload[SocketCallback.FORMAT] == SocketCallback.CHUNKED_FORMAT:
                    key = payload[SocketCallback.ID]

                    chunks: list[tuple[int, str]] = self.chunks.setdefault(key, [])
                    chunks.append((payload[SocketCallback.PART], payload[BaseCallback.DATA]))

                    if len(chunks) == payload[SocketCallback.CHUNKS]:
                        payload = json.loads(
                            ''.join(
                                parts[1] for parts in
                                sorted(chunks, key=lambda pair: pair[0])
                            )
                        )

                        self.chunks.pop(key)

                        complete = True

                else:
                    complete = True

                if complete:
                    packet = payload[BaseCallback.DATA]

                    self.collect(
                        dict(
                            name=payload[SocketCallback.KEY],
                            data=packet[BaseCallback.DATA],
                            exchange=packet[BaseCallback.EXCHANGE],
                            symbol=packet[BaseCallback.SYMBOL],
                            interval=packet[BaseCallback.INTERVAL]
                        )
                    )

        except Exception as e:
            self.fail_record.setdefault(
                writer.get_extra_info('peername'), []
            ).append((data, e))

            self.exception(exception=e, data=data)

    async def receiving_loop(
            self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """
        Receives the data from the senders.

        :param reader: The data reader.
        :param writer: The data writer.
        """

        while self.screening:
            try:
                await self.receive(reader=reader, writer=writer)

            except (
                ConnectionResetError, ConnectionError,
                ConnectionAbortedError, ConnectionRefusedError
            ) as e:
                warnings.warn(str(e))

                self.stop()

    def screening_loop(self, loop: asyncio.AbstractEventLoop = None) -> None:
        """
        Runs the process of the price screening.

        :param loop: The event loop.
        """

        if loop is None:
            loop = asyncio.new_event_loop()

        self.loop = loop

        asyncio.set_event_loop(loop)

        async def run() -> None:
            """Runs the program to receive data."""

            server = await asyncio.start_server(
                self.receiving_loop, self.address, self.port
            )

            await server.serve_forever()

        self._screening = True

        asyncio.run(run())

    def stop_screening(self) -> None:
        """Stops the screening process."""

        if not isinstance(self.loop, asyncio.AbstractEventLoop):
            return

        super().stop_screening()

        self.loop: asyncio.AbstractEventLoop

        for task in asyncio.all_tasks(self.loop):
            task.cancel()

        self.loop.stop()

        while self.loop.is_running():
            time.sleep(0.001)

        try:
            self.loop.close()

        except (AttributeError, RuntimeError):
            pass

        self.loop = None
