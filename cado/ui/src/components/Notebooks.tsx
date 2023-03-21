import { DeleteNotebook, MessageType, NewNotebook, OpenNotebook } from "../lib/models/message";
import { FilePlus, Notebook as NotebookIcon, X } from "@phosphor-icons/react";

import NotebookDetails from "../lib/models/notebookDetails";
import { formatDateDiff } from "../lib/format";
import { sorter } from "../lib/sorting";

interface NotebooksProps {
  notebookDetails: NotebookDetails[];
  sendMessage: <M>(message: M) => void;
}

export default function Notebooks(props: NotebooksProps) {
  function openNotebook(filepath: string) {
    props.sendMessage<OpenNotebook>({
      filepath: filepath,
      type: MessageType.OPEN_NOTEBOOK,
    });
  }

  function newNotebook() {
    props.sendMessage<NewNotebook>({
      type: MessageType.NEW_NOTEBOOK,
    });
  }

  function deleteNotebook(filepath: string) {
    props.sendMessage<DeleteNotebook>({
      filepath: filepath,
      type: MessageType.DELETE_NOTEBOOK,
    });
  }

  return (
    <div className="bg-rock px-32 pb-5 pt-20">
      <div className="text-4xl">Notebooks</div>
      <div className="mt-6">
        {sorter(props.notebookDetails, (d) => d.updated).map((details) => (
          <div key={details.id} className="relative inline-block">
            <button
              className="absolute top-0 right-3 inline-block cursor-pointer rounded-full bg-lighter-rock px-1 py-1 duration-150 hover:bg-light-rock active:ease-linear"
              onClick={() => deleteNotebook(details.filepath)}
              title="Delete notebook"
            >
              <X className="" size={16} weight="bold" />
            </button>

            <div
              className="my-2 mr-4 cursor-pointer rounded-lg bg-dark-rock py-4 px-7 text-center text-gray-400 duration-150 hover:bg-darkish-rock hover:text-gray-300 active:ease-linear"
              onClick={() => openNotebook(details.filepath)}
            >
              <div className="mb-3 flex items-center">
                <NotebookIcon className="mr-2" size={24} />
                <div>{details.name}</div>
              </div>

              <div className="">{formatDateDiff(details.updated)}</div>
            </div>
          </div>
        ))}
      </div>
      <div
        className="mt-6 flex cursor-pointer items-center text-gray-400 duration-150 hover:text-gray-300 active:ease-linear"
        onClick={newNotebook}
      >
        <FilePlus className="mr-2" size={24} />
        <div>New notebook</div>
      </div>
    </div>
  );
}
