import builtins
import math
import random
from time import sleep

import numlab.exceptions as excpt
from numlab.lang.type import Type

__BUILTINS = {}

nl_float = Type.get("float")
nl_int = Type.get("int")
nl_str = Type.get("str")
nl_list = Type.get("list")
nl_bool = Type.get("bool")
nl_function = Type.get("function")


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
    raise excpt.InvalidTypeError("sum() can't sum non-iterable")


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


@builtin_func("range")
def nl_range(start, stop=None, step=None):
    if stop is None:
        stop = start
        start = nl_int(0)
    if step is None:
        step = nl_int(1)

    def move_next(self):
        if not "current" in self._dict:
            self.set("current", start)
            return start
        old_current = self.get("current")
        self.set("current", old_current.get("__add__")(old_current, step))
        current = self.get("current")
        if current.get("__ge__")(current, stop).get("value"):
            raise StopIteration
        return current

    return Type.new("generator", move_next)


@builtin_func("rand")
def nl_rand():
    return nl_float(random.random())


@builtin_func("randint")
def nl_randint(a, b):
    return nl_int(random.randint(a.get("value"), b.get("value")))


@builtin_func("norm")
def nl_norm():
    return nl_float(random.normalvariate(0, 1))


@builtin_func("sqrt")
def nl_sqrt(x):
    return nl_float(math.sqrt(x.get("value")))


@builtin_func("sleep")
def nl_sleep(x: nl_float):
    return nl_float(sleep(x))


@builtin_func("log")
def log(x, base):
    return nl_float(math.log(x.get("value"), base.get("value")))


@builtin_func("log2")
def log2(x):
    return nl_float(math.log2(x.get("value")))


@builtin_func("exp")
def exp(x):
    return nl_float(math.exp(x.get("value")))


@builtin_func("ceil")
def ceil(x):
    return nl_int(math.ceil(x.get("value")))


@builtin_func("floor")
def floor(x):
    return nl_int(math.floor(x.get("value")))


@builtin_func("sin")
def sin(x):
    return nl_float(math.sin(x.get("value")))


@builtin_func("cos")
def cos(x):
    return nl_int(math.cos(x.get("value")))


@builtin_func("tan")
def tan(x):
    return nl_int(math.tan(x.get("value")))


@builtin_func("montcar")
def nl_montcar(n, func):
    if not n.type.subtype(nl_int):
        raise excpt.InvalidTypeError("montcar() argument 1 must be an integer")
    if n.get("value") <= 0:
        raise excpt.ValueError("montcar() argument 1 must be > 0")
    if not func.type.subtype(nl_function):
        raise excpt.InvalidTypeError(
            "montcar() argument 2 must be a function (predicate)"
        )
    true_count, total_count = 0, 0
    for _ in range(n.get("value")):
        total_count += 1
        if func.get("__call__")(func).get("value"):
            true_count += 1
    return nl_float(true_count / total_count)
