import { Books, Gear, Plus } from "@phosphor-icons/react";
import { MessageType, NewCell } from "../lib/models/message";

import Button from "../widgets/Button";

interface ToolbarProps {
  sendMessage: <M>(message: M) => void;
}

export default function Toolbar(props: ToolbarProps) {
  function newCell() {
    props.sendMessage<NewCell>({
      type: MessageType.NEW_CELL,
    });
  }

  function goToLibrary() {
    alert("Library page not implemented yet");
  }

  function goToSettings() {
    alert("Settings page not implemented yet");
  }

  return (
    <div className="mb-5 flex items-center justify-between bg-dark-rock px-8">
      <div className="flex items-center">
        <div className="mr-5 select-none py-4 font-sen text-xl font-bold">Cado</div>
        <div
          className="mr-5 cursor-pointer rounded-md bg-rock py-2 px-4 duration-150 hover:bg-light-rock hover:ease-linear"
          onClick={newCell}
        >
          <Plus weight="bold" />
        </div>
      </div>
      <div className="flex items-center">
        <Button onClick={goToLibrary} tooltip="Library" iconClass={Books} />
        <Button onClick={goToSettings} tooltip="Settings" iconClass={Gear} />
      </div>
    </div>
  );
}
