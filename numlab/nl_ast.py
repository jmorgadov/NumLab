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
    __slots__ = ("stmts",)

    def __init__(self, stmts: List[Stmt]):
        self.stmts = stmts


class Stmt(AST):
    pass


class FuncDefStmt(Stmt):
    __slots__ = ("name", "args", "body", "decorators")

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
    __slots__ = ("name", "bases", "body", "decorators")

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
    __slots__ = ("expr",)

    def __init__(self, expr: Expr = None):
        self.expr = expr


class DeleteStmt(Stmt):
    __slots__ = ("targets",)

    def __init__(self, targets: List[Expr]):
        self.targets = targets


class AssignStmt(Stmt):
    __slots__ = ("targets", "value")

    def __init__(self, targets: List[Expr], value: Expr):
        self.targets = targets
        self.value = value


class AugAssignStmt(Stmt):
    __slots__ = ("target", "op", "value")

    def __init__(self, target: Expr, op: Operator, value: Expr):
        self.target = target
        self.op = op
        self.value = value

    def set_target(self, target: Expr) -> AugAssignStmt:
        self.target = target
        return self


class AnnAssignStmt(Stmt):
    __slots__ = ("target", "annotation", "value")

    def __init__(self, target: Expr, annotation: Expr, value: Expr):
        self.target = target
        self.annotation = annotation
        self.value = value

    def set_target(self, target: Expr) -> AnnAssignStmt:
        self.target = target
        return self


class ConfDefStmt(Stmt):
    __slots__ = ("name", "base", "configs")

    def __init__(self, name: str, cofigs: List[ConfOption], base: str = None):
        self.name = name
        self.base = base
        self.configs = cofigs


class ConfOption(AST):
    __slots__ = ("name", "value")

    def __init__(self, name: str, value: Expr):
        self.name = name
        self.value = value


class Begsim(Stmt):
    __slots__ = ("config",)

    def __init__(self, config: Expr):
        self.config = config


class Endsim(Stmt):
    pass


class ResetStats(Stmt):
    pass


class ForStmt(Stmt):
    __slots__ = ("target", "iter_expr", "body", "orelse")

    def __init__(
        self, target: Expr, iter_expr: Expr, body: List[Stmt], orelse: List[Stmt] = None
    ):
        self.target = target
        self.iter_expr = iter_expr
        self.body = body
        self.orelse = orelse or []


class WhileStmt(Stmt):
    __slots__ = ("test", "body", "orelse")

    def __init__(self, test: Expr, body: List[Stmt], orelse: List[Stmt] = None):
        self.test = test
        self.body = body
        self.orelse = orelse or []


class IfStmt(Stmt):
    __slots__ = ("test", "body", "orelse")

    def __init__(self, test: Expr, body: List[Stmt], orelse: List[Stmt] = None):
        self.test = test
        self.body = body
        self.orelse = orelse or []


class WithStmt(Stmt):
    __slots__ = ("items", "body")

    def __init__(self, items: List[WithItem], body: List[Stmt]):
        self.items = items
        self.body = body


class WithItem(AST):
    __slots__ = ("context_expr", "optional_vars")

    def __init__(self, context_expr: Expr, optional_vars: List[Expr] = None):
        self.context_expr = context_expr
        self.optional_vars = optional_vars


class RaiseStmt(Stmt):
    __slots__ = ("exc", "cause")

    def __init__(self, exc: Expr = None, cause: Expr = None):
        self.exc = exc
        self.cause = cause


class TryStmt(Stmt):
    __slots__ = ("body", "handlers", "orelse", "finalbody")

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
    __slots__ = ("hand_type", "name", "body")

    def __init__(self, hand_type: Expr, name: Expr, body: List[Stmt]):
        self.hand_type = hand_type
        self.name = name
        self.body = body


class AssertStmt(Stmt):
    __slots__ = ("test", "msg")

    def __init__(self, test: Expr, msg: Expr = None):
        self.test = test
        self.msg = msg


class GlobalStmt(Stmt):
    __slots__ = ("names",)

    def __init__(self, names: List[str]):
        self.names = names


class NonlocalStmt(Stmt):
    __slots__ = ("names",)

    def __init__(self, names: List[str]):
        self.names = names


class ExprStmt(Stmt):
    __slots__ = ("expr",)

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
    __slots__ = ("left", "op", "right")

    def __init__(self, left: Expr, op: str, right: Expr):
        self.op = op
        self.left = left
        self.right = right


class UnaryOpExpr(Expr):
    __slots__ = ("op", "operand")

    def __init__(self, op: UnaryOp, operand: Expr):
        self.op = op
        self.operand = operand


class LambdaExpr(Expr):
    __slots__ = ("args", "body")

    def __init__(self, args: Args, body: Expr):
        self.args = args
        self.body = body


class IfExpr(Expr):
    __slots__ = ("test", "body", "orelse")

    def __init__(self, test: Expr, body: Expr, orelse: Expr = None):
        self.test = test
        self.body = body
        self.orelse = orelse


class DictExpr(Expr):
    __slots__ = ("keys", "values")

    def __init__(self, keys: List[Expr] = None, values: List[Expr] = None):
        self.keys = keys or []
        self.values = values or []


class SetExpr(Expr):
    __slots__ = ("elts",)

    def __init__(self, elts: List[Expr] = None):
        self.elts = elts or []


class ListCompExpr(Expr):
    __slots__ = ("elt", "generators")

    def __init__(self, elt: Expr, generators: List[Comprehension]):
        self.elt = elt
        self.generators = generators


class SetCompExpr(Expr):
    __slots__ = ("elt", "generators")

    def __init__(self, elt: Expr, generators: List[Comprehension]):
        self.elt = elt
        self.generators = generators


class DictCompExpr(Expr):
    __slots__ = ("key", "value", "generators")

    def __init__(self, key: Expr, value: Expr, generators: List[Comprehension]):
        self.key = key
        self.value = value
        self.generators = generators


class GeneratorExpr(Expr):
    __slots__ = ("elt", "generators")

    def __init__(self, elt: Expr, generators: List[Comprehension]):
        self.elt = elt
        self.generators = generators

    def add_elt(self, elt: Expr) -> GeneratorExpr:
        self.elt = elt
        return self


class Comprehension(AST):
    __slots__ = ("target", "comp_iter", "ifs")

    def __init__(self, target: Expr, comp_iter: Expr, ifs: List[Expr] = None):
        self.target = target
        self.comp_iter = comp_iter
        self.ifs = ifs or []


class YieldExpr(Expr):
    __slots__ = ("value",)

    def __init__(self, value: List[Expr] = None):
        self.value = value


class YieldFromExpr(Expr):
    __slots__ = ("value",)

    def __init__(self, value: Expr):
        self.value = value


class CompareExpr(Expr):
    __slots__ = ("left", "ops", "comparators")

    def __init__(self, left: Expr, ops: List[CmpOp], comparators: List[Expr]):
        self.left = left
        self.ops = ops
        self.comparators = comparators


class CallExpr(Expr):
    __slots__ = ("func", "args", "keywords")

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
    __slots__ = ("arg", "value")

    def __init__(self, arg: Expr, value: Expr):
        self.arg = arg
        self.value = value


class StarredExpr(Expr):
    __slots__ = ("value", "ctx")

    def __init__(self, value: Expr, ctx: ExprCtx = ExprCtx.LOAD):
        self.value = value
        self.ctx = ctx


class ConstantExpr(Expr):
    __slots__ = ("value",)

    def __init__(self, value: Any):
        self.value = value

    def show(self):
        return f"ConstantExpr({self.value})"


class AttributeExpr(Expr):
    __slots__ = ("value", "attr", "ctx")

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
    __slots__ = ("value", "slice_expr", "ctx")

    def __init__(self, value: Expr, slice_expr: SliceExpr, ctx: ExprCtx = ExprCtx.LOAD):
        self.value = value
        self.slice_expr = slice_expr
        self.ctx = ctx


class NameExpr(Expr):
    __slots__ = ("name_id", "ctx")

    def __init__(self, name_id: str, ctx: ExprCtx = ExprCtx.LOAD):
        self.name_id = name_id
        self.ctx = ctx

    def show(self):
        return f"NameExpr('{self.name_id}', ctx={self.ctx})"


class ListExpr(Expr):
    __slots__ = ("elts", "ctx")

    def __init__(self, elts: List[Expr] = None, ctx: ExprCtx = ExprCtx.LOAD):
        self.elts = elts or []
        self.ctx = ctx


class TupleExpr(Expr):
    __slots__ = ("elts", "ctx")

    def __init__(self, elts: List[Expr] = None, ctx: ExprCtx = ExprCtx.LOAD):
        self.elts = elts
        self.ctx = ctx


class SliceExpr(Expr):
    __slots__ = ("lower", "upper", "step")

    def __init__(self, lower: Expr = None, upper: Expr = None, step: Expr = None):
        self.lower = lower
        self.upper = upper
        self.step = step


class Args(AST):
    __slots__ = ("args", "vararg", "kwarg")

    def __init__(
        self,
        args: List[Arg] = None,
        vararg=None,
        kwarg=None,
    ):
        self.args = args or []
        self.vararg = vararg
        self.kwarg = kwarg


class Arg(AST):
    __slots__ = ("arg", "annotation", "default", "is_arg", "is_kwarg")

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
