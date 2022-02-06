from math import log2

import numlab.nl_ast as ast
from numlab.lang.visitor import Visitor
from numlab.optimization.fuzzy_opt_classifier import FuzzyOptClassifier

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring


SHIFT_CAT = 0.2
IF_COND_CAT = 0.6
WHILE_COND_CAT = 0.9

class OptVisitor:

    visitor = Visitor().visitor

    def __init__(self):
        self.changes = []
        self.values = {}
        self.classifier = FuzzyOptClassifier()
        self.loop_depth = 0

    @visitor
    def check(self, node: ast.Program):
        for elem in node.stmts:
            self.check(elem)

    @visitor
    def check(self, node: ast.FuncDefStmt):
        for arg in node.args.args:
            if arg.default is not None:
                self.check(arg.default)
        for stmt in node.body:
            self.check(stmt)

    @visitor
    def check(self, node: ast.ClassDefStmt):
        for base in node.bases:
            self.check(base)
        for stmt in node.body:
            self.check(stmt)

    @visitor
    def check(self, node: ast.ConfDefStmt):
        for conf_opt in node.configs:
            self.check(conf_opt)

    @visitor
    def check(self, node: ast.ConfOption):
        self.check(node.value)

    @visitor
    def check(self, node: ast.ReturnStmt):
        for val in node.expr.elts:
            self.check(val)

    @visitor
    def check(self, node: ast.DeleteStmt):
        for target in node.targets:
            self.check(target)

    @visitor
    def check(self, node: ast.AssignStmt):
        for item in node.value.elts:
            self.check(item)

    @visitor
    def check(self, node: ast.AugAssignStmt):
        self.check(node.value.elts[0])

    @visitor
    def check(self, node: ast.AnnAssignStmt):
        self.check(node.value)

    @visitor
    def check(self, node: ast.ForStmt):
        self.check(node.iter_expr.elts[0])
        self.loop_depth += 1
        for stmt in node.body:
            self.check(stmt)
        self.loop_depth -= 1
        for stmt in node.orelse:
            self.check(stmt)

    def flat_test(self, test: ast.Expr, oper: ast.Operator):
        if isinstance(test, ast.BinOpExpr) and test.op == oper:
            flat_left = self.flat_test(test.left, oper)
            flat_right = self.flat_test(test.right, oper)
            return flat_left + flat_right
        return [test]

    def unflat_test(self, items, oper=ast.Operator.OR):
        if not isinstance(items, list):
            return items
        if len(items) == 1:
            return self.unflat_test(items[0])
        and_items = [
            self.unflat_test(item, ast.Operator.AND) if isinstance(item, list) else item
            for item in items
        ]

        return ast.BinOpExpr(
            oper,
            self.unflat_test(and_items[0]),
            self.unflat_test(and_items[1:]),
        )

    def testcheck(self, test, from_while=False):
        if isinstance(test, ast.BinOpExpr):
            op = test.op
            if op == ast.Operator.AND or op == ast.Operator.OR:

                def change_logical_ops(node: ast.BinOpExpr):
                    node.right, node.left = node.left, node.right

                self.changes.append((test, change_logical_ops, change_logical_ops))
                cat = WHILE_COND_CAT if from_while else IF_COND_CAT
                self.classifier.add_change(cat, self.loop_depth)

    @visitor
    def check(self, node: ast.WhileStmt):
        self.testcheck(node.test, True)
        self.check(node.test)
        for stmt in node.body:
            self.check(stmt)
        for stmt in node.orelse:
            self.check(stmt)

    @visitor
    def check(self, node: ast.IfStmt):
        self.testcheck(node.test)
        self.check(node.test)
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
        pass

    @visitor
    def check(self, node: ast.BreakStmt):
        pass

    @visitor
    def check(self, node: ast.ContinueStmt):
        pass

    @visitor
    def check(self, node: ast.ExprStmt):
        self.check(node.expr)

    def can_shift(self, node):
        if isinstance(node, ast.ConstantExpr) and isinstance(node.value, int):
            orig = node.value
            fac = log2(orig)
            if int(fac) == fac:
                return True, orig, int(fac)
        return False, None, None

    @visitor
    def check(self, node: ast.BinOpExpr):
        op = node.op
        if op == ast.Operator.MUL:
            ret, orig1, fac1 = self.can_shift(node.right)
            if ret:

                def change_mult_by_lshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.LSHIFT
                    node.right.value = fac1

                def reverse_lshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.MUL
                    node.right.value = orig1

                self.changes.append((node, change_mult_by_lshift, reverse_lshift))
                self.classifier.add_change(SHIFT_CAT, self.loop_depth)
            ret, orig2, fac2 = self.can_shift(node.left)
            if ret:

                def change_mult_by_lshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.LSHIFT
                    node.left.value = fac2
                    node.left, node.right = node.right, node.left

                def reverse_lshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.MUL
                    node.left, node.right = node.right, node.left
                    node.left.value = orig2

                self.changes.append((node, change_mult_by_lshift, reverse_lshift))
                self.classifier.add_change(SHIFT_CAT, self.loop_depth)
        if op == ast.Operator.DIV:
            ret, orig3, fac3 = self.can_shift(node.right)
            if ret:

                def change_div_by_rshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.RSHIFT
                    node.right.value = fac3

                def reverse_rshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.DIV
                    node.right.value = orig3

                self.changes.append((node, change_div_by_rshift, reverse_rshift))
                self.classifier.add_change(SHIFT_CAT, self.loop_depth)
            ret, orig4, fac4 = self.can_shift(node.left)
            if ret:

                def change_div_by_rshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.RSHIFT
                    node.left.value = fac4
                    node.left, node.right = node.right, node.left

                def reverse_rshift(node: ast.BinOpExpr):
                    node.op = ast.Operator.DIV
                    node.left, node.right = node.right, node.left
                    node.left.value = orig4

                self.changes.append((node, change_div_by_rshift, reverse_rshift))
                self.classifier.add_change(SHIFT_CAT, self.loop_depth)
        self.check(node.left)
        self.check(node.right)

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
        pass

    @visitor
    def check(self, node: ast.SetCompExpr):
        pass

    @visitor
    def check(self, node: ast.DictCompExpr):
        pass

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
        pass

    @visitor
    def check(self, node: ast.CallExpr):
        for arg in node.args:
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
        pass

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
        pass

    @visitor
    def check(self, node: ast.Arg):
        pass
