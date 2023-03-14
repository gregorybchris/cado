import Cell from "./Cell";
import CellModel from "../lib/models/cell";

interface NotebookProps {
  cells: CellModel[];
  sendMessage: <M>(message: M) => void;
}

export default function Notebook(props: NotebookProps) {
  return (
    <div>
      {props.cells.map((cell, i) => (
        <Cell key={i} sendMessage={props.sendMessage} cell={cell} />
      ))}
    </div>
  );
}
