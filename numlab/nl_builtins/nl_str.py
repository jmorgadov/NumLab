from ctypes import sizeof

from numlab.lang.type import Instance, Type

nl_bool = Type.get("bool")
nl_int = Type.get("int")
nl_str = Type.get("str")
nl_string = Type.get("str")


@nl_string.method("__new__")
def nl__new__(value: str):
    _inst = Instance(nl_string)
    _inst.set("value", str(value))
    return _inst


@nl_string.method("__add__")
def nl__add__(self, other: Instance):
    if other.type.subtype(nl_string):
        return nl__new__(self.get("value") + other.get("value"))
    raise TypeError("Cant concat string to non-string")


@nl_string.method("__iadd__")
def nl__iadd__(self, other: Instance):
    if other.type.subtype(nl_string):
        self.set("value", self.get("value") + other.get("value"))
        return self
    raise TypeError("Cant concat string to non-string")


@nl_string.method("__contains__")
def nl__contains__(self, other: Instance):
    if other.type.subtype(nl_string):
        return nl_bool(self.get("value") in other.get("value"))
    raise TypeError("Can't match string to non-string")


@nl_string.method("__eq__")
def nl__eq__(self, other: Instance):
    if other.type.subtype(nl_string):
        return nl_bool(self.get("value") == other.get("value"))
    raise TypeError("Cant compare string to non-string")


@nl_string.method("__sizeof__")
def nl__sizeof__(self):
    return nl_int(sizeof(self.get("value")))


@nl_string.method("__mul__")
def nl__mul__(self, other):
    if other.type.subtype(Type.get("int")):
        return nl__new__(self.get("value") * other.get("value"))
    raise TypeError("Can't multiply sequence by non-int")


@nl_string.method("__getitem__")
def nl__getitem__(self, other: Instance):
    if other.type.subtype(Type.get("int")):
        return self.get("value")[other.get("value")]
    raise TypeError("String indices must be integers")


@nl_string.method("__iter__")
def nl__iter__(self):
    iterator = iter(self.get("value"))
    move_next = iterator.__next__
    return Type.new("generator", move_next)


@nl_string.method("__len__")
def nl__len__(self):
    return nl_int(len(self.get("value")))


@nl_string.method("__str__")
def nl__str__(self):
    return self


@nl_string.method("__repr__")
def nl__repr__(self):
    return nl_str(f'\'{self.get("value")}\'')


@nl_string.method("__hash__")
def nl__hash__(self):
    return nl_int(hash(self.get("value")))


@nl_string.method("capitalize")
def nl_capitalize(self):
    return nl_str(self.get("value").capitalize())


@nl_string.method("isalnum")
def nl_isalnum(self):
    return nl_bool(self.get("value").isalnum())


@nl_string.method("isalpha")
def nl_isalpha(self):
    return nl_bool(self.get("value").isalpha())
