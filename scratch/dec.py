from functools import wraps

counter = 0

def dec(f):
    globals()['counter'] += 1
    @wraps(f)
    def newfunc(*args, **kwargs):
        r = f(*args, **kwargs)
        print('dec printing during execution ... ' + str(globals()['counter']))
        return r
    print('dec printing during definition ... ' + str(globals()['counter']))
    return newfunc
