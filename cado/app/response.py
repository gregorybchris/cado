import logging
from typing import Any
from cado.app.disk import create_new_notebook, delete_existing_notebook, list_local_notebooks, save_notebook

from cado.app.message import (ClearCell, DeleteCell, DeleteNotebook, ErrorResponse, ExitNotebook, GetNotebook,
                              GetNotebookResponse, ListNotebooks, ListNotebooksResponse, Message, MessageType, NewCell,
                              NewNotebook, OpenNotebook, ReorderCells, RunCell, UpdateCellCode, UpdateCellInputNames,
                              UpdateCellLanguage, UpdateCellOutputName, UpdateNotebookName)
from cado.app.session_state import SessionState
from cado.core.notebook import Notebook

logger = logging.getLogger(__name__)


# pylint: disable=too-many-locals
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def process_message(
    message_type: MessageType,
    message_json: Any,
    session_state: SessionState,
) -> Message:
    """Process a request message from the client, update the session state, and return a response message.

    Args:
        message_type (MessageType): Type of request message.
        message_json (Any): Raw request message object.
        session_state (SessionState): Current session state.

    Returns:
        Message: A response message.
    """
    notebook = session_state.notebook

    if message_type == MessageType.GET_NOTEBOOK:
        GetNotebook.parse_obj(message_json)
    elif message_type == MessageType.UPDATE_CELL_CODE:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        update_cell_code = UpdateCellCode.parse_obj(message_json)
        notebook.set_cell_code(update_cell_code.cell_id, update_cell_code.code)
    elif message_type == MessageType.UPDATE_CELL_OUTPUT_NAME:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        update_cell_output_name = UpdateCellOutputName.parse_obj(message_json)
        notebook.update_cell_output_name(update_cell_output_name.cell_id, update_cell_output_name.output_name)
    elif message_type == MessageType.RUN_CELL:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        run_cell = RunCell.parse_obj(message_json)
        notebook.run_cell(run_cell.cell_id)
    elif message_type == MessageType.CLEAR_CELL:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        clear_cell = ClearCell.parse_obj(message_json)
        notebook.clear_cell(clear_cell.cell_id)
    elif message_type == MessageType.NEW_CELL:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        NewCell.parse_obj(message_json)
        notebook.add_cell()
    elif message_type == MessageType.DELETE_CELL:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        delete_cell = DeleteCell.parse_obj(message_json)
        notebook.delete_cell(delete_cell.cell_id)
    elif message_type == MessageType.UPDATE_CELL_INPUT_NAMES:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        update_cell_input_names = UpdateCellInputNames.parse_obj(message_json)
        notebook.update_cell_input_names(update_cell_input_names.cell_id, update_cell_input_names.input_names)
    elif message_type == MessageType.UPDATE_CELL_LANGUAGE:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        update_cell_language = UpdateCellLanguage.parse_obj(message_json)
        notebook.update_cell_language(update_cell_language.cell_id, update_cell_language.language)
    elif message_type == MessageType.REORDER_CELLS:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
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
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        ExitNotebook.parse_obj(message_json)
        session_state.notebook = None
        session_state.filepath = None
    elif message_type == MessageType.UPDATE_NOTEBOOK_NAME:
        if notebook is None:
            return ErrorResponse(error=f"Can't process {message_type}, no active notebook")
        update_notebook_name = UpdateNotebookName.parse_obj(message_json)
        notebook.name = update_notebook_name.name
        # TODO: Update filename
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
