from enum import Enum


class CellStatus(Enum):
    OK = "ok"
    EXPIRED = "expired"
    RUNNING = "running"
    ERROR = "error"
