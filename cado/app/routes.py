import logging
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from cado.app.message import (ClearCellResponse, ErrorResponse, GetNotebook, GetNotebookResponse, MessageType, NewCell,
                              NewCellResponse, RunCell, RunCellResponse, UpdateCellCode, UpdateCellOutputName,
                              UpdateCellResponse)
from cado.core.cell import Cell
from cado.core.notebook import Notebook

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket(path="/stream")
async def stream_api(socket: WebSocket) -> None:
    """Websocket endpoint for streaming commands."""
    logger.info("Starting connection...")

    await socket.accept()
    logger.info("Connection open")

    # TODO: Use Notebook class as storage for cells
    # TODO: Load notebook from file

    EXAMPLE_CODE = "def add_one(a):\n    return a + 1\n\na = 5 + add_one(4)\n\nfor i in range(5):\n    a += 2"
    example_cell = Cell(output_name="a", code=EXAMPLE_CODE)
    notebook = Notebook(filepath="")
    notebook.add_cell(example_cell)

    try:
        while True:
            try:
                message_json = await socket.receive_json()
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
                    response = UpdateCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.UPDATE_CELL_OUTPUT_NAME:
                    message = UpdateCellOutputName.parse_obj(message_json)
                    cell = notebook.get_cell(message.cell_id)
                    cell.set_output_name(message.output_name)
                    response = UpdateCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.RUN_CELL:
                    message = RunCell.parse_obj(message_json)
                    cell = notebook.get_cell(message.cell_id)
                    cell.run()
                    response = RunCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.CLEAR_CELL:
                    message = RunCell.parse_obj(message_json)
                    cell = notebook.get_cell(message.cell_id)
                    cell.clear()
                    response = ClearCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.NEW_CELL:
                    message = NewCell.parse_obj(message_json)
                    new_cell = Cell(output_name="a")
                    logger.info("New cell created: %s", new_cell)
                    notebook.add_cell(new_cell)
                    response = NewCellResponse(cell=new_cell)
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
        # TODO: Save to file


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
