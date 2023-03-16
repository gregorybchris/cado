import Cell from "./Cell";
import Notebook from "../lib/models/notebook";
import { Reorder } from "framer-motion";
import { MessageType, ReorderCells } from "../lib/models/message";
import CellModel from "../lib/models/cell";

interface NotebookProps {
  notebook: Notebook;
  sendMessage: <M>(message: M) => void;
}

export default function Notebook(props: NotebookProps) {
  function reorderCells(cells: CellModel[]) {
    props.sendMessage<ReorderCells>({
      cell_ids: cells.map((cell) => cell.id),
      type: MessageType.REORDER_CELLS,
    });
  }

  return (
    <div className="bg-rock pb-5">
      {/* <div className="text-lg">{props.notebook.name}</div> */}

      <Reorder.Group axis="y" onReorder={reorderCells} values={props.notebook.cells}>
        {props.notebook.cells.map((cell) => (
          <Cell key={cell.id} sendMessage={props.sendMessage} cell={cell} />
        ))}
      </Reorder.Group>
    </div>
  );
}
