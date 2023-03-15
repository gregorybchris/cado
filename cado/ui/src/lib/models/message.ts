import Cell from "./cell";
import Notebook from "./notebook";

export enum MessageType {
  // publish
  GET_NOTEBOOK = "get-notebook",
  UPDATE_CELL_CODE = "update-cell-code",
  UPDATE_CELL_OUTPUT_NAME = "update-cell-output-name",
  UPDATE_CELL_INPUT_NAMES = "update-cell-input-names",
  RUN_CELL = "run-cell",
  CLEAR_CELL = "clear-cell",
  NEW_CELL = "new-cell",
  DELETE_CELL = "delete-cell",

  // subscribe
  GET_NOTEBOOK_RESPONSE = "get-notebook-response",
  GET_CELL_RESPONSE = "get-cell-response",
  ERROR_RESPONSE = "error-response",
}

export interface Message {
  type: string;
}

export interface GetNotebook {
  type: MessageType.GET_NOTEBOOK;
}

export interface UpdateCellCode {
  cell_id: string;
  code: string;
  type: MessageType.UPDATE_CELL_CODE;
}

export interface UpdateCellOutputName {
  cell_id: string;
  output_name: string;
  type: MessageType.UPDATE_CELL_OUTPUT_NAME;
}

export interface UpdateCellInputNames {
  cell_id: string;
  input_names: string[];
  type: MessageType.UPDATE_CELL_INPUT_NAMES;
}

export interface RunCell {
  cell_id: string;
  type: MessageType.RUN_CELL;
}

export interface ClearCell {
  cell_id: string;
  type: MessageType.CLEAR_CELL;
}

export interface NewCell {
  type: MessageType.NEW_CELL;
}

export interface DeleteCell {
  cell_id: string;
  type: MessageType.DELETE_CELL;
}

export interface GetNotebookResponse {
  notebook: Notebook;
  type: MessageType.GET_NOTEBOOK_RESPONSE;
}

export interface GetCellResponse {
  cell: Cell;
  type: MessageType.GET_CELL_RESPONSE;
}

export interface ErrorResponse {
  error: string;
  type: MessageType.ERROR_RESPONSE;
}