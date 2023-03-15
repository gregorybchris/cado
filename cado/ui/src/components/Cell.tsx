import { ArrowRight, CheckCircle, Circle, Eraser, Play, Spinner, Trash, WarningCircle } from "@phosphor-icons/react";
import {
  ClearCell,
  DeleteCell,
  MessageType,
  RunCell,
  UpdateCellCode,
  UpdateCellInputNames,
  UpdateCellOutputName,
} from "../lib/models/message";
import { useEffect, useState } from "react";

import Button from "../widgets/Button";
import CellModel from "../lib/models/cell";
import { CellStatus } from "../lib/models/cellStatus";
import CodeEditor from "@uiw/react-textarea-code-editor";
import TextBox from "../widgets/TextBox";

interface CellProps {
  cell: CellModel;
  sendMessage: <M>(message: M) => void;
}

export default function Cell(props: CellProps) {
  const [outputName, setOutputName] = useState<string>("");
  const [inputNames, setInputNames] = useState<string>("");

  useEffect(() => {
    setOutputName(props.cell.output_name);
  }, [props.cell.output_name]);

  useEffect(() => {
    setInputNames(props.cell.input_names.join(", "));
  }, [props.cell.input_names]);

  function updateCellOutputName() {
    setOutputName(props.cell.output_name);
    props.sendMessage<UpdateCellOutputName>({
      cell_id: props.cell.id,
      output_name: outputName,
      type: MessageType.UPDATE_CELL_OUTPUT_NAME,
    });
  }

  function updateCellInputNames() {
    setInputNames(props.cell.input_names.join(", "));
    const inputNamesParsed = inputNames.replace(" ", "").split(",");
    props.sendMessage<UpdateCellInputNames>({
      cell_id: props.cell.id,
      input_names: inputNamesParsed,
      type: MessageType.UPDATE_CELL_INPUT_NAMES,
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
    <div className="mx-5 my-4 rounded-lg bg-dark-rock py-3">
      <div className="flex items-center justify-between px-5">
        <div className="flex items-center">
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

        <div className="flex items-center">
          <TextBox value={inputNames} placeholder="Inputs" onBlur={updateCellInputNames} onChange={setInputNames} />
        </div>
      </div>

      <div className="my-3 bg-black-rock px-5">
        <CodeEditor
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

      <div className="flex items-center px-5">
        <TextBox value={outputName} placeholder="Output" onBlur={updateCellOutputName} onChange={setOutputName} />

        {props.cell.output && (
          <div className="inline-block">
            <div className="flex items-center">
              <ArrowRight weight="bold" className="mx-2" />
              <div>{JSON.stringify(props.cell.output)}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
