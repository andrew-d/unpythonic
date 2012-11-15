"""
Inject variables into a function's scope.
"""

from types import FunctionType
from functools import update_wrapper, wraps

# Injects some variables into a function, returns a new function with the
# variables injected.
def injector(to_inject):
    def inject_to(func):
        new_globals = dict(func.func_globals)
        new_globals.update(to_inject)

        new_func = FunctionType(func.func_code, new_globals)
        return update_wrapper(new_func, func)
    return inject_to


inj = {"x": 1, "y": 2}
@injector(inj)
def my_func():
    print x + y


# This should print "3".
my_func()


# Injects "self" into the globals of all functions in a class.
def inject_self(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Create a new function object with the new globals.
        new_globals = func.func_globals.copy()
        new_globals['self'] = self

        new_func = FunctionType(func.func_code, new_globals)
        return new_func(*args, **kwargs)

    return wrapper

class InjectingMetaclass(type):
    def __new__(meta, classname, bases, classdict):
        for item in classdict:
            if hasattr(classdict[item], '__call__'):
                classdict[item] = inject_self(classdict[item])

        return type.__new__(meta, classname, bases, classdict)


# Example
class HasSelfInjected(object):
    __metaclass__ = InjectingMetaclass

    value = 'foobar'

    def func_one():
        print self.value

    def func_two(val):
        self.value = val


ob = HasSelfInjected()
ob.func_one()               # Should print: foobar
ob.func_two('asdf')
ob.func_one()               # Should print: asdf

