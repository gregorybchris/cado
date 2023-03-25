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
        logger.debug("Not saving notebook to file, notebook was None")
        return

    filepath = session_state.filepath
    if filepath is None:
        logger.debug("Not saving notebook to file, filepath was None")
        return

    notebook.set_updated_time()
    logger.debug("Saving notebook to file: %s", filepath)
    notebook.to_filepath(filepath)


def create_notebook(session_state: SessionState) -> None:
    """Create a new notebook and set it as the current session notebook.
    Also save the new empty notebook to disk.

    Args:
        session_state (SessionState): Current session state.
    """
    cwd = Path.cwd()
    name = get_unique_notebook_name("notebook", cwd)
    filename = f"{name}.cado"
    filepath = cwd / filename
    notebook = Notebook(name=name)
    notebook.add_cell()
    notebook.to_filepath(filepath)
    session_state.filepath = filepath
    session_state.notebook = notebook


def get_unique_notebook_name(name: str, dirpath: Path) -> str:
    """Attempts to find a unique notebook name and avoids duplicates.

    Args:
        name (str): The desired name for the notebook.
        dirpath (Path): The directory where the notebook will be saved.

    Returns:
        str: The unique name the notebook should be saved as.
    """
    for i in range(1, 100):
        name = name if i == 1 else f"{name}-{i}"
        filename = f"{name}.cado"
        filepath = dirpath / filename
        if not filepath.exists():
            return name
    raise ValueError("Could not create a new notebook, found too many existing new notebooks")


def delete_existing_notebook(filepath: Path) -> None:
    """Delete a notebook from the disk.

    Args:
        filepath (Path): Path on disk to the notebook.
    """
    filepath.unlink()


def rename_notebook(session_state: SessionState, notebook: Notebook, name: str) -> None:
    """Rename the notebook given a new name.

    Args:
        session_state (SessionState): Current session state.
        notebook (Notebook): Notebook to update.
        name (str): Name to use when renaming the notebook.
    """
    notebook.name = name

    if name == "":
        return

    old_filepath = session_state.filepath
    if old_filepath is None:
        return

    dirpath = old_filepath.parent
    new_name = get_unique_notebook_name(name, dirpath)
    new_filepath = dirpath / f"{new_name}.cado"

    session_state.filepath = new_filepath
    save_notebook(session_state)
    delete_existing_notebook(old_filepath)


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
