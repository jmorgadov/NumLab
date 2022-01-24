from __future__ import annotations

from typing import List

from numlab.compiler import AST

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class Program(AST):
    def __init__(self, stmts: List[Stmt]):
        self.stmts = stmts


class Stmt(AST):
    def __init__(self, stmt):
        self.stmt = stmt


class StmtList(AST):
    def __init__(self, stmts):
        self.stmts = stmts


class SimpleStmt(AST):
    def __init__(self, small_stmt):
        self.small_stmt = small_stmt


class FuncDef(AST):
    def __init__(self, name, suite, parameters=None):
        self.name = name
        self.suite = suite
        self.parameters = parameters


class ClassDef(AST):
    def __init__(self, name, suite, arg_list=None):
        self.name = name
        self.suite = suite
        self.arg_list = arg_list


class Parameters(AST):
    def __init__(self, parameters):
        self.parameters = parameters


class TFPDefParam(AST):
    def __init__(self, tfpdef):
        self.tfpdef = tfpdef


class TFPDefEqParam(AST):
    def __init__(self, tfpdef, test):
        self.tfpdef = tfpdef
        self.test = test


class StarParam(AST):
    def __init__(self, tfpdef):
        self.tfpdef = tfpdef


class SmallStmt(AST):
    def __init__(self, stmt):
        self.stmt = stmt


class DoubleStarParam(AST):
    def __init__(self, tfpdef):
        self.tfpdef = tfpdef


class VarArgList(AST):
    def __init__(self, var_args):
        self.var_args = var_args


class TFPDef(AST):
    def __init__(self, name, test=None):
        self.name = name
        self.test = test


class VFPDefVarArg(AST):
    def __init__(self, vfpdef):
        self.vfpdef = vfpdef


class VFPDefEqVarArg(AST):
    def __init__(self, vfpdef, test):
        self.vfpdef = vfpdef
        self.test = test


class StarVarArg(AST):
    def __init__(self, vfpdef):
        self.vfpdef = vfpdef


class DoubleStarVarArg(AST):
    def __init__(self, vfpdef):
        self.vfpdef = vfpdef


class VFPDef(AST):
    def __init__(self, name):
        self.name = name


class ExprSmallStmt(AST):
    def __init__(self, expr):
        self.expr = expr


class DelSmallStmt(AST):
    def __init__(self, expr_list):
        self.expr_list = expr_list


class PassSmallStmt(AST):
    pass


class GlobalSmallStmt(AST):
    def __init__(self, name_list):
        self.name_list = name_list


class NonlocalSmallStmt(AST):
    def __init__(self, name_list):
        self.name_list = name_list


class AssertSmallStmt(AST):
    def __init__(self, test_list):
        self.test_list = test_list


class NameList(AST):
    def __init__(self, name_list):
        self.name_list = name_list


class FlowStmt(AST):
    def __init__(self, flow_stmt):
        self.flow_stmt = flow_stmt


class BreakStmt(AST):
    pass


class ContinueStmt(AST):
    pass


class ReturnStmt(AST):
    def __init__(self, expr_list=None):
        self.expr_list = expr_list


class YieldStmt(AST):
    def __init__(self, expr_list=None):
        self.expr_list = expr_list


class RaiseStmt(AST):
    def __init__(self, test=None, from_test=None):
        self.test = test
        self.from_test = from_test


class CompoundStmt(AST):
    def __init__(self, comp_stmt):
        self.comp_stmt = comp_stmt


class IfStmt(AST):
    def __init__(self, test, suite, elif_list, else_suite=None):
        self.test = test
        self.suite = suite
        self.elif_list = elif_list
        self.else_suite = else_suite


class ElifClause(AST):
    def __init__(self, test_list, suite_list):
        self.test_list = test_list
        self.suite_list = suite_list


class WhileStmt(AST):
    def __init__(self, test, suite, else_suite=None):
        self.test = test
        self.suite = suite
        self.else_suite = else_suite


class ForStmt(AST):
    def __init__(self, expr_list, test_list, suite, else_suite=None):
        self.expr_list = expr_list
        self.test_list = test_list
        self.suite = suite
        self.else_suite = else_suite


class TryStmt(AST):
    def __init__(
        self,
        suite,
        except_clause=None,
        except_clause_suite=None,
        else_suite=None,
        finally_suite=None,
    ):
        self.suite = suite
        self.except_clause = except_clause
        self.except_clause_suite = except_clause_suite
        self.else_suite = else_suite
        self.finally_suite = finally_suite


class ExceptClause(AST):
    def __init__(self, test=None, as_name=None):
        self.test = test
        self.as_name = as_name


class WithStmt(AST):
    def __init__(self, with_item_list, suite):
        self.with_item_list = with_item_list
        self.suite = suite


class WithItemList(AST):
    def __init__(self, items):
        self.items = items


class WithItem(AST):
    def __init__(self, test, as_expr=None):
        self.test = test
        self.as_expr = as_expr


class SimpleStmtSuite(AST):
    def __init__(self, simple_stmt):
        self.simple_stmt = simple_stmt


class StmtListSuite(AST):
    def __init__(self, stmts):
        self.stmts = stmts


class DecoratedFunc(AST):
    def __init__(self, decorator_list, funcdef):
        self.decorator_list = decorator_list
        self.funcdef = funcdef


class DecoratedClass(AST):
    def __init__(self, decorator_list, classdef):
        self.decorator_list = decorator_list
        self.classdef = classdef


class DecoratorList(AST):
    def __init__(self, decorators):
        self.decorators = decorators


class Decorator(AST):
    def __init__(self, dotted_name, arg_list=None):
        self.dotted_name = dotted_name
        self.arg_list = arg_list


class DottedName(AST):
    def __init__(self, name_list):
        self.name_list = name_list


class ArgList(AST):
    def __init__(self, arguments):
        self.arguments = arguments


class EmptyTest(AST):
    pass


class TestArg(AST):
    def __init__(self, test):
        self.test = test

class TestCompForArg(AST):
    def __init__(self, test, comp_for):
        self.test = test
        self.comp_for = comp_for


class TestEqTestArg(AST):
    def __init__(self, test, eq_test):
        self.test = test
        self.eq_test = eq_test


class StarTestArg(AST):
    def __init__(self, test):
        self.test = test


class DoubleStarTestArg(AST):
    def __init__(self, test):
        self.test = test


class EmptyCompIter(AST):
    pass


class CompFor(AST):
    def __init__(self, expr_list, or_test, comp_iter):
        self.expr_list = expr_list
        self.or_test = or_test
        self.comp_iter = comp_iter


class CompIf(AST):
    def __init__(self, test_no_cond, comp_iter):
        self.test_no_cond = test_no_cond
        self.comp_iter = comp_iter


class SimpleExprStmt(AST):
    def __init__(self, test_list_star_expr):
        self.test_list_star_expr = test_list_star_expr


class AnnassignExprStmt(AST):
    def __init__(self, test_list_star_expr, annassign):
        self.test_list_star_expr = test_list_star_expr
        self.annassign = annassign


class AugassignExprStmt(AST):
    def __init__(self, test_list_star_expr, augassign, yield_or_test_list):
        self.test_list_star_expr = test_list_star_expr
        self.augassign = augassign
        self.yield_or_test_list = yield_or_test_list


class AssignExprStmt(AST):
    def __init__(self, test_list_star_expr, assign):
        self.test_list_star_expr = test_list_star_expr
        self.assign = assign


class TestListStarExpr(AST):
    def __init__(self, test_star_exprs):
        self.test_star_exprs = test_star_exprs


class YieldExpr(AST):
    def __init__(self, yield_arg=None):
        self.yield_arg = yield_arg


class FromTestYieldArg(AST):
    def __init__(self, from_test):
        self.from_test = from_test


class TestListYieldArg(AST):
    def __init__(self, test_list):
        self.test_list = test_list


class Assign(AST):
    def __init__(self, assignements):
        self.assignements = assignements


class Annassign(AST):
    def __init__(self, annotation, test):
        self.annotation = annotation
        self.test = test


class Augassign(AST):
    def __init__(self, sign):
        self.sign = sign


class OrTestTest(AST):
    def __init__(self, or_test):
        self.or_test = or_test


class CondOrTestTest(AST):
    def __init__(self, or_test, if_or_test, else_or_test):
        self.or_test = or_test
        self.if_or_test = if_or_test
        self.else_or_test = else_or_test


class LambdaDefTest(AST):
    def __init__(self, lambda_def):
        self.lambda_def = lambda_def


class LambdaDef(AST):
    def __init__(self, test, var_arg_list=None):
        self.test = test
        self.var_arg_list = var_arg_list


class NoCondLambdaDefTest(AST):
    def __init__(self, test_no_cond, var_arg_list=None):
        self.test_no_cond = test_no_cond
        self.var_arg_list = var_arg_list


class OrTest(AST):
    def __init__(self, and_test_list):
        self.and_test_list = and_test_list


class AndTest(AST):
    def __init__(self, not_test_list):
        self.not_test_list = not_test_list


class NotTest(AST):
    def __init__(self, not_test=None, comparison=None):
        self.not_test = not_test
        self.comparison = comparison


class Comparison(AST):
    def __init__(self, expr_list, comp_op_list):
        self.expr_list = expr_list
        self.comp_op_list = comp_op_list


class CompOp(AST):
    def __init__(self, sign):
        self.sign = sign


class StarExpr(AST):
    def __init__(self, expr):
        self.expr = expr


class Expr(AST):
    def __init__(self, xor_expr_list):
        self.xor_expr_list = xor_expr_list


class XorExpr(AST):
    def __init__(self, and_expr_list):
        self.and_expr_list = and_expr_list


class AndExpr(AST):
    def __init__(self, shift_expr_list):
        self.shift_expr_list = shift_expr_list


class ShiftExpr(AST):
    def __init__(self, arith_expr_list, shift_op_list):
        self.arith_expr_list = arith_expr_list
        self.shift_op_list = shift_op_list


class ArithExpr(AST):
    def __init__(self, term_list, arith_op_list):
        self.term_list = term_list
        self.arith_op_list = arith_op_list


class Term(AST):
    def __init__(self, factor_list, term_op_list):
        self.factor_list = factor_list
        self.term_op_list = term_op_list


class Factor(AST):
    def __init__(self, factor, op=None):
        self.factor = factor
        self.op = op


class Power(AST):
    def __init__(self, atom_expr, factor=None):
        self.atom_expr = atom_expr
        self.factor = factor


class AtomExpr(AST):
    def __init__(self, atom, trailer_expr):
        self.atom = atom
        self.trailer_expr = trailer_expr


class TrailerExpr(AST):
    def __init__(self, trailer_list):
        self.trailer_list = trailer_list


class ParenTrailer(AST):
    def __init__(self, arg_list):
        self.arg_list = arg_list


class BracketTrailer(AST):
    def __init__(self, subscript_list):
        self.subscript_list = subscript_list


class DotNameTrailer(AST):
    def __init__(self, name):
        self.name = name


class SubscriptList(AST):
    def __init__(self, subscript_list):
        self.subscript_list = subscript_list


class TestSubscript(AST):
    def __init__(self, test):
        self.test = test


class SliceSubscript(AST):
    def __init__(self, test_a=None, test_b=None, slice_op=None):
        self.test_a = test_a
        self.test_b = test_b
        self.slice_op = slice_op


class SliceOp(AST):
    def __init__(self, test=None):
        self.test = test


class EmptySliceOp(AST):
    pass


class ParYieldAtom(AST):
    def __init__(self, yield_expr):
        self.yield_expr = yield_expr


class TestListCompParAtom(AST):
    def __init__(self, test_list_comp):
        self.test_list_comp = test_list_comp


class TestListCompBracketAtom(AST):
    def __init__(self, test_list_comp):
        self.test_list_comp = test_list_comp


class EmptyParAtom(AST):
    pass


class EmptyBracketAtom(AST):
    pass


class EmptyBraceAtom(AST):
    pass


class NameAtom(AST):
    def __init__(self, name):
        self.name = name


class NumberAtom(AST):
    def __init__(self, number):
        self.number = number


class StringAtom(AST):
    def __init__(self, string):
        self.string = string


class NoneAtom(AST):
    pass


class BooleanAtom(AST):
    def __init__(self, boolean):
        self.boolean = boolean


class TestListComp(AST):
    def __init__(self, test_or_star_expr_list, comp_for):
        self.test_or_star_expr_list = test_or_star_expr_list
        self.comp_for = comp_for


class ExprList(AST):
    def __init__(self, expr_or_star_expr_list):
        self.expr_or_star_expr_list = expr_or_star_expr_list


class TestList(AST):
    def __init__(self, test_list):
        self.test_list = test_list