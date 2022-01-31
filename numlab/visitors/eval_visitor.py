from __future__ import annotations

from typing import List

import numlab.nl_ast as ast
import numlab.nl_types as nltp
from numlab.lang.context import Context
from numlab.lang.type import Instance, Type
from numlab.lang.visitor import Visitor

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring

OPERATOR_FUNC = {
    ast.Operator.ADD: "__add__",
    ast.Operator.SUB: "__sub__",
    ast.Operator.MUL: "__mul__",
    ast.Operator.DIV: "__truediv__",
    ast.Operator.POW: "__pow__",
    ast.Operator.MOD: "__mod__",
    ast.Operator.POW: "__pow__",
    ast.Operator.LSHIFT: "__lshift__",
    ast.Operator.RSHIFT: "__rshift__",
    ast.Operator.BIT_XOR: "__xor__",
    ast.Operator.BIT_AND: "__and__",
    ast.Operator.BIT_OR: "__or__",
    ast.Operator.FLOORDIV: "__floordiv__",
    ast.Operator.MATMUL: "__matmul__",
    ast.CmpOp.IN: "__contains__",
    ast.CmpOp.EQ: "__eq__",
    ast.CmpOp.NOT_EQ: "__ne__",
    ast.CmpOp.LT: "__lt__",
    ast.CmpOp.GT: "__gt__",
    ast.CmpOp.LTE: "__le__",
    ast.CmpOp.GTE: "__ge__",
}


def _truth(inst: Instance) -> bool:
    if "__bool__" in inst._dict:
        return inst.get("__bool__")(inst).get("value")
    if "__len__" in inst._dict:
        return inst.get("__len__")(inst).get("value") > 0
    return nltp.nl_bool(True).get("value")


def ioper(oper: str) -> str:
    return f"__i{oper[2:-2]}__"


def roper(oper: str) -> str:
    return f"__r{oper[2:-2]}__"


class EvalVisitor:

    visitor = Visitor().visitor

    def __init__(self, context: Context):
        self.context = context
        self.flags = {
            "inside_loop": 0,
            "pass": 0,
            "break": False,
            "continue": False,
        }

    @visitor
    def eval(self, node: ast.Program):
        for stmt in node.stmts:
            self.eval(stmt)

    @visitor
    def eval(self, node: ast.FuncDefStmt):
        for arg in node.args.args:
            if arg.default is not None:
                arg.default = self.eval(arg.default)

        def func(*args, **kwargs):
            self.context = self.context.make_child()
            for arg, value in zip(node.args.args, args):
                self.context.define(arg.arg.name_id, value)
            for arg, value in kwargs.items():
                self.context.define(arg, value)
            print(self.context.symbols)
            for stmt in node.body:
                self.eval(stmt)
            return_val = self.context.resolve("0")
            self.context = self.context.parent
            return return_val

        func_obj = nltp.nl_function(func)
        func_obj.set("args", node.args)
        if node.name is not None:
            self.context.define(node.name.name_id, func_obj)
        return func_obj

    @visitor
    def eval(self, node: ast.ClassDefStmt):
        bases = [self.eval(base) for base in node.bases]
        if len(bases) > 1:
            raise NotImplementedError("Multiple inheritance not supported")
        if not bases:
            bases = [nltp.nl_object]
        new_type = Type(node.name, bases[0])
        self.context.define(node.name, new_type)
        self.context = self.context.make_child()
        for stmt in node.body:
            self.eval(stmt)
        if node.decorators:
            raise NotImplementedError("Decorators not supported")
        self.context = self.context.parent

    @visitor
    def eval(self, node: ast.ReturnStmt):
        self.context.define("0", self.eval(node.expr))

    @visitor
    def eval(self, node: ast.DeleteStmt):
        for target in node.targets:
            target.ctx = ast.ExprCtx.DEL
            self.eval(target)

    def _assign(self, target, value):
        if isinstance(target, ast.NameExpr):
            self.context.define(target.name_id, value)
        elif isinstance(target, ast.AttributeExpr):
            attr_val = self.eval(target.value)
            attr_val.set(target.attr, value)
        elif isinstance(target, ast.SubscriptExpr):
            subs_value = self.eval(target.value)
            slc = self.eval(target.slice)
            subs_value.get("__setitem__")(subs_value, slc)
        else:
            raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AssignStmt):
        targets: List[ast.TupleExpr] = node.targets
        values = [self.eval(item) for item in node.value.elts]
        for i, val in enumerate(values):
            if isinstance(val, ast.NameExpr):
                values[i] = self.context.resolve(val.name_id)
            values[i] = values[i].get_value()
        for target_tuple in targets:
            if len(target_tuple.elts) != len(values):
                raise ValueError("Too many values to unpack")
            for target, value in zip(target_tuple.elts, values):
                self._assign(target, value)

    @visitor
    def eval(self, node: ast.AugAssignStmt):
        target = node.target
        value = self.eval(node.value)
        oper = ioper(OPERATOR_FUNC[node.op])
        target.get(oper)(value)

    @visitor
    def eval(self, node: ast.AnnAssignStmt):
        target = self.eval(node.target)
        value = self.eval(node.value)
        self._assign(target, value)

    @visitor
    def eval(self, node: ast.ForStmt):
        self.flags["inside_loop"] += 1
        obj = self.eval(node.iter_expr)
        iterator = obj.get("__iter__")(obj)
        if not isinstance(node.target, ast.NameExpr):
            raise ValueError("For loop target must be a NameExpr")
        while True:
            try:
                item = iterator.get("__next__")(iterator)
            except StopIteration:
                break
            target_name = node.target.name_id
            self.context.define(target_name, item)
            for stmt in node.body:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    self.flags["continue"] = False
                    break
            if self.flags["break"]:
                break
        if self.flags["break"]:
            self.flags["break"] = False
        else:
            for stmt in node.orelse:
                self.eval(stmt)
        self.flags["inside_loop"] -= 1

    @visitor
    def eval(self, node: ast.WhileStmt):
        self.flags["inside_loop"] += 1
        while _truth(self.eval(node.test)):
            for stmt in node.body:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    self.flags["continue"] = False
                    break
            if self.flags["break"]:
                break
        if self.flags["break"]:
            self.flags["break"] = False
        else:
            for stmt in node.orelse:
                self.eval(stmt)
        self.flags["inside_loop"] -= 1

    @visitor
    def eval(self, node: ast.IfStmt):
        if _truth(self.eval(node.test)):
            for stmt in node.body:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    break
        else:
            for stmt in node.orelse:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    break

    @visitor
    def eval(self, node: ast.WithStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.WithItem):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.RaiseStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.TryStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ExceptHandler):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AssertStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.GlobalStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.NonlocalStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.PassStmt):
        self.flags["pass"] += 1

    @visitor
    def eval(self, node: ast.BreakStmt):
        self.flags["break"] = True

    @visitor
    def eval(self, node: ast.ContinueStmt):
        self.flags["continue"] = True

    @visitor
    def eval(self, node: ast.ExprStmt):
        return self.eval(node.expr)

    @visitor
    def eval(self, node: ast.BinOpExpr):
        left: Instance = self.eval(node.left)
        right: Instance = self.eval(node.right)
        op = node.op
        if op == ast.Operator.AND:
            return nltp.nl_bool(_truth(left) and _truth(right))
        if op == ast.Operator.OR:
            return nltp.nl_bool(_truth(left) or _truth(right))

        neg = False
        if op == ast.CmpOp.IS:
            return nltp.nl_bool(left.type.subtype(right.type))
        if op == ast.CmpOp.IS_NOT:
            return nltp.nl_bool(not left.type.subtype(right.type))

        if op == ast.CmpOp.NOT_IN:
            neg = True
            op = ast.CmpOp.IN

        oper = OPERATOR_FUNC[op]
        val = left.get(oper)(left, right)
        if neg:
            val = nltp.nl_bool(not _truth(val))
        return val

    @visitor
    def eval(self, node: ast.UnaryOpExpr):
        op = node.op
        val: Instance = self.eval(node.operand)
        if op == ast.UnaryOp.NOT:
            return nltp.nl_bool(not _truth(val))
        if op == ast.UnaryOp.INVERT:
            return val.get("__invert__")(val)
        if op == ast.UnaryOp.UADD:
            return val
        if op == ast.UnaryOp.USUB:
            return val.get("__sub__")(nltp.nl_int(0), val)
        raise ValueError("Unsupported unary operator")

    @visitor
    def eval(self, node: ast.LambdaExpr):
        for dec in node.decorator[::-1]:
            dec_val = self.eval(dec)

    @visitor
    def eval(self, node: ast.IfExpr):
        if _truth(self.eval(node.test)):
            return self.eval(node.body)
        if node.orelse is not None:
            return self.eval(node.orelse)

    @visitor
    def eval(self, node: ast.DictExpr):
        dic = {self.eval(k): self.eval(v) for k, v in zip(node.keys, node.values)}
        return nltp.nl_dict(dic)

    @visitor
    def eval(self, node: ast.SetExpr):
        values = {self.eval(v) for v in node.values}
        return nltp.nl_set(values)

    def _generate(self, compr: List[ast.Comprehension]):
        current = compr[0]
        obj = self.eval(current.comp_iter)
        iterator = obj.get("__iter__")(obj)
        while True:
            try:
                item = iterator.get("__next__")(iterator)
                if isinstance(current.target, ast.NameExpr):
                    self.context.define(current.target.name_id, item)
                else:
                    raise NotImplementedError("Tuple target not supported")
                valid = True
                for if_expr in current.ifs:
                    if not _truth(self.eval(if_expr.test)):
                        valid = False
                        break
                if not valid:
                    continue
            except StopIteration:
                break
            if len(compr) == 1:
                if not isinstance(current.target, ast.NameExpr):
                    raise ValueError("Invalid target")
                yield self.context.resolve(current.target.name_id)
            else:
                yield from self._generate(compr[1:])

    @visitor
    def eval(self, node: ast.ListCompExpr):
        items = []
        if not isinstance(node.elt, ast.NameExpr):
            raise ValueError("Invalid target")
        self.context = self.context.make_child()
        for _ in self._generate(node.generators):
            item = self.context.resolve(node.elt.name_id)
            items.append(item)
        self.context = self.context.parent
        return nltp.nl_list(items)

    @visitor
    def eval(self, node: ast.SetCompExpr):
        items = set()
        if not isinstance(node.target, ast.NameExpr):
            raise ValueError("Invalid target")
        for _ in self._generate(node.generators):
            item = self.context.resolve(node.target.name_id)
            items.add(item)
        return nltp.nl_list(items)

    @visitor
    def eval(self, node: ast.DictCompExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.GeneratorExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.Comprehension):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.YieldExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.YieldFromExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.CompareExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.CallExpr):
        args = [self.eval(arg) for arg in node.args]
        kwargs = {}
        for kwarg in node.keywords:
            kw_arg = self.eval(kwarg)
            kwargs[kw_arg[0]] = kw_arg[1]  # pylint: disable=unsubscriptable-object
        obj = None
        if isinstance(node.func, ast.NameExpr):
            func = self.context.resolve(node.func.name_id)
        elif isinstance(node.func, ast.AttributeExpr):
            obj = self.eval(node.func.value)
            func = node.func.attr
        else:
            func = self.eval(node.func)
        func_args = func.get("args").args

        # Setting arg values
        call_args = {}
        varargs = None
        for arg in func_args:
            call_args[arg.arg] = arg.default
            if arg.is_arg:
                call_args[arg.arg] = []
                varargs = arg.arg
                break
        count = len(call_args)
        names = list(call_args.keys())

        i = 0
        for arg in args:
            if i >= count:
                raise ValueError("Too many positional arguments")
            if func_args[i].is_arg:
                call_args[names[i]].append(arg)
                continue
            call_args[names[i]] = arg
            i += 1

        if varargs is not None:
            call_args[varargs] = Type.get("tuple")(call_args[varargs])

        # Setting keyword values
        call_kwargs = {}
        kwarguments = None
        passed_varargs = False
        for arg in func_args:
            if not passed_varargs:
                if arg.is_arg:
                    passed_varargs = True
                continue

            if arg.is_kwarg:
                call_kwargs[arg.arg.name_id] = {}
                kwarguments = arg.arg.name_id
                break
            call_kwargs[arg.arg.name_id] = arg.default

        for kwarg in kwargs:
            if kwarg in call_args:
                if call_args[kwarg] is None:
                    call_args[kwarg] = kwargs[kwarg]
                else:
                    raise ValueError("Duplicate argument")
                continue
            if kwarg in call_kwargs:
                call_kwargs[kwarg] = kwargs[kwarg]
            elif kwarguments is not None:
                call_kwargs[kwarguments][kwarg] = kwargs[kwarg]
            else:
                raise ValueError("Unknown argument")

        if kwarguments is not None:
            call_kwargs[kwarguments] = Type.get("dict")(call_kwargs[kwarguments])

        if None in call_args.values():
            raise ValueError("Missing argument")

        if obj is None:
            return func.get("__call__")(func, *call_args.values(), **call_kwargs)
        return obj.get(func)(obj, *args, **kwargs)

    @visitor
    def eval(self, node: ast.Keyword):
        if not isinstance(node.arg, ast.NameExpr):
            raise ValueError("Keyword value must be a name")
        arg = node.arg.name_id
        val = self.eval(node.value)
        return arg, val

    @visitor
    def eval(self, node: ast.ConstantExpr):
        if isinstance(node.value, str):
            return nltp.nl_str(node.value)
        if isinstance(node.value, bool):
            return nltp.nl_bool(node.value)
        if isinstance(node.value, int):
            return nltp.nl_int(node.value)
        if isinstance(node.value, float):
            return nltp.nl_float(node.value)
        raise ValueError(f"Unsupported constant type {type(node.value)}")

    @visitor
    def eval(self, node: ast.AttributeExpr):
        if node.ctx == ast.ExprCtx.STORE:
            return node
        val: Instance = self.eval(node.value)
        if node.ctx == ast.ExprCtx.LOAD:
            return val.get(node.attr)
        val._dict.pop(node.attr)

    @visitor
    def eval(self, node: ast.SubscriptExpr):
        if node.ctx == ast.ExprCtx.STORE:
            return node
        val = self.eval(node.value)
        idx = self.eval(node.slice_expr)
        if node.ctx == ast.ExprCtx.LOAD:
            return val.get("__getitem__")(val, idx)
        val.get("__delitem__")(val, idx)

    @visitor
    def eval(self, node: ast.StarredExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.NameExpr):
        if node.ctx == ast.ExprCtx.STORE:
            return node
        if node.ctx == ast.ExprCtx.LOAD:
            return self.context.resolve(node.name_id)
        self.context.symbols.pop(node.name_id)

    @visitor
    def eval(self, node: ast.ListExpr):
        items = [self.eval(i) for i in node.elts]
        return nltp.nl_list(items)

    @visitor
    def eval(self, node: ast.TupleExpr):
        items = tuple(self.eval(i) for i in node.elts)
        return nltp.nl_tuple(items)

    @visitor
    def eval(self, node: ast.SliceExpr):
        low = self.eval(node.lower) if node.lower is not None else None
        upper = self.eval(node.upper) if node.upper is not None else None
        step = self.eval(node.step) if node.step is not None else None
        return nltp.nl_slice(low, upper, step)

    @visitor
    def eval(self, node: ast.Args):
        return node

    @visitor
    def eval(self, node: ast.Arg):
        return node
