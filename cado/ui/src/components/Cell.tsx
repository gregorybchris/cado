import { ArrowRight, Broom, CheckCircle, Circle, Play, Trash, WarningCircle } from "@phosphor-icons/react";
import {
  ClearCell,
  DeleteCell,
  MessageType,
  UpdateCellCode,
  UpdateCellInputNames,
  UpdateCellLanguage,
  UpdateCellOutputName,
} from "../lib/models/message";
import { Reorder, useDragControls, useMotionValue } from "framer-motion";
import { useEffect, useRef, useState } from "react";

import Button from "../widgets/Button";
import CellModel from "../lib/models/cell";
import { CellStatus } from "../lib/models/cellStatus";
import CodeEditor from "@uiw/react-textarea-code-editor";
import { Language } from "../lib/models/language";
import { BsMarkdown as MarkdownIcon } from "react-icons/bs";
import { None } from "../lib/types";
import { TbBrandPython as PythonIcon } from "react-icons/tb";
import ReorderIcon from "../widgets/ReorderIcon";
import TextBox from "../widgets/TextBox";

interface CellProps {
  cell: CellModel;
  sendMessage: <M>(message: M) => void;
  active: boolean;
  onSetActive: () => void;
  runCell: (cell: CellModel) => void;
  clearCell: (cell: CellModel) => void;
  editMode: boolean;
  onSetEditMode: (editMode: boolean) => void;
}

export default function Cell(props: CellProps) {
  const [outputName, setOutputName] = useState<string>("");
  const [inputNames, setInputNames] = useState<string>("");
  const editorRef = useRef<HTMLTextAreaElement | null>(null);

  const y = useMotionValue(0);
  const dragControls = useDragControls();

  useEffect(() => {
    if (props.active && props.editMode) {
      editorRef.current?.focus();
    } else {
      editorRef.current?.blur();
    }
  }, [props.editMode, props.active]);

  useEffect(() => {
    setOutputName(props.cell.output_name);
  }, [props.cell.output_name]);

  useEffect(() => {
    setInputNames(props.cell.input_names.join(", "));
  }, [props.cell.input_names]);

  function updateCellOutputName() {
    if (outputName == props.cell.output_name) return;
    props.sendMessage<UpdateCellOutputName>({
      cell_id: props.cell.id,
      output_name: outputName,
      type: MessageType.UPDATE_CELL_OUTPUT_NAME,
    });
  }

  function updateCellInputNames() {
    const cellInputNamesString = props.cell.input_names.join(", ");
    if (inputNames == cellInputNamesString) return;

    const inputNamesParsed = inputNames.length === 0 ? [] : inputNames.replace(" ", "").split(",");
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

  function onClick(e: any) {
    e.stopPropagation();
    props.onSetActive();
  }

  function onClickEditor(e: any) {
    e.stopPropagation();
    props.onSetEditMode(true);
    props.onSetActive();
  }

  const activeStyles = props.active ? "border-l-4 border-lighter-rock" : "";

  return (
    <Reorder.Item value={props.cell} id={props.cell.id} style={{ y }} dragListener={false} dragControls={dragControls}>
      <div className={`mx-5 mb-4 select-none rounded-lg bg-dark-rock py-3 ${activeStyles}`} onClick={onClick}>
        <div className="flex items-center justify-between px-5">
          <div>
            {props.cell.language == Language.PYTHON && (
              <div className="flex items-center">
                <Button onClick={() => props.runCell(props.cell)} tooltip="Run" iconClass={Play} />
                <Button onClick={() => props.clearCell(props.cell)} tooltip="Clear" iconClass={Broom} />

                <div className="flex items-center">
                  {props.cell.status === CellStatus.ERROR && (
                    <WarningCircle className="text-red-500" weight="bold" size={18} />
                  )}
                  {props.cell.status === CellStatus.OK && (
                    <CheckCircle className="text-green-500" weight="bold" size={18} />
                  )}
                  {props.cell.status === CellStatus.EXPIRED && <Circle weight="bold" size={18} />}
                </div>
              </div>
            )}
          </div>

          <div className="flex items-center">
            {props.cell.language == Language.PYTHON && (
              <TextBox value={inputNames} placeholder="Inputs" onBlur={updateCellInputNames} onChange={setInputNames} />
            )}

            <button
              onClick={updateCellLanguage}
              title="Toggle language"
              className="mx-5 cursor-pointer rounded-lg bg-rock px-2 py-2 duration-150 hover:bg-light-rock hover:ease-linear"
            >
              {props.cell.language == Language.MARKDOWN && <MarkdownIcon />}
              {props.cell.language == Language.PYTHON && <PythonIcon />}
            </button>

            <Button onClick={deleteCell} tooltip="Delete" iconClass={Trash} />

            <ReorderIcon dragControls={dragControls} />
          </div>
        </div>

        <div className="my-3 bg-black-rock px-5">
          <CodeEditor
            ref={editorRef}
            value={props.cell.code}
            language={getLanguageCode()}
            onChange={(event) => updateCellCode(event.target.value)}
            padding={15}
            onClick={onClickEditor}
            style={{
              fontSize: 12,
              backgroundColor: "#1d1f23",
              fontFamily: "Menlo",
            }}
          />
        </div>

        {props.cell.language == Language.PYTHON && (
          <div>
            <div className="flex items-center px-5">
              <TextBox value={outputName} placeholder="Output" onBlur={updateCellOutputName} onChange={setOutputName} />

              {props.cell.output !== None && props.cell.output !== null && (
                <div className="flex items-center">
                  <ArrowRight weight="bold" className="mx-2" />
                  <div className="select-text">{JSON.stringify(props.cell.output)}</div>
                </div>
              )}
            </div>
            {(!!props.cell.stdout || !!props.cell.stderr) && (
              <div className="mt-3 bg-black-rock px-5">
                <CodeEditor
                  value={!props.cell.stderr ? props.cell.stdout : props.cell.stderr}
                  language="txt"
                  contentEditable={false}
                  padding={15}
                  style={{
                    fontSize: 12,
                    backgroundColor: "#1d1f23",
                    fontFamily: "Menlo",
                    color: !!props.cell.stderr ? "#ef4444" : undefined,
                  }}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </Reorder.Item>
  );
}
