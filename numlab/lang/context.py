from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from numlab.lang.type import Type


class Context:
    def __init__(self, parent: Context = None):
        self.parent: Context = parent
        self.symbols: Dict[str, Any] = {}

    def make_child(self) -> Context:
        return Context(self)

    def define(self, name: str, value: Any):
        self.symbols[name] = value

    def resolve(self, name: str) -> Optional[Any]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None
