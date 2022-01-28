from numlab.lang.type import Type, Instance
from numlab.nl_types.nl_object import nl_object
from numlab.nl_types.nl_int import nl_int
from numlab.nl_types.nl_bool import nl_bool
from numlab.nl_types.nl_slice import nl_slice

nl_tuple = Type('tuple', nl_object)

@nl_tuple.method('__new__')
def nl__new__(value: set):
    _inst = Instance(nl_tuple)
    _inst.set('value', tuple(value))
    return _inst

@nl_tuple.method('__contains__')
def nl__contains__(self, indx: Instance):
    if indx.type.subtype(nl_int):
        return nl_bool.__new__(indx.value in self.value)
    raise TypeError('Tuple indices must be integers')

@nl_tuple.method('__getitem__')
def nl__getitem__(self, indx: Instance):
    if indx.type.subtype(nl_int):
        return nl_object.__new(self.value[indx])
    if indx.type.subtype(nl_slice):
        low = indx.low if indx.low is not None else 0
        up = indx.up if indx.low is not None else len(self.value)
        step = indx.step if indx.low is not None else 0
        if not isinstance(low, int) and not low.type.subtype(nl_int):
            raise TypeError(f"Slice indices must be integers, not {low.type}")
        if not isinstance(up, int) and not up.type.subtype(nl_int):
            raise TypeError(f"Slice indices must be integers, not {up.type}")
        if not isinstance(step, int) and not step.type.subtype(nl_int):
            raise TypeError(f"Slice indices must be integers, not {step.type}")
        return nl_tuple.__new__(self.value[low:up:step])
    raise TypeError(f"Tuple indices must be integer or slice, not {indx.type}")

@nl_tuple.method('__iter__')
def nl__iter__(self):
    for elem in self.value:
        yield nl_object.__new__(elem)

@nl_tuple.method('__len__')
def nl__len__(self):
    return nl_int.__new__(len(self.value))

@nl_tuple.method('__add__')
def nl__add__(self, other: Instance):
    if other.type.subtype(nl_tuple):
        return nl_tuple.__new__(self.value + other.value)
    raise TypeError("Can't concatenate tuple with non-tuple")

@nl_tuple.method('__mul__')
def nl__mul__(self, value: Instance):
    if value.type.subtype(nl_int):
        return nl_tuple.__new__(self.value * value.value)
    raise TypeError("Can't multiply tuple with non-integers")

@nl_tuple.method('count')
def nl_count(self, value: Instance):
    if value.type.subtype(nl_object):
        return nl_int.__new__(self.value.count(value.value))

@nl_tuple.method('index')
def nl_count(self, value: Instance, start: Instance):
    if value.type.subtype(nl_object):
        if start.type.subtype(nl_int):
            start_indx = start.value if start.value is not None else 0
            return nl_int.__new__(self.value.index(value.value, start_indx))

