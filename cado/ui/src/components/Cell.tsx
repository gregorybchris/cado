import { ArrowRight, CheckCircle, Circle, Eraser, Play, Spinner, Trash, WarningCircle } from "@phosphor-icons/react";
import {
  ClearCell,
  DeleteCell,
  MessageType,
  RunCell,
  UpdateCellCode,
  UpdateCellOutputName,
} from "../lib/models/message";
import { useEffect, useState } from "react";

import Button from "../widgets/Button";
import CellModel from "../lib/models/cell";
import { CellStatus } from "../lib/models/cellStatus";
import CodeEditor from "@uiw/react-textarea-code-editor";

interface CellProps {
  cell: CellModel;
  sendMessage: <M>(message: M) => void;
}

export default function Cell(props: CellProps) {
  const [outputName, setOutputName] = useState("");

  useEffect(() => {
    setOutputName(props.cell.output_name);
  }, [props.cell.output_name]);

  function updateCellOutputName() {
    props.sendMessage<UpdateCellOutputName>({
      cell_id: props.cell.id,
      output_name: outputName,
      type: MessageType.UPDATE_CELL_OUTPUT_NAME,
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

  function deleteCell() {
    props.sendMessage<DeleteCell>({
      cell_id: props.cell.id,
      type: MessageType.DELETE_CELL,
    });
  }

  return (
    <div>
      <div className="mx-5 mb-5 bg-dark-rock py-3">
        <div className="flex items-center px-8">
          <Button onClick={runCell} tooltip="Run" iconClass={Play} />
          <Button onClick={clearCell} tooltip="Clear" iconClass={Eraser} />
          <Button onClick={deleteCell} tooltip="Delete" iconClass={Trash} />

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
            className="inline-block w-24 rounded-md bg-rock py-2 px-4 outline-none duration-150 focus:bg-light-rock active:ease-linear"
            type="text"
            value={outputName}
            placeholder="Output"
            onBlur={updateCellOutputName}
            onChange={(event) => setOutputName(event.target.value)}
          ></input>

          {props.cell.output && (
            <div className="inline-block">
              <div className="flex items-center">
                <ArrowRight weight="bold" className="mx-2" />
                <div className="">{JSON.stringify(props.cell.output)}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
