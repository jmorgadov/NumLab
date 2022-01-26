from numlab.lang.type import Type, Instance
from numlab.nl_types.nl_object import nl_object
from numlab.nl_types.nl_int import nl_int


nl_string = Type('int', nl_object)

nl_string.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_string)
    _inst.set('value', str(value))
    return _inst

nl_string.method("__add__")
def nl__add__(self, other: Instance):
    if other.type.subtype(nl_string):
        return nl__new__(self.value + other.value)
    raise TypeError("Can't concat string to non-string")

nl_string.method("__mul__")
def nl__mul__(self, other: nl_int):
    if other.type.subtype(nl_int):
        return nl__new__(self.value * other.value)
    raise TypeError("Can't multiply sequence by non-int")

nl_string.method("__idx__")
def nl__idx__(self, other: Instance):
    if other.type.subtype(nl_int):
        return self.value[other.value]
    raise TypeError("String indices must be integers")

nl_string.method("__iter__")
def nl__iter__(self):
    for pos in self.value:
        yield self.value[pos]

nl_string.method("__len__")
def nl__len__(self):
    return len(self.value)

nl_float.method('__str__')
def nl__str__(self):
    return self.value

nl_float.method('__repr__')
def nl__repr__(self):
    return self.value

nl_float.method('__hash__')
def nl__hash__(self):
    return hash(self.value)
