import traceback
from typing import Any, List, Mapping, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cado.core.cell_status import CellStatus


class Cell(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    code: str = ""

    output_name: str
    output: Optional[Any] = None
    input_names: List[str] = []

    parents: List["Cell"] = []
    children: List["Cell"] = []
    printed: Optional[str] = None
    status: CellStatus = CellStatus.ERROR

    def set_status(self, status: CellStatus) -> None:
        """Set the cell's status.

        Args:
            status (CellStatus): New cell status.
        """
        self.status = status

    def set_code(self, code: str) -> None:
        """Set the cell's code block.

        Args:
            code (str): Code the cell should contain.
        """
        self.status = CellStatus.EXPIRED
        self.output = None
        self.printed = None
        self.code = code

    def set_output_name(self, output_name: str) -> None:
        """Set the output name of the cell.

        Args:
            output_name (str): The new output_name of the cell.
        """
        if self.output_name == output_name:
            return

        self.output_name = output_name
        self.output = None
        self.printed = None

        if output_name == "":
            self.status = CellStatus.ERROR
            raise ValueError(f"Cell name for cell ({self.id}) is empty")

        self.status = CellStatus.EXPIRED
        for child in self.children:
            child.status = CellStatus.EXPIRED
        # TODO: Check if name is already taken by another cell in the notebook? Maybe just do this in notebook

    def run(self) -> None:
        """Run the cell.

        Returns:
            Any: The output of running the cell.
        """
        self.status = CellStatus.OK
        if self.code == "":
            self.output = None
            self.printed = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Code is empty for cell {self.id} (name=\"{self.output_name}\")")
        context = {}
        for parent in self.parents:
            if parent.status == CellStatus.EXPIRED:
                parent.run()
            context[parent.output_name] = parent.output

        defs: Mapping[str, object] = {}
        try:
            # pylint: disable=exec-used
            exec(self.code, context, defs)
        except Exception:
            self.output = None
            self.printed = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Failed to exec: {traceback.format_exc()}")

        if self.output_name not in defs:
            self.output = None
            self.printed = None
            self.status = CellStatus.ERROR
            raise ValueError(f"Cell name \"{self.output_name}\" was not found in exec locals for cell ({self.id})")
        self.output = defs[self.output_name]
        self.status = CellStatus.OK

        for child in self.children:
            child.run()

    def clear(self) -> None:
        self.output = None
        self.printed = None
