from numlab.lang.type import Type, Instance
from numlab.nl_types.nl_object import nl_object
from numlab.nl_types.nl_int import nl_int
from ctypes import sizeof


nl_string = Type('int', nl_object)

nl_string.method('__new__')
def nl__new__(value: str):
    _inst = Instance(nl_string)
    _inst.set('value', str(value))
    return _inst

nl_string.method('__add__')
def nl__add__(self, other: Instance):
    if other.type.subtype(nl_string):
        return nl__new__(self.value + other.value)
    raise TypeError("Cant concat string to non-string")

nl_string.method('__contains__')
def nl__contains__(self, other: Instance):
    if other.type.subtype(nl_string):
        return other.value in other.value
    raise TypeError("Cant match string to non-string")

nl_string.method('__eq__')
def nl__eq__(self, other: Instance):
    if other.type.subtype(nl_string):
        return self.value == other.value
    raise TypeError("Cant compare string to non-string")
    
nl_string.method('__sizeof__')
def nl__sizeof__(self):
    return sizeof(self.value)

nl_string.method('__mul__')
def nl__mul__(self, other: nl_int):
    if other.type.subtype(nl_int):
        return nl__new__(self.value * other.value)
    raise TypeError("Can't multiply sequence by non-int")

nl_string.method('__getitem__')
def nl__getitem__(self, other: Instance):
    if other.type.subtype(nl_int):
        return self.value[other.value]
    raise TypeError('String indices must be integers')

nl_string.method('__iter__')
def nl__iter__(self):
    for pos in self.value:
        yield self.value[pos]

nl_string.method('__len__')
def nl__len__(self):
    return len(self.value)

nl_string.method('__str__')
def nl__str__(self):
    return self.value

nl_string.method('__repr__')
def nl__repr__(self):
    return self.value

nl_string.method('__hash__')
def nl__hash__(self):
    return hash(self.value)

nl_string.method('capitalize')
def nl_capitalize(self):
    return nl__new__(str.capitalize(self.value))

nl_string.method('isalnum')
def nl_isalnum(self):
    return str.isalnum(self.value)

nl_string.method('isalpha')
def nl_isalpha(self):
    return str.isalpha(self.value)

# nl_string.method('join')
# def nl_join(self, iterable: Instance):
#     if iterable.type.subtype(nl_string):
#         return nl__new__(join(self.value, iterable))