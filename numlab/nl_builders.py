import numlab.nl_ast as ast

builders = {
    # -------------------------------------------------------------------------
    "program -> stmt program": lambda s, p: ast.Program([s] + p.stmts),
    "program -> NEWLINE program": lambda n, p: p,
    "program -> EPS": lambda: ast.Program([]),
    # -------------------------------------------------------------------------
    "stmt -> simple_stmt": lambda s: ast.Stmt(s),
    "stmt -> compound_stmt": lambda c: ast.Stmt(c),
    # -------------------------------------------------------------------------
    "stmt_list -> stmt": lambda s: ast.StmtList([s]),
    "stmt_list -> stmt stmt_list": lambda s, sl: ast.StmtList([s] + sl.stmts),
    # -------------------------------------------------------------------------
    "simple_stmt -> small_stmt NEWLINE": lambda s, n: ast.SimpleStmt(s),
    # -------------------------------------------------------------------------
    "funcdef -> def NAME ( ) : suite": lambda d, n, p, p2, c, s: ast.FuncDef(n, s),
    "funcdef -> def NAME ( parameters ) : suite": lambda d, n, p, par, p2, c, s: ast.FuncDef(
        n, s, par
    ),
    # -------------------------------------------------------------------------
    "classdef -> class NAME : suite": lambda c, n, c_, s: ast.ClassDef(n, s),
    "classdef -> class NAME ( arglist ) : suite": lambda c, n, p, a, c_, s: ast.ClassDef(
        n, s, a
    ),
    # -------------------------------------------------------------------------
    "parameters -> param": lambda p: ast.Parameters([p]),
    "parameters -> param , parameters": lambda p, ps: ast.Parameters([p] + ps.params),
    # -------------------------------------------------------------------------
    "param -> tfpdef": lambda p: ast.TFPDefParam(p),
    "param -> tfpdef = test": lambda p, e, t: ast.TFPDefEqParam(p, t),
    "param -> * tfpdef": lambda s, p: ast.StarParam(p),
    "param -> ** tfpdef": lambda ss, p: ast.DoubleStarParam(p),
    # -------------------------------------------------------------------------
    "tfpdef -> NAME": lambda n: ast.TFPDef(n.value),
    "tfpdef -> NAME : test": lambda n, t: ast.TFPDef(n.value, t),
    # -------------------------------------------------------------------------
    "varargslist -> vfpdef": lambda v: ast.VarArgList([v]),
    "varargslist -> vfpdef , varargslist": lambda v, c, va: ast.VarArgList(
        [v] + va.vargs
    ),
    # -------------------------------------------------------------------------
    "vararg -> vfpdef": lambda v: ast.VFPDefVarArg(v),
    "vararg -> vfpdef = test": lambda v, e, t: ast.VFPDefEqVarArg(v, t),
    "vararg -> * vfpdef": lambda s, v: ast.StarVarArg(v),
    "vararg -> ** vfpdef": lambda ss, v: ast.DoubleStarVarArg(v),
    # -------------------------------------------------------------------------
    "vfpdef -> NAME": lambda n: ast.VFPDef(n.value),
    # -------------------------------------------------------------------------
    "small_stmt -> expr_stmt": lambda e: ast.SmallStmt(e),
    "small_stmt -> del_stmt": lambda d: ast.SmallStmt(d),
    "small_stmt -> pass_stmt": lambda p: ast.SmallStmt(p),
    "small_stmt -> flow_stmt": lambda f: ast.SmallStmt(f),
    "small_stmt -> global_stmt": lambda g: ast.SmallStmt(g),
    "small_stmt -> nonlocal_stmt": lambda n: ast.SmallStmt(n),
    "small_stmt -> assert_stmt": lambda a: ast.SmallStmt(a),
    # "small_stmt -> import_stmt": lambda i: ast.SmallStmt(i),
    # -------------------------------------------------------------------------
    "del_stmt -> del exprlist": lambda l, e: ast.DelSmallStmt(e),
    # -------------------------------------------------------------------------
    "pass_stmt -> pass": lambda p: ast.PassSmallStmt(),
    # -------------------------------------------------------------------------
    "global_stmt -> global namelist": lambda g, nl: ast.GlobalSmallStmt(nl),
    # -------------------------------------------------------------------------
    "nonlocal_stmt -> nonlocal namelist": lambda n, nl: ast.NonlocalSmallStmt(nl),
    # -------------------------------------------------------------------------
    "assert_stmt -> assert test_list": lambda a, t: ast.AssertSmallStmt(t),
    # -------------------------------------------------------------------------
    "namelist -> NAME": lambda n: ast.NameList([n]),
    "namelist -> NAME , namelist": lambda n, c, nl: ast.NameList([n] + nl.name_list),
    # -------------------------------------------------------------------------
    "flow_stmt -> break_stmt": lambda b: ast.FlowStmt(b),
    "flow_stmt -> continue_stmt": lambda c: ast.FlowStmt(c),
    "flow_stmt -> return_stmt": lambda r: ast.FlowStmt(r),
    "flow_stmt -> raise_stmt": lambda r: ast.FlowStmt(r),
    "flow_stmt -> yield_stmt": lambda y: ast.FlowStmt(y),
    # -------------------------------------------------------------------------
    "break_stmt -> break": lambda b: ast.BreakStmt(),
    # -------------------------------------------------------------------------
    "continue_stmt -> continue": lambda c: ast.ContinueStmt(),
    # -------------------------------------------------------------------------
    "return_stmt -> return": lambda r: ast.ReturnStmt(),
    "return_stmt -> return exprlist": lambda r, e: ast.ReturnStmt(e),
    # -------------------------------------------------------------------------
    "yield_stmt -> yield": lambda y: ast.YieldStmt(),
    "yield_stmt -> yield exprlist": lambda y, e: ast.YieldStmt(e),
    # -------------------------------------------------------------------------
    "raise_stmt -> raise": lambda r: ast.RaiseStmt(),
    "raise_stmt -> raise test": lambda r, t: ast.RaiseStmt(t),
    "raise_stmt -> raise test from test": lambda r, t, f, t2: ast.RaiseStmt(t, t2),
    # -------------------------------------------------------------------------
    "compound_stmt -> if_stmt": lambda i: ast.CompoundStmt(i),
    "compound_stmt -> while_stmt": lambda w: ast.CompoundStmt(w),
    "compound_stmt -> for_stmt": lambda f: ast.CompoundStmt(f),
    "compound_stmt -> try_stmt": lambda t: ast.CompoundStmt(t),
    "compound_stmt -> with_stmt": lambda w: ast.CompoundStmt(w),
    "compound_stmt -> funcdef": lambda f: ast.CompoundStmt(f),
    "compound_stmt -> classdef": lambda c: ast.CompoundStmt(c),
    "compound_stmt -> decorated": lambda d: ast.CompoundStmt(d),
    # -------------------------------------------------------------------------
    "if_stmt -> if test : suite elif_clause": lambda i, t, s, e: ast.IfStmt(t, s, e),
    "if_stmt -> if test : suite elif_clause else : suite": (
        lambda i, t, s, e, el, s2: ast.IfStmt(t, s, e, s2)
    ),
    # -------------------------------------------------------------------------
    "elif_clause -> elif test : suite elif_clause": (
        lambda e, t, s, e2: ast.ElifClause([t] + e2.test_list, [s] + e2.suite_list)
    ),
    "elif_clause -> EPS": lambda: ast.ElifClause([], []),
    # -------------------------------------------------------------------------
    "while_stmt -> while test : suite": lambda w, t, c, s: ast.WhileStmt(t, s),
    "while_stmt -> while test : suite else : suite": (
        lambda w, t, c, s, e, c2, s2: ast.WhileStmt(t, s, s2)
    ),
    # -------------------------------------------------------------------------
    "for_stmt -> for exprlist in test_list : suite": (
        lambda f, e, i, t, c, s: ast.ForStmt(e, t, s)
    ),
    "for_stmt -> for exprlist in test_list : suite else : suite": (
        lambda f, e, i, t, c, s, e2, c2, s2: ast.ForStmt(e, t, s, s2)
    ),
    # -------------------------------------------------------------------------
    "try_stmt -> try : suite except_clause : suite": (
        lambda t, c, s, e, c2, s2: ast.TryStmt(s, e, s2)
    ),
    "try_stmt -> try : suite": lambda t, c, s: ast.TryStmt(s),
    "try_stmt -> try : suite except_clause : suite": (
        lambda t, c, s, e, c2, s2: ast.TryStmt(s, e, s2)
    ),
    "try_stmt -> try : suite except_clause : suite else : suite": (
        lambda t, c, s, e, c2, s2, e2, c3, s3: ast.TryStmt(s, e, s2, else_suite=s3)
    ),
    "try_stmt -> try : suite except_clause : suite finally : suite": (
        lambda t, c, s, e, c2, s2, f, c3, s3: ast.TryStmt(s, e, s2, finally_suite=s3)
    ),
    "try_stmt -> try : suite except_clause : suite else : suite finally : suite": (
        lambda t, c, s, e, c2, s2, e2, c3, s3, f, c4, s4: ast.TryStmt(
            s, e, s2, else_suite=s3, finally_suite=s4
        )
    ),
    # -------------------------------------------------------------------------
    "except_clause -> except": lambda e: ast.ExceptClause(),
    "except_clause -> except test": lambda e, t: ast.ExceptClause(t),
    "except_clause -> except test as NAME": lambda e, t, a, n: ast.ExceptClause(t, n),
    # -------------------------------------------------------------------------
    "with_stmt -> with with_items : suite": lambda w, i, c, s: ast.WithStmt(i, s),
    # -------------------------------------------------------------------------
    "with_items -> with_item": lambda i: ast.WithItemList([i]),
    "with_items -> with_item , with_items": (
        lambda i, c, i2: ast.WithItemList([i] + i2.items)
    ),
    # -------------------------------------------------------------------------
    "with_item -> test": lambda t: ast.WithItem(t),
    "with_item -> test as expr": lambda t, a, e: ast.WithItem(t, e),
    # -------------------------------------------------------------------------
    "suite -> simple_stmt": lambda s: ast.SimpleStmtSuite(s),
    "suite -> NEWLINE INDENT stmt_list DEDENT": lambda n, i, l, d: ast.StmtListSuite(l),
    # -------------------------------------------------------------------------
    "decorated -> decorators funcdef": lambda d, f: ast.DecoratedFunc(d, f),
    "decorated -> decorators classdef": lambda d, c: ast.DecoratedClass(d, c),
    # -------------------------------------------------------------------------
    "decorators -> decorator decorators": lambda d, d2: ast.DecoratorList(
        [d] + d2.decorators
    ),
    "decorators -> decorator": lambda d: ast.DecoratorList([d]),
    # -------------------------------------------------------------------------
    "decorator -> @ dotted_name NEWLINE": lambda d, n, nl: ast.Decorator(n),
    "decorator -> @ dotted_name ( ) NEWLINE": lambda d, n, p, nl: ast.Decorator(n, []),
    "decorator -> @ dotted_name ( arglist ) NEWLINE": (
        lambda d, n, p, a, nl: ast.Decorator(n, a.arg_list)
    ),
    # -------------------------------------------------------------------------
    "dotted_name -> NAME": lambda n: ast.DottedName([n]),
    "dotted_name -> NAME . dotted_name": (
        lambda n, c, n2: ast.DottedName([n] + n2.name_list)
    ),
    # -------------------------------------------------------------------------
    "arglist -> argument": lambda a: ast.ArgList([a]),
    "arglist -> argument , arglist": (lambda a, c, a2: ast.ArgList([a] + a2.arguments)),
    # -------------------------------------------------------------------------
    "argument -> test": lambda t: ast.TestArg(t),
    "argument -> test comp_for": lambda t, c: ast.TestCompForArg(t, c),
    "argument -> test = test": lambda t, e, t2: ast.TestEqTestArg(t, t2),
    "argument -> * test": lambda a, t: ast.StarTestArg(t),
    "argument -> ** test": lambda a, t: ast.DoubleStarTestArg(t),
    # -------------------------------------------------------------------------
    "comp_for -> for exprlist in or_test comp_iter": (
        lambda f, e, i, o, c: ast.CompFor(e, o, c)
    ),
    # -------------------------------------------------------------------------
    "comp_if -> if test_nocond comp_iter": lambda i, t, c: ast.CompIf(t, c),
    # -------------------------------------------------------------------------
    "comp_iter -> comp_for": lambda c: c,
    "comp_iter -> comp_if": lambda c: c,
    "comp_iter -> EPS": lambda: ast.EmptyCompIter(),
    # -------------------------------------------------------------------------
    "expr_stmt -> testlist_star_expr annassign": (
        lambda t, a: ast.AnnassignExprStmt(t, a)
    ),
    "expr_stmt -> testlist_star_expr augassign yield_or_testlist": (
        lambda t, a, y: ast.AugassignExprStmt(t, a, y)
    ),
    "expr_stmt -> testlist_star_expr assign": lambda t, a: ast.AssignExprStmt(t, a),
    # -------------------------------------------------------------------------
    "testlist_star_expr -> test_or_star_expr": lambda t: ast.TestListStarExpr([t]),
    "testlist_star_expr -> test_or_star_expr , testlist_star_expr": (
        lambda t, c, t2: ast.TestListStarExpr([t] + t2.test_star_exprs)
    ),
    # -------------------------------------------------------------------------
    "yield_or_testlist -> yield_expr": lambda y: y,
    "yield_or_testlist -> test_list": lambda t: t,
    # -------------------------------------------------------------------------
    "yield_expr -> yield": lambda y: ast.YieldExpr(),
    "yield_expr -> yield yield_arg": lambda y, a: ast.YieldExpr(a),
    # -------------------------------------------------------------------------
    "yield_arg -> from test": lambda f, t: ast.FromTestYieldArg(t),
    "yield_arg -> test_list": lambda t: ast.TestListYieldArg(t),
    # -------------------------------------------------------------------------
    "assign -> = yield_expr assign": (lambda e, y, a: ast.Assign([a] + a.assignements)),
    "assign -> = testlist_star_expr assign": (
        lambda e, y, a: ast.Assign([a] + a.assignements)
    ),
    "assign -> EPS": lambda: ast.Assign([]),
    # -------------------------------------------------------------------------
    "annassign -> : test = test": lambda c, a, e, t: ast.Annassign(a, t),
    # -------------------------------------------------------------------------
    "augassign -> +=": lambda a: ast.Augassign(a.value),
    "augassign -> -=": lambda a: ast.Augassign(a.value),
    "augassign -> *=": lambda a: ast.Augassign(a.value),
    "augassign -> @=": lambda a: ast.Augassign(a.value),
    "augassign -> /=": lambda a: ast.Augassign(a.value),
    "augassign -> %=": lambda a: ast.Augassign(a.value),
    "augassign -> &=": lambda a: ast.Augassign(a.value),
    "augassign -> |=": lambda a: ast.Augassign(a.value),
    "augassign -> ^=": lambda a: ast.Augassign(a.value),
    "augassign -> <<=": lambda a: ast.Augassign(a.value),
    "augassign -> >>=": lambda a: ast.Augassign(a.value),
    "augassign -> **=": lambda a: ast.Augassign(a.value),
    "augassign -> //=": lambda a: ast.Augassign(a.value),
    # -------------------------------------------------------------------------
    "test -> or_test": lambda o: ast.OrTestTest(o),
    "test -> or_test if or_test else test": (
        lambda o, i, o2, e, t: ast.CondOrTestTest(o, o2, t)
    ),
    "test -> lambdef": lambda l: ast.LambdaDefTest(l),
    # -------------------------------------------------------------------------
    "test_nocond -> or_test": lambda o: ast.OrTestTest(o),
    "test_nocond -> lambdef_nocond": lambda l: ast.NoCondLambdaDefTest(l),
    # -------------------------------------------------------------------------
    "lambdef -> lambda : test": lambda l, c, t: ast.LambdaDef(t),
    "lambdef -> lambda varargslist : test": lambda l, v, c, t: ast.LambdaDef(t, v),
    # -------------------------------------------------------------------------
    "lambdef_nocond -> lambda : test_nocond": lambda l, c, t: ast.LambdaDef(t),
    "lambdef_nocond -> lambda varargslist : test_nocond": (
        lambda l, v, c, t: ast.LambdaDef(t, v)
    ),
    # -------------------------------------------------------------------------
    "or_test -> and_test": lambda a: ast.OrTest([a]),
    "or_test -> and_test or or_test": (
        lambda a, o, o2: ast.OrTest([a] + o2.or_test_list)
    ),
    # -------------------------------------------------------------------------
    "and_test -> not_test": lambda n: ast.AndTest([n]),
    "and_test -> not_test and and_test": (
        lambda n, a, a2: ast.AndTest([n] + a2.and_test_list)
    ),
    # -------------------------------------------------------------------------
    "not_test -> not not_test": lambda n, t: ast.NotTest(t),
    "not_test -> comparison": lambda c: ast.NotTest(c),
    # -------------------------------------------------------------------------
    "comparison -> expr": lambda e: ast.Comparison(e, []),
    "comparison -> expr comp_op comparison": (
        lambda e, o, c: ast.Comparison(e, [o] + c.comparison_list)
    ),
    # -------------------------------------------------------------------------
    "comp_op -> <": lambda c: ast.CompOp(c.value),
    "comp_op -> >": lambda c: ast.CompOp(c.value),
    "comp_op -> ==": lambda c: ast.CompOp(c.value),
    "comp_op -> >=": lambda c: ast.CompOp(c.value),
    "comp_op -> <=": lambda c: ast.CompOp(c.value),
    "comp_op -> !=": lambda c: ast.CompOp(c.value),
    "comp_op -> in": lambda c: ast.CompOp(c.value),
    "comp_op -> not in": lambda c, c2: ast.CompOp(f"{c.value} {c2.value}"),
    "comp_op -> is": lambda c: ast.CompOp(c.value),
    "comp_op -> is not": lambda c, c2: ast.CompOp(f"{c.value} {c2.value}"),
    # -------------------------------------------------------------------------
    "star_expr -> * expr": lambda e: ast.StarExpr(e),
    # -------------------------------------------------------------------------
    "expr -> xor_expr": lambda x: ast.Expr([x]),
    "expr -> xor_expr | expr": (lambda x, o, e: ast.Expr([x] + e.xor_expr_list)),
    # -------------------------------------------------------------------------
    "xor_expr -> and_expr": lambda a: ast.XorExpr([a]),
    "xor_expr -> and_expr ^ xor_expr": (
        lambda a, o, x: ast.XorExpr([a] + x.and_expr_list)
    ),
    # -------------------------------------------------------------------------
    "and_expr -> shift_expr": lambda s: ast.AndExpr([s]),
    "and_expr -> shift_expr & and_expr": (
        lambda s, o, a: ast.AndExpr([s] + a.shift_expr_list)
    ),
    # -------------------------------------------------------------------------
    "shift_expr -> arith_expr": lambda a: ast.ShiftExpr([a], []),
    "shift_expr -> arith_expr << shift_expr": (
        lambda a, o, s: ast.ShiftExpr(
            [a] + s.arith_expr_list, [o.value] + s.shift_op_list
        )
    ),
    "shift_expr -> arith_expr >> shift_expr": (
        lambda a, o, s: ast.ShiftExpr(
            [a] + s.arith_expr_list, [o.value] + s.shift_op_list
        )
    ),
    # -------------------------------------------------------------------------
    "arith_expr -> term": lambda t: ast.ArithExpr([t], []),
    "arith_expr -> term + arith_expr": (
        lambda t, o, a: ast.ArithExpr([t] + a.term_list, [o.value] + a.arith_op_list)
    ),
    "arith_expr -> term - arith_expr": (
        lambda t, o, a: ast.ArithExpr([t] + a.term_list, [o.value] + a.arith_op_list)
    ),
    # -------------------------------------------------------------------------
    "term -> factor": lambda f: ast.Term([f], []),
    "term -> factor * term": (
        lambda f, o, t: ast.Term([f] + t.factor_list, [o.value] + t.term_op_list)
    ),
    "term -> factor @ term": (
        lambda f, o, t: ast.Term([f] + t.factor_list, [o.value] + t.term_op_list)
    ),
    "term -> factor / term": (
        lambda f, o, t: ast.Term([f] + t.factor_list, [o.value] + t.term_op_list)
    ),
    "term -> factor % term": (
        lambda f, o, t: ast.Term([f] + t.factor_list, [o.value] + t.term_op_list)
    ),
    "term -> factor // term": (
        lambda f, o, t: ast.Term([f] + t.factor_list, [o.value] + t.term_op_list)
    ),
    # -------------------------------------------------------------------------
    "factor -> + factor": lambda o, f: ast.Factor(f, o.value),
    "factor -> - factor": lambda o, f: ast.Factor(f, o.value),
    "factor -> ~ factor": lambda o, f: ast.Factor(f, o.value),
    "factor -> power": lambda p: ast.Factor(p),
    # -------------------------------------------------------------------------
    "power -> atom_expr": lambda a: ast.Power(a),
    "power -> atom_expr ** factor": lambda a, o, f: ast.Power(a, f),
    # -------------------------------------------------------------------------
    "atom_expr -> atom trailer_expr": lambda a, t: ast.AtomExpr(a, t),
    # -------------------------------------------------------------------------
    "trailer_expr -> trailer trailer_expr": (
        lambda t, t2: ast.TrailerExpr([t] + t2.trailer_list)
    ),
    "trailer_expr -> EPS": lambda: ast.TrailerExpr([]),
    # -------------------------------------------------------------------------
    "trailer -> ( arglist )": lambda p, a, p2: ast.ParenTrailer(a),
    "trailer -> [ subscriptlist ]": lambda b, s, b2: ast.BracketTrailer(s),
    "trailer -> . NAME": lambda d, n: ast.DotNameTrailer(n),
    # -------------------------------------------------------------------------
    "subscriptlist -> subscript": lambda s: ast.SubscriptList([s]),
    "subscriptlist -> subscript , subscriptlist": (
        lambda s, o, s2: ast.SubscriptList([s] + s2.subscript_list)
    ),
    # -------------------------------------------------------------------------
    "subscript -> test": lambda t: ast.TestSubscript(t),
    "subscript -> maybe_test : maybe_test sliceop": (
        lambda ta, o, tb, so: ast.SliceSubscript(ta, tb, so)
    ),
    # -------------------------------------------------------------------------
    "sliceop -> : maybe_test": lambda o, t: ast.SliceOp(t),
    "sliceop -> EPS": lambda: ast.EmptySliceOp(),
    # -------------------------------------------------------------------------
    "maybe_test -> test": lambda t: t,
    "maybe_test -> EPS": lambda: ast.EmptyTest(),
    # -------------------------------------------------------------------------
    "atom -> ( yield_expr )": lambda p1, y, p2: ast.ParYieldAtom(y),
    "atom -> ( testlist_comp )": lambda p1, t, p2: ast.TestListCompParAtom(t),
    "atom -> [ testlist_comp ]": lambda b1, t, b2: ast.TestListCompBracketAtom(t),
    "atom -> ( )": lambda p1, p2: ast.EmptyParAtom(),
    "atom -> [ ]": lambda p1, p2: ast.EmptyBracketAtom(),
    "atom -> { }": lambda b1, b2: ast.EmptyBraceAtom(),
    "atom -> NAME": lambda n: ast.NameAtom(n.value),
    "atom -> NUMBER": lambda n: ast.NumberAtom(n.value),
    "atom -> STRING": lambda s: ast.StringAtom(s.value),
    "atom -> None": lambda n: ast.NoneAtom(),
    "atom -> True": lambda t: ast.BooleanAtom(True),
    "atom -> False": lambda f: ast.BooleanAtom(False),
    # -------------------------------------------------------------------------
    "test_list_comp -> test_or_star_expr comp_for": (
        lambda t, c: ast.TestListComp([t], c)
    ),
    "test_list_comp -> test_or_star_expr , test_list_comp": (
        lambda t, o, tl: ast.TestListComp([t] + tl.test_list_comp_list, tl.comp_for)
    ),
    # -------------------------------------------------------------------------
    "test_or_star_expr -> test": lambda t: t,
    "test_or_star_expr -> star_expr": lambda s: s,
    # -------------------------------------------------------------------------
    "expr_or_star_expr -> expr": lambda e: e,
    "expr_or_star_expr -> star_expr": lambda s: s,
    # -------------------------------------------------------------------------
    "exprlist -> expr_or_star_expr": lambda e: ast.ExprList([e]),
    "exprlist -> expr_or_star_expr , exprlist": (
        lambda e, o, el: ast.ExprList([e] + el.expr_or_star_expr_list)
    ),
    # -------------------------------------------------------------------------
    "test_list -> test": lambda t: ast.TestList([t]),
    "test_list -> test , test_list": (
        lambda t, o, tl: ast.TestList([t] + tl.test_list_list)
    ),
    # -------------------------------------------------------------------------
}
