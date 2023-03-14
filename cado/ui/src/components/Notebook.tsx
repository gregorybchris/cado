import Cell from "./Cell";
import Notebook from "../lib/models/notebook";

interface NotebookProps {
  notebook: Notebook;
  sendMessage: <M>(message: M) => void;
}

export default function Notebook(props: NotebookProps) {
  return (
    <div className="bg-rock pb-5">
      {/* <div className="text-lg">{props.notebook.name}</div> */}
      <div>
        {props.notebook.cells.map((cell, i) => (
          <Cell key={i} sendMessage={props.sendMessage} cell={cell} />
        ))}
      </div>
    </div>
  );
}
