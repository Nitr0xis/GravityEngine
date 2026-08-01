from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from main import Engine
    from physics.circle import Circle

engine: Optional[Engine] = None
circles: list[Circle] = []
