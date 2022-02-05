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
        for elem in node.stmts:
            self.check(elem)

    @visitor
    def check(self, node: ast.FuncDefStmt):
        for arg in node.args.args:
            if arg.default is not None:
                self.check(arg.default)

    @visitor
    def check(self, node: ast.ClassDefStmt):
        for base in node.bases:
            self.check(base) 

    @visitor
    def check(self, node: ast.ConfDefStmt):
        for conf_opt in node.configs:
            self.check(conf_opt)

    @visitor
    def check(self, node: ast.ConfOption):
        self.check(node.value)

    @visitor
    def check(self, node: ast.ReturnStmt):
        val = node.expr.elts
        if len(val) == 1:
            val = val[0]
        self.eval(val)

    @visitor
    def check(self, node: ast.DeleteStmt):
        for target in node.targets:
            target.ctx = ast.ExprCtx.DEL
            self.check(target)

    @visitor
    def check(self, node: ast.AssignStmt):
        for item in node.value.elts:
            self.check(item)

    @visitor
    def check(self, node: ast.AugAssignStmt):
        self.check(node.target.elts[0])
        self.check(node.value.elts[0])

    @visitor
    def check(self, node: ast.AnnAssignStmt):
        self.check(node.target)
        self.check(node.value)

    @visitor
    def check(self, node: ast.ForStmt):
        self.check(node.iter_expr.elts[0])
        for stmt in node.body:
            self.check(stmt)
        for stmt in node.orelse:
            self.check(stmt)

    def testcheck(self, test: ast.Expr):
        if isinstance(test, ast.BinOpExpr):
            op: ast.BinOpExpr = test.op
            if op == ast.Operator.AND or op == ast.Operator.OR:
                def change_logical_ops(node: ast.BinOpExpr):
                    node.right, node.left = node.left, node.right
                self.changes.append(test, change_logical_ops, change_logical_ops)

    @visitor
    def check(self, node: ast.WhileStmt):
        testcheck(node.test)
        for stmt in node.body:
            self.check(stmt)
        for stmt in node.orelse:
            self.check(stmt)

    @visitor
    def check(self, node: ast.IfStmt):
        testcheck(node.test)
        for stmt in node.body:
            self.check(stmt)
        for stmt in node.orelse:
            self.check(stmt)

    @visitor
    def check(self, node: ast.Begsim):
        pass

    @visitor
    def check(self, node: ast.Endsim):
        pass

    @visitor
    def check(self, node: ast.ResetStats):
        pass

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
        pass

    @visitor
    def check(self, node: ast.ContinueStmt):
        pass

    @visitor
    def check(self, node: ast.ExprStmt):
        self.check(node.expr)

    @visitor
    def check(self, node: ast.BinOpExpr):
        op = node.op
        if op == ast.Operator.MUL:
            if isinstance(node.right, ast.ConstantExpr) and isinstance(node.right.value, int):
                fac = log2(node.right)
                if fac % 2 == 0:
                    def change_mult_by_lshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.LSHIFT
                        node.right.value = factor
                    def reverse_lshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.MUL
                        node.right.value = factor
                    self.changes.append(node, change_mult_by_lshift, reverse_lshift)
        if op == ast.Operator.DIV:
            if isinstance(node.right, ast.ConstantExpr) and isinstance(node.right.value, int):
                fac = log2(node.right)
                if fac % 2 == 0:
                    def change_div_by_rshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.RSHIFT
                        node.right.value = factor
                    def reverse_rshift(node: ast.BinOpExpr, factor: int):
                        node.op = ast.Operator.DIV
                        node.right.value = factor
                    self.changes.append(node, change_div_by_rshift, reverse_rshift)

    @visitor
    def check(self, node: ast.UnaryOpExpr):
        self.check(node.operand)

    @visitor
    def check(self, node: ast.LambdaExpr):
        for dec in node.decorator[::-1]:
            self.check(dec)
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.IfExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.DictExpr):
        for key, value in zip(node.keys, node.values):
            self.check(key)
            self.check(value)

    @visitor
    def check(self, node: ast.SetExpr):
        for elem in node.values:
            self.check(elem)

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
        for arg in node .args:
            self.check(arg)
        for kwarg in node.keywords:
            self.check(kwarg)
        if isinstance(node.func, ast.AttributeExpr):
            self.check(node.func.value)
        if not isinstance(node.func, ast.NameExpr):
            self.check(node.func)

    @visitor
    def check(self, node: ast.Keyword):
        self.check(node.value)

    @visitor
    def check(self, node: ast.ConstantExpr):
        pass

    @visitor
    def check(self, node: ast.AttributeExpr):
        self.check(node.value)

    @visitor
    def check(self, node: ast.SubscriptExpr):
        self.check(node.value)
        self.check(node.slice_expr)

    @visitor
    def check(self, node: ast.StarredExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.NameExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ListExpr):
        items = [self.check(i) for i in node.elts]

    @visitor
    def check(self, node: ast.TupleExpr):
        items = tuple(self.check(i) for i in node.elts)

    @visitor
    def check(self, node: ast.SliceExpr):
        low = self.check(node.lower) if node.lower is not None else None
        upper = self.check(node.upper) if node.upper is not None else None
        step = self.check(node.step) if node.step is not None else None

    @visitor
    def check(self, node: ast.Args):
        return node

    @visitor
    def check(self, node: ast.Arg):
        return node
