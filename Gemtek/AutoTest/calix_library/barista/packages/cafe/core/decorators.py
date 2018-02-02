"""Collections of cafe framework decorator(s)

This modules contains decorators which are useful for Cafe API development

"""
from functools import wraps, update_wrapper
from inspect import getargspec, isfunction, currentframe, getframeinfo
from itertools import izip, ifilter, starmap
import gc
import resource
import os
import sys

__author__ = 'kelvin'

try:
    import objgraph
except ImportError:
    sys.__stderr__.write("Error: python package 'objgraph' is required. please do '/opt/ActivePython2/bin/pip2 install objgraph'")
    exit(1)

try:
    import psutil
except ImportError:
    sys.__stderr__.write("Error: python package 'psutil' is required. please do '/opt/ActivePython2/bin/pip2 install psutil'")
    exit(1)

#
# Use python builtin variable __debug__ to turn on/off the debug print
# __debug__ is True by default.
# use command line "-O" option to change __debug__ to False
#
_is_debug_off = __debug__


def debug(s):
    """debug print for this module
    """

    if not _is_debug_off:
        if isinstance(s, str):
            for _s in s.splitlines():
                sys.__stdout__.write("*** debug ***: " + _s + "\n")
        if isinstance(s, (list, tuple)):
            for _s in s:
                sys.__stdout__.write("*** debug ***: " + str(_s) + "\n")


class mem_debug(object):
    """
    decorator - print python memory/cpu/leak-objects debug information which a
    function is called
    This decorator is enabled/disabled by "-O" flag of python command line interface

    Example:
    >>> @mem_debug()
    >>> def func():
            pass

    >>> func()
    >>> #sample printout
    >>> #Remaining Garbage: []
    >>> #   *** debug ***:
    >>> #   *** debug ***: callable ==> func
    >>> #   *** debug ***: gc information ........
    >>> #   *** debug ***: 	--Unreachable objects: 582
    >>> #   *** debug ***: 	--Remaining Garbage:
    >>> #   *** debug ***: memory information ........
    >>> #   *** debug ***: 	--process pid=9385 : memory usage 53508 KBytes
    >>> #   *** debug ***: 	--number of objects: 53873
    >>> #   *** debug ***: objgraph information .......
    >>> #   *** debug ***: 	--number of leak objects 1299
    >>> #   *** debug ***:
    >>> #   *** debug ***: Shutdown list size 0
    >>> #   *** debug ***:
    >>> #   *** debug ***: Number of opened file descriptor for this process 9385: 1
    >>> #   *** debug ***: Memory usage of this process 9385: pmem(rss=49770496, vms=409833472, shared=2719744, text=1372160, lib=0, data=200257536, dirty=0)
    >>> #   *** debug ***: CPU usage of this process 9385: 0.0
    """
    def __init__(self, title=""):
        """
        """
        self.log_func = debug
        self.title = title

    def __call__(self, func):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)

            if not _is_debug_off:
                if self.title:
                    self.log_func("mem info -- %s --" % (self.title, ))
                self.log_func("\ncallable ==> %s %s" % (func.__module__, func.__name__,))
                self.log_func("gc information ........")

                #need to gc so that the rest of debug printout is accurate
                n = gc.collect()
                self.log_func("")
                self.log_func("\t--Unreachable objects: %s" % str(n))
                self.log_func("\t--Remaining Garbage:")
                self.log_func(gc.garbage)
                del gc.garbage[:]

                #
                self.log_func("")
                self.log_func("memory information ........")
                self.log_func("\t--process pid=%d : memory usage %s KBytes" %
                              (os.getpid(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
                self.log_func("\t--number of objects: %d" % len(gc.get_objects()))
                self.log_func("")

                self.log_func("objgraph information .......")
                objgraph.show_growth()
                roots = objgraph.get_leaking_objects()
                #python itself has ~1000 leak objects internally
                self.log_func("\t--number of leak objects %d " % len(roots))

                import shutdown
                self.log_func("")
                self.log_func('\nShutdown list size %d' % len(shutdown._Shutdown().get_shutdown_list()))

                proc = psutil.Process()
                self.log_func('\nNumber of opened file descriptor for this process %d: %d' %
                              (proc.pid, len(proc.open_files())))
                self.log_func('Memory usage of this process %s: %s' %
                              (proc.pid, str(proc.memory_info())))
                self.log_func('CPU usage of this process %d: %s' %
                              (proc.pid, str(proc.cpu_percent())))


            return ret
        return wrapper


def add_prefix(prefix):
    """
    Decorator function to add prefix to all public methods (methods that not start with "_")

        Usage:
            @aliased("prefix")
            class MyClass(object):
                def boring_method():
                    # ...

            i = MyClass()
            i.prefix_boring_method() # equivalent i.boring_method()
    """

    def wrap(aliased_class):

        original_methods = aliased_class.__dict__.copy()

        for name, method in original_methods.iteritems():

            if name[0] is not "_":
                alias = prefix + "_" + name
                setattr(aliased_class, alias, method)

        return aliased_class

    return wrap


def autoassign(*names, **kwargs):
    """Decorator for automatic class attributes generation

    Args:
        *names: non-keyworded, variable-length argument list.
                If used, only the list of variables are assigned as class attributes
        **kwargs: current support keyword is "excluded" only.
                If used, variables in the excluded list are not assigned as class attributes

    Examples:
        allow a method to assign (some of) its arguments as attributes of
        'self' automatically. e.g

        >>> class Foo(object):
        ...     @autoassign
        ...     def __init__(self, foo, bar): pass
        ...
        >>> breakfast = Foo('spam', 'eggs')
        >>> breakfast.foo, breakfast.bar
        ('spam', 'eggs')

        To restrict autoassignment to 'bar' and 'baz', write:

            @autoassign('bar', 'baz')
            def method(self, foo, bar, baz): ...

        To prevent 'foo' and 'baz' from being autoassigned, use:

            @autoassign(exclude=('foo', 'baz'))
            def method(self, foo, bar, baz): ...
    """
    if kwargs:
        exclude, f = set(kwargs['exclude']), None
        sieve = lambda l: ifilter(lambda nv: nv[0] not in exclude, l)
    elif len(names) == 1 and isfunction(names[0]):
        f = names[0]
        sieve = lambda l: l
    else:
        names, f = set(names), None
        sieve = lambda l: ifilter(lambda nv: nv[0] in names, l)

    def decorator(f):
        fargnames, _, _, fdefaults = getargspec(f)
        # Remove self from fargnames and make sure fdefault is a tuple
        fargnames, fdefaults = fargnames[1:], fdefaults or ()
        defaults = list(sieve(izip(reversed(fargnames), reversed(fdefaults))))

        @wraps(f)
        def decorated(self, *args, **kwargs):
            assigned = dict(sieve(izip(fargnames, args)))
            assigned.update(sieve(kwargs.iteritems()))
            for _ in starmap(assigned.setdefault, defaults): pass
            self.__dict__.update(assigned)
            return f(self, *args, **kwargs)
        return decorated
    return f and decorator(f) or decorator


class SingletonClass:
    """Singleton class decorator

    Use decorator to restricts the instantiation of a class to one object

    In Cafe, we use it is to declare a global object.

    Example:
        >>> @SingletonClass
        >>> class Foo(object): pass
        >>> f1 = Foo()
        >>> f2 = Foo()
        >>> f1 is f2
        True

    """

    def __init__(self, klass):
        self.klass = klass
        self.instance = None
        update_wrapper(self, klass)

    def __call__(self, *args, **kwds):

        if self.instance is None:

            #debug code to trace when singleton object is created.
            if not __debug__:
                frameinfo = getframeinfo(currentframe().f_back)
                debug("creating singleton instance of %s\n" % str(self.klass))
                debug("caller %s:%s:%s\n" % (frameinfo.function, frameinfo.filename, str(frameinfo.lineno)))
                try:
                    frameinfo = getframeinfo(currentframe().f_back.f_back)
                    debug("caller %s:%s:%s\n" % (frameinfo.function, frameinfo.filename, str(frameinfo.lineno)))
                except TypeError:
                    # nothing to do
                    pass

            #


            self.instance = self.klass(*args, **kwds)

        return self.instance
