import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
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

    stdout: Optional[str] = None
    stderr: Optional[str] = None
    status: CellStatus = CellStatus.EXPIRED

    def run(self, context: Dict[str, Any]) -> None:
        """Run the cell.

        Returns:
            Any: The output of running the cell.
        """
        if self.code == "":
            error = ValueError(f"Code is empty for cell \"{self.id}\"")
            self.set_error(error)
            raise error

        exec_locals: Mapping[str, object] = {}
        try:

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                # pylint: disable=exec-used
                exec(self.code, context, exec_locals)

            self.stdout = stdout.getvalue().rstrip()
            self.stderr = stderr.getvalue().rstrip()
        except Exception as exc:
            error = ValueError(f"Failed to exec: {traceback.format_exc()}")
            self.set_error(error)
            raise error from exc

        if self.output_name != "":
            # Check that a variable with the cell output name was emitted by exec
            if self.output_name not in exec_locals:
                error = ValueError(
                    f"Cell name \"{self.output_name}\" was not found in exec locals for cell ({self.id})")
                self.set_error(error)
                raise error
            self.output = exec_locals[self.output_name]
        self.status = CellStatus.OK

    def clear(self) -> None:
        """Clear the cell outputs and set the status to expired."""
        self.output = None
        self.stdout = None
        self.stderr = None
        self.status = CellStatus.EXPIRED

    def set_error(self, error: ValueError) -> None:
        """Clear the cell outputs and set the status to error."""
        self.output = None
        self.status = CellStatus.ERROR
        self.stderr = str(error).rstrip()
