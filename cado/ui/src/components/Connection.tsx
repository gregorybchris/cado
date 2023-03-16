import {
  ErrorResponse,
  GetCellResponse,
  GetNotebook,
  GetNotebookResponse,
  Message,
  MessageType,
} from "../lib/models/message";
import { None, Optional } from "../lib/types";
import NotebookModel, { updateNotebookCell } from "../lib/models/notebook";
import { useEffect, useRef, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

import CadoImage from "../images/cado.png";
import Disconnect from "./Disconnect";
import Notebook from "./Notebook";
import Toolbar from "./Toolbar";
import useImagePreloader from "../hooks/image";

export default function Connection() {
  const didUnmount = useRef(false);
  const { sendMessage, lastMessage, readyState } = useWebSocket("ws://localhost:8000/stream", {
    shouldReconnect: (closeEvent) => {
      return didUnmount.current === false;
    },
    reconnectAttempts: 150,
    reconnectInterval: 2000,
  });
  const [notebook, setNotebook] = useState<Optional<NotebookModel>>(None);
  useImagePreloader([CadoImage]);

  useEffect(() => {
    return () => {
      didUnmount.current = true;
    };
  }, []);

  function send<M>(message: M) {
    console.log("Sending message: ", message);
    sendMessage(JSON.stringify(message));
  }

  function loadNotebook() {
    send<GetNotebook>({
      type: MessageType.GET_NOTEBOOK,
    });
  }

  useEffect(() => {
    loadNotebook();
  }, []);

  useEffect(() => {
    if (lastMessage !== null) {
      const messageJson = JSON.parse(JSON.parse(lastMessage.data));
      const message = messageJson as Message;
      console.log("Got websocket message: ", message);

      if (message.type == MessageType.GET_NOTEBOOK_RESPONSE) {
        const response = message as GetNotebookResponse;
        setNotebook(response.notebook);
      } else if (message.type == MessageType.GET_CELL_RESPONSE) {
        const response = message as GetCellResponse;
        if (!notebook) {
          console.error("No notebook found");
          return;
        }
        setNotebook(updateNotebookCell(notebook, response.cell));
      } else if (message.type == MessageType.ERROR_RESPONSE) {
        const response = message as ErrorResponse;
        console.error(response);
        loadNotebook();
      } else {
        console.error("Response type did not match any known message types", message.type);
      }
    }
  }, [lastMessage]);

  return (
    <div>
      <Toolbar sendMessage={send} />
      {readyState === ReadyState.OPEN && notebook && <Notebook notebook={notebook} sendMessage={send} />}
      {readyState !== ReadyState.OPEN && <Disconnect image={CadoImage} />}
    </div>
  );
}
