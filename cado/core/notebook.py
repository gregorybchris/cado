import json
from pathlib import Path
from typing import List
from uuid import UUID

from pydantic import BaseModel

from cado.core.cell import Cell


class Notebook(BaseModel):
    filepath: Path
    cells: List[Cell] = []

    def get_cell(self, cell_id: UUID) -> Cell:
        for cell in self.cells:
            if cell.id == cell_id:
                return cell
        raise ValueError(f"No cell with ID {cell_id} found in notebook")

    def add_cell(self, cell: Cell) -> None:
        """Add a cell to the notebook.

        Args:
            cell (Cell): Cell to add to the notebook.
        """
        self.cells.append(cell)

    def run_cell(self, cell_id: UUID) -> None:
        """Run a cell in the notebook.

        Args:
            cell_id (UUID): ID of the cell to run.
        """
        for cell in self.cells:
            if cell.id == cell_id:
                cell.run()
                return
        raise ValueError(f"Cell {cell_id} is not in this notebook")

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
