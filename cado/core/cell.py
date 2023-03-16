import traceback
from typing import Any, Dict, List, Mapping, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cado.core.cell_status import CellStatus
from cado.core.language import Language


class Cell(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    code: str = ""

    output_name: str
    output: Optional[Any] = None
    input_names: List[str] = []
    language: Language = Language.PYTHON

    printed: Optional[str] = None
    status: CellStatus = CellStatus.EXPIRED

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
        self.status = CellStatus.OK

    def clear(self) -> None:
        """Clear the cell outputs and set the status to expired."""
        self.output = None
        self.printed = None
        self.status = CellStatus.EXPIRED

    def set_error(self) -> None:
        """Clear the cell outputs and set the status to error."""
        self.output = None
        self.status = CellStatus.ERROR
