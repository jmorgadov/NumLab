import numlab.nl_ast as ast
from numlab.lang.visitor import Visitor

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring


class OptVisitor:

    visitor = Visitor().visitor

    def __init__(self):
        self.changes = []

    @visitor
    def check(self, node: ast.Program):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.FuncDefStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ClassDefStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ConfDefStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ConfOption):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ReturnStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.DeleteStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.AssignStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.AugAssignStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.AnnAssignStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ForStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.WhileStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.IfStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.Begsim):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.Endsim):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ResetStats):
        raise NotImplementedError()

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
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.BreakStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ContinueStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.ExprStmt):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.BinOpExpr):
        raise NotImplementedError()

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
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.TupleExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.SliceExpr):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.Args):
        raise NotImplementedError()

    @visitor
    def check(self, node: ast.Arg):
        raise NotImplementedError()
