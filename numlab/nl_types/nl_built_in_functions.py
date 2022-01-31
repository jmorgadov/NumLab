import builtins

from numlab.lang.type import Type

__BUILTINS = {}

nl_float = Type.get('float')
nl_int = Type.get('int')
nl_str = Type.get('str')

def builtin_func(func_name):
    def deco(func):
        __BUILTINS[func_name] = func
        return func
    return deco

def resolve(func_name):
    return func_name in __BUILTINS

@builtin_func('print')
def print(*args, **kwargs):
    builtins.print(*args, **kwargs)

@builtin_func('abs')
def abs(x: nl_float):
    return x if x.value > 0 else nl_float.__new__(-1*x.value)

@builtin_func('bin')
def bin(x: nl_int):
    return nl_str.__new__(builtins.bin(x.value))

@builtin_func('pow')
def pow(base, exp, mod):
    return nl_float.__new__(builtins.pow(base.value, exp.value, mod.value))

@builtin_func('round')
def round(x, ndigits = None):
    return nl_float.__new__(builtins.round(x.value, ndigits))

@builtin_func('sum')
def sum(iterable, start = 0):
    pass

@builtin_func('sorted')
def sorted(iterable):
    pass

@builtin_func('min')
def min(iterable):
    pass

@builtin_func('max')
def max(iterable):
    pass

@builtin_func('open')
def opne(iterable):
    pass

@builtin_func('len')
def len(x):
    return x.__len__()

@builtin_func('hash')
def hash(x):
    return x.__hash__()

# @builtin_func('input')
# def input():
#     return nl_str.__new__(builtins.input())
