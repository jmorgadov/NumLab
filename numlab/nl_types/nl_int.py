from numlab.lang.type import Type, Instance
from numlab.nl_types.nl_float import nl_float

nl_int = Type('int', nl_float)

nl_int.method("__new__")
def nl__new__(value: float):
    _inst = Instance(nl_int)
    _inst.set('value', int(value))
    return _inst
