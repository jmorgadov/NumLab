from numlab.lang.type import Instance, Type

nl_object = Type.get("object")


@nl_object.method("__new__")
def nl__new__():
    return Instance(nl_object)


@nl_object.method("__init__")
def nl__init__(self):
    pass


@nl_object.method("__str__")
def nl__str__(self):
    return f"<NumLab instance of type {self.type.type_name} at {hex(id(self))}>"


@nl_object.method("__repr__")
def nl__repr__(self):
    return f"<NumLab instance of type {self.type.type_name} at {hex(id(self))}>"
