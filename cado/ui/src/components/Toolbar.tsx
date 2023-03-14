import { MessageType, NewCell } from "../lib/models/message";

import { Plus } from "@phosphor-icons/react";

interface ToolbarProps {
  sendMessage: <M>(message: M) => void;
}

export default function Toolbar(props: ToolbarProps) {
  function newCell() {
    props.sendMessage<NewCell>({
      type: MessageType.NEW_CELL,
    });
  }

  return (
    <div className="mb-5 flex items-center bg-dark-rock px-8">
      <div className="mr-5 select-none py-4 text-xl font-bold">Cado</div>
      <div
        className="mr-5 cursor-pointer rounded-md bg-rock py-2 px-4 duration-150 hover:bg-light-rock hover:ease-linear"
        onClick={newCell}
      >
        <Plus weight="bold" />
      </div>
    </div>
  );
}
