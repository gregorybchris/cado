class Cell:
    def __init__(self, cell_id, contents, out_var):
        self._cell_id = cell_id
        self._contents = contents
        self._out_var = out_var
        self._dependents = []
        self._dependencies = []
        self._result = None
        self._dirty = True

    def get_id(self):
        return self._cell_id

    def set_contents(self, contents):
        self._contents = contents
        self._dirty = True

    def set_out_var(self, out_var):
        # TODO: All depenents are now dirty
        self._out_var = out_var

    def get_result(self):
        return self._result

    def get_out_var(self):
        return self._out_var

    def add_dependent(self, cell):
        self._dependents.append(cell)

    def add_dependency(self, cell):
        self._dependencies.append(cell)

    def is_dirty(self):
        return self._dirty

    def run(self):
        context = dict()
        for dependency in self._dependencies:
            if dependency.is_dirty():
                dependency.run()
            context[dependency.get_out_var()] = dependency.get_result()

        defs = dict()
        exec(self._contents, context, defs)

        if self._out_var is not None:
            self._result = defs[self._out_var]
        self._dirty = False
        return self._result
