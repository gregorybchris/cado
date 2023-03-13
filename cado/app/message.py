from pydantic import BaseModel, Extra
from typing import Any


class Message(BaseModel):
    message: Any

    class Config:
        extra = Extra.forbid

    @classmethod
    def parse(cls, message: Any):
        return cls.parse_obj(message)
