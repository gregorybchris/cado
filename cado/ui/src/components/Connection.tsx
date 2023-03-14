import {
  ClearCellResponse,
  ErrorResponse,
  GetNotebook,
  GetNotebookResponse,
  Message,
  MessageType,
  NewCellResponse,
  RunCellResponse,
  UpdateCellResponse,
} from "../lib/models/message";
import { useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

import CellModel from "../lib/models/cell";
import { JsonObject } from "react-use-websocket/dist/lib/types";
import Notebook from "./Notebook";
import Toolbar from "./Toolbar";

export default function Connection() {
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket("ws://localhost:8000/stream");
  const [cells, setCells] = useState<CellModel[]>([]);

  function sendMessage<M>(message: M) {
    console.log("Sending message: ", message);
    sendJsonMessage(message as JsonObject);
  }

  function serverSync() {
    sendMessage<GetNotebook>({
      type: MessageType.GET_NOTEBOOK,
    });
  }

  useEffect(() => {
    serverSync();
  }, []);

  useEffect(() => {
    if (lastJsonMessage !== null) {
      const message = JSON.parse(lastJsonMessage as unknown as string) as Message;
      console.log("Got websocket message: ", message);

      if (message.type == MessageType.GET_NOTEBOOK_RESPONSE) {
        const response = message as GetNotebookResponse;
        setCells(response.notebook.cells);
      } else if (message.type == MessageType.RUN_CELL_RESPONSE) {
        const response = message as RunCellResponse;
        const updatedCell = response.cell;
        setCells(cells.map((c) => (c.id == updatedCell.id ? updatedCell : c)));
      } else if (message.type == MessageType.ERROR_RESPONSE) {
        const response = message as ErrorResponse;
        console.error(response);
        serverSync();
      } else if (message.type == MessageType.UPDATE_CELL_RESPONSE) {
        const response = message as UpdateCellResponse;
        const updatedCell = response.cell;
        setCells(cells.map((c) => (c.id == updatedCell.id ? updatedCell : c)));
      } else if (message.type == MessageType.NEW_CELL_RESPONSE) {
        const response = message as NewCellResponse;
        const newCell = response.cell;
        setCells([...cells, newCell]);
      } else if (message.type == MessageType.CLEAR_CELL_RESPONSE) {
        const response = message as ClearCellResponse;
        const updatedCell = response.cell;
        setCells(cells.map((c) => (c.id == updatedCell.id ? updatedCell : c)));
      } else {
        console.error("Response type did not match any known message types", message.type);
      }
    }
  }, [lastJsonMessage]);

  return (
    <div>
      <Toolbar sendMessage={sendMessage} />
      {readyState === ReadyState.OPEN && <Notebook cells={cells} sendMessage={sendMessage} />}
      {readyState !== ReadyState.OPEN && <div className="px-8">Could not connect to the Cado sever</div>}
    </div>
  );
}
