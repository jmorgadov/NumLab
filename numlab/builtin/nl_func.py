from numlab.lang.type import Instance, Type

nl_function = Type.get("function")

@nl_function.method('__new__')
def nl__new__(func):
    _inst = Instance(nl_function)
    _inst.set('func', func)
    return _inst

@nl_function.method('__call__')
def nl__call__(self, *args, **kwargs):
    return self.get("func")(*args, **kwargs)

