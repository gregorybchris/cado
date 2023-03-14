import { ArrowRight, CheckCircle, Circle, Eraser, Play, Spinner, WarningCircle } from "@phosphor-icons/react";
import { ClearCell, Message, MessageType, RunCell, UpdateCellCode, UpdateCellName } from "../lib/models/message";

import CellModel from "../lib/models/cell";
import { CellStatus } from "../lib/models/cellStatus";
import CodeEditor from "@uiw/react-textarea-code-editor";

interface CellProps {
  cell: CellModel;
  sendMessage: <M>(message: M) => void;
}

export default function Cell(props: CellProps) {
  function updateCellName(name: string) {
    props.sendMessage<UpdateCellName>({
      cell_id: props.cell.id,
      name: name,
      type: MessageType.UPDATE_CELL_NAME,
    });
  }

  function updateCellCode(code: string) {
    props.sendMessage<UpdateCellCode>({
      cell_id: props.cell.id,
      code: code,
      type: MessageType.UPDATE_CELL_CODE,
    });
  }

  function runCell() {
    props.sendMessage<RunCell>({
      cell_id: props.cell.id,
      type: MessageType.RUN_CELL,
    });
  }

  function clearCell() {
    props.sendMessage<ClearCell>({
      cell_id: props.cell.id,
      type: MessageType.CLEAR_CELL,
    });
  }

  return (
    <div>
      <div className="mb-5 bg-dark-rock py-3">
        <div className="flex items-center px-8">
          <div
            className="mr-5 cursor-pointer rounded-md bg-rock py-2 px-4 duration-150 hover:bg-light-rock hover:ease-linear"
            onClick={() => runCell()}
          >
            <Play weight="bold" />
          </div>

          <div
            className="mr-5 cursor-pointer rounded-md bg-rock py-2 px-4 duration-150 hover:bg-light-rock hover:ease-linear"
            onClick={() => clearCell()}
          >
            <Eraser weight="bold" />
          </div>

          <div className="flex items-center">
            {props.cell.status === CellStatus.ERROR && (
              <WarningCircle className="text-red-500" weight="bold" size={18} />
            )}
            {props.cell.status === CellStatus.OK && <CheckCircle className="text-green-500" weight="bold" size={18} />}
            {props.cell.status === CellStatus.EXPIRED && <Circle weight="bold" size={18} />}
            {props.cell.status === CellStatus.RUNNING && <Spinner weight="bold" size={18} />}
          </div>
        </div>

        <div className="bg-black-rock px-8">
          <CodeEditor
            className="my-3"
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

        <div className="mt-3 flex items-center px-8">
          <input
            className="inline-block w-20 rounded-md bg-rock py-2 px-4 outline-none duration-150 focus:bg-light-rock active:ease-linear"
            type="text"
            value={props.cell.name}
            placeholder="Cell name"
            onChange={(event) => updateCellName(event.target.value)}
          ></input>

          {props.cell.result && (
            <div className="inline-block">
              <div className="flex items-center">
                <ArrowRight weight="bold" className="mx-2" />
                <div>{props.cell.result}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
