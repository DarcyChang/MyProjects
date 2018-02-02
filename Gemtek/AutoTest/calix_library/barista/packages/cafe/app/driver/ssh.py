from cafe import Param
from cafe.app.driver.handle import Handle
from cafe.app.driver.proto.shell import ShellDriver, ShellHandle
from cafe.core.logger import CLogger
from cafe.util.helper import check_ping
__author__ = 'kelvin'


_module_logger = CLogger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


class SSHDriver(ShellDriver):
    error_response = r"error"

    def __init__(self, session=None, name=None, default_timeout=5, crlf="\n"):
        super(SSHDriver, self).__init__(session, name, default_timeout, crlf)
        self._handle = None

    def set_session(self, session):
        self._session = session

    @property
    def session(self):
        return self._session

    def _is_handle_opened(self):
        if self._handle and self._handle.is_opened():
            return True

        info('handle is closed')
        return False

    def is_reachable(self):
        """Return true if driver/device is response to ping
        """
        host = self._session.host

        if host and check_ping(host):
            return True
        else:
            return False

    def is_connected(self):
        return self._is_handle_opened()

    def open_handle(self):
        if self._is_handle_opened():
            return

        self._open_handle()

    def _open_handle(self):
        if self._handle:
            warn('connection is disconnected, need reconnect!')
            self.close_handle()

        info('open ssh handle')
        self._handle = SSHHandle(self, self._session.open_entity())

    def close_handle(self):
        if self._handle is None:
            return

        info('close ssh handle')
        self._handle.close()
        self._handle = None

    def top(self):
        pass

    def set_ports(self, ports={}):
        for k, v in ports.items():
            try:
                port = v["port"]
            except KeyError:
                port = None

            try:
                neighbor = Param(v["neighbor"])
            except KeyError:
                neighbor = Param()

            setattr(self, k, Handle(k, port, neighbor=neighbor))

    # def set_ports(self, ports={}):
    #     for k, v in ports.items():
    #         try:
    #             port = v["port"]
    #         except:
    #             port = None
    #
    #         try:
    #             neighbor = Param(v["neighbor"])
    #         except:
    #             neighbor = Param()
    #
    #         setattr(self, k, Handle(k, port, neighbor=neighbor))

    def session_command(self, cmd, prompt=None, timeout=None, newline=None, retry=1):
        """compatible with old usage

        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.open_handle()
        return self._handle.session_command(cmd, prompt, timeout, newline)

    command = session_command

    cli = session_command

    def one_time_command(self, *args, **kwargs):
        """compatible with old usage

        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.open_handle()
        return self._handle.one_time_command(*args, **kwargs)

    def disconnect(self):
        self.close_handle()
        self._session.close_ssh_client()


class SSHHandle(ShellHandle):
    def is_opened(self):
        if self._entity is None:
            return False

        return self._entity.is_connected()

