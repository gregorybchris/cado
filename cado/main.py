def get_cell_content(cell_name):
    with open(f'{cell_name}.txt', 'r') as f:
        return f.read()


def get_cells_content(cell_names):
    return [get_cell_content(cell_name) for cell_name in cell_names]


def run():
    print("Thanks for using notede")
    cells_content = get_cells_content(['cell_1', 'cell_2'])
    scoped_locals = {}
    scoped_globals = {}

    # print("A!!!")
    # print(scoped_locals)
    # print("B!!!")
    # print(scoped_globals)
    print("C!!!")
    print(locals())
    # print("D!!!")
    # print(globals())

    exec(cells_content[0], scoped_locals, scoped_globals)

    # print("E!!!")
    # print(scoped_locals)
    # print("F!!!")
    # print(scoped_globals)
    print("G!!!")
    print(locals())
    # print("H!!!")
    # print(globals())

    # exec(cells_content[1])
