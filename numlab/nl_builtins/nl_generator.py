from numlab.lang.type import Instance, Type

nl_generator = Type.get("generator")


@nl_generator.method("__new__")
def nl__new__(func):
    _inst = Instance(nl_generator)
    _inst.set("func", func)
    return _inst


@nl_generator.method("__iter__")
def nl__iter__(self):
    return self


@nl_generator.method("__next__")
def nl__next__(self):
    return self.get("func")(self)
