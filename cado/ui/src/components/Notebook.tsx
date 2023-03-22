import Cell from "./Cell";
import Notebook from "../lib/models/notebook";
import { Reorder } from "framer-motion";
import { ClearCell, DeleteCell, MessageType, NewCell, ReorderCells, RunCell } from "../lib/models/message";
import CellModel from "../lib/models/cell";
import { useEffect, useState } from "react";
import { None, Optional } from "../lib/types";
import { useKeyCombos } from "../hooks/keys";

interface NotebookProps {
  notebook: Notebook;
  sendMessage: <M>(message: M) => void;
}

export default function Notebook(props: NotebookProps) {
  const [activeCell, setActiveCell] = useState<Optional<CellModel>>(None);
  const [editMode, setEditMode] = useState<boolean>(false);

  useKeyCombos(
    [
      {
        pattern: "Shift+Enter",
        callback: () => {
          if (!activeCell || editMode) return false;
          runCell(activeCell);
        },
      },
      {
        pattern: "Enter",
        callback: () => {
          if (!activeCell || editMode) return false;
          setEditMode(true);
        },
      },
      {
        pattern: "Escape",
        callback: () => {
          if (!editMode) return false;
          setEditMode(false);
        },
      },
      {
        pattern: "ArrowUp",
        callback: () => {
          if (editMode) return false;
          offsetActiveCell(-1);
        },
      },
      {
        pattern: "ArrowDown",
        callback: () => {
          if (editMode) return false;
          offsetActiveCell(1);
        },
      },
      {
        pattern: "Shift+Backspace",
        callback: () => {
          if (!activeCell || editMode) return false;
          clearCell(activeCell);
        },
      },
      {
        pattern: "Control+n",
        callback: () => {
          if (editMode) return false;
          newCell();
        },
      },
      {
        pattern: "Control+d",
        callback: () => {
          if (!activeCell || editMode) return false;
          deleteCell(activeCell);
        },
      },
      {
        pattern: "Control+a",
        callback: () => {
          if (!activeCell || editMode) return false;
          insertCell(false);
        },
      },
      {
        pattern: "Control+b",
        callback: () => {
          if (!activeCell || editMode) return false;
          insertCell(true);
        },
      },
    ],
    [activeCell, props.notebook]
  );

  useEffect(() => {
    if (props.notebook.cells.length > 0) {
      setActiveCell(props.notebook.cells[0]);
    }
  }, []);

  function runCell(cell: CellModel) {
    props.sendMessage<RunCell>({
      cell_id: cell.id,
      type: MessageType.RUN_CELL,
    });
  }

  function clearCell(cell: CellModel) {
    props.sendMessage<ClearCell>({
      cell_id: cell.id,
      type: MessageType.CLEAR_CELL,
    });
  }

  function offsetActiveCell(offset: number) {
    if (!activeCell) return;
    const cellIndex = props.notebook.cells.findIndex((c) => c.id == activeCell.id);
    if (cellIndex === None) {
      console.error("Failed to find current cell in notebook");
      return;
    }
    const newIndex = cellIndex + offset;
    if (newIndex >= props.notebook.cells.length || newIndex < 0) {
      return;
    }
    setActiveCell(props.notebook.cells[newIndex]);
  }

  function insertCell(direction: boolean) {
    if (!activeCell) return;
    const cellIndex = props.notebook.cells.findIndex((c) => c.id == activeCell.id);
    const newIndex = cellIndex + (direction ? 1 : 0);
    props.sendMessage<NewCell>({
      index: newIndex,
      type: MessageType.NEW_CELL,
    });
  }

  function newCell() {
    props.sendMessage<NewCell>({
      index: None,
      type: MessageType.NEW_CELL,
    });
  }

  function deleteCell(cell: CellModel) {
    if (activeCell) {
      const cellIndex = props.notebook.cells.findIndex((c) => c.id == activeCell.id);
      const offset = cellIndex == 0 ? 1 : -1;
      offsetActiveCell(offset);
    }
    props.sendMessage<DeleteCell>({
      cell_id: cell.id,
      type: MessageType.DELETE_CELL,
    });
  }

  function reorderCells(cells: CellModel[]) {
    props.sendMessage<ReorderCells>({
      cell_ids: cells.map((cell) => cell.id),
      type: MessageType.REORDER_CELLS,
    });
  }

  return (
    <div className="bg-rock py-5" onClick={() => setActiveCell(None)}>
      <Reorder.Group axis="y" onReorder={reorderCells} values={props.notebook.cells}>
        {props.notebook.cells.map((cell) => (
          <Cell
            key={cell.id}
            sendMessage={props.sendMessage}
            cell={cell}
            runCell={runCell}
            clearCell={clearCell}
            active={activeCell?.id == cell.id}
            editMode={editMode}
            onSetActive={() => setActiveCell(cell)}
            onSetEditMode={(editMode) => setEditMode(editMode)}
          />
        ))}
      </Reorder.Group>
    </div>
  );
}
