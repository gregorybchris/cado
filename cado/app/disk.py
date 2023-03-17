import logging
from pathlib import Path
from typing import List

from cado.app.example import load_example_notebook
from cado.app.session_state import SessionState
from cado.core.notebook import Notebook
from cado.core.notebook_details import NotebookDetails

logger = logging.getLogger(__name__)


def save_notebook(session_state: SessionState) -> None:
    """Save the current session notebook to the disk.

    Args:
        session_state (SessionState): Current session state.
    """
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
    """Create a new notebook and set it as the current session notebook.
    Also save the new empty notebook to disk.

    Args:
        session_state (SessionState): Current session state.
    """
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
    """Delete a notebook from the disk.

    Args:
        filepath (Path): Path on disk to the notebook.
    """
    filepath.unlink()


def list_local_notebooks() -> List[NotebookDetails]:
    """List all of the notebooks on the local disk.

    Returns:
        List[NotebookDetails]: A list of NotebookDetail objects.
    """
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
