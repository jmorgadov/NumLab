from numlab.lang.type import Instance, Type

nl_bool = Type.get("bool")
nl_str = Type.get("str")
nl_float = Type.get("float")


@nl_float.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_float)
    _inst.set("value", value)
    return _inst


@nl_float.method("__bool__")
def nl__bool__(self: Instance):
    return nl_bool(self.get("value") != 0)


@nl_float.method("__add__")
def nl__add__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl__new__(self.get("value") + other.get("value"))
    raise TypeError("Can't add float to non-float")


@nl_float.method("__iadd__")
def nl__iadd__(self, other: Instance):
    if other.type.subtype(nl_float):
        self.set("value", self.get("value") + other.get("value"))
        return self
    raise TypeError("Can't add float to non-float")


@nl_float.method("__sub__")
def nl__sub__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl__new__(self.get("value") - other.get("value"))
    raise TypeError("Can't subtract float from non-float")


@nl_float.method("__isub__")
def nl__isub__(self, other: Instance):
    if other.type.subtype(nl_float):
        self.set("value", self.get("value") - other.get("value"))
        return self
    raise TypeError("Can't subtract float from non-float")


@nl_float.method("__mul__")
def nl__mul__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl__new__(self.get("value") * other.get("value"))
    raise TypeError("Can't multiply float by non-float")


@nl_float.method("__imul__")
def nl__imul__(self, other: Instance):
    if other.type.subtype(nl_float):
        self.set("value", self.get("value") * other.get("value"))
        return self
    raise TypeError("Can't multiply float by non-float")


@nl_float.method("__div__")
def nl__div__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl__new__(self.get("value") / other.get("value"))
    raise TypeError("Can't divide float by non-float")


@nl_float.method("__idiv__")
def nl__idiv__(self, other: Instance):
    if other.type.subtype(nl_float):
        self.set("value", self.get("value") / other.get("value"))
        return self
    raise TypeError("Can't divide float by non-float")


@nl_float.method("__eq__")
def nl__eq__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl_bool(self.get("value") == other.get("value"))
    raise TypeError("Can't compare float to non-float")


@nl_float.method("__lt__")
def nl__lt__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl_bool(self.get("value") < other.get("value"))
    raise TypeError("Can't compare float to non-float")


@nl_float.method("__gt__")
def nl__gt__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl_bool(self.get("value") > other.get("value"))
    raise TypeError("Can't compare float to non-float")


@nl_float.method("__le__")
def nl__le__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl_bool(self.get("value") <= other.get("value"))
    raise TypeError("Can't compare float to non-float")


@nl_float.method("__ge__")
def nl__ge__(self, other: Instance):
    if other.type.subtype(nl_float):
        return nl_bool(self.get("value") >= other.get("value"))
    raise TypeError("Can't compare float to non-float")


@nl_float.method("__str__")
def nl__str__(self):
    return nl_str(str(self.get("value")))


@nl_float.method("__repr__")
def nl__repr__(self):
    return nl_str(str(self.get("value")))


@nl_float.method("__hash__")
def nl__hash__(self):
    return hash(self.get("value"))
