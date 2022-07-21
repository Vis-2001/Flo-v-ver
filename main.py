import sys
import subprocess

from traverse import *

#os.system('gcc eps.c')
#epsilon = os.system('./a.out', shell = True)
#os.system('rm a.out')
#epsilon = sys.float_info.epsilon


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        filename = 'test.c'

    v = Verify(filename)
    v.analyze_fn('main')
