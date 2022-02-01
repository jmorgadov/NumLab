from numlab.lang.type import Instance, Type

nl_object = Type.get("object")


@nl_object.method("__new__")
def nl__new__(cls, *args, **kwargs):
    inst = Instance(nl_object)
    inst.get("__init__")(inst, *args, **kwargs)
    return inst


@nl_object.method("__init__")
def nl__init__(self, *args, **kwargs):
    pass


@nl_object.method("__str__")
def nl__str__(self):
    return self.get("__repr__")(self)


@nl_object.method("__repr__")
def nl__repr__(self):
    return Type.get("str")(
        f"<NumLab instance of type {self.type.type_name} at {hex(id(self))}>"
    )
