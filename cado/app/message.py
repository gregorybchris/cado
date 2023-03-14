from enum import Enum
from typing import List

from pydantic import BaseModel

from cado.core.cell import Cell


class MessageType(Enum):
    # publish
    GET_CELLS = "get-cells"
    UPDATE_CELL_CODE = "update-cell-code"
    UPDATE_CELL_NAME = "update-cell-name"
    RUN_CELL = "run-cell"
    NEW_CELL = "new-cell"
    DELETE_CELL = "delete-cell"

    # subscribe
    GET_CELLS_RESPONSE = "get-cells-response"
    UPDATE_CELL_RESPONSE = "update-cell-response"
    RUN_CELL_RESPONSE = "run-cell-response"
    NEW_CELL_RESPONSE = "new-cell-response"
    ERROR_RESPONSE = "error-response"

    @classmethod
    def from_str(cls, message_name: str) -> 'MessageType':
        for _, enum_value in cls.__members__.items():
            if enum_value.value == message_name:
                return enum_value
        raise ValueError(f"Unknown message type '{message_name}'")


class Message(BaseModel):
    type: MessageType


# region: publish


class GetCells(Message):
    type = MessageType.GET_CELLS


class UpdateCellCode(Message):
    cell_id: str
    code: str
    type = MessageType.UPDATE_CELL_CODE


class UpdateCellName(Message):
    cell_id: str
    name: str
    type = MessageType.UPDATE_CELL_NAME


class RunCell(Message):
    cell_id: str
    type = MessageType.RUN_CELL


class NewCell(Message):
    type = MessageType.NEW_CELL


class DeleteCell(Message):
    cell_id: str
    type = MessageType.DELETE_CELL


# endregion: publish

# region: subscribe


class GetCellsResponse(Message):
    cells: List[Cell]
    type = MessageType.GET_CELLS_RESPONSE


class UpdateCellResponse(Message):
    cell: Cell
    type = MessageType.UPDATE_CELL_RESPONSE


class RunCellResponse(Message):
    cell: Cell
    type = MessageType.RUN_CELL_RESPONSE


class NewCellResponse(Message):
    cell_id: str
    type = MessageType.NEW_CELL_RESPONSE


class ErrorResponse(Message):
    error: str
    type = MessageType.ERROR_RESPONSE


# endregion: subscribe
