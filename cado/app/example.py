from pathlib import Path

from cado.core.notebook import Notebook


def load_example_notebook(example_name: str) -> Notebook:
    """Load a simple example notebook.

    Returns:
        Notebook: A notebook containing a single example cell.
    """
    examples_dirpath = Path(__file__).parent.parent / "examples"
    notebook_filepath = examples_dirpath / f"{example_name}.cado"
    return Notebook.from_filepath(notebook_filepath)
