import Cell from "./cell";
import { Language } from "./language";
import Notebook from "./notebook";
import NotebookDetails from "./notebookDetails";
import { Optional } from "../types";

export enum MessageType {
  // publish
  GET_NOTEBOOK = "get-notebook",
  UPDATE_CELL_CODE = "update-cell-code",
  UPDATE_CELL_OUTPUT_NAME = "update-cell-output-name",
  UPDATE_CELL_INPUT_NAMES = "update-cell-input-names",
  UPDATE_CELL_LANGUAGE = "update-cell-language",
  RUN_CELL = "run-cell",
  CLEAR_CELL = "clear-cell",
  NEW_CELL = "new-cell",
  DELETE_CELL = "delete-cell",
  REORDER_CELLS = "reorder-cells",
  LIST_NOTEBOOKS = "list-notebooks",
  NEW_NOTEBOOK = "new-notebook",
  DELETE_NOTEBOOK = "delete-notebook",
  OPEN_NOTEBOOK = "open-notebook",
  EXIT_NOTEBOOK = "exit-notebook",
  UPDATE_NOTEBOOK_NAME = "update-notebook-name",

  // subscribe
  GET_NOTEBOOK_RESPONSE = "get-notebook-response",
  GET_CELL_RESPONSE = "get-cell-response",
  ERROR_RESPONSE = "error-response",
  LIST_NOTEBOOKS_RESPONSE = "list-notebooks-response",
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

export interface UpdateCellLanguage {
  cell_id: string;
  language: Language;
  type: MessageType.UPDATE_CELL_LANGUAGE;
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
  index: Optional<number>;
  type: MessageType.NEW_CELL;
}

export interface DeleteCell {
  cell_id: string;
  type: MessageType.DELETE_CELL;
}

export interface ReorderCells {
  cell_ids: string[];
  type: MessageType.REORDER_CELLS;
}

export interface ListNotebooks {
  type: MessageType.LIST_NOTEBOOKS;
}

export interface NewNotebook {
  type: MessageType.NEW_NOTEBOOK;
}

export interface DeleteNotebook {
  filepath: string;
  type: MessageType.DELETE_NOTEBOOK;
}

export interface OpenNotebook {
  filepath: string;
  type: MessageType.OPEN_NOTEBOOK;
}

export interface ExitNotebook {
  type: MessageType.EXIT_NOTEBOOK;
}

export interface UpdateNotebookName {
  name: string;
  type: MessageType.UPDATE_NOTEBOOK_NAME;
}

export interface GetNotebookResponse {
  notebook: Optional<Notebook>;
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

export interface ListNotebooksResponse {
  notebook_details: NotebookDetails[];
  type: MessageType.LIST_NOTEBOOKS;
}
