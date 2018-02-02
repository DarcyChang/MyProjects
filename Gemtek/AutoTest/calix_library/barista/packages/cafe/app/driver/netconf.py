__author__ = 'kelvin'
"""
Created on 01/06/2016
@author: Kelvin Lee

"""
import inspect
from cafe.core.utils import Param
from handle import Handle
from cafe.sessions.ncsession import NetConfSession
from decorator import decorator
from cafe.util.helper import check_ping
from .proto.base import DriverBase

class NetConfDriverMeta(type):

    def _forwarder(cls, func):

        @decorator
        def __wrapper(f, self, *args, **kwargs):
            session = self.get_session()
            if not session.is_connected():
                session.login()
            _f = getattr(session, f.__name__)
            return _f(*args, **kwargs)

        return __wrapper(func)

    def __init__(cls, name, bases, dct):

        super(NetConfDriverMeta, cls).__init__(name, bases, dct)

        if "get_session" not in dct:
            raise NotImplementedError("get_session method is not implemented")

        methods = inspect.getmembers(NetConfSession, predicate=inspect.ismethod)

        for m in methods:
            if not str(m[0]).startswith("_"):
                setattr(cls, m[0], cls._forwarder(m[1].__func__))


class NetConfDriver(DriverBase):
    __metaclass__ = NetConfDriverMeta

    def __init__(self, session=None, name=None, app=None):

        if not isinstance(session, NetConfSession):
            raise TypeError("session (%s) is not NetConfSession" % name)

        self._session = session
        self.name = name
        self.app = app

    def is_reachable(self):
        """Return true if driver/device is response to ping
        """
        host = self._session.host

        if check_ping(host):
            return True
        else:
            return False

    def open_handle(self):
        """
        """
        if not self._session.is_connected():
            self._session.login()

    def is_connected(self):
        self._session.is_connected()

    def get_session(self):
        """Return NetConSession object
        """
        return self._session

    def set_ports(self, ports=None):

        if ports is None:
            ports = {}

        for k, v in ports.items():
            try:
                port = v["port"]
            except:
                port = None

            try:
                neighbor = Param(v["neighbor"])
            except:
                neighbor = Param()

            setattr(self, k, Handle(k, port, neighbor=neighbor))
