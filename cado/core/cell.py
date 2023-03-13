import uuid
from typing import Any, List, Mapping, Optional

from pydantic import BaseModel, Extra


class Cell(BaseModel):
    out_var: str
    id: str = uuid.uuid4().hex

    parents: List["Cell"] = []
    children: List["Cell"] = []
    code: str = ""
    result: Optional[Any] = None
    expired = True

    # pylint: disable=too-few-public-methods
    class Config:
        extra = Extra.forbid

    def set_code(self, code: str) -> None:
        """Set the cell's code block.

        Args:
            code (str): Code the cell should contain.
        """
        self.code = code
        self.expired = True

    def set_out_var(self, out_var: str) -> None:
        """Set the name of the output variable.

        Args:
            out_var (str): The new name of the output variable.
        """
        for child in self.children:
            child.expired = True
        # TODO: Check if out_var is already taken by another cell in the notebook? Maybe just do this in notebook
        self.out_var = out_var

    def run(self) -> Any:
        """Run the cell.

        Returns:
            Any: The result of running the cell.
        """
        if self.code == "":
            raise ValueError(f"Code is empty for cell \"{self.out_var}\" ({self.id})")
        context = {}
        for parent in self.parents:
            if parent.expired:
                parent.run()
            context[parent.out_var] = parent.result

        defs: Mapping[str, object] = {}
        # pylint: disable=exec-used
        exec(self.code, context, defs)

        if self.out_var not in defs:
            raise ValueError(f"out_var was not found in exec locals for cell \"{self.out_var}\" ({self.id})")
        self.result = defs[self.out_var]
        self.expired = False

        for child in self.children:
            child.run()

        return self.result
