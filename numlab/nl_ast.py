from __future__ import annotations

import enum
from typing import Any, List

from numlab.compiler import AST

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class ExprCtx(enum.Enum):
    LOAD = enum.auto()
    STORE = enum.auto()
    DEL = enum.auto()


class Operator(enum.Enum):
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    POW = enum.auto()
    AND = enum.auto()
    OR = enum.auto()
    LSHIFT = enum.auto()
    RSHIFT = enum.auto()
    BIT_AND = enum.auto()
    BIT_XOR = enum.auto()
    BIT_OR = enum.auto()
    FLOORDIV = enum.auto()
    MATMUL = enum.auto()


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


class Program(AST):
    def __init__(self, stmts: List[Stmt]):
        self.stmts = stmts


class Stmt(AST):
    pass


class FuncDefStmt(Stmt):
    def __init__(
        self,
        name: str,
        args: Args,
        body: List[Stmt],
        decorators: List[Expr] = None,
    ):
        self.name = name
        self.args = args
        self.body = body
        self.decorators = decorators or []

    def add_decorators(self, decorators: List[Expr]) -> FuncDefStmt:
        self.decorators = decorators
        return self


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
        self.decorators = decorators or []

    def add_decorators(self, decorators: List[Expr]) -> ClassDefStmt:
        self.decorators = decorators
        return self


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
    def __init__(self, target: Expr, op: Operator, value: Expr):
        self.target = target
        self.op = op
        self.value = value

    def set_target(self, target: Expr) -> AugAssignStmt:
        self.target = target
        return self


class AnnAssignStmt(Stmt):
    def __init__(self, target: Expr, annotation: Expr, value: Expr):
        self.target = target
        self.annotation = annotation
        self.value = value

    def set_target(self, target: Expr) -> AnnAssignStmt:
        self.target = target
        return self


class ForStmt(Stmt):
    def __init__(
        self, target: Expr, iter_expr: Expr, body: List[Stmt], orelse: List[Stmt] = None
    ):
        self.target = target
        self.iter_expr = iter_expr
        self.body = body
        self.orelse = orelse


class WhileStmt(Stmt):
    def __init__(self, test: Expr, body: List[Stmt], orelse: List[Stmt] = None):
        self.test = test
        self.body = body
        self.orelse = orelse


class IfStmt(Stmt):
    def __init__(self, test: Expr, body: List[Stmt], orelse: List[Stmt] = None):
        self.test = test
        self.body = body
        self.orelse = orelse or []


class WithStmt(Stmt):
    def __init__(self, items: List[WithItem], body: List[Stmt]):
        self.items = items
        self.body = body


class WithItem(AST):
    def __init__(self, context_expr: Expr, optional_vars: List[Expr] = None):
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
        handlers: List[ExceptHandler] = None,
        orelse: List[Stmt] = None,
        finalbody: List[Stmt] = None,
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
    def __init__(self, test: Expr, body: Expr, orelse: Expr = None):
        self.test = test
        self.body = body
        self.orelse = orelse


class DictExpr(Expr):
    def __init__(self, keys: List[Expr] = None, values: List[Expr] = None):
        self.keys = keys or []
        self.values = values or []


class SetExpr(Expr):
    def __init__(self, elts: List[Expr] = None):
        self.elts = elts or []


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

    def add_elt(self, elt: Expr) -> GeneratorExpr:
        self.elt = elt
        return self


class Comprehension(AST):
    def __init__(self, target: Expr, comp_iter: Expr, ifs: List[Expr] = None):
        self.target = target
        self.comp_iter = comp_iter
        self.ifs = ifs or []


class YieldExpr(Expr):
    def __init__(self, value: List[Expr] = None):
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

    @property
    def value(self):
        return self.func

    @value.setter
    def value(self, value):
        self.func = value


class Keyword(AST):
    def __init__(self, arg: Expr, value: Expr):
        self.arg = arg
        self.value = value


class StarredExpr(Expr):
    def __init__(self, value: Expr, ctx: ExprCtx = ExprCtx.LOAD, stars: int = 1):
        self.value = value
        self.ctx = ctx
        self.stars = stars


class ConstantExpr(Expr):
    def __init__(self, value: Any):
        self.value = value


class AttributeExpr(Expr):
    def __init__(self, value: Expr, attr: str, ctx: ExprCtx = ExprCtx.LOAD):
        self.value = value
        self.attr = attr
        self.ctx = ctx

    def insert_name_at_start(self, name: str) -> AttributeExpr:
        if isinstance(self.value, AttributeExpr):
            self.value.insert_name_at_start(name)
        elif isinstance(self.value, NameExpr):
            new_name_val = NameExpr(name)
            name_val = self.value.name_id
            self.value = AttributeExpr(new_name_val, name_val)
        return self


class SubscriptExpr(Expr):
    def __init__(self, value: Expr, slice_expr: SliceExpr, ctx: ExprCtx = ExprCtx.LOAD):
        self.value = value
        self.slice_expr = slice_expr
        self.ctx = ctx


class NameExpr(Expr):
    def __init__(self, name_id: str, ctx: ExprCtx = ExprCtx.LOAD):
        self.name_id = name_id
        self.ctx = ctx


class ListExpr(Expr):
    def __init__(self, elts: List[Expr] = None, ctx: ExprCtx = ExprCtx.LOAD):
        self.elts = elts
        self.ctx = ctx


class TupleExpr(Expr):
    def __init__(self, elts: List[Expr] = None, ctx: ExprCtx = ExprCtx.LOAD):
        self.elts = elts
        self.ctx = ctx


class SliceExpr(Expr):
    def __init__(self, lower: Expr = None, upper: Expr = None, step: Expr = None):
        self.lower = lower
        self.upper = upper
        self.step = step or 1


class Args(AST):
    def __init__(
        self,
        args: List[Arg] = None,
        keyword_args: List[Arg] = None,
        vararg=None,
        kwarg=None,
    ):
        self.args = args or []
        self.keyword_args = keyword_args or []
        self.vararg = vararg
        self.kwarg = kwarg


class Arg(AST):
    def __init__(
        self,
        arg: str,
        annotation: Expr = None,
        default: Expr = None,
        is_arg: bool = False,
        is_kwarg: bool = False,
    ):
        self.arg = arg
        self.annotation = annotation
        self.default = default
        self.is_arg = is_arg
        self.is_kwarg = is_kwarg

    def set_default(self, default: Expr) -> Arg:
        self.default = default
        return self

    def set_arg(self, is_arg: bool) -> Arg:
        self.is_arg = is_arg
        return self

    def set_kwarg(self, is_kwarg: bool) -> Arg:
        self.is_kwarg = is_kwarg
        return self
