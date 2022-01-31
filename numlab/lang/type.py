from __future__ import annotations

from typing import Any, Callable, Dict, List


class Type:
    nl_types = {}

    def __init__(self, type_name: str, parent: Type = None):
        self.type_name = type_name
        self.attributes: Dict[str, Any] = {}
        self.parent = parent
        Type.nl_types[type_name] = self

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
            all_attrs.update(self.parent.get_attr_dict())
        all_attrs.update(self.attributes)
        return all_attrs

    def subtype(self, other: Type):
        if self.type_name == other.type_name:
            return True
        if self.parent is None:
            return False
        return self.parent.subtype(other)

    def __call__(self, *args, **kwargs):
        return self.attributes["__new__"](*args, **kwargs)

    @staticmethod
    def new(type_name: str, *args, **kwargs):
        if type_name not in Type.nl_types:
            raise ValueError(f"{type_name} is not a valid NumLab type")
        return Type.nl_types[type_name](*args, **kwargs)

    @staticmethod
    def get(type_name: str):
        if type_name not in Type.nl_types:
            raise ValueError(f"{type_name} is not a valid NumLab type")
        return Type.nl_types[type_name]


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

    def get_value(self):
        if self.type.type_name in ["int", "float", "bool", "str"]:
            return self.get("__new__")(self.get("value"))
        return self

    def __repr__(self):
        return self.get("__repr__")(self).get("value")

nl_object = Type("object")
nl_float = Type("float")
nl_int = Type("int", nl_float)
nl_bool = Type("bool", nl_int)
nl_str = Type("str")
nl_dict = Type("dict")
nl_list = Type("list")
nl_tuple = Type("tuple")
nl_set = Type("set")
nl_slice = Type("slice")
nl_function = Type("function")
nl_generator = Type("generator")


