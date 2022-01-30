from gettext import install

from numlab.lang.type import Instance, Type

nl_int = Type.get("int")
nl_bool = Type.get("bool")

nl_dict = Type("dict", Type.get("object"))


@nl_dict.method("__new__")
def nl__new__(value: dict):
    _inst = Instance(nl_dict)
    _inst.set("value", dict(value))
    return _inst


@nl_dict.method("__contains__")
def nl__contains__(self, key: Instance):
    return nl_bool(key in self.value)


@nl_dict.method("__iter__")
def nl__iter__(self):
    for key in self.value:
        yield key


@nl_dict.method("__len__")
def nl__len__(self):
    return nl_int(len(self.value))


@nl_dict.method("__getitem__")
def nl__getitem__(self, key: Instance):
    return self.value[key]


@nl_dict.method("__setitem__")
def nl__setitem__(self, key: Instance, value: Instance):
    self.value[key] = value


@nl_dict.method("clear")
def nl_clear(self):
    self.value.clear()


@nl_dict.method("copy")
def nl_copy(self):
    self.value.copy()


@nl_dict.method("items")
def nl_items(self):
    return self.value.items()


@nl_dict.method("keys")
def nl_keys(self):
    return self.value.keys()


@nl_dict.method("values")
def nl_values(self):
    return self.value.values()


@nl_dict.method("get")
def nl_get(self, key: Instance):
    return nl__getitem__(self, key)


@nl_dict.method("pop")
def nl_pop(self, key: Instance):
    return self.value.pop(key)


@nl_dict.method("popitem")
def nl_popitem(self):
    return self.value.popitem()
