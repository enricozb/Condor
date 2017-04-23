import time as clock

def timing(f):
    def wrap(*args):
        time1 = clock.time()
        ret = f(*args)
        time2 = clock.time()
        s = '%s function took %0.3f ms' % (f.__name__, (time2 - time1) * 1000)
        print(s)
        return ret
    wrap.__name__ = f.__name__
    return wrap

def time(f):
    ''' Returns how long it took to run f in seconds'''
    time1 = clock.time()
    ret = f()
    time2 = clock.time()
    return (time2 - time1)

