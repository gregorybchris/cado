import logging
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from cado.app.disk import save_notebook
from cado.app.message import ErrorResponse, MessageType
from cado.app.response import process_message
from cado.app.session_state import SessionState

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

    session_state = SessionState()

    try:
        while True:
            message_json = await socket.receive_json()
            try:
                message_type = MessageType.from_str(message_json["type"])
                logger.info("Received client message: %s", message_json)
                response = process_message(message_type, message_json, session_state)
                response_json = response.json()
                logger.info("Sending server message: %s", response_json)
                await socket.send_json(response_json)
            # pylint: disable=broad-exception-caught
            except Exception as exc:
                logger.error("Exception raised during cado session loop")
                logger.error("Traceback: %s", traceback.format_exc())
                response = ErrorResponse(error=str(exc))
                response_json = response.json()
                logger.info("Sending server message: %s", response_json)
                await socket.send_json(response_json)
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
        save_notebook(session_state)


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
