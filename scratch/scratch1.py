import inspect

import dec

print(dec.counter)

from func import func
from func1 import func1


print(dec.counter)
#print(inspect.getsource(func))

print(func(1,2))
print(func(1,2))
print(func1(1,2))
print(func1(1,2))

#print(func.__doc__)
print(dec.counter)


