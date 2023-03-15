import { CellStatus } from "./cellStatus";
import { Optional } from "../types";

export default interface Cell {
  id: string;
  code: string;

  output: Optional<any>;
  output_name: string;
  input_names: string[];

  printed: Optional<string>;
  status: CellStatus;
}
