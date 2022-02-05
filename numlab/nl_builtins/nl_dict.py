from gettext import install

from numlab.lang.type import Instance, Type

nl_int = Type.get("int")
nl_bool = Type.get("bool")
nl_dict = Type.get("dict")
nl_str = Type.get("str")


@nl_dict.method("__new__")
def nl__new__(value: dict):
    _inst = Instance(nl_dict)
    _inst.set("value", dict(value))
    return _inst


@nl_dict.method("__contains__")
def nl__contains__(self, key: Instance):
    val = nl_bool(key in self.get("value"))
    if val.get("value"):
        return val
    if key.has_value():
        return nl_bool(key.get("value") in self.get("value"))
    return val


@nl_dict.method("__iter__")
def nl__iter__(self):
    for key in self.get("value"):
        yield key


@nl_dict.method("__len__")
def nl__len__(self):
    return nl_int(len(self.get("value")))


@nl_dict.method("__repr__")
def nl__repr__(self):
    return nl_str(repr(self.get("value")))


@nl_dict.method("__getitem__")
def nl__getitem__(self, key: Instance):
    _dic = self.get("value")
    for k in _dic:
        if k.get("__eq__")(k, key).get("value"):
            return _dic[k]
    raise KeyError(key)


@nl_dict.method("__setitem__")
def nl__setitem__(self, key: Instance, value: Instance):
    _dic = self.get("value")
    for k in _dic:
        if k.get("__eq__")(k, key).get("value"):
            _dic[k] = value
            return
    self.get("value")[key] = value


@nl_dict.method("clear")
def nl_clear(self):
    self.get("value").clear()


@nl_dict.method("copy")
def nl_copy(self):
    self.get("value").copy()


@nl_dict.method("items")
def nl_items(self):
    return self.get("value").items()


@nl_dict.method("keys")
def nl_keys(self):
    return self.get("value").keys()


@nl_dict.method("values")
def nl_values(self):
    return self.get("value").values()


@nl_dict.method("get")
def nl_get(self, key: Instance):
    return nl__getitem__(self, key)


@nl_dict.method("pop")
def nl_pop(self, key: Instance):
    return self.get("value").pop(key)


@nl_dict.method("popitem")
def nl_popitem(self):
    return self.get("value").popitem()
