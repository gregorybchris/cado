import uuid
from enum import Enum
from typing import Any, List, Mapping, Optional

from pydantic import BaseModel


class CellStatus(Enum):
    OK = "ok"
    DONE = "done"
    RUNNING = "running"
    ERROR = "error"


class Cell(BaseModel):
    name: str
    id: str = uuid.uuid4().hex

    parents: List["Cell"] = []
    children: List["Cell"] = []
    code: str = ""
    result: Optional[Any] = None
    output: Optional[str] = None
    status: CellStatus = CellStatus.OK
    expired = True

    def set_code(self, code: str) -> None:
        """Set the cell's code block.

        Args:
            code (str): Code the cell should contain.
        """
        self.status = CellStatus.OK
        self.result = None
        self.output = None
        self.code = code
        self.expired = True

    def set_name(self, name: str) -> None:
        """Set the name of the cell.

        Args:
            name (str): The new name of the cell.
        """
        self.status = CellStatus.OK
        self.result = None
        self.output = None
        for child in self.children:
            child.expired = True
        # TODO: Check if name is already taken by another cell in the notebook? Maybe just do this in notebook
        self.name = name

    def run(self) -> None:
        """Run the cell.

        Returns:
            Any: The result of running the cell.
        """
        self.status = CellStatus.OK
        if self.code == "":
            self.result = None
            self.output = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Code is empty for cell {self.id} (name=\"{self.name}\")")
        context = {}
        for parent in self.parents:
            if parent.expired:
                parent.run()
            context[parent.name] = parent.result

        defs: Mapping[str, object] = {}
        # pylint: disable=exec-used
        exec(self.code, context, defs)

        if self.name not in defs:
            self.result = None
            self.output = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Cell name \"{self.name}\" was not found in exec locals for cell ({self.id})")
        self.result = defs[self.name]
        self.expired = False

        for child in self.children:
            child.run()
