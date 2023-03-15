from cado.core.notebook import Notebook


class TestNotebook:

    def test_create(self):
        notebook_filename = "notebook.cado"
        notebook = Notebook(name=notebook_filename)
        assert notebook.name == notebook_filename
