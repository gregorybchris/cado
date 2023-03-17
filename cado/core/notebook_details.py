from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel

from cado.core.notebook import Notebook


class NotebookDetails(BaseModel):
    id: UUID
    name: str
    filepath: Path
    created: datetime
    updated: datetime

    @classmethod
    def from_filepath(cls, filepath: Path) -> "NotebookDetails":
        """Load notebook details from a .cado notebook file.

        Args:
            filepath (Path): Filepath to a .cado notebook file.

        Returns:
            NotebookDetails: Loaded notebook details.
        """
        notebook = Notebook.from_filepath(filepath)
        return NotebookDetails(
            id=notebook.id,
            name=notebook.name,
            filepath=filepath,
            created=notebook.created,
            updated=notebook.updated,
        )
