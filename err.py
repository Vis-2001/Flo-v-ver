import sys
from z3 import *
from decimal import Decimal
import log


epsilon = RealVal(sys.float_info.epsilon)
dela = RealVal(simplify(epsilon/2))
delr = RealVal(0)
#delr=RealVal(0.000049948692321777343750000000)
#dela=RealVal(0.000000119209289550781250000000)

def setp(presc):
    set_option(precision=presc,rational_to_decimal=True)

def z3zero(v1,v2):
    if (str(simplify(v1-v2))=='0'):
        return True
    else:
        return False

def z3max(v1,v2):
    if(str(simplify(v1-v2))[0]=='-'):
        return [v2, True]
    else:
        return [v1, False]

def error(val):
    return z3max(simplify(delr*val),dela)[0]

def get_max(lst):
    max = None
    for item in lst:
        if max is None or z3max(max,item)[1]:
            max = item
    return item

def get_min(lst):
    min = None
    for item in lst:
        if min is None or not z3max(min,item)[1]:
            min = item
    return item

class BoundedFloat():
    def __init__(self,val = None,fval = None,ulmt = None, llmt = None):  #Redefine ctr
        if val == None:
            self.real = None
            self.flt = None
            self.err = None
            self.bounds = [0,0]
            return

        self.real = RealVal(val)
        if isinstance(val, str):
            if '.' in val:
                val = float(val)
            else:
                val = int(val)

        self.flt=val
        self.err = simplify(self.real-RealVal(Decimal(self.flt)))
        if z3zero(self.err, RealVal(0)):
            self.err = error(val)  #fix function
        self.bounds = [0,0]

        if llmt is None:
            if isinstance(val, float):
                self.bounds[0] = simplify(self.real-self.err)
            elif isinstance(val, int):
                self.bounds[0] = RealVal(val)
                self.err = RealVal(0)
        else:
            if isinstance(llmt, RealVal):
                self.bounds[0] = llmt
            else:
                self.bounds[0] = RealVal(llmt)
        if ulmt is None:
            if isinstance(val, float):
                self.bounds[1] = simplify(self.real+self.err)
            elif isinstance(val, int):
                self.bounds[1] = RealVal(val)
                self.err = RealVal(0)
        else:
            if isinstance(ulmt, RealVal):
                self.bounds[1] = ulmt
            else:
                self.bounds[1] = RealVal(ulmt)


    def __str__(self):
        if log.verbose:
            return "{0}\nFloat value:{1}\nReal value: {2}\nBounds:{3}\nError:{4}".format(self.flt, Decimal(self.flt), self.real, self.bounds,self.err)
        else:
            return str(self.flt)
    def __add__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        new = BoundedFloat()
        new.real = simplify(self.real + other.real)
        new.flt = self.flt + other.flt
        new.bounds = [simplify(self.bounds[0] + other.bounds[0]), simplify(self.bounds[1] + other.bounds[1])]
        new.err = simplify(self.err+other.err)
        return new

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        new = BoundedFloat()
        new.real = simplify(self.real - other.real)
        new.flt = self.flt - other.flt
        new.bounds = [simplify(self.bounds[0] - other.bounds[0]), simplify(self.bounds[1] - other.bounds[1])]
        new.err = simplify(self.err-other.err)
        return new

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        new = BoundedFloat()
        new.real = simplify(self.real*other.real)
        new.flt = self.flt * other.flt
        set = [simplify(self.bounds[0]*other.bounds[0]),simplify(self.bounds[1]*other.bounds[0]),simplify(self.bounds[0]*other.bounds[1]),simplify(self.bounds[1]*other.bounds[1])]
        new.bounds = [get_min(set), get_max(set)]
        new.err = simplify(RealVal(new.flt)-new.real)
#        new.err = simplify(self.err + self.err*RealVal(other.flt)+ other.err*RealVal(self.flt)) #fix
        return new

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        new = BoundedFloat()
        new.real = simplify(self.real/other.real)
        new.flt = self.flt / other.flt
        set = [simplify(self.bounds[0]/other.bounds[0]),simplify(self.bounds[1]/other.bounds[0]),simplify(self.bounds[0]/other.bounds[1]),simplify(self.bounds[1]/other.bounds[1])]
        new.bounds = [get_min(set), get_max(set)]
        new.err = simplify(RealVal(new.flt)-new.real)
#        new.err = simplify(self.err + self.err/RealVal(other.flt) + RealVal(self.flt)/other.err) #fix
        return new

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __eq__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        if self.flt == other.flt:
            if not z3zero(self.real, other.real):
                log.l_print()
                log.l_print('LHS: ', self)
                log.l_print('RHS: ', other)
                log.l_print('Operator: ==')
                log.l_print('WARNING: Float equal, Real unequal, branch taken, possible issue\n')
            return True
        else:
            if z3zero(self.real, other.real):
                log.l_print()
                log.l_print('LHS: ', self)
                log.l_print('RHS: ', other)
                log.l_print('Operator: ==')
                log.l_print('WARNING: Float unequal, Real equal, branch not taken, possible issue\n')
            return False

    def __ne__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        if self.flt != other.flt:
            if z3zero(self.real, other.real):
                log.l_print()
                log.l_print('LHS: ', self)
                log.l_print('RHS: ', other)
                log.l_print('Operator: !=')
                log.l_print('WARNING: Float unequal, Real equal, branch taken, possible issue\n')
            return True
        else:
            if not z3zero(self.real, other.real):
                log.l_print()
                log.l_print('LHS: ', self)
                log.l_print('RHS: ', other)
                log.l_print('Operator: !=')
                log.l_print('WARNING: Float equal, Real unequal, branch not taken, possible issue\n')
            return False


    def __lt__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        if self.flt > other.flt:
            return True
        else:
            return False

    def __le__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        if self.flt >= other.flt:
            return True
        else:
            return False

    def __ge__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        if self.flt <= other.flt:
            return True
        else:
            return False

    def __gt__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        if self.flt < other.flt:
            return True
        else:
            return False

    def __int__(self):
        nval = int(self.flt)
        return nval  #fix

    def __float__(self):
        return self


if __name__ == "__main__":
    s1= BoundedFloat(22.3)
    s2 = BoundedFloat(7.2)
    print(s1, '\n')
    print(s2, '\n')
    print(s1+s2*3.4)
