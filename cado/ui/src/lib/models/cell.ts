import { CellStatus } from "./cellStatus";
import { Language } from "./language";
import { Optional } from "../types";

export default interface Cell {
  id: string;
  code: string;

  output: Optional<any>;
  output_name: string;
  input_names: string[];
  language: Language;

  stdout: Optional<string>;
  stderr: Optional<string>;
  status: CellStatus;
}
