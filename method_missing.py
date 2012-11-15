"""
This is an example of something similar to method_missing in Ruby
"""

from functools import partial, wraps


def make_getattribute(old_func):
    if old_func is None:
        old_func = object.__getattribute__

    def new_getattribute(self, name):
        try:
            val = old_func(self, name)
            return val
        except AttributeError as e1:
            try:
                missing_attr = old_func(self, 'method_missing')
            except AttributeError as e2:
                raise e1

            return partial(missing_attr, name)

    return new_getattribute

class MissingMetaclass(type):
    def __new__(meta, classname, bases, classdict):
        old_getattribute = classdict.get('__getattribute__')
        classdict['__getattribute__'] = make_getattribute(old_getattribute)

        return type.__new__(meta, classname, bases, classdict)


# Example
class WithMethodMissing(object):
    __metaclass__ = MissingMetaclass

    def method_missing(self, name, *args, **kwargs):
        print("Tried to call '%s' with args '%r' and kwargs '%r'" % (name, args, kwargs))
        return 'missing value'

    def not_missing(self):
        return 123


m = WithMethodMissing()
print(repr(m))
print(m.not_missing())
print(m.missing(1,2,three=4))

