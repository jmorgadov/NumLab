from __future__ import annotations

from typing import List


class Attribute:
    def __init__(self, attr_name: str, atrr_type: Type):
        self.name = attr_name
        self.type = atrr_type


class Function:
    def __init__(
        self, func_name: str, func_type: Type, func_args: List[Attribute]
    ):
        self.name = func_name
        self.type = func_type
        self.args = func_args


class Type:
    def __init__(self, type_name: str):
        self.type_name = type_name
        self.attributes = []
        self.methods = []

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)

    def add_method(self, func: Function):
        self.methods.append(func)

    def get_attribute(self, attribute_name: str):
        for attribute in self.attributes:
            if attribute.name == attribute_name:
                return attribute
        return None

    def get_func(self, func_name: str):
        for func in self.methods:
            if func.name == func_name:
                return func
        return None
