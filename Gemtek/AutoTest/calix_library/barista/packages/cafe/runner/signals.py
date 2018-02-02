__author__ = 'akhanov'

from cafe.core.utils import SingletonClass
from cafe.core.logger import CLogger as Logger
import os
import sys
import inspect

_signal_logger = Logger('signals')
""" Logger of signals
"""


def default_handler(sig):
    """The default callback for Signals. Logs the signal to the log.

    Args
        sig (Signal): the signal that was raised
    """
    sys.exc_clear()
    message = "%s:%s" % (sig.filename, sig.lineno)
    _signal_logger.exception(message, sig.message)
    #sig.clear()


class Signal(object):
    """ The base Signal class. The class keeps track of all its instances, as well as information about the signal for
    the instance
    """
    errno = 0
    """ (int): The error code of the signal
    """
    message = "A signal was generated"
    """ (str): The message of the signal raised
    """
    default_handler = None
    """ (func(Signal)): The default handler callback function that will get called when the Signal is raised
    """

    def __init__(self, message=None, filename=None, lineno=None):
        """ Initialize the signal object

        Args:
            message (Optional[str]): Defaults to None. The message of the signal raised. If None, set to Signal.message.
            filename (Optional[str]): Defaults to None. The name of the file relevant to the signal. If None, set to the
                name of the file where the signal was raised.
            lineno (Optional[str]): Defaults to None. The line number relevant to the signal. If None, set to the line
                number of the line where the signal was raised.
        """
        if message is not None:
            self.message = message

        self.filename = filename
        self.lineno = lineno
        self.type = self.__class__

    def __str__(self):
        """ Returns the string representation of the Signal. Format: '<SignalName>(<errno>)@<filename>:<lineno>'.

        Returns:
            str: The string representation of the Signal.
        """
        lineno = self.lineno
        filename = self.filename
        message = self.message

        if lineno is None:
            lineno = "UNKNOWN_LINE"

        if filename is None:
            filename = "UNKNOWN_FILE"

        if message is None:
            message = "UNKOWN_MESSAGE"

        return "%s(%s)@%s:%s - %s" % (self.__class__.__name__, self.__class__.errno, os.path.basename(filename), lineno,
                                      message)

    def __repr__(self):
        """ Returns a formal representation of the Signal. Format same as __str__

        Returns:
            str: The formal representation of the Signal
        """
        return self.__str__()

    # @classmethod
    # def get_instance_list(cls, exec_level_index=None):
    #     """ Returns a list of all instances of this class
    #
    #     Returns:
    #         list: The list of all instances of this class
    #     """
    #     ret = []
    #
    #     if exec_level_index is None:
    #         pass
    #
    #     return list(cls.instance_list)
    #
    # @classmethod
    # def clear(cls):
    #     """ Clears all signals of this type
    #     """
    #     for i in cls.instance_list:
    #         clear_signal(i)


@SingletonClass
class _SignalManager(object):
    """ Singleton class that manages signals and levels of execution
    """
    __level_stack = []
    __current_level = {}

    def __init__(self):
        """ Initialize the singleton object
        """
        self.__current_level = self.__level_template()

    def __level_template(self):
        """ Central location for the level template
        """
        return dict({'signals': {}, 'handlers': {}})

    def new_exec_level(self):
        """ Backs up the current execution level in the stack, and creates a new one. Execution levels are isolated
        blocks of execution. Usually, there will be at most 3: Global, In-Test-Suite, and In-Test-Case levels.
        """
        self.__level_stack.append(self.__current_level)
        self.__current_level = self.__level_template()

    def finish_exec_level(self):
        """ Closes & removes the current execution level. If any signals were uncleared in this level, they are
        carried over to the previous execution level. Then, the previous execution level is restored as the current one.
        """
        ret = self.__current_level
        self.__current_level = self.__level_stack.pop()

        for sig_type in ret['signals']:
            for sig in ret['signals'][sig_type]:
                self.add(sig, propagating=True)

        return ret

    def peek(self):
        """ Returns the open signals and registered handlers for the current execution level.

        Returns:
            dict: open signals and registered handlers.
                Format:
                ::

                    {
                        'signals': [...], # List of Signal objects
                        'handlers': [ # List of handler dictionaries
                            {
                                'handler': <func>, # The callback function
                                'running': <bool> # Boolean value specifying if the handler is currently running
                            }
                        ]
                    }
        """
        ret = self.__current_level
        return ret

    def get_level_index(self):
        return len(self.__level_stack)

    def get_signal_list(self, signal_type=Signal):
        """ Returns the list of open signals in the current execution level

        Returns:
            list: objects of type Signal that are open in the current execution level
        """
        ret = []

        for i in self.__current_level['signals']:
            if issubclass(i, signal_type):
                ret.extend(self.__current_level['signals'][i])

        return ret

    def add(self, signal, propagating=False):
        """ Adds a signal to the current execution level. Registers the default handler, if signal of this type has not
        been added before.

        Args:
            signal (Signal): The signal object to add

        Raises:
            AssertionError: if signal is not an instance of Signal or its subclasses
        """
        assert(isinstance(signal, Signal))

        try:
            self.__current_level['signals'][signal.__class__]
        except KeyError:
            self.__current_level['signals'][signal.__class__] = []
            if (not propagating) and (signal.__class__.default_handler is not None):
                self.register_handler(signal.__class__, signal.__class__.default_handler)
        finally:
            self.__current_level['signals'][signal.__class__].append(signal)

        try:
            handler_list = []

            for h in self.__current_level['handlers']:
                if issubclass(signal.__class__, h):
                    handler_list.extend(self.__current_level['handlers'][h])

            for i in handler_list:
                if not i['running']:
                    i['running'] = True
                    i['handler'](signal)
                    i['running'] = False

            _signal_logger.debug("Signal raised: %s" % signal)

        except KeyError:
            pass

    def clear(self, signal):
        """ Clears the signal, removing it from the execution level.

        Args:
            signal (Signal): The signal object to clear

        Raises:
            AssertionError: if signal is not an instance of Signal or its subclasses
        """
        assert(isinstance(signal, Signal))

        try:
            self.__current_level['signals'][signal.__class__].remove(signal)

            if len(self.__current_level['signals'][signal.__class__]) == 0:
                del(self.__current_level['signals'][signal.__class__])
        except ValueError:
            pass

    def register_handler(self, signal_type, handler):
        """ Registers a handler for a signals of signal_type. Whenever a signal of this type is raised, the handler
        function will be called.

        Args:
            signal_type (class): The type of signal (Signal or its subclasses) to register the handler for.
            handler (func): The handler function. Format: func_name(signal)

        Raises:
            AssertionError: if signal_type is not a subclass of Signal
        """
        assert(issubclass(signal_type, Signal))

        try:
            self.__current_level['handlers'][signal_type]
        except KeyError:
            self.__current_level['handlers'][signal_type] = []
        finally:
            entry = {'handler': handler, 'running': False}
            if entry not in self.__current_level['handlers'][signal_type]:
                self.__current_level['handlers'][signal_type].append(entry)

SignalManager = _SignalManager()
""" Instance of the _SignalManager singleton class
"""


def raise_signal(signal_type, message=None, filename=None, lineno=None):
    """ Raises the signal of the specified type. Simple wrapper around SignalManager.add().

    Args:
        signal_type (class): The type of signal to raise. Must be Signal or one of its subclasses.
        message (Optional[str]): Defaults to None. The message of the signal. If None, signal_type's default message
            will be used.
        filename (Optional[str]): Defaults to None. The name of the file relevant to the signal. If None, defaults to
            the name of the file where the signal is raised.
        lineno (Optional[str]): Defaults to None. The line number of the line relevant to the signal. If None, defaults
            to the line number of the line where raise_signal() is called.

    Raises:
        AssertionError: if signal_type is not Signal or its subclass
        TypeError: if signal_type is not a class

    Example:
        ::

            ...
            if self.connection_down():
                raise_signal(cafe.Signal, "connection is down!!!")
            ...

    """
    assert(issubclass(signal_type, Signal))

    if (filename is None) or (lineno is None):
        frame = inspect.stack()[1]

        if filename is None:
            filename = frame[1]

        if lineno is None:
            lineno = frame[2]

    signal = signal_type(message=message, filename=filename, lineno=lineno)
    SignalManager.add(signal)


def on_signal(signal_type, handler):
    """ Register a callback hander to be called each time a signal is raised. Simple wrapper around
    SignalManager.register_handler()

    Note:
        Signals raised before a handler is registered for them will not be processed by the handler

    Note:
        Handlers are triggered not only by signals of a specific signal type, but also by the subclasses of that signal
        type. For example, consider the following inheritance tree:

                 TelnetSignal --- TelnetNoConnectionSignal
               /
        Signal
               \
                SSHSignal

        A handler for type 'Signal' will run whenever a signal of ANY type is raised: Signal, TelnetSignal, SSHSignal,
        and TelnetNoConnectionSignal. A handler for type 'TelnetSignal' will run for only TelnetSignal and
        TelnetNoConnectionSignal. A handler for type 'SSHSignal' will run only for SSHSignal.

    Args:
        signal_type (class): The type of the signal to raise. Must be Signal or one of its subclasses
        handler (func): The callback function to register as the handler. Format: func_name(signal)

    Raises:
        AssertionError: if signal_type is not Signal or one of its subclasses.
        TypeError: if signal_type is not a class

    Example:
        ::

            def sig_handler(sgnl):
                cafe.print_console("Signal of type '%s' is raised in file '%s' on line '%s'" %
                                   (sgnl.__class__, sgnl.filename, sgnl.lineno))

            cafe.on_signal(cafe.Signal, sig_handler)

    """
    assert(issubclass(signal_type, Signal))
    SignalManager.register_handler(signal_type, handler)


def get_signals(signal_type=Signal):
    """ Returns the list of open signals for the current scope. Simple wrapper for SignalManager.get_signal_list()

    Args:
        signal_type (Optional[class]): The signal type to limit the returned list of signals to. By default, returns all
            signals.

    Returns:
        list: list of signals
    """
    return SignalManager.get_signal_list(signal_type)


def clear_signal(signal):
    """ Clears the signal and removes it from the list of signals for the current scope. Simple wrapper for
    SignalManager.clear().

    Args:
        signal (Signal): The signal to clear

    Example:
        ::

            # There are two ways to manage signals
            # One is by callback handler:
            def sig_handler(sgnl):
                cafe.print_console("Signal caught!!!")
                cafe.clear_signal(sgnl)

            # And the other is procedural:
            for sgnl in cafe.get_signals(MyCustomSignal):
                cafe.pritn_console("Signal caught!!!")
                cafe.clear_signal(sgnl)

    """
    SignalManager.clear(signal)

if __name__ == "__main__":
    class CustomSignal(Signal):
        pass

    raise_signal(CustomSignal, "HI")

    def hello(sgnl):
        print(sgnl.message)
        raise_signal(Signal, "HERE COMES JOHNNY")

    on_signal(Signal, hello)

    raise_signal(Signal, "LOLOLO")

    print(CustomSignal.instance_list)
    print(SignalManager.get_signal_list())

    if CustomSignal in get_signals():
        instances = CustomSignal.get_instance_list()
        print("================")
        for i in instances:
            print(i)
        print("================")

    print(SignalManager.get_signal_list())

    print(Signal.instance_list)
    print(CustomSignal.instance_list)
