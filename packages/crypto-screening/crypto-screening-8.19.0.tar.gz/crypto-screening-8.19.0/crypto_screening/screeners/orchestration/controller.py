# controller.py

import json
import socket
from typing import Any

from represent import represent

from crypto_screening.screeners.orchestration.responses import (
    ServiceResponse, load_response
)
from crypto_screening.screeners.orchestration.requests import (
    RunRequest, StopRequest, UpdateRequest,
    PauseRequest, UnpauseRequest, ConfigRequest
)

__all__ = [
    "DataPublisherController"
]

Connection = socket.socket
Address = tuple[str, int]
Data = bytes | str | dict[str, str]

@represent
class DataPublisherController:
    """A class to represent arbitrage events receiver client."""

    def __init__(
            self,
            config: dict[str, Any] = None,
            running: bool = False,
            paused: bool = False
    ) -> None:
        """
        Defines the data of the server-side client.

        :param paused: The value to pause the data receiving.
        """

        if config is None:
            config = {}

        self._paused = paused
        self._running = running
        self._config = config

        self.responses: list[ServiceResponse] = []

    @property
    def paused(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._paused

    @property
    def running(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self._running

    @property
    def local_config(self) -> dict[str, Any]:
        """
        returns the value of config data.

        :return: The value.
        """

        return self._config

    @staticmethod
    def receive(data: Data) -> ServiceResponse | None:
        """
        Collects the data into the record of arbitrage events.

        :param data: The data from the server.

        :return: The error responses.
        """

        if not data:
            return

        if isinstance(data, bytes):
            data = data.decode()

        if isinstance(data, str):
            data = json.loads(data)

        try:
            return load_response(data)

        except json.decoder.JSONDecodeError:
            raise ValueError(
                f"JSON incompatible data received from server: {data}"
            )

        except ValueError as e:
            raise e

    def register(self, data: bytes) -> ServiceResponse | None:
        """
        Collects the data into the record of arbitrage events.

        :param data: The data from the server.

        :return: The error responses.
        """

        if not data:
            return

        response = self.receive(data)

        self.responses.append(response)

        return response

    @staticmethod
    def config() -> bytes:
        """
        Requests the data.

        :return: The bytes stream to send to the server as a request.
        """

        return json.dumps(ConfigRequest().json()).encode()

    def pause(self) -> bytes:
        """
        Pauses the data receiving.

        :return: The bytes stream to send to the server as a request.
        """

        self._paused = True

        return json.dumps(PauseRequest().json()).encode()

    def unpause(self) -> bytes:
        """
        Unpauses the data receiving.

        :return: The bytes stream to send to the server as a request.
        """

        self._paused = False

        return json.dumps(UnpauseRequest().json()).encode()

    def run(self) -> bytes:
        """
        Runs the data publishing process.

        :return: The bytes stream to send to the server as a request.
        """

        self._running = True

        return json.dumps(RunRequest().json()).encode()

    def stop(self) -> bytes:
        """
        Runs the data publishing process.

        :return: The bytes stream to send to the server as a request.
        """

        self._running = False

        return json.dumps(StopRequest().json()).encode()

    def update(self, config: dict[str, Any]) -> bytes:
        """
        Updates the configuration of the market of the data publisher.

        :return: The bytes stream to send to the server as a request.
        """

        self._config.update(config)

        return json.dumps(UpdateRequest(config).json()).encode()
