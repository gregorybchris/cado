from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel

from cado.core.cell import Cell
from cado.core.language import Language
from cado.core.notebook import Notebook


class MessageType(Enum):
    # publish
    GET_NOTEBOOK = "get-notebook"
    UPDATE_CELL_CODE = "update-cell-code"
    UPDATE_CELL_OUTPUT_NAME = "update-cell-output-name"
    UPDATE_CELL_INPUT_NAMES = "update-cell-input-names"
    UPDATE_CELL_LANGUAGE = "update-cell-language"
    RUN_CELL = "run-cell"
    CLEAR_CELL = "clear-cell"
    NEW_CELL = "new-cell"
    DELETE_CELL = "delete-cell"
    REORDER_CELLS = "reorder-cells"

    # subscribe
    GET_NOTEBOOK_RESPONSE = "get-notebook-response"
    GET_CELL_RESPONSE = "get-cell-response"
    ERROR_RESPONSE = "error-response"

    @classmethod
    def from_str(cls, message_name: str) -> 'MessageType':
        """Parse MessageType from string.

        Args:
            message_name (str): Name of message type to parse.

        Raises:
            ValueError: If the name was not a valid message type.

        Returns:
            MessageType: The parsed MessageType.
        """
        for _, enum_value in cls.__members__.items():
            if enum_value.value == message_name:
                return enum_value
        raise ValueError(f"Unknown message type '{message_name}'")


class Message(BaseModel):
    type: MessageType


# region: publish


class GetNotebook(Message):
    type: MessageType = MessageType.GET_NOTEBOOK


class UpdateCellCode(Message):
    cell_id: UUID
    code: str
    type: MessageType = MessageType.UPDATE_CELL_CODE


class UpdateCellOutputName(Message):
    cell_id: UUID
    output_name: str
    type: MessageType = MessageType.UPDATE_CELL_OUTPUT_NAME


class UpdateCellInputNames(Message):
    cell_id: UUID
    input_names: List[str]
    type: MessageType = MessageType.UPDATE_CELL_INPUT_NAMES


class UpdateCellLanguage(Message):
    cell_id: UUID
    language: Language
    type: MessageType = MessageType.UPDATE_CELL_LANGUAGE


class RunCell(Message):
    cell_id: UUID
    type: MessageType = MessageType.RUN_CELL


class ClearCell(Message):
    cell_id: UUID
    type: MessageType = MessageType.CLEAR_CELL


class NewCell(Message):
    type: MessageType = MessageType.NEW_CELL


class DeleteCell(Message):
    cell_id: UUID
    type: MessageType = MessageType.DELETE_CELL


class ReorderCells(Message):
    cell_ids: List[UUID]
    type: MessageType = MessageType.REORDER_CELLS


# endregion: publish

# region: subscribe


class GetNotebookResponse(Message):
    notebook: Notebook
    type: MessageType = MessageType.GET_NOTEBOOK_RESPONSE


class GetCellResponse(Message):
    cell: Cell
    type: MessageType = MessageType.GET_CELL_RESPONSE


class ErrorResponse(Message):
    error: str
    type: MessageType = MessageType.ERROR_RESPONSE


# endregion: subscribe
