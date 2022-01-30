from numlab.lang.type import Instance, Type

nl_bool = Type("bool", Type.get("int"))


@nl_bool.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_bool)
    _inst.set("value", bool(value))
    return _inst
