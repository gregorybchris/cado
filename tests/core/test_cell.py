from cado.core.cell import Cell


class TestCell:

    def test_create(self):
        cell = Cell(name="out")
        cell.set_code("out = 4 + 5")
        cell.run()
        print(cell.output)
