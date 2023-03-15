import json
from pathlib import Path
from typing import List
from uuid import UUID

from pydantic import BaseModel

from cado.core.cell import Cell
from cado.core.cell_status import CellStatus


class Notebook(BaseModel):
    name: str
    cells: List[Cell] = []

    def update_cell_output_name(self, cell_id: UUID, output_name: str) -> None:
        output_names = set()
        for cell in self.cells:
            if cell.id != cell_id:
                output_names.add(cell.output_name)

        for cell in self.cells:
            if cell.id == cell_id:
                if output_name in output_names and output_name != "":
                    cell.clear()
                    cell.set_status(CellStatus.ERROR)
                    cell.set_output_name("")
                    raise ValueError(f"Cell with output name \"{output_name}\" already exists in the notebook")
                cell.set_output_name(output_name)

    def update_cell_input_names(self, cell_id: UUID, input_names: str) -> None:
        output_names = set()
        for cell in self.cells:
            if cell.id != cell_id:
                output_names.add(cell.output_name)

        for cell in self.cells:
            if cell.id == cell_id:
                valid_input_names = []
                for input_name in input_names:
                    if input_name in output_names:
                        valid_input_names.append(input_name)
                cell.set_input_names(valid_input_names)

    def set_cell_code(self, cell_id: UUID, code: str) -> None:
        """Set a notebook cell's code.

        Args:
            cell_id (UUID): ID of the cell.
            code (str): String of code to set on the cell.
        """
        for cell in self.cells:
            if cell.id == cell_id:
                cell.set_code(code)
        raise ValueError(f"No cell with ID {cell_id} found in notebook")

    def get_cell(self, cell_id: UUID) -> Cell:
        """Get a cell from the notebook.

        Args:
            cell_id (UUID): ID of the cell to get from the notebook.
        """
        for cell in self.cells:
            if cell.id == cell_id:
                return cell
        raise ValueError(f"No cell with ID {cell_id} found in notebook")

    def delete_cell(self, cell_id: UUID) -> None:
        """Delete a cell from the notebook.

        Args:
            cell_id (UUID): ID of the cell to delete from the notebook.
        """
        self.cells = [c for c in self.cells if c.id != cell_id]

    def add_cell(self) -> None:
        """Add a cell to the notebook."""
        new_cell = Cell(output_name="")
        self.cells.append(new_cell)

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

    def clear_cell(self, cell_id: UUID) -> None:
        """Clear a cell in the notebook.

        Args:
            cell_id (UUID): ID of the cell to clear.
        """
        for cell in self.cells:
            if cell.id == cell_id:
                cell.clear()
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

    def to_filepath(self, filepath: Path) -> None:
        """Save a notebook to a .cado notebook file.

        Args:
            filepath (Path): Filepath to a .cado notebook file.
        """
        with filepath.open("w") as f:
            notebook_json = self.json()
            f.write(notebook_json)

        # TODO: Check that the graph is acyclic
