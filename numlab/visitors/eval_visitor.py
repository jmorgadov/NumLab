from __future__ import annotations

from time import sleep, time
from typing import Any, List, Tuple

import numlab.nl_ast as ast
from numlab import builtin
from numlab.lang.context import Context
from numlab.lang.type import Instance, Type
from numlab.lang.visitor import Visitor
import numlab.exceptions as excpt

# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring

OPERATOR_FUNC = {
    ast.Operator.ADD: "__add__",
    ast.Operator.SUB: "__sub__",
    ast.Operator.MUL: "__mul__",
    ast.Operator.DIV: "__truediv__",
    ast.Operator.POW: "__pow__",
    ast.Operator.MOD: "__mod__",
    ast.Operator.POW: "__pow__",
    ast.Operator.LSHIFT: "__lshift__",
    ast.Operator.RSHIFT: "__rshift__",
    ast.Operator.BIT_XOR: "__xor__",
    ast.Operator.BIT_AND: "__and__",
    ast.Operator.BIT_OR: "__or__",
    ast.Operator.FLOORDIV: "__floordiv__",
    ast.Operator.MATMUL: "__matmul__",
    ast.CmpOp.IN: "__contains__",
    ast.CmpOp.EQ: "__eq__",
    ast.CmpOp.NOT_EQ: "__ne__",
    ast.CmpOp.LT: "__lt__",
    ast.CmpOp.GT: "__gt__",
    ast.CmpOp.LTE: "__le__",
    ast.CmpOp.GTE: "__ge__",
}

OPER_STAT_NAME = {
    ast.Operator.ADD: "add_count",
    ast.Operator.SUB: "sub_count",
    ast.Operator.MUL: "mul_count",
    ast.Operator.DIV: "truediv_count",
    ast.Operator.POW: "pow_count",
    ast.Operator.MOD: "mod_count",
    ast.Operator.POW: "pow_count",
    ast.Operator.LSHIFT: "lshift_count",
    ast.Operator.RSHIFT: "rshift_count",
    ast.Operator.BIT_XOR: "bit_xor_count",
    ast.Operator.BIT_AND: "bit_and_count",
    ast.Operator.BIT_OR: "bit_or_count",
    ast.Operator.FLOORDIV: "floordiv_count",
    ast.Operator.MATMUL: "matmul_count",
    ast.Operator.OR: "or_count",
    ast.Operator.AND: "and_count",
    ast.CmpOp.IN: "contains_count",
    ast.CmpOp.EQ: "eq_count",
    ast.CmpOp.NOT_EQ: "ne_count",
    ast.CmpOp.LT: "lt_count",
    ast.CmpOp.GT: "gt_count",
    ast.CmpOp.LTE: "le_count",
    ast.CmpOp.GTE: "ge_count",
}


CONFIG_OPTS_VALIDATOR = {
    "max_time": (builtin.nl_float,),
    "max_var_count": (builtin.nl_int,),
    "max_call_count": (builtin.nl_int,),
    "max_add_count": (builtin.nl_int,),
    "max_sub_count": (builtin.nl_int,),
    "max_mul_count": (builtin.nl_int,),
    "max_truediv_count": (builtin.nl_int,),
    "max_pow_count": (builtin.nl_int,),
    "max_mod_count": (builtin.nl_int,),
    "max_lshift_count": (builtin.nl_int,),
    "max_rshift_count": (builtin.nl_int,),
    "max_bit_xor_count": (builtin.nl_int,),
    "max_bit_and_count": (builtin.nl_int,),
    "max_bit_or_count": (builtin.nl_int,),
    "max_floordiv_count": (builtin.nl_int,),
    "max_matmul_count": (builtin.nl_int,),
    "max_contains_count": (builtin.nl_int,),
    "max_eq_count": (builtin.nl_int,),
    "max_ne_count": (builtin.nl_int,),
    "max_lt_count": (builtin.nl_int,),
    "max_gt_count": (builtin.nl_int,),
    "max_le_count": (builtin.nl_int,),
    "max_ge_count": (builtin.nl_int,),
    "call_time": (builtin.nl_float, builtin.nl_function),
    "assign_time": (builtin.nl_float, builtin.nl_function),
    "add_time": (builtin.nl_float, builtin.nl_function),
    "sub_time": (builtin.nl_float, builtin.nl_function),
    "mul_time": (builtin.nl_float, builtin.nl_function),
    "truediv_time": (builtin.nl_float, builtin.nl_function),
    "pow_time": (builtin.nl_float, builtin.nl_function),
    "mod_time": (builtin.nl_float, builtin.nl_function),
    "lshift_time": (builtin.nl_float, builtin.nl_function),
    "rshift_time": (builtin.nl_float, builtin.nl_function),
    "bit_xor_time": (builtin.nl_float, builtin.nl_function),
    "bit_and_time": (builtin.nl_float, builtin.nl_function),
    "bit_or_time": (builtin.nl_float, builtin.nl_function),
    "floordiv_time": (builtin.nl_float, builtin.nl_function),
    "matmul_time": (builtin.nl_float, builtin.nl_function),
    "contains_time": (builtin.nl_float, builtin.nl_function),
    "eq_time": (builtin.nl_float, builtin.nl_function),
    "ne_time": (builtin.nl_float, builtin.nl_function),
    "lt_time": (builtin.nl_float, builtin.nl_function),
    "gt_time": (builtin.nl_float, builtin.nl_function),
    "le_time": (builtin.nl_float, builtin.nl_function),
    "ge_time": (builtin.nl_float, builtin.nl_function),
}


def _truth(inst: Instance) -> bool:
    if "__bool__" in inst._dict:
        return inst.get("__bool__")(inst).get("value")
    if "__len__" in inst._dict:
        return inst.get("__len__")(inst).get("value") > 0
    return builtin.nl_bool(True).get("value")


def ioper(oper: str) -> str:
    return f"__i{oper[2:-2]}__"


def roper(oper: str) -> str:
    return f"__r{oper[2:-2]}__"


def convert_to_nl_obj(obj: Any):
    if isinstance(obj, Instance):
        return obj
    if isinstance(obj, bool):
        return builtin.nl_bool(obj)
    if isinstance(obj, int):
        return builtin.nl_int(obj)
    if isinstance(obj, float):
        return builtin.nl_float(obj)
    if isinstance(obj, str):
        return builtin.nl_str(obj)
    if isinstance(obj, list):
        items = [convert_to_nl_obj(item) for item in obj]
        return builtin.nl_list(items)
    if isinstance(obj, tuple):
        items = [convert_to_nl_obj(item) for item in obj]
        return builtin.nl_tuple(items)
    raise TypeError(f"Unsupported type: {type(obj)}")


class EvalVisitor:

    visitor_obj = Visitor()
    visitor = visitor_obj.visitor
    callback = visitor_obj.callback

    def __init__(self, context: Context):
        self.context = context
        self.flags = {
            "inside_loop": 0,
            "break": False,
            "continue": False,
            "return_val": [],
            "class": [],
            "current_config": None,
            "start_time": 0,
        }
        self.stats = {}
        self.reset_stats()
        self.configs = {}
        self.in_sim = []

    @callback
    def check_time_callback(self, node: ast.AST):
        if not self.in_sim:
            return
        config = self.in_sim[-1]
        if not "max_time" in config:
            return
        start = self.flags["start_time"]
        now = time()
        if now - start > config["max_time"].get("value"):
            raise TimeoutError(f"Time limit exceeded: {config['max_time']}s")

    @callback
    def main_callbalck(self, node: ast.AST):
        self.set_stat("time", time() - self.flags["start_time"])

    @callback
    def time_config_callback(self, node: ast.AST):
        if not self.in_sim:
            return
        config = self.in_sim[-1]
        if isinstance(node, ast.CallExpr) and "call_time" in config:
            val = self.get_config_val("call_time", config).get("value")
            sleep(val)
            return
        if (
            isinstance(node, (ast.AnnAssignStmt, ast.AugAssignStmt, ast.AssignStmt))
            and "assign_time" in config
        ):
            val = self.get_config_val("assign_time", config).get("value")
            sleep(val)
            return
        if isinstance(node, ast.Stmt) and "stmt_time" in config:
            val = self.get_config_val("stmt_time", config).get("value")
            sleep(val)
            return
        if isinstance(node, ast.BinOpExpr):
            conf_name = OPER_STAT_NAME[node.op][:-5] + "time"
            if conf_name in config:
                val = self.get_config_val(conf_name, config).get("value")
                sleep(val)
                return

    @callback
    def check_max_callbalck(self, node: ast.AST):
        if not self.in_sim:
            return
        config = self.in_sim[-1]
        if (
            "max_var_count" in config
            and self.context.count_vars() > config["max_var_count"].get("value")
        ):
            raise TimeoutError(f"Variable limit exceeded: {config['max_var_count']}")
        max_configs = [k for k in config if k.startswith("max_")]
        for max_config in max_configs:
            if not max_config in config:
                continue
            stat_name = max_config[4:]
            if self.stats[stat_name] > config[max_config].get("value"):
                raise Exception(f"{stat_name} limit exceeded: {config[max_config]}")

    def get_config_val(self, name, config) -> Instance:
        if not name in config:
            return None
        obj = config[name]
        base_type = CONFIG_OPTS_VALIDATOR[name][0]
        if obj.type.subtype(builtin.nl_function):
            val = obj.get("__call__")(obj)
            if not val.type.subtype(base_type):
                raise TypeError(
                    f"{name} must be {base_type.type_name}. Function is "
                    f"returning type {val.type.type_name}"
                )
            return val
        return obj

    def reset_stats(self):
        self.define("stats", builtin.nl_dict({}))
        self.set_stats(
            [
                ("time", 0),
                ("assign_count", 0),
                ("var_count", 0),
                ("call_count", 0),
                ("add_count", 0),
                ("sub_count", 0),
                ("mul_count", 0),
                ("truediv_count", 0),
                ("pow_count", 0),
                ("mod_count", 0),
                ("floordiv_count", 0),
                ("lshift_count", 0),
                ("rshift_count", 0),
                ("matmul_count", 0),
                ("bit_xor_count", 0),
                ("bit_and_count", 0),
                ("bit_or_count", 0),
                ("contains_count", 0),
                ("eq_count", 0),
                ("ne_count", 0),
                ("lt_count", 0),
                ("gt_count", 0),
                ("le_count", 0),
                ("ge_count", 0),
                ("and_count", 0),
                ("or_count", 0),
            ]
        )

    def set_stats(self, items: List[Tuple[str, Any]]):
        stats = self.resolve("stats")
        for name, value in items:
            self.stats[name] = value
            stats.get("__setitem__")(
                stats, convert_to_nl_obj(name), convert_to_nl_obj(value)
            )

    def set_stat(self, name, value):
        self.stats[name] = value
        stats = self.resolve("stats")
        stats.get("__setitem__")(
            stats, convert_to_nl_obj(name), convert_to_nl_obj(value)
        )

    def resolve(self, obj_name):
        val = self.context.resolve(obj_name)
        if val is None:
            val = builtin.resolve(obj_name)
        if val is None:
            raise excpt.RuntimeError(f"{obj_name} is not defined")
        return val

    def define(self, name, value):
        if self.flags["class"]:
            class_obj = self.flags["class"][-1]
            class_obj.add_attribute(name, value)
        else:
            self.context.define(name, value)
        self.set_stat("var_count", self.context.count_vars())

    @visitor
    def eval(self, node: ast.Program):
        start = time()
        self.flags["start_time"] = start
        for stmt in node.stmts:
            self.eval(stmt)
        end = time()
        self.set_stat("time", end - start)

    @visitor
    def eval(self, node: ast.FuncDefStmt):
        for arg in node.args.args:
            if arg.default is not None:
                arg.default = self.eval(arg.default)

        def func(*args, **kwargs):
            self.context = self.context.make_child()
            for arg, value in zip(node.args.args, args):
                self.define(arg.arg.name_id, value)
            for arg, value in kwargs.items():
                self.define(arg, value)
            last_stmt = None
            for stmt in node.body:
                last_stmt = self.eval(stmt)
                if self.flags["return_val"]:
                    break
            self.context = self.context.parent
            val = (
                self.flags["return_val"].pop()
                if self.flags["return_val"]
                else Type.get("none")
            )
            return last_stmt if node.name is None else val

        func_obj = builtin.nl_function(func)
        func_obj.set("args", node.args)
        if node.name is not None:
            self.define(node.name.name_id, func_obj)
        return func_obj

    @visitor
    def eval(self, node: ast.ClassDefStmt):
        bases = [self.eval(base) for base in node.bases]
        if len(bases) > 1:
            raise NotImplementedError("Multiple inheritance not supported")
        if not bases:
            bases = [builtin.nl_object]
        new_type = Type(node.name, bases[0])
        self.define(node.name.name_id, new_type)
        self.flags["class"].append(new_type)

        def new(cls, *args, **kwargs):
            inst = Instance(cls)
            init = inst.get("__init__")
            if isinstance(init, Instance):
                init.get("__call__")(init, inst, *args, **kwargs)
            else:
                init(inst, *args, **kwargs)
            return inst

        new_type.add_attribute("__new__", new)
        self.context = self.context.make_child()
        for stmt in node.body:
            self.eval(stmt)
        if node.decorators:
            raise NotImplementedError("Decorators not supported")
        self.flags["class"].pop()
        self.context = self.context.parent

    @visitor
    def eval(self, node: ast.ConfDefStmt):
        base_config = {}
        if node.base is not None:
            base_config = self.configs.get(node.base, None)
            if base_config is None:
                raise excpt.RuntimeError(f"Config {node.base} is not defined")
        self.flags["current_config"] = node.name
        self.configs[node.name] = base_config.copy()
        for conf_opt in node.configs:
            self.eval(conf_opt)

    @visitor
    def eval(self, node: ast.ConfOption):
        if node.name not in CONFIG_OPTS_VALIDATOR:
            raise excpt.InvalidConfigError(f"Unknown config option: {node.name}")
        val = self.eval(node.value)
        if not val.type.subtype(CONFIG_OPTS_VALIDATOR[node.name]):
            raise excpt.InvalidTypeError(
                f"Invalid value for config option: {node.name}. "
                "Expected: "
                + repr([ct.type_name for ct in CONFIG_OPTS_VALIDATOR[node.name]])
            )
        self.configs[self.flags["current_config"]][node.name] = val

    @visitor
    def eval(self, node: ast.ReturnStmt):
        if self.context.parent is None:
            raise RuntimeError("Cannot return from top-level code")
        val = node.expr.elts
        if len(val) == 1:
            val = val[0]
        self.flags["return_val"].append(self.eval(val))

    @visitor
    def eval(self, node: ast.DeleteStmt):
        for target in node.targets:
            target.ctx = ast.ExprCtx.DEL
            self.eval(target)

    def _assign(self, target, value):
        self.set_stat("assign_count", self.stats["assign_count"] + 1)
        if isinstance(target, ast.NameExpr):
            self.define(target.name_id, value)
        elif isinstance(target, ast.AttributeExpr):
            attr_val = self.eval(target.value)
            attr_val.set(target.attr, value)
        elif isinstance(target, ast.SubscriptExpr):
            subs_value = self.eval(target.value)
            slc = self.eval(target.slice)
            subs_value.get("__setitem__")(subs_value, slc)
        else:
            raise NotImplementedError()

    @visitor
    def eval(self, node: ast.AssignStmt):
        targets: List[ast.TupleExpr] = node.targets
        values = [self.eval(item) for item in node.value.elts]
        for i, val in enumerate(values):
            if isinstance(val, ast.NameExpr):
                values[i] = self.resolve(val.name_id)
            values[i] = values[i].get_value()
        for target_tuple in targets:
            if len(target_tuple.elts) != len(values):
                raise excpt.RuntimeError("Too many values to unpack")
            for target, value in zip(target_tuple.elts, values):
                self._assign(target, value)

    @visitor
    def eval(self, node: ast.AugAssignStmt):
        target = self.eval(node.target.elts[0])
        value = self.eval(node.value.elts[0])
        self.set_stat("assign_count", self.stats["assign_count"] + 1)
        self.set_stat(OPER_STAT_NAME[node.op], self.stats[OPER_STAT_NAME[node.op]] + 1)
        oper = ioper(OPERATOR_FUNC[node.op])
        target.get(oper)(target, value)

    @visitor
    def eval(self, node: ast.AnnAssignStmt):
        target = self.eval(node.target)
        value = self.eval(node.value)
        self._assign(target, value)

    @visitor
    def eval(self, node: ast.ForStmt):
        self.flags["inside_loop"] += 1
        obj = self.eval(node.iter_expr.elts[0])
        if not isinstance(node.target, ast.NameExpr):
            raise excpt.RuntimeError("For loop target must be a NameExpr")
        for item in obj:  # pylint: disable=not-an-iterable
            target_name = node.target.name_id
            self.define(target_name, item)
            for stmt in node.body:
                self.eval(stmt)
                if self.flags["break"] or self.flags["return_val"]:
                    break
                if self.flags["continue"]:
                    self.flags["continue"] = False
                    break
            if self.flags["break"] or self.flags["return_val"]:
                break
        if self.flags["break"]:
            self.flags["break"] = False
        elif not self.flags["return_val"]:
            for stmt in node.orelse:
                self.eval(stmt)
        self.flags["inside_loop"] -= 1

    @visitor
    def eval(self, node: ast.WhileStmt):
        self.flags["inside_loop"] += 1
        while _truth(self.eval(node.test)):
            for stmt in node.body:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    self.flags["continue"] = False
                    break
            if self.flags["break"]:
                break
        if self.flags["break"]:
            self.flags["break"] = False
        else:
            for stmt in node.orelse:
                self.eval(stmt)
        self.flags["inside_loop"] -= 1

    @visitor
    def eval(self, node: ast.IfStmt):
        if _truth(self.eval(node.test)):
            for stmt in node.body:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    break
                if self.flags["return_val"]:
                    break
        else:
            for stmt in node.orelse:
                self.eval(stmt)
                if self.flags["break"]:
                    break
                if self.flags["continue"]:
                    break
                if self.flags["return_val"]:
                    break

    @visitor
    def eval(self, node: ast.Begsim):
        val = node.config
        if not isinstance(val, ast.NameExpr):
            raise excpt.InvalidTypeError("Invalid value for begsim config option")
        conf_name = val.name_id
        if not conf_name in self.configs:
            raise excpt.RuntimeError(f"Unknown config: {conf_name}")
        self.in_sim.append(self.configs[val.name_id])

    @visitor
    def eval(self, node: ast.Endsim):
        if not self.in_sim:
            raise excpt.RuntimeError("Endsim without begsim")
        self.in_sim.pop()

    @visitor
    def eval(self, node: ast.ResetStats):
        self.reset_stats()

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
        return node

    @visitor
    def eval(self, node: ast.BreakStmt):
        self.flags["break"] = True

    @visitor
    def eval(self, node: ast.ContinueStmt):
        self.flags["continue"] = True

    @visitor
    def eval(self, node: ast.ExprStmt):
        return self.eval(node.expr)

    @visitor
    def eval(self, node: ast.BinOpExpr):
        left: Instance = self.eval(node.left)
        op = node.op
        if op == ast.Operator.AND:
            self.set_stat("and_count", self.stats["and_count"] + 1)
            if _truth(left):
                return self.eval(node.right)
            return left
        if op == ast.Operator.OR:
            self.set_stat("or_count", self.stats["or_count"] + 1)
            if _truth(left):
                return left
            return self.eval(node.right)

        right: Instance = self.eval(node.right)

        self.set_stat(OPER_STAT_NAME[op], self.stats[OPER_STAT_NAME[op]] + 1)
        neg = False
        if op == ast.CmpOp.IS:
            return builtin.nl_bool(left.type.subtype(right.type))
        if op == ast.CmpOp.IS_NOT:
            return builtin.nl_bool(not left.type.subtype(right.type))

        if op == ast.CmpOp.NOT_IN:
            neg = True
            op = ast.CmpOp.IN

        if op == ast.CmpOp.IN:
            val = right.get("__contains__")(right, left)
            if neg:
                return builtin.nl_bool(not val.get("value"))
            return val

        oper = OPERATOR_FUNC[op]
        val = left.get(oper)(left, right)
        if neg:
            val = builtin.nl_bool(not _truth(val))
        return val

    @visitor
    def eval(self, node: ast.UnaryOpExpr):
        op = node.op
        val: Instance = self.eval(node.operand)
        if op == ast.UnaryOp.NOT:
            return builtin.nl_bool(not _truth(val))
        if op == ast.UnaryOp.INVERT:
            return val.get("__invert__")(val)
        if op == ast.UnaryOp.UADD:
            return val
        if op == ast.UnaryOp.USUB:
            return val.get("__sub__")(builtin.nl_int(0), val)
        raise excpt.RuntimeError("Unsupported unary operator")

    @visitor
    def eval(self, node: ast.LambdaExpr):
        for dec in node.decorator[::-1]:
            dec_val = self.eval(dec)

    @visitor
    def eval(self, node: ast.IfExpr):
        if _truth(self.eval(node.test)):
            return self.eval(node.body)
        if node.orelse is not None:
            return self.eval(node.orelse)

    @visitor
    def eval(self, node: ast.DictExpr):
        dic = {self.eval(k): self.eval(v) for k, v in zip(node.keys, node.values)}
        return builtin.nl_dict(dic)

    @visitor
    def eval(self, node: ast.SetExpr):
        values = {self.eval(v) for v in node.values}
        return builtin.nl_set(values)

    def _generate(self, compr: List[ast.Comprehension]):
        current = compr[0]
        obj = self.eval(current.comp_iter)
        iterator = obj.get("__iter__")(obj)
        while True:
            try:
                item = iterator.get("__next__")(iterator)
                if isinstance(current.target, ast.NameExpr):
                    self.define(current.target.name_id, item)
                else:
                    raise NotImplementedError("Tuple target not supported")
                valid = True
                for if_expr in current.ifs:
                    if not _truth(self.eval(if_expr.test)):
                        valid = False
                        break
                if not valid:
                    continue
            except StopIteration:
                break
            if len(compr) == 1:
                if not isinstance(current.target, ast.NameExpr):
                    raise excpt.RuntimeError("Invalid target")
                yield self.resolve(current.target.name_id)
            else:
                yield from self._generate(compr[1:])

    @visitor
    def eval(self, node: ast.ListCompExpr):
        items = []
        if not isinstance(node.elt, ast.NameExpr):
            raise excpt.RuntimeError("Invalid target")
        self.context = self.context.make_child()
        for _ in self._generate(node.generators):
            item = self.resolve(node.elt.name_id)
            items.append(item)
        self.context = self.context.parent
        return builtin.nl_list(items)

    @visitor
    def eval(self, node: ast.SetCompExpr):
        items = set()
        if not isinstance(node.target, ast.NameExpr):
            raise excpt.RuntimeError("Invalid target")
        for _ in self._generate(node.generators):
            item = self.resolve(node.target.name_id)
            items.add(item)
        return builtin.nl_list(items)

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

    def _call_func(self, func, args, kwargs):
        func_args = func.get("args").args

        # Setting arg values
        call_args = {}
        varargs = None
        for arg in func_args:
            call_args[arg.arg] = arg.default
            if arg.is_arg:
                call_args[arg.arg] = []
                varargs = arg.arg
                break
        count = len(call_args)
        names = list(call_args.keys())

        i = 0
        for arg in args:
            if i >= count:
                raise excpt.RuntimeError("Too many positional arguments")
            if func_args[i].is_arg:
                call_args[names[i]].append(arg)
                continue
            call_args[names[i]] = arg
            i += 1

        if varargs is not None:
            call_args[varargs] = Type.get("tuple")(call_args[varargs])

        # Setting keyword values
        call_kwargs = {}
        kwarguments = None
        passed_varargs = False
        for arg in func_args:
            if not passed_varargs:
                if arg.is_arg:
                    passed_varargs = True
                continue

            if arg.is_kwarg:
                call_kwargs[arg.arg.name_id] = {}
                kwarguments = arg.arg.name_id
                break
            call_kwargs[arg.arg.name_id] = arg.default

        for kwarg in kwargs:
            if kwarg in call_args:
                if call_args[kwarg] is None:
                    call_args[kwarg] = kwargs[kwarg]
                else:
                    raise excpt.RuntimeError("Duplicate argument")
                continue
            if kwarg in call_kwargs:
                call_kwargs[kwarg] = kwargs[kwarg]
            elif kwarguments is not None:
                call_kwargs[kwarguments][kwarg] = kwargs[kwarg]
            else:
                raise excpt.RuntimeError("Unknown argument")

        if kwarguments is not None:
            call_kwargs[kwarguments] = Type.get("dict")(call_kwargs[kwarguments])

        if None in call_args.values():
            raise excpt.RuntimeError("Missing argument")

        return func.get("__call__")(func, *call_args.values(), **call_kwargs)

    def _class_init(self, cls, args, kwargs):
        return cls(cls, *args, **kwargs)

    @visitor
    def eval(self, node: ast.CallExpr):
        self.set_stat("call_count", self.stats["call_count"] + 1)
        args = [self.eval(arg) for arg in node.args]
        kwargs = {}
        for kwarg in node.keywords:
            kw_arg = self.eval(kwarg)
            kwargs[kw_arg[0]] = kw_arg[1]  # pylint: disable=unsubscriptable-object
        obj = None
        if isinstance(node.func, ast.NameExpr):
            func = self.context.resolve(node.func.name_id)
            if func is None:
                bi_func = builtin.resolve(node.func.name_id)
                if bi_func is None:
                    raise excpt.RuntimeError("Unknown function")
                return bi_func(*args, **kwargs)
        elif isinstance(node.func, ast.AttributeExpr):
            obj = self.eval(node.func.value)
            func = obj.get(node.func.attr)
            args.insert(0, obj)
        else:
            func = self.eval(node.func)

        if isinstance(func, Instance):
            return self._call_func(func, args, kwargs)
        elif isinstance(func, Type):
            return self._class_init(func, args, kwargs)
        elif callable(func):
            return func(*args, *kwargs)
        else:
            raise excpt.RuntimeError("Unknown function")

    @visitor
    def eval(self, node: ast.Keyword):
        if not isinstance(node.arg, ast.NameExpr):
            raise excpt.RuntimeError("Keyword value must be a name")
        arg = node.arg.name_id
        val = self.eval(node.value)
        return arg, val

    @visitor
    def eval(self, node: ast.ConstantExpr):
        if isinstance(node.value, str):
            return builtin.nl_str(node.value)
        if isinstance(node.value, bool):
            return builtin.nl_bool(node.value)
        if isinstance(node.value, int):
            return builtin.nl_int(node.value)
        if isinstance(node.value, float):
            return builtin.nl_float(node.value)
        if node.value is None:
            return builtin.nl_none()
        raise excpt.RuntimeError(f"Unsupported constant type {type(node.value)}")

    @visitor
    def eval(self, node: ast.AttributeExpr):
        if node.ctx == ast.ExprCtx.STORE:
            return node
        val: Instance = self.eval(node.value)
        if node.ctx == ast.ExprCtx.LOAD:
            return val.get(node.attr)
        val._dict.pop(node.attr)

    @visitor
    def eval(self, node: ast.SubscriptExpr):
        if node.ctx == ast.ExprCtx.STORE:
            return node
        val = self.eval(node.value)
        idx = self.eval(node.slice_expr)
        if node.ctx == ast.ExprCtx.LOAD:
            return val.get("__getitem__")(val, idx)
        val.get("__delitem__")(val, idx)

    @visitor
    def eval(self, node: ast.StarredExpr):
        raise NotImplementedError()

    @visitor
    def eval(self, node: ast.NameExpr):
        if node.ctx == ast.ExprCtx.STORE:
            return node
        if node.ctx == ast.ExprCtx.LOAD:
            return self.resolve(node.name_id)
        self.context.delete(node.name_id)
        self.set_stat("var_count", self.context.count_vars())

    @visitor
    def eval(self, node: ast.ListExpr):
        items = [self.eval(i) for i in node.elts]
        return builtin.nl_list(items)

    @visitor
    def eval(self, node: ast.TupleExpr):
        items = tuple(self.eval(i) for i in node.elts)
        return builtin.nl_tuple(items)

    @visitor
    def eval(self, node: ast.SliceExpr):
        low = self.eval(node.lower) if node.lower is not None else None
        upper = self.eval(node.upper) if node.upper is not None else None
        step = self.eval(node.step) if node.step is not None else None
        return builtin.nl_slice(low, upper, step)

    @visitor
    def eval(self, node: ast.Args):
        return node

    @visitor
    def eval(self, node: ast.Arg):
        return node
