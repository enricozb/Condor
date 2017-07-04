from condor.c.condor import *

def begin():
    import __main__, inspect

    allowed_funcs = ['setup', 'draw']

    funcs = inspect.getmembers(__main__, inspect.isfunction)
    funcs = {name : f for name, f in funcs if name in allowed_funcs}

    setup_funcs(funcs)
    begin_c()

