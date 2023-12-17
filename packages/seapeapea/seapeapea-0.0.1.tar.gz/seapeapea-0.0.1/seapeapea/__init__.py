import sys
import os
from lark import Lark, Tree, Token, Transformer
import unittest
from collections import defaultdict
from dataclasses import dataclass, field
import time
import re
import argparse
import json
from inspect import currentframe
import glob

# set DEBUG_SEAPEAPEA=1

DEBUG = os.environ.get('DEBUG_SEAPEAPEA') == '1'

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

@dataclass
class Decl:
    qname: list[str]
    args: list[str]
    body: str
    attrs: list[str]

@dataclass
class Enum:
    name: str
    items: list[str, str]
    simple: bool
    rendered: str

@dataclass
class DeclArg:
    type: str
    name: str
    
@dataclass
class Signal:
    name: str
    args: list[DeclArg]
    rendered: str

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport, QtSql

class ExampleFinder:
    def __init__(self, base):
        pros = defaultdict(list)
        for root, dirs, files in os.walk(base):
            for name in files:
                if os.path.splitext(name)[1] != '.pro':
                    continue
                pros[os.path.splitext(name)[0]].append(os.path.join(root, name))
        self._pros = pros

    def paths(self, name, order = None):

        if os.path.isabs(name):
            pros = [name]
        else:
            if name.endswith(".pro"):
                name = os.path.splitext(name)[0]

            if name not in self._pros:
                raise Exception("name {} not in pros".format(name))

            pros = self._pros[name]
            if len(pros) > 1:
                raise Exception("len(pros) > 1 {} ambigous".format(name))

        base = os.path.dirname(pros[0])
        names = [n for n in os.listdir(base) if os.path.splitext(n)[1] == '.cpp']
        if 'main.cpp' in names:
            names = [n for n in names if n != 'main.cpp'] + ['main.cpp']
        return [os.path.join(base,n) for n in names]

def get_first_token(child):
    if isinstance(child, str):
        return child
    return get_first_token(child.children[0])

def get_last_token(child):
    if isinstance(child, str):
        return child
    return get_last_token(child.children[-1])

class Ctx:

    QtWidgets = dir(QtWidgets)
    QtCore = dir(QtCore)
    QtGui = dir(QtGui)
    QtPrintSupport = dir(QtPrintSupport)
    QtSql = dir(QtSql)

    def __init__(self, code):
        self._methods = dict()
        self._methods[None] = []
        self._methods_attrs = dict()
        self._classname = None
        self._inh = defaultdict(list)
        self._members = defaultdict(list)
        self._signals: dict[list[Signal]] = defaultdict(list)
        self._imports = {
            "QtWidgets": set(),
            "QtCore": set(),
            "QtGui": set(),
            "QtPrintSupport": set(),
            "QtSql": set(),
        }
        self._has_main = False
        self._code = code.split("\n")
        self._map = []
        self._enums: list[Enum] = []
        self._class_enums: dict[str, list[Enum]] = defaultdict(list)
        self._decl_fn_in_decl_class = None
        self._itertools = False
        self._import_signal = False
        self._static_fn = False

    def add_map(self, child, res: str):
        first_token = get_first_token(child)
        last_token = get_last_token(child)
        if first_token.line != last_token.line:
            return
        orig = self._code[first_token.line - 1][first_token.column - 1: last_token.end_column - 1]
        self._map.append((orig, res))

    def add_enum(self, enum):
        self._enums.append(enum)

    def add_class_enum(self, classname, enum):
        self._class_enums[classname].append(enum)

    def add_import(self, name):
        if name == 'Signal':
            self._import_signal = True

        if name in self.QtWidgets:
            self._imports["QtWidgets"].add(name)
        if name in self.QtCore:
            self._imports["QtCore"].add(name)
        if name in self.QtGui:
            self._imports["QtGui"].add(name)
        if name in self.QtPrintSupport:
            self._imports["QtPrintSupport"].add(name)
        if name in self.QtSql:
            self._imports["QtSql"].add(name)

    """
    def add_member(self, name):
        self._members[self._classname].append(name)
    """

    def render_imports(self, dialect):
        res = ['import sys']
        if self._itertools:
            res.append('import itertools')

        pyside2 = []
        pyqt5 = []

        for k, values in self._imports.items():
            values = list(values)
            values.sort()
            if len(values) > 0:
                pyqt5.append("from PyQt5.{} import {}".format(k, ", ".join(values)))
                pyside2.append("from PySide2.{} import {}".format(k, ", ".join(values)))
        if self._import_signal:
            pyqt5.append("from PyQt5.{} import {}".format("QtCore", "pyqtSignal as Signal"))
            pyside2.append("from PySide2.{} import {}".format("QtCore", "Signal"))

        imports = ["import sys"]

        if len(pyside2) == 0 and len(pyqt5) == 0:
            return ''
        if dialect == 'pyqt5':
            return "\n".join(pyqt5) + '\n'
        elif dialect == "pyside2":
            return "\n".join(pyside2) + '\n'

        return "{}\ntry:\n{}\nexcept ImportError:\n{}\n\n".format(
            "\n".join(imports),
            indent("\n".join(pyside2)),
            indent("\n".join(pyqt5)),
        )

    def begin_fn(self, decl):
        name = parse_qname(find_first(decl, 'qname'), self)

        attrs = []
        try:
            attrs = self._methods_attrs[name[0]][name[1]]
        except KeyError:
            pass

        self._static_fn = 'static' in attrs

        if DEBUG and 0:
            print("begin_fn", name, "is_static?", self._static_fn)

        self._classname = None
        if len(name) == 2:
            self._classname = name[0]
        
    def inh(self, name):
        return self._inh[name]

    def begin_class(self, decl: Tree):

        ctx = self

        if decl.data != 'decl_class':
            return
        
        classname = find_class_name(decl)

        classes = []
        inh = find_first(decl, 'inh')
        if inh:
            for inh_item in find_all(inh, 'inh_item'):
                names = parse_qname(find_first(find_first(inh_item, 'type'), 'qname'), ctx)
                name = ".".join(names)
                classes.append(name)
                self.add_import(name)

        self._inh[classname] = classes

        methods = []

        for c in classes:
            if c in self.QtWidgets:
                methods += dir(getattr(QtWidgets, c))
            if c in self.QtCore:
                methods += dir(getattr(QtCore, c))
            if c in self.QtGui:
                methods += dir(getattr(QtGui, c))
        
        methods_attrs = dict()
        for child_decl in find_all(decl, 'decl'):
            if child_decl.children[0].data == 'decl_fn':
                decl_fn = child_decl.children[0]

                method_attrs = []

                attrs = find_all(decl_fn, 'attr')
                for attr in attrs:
                    for ch in attr.children:
                        method_attrs.append(str(ch))

                qname = parse_qname(find_first(decl_fn, "qname"), ctx)
                methods.append(qname[0])
                methods_attrs[qname[0]] = method_attrs

        methods = [m for m in methods if not m.startswith("__")]

        self._methods[classname] = methods
        self._methods_attrs[classname] = methods_attrs

        for c in classes:
            if c in self._inh:
                self._methods[classname] += self._methods[c]

        for decl_mem in find_all(decl, 'decl_mem'):
            members = [find_token(decl_mem_name, 'NAME') for decl_mem_name in find_all(decl_mem, 'decl_mem_name')]
            #print("members", classname, members)
            self._members[classname] += members

        for decl_child in [item.children[0] for item in find_all(decl, 'decl')]:
            if decl_child.data == 'decl_enum':
                enum = parse_decl_enum(decl_child, ctx)
                self._class_enums[classname].append(enum)

        signals = False
        for child in decl.children:
            
            if isinstance(child, str):
                pass
            else:
                if child.data == 'access':
                    #print("access")
                    signals = False
                elif child.data == 'signals':
                    #print("access")
                    signals = True
                elif child.data == 'decl':
                    if signals and child.children[0].data == 'decl_fn':
                        decl_fn = child.children[0]
                        signal = parse_signal(decl_fn, ctx)
                        self._signals[classname].append(signal)
                        self.add_import('Signal')

    def end_class(self):
        pass

    def asis_tree(self, tree) -> str:
        if tree is None:
            return ''
        first_token = get_first_token(tree)
        last_token = get_last_token(tree)
        return self.asis_range(first_token, last_token)

    def asis_range(self, first_token, last_token) -> str:

        def line_tail_with_token(token: Token):
            line = self._code[token.line - 1]
            return line[token.column - 1:]

        def line_head_with_token(token: Token):
            line = self._code[token.line - 1]
            return line[:token.end_column - 1]

        if first_token.line == last_token.line:
            return self._code[first_token.line - 1][first_token.column - 1: last_token.end_column - 1]
        
        fragment = []
        for i in range(first_token.line, last_token.line + 1):
            if i == first_token.line:
                fragment.append(line_tail_with_token(first_token))
            elif i == last_token.line:
                fragment.append(line_head_with_token(last_token))
            else:
                fragment.append(self._code[i - 1])
        return "\n".join(fragment)
    
    def cls_or_self(self):
        return "cls" if self._static_fn else "self"

    def has_method(self, method):

        classname = self._classname
        if self._decl_fn_in_decl_class:
            classname = self._decl_fn_in_decl_class

        if classname not in self._methods:
            return False

        return method in self._methods[classname]

    def has_member(self, name):

        classname = self._classname
        if self._decl_fn_in_decl_class:
            classname = self._decl_fn_in_decl_class

        if classname not in self._members:
            return False

        if name in self._members[classname]:
            return True

        for enum in self._class_enums[classname]:
            if name in enum.items.keys():
                return True

        return False

def parse_signal(decl_fn, ctx) -> Signal:
    qname = parse_qname(find_first(decl_fn, "qname"), ctx)
    args = parse_decl_args(decl_fn, ctx)
    types = [arg.type for arg in args]
    name = qname[0]
    rendered = '{} = Signal({})'.format(name, ", ".join(types))
    return Signal(name, args, rendered)

class Preprocessor:

    def __init__(self, includepath = None):
        if includepath is None:
            includepath = set()
        self._includepath = set(includepath)
        
    def _find(self, name):
        for base in self._includepath:
            path = os.path.join(base, name)
            if os.path.exists(path):
                return path
        name = os.path.basename(name)
        for base in self._includepath:
            path = os.path.join(base, name)
            if os.path.exists(path):
                return path

    def read(self, paths):

        for path in paths:
            base = os.path.dirname(path)
            self._includepath.add(base)

        once = set()
        once.add(None)
        
        lines = []

        for path in paths:
            once.add(path)
            with open(path, encoding='utf-8') as f:
                lines += f.readlines()
        
        def expand(path):
            with open(path, encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines) + "\n"

        def uncomment(text):
            while "/*" in text:
                p1 = text.index("/*")
                p2 = text.index("*/", p1 + 1)
                text = text[:p1] + text[p2+2:]
            lines = [line for line in text.split("\n") if re.match("//", line) is None]
            return "\n".join(lines)

        while True:
            expanded = False
            for i, line in enumerate(lines):
                m = re.match('#\\s*include\\s*["<](.*)[">]', line)
                if m:
                    path = self._find(m.group(1))
                    if path not in once:
                        lines[i] = expand(path)
                        once.add(path)
                        expanded = True
            if not expanded:
                return uncomment("".join(lines) + "\n")
            lines = [line + "\n" for line in "".join(lines).split("\n")]


def find_all(tree, data, trace = False):
    if tree is None:
        raise Exception("foo")
    return [child for child in tree.children if hasattr(child, 'data') and child.data == data]

def find_token(tree, type) -> str:
    for child in tree.children:
        if isinstance(child, str):
            if child.type == type:
                return child.value

def find_tokens(tree, type) -> list[str]:
    res = []
    for child in tree.children:
        if isinstance(child, str):
            if child.type == type:
                res.append(child.value)
    return res

def find_first(tree, data, trace = False):
    for child in tree.children:
        if hasattr(child, 'data') and child.data == data:
            return child
    t = 1

def parse_qname(qname, ctx):
    return [child.value for child in qname.children if child.type == 'NAME']

def parse_stat_var(stat_var, ctx: Ctx):
    varname = find_and_parse_qname(find_first(stat_var, 'stat_var_name'), ctx)
    varname = varname[0]
    varname = {
        'from': 'from_',
        'in': 'in_'
    }.get(varname, varname)

    expr = find_first(stat_var, 'expr')
    type = find_token(find_first(stat_var, 'type'), 'NAME')
    ctx.add_import(type)
    return "{} = {}".format(varname, parse_expr(expr, ctx))

"""
def parse_name(name, ctx: Ctx):
    names = [child.value for child in name.children if child.value != '::']

    if len(names) > 1:
        print("len(names) > 1", names)
    return names
"""

"""
def call_chain(expr_call, ctx, res = None):
    if res is None:
        res = []
    expr = find_first(expr_call, 'expr')
    if expr is None:
        return res
    expr_call = expr.children[0]
    if expr_call.data == 'expr_call':
        res.append(expr_call)
        return call_chain(expr_call, ctx, res)
    else:
        return res
"""

(
    NONE,
    SUBSCR,
    CALL,
    CONSTR,
    SUBEXPR
) = range(5)

def get_name_and_args(child, ctx: Ctx):

    if child.data == 'expr_call':
        return get_name_and_args(child.children[0], ctx)

    if child.data in ['expr_call_simple', 'expr_call_chain']:
        call_base = find_first(child, 'call_base')
        name = find_token(call_base, 'NAME')
        expr_cast = find_first(call_base, 'expr_cast')
        expr_sub = find_first(call_base, 'expr_sub')

        if DEBUG and 0:
            print("call_base", call_base)

        if name == "this":
            name = "self"

        ctx.add_import(name)

        if name is None:
            print("name is none {}".format(get_linenumber()))

    elif child.data == 'call_item':

        name = find_token(child, 'NAME')
        expr_cast = None
        expr_sub = None

    else:
        raise Exception("not implemented {}".format(get_linenumber()))

    if expr_cast:
        expr = find_first(expr_cast, 'expr')
        if expr.children[0].data == 'expr_call':
            expr_call = expr.children[0]
            if expr_call.children[0].data == 'expr_call_simple':
                return get_name_and_args(expr_call.children[0], ctx)
        raise Exception("not implemented {}".format(get_linenumber()))

    subscr = find_first(child, 'subscr')
    call = find_first(child, 'call')
    constr = find_first(child, 'constr')

    if expr_sub:
        name = parse_expr_sub(expr_sub, ctx)
        args = []
        type = SUBEXPR
        has_args = False
    elif subscr:
        args = find_and_parse_args(subscr, ctx)
        has_args = True
        type = SUBSCR
    elif call:
        args = find_and_parse_args(call, ctx)
        has_args = True
        type = CALL
    elif constr:
        args = find_and_parse_args(constr, ctx)
        has_args = True
        type = CONSTR
    else:
        args = []
        has_args = False
        type = NONE

    return name, args, has_args, type

def is_cast_expr(expr):
    call_base = find_first(expr, 'call_base')
    if call_base is None:
        return False
    expr_sub = find_first(call_base, 'expr_sub')
    if expr_sub is None:
        return False
    if len(expr_sub.children) == 3 and expr_sub.children[0].value == '(' and expr_sub.children[1].data == 'expr' and expr_sub.children[1].children[0].data == 'expr_name' and expr_sub.children[2].value == ')':
        return True
    return False

def parse_expr_call(expr_call, ctx: Ctx):

    child = expr_call.children[0]

    if DEBUG and 1:
        print("parse_expr_call", child.data, str(child)[:20])

    if child.data == 'expr_call_simple':

        expr_call_simple = child

        if is_cast_expr(expr_call_simple):
            call = find_first(expr_call_simple, 'call')
            args = find_all(call, 'args')
            if len(args) == 1:
                arg = args[0]
                expr = arg.children[0]
                if expr.data == 'expr':
                    expr_call_ = expr.children[0]
                    if expr_call_.data == 'expr_call':
                        return parse_expr_call(expr_call_, ctx)
            print("unexpected form of cast {}".format(get_linenumber()))

        name, args, has_args, call_type = get_name_and_args(expr_call_simple, ctx)

        if call_type != SUBEXPR:
            ctx.add_import(name)

        if call_type in [CALL, CONSTR]:
            if ctx.has_method(name):
                name = ctx.cls_or_self() + "." + name
        elif call_type == SUBSCR:
            if ctx.has_member(name):
                name = ctx.cls_or_self() + "." + name

        if name == 'connect' and len(args) == 4:
            emitter, signal, receiver, slot = args
            signal = signal.split(".")[-1]
            slot = slot.split(".")[-1]
            if ctx.has_member(emitter):
                emitter = "self." + emitter
            res = "{}.{}.connect({}.{})".format(emitter, signal, receiver, slot)

            return res
        
        if name == 'qMin':
            name = 'min'
        if name == 'qMax':
            name = 'max'
        
        if name in ['QStringLiteral', 'QLatin1String', 'QString', 'tr', 
            'cls.tr', 'self.tr', 'qreal', 'qobject_cast', 'qAsConst', 'QLatin1Char', 'qOverload'] and len(args) == 1:
            return args[0]

        if name == 'QString' and len(args) == 0:
            return '""'

        if call_type == SUBSCR:
            op = "["
            cl = "]"
        elif call_type == CALL:
            op = "("
            cl = ")"
        elif call_type == SUBEXPR:
            op = "("
            cl = ")"
        else:
            op = "[not implemented]"
            cl = "[not implemented]"
            print("unexpected call type {} {}".format(call_type, get_linenumber()))

        return "{}{}{}{}".format(name, op, ", ".join(args), cl)

    elif child.data == 'expr_call_chain':

        expr_call_chain = child
        name, args, has_args, call_type = get_name_and_args(expr_call_chain, ctx)
        ctx.add_import(name)

        if has_args:
            if call_type == SUBSCR and ctx.has_member(name):
                name = ctx.cls_or_self() + "." + name
            elif call_type in [CALL, CONSTR] and ctx.has_method(name):
                name = ctx.cls_or_self() + "." + name
        else:
            if ctx.has_member(name):
                name = ctx.cls_or_self() + "." + name

        basename = name
        baseargs = args
        chain = []
        if has_args:
            if call_type == SUBSCR:
                chain.append("{}[{}]".format(name, ", ".join(args)))
            else:
                chain.append("{}({})".format(name, ", ".join(args)))
        else:
            chain.append("{}".format(name))

        chain_name = []
        chain_args = []

        for call_item in find_all(expr_call_chain, 'call_item'):
            name, args, has_args, call_type = get_name_and_args(call_item, ctx)
            if has_args:
                if call_type == SUBSCR:
                    chain.append("{}[{}]".format(name, ", ".join(args)))
                elif call_type == CALL:
                    if name == 'mid' and len(args) in [1, 2]:
                        if len(args) == 2:
                            arg1, arg2 = args
                            chain.append("[{}:{}]".format(arg1, arg1 + "+" + arg2))
                        elif len(args) == 1:
                            arg1, = args
                            chain.append("[{}:]".format(arg1))
                    else:
                        chain.append("{}({})".format(name, ", ".join(args)))
            else:
                chain.append("{}".format(name))
            chain_name.append(name)
            chain_args.append(args)

        if len(chain_name) > 0 and chain_name[-1] == 'drawConvexPolygon':
            chain[-1] = 'drawConvexPolygon(QPolygonF({}))'.format(chain_args[-1][0])
            ctx.add_import('QPolygonF')

        if basename in ['QString', 'tr', 'self.tr'] and set(chain_name) == set(['arg']):
            pattern = baseargs[0]
            pattern = re.sub("%[0-9]", lambda m: "{" + m.group(0).replace("%", "arg") + "}", pattern)
            args = []
            for item in chain_args:
                args += item
            return pattern + ".format(" + ", ".join(["arg{} = {}".format(i+1, arg) for i, arg in enumerate(args)]) + ")"

        if basename == 'QOverload' and len(args) == 1:
            return args[0]

        if basename == 'QString' and chain_name == ['number']:
            return "str({})".format(args[0])

        if basename == 'QString' and chain_name[0] == 'fromLatin1' and set(chain_name[1:]) == set(['arg']):
            pattern = chain_args[0][0]
            pattern = re.sub("%[0-9]", lambda m: "{" + m.group(0).replace("%", "arg") + "}", pattern)
            args = [args[0] for args in chain_args[1:]]
            return pattern + ".format(" + ", ".join(["arg{} = {}".format(i+1, arg) for i, arg in enumerate(args)]) + ")"

        return dot_join(chain)
    else:
        raise Exception("not implemented {} {}".format(child.data, get_linenumber()))

def dot_join(chain):
    res = []
    for item in chain:
        if len(res) > 0 and not item.startswith("["):
            res.append(".")
        res.append(item)
    return "".join(res)

# todo replace
def parse_args_(args, ctx: Ctx):
    if args is None:
        #raise Exception("parse_args")
        return []
    return [parse_expr(child, ctx) for child in find_all(args, 'expr')]

def find_and_parse_args(tree, ctx) -> list[str]:
    args = find_first(tree, 'args')
    if args is None:
        return []
    return [parse_expr(expr, ctx) for expr in find_all(args, 'expr')]

def parse_expr_new(expr_new, ctx: Ctx):
    type = find_and_parse_qname(expr_new, ctx)
    ctx.add_import(type[0])
    type = ".".join(type)
    args = parse_args_(find_first(expr_new, 'args'), ctx)
    return "{}({})".format(type, ", ".join(args))

def parse_expr_name(expr_name, ctx: Ctx):
    value = expr_name.children[0].value
    value = {
        'this': 'self',
        'true': 'True',
        'false': 'False',
        'from': 'from_',
        'in': 'in_'
    }.get(value, value)
    if ctx.has_member(value):
        value = "self." + value
    return value

def parse_expr_overload(expr_overload, ctx: Ctx):
    return parse_expr(find_first(expr_overload, "expr"), ctx)

def parse_expr_fnref(expr_fnref, ctx: Ctx):
    #names = [child.value for child in expr_fnref.children if child.value != '::']
    names = [child.value for child in expr_fnref.children if child.type == 'NAME']
    ctx.add_import(names[0])
    return ".".join(names)

def parse_init_list(init_list, ctx):
    return "[" + ", ".join(parse_expr(expr, ctx) for expr in find_all(init_list, 'expr')) + "]"

def parse_expr_pref(expr_pref, ctx):
    expr = find_first(expr_pref, 'expr')
    expr_ = parse_expr(expr, ctx)
    op = expr_pref.children[0].value
    op = {
        "!": "not "
    }.get(op, op)
    return op + expr_

def parse_expr_inf(expr_inf, ctx):
    [expr1, expr2] = [parse_expr(expr, ctx) for expr in find_all(expr_inf, 'expr')]
    op = find_first(expr_inf, 'expr_inf_op').children[0].value
    op = {
        "&&": "and",
        "||": "or"
    }.get(op, op)

    return "{} {} {}".format(expr1, op, expr2)

def parse_expr_sub(expr_sub, ctx):
    expr = parse_expr(find_first(expr_sub, 'expr'), ctx)
    name = find_token(expr_sub, 'NAME')
    if name:
        return "({} = {})".format(name, expr)
    return "({})".format(expr)

def parse_expr_nref(expr_nref, ctx: Ctx):
    name = find_token(expr_nref, 'NAME')
    if ctx.has_member(name):
        return "self." + name
    return name

def parse_expr_tern(expr_tern, ctx):
    exprs = [parse_expr(expr, ctx) for expr in find_all(expr_tern, 'expr')]
    return "{} if {} else {}".format(exprs[1], exprs[0], exprs[2])

def parse_expr_ccast(expr_ccast, ctx):
    return parse_expr(find_first(expr_ccast, 'expr'), ctx)

def parse_expr_inc(expr_inc, ctx):
    expr = parse_expr(find_first(expr_inc, 'expr'), ctx)
    return "{} += 1".format(expr)

def parse_expr_dec(expr_dec, ctx):
    expr = parse_expr(find_first(expr_dec, 'expr'), ctx)
    return "{} -= 1".format(expr)

def parse_expr_signal(expr_signal, ctx: Ctx):
    name = find_and_parse_qname(expr_signal, ctx)
    name = ".".join(name)
    if ctx.has_method(name):
        name = ctx.cls_or_self() + "." + name
    args = parse_decl_args(expr_signal, ctx)
    types = [arg.type for arg in args]
    return "{}[{}]".format(name, ", ".join(types))

def parse_expr_slot(expr_slot, ctx: Ctx):
    name = find_and_parse_qname(expr_slot, ctx)
    name = ".".join(name)
    if ctx.has_method(name):
        name = ctx.cls_or_self() + "." + name
    args = parse_decl_args(expr_slot, ctx)
    types = [arg.type for arg in args]
    return "{}[{}]".format(name, ", ".join(types))

def parse_expr(expr, ctx: Ctx):

    child = expr.children[0]

    if DEBUG and 1:
        print("parse_expr", child.data)

    res = ""

    if child.data == 'expr_call':
        res = parse_expr_call(child, ctx)
    elif child.data == 'expr_new':
        res = parse_expr_new(child, ctx)
    elif child.data == 'expr_name':
        res = parse_expr_name(child, ctx)
    elif child.data == 'expr_overload':
        res = parse_expr_overload(child, ctx)
    elif child.data == 'expr_fnref':
        res = parse_expr_fnref(child, ctx)
    elif child.data == 'expr_lit':
        res = parse_expr_lit(child, ctx)
    elif child.data == 'init_list':
        res = parse_init_list(child, ctx)
    elif child.data == 'expr_pref':
        res = parse_expr_pref(child, ctx)
    elif child.data == 'expr_inf':
        res = parse_expr_inf(child, ctx)
    elif child.data == 'expr_sub':
        res = parse_expr_sub(child, ctx)
    elif child.data == 'expr_nref':
        res = parse_expr_nref(child, ctx)
    elif child.data == 'expr_tern':
        res = parse_expr_tern(child, ctx)
    elif child.data == 'expr_ccast':
        res = parse_expr_ccast(child, ctx)
    elif child.data == 'expr_inc':
        res = parse_expr_inc(child, ctx)
    elif child.data == 'expr_dec':
        res = parse_expr_dec(child, ctx)
    elif child.data == 'expr_signal':
        res = parse_expr_signal(child, ctx)
    elif child.data == 'expr_slot':
        res = parse_expr_slot(child, ctx)
    else:
        res = "not implemented {} {}".format(child.data, get_linenumber())

    ctx.add_map(child, res)

    return res

def asis(tree):
    if tree is None:
        return " "
    if isinstance(tree, str):
        return tree.value
    else:
        return " ".join([asis(child) for child in tree.children])

def parse_comp_stat(comp_stat, ctx: Ctx):
    res = []
    for stat in find_all(comp_stat, 'stat'):
        res.append(parse_stat(stat, ctx))
    return "\n".join(res)

def get_inc_var(var_inc, ctx: Ctx):
    expr = find_first(var_inc, 'expr')
    expr_inc = expr.children[0]
    if expr_inc.data != 'expr_inc':
        return None
    return parse_expr(find_first(expr_inc, 'expr'), ctx)

def parse_stat_for(stat_for, ctx: Ctx):
    for_init = find_first(stat_for, 'for_init')
    for_test = find_first(stat_for, 'for_test')
    for_inc = find_first(stat_for, 'for_inc')
    body = parse_comp_stat(find_first(stat_for, 'comp_stat'), ctx)

    init = dict()
    test = []
    var_inc = None
    var_dec = None
    
    if for_init:
        for item in find_all(for_init, 'for_init_item'):
            name = find_token(item, 'NAME')
            value = parse_expr(find_first(item, 'expr'), ctx)
            init[name] = value
        
    if for_test:
        expr = for_test.children[0]
        if expr.children[0].data == 'expr_inf':
            lhs, op, rhs = expr.children[0].children
            lhs = parse_expr(lhs, ctx)
            rhs = parse_expr(rhs, ctx)
            op = op.children[0].value
            test = lhs, op, rhs
    
    if for_inc:
        inc_items = find_all(for_inc, 'inc_item')
        if len(inc_items) == 1:
            expr = find_first(inc_items[0], 'expr')
            if expr.children[0].data == 'expr_inc':
                expr_inc = expr.children[0]
                var_inc = parse_expr(find_first(expr_inc, 'expr'), ctx)
            if expr.children[0].data == 'expr_dec':
                expr_dec = expr.children[0]
                var_dec = parse_expr(find_first(expr_dec, 'expr'), ctx)
    
    head = None
    if len(init) > 0 and len(test) > 0:
        init_vars = init.keys()
        if var_inc is not None:
            lhs, op, rhs = test
            if op in ['<','<='] and var_inc == lhs and var_inc in init_vars:
                if op == '<':
                    stop = rhs
                else:
                    stop = rhs + " + 1"
                head = "for {} in range({}, {}):".format(var_inc, init[var_inc], stop)
        if var_dec is not None:
            lhs, op, rhs = test
            if op == '<':
                stop = rhs
            else:
                stop = rhs + " - 1"
            if op in ['>', '>='] and var_dec == lhs and var_dec in init_vars:
                head = "for {} in range({}, {}, -1):".format(var_dec, init[var_dec], stop)

    if head is None:
        first, last = [token for token in stat_for.children if isinstance(token, str) and token.value in ['for', ')']]
        orig = ctx.asis_range(first, last)

        head = "not implemented {} {}".format(orig, get_linenumber())
    return head + "\n" + indent(body)

def indent(text):
    return "\n".join(["    " + line for line in text.split("\n")])

def parse_stat_if(stat_if, ctx: Ctx):

    def get_body(child):
        comp_stat = find_first(child, 'comp_stat')
        if comp_stat is None:
            t = 1
        return indent(parse_comp_stat(comp_stat, ctx)) + "\n"

    def get_head(word, child):
        expr = find_first(child, 'expr')
        if expr:
            cond = " " + parse_expr(expr, ctx)
        else:
            cond = ""
        return "{}{}:\n".format(word, cond)

    res = []
    for child in stat_if.children:
        #print(child.data)
        if child.data == 'stat_if_if':
            head = get_head("if", child)
            body = get_body(child)
            res.append(head + body)
        elif child.data == 'stat_if_else_if':
            head = get_head("elif", child)
            body = get_body(child)
            res.append(head + body)
        elif child.data == 'stat_if_else':
            head = get_head("else", child)
            body = get_body(child)
            res.append(head + body)

    #t = 1

    return "".join(res)


def parse_type(type, ctx: Ctx):
    return parse_qname(find_first(type, 'qname'), ctx)

def find_and_parse_qname(tree, ctx: Ctx):
    return parse_qname(find_first(tree, 'qname'), ctx)

def parse_stat_stack(stat_stack, ctx: Ctx):
    types = parse_type(find_first(stat_stack, 'type'), ctx)
    ctx.add_import(types[0])
    
    names = [parse_qname(qname, ctx) for qname in find_all(stat_stack, 'qname')]
    type = ".".join(types)

    if DEBUG and 1:
        print("type", type)

    ctx.add_import(type)

    if len(names) > 1:
        if contains_token(stat_stack, '(') or contains_token(stat_stack, '{'):
            return "not implemented for len(names) > 1 and args {}".format(get_linenumber())
        qnames = [parse_qname(qname, ctx) for qname in find_all(stat_stack, 'qname')]
        res = []
        for qname in qnames:
            name = ".".join(qname)
            res.append("{} = {}()".format(name, type))
        return "\n".join(res)

    args = find_and_parse_args(stat_stack, ctx)

    if type in ['QApplication', 'QGuiApplication']:
        args = ['sys.argv']

    name = ".".join(names[0])

    if type == 'QString' and len(args) == 0:
        return '{} = ""'.format(name)
    
    if type in ["QStringList", "QList"]:
        return "{} = [{}]".format(name, ", ".join(args))

    return "{} = {}({})".format(name, type, ", ".join(args))

def parse_stat_return(stat_return, ctx):
    return "return {}".format(parse_expr(find_first(stat_return, 'expr'), ctx))

def parse_stat_stack_array(stat_stack_array: Tree, ctx):
    name = find_token(stat_stack_array, 'NAME')
    expr = parse_expr(find_first(stat_stack_array, 'expr'), ctx)
    return "{} = [None] * {}".format(name, expr)

def contains_token(tree, value):
    for child in tree.children:
        if isinstance(child, str) and child.value == value:
            return True
    return False

def parse_stat_assign(stat_assign, ctx: Ctx):

    child = stat_assign.children[0]

    op = find_first(child, 'assing_op').children[0].value
    
    if child.data == 'stat_assing_var':
        stat_assing_var = child
        name = find_tokens(stat_assing_var, 'NAME')
        #expr = parse_expr(find_first(stat_assing_var, 'expr'), ctx)
        exprs = []
        for expr in find_all(stat_assing_var, 'expr'):
            exprs.append(parse_expr(expr, ctx))
        rhs = exprs.pop()
        lhs = ".".join(name) + "".join(["[{}]".format(e) for e in exprs])
        s = "{} {} {}".format(lhs, op, rhs)
        if ctx.has_member(name[0]):
            s = ctx.cls_or_self() + "." + s
        return s
    elif child.data == 'stat_assing_ref':
        stat_assing_ref = child
        expr_call = parse_expr_call(find_first(stat_assing_ref, 'expr_call'), ctx)
        expr = parse_expr(find_first(stat_assing_ref, 'expr'), ctx)
        s = "{} {} {}".format(expr_call, op, expr)
        return s
    else:
        raise Exception("not implemented {} {}".format(child.data, get_linenumber()))

def parse_stat_emit(stat_emit, ctx: Ctx):
    expr = find_first(stat_emit, 'expr')
    expr_call = expr.children[0]

    if expr_call.data != 'expr_call':
        return "not implemented {} {} {}".format(expr_call.data, ctx.asis_tree(stat_emit), get_linenumber())

    name, args, has_args, call_type = get_name_and_args(expr_call, ctx)

    return "self.{}.emit({})".format(name, ", ".join(args))

def parse_expr_lit(expr_lit, ctx):
    if expr_lit.children[0].type == 'STR':
        value = " + ".join([t.value for t in expr_lit.children])
    else:
        value = expr_lit.children[0].value
    return value

def parse_stat_switch(stat_switch, ctx):

    res = []

    expr = parse_expr(find_first(stat_switch, 'expr'), ctx)

    for case in find_all(stat_switch, 'stat_switch_case'):
        qname = find_first(case, 'qname')
        expr_lit = find_first(case, 'expr_lit')
        body = [e for e in [parse_stat(stat, ctx) for stat in find_all(case, 'stat')] if e != 'break']
        body = "\n".join(body)
        if qname:
            value = ".".join(parse_qname(qname, ctx))
        elif expr_lit:
            value = parse_expr_lit(expr_lit, ctx)
        else:
            value = None

        if value is None:
            head = "else:"
        else:
            cmp = "{} == {}".format(expr, value)
            if len(res) == 0:
                head = "if {}:".format(cmp)
            else:
                head = "elif {}:".format(cmp)
        res.append(head + "\n" + indent(body) + "\n")
    return "".join(res)
        
def parse_stat_scope(stat_scope, ctx):
    return "\n".join([parse_stat(stat, ctx) for stat in find_all(stat_scope, 'stat')])

def parse_stat_foreach(stat_foreach, ctx):
    name = find_token(stat_foreach, 'NAME')
    items = parse_expr(find_first(stat_foreach, 'expr'), ctx)
    body = parse_comp_stat(find_first(stat_foreach, 'comp_stat'), ctx)
    head = "for {} in {}:".format(name, items)
    return head + "\n" + indent(body) + "\n"

def parse_stat_foreach_macro(stat_foreach_macro, ctx):
    name = find_token(stat_foreach_macro, 'NAME')
    items = parse_expr(find_first(stat_foreach_macro, 'expr'), ctx)
    body = parse_comp_stat(find_first(stat_foreach_macro, 'comp_stat'), ctx)
    head = "for {} in {}:".format(name, items)
    return head + "\n" + indent(body) + "\n"

def parse_stat_while(stat_while, ctx):
    cond = parse_expr(find_first(stat_while, 'expr'), ctx)
    body = parse_comp_stat(find_first(stat_while, 'comp_stat'), ctx)
    head = "while {}:".format(cond)
    return head + "\n" + indent(body) + "\n"

def parse_stat(stat: Tree, ctx: Ctx):
    #print("parse_stat")
    child = stat.children[0]

    if DEBUG and 1:
        print("parse_stat", child.data, str(child)[:60])

    #print("stat", child.data)

    if child.data == 'stat_var':
        return parse_stat_var(child, ctx)
    elif child.data == 'stat_expr':
        expr = child.children[0]
        return parse_expr(expr, ctx)
    elif child.data == 'stat_for':
        return parse_stat_for(child, ctx)
    elif child.data == 'stat_if':
        return parse_stat_if(child, ctx)
    elif child.data == 'stat_stack':
        return parse_stat_stack(child, ctx)
    elif child.data == 'stat_return':
        return parse_stat_return(child, ctx)
    elif child.data == 'stat_assign':
        return parse_stat_assign(child, ctx)
    elif child.data == 'stat_emit':
        return parse_stat_emit(child, ctx)
    elif child.data == 'prepr':
        return ''
    elif child.data == 'stat_switch':
        return parse_stat_switch(child, ctx)
    elif child.data == 'stat_scope':
        return parse_stat_scope(child, ctx)
    elif child.data == 'stat_foreach':
        return parse_stat_foreach(child, ctx)
    elif child.data == 'stat_foreach_macro':
        return parse_stat_foreach_macro(child, ctx)
    elif child.data == 'decl_enum':
        enum = parse_decl_enum(child, ctx)
        ctx.add_enum(enum)
        return ''
    elif child.data == 'qtmacro':
        return ''
    elif child.data == 'stat_while':
        return parse_stat_while(child, ctx)
    elif child.data == 'stat_stack_array':
        return parse_stat_stack_array(child, ctx)
    else:
        return "not implemented {} {}".format(child.data, get_linenumber())

def parse_decl_args(decl, ctx: Ctx) -> list[DeclArg]:
    args = []
    decl_args = find_first(decl, 'decl_args')
    if decl_args is None:
        return []
    for i, decl_arg in enumerate(find_all(decl_args, 'decl_arg')):
        name = find_token(decl_arg, 'NAME')
        if name is None:
            name = "_{}".format(i)
        type = parse_qname(find_first(find_first(decl_arg, 'type'), 'qname'), ctx)
        type = ".".join(type)
        args.append(DeclArg(type, name))
        ctx.add_import(type)
    return args

def parse_decl_fn_stats(decl_fn, ctx: Ctx):
    fn_body = find_first(decl_fn, 'fn_body')
    if fn_body:
        stats = [parse_stat(stat, ctx) for stat in find_all(fn_body, 'stat')]
    else:
        stats = []
    return stats

def decl_fn_imports(decl_fn, ctx: Ctx):
    decl_args = find_first(decl_fn, 'decl_args')
    if decl_args:
        for decl_arg in find_all(decl_args, 'decl_arg'):
            type = find_first(decl_arg, 'type')
            name = find_token(type, 'NAME')
            if name:
                ctx.add_import(name)

def parse_decl_fn(decl_fn, ctx: Ctx) -> list[Decl]:
    #print("decl_fn")
    #qname = [child.value for child in find_first(decl_fn, 'qname').children if isinstance(child, str)]
    ctx.begin_fn(decl_fn)
    qname = parse_qname(find_first(decl_fn, 'qname'), ctx)
    if qname == ['main']:
        ctx._has_main = True
    args = parse_decl_args(decl_fn, ctx)

    """
    def render_decl_fn(decl: Decl):
        head = "def {}({}):".format(decl.name, ", ".join([arg.name for arg in decl.args]))
        body = indent(decl.body)
        return head + "\n" + indent(body)
    """

    fn_body = find_first(decl_fn, 'fn_body')
    if fn_body:
        stats = parse_decl_fn_stats(decl_fn, ctx)
        enums = [parse_decl_enum(enum, ctx) for enum in find_all(fn_body, 'decl_enum')]
        for enum in enums:
            ctx.add_enum(enum)
        #fns = [parse_decl_fn(decl_fn, ctx) for decl_fn in find_all(fn_body, 'decl_fn')]
        #stats = [enum.rendered for enum in enums] + [render_decl_fn(decl) for decl in fns] + stats
    else:
        stats = []

    attrs = []
    try:
        attrs = ctx._methods_attrs[qname[0]][qname[1]]
    except KeyError:
        pass

    decl_fn_imports(decl_fn, ctx)
    return [Decl(qname, args, "\n".join(stats), attrs)]

def parse_decl_oper(decl_oper, ctx: Ctx) -> list[Decl]:
    op = find_first(decl_oper, 'decl_oper_op').children[0].value
    qname = ['operator {}'.format(op)]
    args = parse_decl_args(decl_oper, ctx)
    stats = [parse_stat(stat, ctx) for stat in find_all(decl_oper, 'stat')]
    decl_fn_imports(decl_oper, ctx)
    attrs = []
    return [Decl(qname, args, "\n".join(stats), attrs)]

def find_class_name(decl_class):
    names = find_tokens(decl_class, 'NAME')
    classname = None
    if len(names) == 1:
        classname = names[0]
    elif len(names) == 2:
        # import-export macro
        if re.match('^[A-Z0-9_]+$', names[0]):
            classname = names[1]
    if classname is None:
        print("cannot parse class name {}".format(names))
    return classname

def parse_decl_class(decl_class: Tree, ctx: Ctx):
    ctx.begin_class(decl_class)
    
    classname = find_class_name(decl_class)

    res = []

    for child in find_all(decl_class, 'decl'):
        if child.children[0].data == 'decl_fn':
            decl_fn = child.children[0]

            qname = parse_qname(find_first(decl_fn, 'qname'), ctx)
            args = parse_decl_args(decl_fn, ctx)
            last_child = decl_fn.children[-1]
            if isinstance(last_child, str) and last_child.value == ";":
                pass
            else:
                ctx._decl_fn_in_decl_class = classname
                stats = parse_decl_fn_stats(decl_fn, ctx)    
                ctx._decl_fn_in_decl_class = None
                attrs = []
                try:
                    attrs = ctx._methods_attrs[classname][qname[-1]]
                except KeyError:
                    pass
                res.append(Decl([classname] + qname, args, "\n".join(stats), attrs))
    return res

def parse_decl_ns(decl_ns, ctx):
    res = []
    for child in decl_ns.children:
        if isinstance(child, str):
            continue
        if child.data == 'decl':
            res += parse_decl(child, ctx)
        elif child.data in ['prepr', 'qtmacro']:
            pass
        else:
            raise Exception("not implemented {} {}".format(child.data, get_linenumber()))
    return res

def parse_decl_enum(decl_enum, ctx: Ctx) -> Enum:

    simple = True
    names = dict()

    enum_name = find_token(decl_enum, 'NAME')

    named = find_all(decl_enum, 'named')

    for i, item in enumerate(find_all(named[0], 'named_item')):
        expr = find_first(item, 'expr')
        if expr:
            value = parse_expr(expr, ctx)
            simple = False
        else:
            value = str(i)
        name = find_token(item, 'NAME')
        names[name] = value
    
    if simple:
        rendered = "(" + ", ".join(names.keys()) + ") = range({})".format(len(names))
    else:
        rendered = "\n".join(["{} = {}".format(name, value) for name, value in names.items()])
    
    if len(named) == 2:

        for item in find_all(named[1], 'named_item'):
            expr = find_first(item, 'expr')
            if expr:
                value = parse_expr(expr, ctx)
            else:
                value = "?"
            name = find_token(item, 'NAME')
            rendered += "\n{} = {}".format(name, value)

    return Enum(enum_name, names, simple, rendered)



def parse_decl(decl, ctx: Ctx) -> list[Decl]:
    child = decl.children[0]
    if child.data == 'decl_fn':
        return parse_decl_fn(child, ctx)
    elif child.data == 'decl_class':
        return parse_decl_class(child, ctx)
    elif child.data == 'decl_class_fw':
        return []
    elif child.data == 'decl_mem':
        # handled in ctx
        return []
    elif child.data == 'decl_ns':
        return parse_decl_ns(child, ctx)
    elif child.data == 'decl_enum':
        enum = parse_decl_enum(child, ctx)
        ctx.add_enum(enum)
        return []
    elif child.data == 'decl_oper':
        return parse_decl_oper(child, ctx)
    else:
        body = 'not implemented {} {}'.format(child.data, get_linenumber())
        print(body)
        decl = Decl('not_implemented', [], '', [])
        return [decl]

def render_fns(decls: list[Decl], ctx: Ctx):
    res = []

    enums = [enum.rendered for enum in ctx._enums]

    res.append("\n".join(enums))

    for decl in decls:
        qname = decl.qname
        if len(qname) == 1:
            n = qname[0]
            if n == 'main':
                args = []
            else:
                args = [arg.name for arg in decl.args]
            block = "def {}({}):\n".format(n, ", ".join(args)) + indent(decl.body)
            res.append(block)

    if ctx._has_main:
        res.append('if __name__ == "__main__":\n    main()\n')

    return "\n\n".join(res) + "\n\n"

def render_classes(decls, ctx: Ctx):
    classnames = []
    decl: Decl
    for decl in decls:
        qname = decl.qname
        classname = qname[0]
        if len(qname) == 2 and classname not in classnames:
            classnames.append(classname)

    classes = []
    for c in classnames:
        res = []
        for decl in decls:
            qname = decl.qname
            if len(qname) == 2 and qname[0] == c:
                n = qname[1]
                if n == c:
                    n = "__init__"

                is_static = False
                try:
                    is_static = 'static' in ctx._methods_attrs[qname[0]][qname[1]]
                except KeyError:
                    pass

                arg0 = 'cls' if is_static else 'self'

                arg_names = [arg0] + [arg.name for arg in decl.args]
                
                super_arg_names = [arg.name for arg in decl.args]

                if n == "__init__" and len(arg_names) > 0 and arg_names[-1] == "parent":
                    arg_names[-1] = "parent = None"

                body = decl.body
                if n == '__init__':
                    body = "super().__init__({})\n".format(", ".join(super_arg_names)) + body

                if body == '':
                    body = 'pass'

                block = "def {}({}):\n".format(n, ", ".join(arg_names)) + indent(body) + "\n"
                if is_static:
                    block = '@classmethod\n' + block
                res.append(block)

        inh = ctx.inh(c)
        if len(inh) > 0:
            inh_ = "(" + inh[0] + ")"
        else:
            inh_ = ""

        signals = [signal.rendered for signal in ctx._signals[c]]
        if len(signals):
            signals = indent("\n".join(signals)) + "\n\n"
        else:
            signals = ""
        
        enums = [enum.rendered for enum in ctx._class_enums[c]]
        if len(enums) == 0:
            enums = ""
        else:
            enums = indent("\n".join(enums)) + "\n"

        classes.append("class {}{}:\n\n".format(c, inh_) + signals + enums + "\n".join([indent(item) for item in res]))
    return "\n".join(classes) + "\n"


base = os.path.dirname(__file__)
path = os.path.join(base, "cpp.lark")
with open(path, encoding='utf-8') as f:
    GRAMMAR = f.read()

def main():
    parser = argparse.ArgumentParser(prog='seapeapea', description='transpiles c++ into python')
    parser.add_argument("src", nargs="+", help="cpp files")
    parser.add_argument("-I", "--include", action='append', help="includepath")
    parser.add_argument("-o", "--output", help="output")
    parser.add_argument("-p", "--preprocessed", help="path to save preprocessed")
    parser.add_argument("-m", "--map", help="save map for side by side")
    parser.add_argument("--no-imports", action="store_true", help="do not add imports")
    parser.add_argument("--qt", choices=['pyqt5', 'pyside2'], help="python qt library")
    parser.add_argument("--time", action="store_true", help='print time stat')

    args = parser.parse_args()
    #print(args); exit()

    #print([os.path.abspath(path) for path in args.src], file=sys.stderr)
    
    t1 = time.time()
    parser = Lark(GRAMMAR, keep_all_tokens=True)
    t2 = time.time()
    if args.time:
        print("parser init in {:.3f}s".format(t2 - t1), file=sys.stderr)

    paths = []
    for path in args.src:
        if glob.has_magic(path):
            paths += glob.glob(path)
        else:
            paths.append(path)

    main = [item for item in paths if os.path.basename(item) == 'main.cpp']

    other = [item for item in paths if os.path.basename(item) != 'main.cpp']

    paths = other + main

    preprocessor = Preprocessor(args.include)
    code = preprocessor.read(paths)

    if args.preprocessed:
        with open(args.preprocessed, "w", encoding="utf-8") as f:
            f.write(code)

    t1 = time.time()
    tree = parser.parse(code)
    t2 = time.time()
    if args.time:
        print("code parsed in {:.3f}s".format(t2 - t1), file=sys.stderr)

    decls = []
    stats = []
    preprs = []

    ctx = Ctx(code)

    t1 = time.time()
    for child in tree.children:
        res = []
        if child.data == 'decl':
            for item in parse_decl(child, ctx):
                decls.append(item)
        elif child.data == 'stat':
            stats.append(parse_stat(child, ctx))
        elif child.data == 'prepr':
            pass
        else:
            raise Exception("not implemented")

    if args.no_imports:
        imports = ''
    else:
        imports = ctx.render_imports(args.qt)

    text = imports + render_classes(decls, ctx) + render_fns(decls, ctx)
    t2 = time.time()
    #print("result rendered in {:.3f}s".format(t2 - t1), file=sys.stderr)

    if args.output:
        file = open(args.output, "w", encoding='utf-8')
    else:
        file = sys.stdout
    file.write(text)
    if args.output:
        file.close()

    if args.map:
        with open(args.map, "w", encoding='utf-8') as f:
            json.dump(ctx._map, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
