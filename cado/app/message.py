from typing import Any

from pydantic import BaseModel, Extra


class Message(BaseModel):
    message: Any

    # pylint: disable=too-few-public-methods
    class Config:
        extra = Extra.forbid

    @classmethod
    def parse(cls, message: Any) -> "Message":
        """Parse message from JSON.

        Args:
            message (Any): A JSON-serialized Message object.

        Returns:
            Message: A parsed Message.
        """
        return cls.parse_obj(message)
