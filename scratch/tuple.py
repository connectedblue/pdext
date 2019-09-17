from collections import namedtuple

import inspect

x={'a':1,'b':2, 'c':3}
y={'d':4,'e':5, 'f':6}
z={'g':7,'h':8, 'i':9}


def d2t(x):
    return namedtuple('test',' '.join(x.keys()))(**x)

d2t(x)

a={'x': x, 'y': y, 'z': z}

b=d2t({k:d2t(v) for k,v in a.items()})

class Test(object):
    def __getattr__(self, func):
        # if func in a.keys():
        #     collection = func
        #     yield Test
        #     return a[collection][func]
        print(inspect.stack())

t = Test()