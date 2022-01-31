from typing import Optional

from numlab.lang.type import Instance, Type

nl_slice = Type.get("slice")


@nl_slice.method("__new__")
def nl__new__(low: Optional[int], upper: Optional[int], step: Optional[int]):
    _inst = Instance(nl_slice)
    _inst.set("low", low)
    _inst.set("upper", upper)
    _inst.set("step", step)
    return _inst
