import json
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Extra

from cado.core.cell import Cell


class Notebook(BaseModel):
    filepath: Path
    cells: Dict[str, Cell] = {}

    class Config:
        extra = Extra.forbid

    def run_cell(self, cell_id: str):
        if cell_id not in self.cells:
            raise ValueError(f"Cell \{cell_id} is not in this notebook")

        cell = self.cells[cell_id]
        return cell.run()

    @classmethod
    def from_filepath(cls, filepath: Path):
        with filepath.open() as f:
            notebook_json = json.load(f)
            return cls.parse_obj(notebook_json)

        # TODO: Check that the graph is acyclic
