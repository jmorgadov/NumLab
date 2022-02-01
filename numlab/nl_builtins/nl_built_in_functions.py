import builtins

from numlab.lang.type import Type

__BUILTINS = {}

nl_float = Type.get("float")
nl_int = Type.get("int")
nl_str = Type.get("str")
nl_list = Type.get("list")
nl_bool = Type.get("bool")


def builtin_func(func_name):
    def deco(func):
        __BUILTINS[func_name] = func
        return func

    return deco


def resolve(func_name):
    return __BUILTINS.get(func_name, None)


@builtin_func("repr")
def nl_repr(arg):
    return arg.get("__repr__")(arg)


@builtin_func("print")
def nl_print(value, *args, sep=nl_str(" "), end=nl_str("\n")):
    values = [value.get("__str__")(value).get("value")] + [
        arg.get("__str__")(arg).get("value") for arg in args
    ]
    builtins.print(*values, sep=sep.get("value"), end=end.get("value"))


@builtin_func("abs")
def nl_abs(x: nl_float):
    return nl_float(builtins.abs(x.get("value")))


@builtin_func("bin")
def nl_bin(x: nl_int):
    return nl_str(builtins.bin(x.get("value")))


@builtin_func("pow")
def nl_pow(base, exp, mod):
    return nl_float(builtins.pow(base.get("value"), exp.get("value"), mod.get("value")))


@builtin_func("round")
def nl_round(x, ndigits=None):
    if ndigits is None:
        return nl_float(builtins.round(x.get("value")))
    return nl_float(builtins.round(x.get("value"), ndigits.get("value")))


@builtin_func("sum")
def nl_sum(iterable, start=nl_int(0)):
    if "__iter__" in iterable._dict:
        answ = None
        for item in iterable:
            if answ is None:
                answ = item
            else:
                answ = answ.get("__add__")(answ, item)
        return answ
    raise TypeError("sum() can't sum non-iterable")


@builtin_func("sorted")
def nl_sorted(iterable, key=None, reverse=nl_bool(False)):
    raise NotImplementedError("sorted() is not implemented yet")


@builtin_func("iter")
def nl_iter(x):
    return x.get("__iter__")(x)


@builtin_func("max")
def nl_max(a, *args):
    if args:
        answ = a
        for arg in args:
            answ = answ.get("__gt__")(answ, arg)
        return answ

    if "__iter__" in a._dict:
        answ = None
        for item in a:
            if answ is None:
                answ = item
            else:
                answ = answ.get("__gt__")(answ, item)
        return answ
    return a


@builtin_func("min")
def nl_min(a, *args):
    if args:
        answ = a
        for arg in args:
            answ = answ.get("__lt__")(answ, arg)
        return answ

    if "__iter__" in a._dict:
        answ = None
        for item in a:
            if answ is None:
                answ = item
            else:
                answ = answ.get("__lt__")(answ, item)
        return answ
    return a


@builtin_func("len")
def nl_len(x):
    return x.get("__len__")(x)


@builtin_func("hash")
def nl_hash(x):
    return x.get("__hash__")(x)


@builtin_func("input")
def nl_input():
    return nl_str(builtins.input())
