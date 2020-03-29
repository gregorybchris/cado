import json

from cado.core.cell import Cell


class Notebook:
    FIELD_CELLS = 'cells'
    FIELD_CELL_ID = 'id'
    FIELD_CELL_CONTENTS = 'contents'
    FIELD_CELL_DEPENDENCIES = 'dependencies'
    FIELD_CELL_OUT_VAR = 'out_var'

    def __init__(self, filepath):
        self._cells = dict()

    def run_cell(self, cell_id):
        if cell_id not in self._cells:
            raise ValueError(f"Cell ID {cell_id} is not in this notebook")

        cell = self._cells[cell_id]
        return cell.run()

    @classmethod
    def create_from_file(cls, filepath):
        with open(filepath, 'r') as f:
            notebook_json = json.load(f)

        notebook = cls(filepath)
        dependency_map = dict()
        for cell_json in notebook_json[cls.FIELD_CELLS]:
            cell_id = cell_json[cls.FIELD_CELL_ID]
            contents = cell_json[cls.FIELD_CELL_CONTENTS]
            out_var = cell_json[cls.FIELD_CELL_OUT_VAR]
            cell = Cell(cell_id, contents, out_var)
            dependency_map[cell_id] = cell_json[cls.FIELD_CELL_DEPENDENCIES]
            notebook._cells[cell.get_id()] = cell

        for depenent_id, dependency_ids in dependency_map.items():
            dependent = notebook._cells[depenent_id]
            for dependency_id in dependency_ids:
                dependency = notebook._cells[dependency_id]
                dependency.add_dependent(dependent)
                dependent.add_dependency(dependency)

        # TODO: Check that the graph is acyclic

        return notebook
