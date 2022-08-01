from pycparser import c_ast
from err import *

def cast(typ, val):
    if not isinstance(typ, str):
        typ = typ[0]
#    print('val = ',val,type(val), typ)
    if typ == 'float' and isinstance(val, int):
        val = BoundedFloat(val)
    elif typ == 'char' and isinstance(val, str):
        if len(val) == 1:
            val = ord(val)
    elif typ == 'int' and isinstance(val, BoundedFloat):
        val = int(val)
    return val


def loopterminate(table, node, iterval):
    pass

#[name, V, variable type, variable value, node info] OR [name, F, return type, argument list, body] OR [name, AR, type, [list], dimension]
class Table():
    def __init__(self, uscope = None):
        if isinstance(uscope, Table):
            self.__upperscope = uscope
        else:
            self.__upperscope = None
        self.__table = []

    def add_entry(self, node, arrindex = None):
        if isinstance(node, c_ast.Decl):
            if isinstance(node.type, c_ast.FuncDecl):
                pass
            elif isinstance(node.type, c_ast.TypeDecl):
                val = cast(node.type.type.names, eval_expr(node.init, self))
                self.__table.append([node.name,'V',node.type.type.names[0],val,node])

            elif isinstance(node.type, c_ast.ArrayDecl):
                array = []
                dimarr = []
                initref = node.init
                node = node.type
                while isinstance(node, c_ast.ArrayDecl):
                    val = eval_expr(node.dim, self)
                    if val is not None:
                        dimarr.append(val)
                    node = node.type
                if len(dimarr) != 0:
                    ldarr = [0 for x in range(dimarr[-1:][0])]
                    for dimension in dimarr[-2::-1]:
                        array = [ldarr.copy() for x in range(dimension)]
                        ldarr = array

                if initref is not None:      #add multidim init support
                    for item in initref:
                        array.append(cast(node.type.names, eval_expr(item, self)))
                if len(dimarr) != 0:
                    size = dimarr[0]
                    if len(array)>size:
                        array = array[:size]
                else:
                    size = len(array)
                while len(array)<size:
                    array.append(0)
                self.__table.append([node.declname, 'AR',node.type.names,array,dimarr])

            elif isinstance(node.type, c_ast.PtrDecl):
                pass

        elif isinstance(node, c_ast.FuncDef):
            self.__table.append([node.decl.name, 'F', node.decl.type.type.type.names, node.decl.type.args, node.body])

    def update_entry(self, node, new_val, index = None):   #takes ID/ArrayRef node as input
        if isinstance(node, c_ast.ArrayRef):
            index = [eval_expr(node.subscript, self)]
            node = node.name
            while isinstance(node, c_ast.ArrayRef):
                index.append(eval_expr(node.subscript, self))
                node = node.name
        for item in self.__table:
            if node.name == item[0]:
                if item[1] == 'V':
                    item[3] = cast(item[2],new_val)
                    return True
                elif item[1] == 'AR':
                    if index is not None:
                        if(len(index)>1):
                            elemref = item[3][index[0]]
                        else:
                            elemref = item[3]
                        for subscript in range(1, len(index)-1):
                            elemref = elemref[subscript]
                        elemref[index[-1]] = cast(item[2], new_val)
                        return True
        if self.__upperscope is None:
            return False
        return self.__upperscope.update_entry(node,new_val, index)

    def get_value(self, node, index = None):
        if isinstance(node, c_ast.ArrayRef):
            index = [eval_expr(node.subscript, self)]
            node = node.name
            while isinstance(node, c_ast.ArrayRef):
                index.append(eval_expr(node.subscript, self))
                node = node.name
        for item in self.__table:
            if node.name == item[0]:
                if item[1] == 'V':
                    return item[3]
                elif item[1] == 'AR':
                    if index is not None:
                        if(len(index)>1):
                            elemref = item[3][index[0]]
                        else:
                            elemref = item[3]
                        for subscript in range(1, len(index)-1):
                            elemref = elemref[subscript]
                        return elemref[index[-1]]
                else:
                    return 'Function'
        if self.__upperscope is None:
            return None
        return self.__upperscope.get_value(node, index)

    def get_type(self, node):
        for item in self.__table:
            if node.name == item[0] and (item[1] == 'V' or item[1] == 'AR'):
                return item[2]
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

    def show(self):
        space = ''
        if self.__upperscope is not None:
            space = self.__upperscope.show()
        for elem in self.__table:
            if elem[1] == 'V':
                print(space, elem[0], elem[2], elem[3])
            if elem[1] == "AR":
                print(space, elem[0], elem[2], elem[3], elem[4])
        return space + '--'




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

    elif isinstance(node, c_ast.UnaryOp):
        if isinstance(node.expr, c_ast.ID):
            if node.op == 'p++':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val+1)
                return val
            elif node.op == '++p' or '++':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val+1)
                return val+1
            elif node.op == 'p--':
                val = symb_table.get_value(node.expr)
                symb_table.update_entry(node.expr, val-1)
                return val
            elif node.op == '--p' or '--':
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


    elif isinstance(node, c_ast.TernaryOp):
        val = eval_expr(node.cond, symb_table)
        if val:
            return eval_expr(node.iftrue, symb_table)
        else:
            return eval_expr(node.iffalse, symb_table)

    elif isinstance(node, c_ast.Constant):
        if node.type == 'int':
            return int(node.value)
        elif node.type == 'float' or node.type == 'double':
            return BoundedFloat(node.value)
        elif node.type == 'string':
            return node.value
        elif node.type =='char':
            return ord(node.value.replace("'", ""))
    elif isinstance(node, c_ast.ID):
        val =  symb_table.get_value(node)
        if val is None:
            print('Variable',node.name,'not declared/not in scope at', node.coord)
            exit()
        return val
    elif isinstance(node, c_ast.FuncCall):
        return eval_fncall(node, symb_table)
    elif isinstance(node, c_ast.ArrayRef):
        return symb_table.get_value(node)

def eval_fncall(node, symb_table_og):
    symb_table = Table(symb_table_og)
    func_det = symb_table.get_func(node.name)
    if func_det is None:
        #print(node.name.name, 'not defined')
        return
    print('Function', node.name.name, end = '')
    if node.args is not None:
        print(' with args:')
        for arg in zip(func_det[3], node.args):
            arg[0].init = arg[1]
            symb_table.add_entry(arg[0])
            if isinstance(arg[1],c_ast.ID):
                print(f"    variable {arg[1].name} with value {symb_table.get_value(arg[1])}")
            else:
                val = eval_expr(arg[1], global_table)
                print(f"    constant of type {type(val).__name__} with value {val}")
    else:
        print(' with no args called')
    print()

    ret = eval_stat(func_det[4], symb_table)
    if isinstance(ret, tuple):
        ret = ret[1]
    ret = cast(func_det[2], ret)
#    print('Function', node.name.name, 'returns', ret)
    return ret


def eval_stat(node, symb_table, loop = None):
    caseft = 0
    if not isinstance(node, c_ast.Compound):
        node = c_ast.Compound([node])
    for statement in node.block_items:
        if isinstance(statement, c_ast.Compound):
            loopval = eval_stat(statement, Table(symb_table))
            if loopval == 'break' or loopval == 'continue' or isinstance(loopval, tuple):
                return loopval
        if isinstance(statement, c_ast.FuncCall):
            eval_fncall(statement, symb_table)
        if isinstance(statement, c_ast.Decl):
            symb_table.add_entry(statement)
        if isinstance(statement, c_ast.Return):
            val = eval_expr(statement.expr, symb_table)
            return ('return', val)
        if isinstance(statement, c_ast.Break):
            return 'break'
        if isinstance(statement, c_ast.Continue):
            return 'continue'
        if isinstance(statement, c_ast.UnaryOp):
            eval_expr(statement, symb_table)

        if isinstance(statement, c_ast.If):
            if eval_expr(statement.cond, symb_table):
                loopval = eval_stat(statement.iftrue, Table(symb_table))
            else:
                loopval = eval_stat(statement.iffalse, Table(symb_table))
            if loopval == 'break' or loopval == 'continue' or isinstance(loopval, tuple):
                return loopval


        if isinstance(statement, c_ast.While):
            runningloop = [statement.coord]
            looptbl = Table(symb_table)
            loopcount = 0
            loopval = None
            while eval_expr(statement.cond, looptbl):
                loopval = eval_stat(statement.stmt, looptbl)
                loopcount += 1
                if loopval == 'break' or  isinstance(loopval, tuple):
                    break
                if loopval == 'continue':
                    continue
                if (loopcount % 2000) == 0:       #rework
                    print('\nWARNING: Loop',statement.coord,'has run', loopcount, 'times.')
                    conf = input('Do you want to exit(y to exit)')
                    if conf == 'y':
                        break


            print("'While' loop at", statement.coord, "ran", loopcount, "times before exiting", end = '')
            if (loopcount%2000)!=0:
                print(' normally')
            else:
                print(', condition doesnt seem to hold')

            print()

            runningloop = []
            if isinstance(loopval, tuple):
                return loopval

        if isinstance(statement, c_ast.For):
            runningloop = [statement.coord]
            looptbl = Table(symb_table)
            loopcount = 0
            for decl in statement.init:
                looptbl.add_entry(decl)
            if isinstance(statement.next, list):
                next = [x for x in statement.next]
            else:
                next = [statement.next]
            next = c_ast.Compound(next)
            loopval = None
            while eval_expr(statement.cond, looptbl):
                loopval = eval_stat(statement.stmt, looptbl)
                loopcount += 1
                if loopval == 'break' or  isinstance(loopval, tuple):
                    break
                if loopval == 'continue':
                    continue
                if (loopcount % 2000) == 0:       #rework
                    print('\nWARNING: Loop',statement.coord,'has run', loopcount, 'times.')
                    conf = input('Do you want to exit(y to exit)')
                    if conf == 'y':
                        break
                eval_stat(next, looptbl)

            print("'For' loop at", statement.coord, "ran", loopcount, "times before exiting", end = '')
            if (loopcount%2000)!=0:
                print(' normally')
            else:
                print(', condition doesnt seem to hold')

            print()
            runningloop = []
            if isinstance(loopval, tuple):
                return loopval


        if isinstance(statement, c_ast.DoWhile):
            runningloop = [statement.coord]
            looptbl = Table(symb_table)
            loopcount = 1
            loopval = eval_stat(statement.stmt, looptbl)
            if loopval != 'break':
                while eval_expr(statement.cond, looptbl):
                    loopval = eval_stat(statement.stmt, looptbl)
                    loopcount += 1
                    if loopval == 'break' or  isinstance(loopval, tuple):
                        break
                    if loopval == 'continue':
                        continue
                    if (loopcount % 2000) == 0:       #rework
                        print('\nWARNING: Loop',statement.coord,'has run', loopcount, 'times.')
                        conf = input('Do you want to exit(y to exit)')
                        if conf == 'y':
                            break

            print("'Do-While' loop at", statement.coord, "ran", loopcount, "times before exiting", end = '')
            if loopcount%2000!=0:
                print(' normally')
            else:
                print(', condition doesnt seem to hold')

            print()
            runningloop = []
            if isinstance(loopval, tuple):
                return loopval


        if isinstance(statement, c_ast.Switch):
            val = eval_expr(statement.cond, symb_table)
            loopval = eval_stat(statement.stmt, Table(symb_table), val)
            if isinstance(loopval, tuple):
                return loopval
        if isinstance(statement, c_ast.Case):
            if loop is not None:
                if loop == eval_expr(statement.expr, symb_table) or caseft:
                    caseft = 1
                    stmt = c_ast.Compound([x for x in statement.stmts])
                    loopval = eval_stat(stmt, symb_table)
                    if loopval == 'break':
                        break
                    if isinstance(loopval, tuple):
                        return loopval
        if isinstance(statement, c_ast.Default):
            stmt = c_ast.Compound([x for x in statement.stmts])
            loopval = eval_stat(stmt, symb_table)
            if loopval == 'break':
                break
            if isinstance(loopval, tuple):
                return loopval


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
