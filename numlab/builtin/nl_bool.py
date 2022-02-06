from numlab.lang.type import Instance, Type

nl_bool = Type.get("bool")


@nl_bool.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_bool)
    _inst.set("value", bool(value))
    return _inst


@nl_bool.method("__bool__")
def nl__bool__(self: Instance):
    return self
