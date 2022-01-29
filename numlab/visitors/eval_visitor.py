from __future__ import annotations

import numlab.nl_ast as ast
import numlab.nl_types as nltp
from numlab.lang.context import Context
from numlab.lang.type import Instance, Type
from numlab.lang.visitor import Visitor

from typing import List

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
    return nltp.nl_bool.new(inst).value


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
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ClassDefStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ReturnStmt):
        exprs = nltp.nl_tuple.new(tuple(self.eval(expr) for expr in node.exprs))
        return exprs

    @visitor
    def eval(self, node: ast.DeleteStmt):
        raise NotImplementedError()

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
        iterator = self.eval(node.iter_expr)
        while iterator.has_next():
            item = iterator.next()
            if not isinstance(node.target, ast.NameExpr):
                raise ValueError("For loop target must be a NameExpr")
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
            return nltp.nl_bool.new(_truth(left) and _truth(right))
        if op == ast.Operator.OR:
            return nltp.nl_bool.new(_truth(left) or _truth(right))

        neg = False
        if op == ast.CmpOp.IS:
            return nltp.nl_bool.new(left.type.subtype(right.type))
        if op == ast.CmpOp.IS_NOT:
            return nltp.nl_bool.new(not left.type.subtype(right.type))

        if op == ast.CmpOp.NOT_IN:
            neg = True
            op = ast.CmpOp.IN

        oper = OPERATOR_FUNC[op]
        val = left.get(oper)(left, right)
        if neg:
            val = nltp.nl_bool.new(not _truth(val))

    @visitor
    def eval(self, node: ast.UnaryOpExpr):
        op = node.op
        val: Instance = self.eval(node.operand)
        if op == ast.UnaryOp.NOT:
            return nltp.nl_bool.new(not _truth(val))
        if op == ast.UnaryOp.INVERT:
            return val.get("__invert__")(val)
        if op == ast.UnaryOp.UADD:
            return val
        if op == ast.UnaryOp.USUB:
            return val.get("__sub__")(nltp.nl_int.new(0), val)
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
        return nltp.nl_dict.new(dic)

    @visitor
    def eval(self, node: ast.SetExpr):
        values = {self.eval(v) for v in node.values}
        return nltp.nl_set.new(values)

    @visitor
    def eval(self, node: ast.ListCompExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.SetCompExpr):
        raise NotImplementedError()

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
            kw_arg: tuple = self.eval(kwarg)
            kwargs[kw_arg[0]] = kw_arg[1]
        func = self.eval(node.func)
        return func.get("__call__")(*args, **kwargs)

    @visitor
    def eval(self, node: ast.Keyword):
        if not isinstance(node.value, ast.NameExpr):
            raise ValueError("Keyword value must be a name")
        arg = node.arg.name_id
        val = self.eval(node.value)
        return arg, val

    @visitor
    def eval(self, node: ast.ConstantExpr):
        if isinstance(node.value, str):
            return nltp.nl_string.new(node.value)
        if isinstance(node.value, bool):
            return nltp.nl_bool.new(node.value)
        if isinstance(node.value, int):
            return nltp.nl_int.new(node.value)
        if isinstance(node.value, float):
            return nltp.nl_float.new(node.value)
        raise ValueError(f"Unsupported constant type {type(node.value)}")

    @visitor
    def eval(self, node: ast.AttributeExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.SubscriptExpr):
        return node

    @visitor
    def eval(self, node: ast.StarredExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.NameExpr):
        return node

    @visitor
    def eval(self, node: ast.ListExpr):
        items = [self.eval(i) for i in node.elts]
        return nltp.nl_list.new(items)

    @visitor
    def eval(self, node: ast.TupleExpr):
        items = tuple(self.eval(i) for i in node.elts)
        return nltp.nl_tuple.new(items)

    @visitor
    def eval(self, node: ast.SliceExpr):
        low = self.eval(node.lower) if node.lower is not None else None
        up = self.eval(node.upper) if node.upper is not None else None
        step = self.eval(node.step) if node.step is not None else None
        return nltp.nl_slice.new(low, up, step)

    @visitor
    def eval(self, node: ast.Args):
        return node

    @visitor
    def eval(self, node: ast.Arg):
        return node
