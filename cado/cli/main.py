from cado.core.cell import Cell
from cado.core.environment import Environment
from cado.core.notebook import Notebook


def run():
    print("Starting Cado Notebook Environment")

    notebook_name = 'notebook.cdo'
    notebook = Notebook.create_from_file(notebook_name)
    # output = notebook.run_cell('cell_1')
    # print(output)
    output = notebook.run_cell('cell_2')
    print(output)
