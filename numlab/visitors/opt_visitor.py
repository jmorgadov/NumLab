from math import log2

import numlab.nl_ast as ast
import numlab.nl_builtins as builtins
from numlab.lang.visitor import Visitor

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring


class OptVisitor:

    visitor = Visitor().visitor

    def __init__(self):
        self.changes = []

    @visitor
    def check(self, node: ast.Program):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.FuncDefStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ClassDefStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ConfDefStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ConfOption):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ReturnStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.DeleteStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.AssignStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.AugAssignStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.AnnAssignStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ForStmt):
        self.changes.append((0,None, None))


    @visitor
    def check(self, node: ast.WhileStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.IfStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.Begsim):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.Endsim):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ResetStats):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.WithStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.WithItem):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.RaiseStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.TryStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ExceptHandler):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.AssertStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.GlobalStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.NonlocalStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.PassStmt):
        return node

    @visitor
    def check(self, node: ast.BreakStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ContinueStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.ExprStmt):
        self.changes.append((0,None, None))

    @visitor
    def check(self, node: ast.BinOpExpr):
        op = node.op
        if op == (ast.Operator.AND or ast.Operator.OR):
            def change_logical_ops(node: ast.BinOpExpr):
                node.right, node.left = node.left, node.right
            self.changes.append(1, change_logical_ops, change_logical_ops)
        if op == ast.Operator.MUL:
            if isinstance(node.right, int):
                fac = log2(node.right)
                if fac % 2 == 0:
                    def change_mult_by_lshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.LSHIFT
                        node.right = factor
                    def reverse_lshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.MUL
                        node.right = factor
                    self.changes.append(1, change_mult_by_lshift, reverse_lshift)
        if op == ast.Operator.DIV:
            if isinstance(node.right, int):
                fac = log2(node.right)
                if fac % 2 == 0:
                    def change_div_by_rshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.RSHIFT
                        node.right = factor
                    def reverse_rshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.DIV
                        node.right = factor
                    self.changes.append(1, change_div_by_rshift, reverse_rshift)

    @visitor
    def check(self, node: ast.UnaryOpExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.LambdaExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.IfExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.DictExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.SetExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ListCompExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.SetCompExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.DictCompExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.GeneratorExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.Comprehension):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.YieldExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.YieldFromExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.CompareExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.CallExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.Keyword):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ConstantExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.AttributeExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.SubscriptExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.StarredExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.NameExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ListExpr):
        items = [self.check(i) for i in node.elts]
        return builtins.nl_list(items)

    @visitor
    def check(self, node: ast.TupleExpr):
        items = tuple(self.check(i) for i in node.elts)
        return builtins.nl_tuple(items)

    @visitor
    def check(self, node: ast.SliceExpr):
        low = self.check(node.lower) if node.lower is not None else None
        upper = self.check(node.upper) if node.upper is not None else None
        step = self.check(node.step) if node.step is not None else None
        return builtins.nl_slice(low, upper, step)

    @visitor
    def check(self, node: ast.Args):
        return node

    @visitor
    def check(self, node: ast.Arg):
        return node
