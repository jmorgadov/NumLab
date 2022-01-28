from numlab.lang.type import Type, Instance
from numlab.nl_types.nl_object import nl_object
from numlab.nl_types.nl_int import nl_int

nl_slice = Type('slice', nl_object)

nl_slice.method('__new__')
def nl__new__(low: int, up: int, step: int):
    _inst = Instance(nl_slice)
    _inst.set('low', low)
    _inst.set('up', up)
    _inst.set('step', step)
    return _inst

nl_slice.method('up')
def up(self):
    return nl_int.__new__(self.up)

nl_slice.method('low')
def low(self):
    return nl_int.__new__(self.low)

nl_slice.method('step')
def step(self):
    return nl_int.__new__(self.step)