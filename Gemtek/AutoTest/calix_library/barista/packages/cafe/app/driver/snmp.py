from cafe.util.helper import check_ping
from .proto.base import DriverBase

class SnmpDriver(DriverBase):
    def __init__(self, session=None, name=None):
        self.session = session
        self.name = name
        self._handle_open = False

    def is_reachable(self):
        """Return true if driver/device is response to ping
        """
        host = None
        try:
            #self.session is a weakref.proxy
            #hasattr won't work.
            host = self.session.host
        except AttributeError:
            pass

        if host and check_ping(host):
            return True
        else:
            return False

    def is_connected(self):
        return self._handle_open

    def open_handle(self):
        if not self._handle_open:
            self.session.login()
            self._handle_open = True

    def close_handle(self):
        if self._handle_open:
            self.session.close()
            self._handle_open = False


     


