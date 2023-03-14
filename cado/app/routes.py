import logging
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from cado.app.message import (ErrorResponse, GetCells, GetCellsResponse, MessageType, RunCell, RunCellResponse,
                              UpdateCellCode, UpdateCellName, UpdateCellResponse)
from cado.core.cell import Cell

router = APIRouter()

logger = logging.getLogger(__name__)


@router.websocket(path="/stream")
async def stream_api(socket: WebSocket) -> None:
    """Websocket endpoint for streaming commands."""
    logger.info("Starting connection...")

    await socket.accept()
    logger.info("Connection open")

    INITIAL_CODE = "def add_one(a):\n    return a + 1\n\na = 5 + add_one(4)\n\nfor i in range(5):\n    a += 2"
    cells = {
        "1234": Cell(name="a", id="1234", code=INITIAL_CODE),
    }

    try:
        while True:
            try:
                message_json = await socket.receive_json()
                message_type = MessageType.from_str(message_json["type"])
                logger.info("Got message: %s", message_json)

                if message_type == MessageType.GET_CELLS:
                    message = GetCells.parse_obj(message_json)
                    response = GetCellsResponse(cells=list(cells.values()))
                    await socket.send_json(response.json())
                elif message_type == MessageType.UPDATE_CELL_CODE:
                    message = UpdateCellCode.parse_obj(message_json)
                    cell = cells[message.cell_id]
                    cell.set_code(message.code)
                    response = UpdateCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.UPDATE_CELL_NAME:
                    message = UpdateCellName.parse_obj(message_json)
                    cell = cells[message.cell_id]
                    cell.set_name(message.name)
                    response = UpdateCellResponse(cell=cell)
                    await socket.send_json(response.json())
                elif message_type == MessageType.RUN_CELL:
                    message = RunCell.parse_obj(message_json)
                    cell = cells[message.cell_id]
                    cell.run()
                    response = RunCellResponse(cell=cell)
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


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
