from pathlib import Path

from cado.core.notebook import Notebook


def load_example_notebook(filename: str) -> Notebook:
    """Load a simple example notebook.

    Args:
        filename (str): Name of notebook file to load.

    Returns:
        Notebook: An example notebook.
    """
    examples_dirpath = Path(__file__).parent.parent / "examples"
    notebook_filepath = examples_dirpath / filename
    return Notebook.from_filepath(notebook_filepath)
