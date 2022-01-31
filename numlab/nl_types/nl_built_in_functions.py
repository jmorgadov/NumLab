import builtins

from numlab.lang.type import Type

__BUILTINS = {}

nl_float = Type.get('float')
nl_int = Type.get('int')
nl_str = Type.get('str')
nl_list = Type.get('list')

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
    return nl_float(builtins.abs(x.get('value')))

@builtin_func('bin')
def bin(x: nl_int):
    return nl_str(builtins.bin(x.get('value')))

@builtin_func('pow')
def pow(base, exp, mod):
    return nl_float(builtins.pow(base.get('value'), exp.get('value'), mod.get('value')))

@builtin_func('round')
def round(x, ndigits = None):
    return nl_float(builtins.round(x.get('value'), ndigits))

@builtin_func('sum')
def sum(a, *args):
    if '__iter__' in a._dict:
        return nl_float(builtins.sum(a))
    if args:
        return nl_float(builtins.sum(a, *args))
    return a

@builtin_func('sorted')
def sorted(a, *args):
    if '__iter__' in a._dict:
        return nl_list(builtins.min(a))
    raise TypeError('Object must be iterable')

@builtin_func('iter')
def iter(x):
    pass

@builtin_func('min')
def min(a, *args):
    if '__iter__' in a._dict:
        return nl_float(builtins.min(a))
    if args:
        return nl_float(builtins.min(a, *args))
    return a

@builtin_func('max')
def max(a, *args):
    if '__iter__' in a._dict:
        return nl_float(builtins.max(a))
    if args:
        return nl_float(builtins.max(a, *args))
    return a

@builtin_func('open')
def open(file, mode, encoding = None):
    builtins.open(file.get('value'), mode.get('value'), encoding = encoding.get('value'))

@builtin_func('len')
def len(x):
    return x.__len__()

@builtin_func('hash')
def hash(x):
    return x.__hash__()

@builtin_func('input')
def input():
    pass
