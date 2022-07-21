import sys

#epsilon = sys.float_info.epsilon
epsilon = 0.1

class BoundedFloat():
    def __init__(self,val, ulmt = None, llmt = None):  #fix bound generation
        self.val=val
        if isinstance(val, str):
            val = ord(val)
        if isinstance(val, int):
            if llmt is None:
                self.val_l = val
            else:
                self.val_l = llmt
            if ulmt is None:
                self.val_u = val
            else:
                self.val_u = ulmt
        elif isinstance(val, float):
            if llmt is None:
                self.val_l = self.val-epsilon
            else:
                self.val_l = llmt
            if ulmt is None:
                self.val_u = self.val+epsilon
            else:
                self.val_u = ulmt

    def __str__(self):
        return "{0} [{1}, {2}]".format(self.val, self.val_l, self.val_u)

    def __add__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        nval = self.val + other.val
        nu = self.val_u + other.val_u
        nl = self.val_l + other.val_l
        return BoundedFloat(nval, nu, nl)

    def __sub__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        nval = self.val - other.val
        nu = self.val_l - other.val_u
        nl = self.val_u - other.val_l
        return BoundedFloat(nval, nu, nl)

    def __mul__(self, other):
        if not isinstance(other, BoundedFloat):
            other = BoundedFloat(other)
        nval = self.val * other.val
        nu = max(self.val_l*other.val_l,self.val_u*other.val_l,self.val_l*other.val_u,self.val_u*other.val_u)
        nl = min(self.val_l*other.val_l,self.val_u*other.val_l,self.val_l*other.val_u,self.val_u*other.val_u)
        return BoundedFloat(nval, nu, nl)


if __name__ == "__main__":
    s1= BoundedFloat(5.4, 5.3, 5.5)
    s2 = BoundedFloat(4.5, 4.4, 4.6)
    print(s1-s2)
