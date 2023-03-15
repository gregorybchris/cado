from cado.core.notebook import Notebook


def load_example_notebook() -> Notebook:
    """Load a simple example notebook.

    Returns:
        Notebook: A notebook containing a single example cell.
    """
    example_code = ("def is_even(v):\n"
                    "    return v % 2 == 0\n\n"
                    "a = 0\n"
                    "xs = [2, 3, 4, 5, 6, 8, 10]\n"
                    "for x in xs:\n"
                    "    if is_even(x):\n"
                    "        a += 1\n"
                    "    else:\n"
                    "        a -= 1")
    notebook = Notebook(name="example.cado")
    cell_id = notebook.add_cell()
    notebook.set_cell_code(cell_id, example_code)
    notebook.update_cell_output_name(cell_id, "a")
    return notebook
