import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cado.core.cell import Cell
from cado.core.cell_status import CellStatus
from cado.core.language import Language

logger = logging.getLogger(__name__)

CURRENT_VERSION = "0.1"


class Notebook(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    version: str = CURRENT_VERSION
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)
    cells: List[Cell] = []

    def update_cell_output_name(self, cell_id: UUID, output_name: str) -> None:
        """Set a notebook cell's output name.

        Args:
            cell_id (UUID): ID of the cell.
            output_name (str): Name for the output variable.
        """
        self.clear_cell(cell_id)

        output_names = set()
        for cell in self.cells:
            if cell.id != cell_id and cell.output_name != "":
                output_names.add(cell.output_name)

        cell = self.get_cell(cell_id)

        for child in self._get_children(cell):
            child.clear()

        if output_name in output_names:
            error = ValueError(f"Cell with output name \"{output_name}\" already exists in the notebook")
            self.error_cell(cell.id, error)
            cell.output_name = ""
            raise error

        cell.output_name = output_name

    def update_cell_input_names(self, cell_id: UUID, input_names: List[str]) -> None:
        """Set a notebook cell's input names.

        Args:
            cell_id (UUID): ID of the cell.
            input_names (List[str]): Names for the input variables.
        """
        self._check_no_self_ancestor(cell_id, cell_id, input_names)
        self.clear_cell(cell_id)

        output_names = set()
        for cell in self.cells:
            if cell.id != cell_id and cell.output_name != "":
                output_names.add(cell.output_name)

        cell = self.get_cell(cell_id)
        for input_name in input_names:
            if input_name not in output_names:
                error = ValueError(f"No cell with output name \"{input_name}\"")
                self.error_cell(cell.id, error)
                cell.input_names = []
                raise error

        cell.input_names = input_names

    def set_cell_code(self, cell_id: UUID, code: str) -> None:
        """Set a notebook cell's code.

        Args:
            cell_id (UUID): ID of the cell.
            code (str): String of code to set on the cell.
        """
        cell = self.get_cell(cell_id)
        cell.code = code
        self.clear_cell(cell.id)

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

    def add_cell(self, index: Optional[int]) -> UUID:
        """Add a cell to the notebook.

        Args:
            index (Optional[int]): Index where the cell should be inserted.

        Returns:
            UUID: ID of the new cell.
        """
        new_cell = Cell(output_name="")
        if index is None:
            self.cells.append(new_cell)
        else:
            self.cells.insert(index, new_cell)
        return new_cell.id

    def _get_children(self, cell: Cell) -> Iterator[Cell]:
        for other in self.cells:
            for input_name in other.input_names:
                if input_name == cell.output_name:
                    yield other

    def _get_parents(self, cell: Cell) -> Iterator[Cell]:
        for other in self.cells:
            for input_name in cell.input_names:
                if other.output_name == input_name:
                    yield other

    def _check_no_self_ancestor(
        self,
        target_cell_id: UUID,
        current_cell_id: UUID,
        input_names: List[str],
    ) -> None:
        for cell in self.cells:
            if cell.id != current_cell_id:
                for input_name in input_names:
                    if input_name == cell.output_name:
                        if cell.id == target_cell_id:
                            error = ValueError("Cycle found in cell dependencies")
                            self.error_cell(target_cell_id, error)
                            raise error
                        self._check_no_self_ancestor(target_cell_id, cell.id, cell.input_names)

    def run_cell(self, cell_id: UUID) -> None:
        """Run a cell in the notebook.

        Args:
            cell_id (UUID): ID of the cell to run.
        """
        cell = self.get_cell(cell_id)

        context: Dict[str, Any] = {}
        for parent in self._get_parents(cell):
            if parent.status in [CellStatus.EXPIRED, CellStatus.ERROR]:
                self.run_cell(parent.id)
            if parent.status == CellStatus.ERROR:
                raise ValueError("Parent cell does not have OK status, could not run child cell")
            context[parent.output_name] = parent.output

        logger.info("Running cell %s", cell.id)
        cell.run(context)

        if cell.status == CellStatus.OK:
            for child in self._get_children(cell):
                self.run_cell(child.id)

    def update_cell_language(self, cell_id: UUID, language: Language) -> None:
        """Run a cell in the notebook.

        Args:
            cell_id (UUID): ID of the cell to run.
            language (Language): New language to use.
        """
        cell = self.get_cell(cell_id)
        cell.language = language
        cell.clear()

    def error_cell(self, cell_id: UUID, error: ValueError) -> None:
        """Error out a cell in the notebook.

        Args:
            cell_id (UUID): ID of the cell to error.
        """
        cell = self.get_cell(cell_id)
        cell.set_error(error)

        for child in self._get_children(cell):
            self.clear_cell(child.id)

    def clear_cell(self, cell_id: UUID) -> None:
        """Clear a cell in the notebook.

        Args:
            cell_id (UUID): ID of the cell to clear.
        """
        cell = self.get_cell(cell_id)
        cell.clear()

        for child in self._get_children(cell):
            self.clear_cell(child.id)

    def reorder_cells(self, cell_ids: List[UUID]) -> None:
        """Reorder cells in the notebook.

        Args:
            cell_ids (List[UUID]): List of cell IDs in the correct order.
        """
        new_cells = []
        for cell_id in cell_ids:
            cell = self.get_cell(cell_id)
            new_cells.append(cell)
        self.cells = new_cells

    def set_updated_time(self) -> None:
        """Set the updated time to now."""
        self.updated = datetime.now()

    @classmethod
    def from_filepath(cls, filepath: Path) -> "Notebook":
        """Load a notebook from a .cado notebook file.

        Args:
            filepath (Path): Filepath to a .cado notebook file.

        Returns:
            Notebook: Loaded cado notebook.
        """
        with filepath.open() as f:
            notebook_json = json.load(f)
            version = notebook_json["version"]
            if version != CURRENT_VERSION:
                raise ValueError(f"Cannot load notebook with version {version}")
            return cls.parse_obj(notebook_json)

    def to_filepath(self, filepath: Path) -> None:
        """Save a notebook to a .cado notebook file.

        Args:
            filepath (Path): Filepath to a .cado notebook file.
        """
        with filepath.open("w") as f:
            notebook_json = self.json()
            f.write(notebook_json)
