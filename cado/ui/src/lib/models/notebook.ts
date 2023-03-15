import Cell from "./cell";

export default interface Notebook {
  name: string;
  cells: Cell[];
}

export function updateNotebookCell(notebook: Notebook, cell: Cell): Notebook {
  return {
    ...notebook,
    cells: notebook.cells.map((c) => (c.id == cell.id ? cell : c)),
  };
}
