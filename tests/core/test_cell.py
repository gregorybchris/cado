from cado.core.cell import Cell


class TestCell:

    def test_create(self):
        cell = Cell(output_name="a")
        cell.set_code("a = 4 + 5")
        cell.run({})
        assert cell.output == 9
