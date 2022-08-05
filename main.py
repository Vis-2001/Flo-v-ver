import argparse
import json
import time


from traverse import *
import log
import err

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        filename = 'test.c'
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="Command list: 'show' to display global variables and defined functions, 'run' to profile function given by 'file'(default file:test.c, default function:main) 'q'/'exit' for quit")
    parser.add_argument("file", help="Input file, not much to describe(default = test.c)", metavar = '<filename>', nargs = '?', default = 'test.c')
    parser.add_argument("-f","--fname", help = "Name of function to be analyzed(default = main)", default = 'main')
    parser.add_argument("--args", help = "Arguments for input function, if necessary", metavar = '<arg1>,<arg2>...', nargs = '+', default = None)
    parser.add_argument("-p","--precision", help="Float precision setting for Z3, number of decimal places in the real number", metavar = 200, type = int, default = 200)
    parser.add_argument("-li", help = "Number of loop iterations before break", metavar = 200, type = int, default = 200 )
    parser.add_argument("-l", help="Loop debug enable", action='store_true')
    parser.add_argument("-v", help="Verbose", action='store_true')
    parser.add_argument("--showtree", help = "Show AST for file", action = 'store_true')

    print("Flo(v)ver\nPES Innovation Lab, PES Univerity, 2022\n\nFor help, type '-h' or '--help'")
    currfname = None
    while True:
        try:
            inp = input('>>').strip().split()
        except EOFError:
            sys.stdout.write('\n')
            break
        try:
            args = parser.parse_args(inp)
        except SystemExit:
            continue
        if args.cmd == 'q' or args.cmd == 'exit':
            print('Quit')
            break
        if currfname != args.file or currfname is None:
            v = Verify(args.file)
        err.setp(args.precision)
#        print(args)
        log.verbose = args.v
        log.loop_break = args.li
        log.loop_en = args.l
        if args.cmd == 'show':
            v.disp_fn()

        if args.cmd == 'run':
            start = time.time()
            v.analyze_fn(args.fname, args = args.args, showtree = args.showtree)
            print()
            print("Time elapsed: ", (time.time()-start)*1000,"ms")
