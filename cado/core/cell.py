import uuid
from typing import Any, List, Optional

from pydantic import BaseModel, Extra


def generate_id() -> str:
    return uuid.uuid4().hex


class Cell(BaseModel):
    out_var: str
    id: str = generate_id()

    parents: List["Cell"] = []
    children: List["Cell"] = []
    code: str = ""
    result: Optional[Any] = None
    expired = True

    class Config:
        extra = Extra.forbid

    def set_code(self, code: str) -> None:
        self.code = code
        self.expired = True

    def set_out_var(self, out_var: str) -> None:
        for child in self.children:
            child.expired = True
        # TODO: Check if out_var is already taken by another cell in the notebook? Maybe just do this in notebook
        self.out_var = out_var

    def run(self) -> Any:
        if self.code == "":
            raise ValueError(f"Code is empty for cell \"{self.out_var}\" ({self.id})")
        context = {}
        for parent in self.parents:
            if parent.expired:
                parent.run()
            context[parent.out_var] = parent.result

        defs = dict()
        exec(self.code, context, defs)

        if self.out_var not in defs:
            raise ValueError(f"out_var was not found in exec locals for cell \"{self.out_var}\" ({self.id})")
        self.result = defs[self.out_var]
        self.expired = False

        for child in self.children:
            child.run()

        return self.result
