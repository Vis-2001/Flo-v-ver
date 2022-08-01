from pycparser import c_ast, parse_file
from err import *
from eval import *

class NodeVisitor(object):
    _method_cache = None

    def visit(self, node):
        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node):
        for c in node:
            self.visit(c)

class NodeCollector(NodeVisitor):
    def visit_Decl(self, node):
        if type(node.type) == c_ast.FuncDecl:
            print('Function %s with return type %s declared at at %s' % (node.name, node.type.type.type.names, node.coord))
            global_table.add_entry(node)
        else:
            val = eval_expr(node.init, global_table)
            print('Global variable %s with value %s declared at at %s' % (node.name, val, node.coord))
            global_table.add_entry(node)
        print()

    def visit_FuncDef(self, node):
        print('Function %s with return type %s defined at %s' % (node.decl.name, node.decl.type.type.type.names, node.decl.coord))
        #print('Syntax tree: ')
        #node.show()
        print()
        global_table.add_entry(node)
        for stmt in node.body.block_items or []:
            if isinstance(stmt, c_ast.FuncCall):
                print (f"Function {node.decl.name} calls {stmt.name.name} with ", end = '')
                if stmt.args is None:
                    print('no arguments')
                else:
                    print('argument(s):')
                    for arg in stmt.args:
                        if isinstance(arg,c_ast.ID):
                            print(f"    variable {arg.name} ")
                        else:
                            val = eval_expr(arg, global_table)
                            print(f"    constant of type {type(val).__name__} with value {val}")
                print()
        print()

class Verify():
    def __init__(self, filename):
        self.ast = parse_file(filename, use_cpp=True,
                         cpp_args=r'-Iutils/fake_libc_include')

    def analyze_fn(self, fname = 'main', args = None, showtree = None):
        if fname is None or fname == '':
            fname = 'main'
        v = NodeCollector()
        if showtree is None:
            self.ast.show()
        else:
            self.ast.show(nodenames = True)
        v.visit(self.ast)
        arglst = None
        if args is not None:
            arglst = []
            for arg in args:
                arglst.append(c_ast.Constant(type(arg), arg))
        fcnode = c_ast.FuncCall(c_ast.ID(fname),arglst)
        print('Return value of function',fname,'=', eval_fncall(fcnode, global_table))
