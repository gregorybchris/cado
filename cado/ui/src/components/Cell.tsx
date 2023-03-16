import { ArrowRight, CheckCircle, Circle, Eraser, Play, Spinner, Trash, WarningCircle } from "@phosphor-icons/react";
import {
  ClearCell,
  DeleteCell,
  MessageType,
  RunCell,
  UpdateCellCode,
  UpdateCellInputNames,
  UpdateCellLanguage,
  UpdateCellOutputName,
} from "../lib/models/message";
import { Reorder, useDragControls, useMotionValue } from "framer-motion";
import { useEffect, useState } from "react";

import Button from "../widgets/Button";
import CellModel from "../lib/models/cell";
import { CellStatus } from "../lib/models/cellStatus";
import CodeEditor from "@uiw/react-textarea-code-editor";
import { Language } from "../lib/models/language";
import { BsMarkdown as MarkdownIcon } from "react-icons/bs";
import { TbBrandPython as PythonIcon } from "react-icons/tb";
import ReorderIcon from "../widgets/ReorderIcon";
import TextBox from "../widgets/TextBox";

interface CellProps {
  cell: CellModel;
  sendMessage: <M>(message: M) => void;
}

export default function Cell(props: CellProps) {
  const [outputName, setOutputName] = useState<string>("");
  const [inputNames, setInputNames] = useState<string>("");

  const y = useMotionValue(0);
  const dragControls = useDragControls();

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

  function updateCellLanguage() {
    const newLanguage = props.cell.language == Language.PYTHON ? Language.MARKDOWN : Language.PYTHON;
    props.sendMessage<UpdateCellLanguage>({
      cell_id: props.cell.id,
      language: newLanguage,
      type: MessageType.UPDATE_CELL_LANGUAGE,
    });
  }

  function getLanguageCode() {
    if (props.cell.language == Language.PYTHON) return "py";
    if (props.cell.language == Language.MARKDOWN) return "md";
    return "py";
  }

  return (
    <Reorder.Item value={props.cell} id={props.cell.id} style={{ y }} dragListener={false} dragControls={dragControls}>
      <div className="mx-5 my-4 rounded-lg bg-dark-rock py-3">
        <div className="flex items-center justify-between px-5">
          <div>
            {props.cell.language == Language.PYTHON && (
              <div className="flex items-center">
                <Button onClick={runCell} tooltip="Run" iconClass={Play} />
                <Button onClick={clearCell} tooltip="Clear" iconClass={Eraser} />

                <div className="flex items-center">
                  {props.cell.status === CellStatus.ERROR && (
                    <WarningCircle className="text-red-500" weight="bold" size={18} />
                  )}
                  {props.cell.status === CellStatus.OK && (
                    <CheckCircle className="text-green-500" weight="bold" size={18} />
                  )}
                  {props.cell.status === CellStatus.EXPIRED && <Circle weight="bold" size={18} />}
                  {props.cell.status === CellStatus.RUNNING && <Spinner weight="bold" size={18} />}
                </div>
              </div>
            )}
          </div>

          <div className="flex items-center">
            {props.cell.language == Language.PYTHON && (
              <TextBox value={inputNames} placeholder="Inputs" onBlur={updateCellInputNames} onChange={setInputNames} />
            )}

            <div
              onClick={updateCellLanguage}
              className="mx-5 cursor-pointer rounded-lg bg-rock px-2 py-2 duration-150 hover:bg-light-rock hover:ease-linear"
            >
              {props.cell.language == Language.MARKDOWN && <MarkdownIcon />}
              {props.cell.language == Language.PYTHON && <PythonIcon />}
            </div>

            <Button onClick={deleteCell} tooltip="Delete" iconClass={Trash} />

            <ReorderIcon dragControls={dragControls} />
          </div>
        </div>

        <div className="my-3 bg-black-rock px-5">
          <CodeEditor
            value={props.cell.code}
            language={getLanguageCode()}
            onChange={(event) => updateCellCode(event.target.value)}
            padding={15}
            style={{
              fontSize: 12,
              backgroundColor: "#1d1f23",
              fontFamily: "Menlo",
            }}
          />
        </div>

        {props.cell.language == Language.PYTHON && (
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
        )}
      </div>
    </Reorder.Item>
  );
}
