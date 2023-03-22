import { Books, Gear, Plus } from "@phosphor-icons/react";
import { MessageType, NewCell, UpdateNotebookName } from "../lib/models/message";

import Button from "../widgets/Button";
import Notebook from "../lib/models/notebook";
import { Optional } from "../lib/types";
import SlyTextBox from "../widgets/SlyTextBox";

interface ToolbarProps {
  sendMessage: <M>(message: M) => void;
  goToNotebooks: () => void;
  notebook: Optional<Notebook>;
}

export default function Toolbar(props: ToolbarProps) {
  function newCell() {
    props.sendMessage<NewCell>({
      type: MessageType.NEW_CELL,
    });
  }

  function updateNotebookName(name: string) {
    props.sendMessage<UpdateNotebookName>({
      name: name,
      type: MessageType.UPDATE_NOTEBOOK_NAME,
    });
  }

  function goToSettings() {
    alert("Settings page not implemented yet");
  }

  return (
    <div className="flex items-center justify-between bg-dark-rock px-8">
      <div className="flex items-center py-3">
        <div className="mr-9 cursor-pointer select-none font-sen text-xl font-bold" onClick={props.goToNotebooks}>
          cado
        </div>
        {props.notebook && (
          <SlyTextBox
            value={props.notebook.name}
            placeholder=""
            onBlur={() => {}}
            onChange={(n) => updateNotebookName(n)}
          ></SlyTextBox>
        )}
      </div>
      <div className="flex items-center">
        {props.notebook && <Button onClick={newCell} tooltip="New cell" iconClass={Plus} />}
        {props.notebook && <Button onClick={props.goToNotebooks} tooltip="Notebooks" iconClass={Books} />}
        {false && <Button onClick={goToSettings} tooltip="Settings" iconClass={Gear} />}
      </div>
    </div>
  );
}
