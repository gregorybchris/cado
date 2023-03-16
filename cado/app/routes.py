import logging
import traceback
from pathlib import Path
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from cado.app.example import load_example_notebook

from cado.app.message import (
    ClearCell,
    DeleteCell,
    ErrorResponse,
    GetNotebook,
    GetNotebookResponse,
    Message,
    MessageType,
    NewCell,
    ReorderCells,
    RunCell,
    UpdateCellCode,
    UpdateCellInputNames,
    UpdateCellLanguage,
    UpdateCellOutputName,
)
from cado.core.notebook import Notebook

logger = logging.getLogger(__name__)

router = APIRouter()


# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
@router.websocket(path="/stream")
async def stream_api(socket: WebSocket) -> None:
    """Websocket endpoint for streaming commands."""
    logger.info("Starting connection...")

    await socket.accept()
    logger.info("Connection open")

    try:
        # TODO: Make filepath configurable
        filepath = Path("./notebook.cado")
        logger.info("Reading notebook from file: %s", filepath)
        notebook = Notebook.from_filepath(filepath)
    # pylint: disable=broad-exception-caught
    except Exception as exc:
        logger.error("Could not load notebook from file %s: %s", filepath, str(exc))
        example_name = "sum"
        logger.error("Using example notebook %s.cado", example_name)
        notebook = load_example_notebook(example_name)

    try:
        while True:
            message_json = await socket.receive_json()
            try:
                message_type = MessageType.from_str(message_json["type"])
                logger.info("Got message: %s", message_json)

                response = _get_response(message_type, message_json, notebook)
                await socket.send_json(response.json())
            # pylint: disable=broad-exception-caught
            except Exception as exc:
                logger.error("Exception raised during session loop")
                logger.error("Traceback: %s", traceback.format_exc())
                response = ErrorResponse(error=str(exc))
                await socket.send_json(response.json())
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
        # TODO: Make filepath configurable
        filepath = Path("./notebook.cado")
        logger.info("Writing notebook to file: %s", filepath)
        notebook.to_filepath(filepath)


def _get_response(message_type: MessageType, message_json: Any, notebook: Notebook) -> Message:
    if message_type == MessageType.GET_NOTEBOOK:
        GetNotebook.parse_obj(message_json)
    elif message_type == MessageType.UPDATE_CELL_CODE:
        update_cell_code = UpdateCellCode.parse_obj(message_json)
        notebook.set_cell_code(update_cell_code.cell_id, update_cell_code.code)
    elif message_type == MessageType.UPDATE_CELL_OUTPUT_NAME:
        update_cell_output_name = UpdateCellOutputName.parse_obj(message_json)
        notebook.update_cell_output_name(update_cell_output_name.cell_id, update_cell_output_name.output_name)
    elif message_type == MessageType.RUN_CELL:
        run_cell = RunCell.parse_obj(message_json)
        notebook.run_cell(run_cell.cell_id)
    elif message_type == MessageType.CLEAR_CELL:
        clear_cell = ClearCell.parse_obj(message_json)
        notebook.clear_cell(clear_cell.cell_id)
    elif message_type == MessageType.NEW_CELL:
        NewCell.parse_obj(message_json)
        notebook.add_cell()
    elif message_type == MessageType.DELETE_CELL:
        delete_cell = DeleteCell.parse_obj(message_json)
        notebook.delete_cell(delete_cell.cell_id)
    elif message_type == MessageType.UPDATE_CELL_INPUT_NAMES:
        update_cell_input_names = UpdateCellInputNames.parse_obj(message_json)
        notebook.update_cell_input_names(update_cell_input_names.cell_id, update_cell_input_names.input_names)
        return GetNotebookResponse(notebook=notebook)
    elif message_type == MessageType.UPDATE_CELL_LANGUAGE:
        update_cell_language = UpdateCellLanguage.parse_obj(message_json)
        notebook.update_cell_language(update_cell_language.cell_id, update_cell_language.language)
        return GetNotebookResponse(notebook=notebook)
    elif message_type == MessageType.REORDER_CELLS:
        reorder_cells = ReorderCells.parse_obj(message_json)
        notebook.reorder_cells(reorder_cells.cell_ids)
        return GetNotebookResponse(notebook=notebook)
    else:
        logger.error("Request type did not match any known message types")
        return ErrorResponse(error=f"Unknown message type from client: {message_type}")
    return GetNotebookResponse(notebook=notebook)


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
