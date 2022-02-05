from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from numlab.lang.type import Instance, Type


class Context:
    def __init__(self, parent: Context = None):
        self.parent: Context = parent
        self.symbols: Dict[str, Any] = {}
        self.var_count: int = 0

    def make_child(self) -> Context:
        return Context(self)

    def _is_countable(self, name, value):
        return (
            not isinstance(value, Type)
            and isinstance(value, Instance)
            and not value.type.subtype(Type.get("function"))
            and name != "stats"
        )

    def define(self, name: str, value: Any):
        current = self.symbols.get(name, None)
        if current is not None and self._is_countable(name, current):
            self.var_count -= 1

        if self._is_countable(name, value):
            self.var_count += 1
        self.symbols[name] = value

    def delete(self, name):
        if name not in self.symbols:
            if self.parent:
                self.parent.delete(name)
            else:
                raise Exception(f"Undefined variable {name}")
            return
        val = self.symbols[name]
        if self._is_countable(name, val):
            self.var_count -= 1
        if name in self.symbols:
            del self.symbols[name]

    def resolve(self, name: str) -> Optional[Any]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None

    def count_vars(self) -> int:
        count = self.var_count
        if self.parent:
            count += self.parent.count_vars()
        return count
