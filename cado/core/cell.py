import traceback
from enum import Enum
from typing import Any, List, Mapping, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CellStatus(Enum):
    OK = "ok"
    EXPIRED = "expired"
    RUNNING = "running"
    ERROR = "error"


class Cell(BaseModel):
    name: str
    id: UUID = Field(default_factory=uuid4)

    parents: List["Cell"] = []
    children: List["Cell"] = []
    code: str = ""
    result: Optional[Any] = None
    output: Optional[str] = None
    status: CellStatus = CellStatus.EXPIRED

    def set_code(self, code: str) -> None:
        """Set the cell's code block.

        Args:
            code (str): Code the cell should contain.
        """
        self.status = CellStatus.EXPIRED
        self.result = None
        self.output = None
        self.code = code

    def set_name(self, name: str) -> None:
        """Set the name of the cell.

        Args:
            name (str): The new name of the cell.
        """
        if name == "":
            self.name = name
            self.status = CellStatus.ERROR
            self.result = None
            self.output = None
            raise ValueError(f"Cell name for cell ({self.id}) is empty")

        self.status = CellStatus.EXPIRED
        self.result = None
        self.output = None
        for child in self.children:
            child.status = CellStatus.EXPIRED
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
            if parent.status == CellStatus.EXPIRED:
                parent.run()
            context[parent.name] = parent.result

        defs: Mapping[str, object] = {}
        try:
            # pylint: disable=exec-used
            exec(self.code, context, defs)
        except Exception:
            self.result = None
            self.output = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Failed to exec: {traceback.format_exc()}")

        if self.name not in defs:
            self.result = None
            self.output = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Cell name \"{self.name}\" was not found in exec locals for cell ({self.id})")
        self.result = defs[self.name]
        self.status = CellStatus.OK

        for child in self.children:
            child.run()

    def clear(self) -> None:
        self.result = None
        self.output = None
        self.status = CellStatus.EXPIRED
