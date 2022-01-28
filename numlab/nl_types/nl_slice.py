from numlab.lang.type import Instance, Type
from numlab.nl_types.nl_int import nl_int
from numlab.nl_types.nl_object import nl_object

from typing import Optional

nl_slice = Type("slice", nl_object)

@nl_slice.method("__new__")
def nl__new__(low: Optional[int], upper: Optional[int], step: Optional[int]):
    _inst = Instance(nl_slice)
    _inst.set("low", low)
    _inst.set("upper", upper)
    _inst.set("step", step)
    return _inst
