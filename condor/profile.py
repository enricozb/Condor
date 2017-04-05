import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        s = '%s function took %0.3f ms' % (f.__name__, (time2 - time1) * 1000)
        print(s)
        return ret
    wrap.__name__ = f.__name__
    return wrap
