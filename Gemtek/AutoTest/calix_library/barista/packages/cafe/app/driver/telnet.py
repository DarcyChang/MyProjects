from cafe.app.driver.proto.shell import ShellDriver, ShellHandle, ShellTimeoutException
from cafe.core.logger import CLogger
from cafe.util.helper import check_ping
__author__ = 'kelvin'


_module_logger = CLogger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


class TelnetDriver(ShellDriver):
    top_prompt = r"[^\r\n].+((\#)|(\>)|(\:))"

    def __init__(self, session=None, name=None, default_timeout=5, crlf='\r'):
        super(TelnetDriver, self).__init__(session, name, default_timeout, crlf)
        self._handle = None

    def is_reachable(self):
        """Return true if driver/device is response to ping
        """
        host = self._session.host

        if host and check_ping(host):
            return True
        else:
            return False

    def is_connected(self):
        if self._handle and self._handle.is_opened():
            return True
        else:
            return False

    def open_handle(self):
        if self._handle and self._handle.is_opened():
            return

        if self._handle:
            warn('connection is disconnected, need reconnect!')
            self.close_handle()

        info('open telnet handle')
        self._handle = TelnetHandle(self, self._session.open_entity())

    def close_handle(self):
        if self._handle is None:
            return

        info('close telnet handle')
        self._handle.close()
        self._handle = None

    def session_command(self, cmd, prompt=None, timeout=None, newline=None, retry=1):
        """compatible with old usage

        Args:
            *args:
            **kwargs:

        Returns:

        """
        result = {'prompt': None, 'value': '', 'content': ''}
        self.open_handle()
        try:
            result = self._handle.session_command(cmd, prompt, timeout, newline)
        except Exception as e:
            if retry <= 0:
                _module_logger.exception('Execute command[%s] failed, does not need to retry and ignore the error' % (cmd,))
                self.close_handle()
                return result

            warn('Execute command[%s] failed, will retry %d times' % (cmd, retry))
            return self._retry_command(cmd, prompt, timeout, newline, retry)

        return result

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

    def _retry_command(self, cmd, prompt, timeout, newline, retry):
        for i in range(1, retry+1):
            info('retry %d/%d...' % (i, retry))
            try:
                self.close_handle()
                self.open_handle()
                result = self._handle.session_command(cmd, prompt, timeout, newline)
                info('retry %d/%d succeed' % (i, retry))
                return result
            except Exception as e:
                warn('retry %d/%d failed' % (i, retry))
                if i == retry:
                    self.close_handle()
                    raise


class TelnetHandle(ShellHandle):
    def is_opened(self):
        return self._entity.is_connected()

