import {
  ErrorResponse,
  ExitNotebook,
  GetCellResponse,
  GetNotebook,
  GetNotebookResponse,
  ListNotebooks,
  ListNotebooksResponse,
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
import NotebookDetails from "../lib/models/notebookDetails";
import Notebooks from "./Notebooks";
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
  const [currentNotebook, setCurrentNotebook] = useState<Optional<NotebookModel>>(None);
  const [notebookDetails, setNotebookDetails] = useState<NotebookDetails[]>([]);
  useImagePreloader([CadoImage]);

  useEffect(() => {
    return () => {
      didUnmount.current = true;
    };
  }, []);

  function send<M>(message: M) {
    console.log("Sending client message: ", message);
    sendMessage(JSON.stringify(message));
  }

  function loadNotebook() {
    send<GetNotebook>({
      type: MessageType.GET_NOTEBOOK,
    });
  }

  function listNotebooks() {
    send<ListNotebooks>({
      type: MessageType.LIST_NOTEBOOKS,
    });
  }

  function goToNotebooks() {
    send<ExitNotebook>({
      type: MessageType.EXIT_NOTEBOOK,
    });
  }

  useEffect(() => {
    listNotebooks();
  }, []);

  useEffect(() => {
    if (lastMessage !== null) {
      const messageJson = JSON.parse(JSON.parse(lastMessage.data));
      const message = messageJson as Message;
      console.log("Received server message: ", message);

      if (message.type == MessageType.GET_NOTEBOOK_RESPONSE) {
        const response = message as GetNotebookResponse;
        if (!response.notebook) {
          listNotebooks();
        }
        setCurrentNotebook(response.notebook);
      } else if (message.type == MessageType.LIST_NOTEBOOKS_RESPONSE) {
        const response = message as ListNotebooksResponse;
        setNotebookDetails(response.notebook_details);
      } else if (message.type == MessageType.GET_CELL_RESPONSE) {
        const response = message as GetCellResponse;
        if (!currentNotebook) {
          console.error("No notebook found");
          return;
        }
        setCurrentNotebook(updateNotebookCell(currentNotebook, response.cell));
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
      <Toolbar sendMessage={send} goToNotebooks={goToNotebooks} notebook={currentNotebook} />
      {readyState === ReadyState.OPEN && currentNotebook && <Notebook notebook={currentNotebook} sendMessage={send} />}
      {readyState === ReadyState.OPEN && !currentNotebook && (
        <Notebooks notebookDetails={notebookDetails} sendMessage={send} />
      )}
      {readyState !== ReadyState.OPEN && <Disconnect image={CadoImage} />}
    </div>
  );
}
