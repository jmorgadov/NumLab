from numlab.lang.type import Instance, Type
from numlab.nl_types.nl_object import nl_object

nl_function = Type.get("function")

@nl_function.method('__new__')
def nl__new__(func):
    _inst = Instance(nl_function)
    _inst.set('func', func)
    return _inst

@nl_function.method('__call__')
def nl__call__(self, *args, **kwargs):
    self.func(*args, **kwargs)

