import {
  ErrorResponse,
  GetCells,
  GetCellsResponse,
  Message,
  MessageType,
  RunCellResponse,
  UpdateCellResponse,
} from "../lib/models/message";
import { useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

import Cell from "./Cell";
import CellModel from "../lib/models/cell";
import { JsonObject } from "react-use-websocket/dist/lib/types";

export default function Notebook() {
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket("ws://localhost:8000/stream");
  const [cells, setCells] = useState<CellModel[]>([]);

  function send(message: any) {
    sendJsonMessage(message as JsonObject);
  }

  function refresh() {
    const message: GetCells = {
      type: MessageType.GET_CELLS,
    };
    send(message);
  }

  useEffect(() => {
    refresh();
  }, []);

  useEffect(() => {
    if (lastJsonMessage !== null) {
      const message = JSON.parse(lastJsonMessage as unknown as string) as Message;
      console.log("Got websocket message: ", message);

      if (message.type == MessageType.GET_CELLS_RESPONSE) {
        const response = message as GetCellsResponse;
        setCells(response.cells);
      } else if (message.type == MessageType.RUN_CELL_RESPONSE) {
        const response = message as RunCellResponse;
        const newCell = response.cell;
        setCells(cells.map((c) => (c.id == newCell.id ? newCell : c)));
      } else if (message.type == MessageType.ERROR_RESPONSE) {
        const response = message as ErrorResponse;
        console.error(response);
        refresh();
      } else if (message.type == MessageType.UPDATE_CELL_RESPONSE) {
        const response = message as UpdateCellResponse;
        const newCell = response.cell;
        setCells(cells.map((c) => (c.id == newCell.id ? newCell : c)));
      } else {
        console.error("Response type did not match any known message types", message.type);
      }
    }
  }, [lastJsonMessage]);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  return (
    <div>
      {readyState === ReadyState.OPEN && (
        <div>
          {cells.map((cell, i) => (
            <Cell key={i} onSend={send} cell={cell} />
          ))}
        </div>
      )}
      {readyState !== ReadyState.OPEN && <div>The WebSocket is currently {connectionStatus}</div>}
    </div>
  );
}
