import numlab.exceptions as excpt
from numlab.lang.type import Instance, Type

nl_int = Type.get("int")
nl_slice = Type.get("slice")
nl_str = Type.get("str")
nl_bool = Type.get("bool")
nl_list = Type("list", Type.get("object"))


@nl_list.method("__new__")
def nl__new__(value: list):
    _inst = Instance(nl_list)
    _inst.set("value", list(value))
    return _inst


@nl_list.method("__bool__")
def nl__bool__(self: Instance):
    return nl_bool(len(self.get("value")) > 0)


@nl_list.method("__contains__")
def nl__contains__(self, obj: Instance):
    return Type.new("bool", obj in self.get("value"))


@nl_list.method("__getitem__")
def nl__getitem__(self, indx: Instance):
    if indx.type.subtype(nl_int):
        return self.get("value")[indx.get("value")]
    if indx.type.subtype(nl_slice):
        low = indx.low if indx.low is not None else 0
        upper = indx.up if indx.upper is not None else len(self.get("value"))
        step = indx.step if indx.step is not None else 1
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
        return self.get("value")[low:upper:step]
    raise excpt.InvalidTypeError(
        f"List indices must be integer or slice, not {indx.type.type_name}"
    )


@nl_list.method("__delitem__")
def nl__delitem__(self, indx: Instance):
    if indx.type.subtype(nl_int):
        return self.get("value").__delitem__(indx.get("value"))
    raise excpt.InvalidTypeError("List indices must be integers")


@nl_list.method("__iter__")
def nl__iter__(self):
    iterator = iter(self.get("value"))
    move_next = iterator.__next__
    return Type.new("generator", move_next)


@nl_list.method("__len__")
def nl__len__(self):
    return nl_int(len(self.get("value")))


@nl_list.method("__reversed__")
def nl__reversed__(self):
    for pos in range(len(self.get("value")) - 1, -1, -1):
        yield self.get("value")[pos]


@nl_list.method("__setitem__")
def nl__setitem__(self, indx: Instance, obj: Instance):
    if indx.type.subtype(nl_int):
        self.get("value")[indx] = obj
    raise excpt.InvalidTypeError("List indices must be integers")


@nl_list.method("__repr__")
def nl__repr__(self):
    return nl_str(repr(self.get("value")))


@nl_list.method("append")
def nl_append(self, obj: Instance):
    self.get("value").append(obj)


@nl_list.method("clear")
def nl_clear(self):
    self.get("value").clear()


@nl_list.method("count")
def nl_count(self, obj: Instance):
    return nl_int(self.get("value").count(obj))


@nl_list.method("insert")
def nl_insert(self, indx: Instance, obj: Instance):
    if indx.type.subtype(nl_int):
        self.get("value").insert(indx.get("value"), obj)


@nl_list.method("sort")
def nl_sort(self):
    self.get("value").sort()


@nl_list.method("remove")
def nl_remove(self, obj: Instance):
    items = self.get("value")
    for pos in range(len(items)):
        val = items[pos]
        if val.get("__eq__")(val, obj):
            items.pop(pos)
            return
    raise excpt.ValueError("list.remove(x): x not in list")
