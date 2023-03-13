import json
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, Extra

from cado.core.cell import Cell


class Notebook(BaseModel):
    filepath: Path
    cells: Dict[str, Cell] = {}

    # pylint: disable=too-few-public-methods
    class Config:
        extra = Extra.forbid

    def run_cell(self, cell_id: str) -> Any:
        """Run a cell in the notebook.

        Args:
            cell_id (str): ID of the cell to run.

        Returns:
            Any: The result of running the cell.
        """
        if cell_id not in self.cells:
            raise ValueError(f"Cell {cell_id} is not in this notebook")

        cell = self.cells[cell_id]
        return cell.run()

    @classmethod
    def from_filepath(cls, filepath: Path) -> "Notebook":
        """Load a notebook from a .cado notebook file.

        Args:
            filepath (Path): Filepath to a .cado notebook file.

        Returns:
            Notebook: Loaded Cado notebook.
        """
        with filepath.open() as f:
            notebook_json = json.load(f)
            return cls.parse_obj(notebook_json)

        # TODO: Check that the graph is acyclic
