from cado.core.cell import Cell
from cado.core.cell_status import CellStatus
from cado.core.notebook import Notebook


def load_example_notebook() -> Notebook:
    EXAMPLE_CODE = ("def is_even(v):\n"
                    "    return v % 2 == 0\n\n"
                    "a = 0\n"
                    "xs = [2, 3, 4, 5, 6, 8, 10]\n"
                    "for x in xs:\n"
                    "    if is_even(x):\n"
                    "        a += 1\n"
                    "    else:\n"
                    "        a -= 1")
    example_cell = Cell(output_name="a", code=EXAMPLE_CODE)
    example_cell.set_status(CellStatus.EXPIRED)
    notebook = Notebook(name="example.cado", filepath="")
    notebook.add_cell(example_cell)
    return notebook
