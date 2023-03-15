import traceback
from typing import Any, Dict, List, Mapping, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cado.core.cell_status import CellStatus


class Cell(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    code: str = ""

    output_name: str
    output: Optional[Any] = None
    input_names: List[str] = []

    printed: Optional[str] = None
    status: CellStatus = CellStatus.EXPIRED

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
        self.code = code

    def set_output_name(self, output_name: str) -> None:
        """Set the output name of the cell.

        Args:
            output_name (str): The new output_name of the cell.
        """
        self.output_name = output_name

    def set_input_names(self, input_names: List[str]) -> None:
        """Set the input names of the cell.

        Args:
            input_names (List[str]): The new input_names of the cell.
        """
        self.input_names = input_names

    def run(self, context: Dict[str, Any]) -> None:
        """Run the cell.

        Returns:
            Any: The output of running the cell.
        """
        if self.code == "":
            self.set_error()
            raise ValueError(f"Code is empty for cell \"{self.id}\"")
        if self.output_name == "":
            self.set_error()
            raise ValueError(f"No output name set for cell \"{self.id}\"")

        exec_locals: Mapping[str, object] = {}
        try:
            # pylint: disable=exec-used
            exec(self.code, context, exec_locals)
        except Exception as exc:
            self.set_error()
            raise ValueError(f"Failed to exec: {traceback.format_exc()}") from exc

        # Check that a variable with the cell output name was emitted by exec
        if self.output_name not in exec_locals:
            self.set_error()
            raise ValueError(f"Cell name \"{self.output_name}\" was not found in exec locals for cell ({self.id})")
        self.output = exec_locals[self.output_name]
        self.set_status(CellStatus.OK)

    def clear(self) -> None:
        """Clear the cell outputs and set the status to expired."""
        self.output = None
        self.printed = None
        self.set_status(CellStatus.EXPIRED)

    def set_error(self) -> None:
        """Clear the cell outputs and set the status to error."""
        self.output = None
        self.set_status(CellStatus.ERROR)
