from numlab.lang.type import Type, Instance
from numlab.nl_types.nl_int import nl_int

nl_bool = Type('bool', nl_int)

@nl_bool.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_bool)
    _inst.set('value', bool(value))
    return _inst
