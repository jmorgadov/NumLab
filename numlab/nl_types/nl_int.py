from numlab.lang.type import Instance, Type

nl_int = Type("int", Type.get("int"))


@nl_int.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_int)
    _inst.set("value", int(value))
    return _inst
