from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from circle import Circle

engine: Optional[Engine] = None
circles: list[Circle] = []
