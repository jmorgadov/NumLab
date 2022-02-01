from symbol import yield_stmt

from numlab.lang.type import Instance, Type

nl_int = Type.get("int")
nl_bool = Type.get("bool")
nl_set = Type.get("set")


@nl_set.method("__new__")
def nl__new__(value: set):
    _inst = Instance(nl_set)
    _inst.set("value", set(value))
    return _inst


@nl_set.method("__contains__")
def nl__contains__(self, obj: Instance):
    return nl_bool(obj in self.get("value"))


@nl_set.method("__iter__")
def nl__iter__(self):
    iterator = iter(self.get("value"))
    move_next = iterator.__next__
    return Type.new("generator", move_next)


@nl_set.method("__len__")
def nl__len__(self):
    return nl_int(len(self.get("value")))


@nl_set.method("add")
def nl_add(self, obj: Instance):
    self.get("value").add(obj.get("value"))


@nl_set.method("clear")
def nl_clear(self):
    self.get("value").clear()


@nl_set.method("copy")
def nl_copy(self):
    return nl__new__(self.get("value").copy())


@nl_set.method("intersection")
def nl_intersection(self, obj: Instance):
    if obj.type.subtype(nl_set):
        self.get("value").intersection(obj.get("value"))
    raise ValueError("Can't intersect a set with a non-set")


@nl_set.method("union")
def nl_union(self, obj: Instance):
    if obj.type.subtype(nl_set):
        return nl_set(self.get("value").union(obj.get("value")))
    raise ValueError("Can't unite a set with a non-set")


@nl_set.method("issubset")
def nl_issubset(self, obj: Instance):
    if obj.type.subtype(nl_set):
        return nl_bool(self.get("value").issubset(obj.get("value")))
    raise ValueError("Can't match a set with a non-set")


@nl_set.method("issuperset")
def nl_issuperset(self, obj: Instance):
    if obj.type.subtype(nl_set):
        return nl_bool(self.get("value").issuperset(obj.get("value")))
    raise ValueError("Can't match a set with a non-set")


@nl_set.method("remove")
def nl_remove(self, obj: Instance):
    self.get("value").remove(obj.get("value"))
