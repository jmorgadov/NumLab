from __future__ import annotations

from typing import Any, Callable, Dict, List


class Type:
    def __init__(self, type_name: str, parent: Type = None):
        self.type_name = type_name
        self.attributes: Dict[str, Any] = {}
        self.parent = parent

    def add_attribute(self, attribute: str, default: Any = None):
        self.attributes[attribute] = default

    def method(self, method_name: str):
        def method_wrapper(func):
            self.add_attribute(method_name, func)
            return func
        return method_wrapper

    def get_attribute(self, attribute_name: str):
        for attribute in self.attributes:
            if attribute.name == attribute_name:
                return attribute
        return None

    def get_attr_dict(self):
        all_attrs = {}
        if self.parent:
            all_attrs.update(self.parent.get_all())
        all_attrs.update(self.attributes)
        return all_attrs


    def subtype(self, other: Type):
        if self.type_name == other.type_name:
            return True
        if self.parent is None:
            return False
        return self.parent.subtype(other)


class Instance:
    def __init__(self, _type: Type):
        self.type = _type
        self._dict = self.type.get_attr_dict()
        self._dict["__dict__"] = self._dict

    def get(self, attr_name):
        if attr_name not in self._dict:
            raise ValueError(f"{self.type.type_name} has no attribute {attr_name}")
        return self._dict[attr_name]

    def set(self, attr_name, value):
        self._dict[attr_name] = value
