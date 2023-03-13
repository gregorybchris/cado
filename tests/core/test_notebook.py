from pathlib import Path

import pytest

from cado.core.notebook import Notebook


class TestNotebook:

    @pytest.mark.skip("Haven't gotten reading working")
    def test_run_cell(self):
        notebook_filename = "notebook.cado"
        notebook = Notebook.from_filepath(Path(notebook_filename))
        notebook.run_cell("cell_1")
