import logging
import traceback
from pathlib import Path

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from cado.app.example import load_example_notebook

from cado.app.message import (DeleteCell, ErrorResponse, GetNotebook, GetNotebookResponse, MessageType, NewCell,
                              RunCell, UpdateCellCode, UpdateCellInputNames, UpdateCellOutputName, GetCellResponse)
from cado.core.cell import Cell
from cado.core.cell_status import CellStatus
from cado.core.notebook import Notebook

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket(path="/stream")
async def stream_api(socket: WebSocket) -> None:
    """Websocket endpoint for streaming commands."""
    logger.info("Starting connection...")

    await socket.accept()
    logger.info("Connection open")

    try:
        # TODO: Make filepath configurable
        filepath = Path("./notebook.cado")
        logger.info(f"Reading notebook from file: {filepath}")
        notebook = Notebook.from_filepath(filepath)
    except Exception as exc:
        logger.error(f"Could not load notebook from file {filepath}: {str(exc)}")
        notebook = load_example_notebook()

    try:
        while True:
            message_json = await socket.receive_json()
            try:
                message_type = MessageType.from_str(message_json["type"])
                logger.info("Got message: %s", message_json)

                if message_type == MessageType.GET_NOTEBOOK:
                    message = GetNotebook.parse_obj(message_json)
                    response = GetNotebookResponse(notebook=notebook)
                    await socket.send_json(response.json())
                elif message_type == MessageType.UPDATE_CELL_CODE:
                    message = UpdateCellCode.parse_obj(message_json)
                    cell = notebook.get_cell(message.cell_id)
                    cell.set_code(message.code)
                    response = GetCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.UPDATE_CELL_OUTPUT_NAME:
                    message = UpdateCellOutputName.parse_obj(message_json)
                    notebook.update_cell_output_name(message.cell_id, message.output_name)
                    cell = notebook.get_cell(message.cell_id)
                    response = GetCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.RUN_CELL:
                    message = RunCell.parse_obj(message_json)
                    cell = notebook.get_cell(message.cell_id)
                    cell.run()
                    response = GetCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.CLEAR_CELL:
                    message = RunCell.parse_obj(message_json)
                    cell = notebook.get_cell(message.cell_id)
                    cell.clear()
                    cell.set_status(CellStatus.EXPIRED)
                    response = GetCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.NEW_CELL:
                    message = NewCell.parse_obj(message_json)
                    new_cell = Cell(output_name="")
                    logger.info("New cell created: %s", new_cell)
                    notebook.add_cell(new_cell)
                    response = GetCellResponse(cell=new_cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.DELETE_CELL:
                    message = DeleteCell.parse_obj(message_json)
                    notebook.delete_cell(message.cell_id)
                    response = GetNotebookResponse(notebook=notebook)
                    await socket.send_json(response.json())
                elif message_type == MessageType.UPDATE_CELL_INPUT_NAMES:
                    message = UpdateCellInputNames.parse_obj(message_json)
                    notebook.update_cell_input_names(message.cell_id, message.input_names)
                    cell = notebook.get_cell(message.cell_id)
                    response = GetCellResponse(cell=cell)
                    await socket.send_json(response.json())
                else:
                    logger.error("Request type did not match any known message types")
            except Exception as exc:
                logger.error("Exception raised during session loop")
                logger.error("Traceback: %s", traceback.format_exc())
                response = ErrorResponse(error=str(exc))
                await socket.send_json(response.json())
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
        # TODO: Make filepath configurable
        filepath = Path("./notebook.cado")
        logger.info(f"Writing notebook to file: {filepath}")
        notebook.to_filepath(filepath)


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
