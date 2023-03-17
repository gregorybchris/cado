import logging
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from cado.app.example import load_example_notebook

from cado.app.message import (
    ClearCell,
    DeleteCell,
    DeleteNotebook,
    ErrorResponse,
    ExitNotebook,
    GetNotebook,
    GetNotebookResponse,
    ListNotebooks,
    ListNotebooksResponse,
    Message,
    MessageType,
    NewCell,
    NewNotebook,
    OpenNotebook,
    ReorderCells,
    RunCell,
    UpdateCellCode,
    UpdateCellInputNames,
    UpdateCellLanguage,
    UpdateCellOutputName,
    UpdateNotebookName,
)
from cado.core.notebook import Notebook
from cado.core.notebook_details import NotebookDetails

logger = logging.getLogger(__name__)

router = APIRouter()


@dataclass
class SessionState:
    notebook: Optional[Notebook] = None
    filepath: Optional[Path] = None


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
                logger.info("Got message: %s", message_json)

                response = process_message(message_type, message_json, session_state)
                await socket.send_json(response.json())
            # pylint: disable=broad-exception-caught
            except Exception as exc:
                logger.error("Exception raised during cado session loop")
                logger.error("Traceback: %s", traceback.format_exc())
                response = ErrorResponse(error=str(exc))
                await socket.send_json(response.json())
    except WebSocketDisconnect:
        logger.info("Websocket disconnected")
        save_notebook(session_state)


def process_message(
    message_type: MessageType,
    message_json: Any,
    session_state: SessionState,
) -> Message:
    notebook = session_state.notebook
    notebook_messages = [
        MessageType.LIST_NOTEBOOKS,
        MessageType.OPEN_NOTEBOOK,
        MessageType.GET_NOTEBOOK,
        MessageType.NEW_NOTEBOOK,
        MessageType.DELETE_NOTEBOOK,
    ]
    if notebook is None and message_type not in notebook_messages:
        return ErrorResponse(error=f"Can't process {message_type}, no active notebook")

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
    elif message_type == MessageType.UPDATE_CELL_LANGUAGE:
        update_cell_language = UpdateCellLanguage.parse_obj(message_json)
        notebook.update_cell_language(update_cell_language.cell_id, update_cell_language.language)
    elif message_type == MessageType.REORDER_CELLS:
        reorder_cells = ReorderCells.parse_obj(message_json)
        notebook.reorder_cells(reorder_cells.cell_ids)
    elif message_type == MessageType.LIST_NOTEBOOKS:
        ListNotebooks.parse_obj(message_json)
        details = list_local_notebooks()
        return ListNotebooksResponse(notebook_details=details)
    elif message_type == MessageType.OPEN_NOTEBOOK:
        open_notebook = OpenNotebook.parse_obj(message_json)
        session_state.notebook = Notebook.from_filepath(open_notebook.filepath)
        session_state.filepath = open_notebook.filepath
    elif message_type == MessageType.EXIT_NOTEBOOK:
        ExitNotebook.parse_obj(message_json)
        session_state.notebook = None
        session_state.filepath = None
    elif message_type == MessageType.UPDATE_NOTEBOOK_NAME:
        update_notebook_name = UpdateNotebookName.parse_obj(message_json)
        notebook.name = update_notebook_name.name
    elif message_type == MessageType.NEW_NOTEBOOK:
        NewNotebook.parse_obj(message_json)
        create_new_notebook(session_state)
    elif message_type == MessageType.DELETE_NOTEBOOK:
        delete_notebook = DeleteNotebook.parse_obj(message_json)
        delete_existing_notebook(delete_notebook.filepath)
        details = list_local_notebooks()
        return ListNotebooksResponse(notebook_details=details)
    else:
        logger.error("Request type did not match any known message types")
        return ErrorResponse(error=f"Unknown message type from client: {message_type}")

    save_notebook(session_state)

    return GetNotebookResponse(notebook=session_state.notebook)


def save_notebook(session_state: SessionState):
    notebook = session_state.notebook
    if notebook is None:
        logger.info("Not saving notebook to file, notebook was None")
        return

    filepath = session_state.filepath
    if filepath is None:
        logger.info("Not saving notebook to file, filepath was None")
        return

    notebook.set_updated_time()
    logger.info("Saving notebook to file: %s", filepath)
    notebook.to_filepath(filepath)


def create_new_notebook(session_state: SessionState) -> None:
    cwd = Path.cwd()
    for i in range(1, 100):
        name = "notebook" if i == 1 else f"notebook-{i}"
        filename = f"{name}.cado"
        filepath = cwd / filename
        if not filepath.exists():
            notebook = Notebook(name=name)
            notebook.add_cell()
            notebook.to_filepath(filepath)
            session_state.filepath = filepath
            session_state.notebook = notebook
            return
    raise ValueError("Could not create a new notebook, found too many existing new notebooks")


def delete_existing_notebook(filepath: Path) -> None:
    filepath.unlink()


def list_local_notebooks() -> List[NotebookDetails]:
    details = []
    cwd = Path.cwd()
    for path in cwd.iterdir():
        if path.is_file():
            if str(path).endswith(".cado"):
                details.append(NotebookDetails.from_filepath(path))

    if len(details) == 0:
        filename = "example.cado"
        filepath = cwd / filename
        notebook = load_example_notebook(filename)
        notebook.to_filepath(filepath)
        details.append(NotebookDetails.from_filepath(filepath))

    return details


@router.get(path="/status")
def get_status() -> JSONResponse:
    """Endpoint for app status."""
    logger.info("GET app status")
    return JSONResponse({
        'status': 'healthy',
    })
