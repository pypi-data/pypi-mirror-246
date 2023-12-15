# base.py

import os
from pathlib import Path

__all__ = [
    "root",
    "source",
    "data"
]

def root() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    try:
        if os.getcwd() in os.environ['VIRTUAL_ENV']:
            path = Path(__file__).parent.parent

        else:
            raise KeyError

    except KeyError:
        if os.getcwd() not in (
            path := str(Path(__file__).parent.parent)
        ):
            path = os.getcwd()

    return str(path)

def source() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    return str(Path(root()) / Path("source"))

def data() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    return str(Path(source()) / Path("data"))
