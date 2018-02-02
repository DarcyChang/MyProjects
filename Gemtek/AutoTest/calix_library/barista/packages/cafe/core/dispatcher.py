__author__ = 'kelvin'
from pydispatch import dispatcher as _dispatcher

SIGNAL_UNKNOWN_1 = "code: -9999 - unknown1"
SIGNAL_UNKNOWN_2 = "code: -9998 - unknown2"

connect = _dispatcher.connect
disconnect = _dispatcher.disconnect
get_all_receivers = _dispatcher.getAllReceivers
get_receivers = _dispatcher.getReceivers

def connections():
    return _dispatcher.connections

def receiver(signal, **kwargs):
    """
    A decorator for connecting receivers to signals. Used by passing in the
    signal (or list of signals) and keyword arguments to connect::
    @receiver("signal abc")
    def signal_receiver(sender, **kwargs):
    ...
    @receiver(["signal abc", "signal efg"])
    def signals_receiver(sender, **kwargs):
    ...
    """
    def _decorator(func):
        if isinstance(signal, (list, tuple)):
            for s in signal:
                _dispatcher.connect(func, signal=s, **kwargs)
        else:
            _dispatcher.connect(func, signal=signal, **kwargs)
        return func

    return _decorator

class Event(object):
    """
    This class represents a event/signal
    When it is fired, it will trigger all receivers associated with the event/signal.
    """
    def __init__(self, signal):
        """
        constructor
        :param signal: <signal name> or list of <signal name>
        :return: None
        """
        self.signal = signal

    def fire(self, *args, **kwargs):
        """
        :param args: variable position arguments required by the <signal receiver function>
        :param kwargs: variable named arguments  required by the <signal receiver function>
        :return: ret - list of (<signal receiver function object>, <value return by the function>)
        """
        ret = []
        if isinstance(self.signal, (list, tuple)):
            for s in self.signal:
                x = _dispatcher.send(signal=s, sender=self, *args, **kwargs)
                ret.extend(x)

        else:
            x = _dispatcher.send(signal=self.signal, sender=self, *args, **kwargs)
            ret.append(x)
        return ret

CEvent = Event
if __name__ == "__main__":

    import threading
    #test code
    @receiver(SIGNAL_UNKNOWN_1)
    def test():
        print("hello")
        return 123

    @receiver([SIGNAL_UNKNOWN_1,SIGNAL_UNKNOWN_2])
    def test2():
        print("hello2")

    @receiver(SIGNAL_UNKNOWN_1)
    def test3(sender, signal, name=None):

        print("hello %s name:%s" % (str(sender), str(name)))
        print("signal %s" % signal)
        print(threading.current_thread().name)
        return "abc"

    class MyObject():

        i = "xxxxxxx"
        def __init__(self):
            connect(self.prt, signal=SIGNAL_UNKNOWN_2)
            pass

        #this does not work. how to fix???
        #@receiver(_UNKNOWN_2)
        def prt(self):
            print (self.i)

    m = MyObject()

    s = CEvent([SIGNAL_UNKNOWN_1, SIGNAL_UNKNOWN_2])
    s.fire()

    def worker():
        _dispatcher.send(signal=SIGNAL_UNKNOWN_1, sender={} )
        s = Event([SIGNAL_UNKNOWN_2])
        x = s.fire(name=123)
        print (threading.current_thread().name)

    for i in range(0,3):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    t.join()

    #print (_dispatcher.connections)
