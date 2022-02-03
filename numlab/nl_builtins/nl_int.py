from numlab.lang.type import Instance, Type

nl_int = Type.get("int")


@nl_int.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_int)
    _inst.set("value", int(value))
    return _inst


@nl_int.method("__mod__")
def nl__mod__(self: Instance, other: Instance):
    if other.type.subtype(nl_int):
        return nl__new__(self.get("value") % other.get("value"))
    raise TypeError(
        "TypeError: unsupported operand type(s) for %: 'int' and '{}'".format(
            other.type.name
        )
    )
