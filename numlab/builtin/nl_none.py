from numlab.lang.type import Instance, Type

nl_bool = Type.get("bool")
nl_none = Type.get("none")


@nl_none.method("__new__")
def nl__new__():
    _inst = Instance(nl_none)
    return _inst


@nl_none.method("__bool__")
def nl__bool__(self: Instance):
    return nl_bool(False)
