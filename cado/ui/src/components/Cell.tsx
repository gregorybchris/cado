import { Message, MessageType, RunCell, UpdateCellCode, UpdateCellName } from "../lib/models/message";

import CellModel from "../lib/models/cell";
import { CellStatus } from "../lib/models/cellStatus";
import CodeEditor from "@uiw/react-textarea-code-editor";
import { useEffect } from "react";

interface CellProps {
  cell: CellModel;
  onSend: (message: Message) => void;
}

export default function Cell(props: CellProps) {
  function updateCellName(name: string) {
    const message: UpdateCellName = {
      cell_id: props.cell.id,
      name: name,
      type: MessageType.UPDATE_CELL_NAME,
    };
    props.onSend(message);
  }

  function updateCellCode(code: string) {
    const message: UpdateCellCode = {
      cell_id: props.cell.id,
      code: code,
      type: MessageType.UPDATE_CELL_CODE,
    };
    props.onSend(message);
  }

  function runCell() {
    const message: RunCell = {
      cell_id: props.cell.id,
      type: MessageType.RUN_CELL,
    };
    props.onSend(message);
  }

  return (
    <div>
      <div className="bg-dark-rock py-5">
        <input
          className="mx-5 inline-block rounded-md bg-rock py-2 px-4 outline-none duration-150 active:bg-light-rock active:ease-linear"
          type="text"
          value={props.cell.name}
          placeholder="Cell name"
          onChange={(event) => updateCellName(event.target.value)}
        ></input>

        <div className="bg-black-rock px-8">
          <CodeEditor
            className="mt-5"
            value={props.cell.code}
            language="py"
            onChange={(event) => updateCellCode(event.target.value)}
            padding={15}
            style={{
              fontSize: 12,
              backgroundColor: "#1d1f23",
              fontFamily: "Menlo",
            }}
          />
        </div>

        <div className="bg-dark-rock px-5 pt-5">
          <div
            className="inline-block cursor-pointer rounded-md bg-rock py-2 px-4 duration-150 hover:bg-light-rock hover:ease-linear"
            onClick={() => runCell()}
          >
            Run Cell
          </div>

          {props.cell.result && (
            <div className="inline-block px-10">
              {props.cell.name} = {props.cell.result}
            </div>
          )}

          {props.cell.status == CellStatus.ERROR && <div className="inline-block px-10 text-red-500">Error</div>}
        </div>
      </div>
    </div>
  );
}
