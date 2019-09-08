import inspect
from functools import wraps

import dec

print(dec.counter)

@dec.dec
def func(a,b):
    """
    This is a func
    """
    # check if comments are included
    c = a  + b
    return c

print(dec.counter)

@dec.dec
def func1(a,b):
    """
    This is a func
    """
    # check if comments are included
    c = a  - b
    return c

print(dec.counter)
#print(inspect.getsource(func))

print(func(1,2))
print(func(1,2))
print(func1(1,2))
print(func1(1,2))

#print(func.__doc__)
print(dec.counter)

hdr = 'import dec\n\n'

open('func.py', 'w').write(hdr + inspect.getsource(func))
open('func1.py', 'w').write(hdr + inspect.getsource(func1))

