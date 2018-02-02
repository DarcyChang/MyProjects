__author__ = 'akhanov'

import abc
import weakref

from cafe.core.utils import SingletonClass


class ShutdownException(Exception):
    def __init__(self, message):
        """An exception class that is raised whenever an error specific to the _Shutdown module occurs

        Args:
            message (str): The error message
        """
        self.__message = message

    def __str__(self):
        """Creates a string representation of the ShutdownException and returns it.

        Returns:
            str: The string representation of the ShutdownException object
        """
        return "ShutdownException: %s" % self.__message


@SingletonClass
class _Shutdown(object):
    """Singleton class for managing a list of objects that need to be shutdown.
    """
    __shutlist = {}

    def register(self, obj):
        """Adds the specified Shutdownable object to list of Shutdownables to shut down
        and returns the key to the object.

        Args:
            obj (Shutdownable): The object to add

        Returns:
            str: The key to the object. This key can be passed to _Shutdown.shutdown method to shutdown the just-added
                object. The key is created using the built-in Python method 'repr'. You can override your class's
                __repr__ method in order to change the key string.

        Raises:
            ShutdownException: if the object is not an instance of Shutdownable
        """
        if not isinstance(obj, Shutdownable):
            raise ShutdownException("'%s' is not an instance of %s" % (str(obj), Shutdownable.__name__))

        key = repr(obj)
        #self.__shutlist[key] = obj
        self.__shutlist[key] = weakref.ref(obj)

        for i in self.__shutlist:
            if self.__shutlist[i]() is None:
                del self.__shutlist[i]

        return key

    def get_shutdown_list_iter(self):
        """A generator of keys to shutdown. These keys can be passed to _Shutdown.shutdown()

        Yields:
            a key of the object to shutdown
        """
        for i in self.__shutlist.iterkeys():
            yield i

    def get_shutdown_list(self):
        return self.__shutlist.keys()

    def shutdown(self, key=None):
        """Sends a shutdown signal to all registered objects, or, optionally, to one specific object

        Args:
            key (Optional[str]): Defaults to None. The key of the registered object to shutdown. If None, shuts down all
                objects
        """
        # if key is None:
        #     for k in self.__shutlist.iterkeys():
        #         self.__shutlist[k].__shutdown__()
        # else:
        #     self.__shutlist[key].__shutdown__()
        if key is None:
            it = self.__shutlist.iterkeys()
        else:
            it = [repr(key)]

        # print(self.__shutlist)

        for i in it:
            ref = self.__shutlist[i]()

            # print("SHUTTING DOWN: %s" % str(ref))

            if ref is not None:
                ref.__shutdown__()
            else:
                del self.__shutlist[i]

    def clear_shutdown_list(self):
        """Clears the shutdown list, removing all previously registered objects
        """
        self.__shutlist = {}


Shutdown = _Shutdown()
"""The global instance of _Shutdown
"""


class ShutdownableMeta(abc.ABCMeta):
    """Metaclass that describes how a Shutdownable class should be created
    """
    _shutdown_name = "__shutdown__"

    def __new__(mcs, name, bases, attrs):
        """Method that describes what happens when a Shutdownable class is created
        Injects a __shutdown__ method into the class, and modifies the constructor
        to register each instance of the class in Shutdown object

        Args:
            name (str): The name of the class being created
            bases (tuple): Names of classes that are specified as base classes
            attrs (dict): A dictionary of the class's attributes and their values
        """
        new_attrs = attrs

        # Make sure __del__ is not overriden
        if '__del__' in new_attrs:
            raise SyntaxError("Not allowed to override __del__")

        def del_func(self, *args, **kwargs):
            self.__shutdown__()

        new_attrs['__del__'] = del_func

        # Inject the __shutdown__ method
        if ShutdownableMeta._shutdown_name not in new_attrs:
            func = None

            for base in bases:
                if ShutdownableMeta._shutdown_name in base.__dict__:
                    func = base.__dict__['__shutdown__']
                    break

            if func is None:
                def __shutdown__(mcs):
                    pass

                func = __shutdown__

            new_attrs[ShutdownableMeta._shutdown_name] = func

        # Inject initialization code into constructor
        if '__init__' in new_attrs:
            init_func = new_attrs['__init__']

            def __init__(self, *args, **kwargs):
                Shutdown.register(self)
                init_func(self, *args, **kwargs)

            func = __init__
        else:
            init_func = None

            for base in bases:
                if '__init__' in base.__dict__:
                    init_func = base.__dict__['__init__']
                    break

            def __init__(self, *args, **kwargs):
                init_func(self, *args, **kwargs)

            func = __init__



        new_attrs['__init__'] = func
        obj = super(ShutdownableMeta, mcs).__new__(mcs, name, bases, new_attrs)
        return obj


class Shutdownable(object):
    """Abstract class (interface) that takes care of setting up its child classes as "Shutdownable"
    Its metaclass is ShutdownableMeta
    """
    __metaclass__ = ShutdownableMeta

    @abc.abstractmethod
    def __shutdown__(self):
        """The abstract method that handles the shutdown signal. Classes that inherit from Shutdownable must override
        this method
        """
        pass

    # def __del__(self):
    #     self.__shutdown__()
