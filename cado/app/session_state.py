from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cado.core.notebook import Notebook


@dataclass
class SessionState:
    notebook: Optional[Notebook] = None
    filepath: Optional[Path] = None
