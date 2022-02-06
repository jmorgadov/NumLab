import numlab.exceptions as excpt
from numlab.lang.type import Instance, Type

nl_bool = Type.get("bool")
nl_int = Type.get("int")
nl_slice = Type.get("slice")
nl_tuple = Type.get("tuple")
nl_str = Type.get("str")


@nl_tuple.method("__new__")
def nl__new__(value: set):
    _inst = Instance(nl_tuple)
    _inst.set("value", tuple(value))
    return _inst


@nl_tuple.method("__contains__")
def nl__contains__(self, obj: Instance):
    return nl_bool(obj in self.get("value"))


@nl_tuple.method("__getitem__")
def nl__getitem__(self, indx: Instance):
    if indx.type.subtype(nl_int):
        return self.get("value")[indx.value]
    if indx.type.subtype(nl_slice):
        low = indx.low if indx.low is not None else 0
        upper = indx.up if indx.upper is not None else len(self.get("value"))
        step = indx.step if indx.step is not None else 0
        if not isinstance(low, int) and not low.type.subtype(nl_int):
            raise excpt.InvalidTypeError(
                f"Slice indices must be integers, not {low.type.type_name}"
            )
        if not isinstance(upper, int) and not upper.type.subtype(nl_int):
            raise excpt.InvalidTypeError(
                f"Slice indices must be integers, not {upper.type.type_name}"
            )
        if not isinstance(step, int) and not step.type.subtype(nl_int):
            raise excpt.InvalidTypeError(
                f"Slice indices must be integers, not {step.type.type_name}"
            )
        return nl_tuple(self.get("value")[low:upper:step])
    raise excpt.InvalidTypeError(
        f"Tuple indices must be integer or slice, not {indx.type.type_name}"
    )


@nl_tuple.method("__iter__")
def nl__iter__(self):
    iterator = iter(self.get("value"))
    move_next = iterator.__next__
    return Type.new("generator", move_next)


@nl_tuple.method("__repr__")
def nl__repr__(self):
    return nl_str(repr(self.get("value")))


@nl_tuple.method("__len__")
def nl__len__(self):
    return nl_int(len(self.get("value")))


@nl_tuple.method("__add__")
def nl__add__(self, other: Instance):
    if other.type.subtype(nl_tuple):
        return nl_tuple(self.get("value") + other.get("value"))
    raise excpt.InvalidTypeError("Can't concatenate tuple with non-tuple")


@nl_tuple.method("__mul__")
def nl__mul__(self, value: Instance):
    if value.type.subtype(nl_int):
        return nl_tuple(self.get("value") * value.get("value"))
    raise excpt.InvalidTypeError("Can't multiply tuple with non-integers")


@nl_tuple.method("count")
def nl_count(self, value: Instance):
    return nl_int(self.get("value").count(value))


@nl_tuple.method("index")
def nl_index(self, value: Instance, start: Instance = None):
    start_indx = 0
    if start is not None:
        if not start.type.subtype(nl_int):
            raise excpt.InvalidTypeError(
                f"start argument must be an integer, not {start.type.type_name}"
            )
        start_indx = start.get("value")
    return nl_int(self.get("value").index(value, start_indx))
