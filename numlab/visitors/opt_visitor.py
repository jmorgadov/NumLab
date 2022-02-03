import numlab.nl_ast as ast
from numlab.lang.visitor import Visitor

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring






class OptVisitor:

    visitor = Visitor().visitor

    def __init__(self):
        self.changes = []



    @visitor
    def check(self,     node: ast.Program):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.FuncDefStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ClassDefStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ConfDefStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ConfOption):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ReturnStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.DeleteStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AssignStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AugAssignStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AnnAssignStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ForStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.WhileStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.IfStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.Begsim):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.Endsim):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ResetStats):
        raise NotImplementedError()

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
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.BreakStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ContinueStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ExprStmt):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.BinOpExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.UnaryOpExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.LambdaExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.IfExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.DictExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.SetExpr):
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.ListExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.TupleExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.SliceExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.Args):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.Arg):
        raise NotImplementedError()
