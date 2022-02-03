import numlab.nl_ast as ast


def build_args(arg: ast.Arg, args: ast.Args = None) -> ast.Args:
    if args is None:
        args = ast.Args()
    if arg.is_arg:
        if args.vararg is not None:
            raise ValueError("Only one *arg is allowed")
        args.vararg = arg

    if arg.is_kwarg:
        if args.kwarg is not None:
            raise ValueError("Only one **arg is allowed")
        if args.vararg is not None:
            raise ValueError("**kwargs must be after *args")
        args.kwarg = arg

    if arg.default is not None:
        if (
            args.args
            and args.args[0].default is None
            and not args.args[0].is_arg
            and not args.args[0].is_kwarg
        ):
            raise ValueError("Default argument must be after positional argument")
    args.args.insert(0, arg)
    return args


def build_if_stmt(test, body, elif_clauses, else_clause=None):
    current_if = ast.IfStmt(test, body)
    start_if = current_if
    for elif_clause in elif_clauses:
        current_if.orelse = [elif_clause]
        current_if = elif_clause
    if else_clause is not None:
        current_if.orelse = [else_clause]
    return start_if


def build_try_stmt(body, except_clauses, else_clause=None, finally_clause=None):
    try_stmt = ast.TryStmt(body)
    for h_type, h_name, h_body in except_clauses:
        handler = ast.ExceptHandler(h_type, h_name, h_body)
        try_stmt.handlers.append(handler)
    if else_clause is not None:
        try_stmt.orelse = [else_clause]
    if finally_clause is not None:
        try_stmt.finalbody = [finally_clause]
    return try_stmt


def build_atom_expr(atom, trailer_list):
    if not trailer_list:
        return atom

    last_trailer = trailer_list.pop()
    first_trailer = last_trailer
    while trailer_list:
        current = trailer_list.pop()
        last_trailer.value = current
        last_trailer = current

    last_trailer.value = atom
    return first_trailer


def build_call_expr(func, args=None):
    call: ast.CallExpr = build_call_trailer(args)
    call.func = func


def build_call_trailer(args=None):
    if args is None:
        return ast.CallExpr(None, [], [])
    is_keyword = False
    for arg in args:
        if isinstance(arg, ast.Keyword):
            is_keyword = True
        elif is_keyword:
            raise ValueError("Positional arguments must be after keyword arguments")
    not_keywords = [arg for arg in args if not isinstance(arg, ast.Keyword)]
    keywords = [arg for arg in args if isinstance(arg, ast.Keyword)]
    return ast.CallExpr(None, not_keywords, keywords)


def build_dotted_name(names):
    last_node = names.pop()
    while names:
        current = names.pop()
        attr = ast.AttributeExpr(last_node, current.name_id)
        last_node = attr
    return last_node


def build_generators(comp_iters):
    generators = []
    for comp in comp_iters:
        if not generators and not isinstance(comp, ast.Comprehension):
            raise ValueError("First element of comp_iters must be a comprehension")
        if isinstance(comp, ast.IfExpr):
            generators[-1].ifs.append(comp)
        else:
            generators.append(comp)
    return generators


builders = {
    # -------------------------------------------------------------------------
    "program -> stmt program": lambda s, p: ast.Program([s] + p.stmts),
    "program -> NEWLINE program": lambda n, p: p,
    "program -> EPS": lambda: ast.Program([]),
    # -------------------------------------------------------------------------
    "stmt -> simple_stmt": lambda s: s,
    "stmt -> compound_stmt": lambda c: c,
    # -------------------------------------------------------------------------
    "stmt_list -> stmt": lambda s: [s],
    "stmt_list -> stmt stmt_list": lambda s, sl: [s] + sl,
    # -------------------------------------------------------------------------
    "simple_stmt -> small_stmt NEWLINE": lambda s, n: s,
    # -------------------------------------------------------------------------
    "funcdef -> def NAME ( ) : suite": (
        lambda d, n, p, p2, c, s: ast.FuncDefStmt(ast.NameExpr(n.value), ast.Args(), s)
    ),
    "funcdef -> def NAME ( parameters ) : suite": (
        lambda d, n, p, par, p2, c, s: ast.FuncDefStmt(ast.NameExpr(n.value), par, s)
    ),
    # -------------------------------------------------------------------------
    "classdef -> class NAME : suite": (
        lambda c, n, c_, s: ast.ClassDefStmt(ast.NameExpr(n.value), [], s)
    ),
    "classdef -> class NAME ( ) : suite": (
        lambda c, n, c_, s: ast.ClassDefStmt(ast.NameExpr(n.value), [], s)
    ),
    "classdef -> class NAME ( arglist ) : suite": (
        lambda c, n, p, a, c_, s: ast.ClassDefStmt(ast.NameExpr(n.value), a, s)
    ),
    # -------------------------------------------------------------------------
    "parameters -> param": lambda p: build_args(p),
    "parameters -> param , parameters": lambda p, c, ps: build_args(p, ps),
    # -------------------------------------------------------------------------
    "param -> tfpdef": lambda p: p,
    "param -> tfpdef = test": lambda p, e, t: p.set_default(t),
    "param -> * tfpdef": lambda s, p: p.set_arg(True),
    "param -> ** tfpdef": lambda ss, p: p.set_kwarg(True),
    # -------------------------------------------------------------------------
    "tfpdef -> NAME": lambda n: ast.Arg(ast.NameExpr(n.value)),
    "tfpdef -> NAME : test": lambda n, t: ast.Arg(ast.NameExpr(n.value), t),
    # -------------------------------------------------------------------------
    "varargslist -> vfpdef": lambda v: build_args(v),
    "varargslist -> vfpdef , varargslist": lambda v, c, va: build_args(v, va),
    # -------------------------------------------------------------------------
    "vararg -> vfpdef": lambda v: v,
    "vararg -> vfpdef = test": lambda v, e, t: v.set_default(t),
    "vararg -> * vfpdef": lambda s, v: v.set_arg(True),
    "vararg -> ** vfpdef": lambda ss, v: v.set_kwarg(True),
    # -------------------------------------------------------------------------
    "vfpdef -> NAME": lambda n: ast.Arg(ast.NameExpr(n.value)),
    # -------------------------------------------------------------------------
    "small_stmt -> expr_stmt": lambda e: e,
    "small_stmt -> del_stmt": lambda d: d,
    "small_stmt -> pass_stmt": lambda p: p,
    "small_stmt -> flow_stmt": lambda f: f,
    "small_stmt -> global_stmt": lambda g: g,
    "small_stmt -> nonlocal_stmt": lambda n: n,
    "small_stmt -> assert_stmt": lambda a: a,
    "small_stmt -> sim_stmt": lambda s: s,
    "small_stmt -> stat_stmt": lambda s: s,
    # "small_stmt -> import_stmt": lambda i: i,
    # -------------------------------------------------------------------------
    "sim_stmt -> begsim test": lambda b, t: ast.Begsim(t),
    "sim_stmt -> endsim": lambda e: ast.Endsim(),
    # -------------------------------------------------------------------------
    "stat_stmt -> resetstats": lambda s: ast.ResetStats(),
    # -------------------------------------------------------------------------
    "del_stmt -> del expr_list": lambda l, e: ast.DeleteStmt(e),
    # -------------------------------------------------------------------------
    "pass_stmt -> pass": lambda p: ast.PassStmt(),
    # -------------------------------------------------------------------------
    "global_stmt -> global namelist": lambda g, nl: ast.GlobalStmt(nl),
    # -------------------------------------------------------------------------
    "nonlocal_stmt -> nonlocal namelist": lambda n, nl: ast.NonlocalStmt(nl),
    # -------------------------------------------------------------------------
    "assert_stmt -> assert test_list": lambda a, t: ast.AssertStmt(t),
    # -------------------------------------------------------------------------
    "namelist -> NAME": lambda n: [ast.NameExpr(n.value)],
    "namelist -> NAME , namelist": lambda n, c, nl: [ast.NameExpr(n.value)] + nl,
    # -------------------------------------------------------------------------
    "flow_stmt -> break_stmt": lambda b: b,
    "flow_stmt -> continue_stmt": lambda c: c,
    "flow_stmt -> return_stmt": lambda r: r,
    "flow_stmt -> raise_stmt": lambda r: r,
    "flow_stmt -> yield_stmt": lambda y: y,
    # -------------------------------------------------------------------------
    "break_stmt -> break": lambda b: ast.BreakStmt(),
    # -------------------------------------------------------------------------
    "continue_stmt -> continue": lambda c: ast.ContinueStmt(),
    # -------------------------------------------------------------------------
    "return_stmt -> return": lambda r: ast.ReturnStmt(),
    "return_stmt -> return test_list": lambda r, e: ast.ReturnStmt(e),
    # -------------------------------------------------------------------------
    "yield_stmt -> yield": lambda y: ast.YieldExpr(),
    "yield_stmt -> yield expr_list": lambda y, e: ast.YieldExpr(e),
    # -------------------------------------------------------------------------
    "raise_stmt -> raise": lambda r: ast.RaiseStmt(),
    "raise_stmt -> raise test": lambda r, t: ast.RaiseStmt(t),
    "raise_stmt -> raise test from test": lambda r, t, f, t2: ast.RaiseStmt(t, t2),
    # -------------------------------------------------------------------------
    "compound_stmt -> if_stmt": lambda i: i,
    "compound_stmt -> while_stmt": lambda w: w,
    "compound_stmt -> for_stmt": lambda f: f,
    "compound_stmt -> try_stmt": lambda t: t,
    "compound_stmt -> with_stmt": lambda w: w,
    "compound_stmt -> funcdef": lambda f: f,
    "compound_stmt -> classdef": lambda c: c,
    "compound_stmt -> decorated": lambda d: d,
    "compound_stmt -> confdef": lambda c: c,
    # -------------------------------------------------------------------------
    "confdef -> conf NAME : NEWLINE INDENT confbody DEDENT": (
        lambda c, n, c_, nl, i, cb, d: ast.ConfDefStmt(n.value, cb)
    ),
    "confdef -> conf NAME ( NAME ) : NEWLINE INDENT confbody DEDENT": (
        lambda c, n, p1, b, p2, c_, nl, i, cb, d: ast.ConfDefStmt(n.value, cb, b.value)
    ),
    # -------------------------------------------------------------------------
    "confbody -> NAME test NEWLINE": lambda n, t, nl: [ast.ConfOption(n.value, t)],
    "confbody -> NAME test NEWLINE confbody": (
        lambda n, t, nl, cb: [ast.ConfOption(n.value, t)] + cb
    ),
    # -------------------------------------------------------------------------
    "if_stmt -> if test : suite elif_clause": lambda i, t, c, s, e: build_if_stmt(
        t, s, e
    ),
    "if_stmt -> if test : suite elif_clause else : suite": (
        lambda i, t, c, s, e, el, s2: build_if_stmt(t, s, e, s2)
    ),
    # -------------------------------------------------------------------------
    "elif_clause -> elif test : suite elif_clause": (lambda e, t, s, e2: [(t, s)] + e2),
    "elif_clause -> EPS": lambda: [],
    # -------------------------------------------------------------------------
    "while_stmt -> while test : suite": lambda w, t, c, s: ast.WhileStmt(t, s),
    "while_stmt -> while test : suite else : suite": (
        lambda w, t, c, s, e, c2, s2: ast.WhileStmt(t, s, s2)
    ),
    # -------------------------------------------------------------------------
    "for_stmt -> for expr_list in test_list : suite": (
        lambda f, e, i, t, c, s: ast.ForStmt(e, t, s)
    ),
    "for_stmt -> for expr_list in test_list : suite else : suite": (
        lambda f, e, i, t, c, s, e2, c2, s2: ast.ForStmt(e, t, s, s2)
    ),
    # -------------------------------------------------------------------------
    "try_stmt -> try : suite except_clause": (lambda t, c, s, e: build_try_stmt(s, e)),
    "try_stmt -> try : suite except_clause else : suite": (
        lambda t, c, s, e, el, s2: build_try_stmt(s, e, else_clause=s2)
    ),
    "try_stmt -> try : suite except_clause finally : suite": (
        lambda t, c, s, e, f, s2: build_try_stmt(s, e, finally_clause=s2)
    ),
    "try_stmt -> try : suite except_clause else : suite finally : suite": (
        lambda t, c, s, e, el, s2, f, s3: build_try_stmt(s, e, s2, s3)
    ),
    # -------------------------------------------------------------------------
    "except_clause -> except : suite maybe_except_clause": (
        lambda e, c, s, m: [(None, None, s)] + m
    ),
    "except_clause -> except test : suite maybe_except_clause": (
        lambda e, t, c, s, m: [(t, None, s)] + m
    ),
    "except_clause -> except test as NAME : suite maybe_except_clause": (
        lambda e, t, c, s, a, n, m: [(t, ast.NameExpr(n.value), s)] + m
    ),
    # -------------------------------------------------------------------------
    "maybe_except_clause -> except_clause": lambda e: [e],
    "maybe_except_clause -> EPS": lambda: [],
    # -------------------------------------------------------------------------
    "with_stmt -> with with_items : suite": lambda w, i, c, s: ast.WithStmt(i, s),
    # -------------------------------------------------------------------------
    "with_items -> with_item": lambda i: [i],
    "with_items -> with_item , with_items": lambda i, c, i2: [i] + i2,
    # -------------------------------------------------------------------------
    "with_item -> test": lambda t: ast.WithItem(t),
    "with_item -> test as expr": lambda t, a, e: ast.WithItem(t, e),
    # -------------------------------------------------------------------------
    "suite -> simple_stmt": lambda s: [s],
    "suite -> NEWLINE INDENT stmt_list DEDENT": lambda n, i, l, d: l,
    # -------------------------------------------------------------------------
    "decorated -> decorators funcdef": lambda d, f: f.add_decorators(d),
    "decorated -> decorators classdef": lambda d, c: c.add_decorators(d),
    # -------------------------------------------------------------------------
    "decorators -> decorator decorators": lambda d, d2: [d] + d2,
    "decorators -> decorator": lambda d: [d],
    # -------------------------------------------------------------------------
    "decorator -> @ dotted_name NEWLINE": lambda d, n, nl: build_dotted_name(n),
    "decorator -> @ dotted_name ( ) NEWLINE": (
        lambda d, n, p, nl: build_call_expr(build_dotted_name(n), [])
    ),
    "decorator -> @ dotted_name ( arglist ) NEWLINE": (
        lambda d, n, p, a, nl: build_call_expr(build_dotted_name(n), a)
    ),
    # -------------------------------------------------------------------------
    "dotted_name -> NAME": lambda n: [ast.NameExpr(n.value)],
    "dotted_name -> NAME . dotted_name": lambda n, c, n2: [ast.NameExpr(n.value)] + n2,
    # -------------------------------------------------------------------------
    "arglist -> argument": lambda a: [a],
    "arglist -> argument , arglist": lambda a, c, a2: [a] + a2,
    # -------------------------------------------------------------------------
    "argument -> test": lambda t: t,
    "argument -> test comp_for": lambda t, c: ast.GeneratorExpr(t, build_generators(c)),
    "argument -> test = test": lambda t, e, t2: ast.Keyword(t, t2),
    "argument -> * test": lambda a, t: ast.StarredExpr(t),
    "argument -> ** test": lambda a, t: ast.Keyword(None, t),
    # -------------------------------------------------------------------------
    "comp_for -> for expr_list in or_test comp_iter": (
        lambda f, e, i, o, c: [ast.Comprehension(e, o)] + c
    ),
    # -------------------------------------------------------------------------
    "comp_if -> if test_nocond": lambda i, t: [ast.IfExpr(t, None)],
    "comp_if -> if test_nocond comp_iter": lambda i, t, c: [ast.IfExpr(t, None)] + c,
    # -------------------------------------------------------------------------
    "comp_iter -> comp_for": lambda c: c,
    "comp_iter -> comp_if": lambda c: c,
    "comp_iter -> EPS": lambda: [],
    # -------------------------------------------------------------------------
    "expr_stmt -> test_list annassign": lambda t, a: a.set_target(t),
    "expr_stmt -> test_list augassign yield_or_testlist": (
        lambda t, a, y: ast.AugAssignStmt(t, a, y)
    ),
    "expr_stmt -> test_list assign": (
        lambda t, a: ast.AssignStmt([t] + a.targets, a.value)
        if isinstance(a, ast.AssignStmt)
        else (ast.AssignStmt([t], a) if isinstance(a, ast.TupleExpr) else t)
    ),
    # -------------------------------------------------------------------------
    "test_list -> test": lambda t: [t],
    "test_list -> test , test_list": lambda t, c, t2: [t] + t2,
    # -------------------------------------------------------------------------
    "yield_or_testlist -> yield_expr": lambda y: y,
    "yield_or_testlist -> test_list": lambda t: t,
    # -------------------------------------------------------------------------
    "yield_expr -> yield": lambda y: ast.YieldExpr(),
    "yield_expr -> yield yield_arg": (
        lambda y, a: ast.YieldExpr(a)
        if isinstance(a, ast.YieldFromExpr)
        else ast.YieldExpr(a)
    ),
    # -------------------------------------------------------------------------
    "yield_arg -> from test": lambda f, t: ast.YieldFromExpr(t),
    "yield_arg -> test_list": lambda t: t,
    # -------------------------------------------------------------------------
    "assign -> = yield_expr assign": (
        lambda e, t, a: ast.AssignStmt([t] + a.targets, a.value)
        if isinstance(a, ast.AssignStmt)
        else (ast.AssignStmt([t], a) if isinstance(a, ast.TupleExpr) else t)
    ),
    "assign -> = test_list assign": (
        lambda e, t, a: ast.AssignStmt([t] + a.targets, a.value)
        if isinstance(a, ast.AssignStmt)
        else (ast.AssignStmt([t], a) if isinstance(a, ast.TupleExpr) else t)
    ),
    "assign -> EPS": lambda: None,
    # -------------------------------------------------------------------------
    "annassign -> : test = test": lambda c, a, e, t: ast.AnnAssignStmt(None, a, t),
    # -------------------------------------------------------------------------
    "augassign -> +=": lambda a: ast.Operator.ADD,
    "augassign -> -=": lambda a: ast.Operator.SUB,
    "augassign -> *=": lambda a: ast.Operator.MUL,
    "augassign -> @=": lambda a: ast.Operator.MATMUL,
    "augassign -> /=": lambda a: ast.Operator.DIV,
    "augassign -> %=": lambda a: ast.Operator.MOD,
    "augassign -> &=": lambda a: ast.Operator.BIT_AND,
    "augassign -> |=": lambda a: ast.Operator.BIT_OR,
    "augassign -> ^=": lambda a: ast.Operator.BIT_XOR,
    "augassign -> <<=": lambda a: ast.Operator.LSHIFT,
    "augassign -> >>=": lambda a: ast.Operator.RSHIFT,
    "augassign -> **=": lambda a: ast.Operator.POW,
    "augassign -> //=": lambda a: ast.Operator.FLOORDIV,
    # -------------------------------------------------------------------------
    "test -> or_test": lambda o: o,
    "test -> or_test if or_test else test": (
        lambda o, i, o2, e, t: ast.IfExpr(o, o2, t)
    ),
    "test -> lambdef": lambda l: l,
    # -------------------------------------------------------------------------
    "test_nocond -> or_test": lambda o: o,
    "test_nocond -> lambdef_nocond": lambda l: l,
    # -------------------------------------------------------------------------
    "lambdef -> lambda : test": lambda l, c, t: ast.FuncDefStmt(None, ast.Args(), [t]),
    "lambdef -> lambda varargslist : test": (
        lambda l, v, c, t: ast.FuncDefStmt(None, v, [t])
    ),
    # -------------------------------------------------------------------------
    "lambdef_nocond -> lambda : test_nocond": (
        lambda l, c, t: ast.FuncDefStmt(None, [], [t]),
    ),
    "lambdef_nocond -> lambda varargslist : test_nocond": (
        lambda l, v, c, t: ast.FuncDefStmt(None, v, [t])
    ),
    # -------------------------------------------------------------------------
    "or_test -> and_test": lambda a: a,
    "or_test -> and_test or or_test": (
        lambda a, o, o2: ast.BinOpExpr(a, ast.Operator.OR, o2)
    ),
    # -------------------------------------------------------------------------
    "and_test -> not_test": lambda n: n,
    "and_test -> not_test and and_test": (
        lambda n, a, a2: ast.BinOpExpr(n, ast.Operator.AND, a2)
    ),
    # -------------------------------------------------------------------------
    "not_test -> not not_test": lambda n, t: ast.UnaryOpExpr(ast.UnaryOp.NOT, t),
    "not_test -> comparison": lambda c: c,
    # -------------------------------------------------------------------------
    "comparison -> expr": lambda e: e,
    "comparison -> expr comp_op comparison": (lambda l, o, r: ast.BinOpExpr(l, o, r)),
    # -------------------------------------------------------------------------
    "comp_op -> <": lambda c: ast.CmpOp.LT,
    "comp_op -> >": lambda c: ast.CmpOp.GT,
    "comp_op -> ==": lambda c: ast.CmpOp.EQ,
    "comp_op -> >=": lambda c: ast.CmpOp.GTE,
    "comp_op -> <=": lambda c: ast.CmpOp.LTE,
    "comp_op -> !=": lambda c: ast.CmpOp.NOT_EQ,
    "comp_op -> in": lambda c: ast.CmpOp.IN,
    "comp_op -> not in": lambda c, c2: ast.CmpOp.NOT_IN,
    "comp_op -> is": lambda c: ast.CmpOp.IS,
    "comp_op -> is not": lambda c, c2: ast.CmpOp.IS_NOT,
    # -------------------------------------------------------------------------
    "expr -> xor_expr": lambda x: x,
    "expr -> xor_expr | expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.BIT_OR, r)
    ),
    # -------------------------------------------------------------------------
    "xor_expr -> and_expr": lambda a: a,
    "xor_expr -> and_expr ^ xor_expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.BIT_XOR, r)
    ),
    # -------------------------------------------------------------------------
    "and_expr -> shift_expr": lambda s: s,
    "and_expr -> shift_expr & and_expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.BIT_AND, r)
    ),
    # -------------------------------------------------------------------------
    "shift_expr -> arith_expr": lambda a: a,
    "shift_expr -> arith_expr << shift_expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.LSHIFT, r)
    ),
    "shift_expr -> arith_expr >> shift_expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.RSHIFT, r)
    ),
    # -------------------------------------------------------------------------
    "arith_expr -> term": lambda t: t,
    "arith_expr -> term + arith_expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.ADD, r)
    ),
    "arith_expr -> term - arith_expr": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.SUB, r)
    ),
    # -------------------------------------------------------------------------
    "term -> factor": lambda f: f,
    "term -> factor * term": lambda l, o, r: ast.BinOpExpr(l, ast.Operator.MUL, r),
    "term -> factor @ term": lambda l, o, r: ast.BinOpExpr(l, ast.Operator.MATMUL, r),
    "term -> factor / term": lambda l, o, r: ast.BinOpExpr(l, ast.Operator.DIV, r),
    "term -> factor % term": lambda l, o, r: ast.BinOpExpr(l, ast.Operator.MOD, r),
    "term -> factor // term": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.FLOORDIV, r)
    ),
    # -------------------------------------------------------------------------
    "factor -> + factor": lambda o, f: ast.UnaryOpExpr(ast.UnaryOp.UADD, f),
    "factor -> - factor": lambda o, f: ast.UnaryOpExpr(ast.UnaryOp.USUB, f),
    "factor -> ~ factor": lambda o, f: ast.UnaryOpExpr(ast.UnaryOp.INVERT, f),
    "factor -> power": lambda p: p,
    # -------------------------------------------------------------------------
    "power -> atom_expr": lambda a: a,
    "power -> atom_expr ** factor": (
        lambda l, o, r: ast.BinOpExpr(l, ast.Operator.POW, r)
    ),
    # -------------------------------------------------------------------------
    "atom_expr -> atom trailer_expr": lambda a, t: build_atom_expr(a, t),
    # -------------------------------------------------------------------------
    "trailer_expr -> trailer trailer_expr": lambda t, t2: [t] + t2,
    "trailer_expr -> EPS": lambda: [],
    # -------------------------------------------------------------------------
    "trailer -> ( )": lambda p, p2: build_call_trailer(),
    "trailer -> ( arglist )": lambda p, a, p2: build_call_trailer(a),
    "trailer -> [ subscriptlist ]": lambda b, s, b2: (
        ast.SubscriptExpr(None, s.elts[0])
        if isinstance(s, ast.TupleExpr) and len(s.elts) == 1
        else ast.SubscriptExpr(None, s)
    ),
    "trailer -> . NAME": lambda d, n: ast.AttributeExpr(None, n.value),
    # -------------------------------------------------------------------------
    "subscriptlist -> subscript": lambda s: ast.TupleExpr([s]),
    "subscriptlist -> subscript , subscriptlist": (
        lambda s, o, s2: ast.TupleExpr([s] + s2.elts)
    ),
    # -------------------------------------------------------------------------
    "subscript -> test": lambda t: t,
    "subscript -> maybe_test : maybe_test sliceop": (
        lambda l, c, u, s: ast.SliceExpr(l, u, s)
    ),
    # -------------------------------------------------------------------------
    "sliceop -> : maybe_test": lambda o, t: t,
    "sliceop -> EPS": lambda: ast.ConstantExpr(1),
    # -------------------------------------------------------------------------
    "maybe_test -> test": lambda t: t,
    "maybe_test -> EPS": lambda: None,
    # -------------------------------------------------------------------------
    "atom -> ( test_list_comp )": (
        lambda b1, t, b2: ast.GeneratorExpr(t[0], build_generators(t[1]))
        if isinstance(t, tuple)
        else (
            t.elts[0]
            if len(t.elts) == 1
            else t
        )
    ),
    "atom -> [ test_list_comp ]": (
        lambda b1, t, b2: ast.ListCompExpr(t[0], build_generators(t[1]))
        if isinstance(t, tuple)
        else ast.ListExpr(t.elts)
    ),
    "atom -> ( )": lambda p1, p2: ast.TupleExpr(),
    "atom -> [ ]": lambda p1, p2: ast.ListExpr(),
    "atom -> { }": lambda b1, b2: ast.DictExpr(),
    "atom -> NAME": lambda n: ast.NameExpr(n.value),
    "atom -> NUMBER": lambda n: ast.ConstantExpr(
        int(n.value) if n.value.isnumeric() else float(n.value)
    ),
    "atom -> STRING": lambda s: ast.ConstantExpr(s.value),
    "atom -> None": lambda n: ast.ConstantExpr(None),
    "atom -> True": lambda t: ast.ConstantExpr(True),
    "atom -> False": lambda f: ast.ConstantExpr(False),
    # -------------------------------------------------------------------------
    "test_list_comp -> test comp_for": lambda t, c: (t, c),
    "test_list_comp -> test_list": lambda t: t,
    # -------------------------------------------------------------------------
    "expr_list -> expr": lambda e: e,
    "expr_list -> expr , expr_list": lambda e, o, el: (
        ast.TupleExpr([e] + el.elts)
        if isinstance(el, ast.TupleExpr)
        else ast.TupleExpr([e, el])
    ),
    # -------------------------------------------------------------------------
    "test_list -> test": lambda t: ast.TupleExpr([t]),
    "test_list -> test , test_list": lambda t, o, tl: ast.TupleExpr([t] + tl.elts),
    # -------------------------------------------------------------------------
}
