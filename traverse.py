from pycparser import c_ast, parse_file
from err import *
from eval import *
import log
class NodeVisitor(object):
    _method_cache = None

    def visit(self, node, global_table):
        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node, global_table)

    def generic_visit(self, node, global_table):
        for c in node:
            self.visit(c, global_table)

class NodeCollector(NodeVisitor):
    def visit_Decl(self, node, global_table):
        if type(node.type) == c_ast.FuncDecl:
            log.logprint('Function %s with return type %s declared at at %s' % (node.name, node.type.type.type.names, node.coord))
            global_table.add_entry(node)
        else:
            val = eval_expr(node.init, global_table)
            log.logprint('Global variable %s with value %s declared at at %s' % (node.name, val, node.coord))
            global_table.add_entry(node)
        log.logprint()

    def visit_FuncDef(self, node, global_table):
        log.logprint('Function %s with return type %s defined at %s' % (node.decl.name, node.decl.type.type.type.names, node.decl.coord))
        log.logprint()
        global_table.add_entry(node)
        for stmt in node.body.block_items or []:
            if isinstance(stmt, c_ast.FuncCall):
                log.verbose_print(f"Function {node.decl.name} calls {stmt.name.name} with ", end = '')
                if stmt.args is None:
                    log.verbose_print('no arguments')
                else:
                    log.verbose_print('argument(s):')
                    for arg in stmt.args:
                        if isinstance(arg,c_ast.ID):
                            log.verbose_print(f"    variable {arg.name} ")
                        else:
                            val = eval_expr(arg, global_table)
                            log.verbose_print(f"    constant of type {type(val).__name__} with value {val}")
                log.verbose_print()
        log.verbose_print()

class Verify():
    def __init__(self, filename):
        self.ast = parse_file(filename, use_cpp=True,
                         cpp_args=r'-Iutils/fake_libc_include')
        self.global_table = Table()

    def disp_fn(self):
        v = NodeCollector()
        v.visit(self.ast, self.global_table)

    def analyze_fn(self, fname = None, args = None, showtree = None):
        if fname is None or fname == '':
            fname = 'main'

        if showtree is True:
            self.ast.show(nodenames = True)

        arglst = None
        if args is not None:
            arglst = []
            for arg in args:
                arglst.append(c_ast.Constant(['double'], arg))
        fcnode = c_ast.FuncCall(c_ast.ID(fname),arglst)

        if self.global_table.isempty():
            self.disp_fn()

        log.logprint('Starting evaluation of function', fname)
        fret = eval_fncall(fcnode, self.global_table)
        temp = log.verbose
        log.verbose = True
        log.logprint('Return value of function',fname,'=', fret)
        log.verbose = temp
