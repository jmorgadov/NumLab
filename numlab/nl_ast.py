from __future__ import annotations

import enum
from typing import Any, List

from numlab.compiler import AST

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class Program(AST):
    def __init__(self, stmts: List[Stmt]):
        self.stmts = stmts


class Stmt(AST):
    pass


class FuncDefStmt(Stmt):
    def __init__(self, name: str, args: Args, body: List[Stmt]):
        self.name = name
        self.args = args
        self.body = body


class ClassDefStmt(Stmt):
    def __init__(
        self,
        name: str,
        bases: List[Expr],
        body: List[Stmt],
        decorators: List[Expr] = None,
    ):
        self.name = name
        self.bases = bases
        self.body = body
        self.decorators = decorators


class ReturnStmt(Stmt):
    def __init__(self, expr: Expr = None):
        self.expr = expr


class DeleteStmt(Stmt):
    def __init__(self, targets: List[Expr]):
        self.targets = targets


class AssignStmt(Stmt):
    def __init__(self, targets: List[Expr], value: Expr):
        self.targets = targets
        self.value = value


class AugAssignStmt(Stmt):
    def __init__(self, target: Expr, op: str, value: Expr):
        self.target = target
        self.op = op
        self.value = value


class AnnAssignStmt(Stmt):
    def __init__(self, target: Expr, annotation: Expr, value: Expr):
        self.target = target
        self.annotation = annotation
        self.value = value


class ForStmt(Stmt):
    def __init__(self, target: Expr, iter: Expr, body: List[Stmt], orelse: List[Stmt]):
        self.target = target
        self.iter = iter
        self.body = body
        self.orelse = orelse


class WhileStmt(Stmt):
    def __init__(self, test: Expr, body: List[Stmt], orelse: List[Stmt]):
        self.test = test
        self.body = body
        self.orelse = orelse


class IfStmt(Stmt):
    def __init__(self, test: Expr, body: List[Stmt], orelse: List[Stmt]):
        self.test = test
        self.body = body
        self.orelse = orelse


class WithStmt(Stmt):
    def __init__(self, items: List[WithItem], body: List[Stmt]):
        self.items = items
        self.body = body


class WithItem(AST):
    def __init__(self, context_expr: Expr, optional_vars: List[Expr]):
        self.context_expr = context_expr
        self.optional_vars = optional_vars


class RaiseStmt(Stmt):
    def __init__(self, exc: Expr = None, cause: Expr = None):
        self.exc = exc
        self.cause = cause


class TryStmt(Stmt):
    def __init__(
        self,
        body: List[Stmt],
        handlers: List[ExceptHandler],
        orelse: List[Stmt],
        finalbody: List[Stmt],
    ):
        self.body = body
        self.handlers = handlers
        self.orelse = orelse
        self.finalbody = finalbody


class ExceptHandler(AST):
    def __init__(self, hand_type: Expr, name: Expr, body: List[Stmt]):
        self.hand_type = hand_type
        self.name = name
        self.body = body


class AssertStmt(Stmt):
    def __init__(self, test: Expr, msg: Expr = None):
        self.test = test
        self.msg = msg


class GlobalStmt(Stmt):
    def __init__(self, names: List[str]):
        self.names = names


class NonlocalStmt(Stmt):
    def __init__(self, names: List[str]):
        self.names = names


class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr


class PassStmt(Stmt):
    pass


class BreakStmt(Stmt):
    pass


class ContinueStmt(Stmt):
    pass


class Expr(AST):
    pass


class BoolOpExpr(Expr):
    def __init__(self, op: str, values: List[Expr]):
        self.op = op
        self.values = values


class BinOpExpr(Expr):
    def __init__(self, left: Expr, op: str, right: Expr):
        self.op = op
        self.left = left
        self.right = right


class UnaryOpExpr(Expr):
    def __init__(self, op: str, operand: Expr):
        self.op = op
        self.operand = operand


class LambdaExpr(Expr):
    def __init__(self, args: Args, body: Expr):
        self.args = args
        self.body = body


class IfExpr(Expr):
    def __init__(self, test: Expr, body: Expr, orelse: Expr):
        self.test = test
        self.body = body
        self.orelse = orelse


class DictExpr(Expr):
    def __init__(self, keys: List[Expr], values: List[Expr]):
        self.keys = keys
        self.values = values


class SetExpr(Expr):
    def __init__(self, elts: List[Expr]):
        self.elts = elts


class ListCompExpr(Expr):
    def __init__(self, elt: Expr, generators: List[Comprehension]):
        self.elt = elt
        self.generators = generators


class SetCompExpr(Expr):
    def __init__(self, elt: Expr, generators: List[Comprehension]):
        self.elt = elt
        self.generators = generators


class DictCompExpr(Expr):
    def __init__(self, key: Expr, value: Expr, generators: List[Comprehension]):
        self.key = key
        self.value = value
        self.generators = generators


class GeneratorExpr(Expr):
    def __init__(self, elt: Expr, generators: List[Comprehension]):
        self.elt = elt
        self.generators = generators


class Comprehension(AST):
    def __init__(self, target: Expr, comp_iter: Expr, ifs: List[Expr]):
        self.target = target
        self.comp_iter = comp_iter
        self.ifs = ifs


class YieldExpr(Expr):
    def __init__(self, value: Expr = None):
        self.value = value


class YieldFromExpr(Expr):
    def __init__(self, value: Expr):
        self.value = value


class CompareExpr(Expr):
    def __init__(self, left: Expr, ops: List[CmpOp], comparators: List[Expr]):
        self.left = left
        self.ops = ops
        self.comparators = comparators


class CallExpr(Expr):
    def __init__(self, func: Expr, args: List[Expr], keywords: List[Keyword]):
        self.func = func
        self.args = args
        self.keywords = keywords


class Keyword(AST):
    def __init__(self, arg: str, value: Expr):
        self.arg = arg
        self.value = value


class ConstantExpr(Expr):
    def __init__(self, value: Any):
        self.value = value


class AttributeExpr(Expr):
    def __init__(self, value: Expr, attr: str, ctx: ExprCtx):
        self.value = value
        self.attr = attr
        self.ctx = ctx


class SubscriptExpr(Expr):
    def __init__(self, value: Expr, slice_expr: SliceExpr, ctx: ExprCtx):
        self.value = value
        self.slice_expr = slice_expr
        self.ctx = ctx


class StarredExpr(Expr):
    def __init__(self, value: Expr, ctx: ExprCtx):
        self.value = value
        self.ctx = ctx


class NameExpr(Expr):
    def __init__(self, name_id: str, ctx: ExprCtx):
        self.name_id = name_id
        self.ctx = ctx


class ListExpr(Expr):
    def __init__(self, elts: List[Expr], ctx: ExprCtx):
        self.elts = elts
        self.ctx = ctx


class TupleExpr(Expr):
    def __init__(self, elts: List[Expr], ctx: ExprCtx):
        self.elts = elts
        self.ctx = ctx


class SliceExpr(Expr):
    def __init__(self, lower: Expr = None, upper: Expr = None, step: Expr = None):
        self.lower = lower
        self.upper = upper
        self.step = step


class Args(AST):
    def __init__(
        self,
        args: List[Arg] = None,
        keyword_args: List[Arg] = None,
        vararg=None,
        kwarg=None,
        defaults: List[Expr] = None,
        kw_defaults: List[Expr] = None,
    ):
        self.args = args if args is not None else []
        self.keyword_args = keyword_args if keyword_args is not None else []
        self.vararg = vararg
        self.kwarg = kwarg
        self.defaults = defaults if defaults is not None else []
        self.kw_defaults = kw_defaults if kw_defaults is not None else []


class Arg(AST):
    def __init__(self, arg: str, annotation: Expr = None):
        self.arg = arg
        self.annotation = annotation


class ExprCtx(enum.Enum):
    LOAD = enum.auto()
    STORE = enum.auto()
    DEL = enum.auto()


class BoolOp(enum.Enum):
    AND = enum.auto()
    OR = enum.auto()


class Operator(enum.Enum):
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    POW = enum.auto()
    LSHIFT = enum.auto()
    RSHIFT = enum.auto()
    BIT_AND = enum.auto()
    BIT_XOR = enum.auto()
    BIT_OR = enum.auto()
    FLOORDIV = enum.auto()


class CmpOp(enum.Enum):
    IN = enum.auto()
    NOT_IN = enum.auto()
    IS = enum.auto()
    IS_NOT = enum.auto()
    EQ = enum.auto()
    NOT_EQ = enum.auto()
    LT = enum.auto()
    LTE = enum.auto()
    GT = enum.auto()
    GTE = enum.auto()


class UnaryOp(enum.Enum):
    UADD = enum.auto()
    USUB = enum.auto()
    NOT = enum.auto()
    INVERT = enum.auto()
