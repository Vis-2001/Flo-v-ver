from pycparser import c_ast
from err import *

def cast(type, val):
    if type == 'float':
        val = float(val)
    elif type == 'char':
        if len(val) == 1 and isinstance(val, str):
            val = ord(val)
    elif type == 'int':
        val = int(val)
    return val



class Table():   #[name, V, variable type, variable value, node info] OR [name, F, return type, argument list, body]
    __table = []
    __upperscope = None
    def __init__(self, uscope = None):
        if isinstance(uscope, Table):
            self.__upperscope = uscope


    def add_entry(self, node):
        if isinstance(node, c_ast.Decl):
            if isinstance(node.type, c_ast.FuncDecl):
                pass
            elif isinstance(node.type, c_ast.TypeDecl):
                val = cast(node.type.type.names, eval_expr(node.init, self))
                self.__table.append([node.name,'V',node.type.type.names,val,node])
        elif isinstance(node, c_ast.FuncDef):
            self.__table.append([node.decl.name, 'F', node.decl.type.type.type, node.decl.type.args, node.body])



    def update_entry(self, node, new_val):                  #takes ID node as input
        for item in self.__table:
            if node.name == item[0] and item[1] == 'V':
                item[3] = cast(item[2],item[3])
                return True
        if self.__upperscope is None:
            return False
        return self.__upperscope.update_entry(node,new_val)

    def get_value(self, node):
        for item in self.__table:
            if node.name == item[0] and item[1] == 'V':
                return item[3]
        if self.__upperscope is None:
            return None
        return self.__upperscope.get_value(node)

    def get_func(self, node):
        if self.__upperscope is None:
            for item in self.__table:
                if node.name == item[0] and item[1] == 'F':
                    return item
            return None
        return self.__upperscope.get_func(node)



global_table = Table()




def eval_expr(node, symb_table):
    if node is None:
        return None
    if isinstance(node, c_ast.BinaryOp):
        left = eval_expr(node.left, symb_table)
        right = eval_expr(node.right, symb_table)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '%':
            return left % right
        elif node.op == '&&':
            return left and right
        elif node.op == '-':
            return left - right
        elif node.op == '||':
            return left or right
        elif node.op == '&':
            return left & right
        elif node.op == '|':
            return left | right
        elif node.op == '^':
            return left ^ right
        elif node.op == '<<':
            return left << right
        elif node.op == '>>':
            return left >> right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '==':
            return left == right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == '!=':
            return left != right
        else:
            return None

    if isinstance(node, c_ast.UnaryOp):
        if isinstance(node.expr, c_ast.ID):
            if node.op == 'p++':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val+1)
                return val
            elif node.op == '++p':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val+1)
                return val+1
            elif node.op == 'p--':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val-1)
                return val
            elif node.op == '--p':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val-1)
                return val-1
        val = eval_expr(node.expr,symb_table)
        if node.op == 'p++' or node.op == '++p':
            return val+1
        elif node.op == 'p--' or node.op == '--p':
            return val-1
        elif node.op == '~':
            return ~val
        elif node.op == '!':
            return not val

    if isinstance(node, c_ast.TernaryOp):
        val = eval_expr(node.cond, symb_table)
        if val:
            return eval_expr(node.iftrue, symb_table)
        else:
            return eval_expr(node.iffalse, symb_table)

    if isinstance(node, c_ast.Constant):
        if node.type == 'int':
            return int(node.value)
        elif node.type == 'float' or node.type == 'double':
            return BoundedFloat(float(node.value))
        elif node.type == 'string':
            return node.value
    if isinstance(node, c_ast.ID):
        return symb_table.get_value(node)
    if isinstance(node, c_ast.FuncCall):
        return eval_fncall(node, symb_table)

def eval_fncall(node, symb_table):
    symb_table = Table(symb_table)
    func_det = symb_table.get_func(node.name)
    if func_det is None:
        print(node.name.name, 'not defined')
        return
    if node.args is not None:
        for arg in zip(func_det[3], node.args):
            arg[0].init = arg[1]
            symb_table.add_entry(arg[0])
    return eval_stat(func_det[4], symb_table)

def eval_stat(node, symb_table):
    if not isinstance(node, c_ast.Compound):
        return
    for statement in node.block_items:
        if isinstance(statement, c_ast.Compound):
            eval_stat(statement, Table(symb_table))
        if isinstance(statement, c_ast.FuncCall):
            eval_fncall(statement, symb_table)
        if isinstance(statement, c_ast.Decl):
            symb_table.add_entry(statement)
        if isinstance(statement, c_ast.Return):
            return eval_expr(statement.expr, symb_table)
        if isinstance(statement, c_ast.Assignment):
            rval = eval_expr(statement.rvalue,symb_table)
            if statement.op == '=':
                symb_table.update_entry(statement.lvalue, rval)
            elif statement.op =='*=':
                symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)*rval)
            elif statement.op =='/=':
                symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)/rval)
            elif statement.op =='+=':
                symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)+rval)
            elif statement.op =='-=':
                symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)-rval)
            elif isinstance(rval, int):
                if statement.op =='%=':
                    symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)%rval)
                elif statement.op =='<<=':
                    symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)<<rval)
                elif statement.op =='>>=':
                    symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)>>rval)
                elif statement.op =='&=':
                    symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)&rval)
                elif statement.op =='|=':
                    symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)|rval)
                elif statement.op =='^=':
                    symb_table.update_entry(statement.lvalue, symb_table.get_value(statement.lvalue)^rval)
