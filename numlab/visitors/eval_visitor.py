from __future__ import annotations

import numlab.nl_ast as ast
import numlab.nl_types as nltp
from numlab.lang.context import Context
from numlab.lang.type import Instance, Type
from numlab.lang.visitor import Visitor

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring

FLAGS = {
    "inside_loop": 0,
    "pass": 0,
    "break": False,
    "continue": False,
}

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
        exprs = [self.eval(expr) for expr in node.exprs]
        return exprs

    @visitor
    def eval(self, node: ast.DeleteStmt):
        raise NotImplementedError()

    def _assign(self, target, value):
        if isinstance(target, ast.NameExpr):
            self.context.set(target.name, value)
        elif isinstance(target, ast.AttributeExpr):
            value.set[target.attr] = value
        elif isinstance(target, ast.SubscriptExpr):
            slc = self.eval(target.slice)
            value.get("__setitem__")(value, slc)
        else:
            raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AssignStmt):
        targets: ast.TupleExpr = node.targets[0]
        values: ast.TupleExpr = node.value[0]
        for target, value in zip(targets.elts, values.elts):
            self._assign(target, self.eval(value))

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
        FLAGS["inside_loop"] += 1
        iterator = self.eval(node.iter_expr)
        while iterator.has_next():
            item = iterator.next()
            if not isinstance(node.target, ast.NameExpr):
                raise ValueError("For loop target must be a NameExpr")
            target_name = node.target.name_id
            self.context.define(target_name, item)
            for stmt in node.body:
                self.eval(stmt)
                if FLAGS["break"]:
                    break
                if FLAGS["continue"]:
                    FLAGS["continue"] = False
                    break
            if FLAGS["break"]:
                break
        if FLAGS["break"]:
            FLAGS["break"] = False
        else:
            for stmt in node.orelse:
                self.eval(stmt)
        FLAGS["inside_loop"] -= 1

    @visitor
    def eval(self, node: ast.WhileStmt):
        FLAGS["inside_loop"] += 1
        while _truth(self.eval(node.test)):
            for stmt in node.body:
                self.eval(stmt)
                if FLAGS["break"]:
                    break
                if FLAGS["continue"]:
                    FLAGS["continue"] = False
                    break
            if FLAGS["break"]:
                break
        if FLAGS["break"]:
            FLAGS["break"] = False
        else:
            for stmt in node.orelse:
                self.eval(stmt)
        FLAGS["inside_loop"] -= 1

    @visitor
    def eval(self, node: ast.IfStmt):
        if _truth(self.eval(node.test)):
            for stmt in node.body:
                self.eval(stmt)
                if FLAGS["break"]:
                    break
                if FLAGS["continue"]:
                    break
        else:
            for stmt in node.orelse:
                self.eval(stmt)
                if FLAGS["break"]:
                    break
                if FLAGS["continue"]:
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
        FLAGS["pass"] += 1

    @visitor
    def eval(self, node: ast.BreakStmt):
        FLAGS["break"] = True

    @visitor
    def eval(self, node: ast.ContinueStmt):
        FLAGS["continue"] = True

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
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.Keyword):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ConstantExpr):
        if isinstance(node.value, str):
            return nltp.nl_str.new(node.value)
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
        raise NotImplementedError()

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
