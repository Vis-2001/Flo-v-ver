loop_break = 2000
loop_en = True

verbose = False

def logprint(*args, **kwargs):
    print(*args, **kwargs)

def l_print(*args, **kwargs):
    if loop_en:
        print(*args, **kwargs)

def loop_print(*args, **kwargs):
    if loop_en:
        print(*args, **kwargs)

def verbose_print(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)
