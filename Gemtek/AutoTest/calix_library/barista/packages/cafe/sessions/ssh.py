from __future__ import print_function

from contextlib import contextmanager
from functools import wraps

import paramiko
import random
import time
import re
import socket
import threading
import logging


from cafe.core.shutdown import Shutdownable
from cafe.core.utils import create_folder
from cafe.core.logger import CLogger as Logger, DEFAULT_LOGGER_CONFIG, init_logging
from cafe.core.signals import SESSION_SSH_ERROR, SESSION_SSH_LOGIN_FAILED
from cafe.sessions.base.shell import ShellEntity, ShellSession
from cafe.core.decorators import mem_debug

_TIMEOUT = 5.0
_CONNECT_TIMEOUT = 5
_COMMAND_ADDITION_WAIT = 5.0
_PROMPT = [r"[^\r\n]+\#", r"[^\r\n]+\>"]
_LOGIN_RETRY = 3
_RECEIVE_MAX = 50
_PORT = 22
_CRLF = "\n"
_TERM = "vt100"
_WIDTH = 80
_HEIGHT = 60
_MORE_PROMPT = [(r"--More--", "\n")]
_LOGFILE = None
# _SSH_TOOL_LOG = "paramiko.log"
_SSH_TOOL_LOG = None

# init_logging()
_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


class SSHLoginException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_SSH_LOGIN_FAILED)


class SSHSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_SSH_ERROR)


# class SSHLoginException(Exception):
#     logging.exception(SESSION_SSH_LOGIN_FAILED)
# class SSHSessionException(Exception):
#     logging.exception(SESSION_SSH_ERROR)


def must_connected(func):
    @wraps(func)
    def wrapper(self, *arg, **kwargs):
        if not self.is_connected():
            self.login()

        return func(self, *arg, **kwargs)

    return wrapper


#class _SSHSession(Shutdownable):
class _SSHSession(ShellSession):
    """
    Ssh session base class
    """

    def __init__(self, sid=None, host=None, port=_PORT, user=None, password=None,
                 prompt=None, connect_timeout=_CONNECT_TIMEOUT, timeout=_TIMEOUT,
                 term=_TERM, width=_WIDTH, height=_HEIGHT,
                 logfile=None, ssh_tool_log=_SSH_TOOL_LOG, logger=Logger(__name__), log_level=None, smart_reconnect=False, **kwargs):
        super(_SSHSession, self).__init__(sid, host, port, user, password, prompt, connect_timeout, timeout, term,
                                          width, height, logfile, logger, log_level)
        self.smart_reconnect = smart_reconnect
        self.crlf = '\n'

        self.ssh_tool_log = ssh_tool_log
        self.ssh_tool_log = Logger("paramiko")
        self.ssh_tool_log.set_level("ERROR")
        #self.session_log.add_network_handler()

    #def __del__(self):
    def __shutdown__(self):
        if self.is_connected():
            self.close()

    def set_prompt(self, new_prompt=None):
        # Unused
        debug('old prompt is: "%s"' % self.prompt)
        if new_prompt is None:
            # send command and wait for timeout
            result = self._entity.command('', [], 5)
            content = result[2]
            p = re.split(r'[\r\n]+', content)[-1]
            debug('p: %s' % p)
            self.prompt = str(p).strip()
        else:
            self.prompt = new_prompt
        debug('new prompt is: "%s"' % self.prompt)

    def login(self):
        self.logger.info('Try login to %s:%s with username=%s, password=%s'
                         % (self.host, self.port, self.user, self.password))
        repeat = 0
        while repeat < 3:
            try:
                self._login()
                if self._session is not None:
                    return True
            except SSHLoginException:
                repeat += 1
                self.logger.debug("ssh session login retry (sid=%s,host=%s, retry=%d)" %
                                  (self.sid, self.host, repeat))
                time.sleep(3)

        raise SSHLoginException("sid=%s, host=%s connect failed" % (self.sid, self.host))

    def _login(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, username=self.user, password=self.password,
                        timeout=self.connect_timeout)
            # time.sleep(2.0)

            self._session = ssh
            self.logger.info("ssh session login complete (sid=%s,host=%s)" % (self.sid, self.host))
        except Exception:
            raise SSHLoginException("sid=%s, host=%s" % (self.sid, self.host))

        finally:
            pass

    def is_connected(self):
        """This method is not reliable.
        When the connection is half-open(peer closed it unexpectedly, like crash or reboot), this method will still
        return True if you did not call function to send/receive data before call this method.
        Please check cafe.sessions.ssh.SSHEntity#_is_connected for details.
        """
        if not self._session:
            self.logger.info('Connection has not built')
            return False

        if self._session.get_transport().is_active():
            return True

        # connection is closed
        self.logger.info('Connection is closed.')
        self.close_entity()
        self.close_ssh_client()

        return False

    def is_entity_opened(self):
        if not self._entity:
            return False

        if self._entity.is_connected():
            return True

        return False

    def read(self, timeout=None):
        self.open_entity()
        return self._entity.read(timeout)

    def write(self, cmd="", crlf=_CRLF):
        self.open_entity()
        return self._entity.write(cmd, crlf)

    def expect_prompt(self, timeout=None):
        return self.expect(self.prompt, timeout)

    def expect(self, expected, timeout=None):
        self.open_entity()
        return self._entity.expect(expected, timeout)

    @must_connected
    def open_entity(self):
        if self._entity:
            return self._entity

        channel = None
        info('[SSH]create a channel to %s:%s, username=%s, password=%s' % (self.host, self.port, self.user, self.password))
        try:
            channel = self._session.invoke_shell(self.term, self.width, self.height)
        except Exception as e:
            self.logger.exception('Connection is closed before create channel, will reconnect.')
            self.close_ssh_client()
            self.login()

        if not channel:
            channel = self._session.invoke_shell(self.term, self.width, self.height)

        entity = SSHEntity(self, channel, self.prompt, self._timeout)
        prompt_idx, _, _ = entity.expect_prompt(self.connect_timeout)
        if prompt_idx < 0:
            raise SSHLoginException('Login failed, cannot receive prompt')
        self._entity = entity
        return self._entity

    def close_entity(self):
        if self._entity is None:
            return

        try:
            self._entity.close()
        except Exception:
            # ignore the exception
            pass
        finally:
            self._entity = None

    def remove_entity(self, entity):
        if self._entity is entity:
            self._entity = None

    @must_connected
    def command(self, cmd='', prompt=None, timeout=None, newline=None):
        self.open_entity()
        result = (-1, None, '')
        try:
            result = self._entity.command(cmd, prompt, timeout, newline)
        except Exception:
            error('send command(%s) failed, close the connection' % cmd)
            self.close_entity()

        return result

    @must_connected
    def one_time_command(self, cmd='', timeout=None):
        with self._lock:
            chan = self._session.get_transport().open_session()
            chan.exec_command(cmd)

            try:
                if timeout is None:
                    timeout = self._timeout

                max_time = time.time() + float(timeout)
                while True:
                    if chan.exit_status_ready():
                        status = chan.recv_exit_status()
                        self.logger.info('get return status: {}'.format(status))
                        return status

                    time.sleep(0.01)

                    if max_time < time.time():
                        break

                self.logger.error('recv return status fail')
                return -1
            finally:
                chan.close()

    def close(self):
        self.close_entity()
        self.close_ssh_client()
        if self.ssh_tool_log:
            self.ssh_tool_log.remove_handlers()
            self.ssh_tool_log = None
        if self.session_log:
            self.session_log.remove_handlers()
            self.session_log = None

        self._lock = None

    def close_ssh_client(self):
        if self._session is None:
            return

        try:
            self._session.close()
        except Exception:
            # ignore the exception
            pass
        finally:
            self._session = None

# alias
SSHSession = _SSHSession
# if __name__ == "__main__":
#     from cafe.core.logger import init_logging
#     init_logging()
#
#     s = SSHSession("exa", host="10.243.19.213", user="root", password="root", logfile=None)
#     s.session_log.console = True
#     s.login()
#
#     s.write("tcpdump -i eth0 -c 100")
#     for i in range(10):
#         r = s.expect([r"root@E5-520\:\~\#"])
#         print(r)
#         if r[0] < 0:
#             print("no prompt yet. continue to pull")
#         else:
#             print(r[1].group())
#             break
#         #sleep for time sec
#         time.sleep(2)
#
#     if r[0] < 0:
#         print("wait time expired. no prompt is found")

# print(x[1].group())


class SSHEntity(ShellEntity):
    """SSH Handle is a wrapper of paramiko.channel
    Data transport occured on SSHHandle, you can treat SSHHandle as a shell terminal
    """

    def __init__(self, session, channel, prompt, timeout):
        super(SSHEntity, self).__init__(session, channel, prompt, timeout)

    def read(self, timeout=None):
        chan_time_bk = self._channel.gettimeout()
        if timeout:
            self._channel.settimeout(timeout)

        s = ''
        try:
            s = str(self._channel.recv(10000))
            self._session.write_session_log(s)
        except socket.timeout:
            pass
        finally:
            self._channel.settimeout(chan_time_bk)

        return s

    def write(self, cmd="", crlf=None):
        if crlf is None:
            crlf = self.crlf
        with self._lock:
            if self._channel:
                self._channel.send(cmd + crlf)
            else:
                raise SSHSessionException("channel is None")

    def close(self):
        self._channel.close()
        self._session.remove_entity(self)
        self._lock = None

    def is_connected(self):
        return self._session.is_connected() and self._is_connected(0.001)

    def _is_connected(self, timeout=None):
        """Check connection status.
        If connection is half open, we should send an ignore packet and receive message from the connection to detect
        whether the connection is broken.
        """
        # send an ignore packet through the socket
        if self._session.smart_reconnect:
            self._channel.get_transport().send_ignore()

        # receive everything from the socket
        @contextmanager
        def modify_connection_timeout(conn_timeout):
            chan_time_bk = self._channel.gettimeout()
            if conn_timeout:
                self._channel.settimeout(conn_timeout)
            yield
            self._channel.settimeout(chan_time_bk)

        with modify_connection_timeout(timeout):
            status = self._check_is_connected_by_recv_and_discard()

        # Sometimes, half open connection will send EOF to CAFE, so we can detect the disconnection here.
        if not status:
            self._session.logger.warn('SSH channel is broken.')
            return False

        # Sometimes, half open connection don't send EOF, so we should check connection after send IGNORE packet
        # to server, it will cause a 'Connection reset by peer' error when recv message and set the transport status
        # to inactive
        if self._channel.get_transport().is_active():
            return True

        self._session.logger.warn('SSH channel is broken.')
        return False

    def _check_is_connected_by_recv_and_discard(self):
        while True:
            # discard the data in the connection,
            # if have data, then recv it and continue the loop
            # if don't have data and is connected, then will catch the `socket.timeout` exception
            # if don't have data and is disconnected, then `s` will be empty
            try:
                s = str(self._channel.recv(10000))
                self._session.write_session_log(s)
            except socket.timeout:
                return True

            if not s:
                return False


