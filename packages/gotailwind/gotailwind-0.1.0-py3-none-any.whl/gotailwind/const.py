"""Asynchronous Python client for Tailwind garage door openeners."""

from enum import StrEnum, auto

OPERATION_WAIT_CYCLES = 120
OPERATION_CYCLE_WAIT = 0.5


class TailwindDoorState(StrEnum):
    """Enum for door state."""

    CLOSED = "close"
    OPEN = "open"


class TailwindDoorOperationCommand(StrEnum):
    """Enum for door operation."""

    CLOSE = auto()
    OPEN = auto()


class TailwindResponseResult(StrEnum):
    """Enum for different response types."""

    OK = "OK"
    ERROR = "Fail"
    AUTH_ERROR = "token fail"


class TailwindRequestType(StrEnum):
    """Enum for different request types."""

    SET = "set"
    GET = "get"
