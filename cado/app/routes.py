import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from cado.app.message import Message

router = APIRouter()

logger = logging.getLogger(__name__)


@router.websocket(path="/stream")
async def stream_api(socket: WebSocket) -> None:
    """Websocket endpoint for streaming commands."""
    logger.info("Starting connection...")

    await socket.accept()
    logger.info("Connection open")

    try:
        while True:
            message_json = await socket.receive_json()
            message = Message.parse(message_json)

            logger.info("Got message: %s", message)

            response = {"message": "hello"}
            await socket.send_json(response)
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
