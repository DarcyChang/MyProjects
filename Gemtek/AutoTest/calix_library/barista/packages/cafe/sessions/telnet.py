from __future__ import with_statement
from contextlib import contextmanager
import telnetlib
import time
import re
import inspect
import struct
import logging
import random
from functools import wraps

import select

from cafe.sessions.base.shell import ShellEntity, ShellSession

''' For telnetlib error handling '''
import errno
import socket
''' '''
#from cafe.core.logger import FORMAT2, DATEFMT
from cafe.core.logger import CLogger as Logger
from cafe.core.signals import SESSION_TELNET_LOGIN_FAILED, SESSION_TELNET_ERROR
from cafe.core.utils import create_folder
from cafe.runner.signals import raise_signal, Signal
from cafe import get_config
#from cafe.core.shutdown import Shutdownable

import cafe.core.signals as signals

import threading
try:
    import pyte
except ImportError:
    pyte = None

_PORT = 23
_WIDTH = 400
_HEIGHT = 100
_CONNECT_TIMEOUT = 5
_TIMEOUT = 5
_TERM = "vt100"
_PROMPT = [r"[^\r\n]+\$"]
_CRLF="\r"


_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

''' Signals - Definitions '''


class TelnetConnectionRefusedSignal(Signal):
    errno = 1023
    message = signals.SESSION_TELNET_LOSS_OF_CONNECTION


class TelnetNoConnectionSignal(Signal):
    errno = 1023
    message = signals.SESSION_TELNET_LOSS_OF_CONNECTION

''' DONE: Signals - Definitions '''


class TelnetLoginException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_TELNET_LOGIN_FAILED)


class TelnetSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_TELNET_ERROR)


class TelnetSession(ShellSession):
    def __init__(self, sid=None, host=None, port=_PORT, user=None, password=None,
                 prompt=None, login_prompt="ogin:", password_prompt="word:", timeout=_TIMEOUT,
                 connect_timeout=_CONNECT_TIMEOUT, crlf=_CRLF, term=_TERM, width=_WIDTH, height=_HEIGHT, enable_log=True, logfile=None,
                 logger=Logger(__name__), auto_login=True, log_level=None, **kwargs):
        super(TelnetSession, self).__init__(sid, host, port, user, password, prompt, connect_timeout, timeout, term, width, height,
                                            logfile, logger, log_level)

        self.login_prompt = login_prompt
        self.password_prompt = password_prompt

        self.terminal_size = (width, height)
        self.crlf = crlf

        self._connected = False
        self._is_login = False

        self.auto_login = auto_login

        self.xprompt = self._set_telnet_connection_prompt(self.prompt)
        debug('self.xprompt = %s' % self.xprompt)

    @staticmethod
    def _set_telnet_connection_prompt(prompt):
        """
        converting list of prompt to string for TelnetConnection requirement
        :param prompt: list of prompt of string of prompt
        :return: string of prompt
        """
        debug('type(prompt) is %s' % type(prompt))
        if isinstance(prompt, (list, tuple)):
            p = []
            for _p in prompt:
                p.append("(%s)" % _p)
            return "|".join(p)
        else:
            return None

    def open_entity(self, auto_login=None):
        """Open a telnet connection, currently every time call this method, will create a socket, this may be optimize in future.

        Returns:

        """
        if self._entity:
            return self._entity

        if auto_login is None:
            auto_login = self.auto_login

        info('[Telnet]create a channel to %s:%s, username=%s, password=%s' % (self.host, self.port, self.user, self.password))
        channel = TelnetConnection(host=self.host, port=self.port,
                                   prompt=self.xprompt, newline=self.crlf,
                                   prompt_is_regexp=True, terminal_emulation=True,
                                   window_size=self.terminal_size,
                                   logger=None)

        entity = TelnetEntity(self, channel, self.prompt, self._timeout)
        if auto_login:
            entity.login(self.user, self.password, self.login_prompt, self.password_prompt, self.connect_timeout)
        self._entity = entity
        return self._entity

    def command(self, cmd='', prompt=None, timeout=None, newline=None, retry=1):
        if not self.is_connected():
            self.login()

        self.open_entity()
        result = (-1, None, '')
        try:
            result = self._entity.command(cmd, prompt, timeout, newline)
        except Exception as e:
            if retry <= 0:
                _module_logger.exception('Execute command[%s] failed, does not need to retry and ignore the error' % (cmd,))
                self.close_entity()
                return result

            warn('Execute command[%s] failed, will retry %d times' % (cmd, retry))
            return self._retry_command(cmd, prompt, timeout, newline, retry)

        return result

    def close_entity(self):
        if self._entity is None:
            return

        try:
            self._entity.close()
        except Exception:
            # close the entity anyway
            pass
        finally:
            self._entity = None

    def remove_entity(self, entity):
        if self._entity is entity:
            self._entity = None

    def close(self):
        if self.session_log:
            self.session_log.remove_handlers()
            self.session_log = None

        self.close_entity()

    def close_session(self):
        self.close()

    def one_time_command(self, cmd='', timeout=None):
        raise NotImplementedError

    def login(self):
        if self.open_entity(auto_login=True) is not None:
            return True

    def is_connected(self):
        try:
            if self._entity.is_connected():
                return True
        except Exception:
            # ignore the exception
            pass

        self.close_entity()

        return False

    def reconnect(self):
        self.close_entity()
        self.open_entity()

    def read(self):
        self.open_entity()
        return str(self._entity.read())

    def write(self, cmd="", crlf=None):
        self.open_entity()
        return self._entity.write(cmd, crlf)

    def expect_prompt(self, timeout=None):
        return self.expect(self.prompt, timeout)

    def expect(self, expected, timeout=None):
        self.open_entity()
        return self._entity.expect(expected, timeout)

    def _retry_command(self, cmd, prompt, timeout, newline, retry):
        for i in range(1, retry+1):
            info('retry %d/%d...' % (i, retry))
            try:
                self.close_entity()
                self.open_entity()
                result = self._entity.session_command(cmd, prompt, timeout, newline)
                info('retry %d/%d succeed' % (i, retry))
                return result
            except Exception as e:
                warn('retry %d/%d failed' % (i, retry))
                if i == retry:
                    self.close_entity()
                    raise


class TelnetEntity(ShellEntity):
    def __init__(self, session, channel, prompt, timeout):
        super(TelnetEntity, self).__init__(session, channel, prompt, timeout)
        self._ep = select.epoll()
        self._ep.register(self._channel.sock.fileno(), select.EPOLLERR | select.EPOLLHUP)

    def read(self, timeout=None):
        # telnet read not process 'timeout' yet
        try:
            resp = self._channel.read()
            buf = resp.encode('ascii', 'backslashreplace')
            self._session.write_session_log(buf)
        except EOFError:
            self._session.logger.exception('Connection is closed when receive data.')
            raise
        except:
            self._session.logger.exception('Cannot process the response.')
            raise

        if not buf:
            time.sleep(0.01)

        return buf

    def write(self, cmd="", crlf=None):
        if crlf is None:
            crlf = self.crlf

        with self._lock:
            try:
                self._channel.write_bare(cmd + crlf)
            except Exception:
                raise TelnetSessionException('send msg fail')

    def close(self):
        self._channel.close_connection()
        self._session.remove_entity(self)

    def is_connected(self):
        if self._ep.poll(0):
            warn('detect disconnect by epoll')
            return False

        if self._channel.eof:
            warn('connection is disconnected')
            return False

        return True

    def login(self, username, password, login_prompt, password_prompt, login_timeout):
        # if output match nothing, send newline and try again, so we at most need invoke the method twice
        for _ in range(2):
            if self._login(username, password, login_prompt, password_prompt, login_timeout):
                return

        raise TelnetLoginException('Login failed, cannot match any prompt')

    def _login(self, username, password, login_prompt, password_prompt, login_timeout):
        if username is None:
            username = ''
        if password is None:
            password = ''
        tmp_prompt = []
        cur_prompt_index = 0

        prompt_cnt, login_prompt, login_prompt_index = self._analysis_prompt(login_prompt, cur_prompt_index)
        tmp_prompt.extend(login_prompt)
        cur_prompt_index += prompt_cnt

        prompt_cnt, password_prompt, password_prompt_index = self._analysis_prompt(password_prompt, cur_prompt_index)
        tmp_prompt.extend(password_prompt)
        cur_prompt_index += prompt_cnt

        tmp_prompt.extend(self._prompt)
        prompt_index, _, _ = self.expect(tmp_prompt, login_timeout)
        if prompt_index == -1:
            # match nothing, send newline and wait again.
            self.write()
            return False
        elif prompt_index in login_prompt_index:
            debug('match login prompt')
            self.write(username)
            ret = self.expect(password_prompt, login_timeout)
            if ret[0] == -1:
                raise TelnetLoginException('Login failed, cannot match password prompt.')
            self.write(password)
            # wait command prompt
            self._wait_command_prompt(login_timeout)
            info('Login success')
            return True
        elif prompt_index in password_prompt_index:
            debug('match password prompt')
            self.write(password)
            # wait command prompt
            self._wait_command_prompt(login_timeout)
            info('Login success')
            return True
        else:
            debug('match command prompt')
            # match cmd prompt
            return True

    def _analysis_prompt(self, in_prompt, start_index):
        cur_prompt_index = start_index
        ret_prompt = []
        ret_prompt_index = []
        if in_prompt:
            if not isinstance(in_prompt, (list, tuple)):
                in_prompt = [in_prompt]
            for p in in_prompt:
                ret_prompt.append(p)
                ret_prompt_index.append(cur_prompt_index)
                cur_prompt_index += 1

        return cur_prompt_index - start_index, ret_prompt, ret_prompt_index

    def _wait_command_prompt(self, timeout):
        prompt_index, _, _ = self.expect_prompt(timeout)
        if prompt_index == -1:
            raise TelnetLoginException('Login failed')


class TelnetConnection(telnetlib.Telnet):

    NEW_ENVIRON_IS = chr(0)
    NEW_ENVIRON_VAR = chr(0)
    NEW_ENVIRON_VALUE = chr(1)
    INTERNAL_UPDATE_FREQUENCY = 0.03
    LINEFEED = ["\r\n", "\r", "\n"]

    def __init__(self, host=None, port=23, timeout=3.0, newline="\n",
                 prompt=None, prompt_is_regexp=False,
                 encoding='UTF-8', encoding_errors='ignore',
                 default_log_level=logging.DEBUG, window_size=None, environ_user=None,
                 terminal_emulation=False, terminal_type=None, logger=None):
        self.logger = logger
        telnetlib.Telnet.__init__(self, host, int(port) if port else 23)
        self._set_timeout(timeout)
        #self._set_newline(newline)
        self._newline = newline
        self._set_prompt(prompt, prompt_is_regexp)
        self._set_encoding(encoding, encoding_errors)
        self._default_log_level = default_log_level
        self._window_size = window_size
        self._environ_user = environ_user
        self._terminal_emulator = self._check_terminal_emulation(terminal_emulation)
        self._terminal_type = str(terminal_type) if terminal_type else None
        self.set_option_negotiation_callback(self._negotiate_options)
        self._buf = ""

    def set_timeout(self, timeout):
        """Sets the timeout used for waiting output in the current connection.

        Read operations that expect some output to appear (`Read Until`, `Read
        Until Regexp`, `Read Until Prompt`, `Login`) use this timeout and fail
        if the expected output does not appear before this timeout expires.

        The `timeout` must be given in `time string format`. The old timeout is
        returned and can be used to restore the timeout later.

        Example:
        | ${old} =       | `Set Timeout` | 2 minute 30 seconds |
        | `Do Something` |
        | `Set Timeout`  | ${old}  |

        See `Configuration` section for more information about global and
        connection specific configuration.
        """
        self._verify_connection()
        old = self._timeout
        self._set_timeout(timeout)
        return secs_to_timestr(old)

    def _set_timeout(self, timeout):
        self._timeout = float(timeout)

    def set_newline(self, newline):
        """Sets the newline used by `Write` keyword in the current connection.

        The old newline is returned and can be used to restore the newline later.
        See `Set Timeout` for a similar example.

        If terminal emulation is used, the newline can not be changed on an open
        connection.

        See `Configuration` section for more information about global and
        connection specific configuration.
        """
        self._verify_connection()
        if self._terminal_emulator:
            raise AssertionError("Newline can not be changed when terminal emulation is used.")
        old = self._newline
        self._set_newline(newline)
        return old

    def _set_newline(self, newline):
        self._newline = str(newline).upper().replace('LF','\n').replace('CR','\r')

    def set_prompt(self, prompt, prompt_is_regexp=False):
        """Sets the prompt used by `Read Until Prompt` and `Login` in the current connection.

        If `prompt_is_regexp` is given any true value, including any non-empty
        string, the given `prompt` is considered to be a regular expression.

        The old prompt is returned and can be used to restore the prompt later.

        Example:
        | ${prompt} | ${regexp} = | `Set Prompt` | $ |
        | `Do Something` |
        | `Set Prompt` | ${prompt} | ${regexp} |

        See the documentation of
        [http://docs.python.org/2/library/re.html|Python `re` module]
        for more information about the supported regular expression syntax.
        Notice that possible backslashes need to be escaped in Robot Framework
        test data.

        See `Configuration` section for more information about global and
        connection specific configuration.
        """
        self._verify_connection()
        old = self._prompt
        self._set_prompt(prompt, prompt_is_regexp)
        if old[1]:
            return old[0].pattern, True
        return old

    def _set_prompt(self, prompt, prompt_is_regexp):
        if prompt_is_regexp:
            self._prompt = (re.compile(prompt), True)
        else:
            self._prompt = (prompt, False)

    def _prompt_is_set(self):
        return self._prompt[0] is not None

    def set_encoding(self, encoding=None, errors=None):
        """Sets the encoding to use for `writing and reading` in the current connection.

        The given `encoding` specifies the encoding to use when written/read
        text is encoded/decoded, and `errors` specifies the error handler to
        use if encoding/decoding fails. Either of these can be omitted and in
        that case the old value is not affected. Use string `NONE` to disable
        encoding altogether.

        See `Configuration` section for more information about encoding and
        error handlers, as well as global and connection specific configuration
        in general.

        The old values are returned and can be used to restore the encoding
        and the error handler later. See `Set Prompt` for a similar example.

        If terminal emulation is used, the encoding can not be changed on an open
        connection.

        Setting encoding in general is a new feature in Robot Framework 2.7.6.
        Specifying the error handler and disabling encoding were added in 2.7.7.
        """
        self._verify_connection()
        if self._terminal_emulator:
            raise AssertionError("Encoding can not be changed when terminal emulation is used.")
        old = self._encoding
        self._set_encoding(encoding or old[0], errors or old[1])
        return old

    def _set_encoding(self, encoding, errors):
        self._encoding = (encoding.upper(), errors)

    def _encode(self, text):
        if isinstance(text, str):
            return text
        if self._encoding[0] == 'NONE':
            return str(text)
        return text.encode(*self._encoding)

    def _decode(self, bytes):
        if self._encoding[0] == 'NONE':
            return bytes
        return bytes.decode(*self._encoding)

    def set_default_log_level(self, level):
        """Sets the default log level used for `logging` in the current connection.

        The old default log level is returned and can be used to restore the
        log level later.

        See `Configuration` section for more information about global and
        connection specific configuration.
        """
        self._verify_connection()
        old = self._default_log_level
        self._set_default_log_level(level)
        return old

    # def _set_default_log_level(self, level):
    #     if level is None or not self._is_valid_log_level(level):
    #         raise AssertionError("Invalid log level '%s'" % level)
    #     self._default_log_level = level.upper()
    # 
    # def _is_valid_log_level(self, level):
    #     if level is None:
    #         return True
    #     if not isinstance(level, basestring):
    #         return False
    #     return level.upper() in (logging.DEBUG, 'DEBUG', 'INFO', 'WARN')

    def close_connection(self, loglevel=None):
        """Closes the current Telnet connection.

        Remaining output in the connection is read, logged, and returned.
        It is not an error to close an already closed connection.

        Use `Close All Connections` if you want to make sure all opened
        connections are closed.

        See `Logging` section for more information about log levels.
        """
        self.close()
        output = self._decode(self.read_all())
        self._log(output, loglevel)
        return output

    def login(self, username, password, login_prompt='login: ',
              password_prompt='Password: ', login_timeout=2,
              login_incorrect='Login incorrect'):
        """Logs in to the Telnet server with the given user information.

        This keyword reads from the connection until the `login_prompt` is
        encountered and then types the given `username`. Then it reads until
        the `password_prompt` and types the given `password`. In both cases
        a newline is appended automatically and the connection specific
        timeout used when waiting for outputs.

        How logging status is verified depends on whether a prompt is set for
        this connection or not:

        1) If the prompt is set, this keyword reads the output until the prompt
        is found using the normal timeout. If no prompt is found, login is
        considered failed and also this keyword fails. Note that in this case
        both `login_timeout` and `login_incorrect` arguments are ignored.

        2) If the prompt is not set, this keywords sleeps until `login_timeout`
        and then reads all the output available on the connection. If the
        output contains `login_incorrect` text, login is considered failed
        and also this keyword fails. Both of these configuration parameters
        were added in Robot Framework 2.7.6. In earlier versions they were
        hard coded.

        See `Configuration` section for more information about setting
        newline, timeout, and prompt.
        """
        output = ''
        if not username and not password:
            # sometimes needn't login, just send ENTER
            self.write_bare(self._newline)
        else:
            output = self._submit_credentials(username, password, login_prompt,
                                              password_prompt)
        # if self._prompt_is_set():
        #     success, output2 = self._read_until_prompt()
        # else:
        #     success, output2 = self._verify_login_without_prompt(
        #             login_timeout, login_incorrect)
        # print "&"*100
        # print output
        # print type(output)
        # print "&"*100
        success, output2 = self._verify_login_without_prompt(
                    login_timeout, login_incorrect)
        output += output2

        if not success:
            #raise AssertionError('Login incorrect')
            raise TelnetLoginException("Login incorrect")

        # print "1234"*25
        # print output2
        # print type(output2)
        # print output
        # print type(output)
        # print "1234"*25

        return output

    def _submit_credentials(self, username, password, login_prompt, password_prompt):
        # Using write_bare here instead of write because don't want to wait for
        # newline: http://code.google.com/p/robotframework/issues/detail?id=1371
        output = ''
        try:
            # sometimes telnet server won't show login prompt until we send a ENTER
            output = self.read_until(login_prompt, logging.DEBUG)
            self.write_bare(username + self._newline)
        except NoMatchError:
            self.write_bare(self._newline)
            output = self.read_until(login_prompt, logging.DEBUG)
            self.write_bare(username + self._newline)

        output += self.read_until(password_prompt, logging.DEBUG)
        self.write_bare(password + self._newline)
        return output

    def _verify_login_without_prompt(self, delay, incorrect):
        time.sleep(float(delay))
        output = self.read(logging.DEBUG)
        # print "2234"*25
        # print output
        # print "2234"*25
        success = incorrect not in output
        if success:
            info('verify login success')
        else:
            error('verify login failed')
        return success, output

    def write(self, text, loglevel=None):
        """Writes the given text plus a newline into the connection.

        The newline character sequence to use can be [#Configuration|configured]
        both globally and per connection basis. The default value is `CRLF`.

        This keyword consumes the written text, until the added newline, from
        the output and logs and returns it. The given text itself must not
        contain newlines. Use `Write Bare` instead if either of these features
        causes a problem.

        *Note:* This keyword does not return the possible output of the executed
        command. To get the output, one of the `Read ...` keywords must be used.
        See `Writing and reading` section for more details.

        See `Logging` section for more information about log levels.
        """
        if self._newline in text:
            raise RuntimeError("'Write' keyword cannot be used with strings "
                               "containing newlines. Use 'Write Bare' instead.")
        self.write_bare(text + self._newline)
        # Can't read until 'text' because long lines are cut strangely in the output
        return self.read_until(self._newline, loglevel)

    def write_bare(self, text):
        """Writes the given text, and nothing else, into the connection.

        This keyword does not append a newline nor consume the written text.
        Use `Write` if these features are needed.
        """
        self._verify_connection()
        #print("'***%s***'" % text)
        telnetlib.Telnet.write(self, self._encode(text))

    def write_until_expected_output(self, text, expected, timeout,
                                    retry_interval, loglevel=None):
        """Writes the given `text` repeatedly, until `expected` appears in the output.

        `text` is written without appending a newline and it is consumed from
        the output before trying to find `expected`. If `expected` does not
        appear in the output within `timeout`, this keyword fails.

        `retry_interval` defines the time to wait `expected` to appear before
        writing the `text` again. Consuming the written `text` is subject to
        the normal [#Configuration|configured timeout].

        Both `timeout` and `retry_interval` must be given in `time string
        format`. See `Logging` section for more information about log levels.

        Example:
        | Write Until Expected Output | ps -ef| grep myprocess\\r\\n | myprocess |
        | ...                         | 5 s                          | 0.5 s     |

        The above example writes command `ps -ef | grep myprocess\\r\\n` until
        `myprocess` appears in the output. The command is written every 0.5
        seconds and the keyword fails if `myprocess` does not appear in
        the output in 5 seconds.
        """
        timeout = float(timeout)
        retry_interval = float(retry_interval)
        maxtime = time.time() + timeout
        while time.time() < maxtime:
            self.write_bare(text)
            self.read_until(text, loglevel)
            try:
                with self._custom_timeout(retry_interval):
                    return self.read_until(expected, loglevel)
            except AssertionError:
                pass
        raise NoMatchError(expected, timeout)

    def write_control_character(self, character):
        """Writes the given control character into the connection.

        The control character is preprended with an IAC (interpret as command)
        character.

        The following control character names are supported: BRK, IP, AO, AYT,
        EC, EL, NOP. Additionally, you can use arbitrary numbers to send any
        control character.

        Example:
        | Write Control Character | BRK | # Send Break command |
        | Write Control Character | 241 | # Send No operation command |
        """
        self._verify_connection()
        self.sock.sendall(telnetlib.IAC + self._get_control_character(character))

    def _get_control_character(self, int_or_name):
        try:
            return chr(int(int_or_name))
        except ValueError:
            return self._convert_control_code_name_to_character(int_or_name)

    def _convert_control_code_name_to_character(self, name):
        code_names = {
                'BRK' : telnetlib.BRK,
                'IP' : telnetlib.IP,
                'AO' : telnetlib.AO,
                'AYT' : telnetlib.AYT,
                'EC' : telnetlib.EC,
                'EL' : telnetlib.EL,
                'NOP' : telnetlib.NOP
        }
        try:
            return code_names[name]
        except KeyError:
            raise RuntimeError("Unsupported control character '%s'." % name)

    def read(self, loglevel=logging.DEBUG):
        """Reads everything that is currently available in the output.

        Read output is both returned and logged. See `Logging` section for more
        information about log levels.
        """
        self._verify_connection()
        output = self.read_very_eager()
        if self._terminal_emulator:
            self._terminal_emulator.feed(output)
            output = self._terminal_emulator.read()
        else:
            output = self._decode(output)
        self._log(output, loglevel)
        return output

    def read_until(self, expected, loglevel=None):
        """Reads output until `expected` text is encountered.

        Text up to and including the match is returned and logged. If no match
        is found, this keyword fails. How much to wait for the output depends
        on the [#Configuration|configured timeout].

        See `Logging` section for more information about log levels. Use
        `Read Until Regexp` if more complex matching is needed.
        """
        success, output = self._read_until(expected)
        self._log(output, loglevel)
        if not success:
            raise NoMatchError(expected, self._timeout, output)
        return output

    def _read_until(self, expected):
        self._verify_connection()
        if self._terminal_emulator:
            return self._terminal_read_until(expected)
        expected = self._encode(expected)
        output = telnetlib.Telnet.read_until(self, expected, self._timeout)
        return output.endswith(expected), self._decode(output)

    @property
    def _terminal_frequency(self):
        return min(self.INTERNAL_UPDATE_FREQUENCY, self._timeout)

    def _terminal_read_until(self, expected):
        max_time = time.time() + self._timeout
        out = self._terminal_emulator.read_until(expected)
        if out:
            return True, out
        while time.time() < max_time:
            input_bytes = telnetlib.Telnet.read_until(self, expected,
                                                      self._terminal_frequency)
            self._terminal_emulator.feed(input_bytes)
            out = self._terminal_emulator.read_until(expected)
            if out:
                return True, out
        return False, self._terminal_emulator.read()

    def _read_until_regexp(self, *expected):
        self._verify_connection()
        if self._terminal_emulator:
            return self._terminal_read_until_regexp(expected)
        expected = [self._encode(exp) if isinstance(exp, unicode) else exp
                    for exp in expected]
        return self._telnet_read_until_regexp(expected)

    def _terminal_read_until_regexp(self, expected_list):
        max_time = time.time() + self._timeout
        regexp_list = [re.compile(rgx) for rgx in expected_list]
        out = self._terminal_emulator.read_until_regexp(regexp_list)
        if out:
            return True, out
        while time.time() < max_time:
            output = self.expect(regexp_list, self._terminal_frequency)[-1]
            self._terminal_emulator.feed(output)
            out = self._terminal_emulator.read_until_regexp(regexp_list)
            if out:
                return True, out
        return False, self._terminal_emulator.read()

    def _telnet_read_until_regexp(self, expected_list):
        try:
            index, _, output = self.expect(expected_list, self._timeout)
        except TypeError:
            index, output = -1, ''
        return index != -1, self._decode(output)

    def read_until_regexp(self, *expected):
        """Reads output until any of the `expected` regular expressions match.

        This keyword accepts any number of regular expressions patterns or
        compiled Python regular expression objects as arguments. Text up to
        and including the first match to any of the regular expressions is
        returned and logged. If no match is found, this keyword fails. How much
        to wait for the output depends on the [#Configuration|configured timeout].

        If the last given argument is a [#Logging|valid log level], it is used
        as `loglevel` similarly as with `Read Until` keyword.

        See the documentation of
        [http://docs.python.org/2/library/re.html|Python `re` module]
        for more information about the supported regular expression syntax.
        Notice that possible backslashes need to be escaped in Robot Framework
        test data.

        Examples:
        | `Read Until Regexp` | (#|$) |
        | `Read Until Regexp` | first_regexp | second_regexp |
        | `Read Until Regexp` | \\\\d{4}-\\\\d{2}-\\\\d{2} | DEBUG |
        """
        if not expected:
            raise RuntimeError('At least one pattern required')
        if self._is_valid_log_level(expected[-1]):
            loglevel = expected[-1]
            expected = expected[:-1]
        else:
            loglevel = None
        success, output = self._read_until_regexp(*expected)
        self._log(output, loglevel)
        if not success:
            expected = [exp if isinstance(exp, basestring) else exp.pattern
                        for exp in expected]
            raise NoMatchError(expected, self._timeout, output)
        return output

    def read_until_prompt(self, loglevel=None):
        """Reads output until the prompt is encountered.

        This keyword requires the prompt to be [#Configuration|configured]
        either in `importing` or with `Open Connection` or `Set Prompt` keyword.

        Text up to and including the prompt is returned and logged. If no prompt
        is found, this keyword fails. How much to wait for the output depends
        on the [#Configuration|configured timeout].

        See `Logging` section for more information about log levels.
        """
        if not self._prompt_is_set():
            raise RuntimeError('Prompt is not set.')
        success, output = self._read_until_prompt()
        self._log(output, loglevel)
        if not success:
            prompt, regexp = self._prompt
            raise AssertionError("Prompt '%s' not found in %s."
                    % (prompt if not regexp else prompt.pattern,
                       secs_to_timestr(self._timeout)))
        return output

    def _read_until_prompt(self):
        prompt, regexp = self._prompt
        read_until = self._read_until_regexp if regexp else self._read_until
        return read_until(prompt)

    def execute_command(self, command, loglevel=None):
        """Executes the given `command` and reads, logs, and returns everything until the prompt.

        This keyword requires the prompt to be [#Configuration|configured]
        either in `importing` or with `Open Connection` or `Set Prompt` keyword.

        This is a convenience keyword that uses `Write` and `Read Until Prompt`
        internally Following two examples are thus functionally identical:

        | ${out} = | `Execute Command`   | pwd |

        | `Write`  | pwd                 |
        | ${out} = | `Read Until Prompt` |

        See `Logging` section for more information about log levels.
        """
        self.write(command, loglevel)
        return self.read_until_prompt(loglevel)

    @contextmanager
    def _custom_timeout(self, timeout):
        old = self.set_timeout(timeout)
        try:
            yield
        finally:
            self.set_timeout(old)

    def _verify_connection(self):
        if not self.sock:
            raise RuntimeError('No connection open')

    def _log(self, msg, level=logging.DEBUG):
        self._buf += msg
        if any(l in self._buf for l in self.LINEFEED):
            if self.logger:
                for _m in self._buf.splitlines():
                    self.logger.log (level, _m)
                    #self.logger.debug(_m)
                self._buf = ""
        # if msg in self.LINEFEED and self.logger:
        #     for _m in msg.splitlines():
        #        self.logger.log(level, _m)

    def _negotiate_options(self, sock, cmd, opt):
        # This is supposed to turn server side echoing on and turn other options off.
        if opt == telnetlib.ECHO and cmd in (telnetlib.WILL, telnetlib.WONT):
            self._opt_echo_on(opt)
        elif cmd == telnetlib.DO and opt == telnetlib.TTYPE and self._terminal_type:
            self._opt_terminal_type(opt, self._terminal_type)
        elif cmd == telnetlib.DO and opt == telnetlib.NEW_ENVIRON and self._environ_user:
            self._opt_environ_user(opt, self._environ_user)
        elif cmd == telnetlib.DO and opt == telnetlib.NAWS and self._window_size:
            self._opt_window_size(opt, *self._window_size)
        elif opt != telnetlib.NOOPT:
            self._opt_dont_and_wont(cmd, opt)

    def _opt_echo_on(self, opt):
        return self.sock.sendall(telnetlib.IAC + telnetlib.DO + opt)

    def _opt_terminal_type(self, opt, terminal_type):
        self.sock.sendall(telnetlib.IAC + telnetlib.WILL + opt)
        self.sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.TTYPE
                          + self.NEW_ENVIRON_IS + terminal_type
                          + telnetlib.IAC + telnetlib.SE)

    def _opt_environ_user(self, opt, environ_user):
        self.sock.sendall(telnetlib.IAC + telnetlib.WILL + opt)
        self.sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.NEW_ENVIRON
                          + self.NEW_ENVIRON_IS + self.NEW_ENVIRON_VAR
                          + "USER" + self.NEW_ENVIRON_VALUE + environ_user
                          + telnetlib.IAC + telnetlib.SE)

    def _opt_window_size(self, opt, window_x, window_y):
        self.sock.sendall(telnetlib.IAC + telnetlib.WILL + opt)
        self.sock.sendall(telnetlib.IAC + telnetlib.SB + telnetlib.NAWS
                          + struct.pack('!HH', window_x, window_y)
                          + telnetlib.IAC + telnetlib.SE)

    def _opt_dont_and_wont(self, cmd, opt):
        if cmd in (telnetlib.DO, telnetlib.DONT):
            self.sock.sendall(telnetlib.IAC + telnetlib.WONT + opt)
        elif cmd in (telnetlib.WILL, telnetlib.WONT):
            self.sock.sendall(telnetlib.IAC + telnetlib.DONT + opt)

    # def msg(self, msg, *args):
    #     # Forward telnetlib's debug messages to log
    #     logger.trace(msg % args)

    def _check_terminal_emulation(self, terminal_emulation):
        if not terminal_emulation:
            return False
        if not pyte:
            raise RuntimeError("Terminal emulation requires pyte module!\n"
                               "https://pypi.python.org/pypi/pyte/")
        return TerminalEmulator(window_size=self._window_size,
                                newline=self._newline, encoding=self._encoding)


class TerminalEmulator(object):

    def __init__(self, window_size=None, newline="\r\n",
                 encoding=('UTF-8', 'ignore')):
        self._rows, self._columns = window_size or (200, 200)
        self._newline = newline
        self._stream = pyte.ByteStream(encodings=[encoding])
        self._screen = pyte.HistoryScreen(self._rows,
                                          self._columns,
                                          history=100000)
        self._stream.attach(self._screen)
        self._screen.set_charset('B', '(')
        self._buffer = ''
        self._whitespace_after_last_feed = ''

    @property
    def current_output(self):
        return self._buffer + self._dump_screen()

    def _dump_screen(self):
        return self._get_history() + \
               self._get_screen(self._screen) + \
               self._whitespace_after_last_feed

    def _get_history(self):
        if self._screen.history.top:
            return self._get_history_screen(self._screen.history.top) + self._newline
        return ''

    def _get_history_screen(self, deque):
        return self._newline.join(''.join(c.data for c in row).rstrip()
                                  for row in deque).rstrip(self._newline)

    def _get_screen(self, screen):
        return self._newline.join(row.rstrip() for row in screen.display).rstrip(self._newline)

    def feed(self, input_bytes):
        self._stream.feed(input_bytes)
        self._whitespace_after_last_feed = input_bytes[len(input_bytes.rstrip()):]

    def read(self):
        current_out = self.current_output
        self._update_buffer('')
        return current_out

    def read_until(self, expected):
        current_out = self.current_output
        exp_index = current_out.find(expected)
        if exp_index != -1:
            self._update_buffer(current_out[exp_index+len(expected):])
            return current_out[:exp_index+len(expected)]
        return None

    def read_until_regexp(self, regexp_list):
        current_out = self.current_output
        for rgx in regexp_list:
            match = rgx.search(current_out)
            if match:
                self._update_buffer(current_out[match.end():])
                return current_out[:match.end()]
        return None

    def _update_buffer(self, terminal_buffer):
        self._buffer = terminal_buffer
        self._whitespace_after_last_feed = ''
        self._screen.reset()
        self._screen.set_charset('B', '(')


class NoMatchError(AssertionError):
    ROBOT_SUPPRESS_NAME = True

    def __init__(self, expected, timeout, output=None):
        self.expected = expected
        self.timeout = secs_to_timestr(timeout)
        self.output = output
        AssertionError.__init__(self, self._get_message())

    def _get_message(self):
        expected = "'%s'" % self.expected \
                   if isinstance(self.expected, basestring) \
                   else seq2str(self.expected, lastsep=' or ')
        msg = "No match found for %s in %s." % (expected, self.timeout)
        if self.output is not None:
            msg += ' Output:\n%s' % self.output
        return msg

def seq2str(sequence, quote="'", sep=', ', lastsep=' and '):
    """Returns sequence in format 'item 1', 'item 2' and 'item 3'"""
    quote_elem = lambda string: quote + _unic(string) + quote
    if not sequence:
        return ''
    if len(sequence) == 1:
        return quote_elem(sequence[0])
    elems = [quote_elem(s) for s in sequence[:-2]]
    elems.append(quote_elem(sequence[-2]) + lastsep + quote_elem(sequence[-1]))
    return sep.join(elems)

def _unic(item, *args):
    # Based on a recipe from http://code.activestate.com/recipes/466341
    try:
        return unicode(item, *args)
    except UnicodeError:
        try:
            return u''.join(c if ord(c) < 128 else c.encode('string_escape')
                            for c in str(item))
        except Exception:
            return _unrepresentable_object(item)
    except Exception:
        return _unrepresentable_object(item)

def _unrepresentable_object(item):
    return "Error: str(item)"

def secs_to_timestr(secs, compact=False):
    """Converts time in seconds to a string representation.

    Returned string is in format like
    '1 day 2 hours 3 minutes 4 seconds 5 milliseconds' with following rules:

    - Time parts having zero value are not included (e.g. '3 minutes 4 seconds'
      instead of '0 days 0 hours 3 minutes 4 seconds')
    - Hour part has a maximun of 23 and minutes and seconds both have 59
      (e.g. '1 minute 40 seconds' instead of '100 seconds')

    If compact has value 'True', short suffixes are used.
    (e.g. 1d 2h 3min 4s 5ms)
    """
    return _SecsToTimestrHelper(secs, compact).get_value()

def plural_or_not(item):
    count = item if isinstance(item, (int, long)) else len(item)
    return '' if count == 1 else 's'

def _float_secs_to_secs_and_millis(secs):
    isecs = int(secs)
    millis = int(round((secs - isecs) * 1000))
    return (isecs, millis) if millis < 1000 else (isecs+1, 0)

class _SecsToTimestrHelper:

    def __init__(self, float_secs, compact):
        self._compact = compact
        self._ret = []
        self._sign, millis, secs, mins, hours, days \
                = self._secs_to_components(float_secs)
        self._add_item(days, 'd', 'day')
        self._add_item(hours, 'h', 'hour')
        self._add_item(mins, 'min', 'minute')
        self._add_item(secs, 's', 'second')
        self._add_item(millis, 'ms', 'millisecond')

    def get_value(self):
        if len(self._ret) > 0:
            return self._sign + ' '.join(self._ret)
        return '0s' if self._compact else '0 seconds'

    def _add_item(self, value, compact_suffix, long_suffix):
        if value == 0:
            return
        if self._compact:
            suffix = compact_suffix
        else:
            suffix = ' %s%s' % (long_suffix, plural_or_not(value))
        self._ret.append('%d%s' % (value, suffix))

    def _secs_to_components(self, float_secs):
        if float_secs < 0:
            sign = '- '
            float_secs = abs(float_secs)
        else:
            sign = ''
        int_secs, millis = _float_secs_to_secs_and_millis(float_secs)
        secs  = int_secs % 60
        mins  = int(int_secs / 60) % 60
        hours = int(int_secs / (60*60)) % 24
        days  = int(int_secs / (60*60*24))
        return sign, millis, secs, mins, hours, days

if __name__ == "__main__":

    logger = logging.getLogger("telnet")

    from cafe.core.logger import init_logging

    init_logging()

    s = TelnetSession(sid="abc", host="localhost", user="kelvin", password="buffy818",
                      prompt=[r"\$"], crlf="\n", logfile="abc.log")
    #s.enable_print_session_log()
    s.session_log.console = True

    s.login()

    s.write("pwd")
    x = s.expect_prompt()
    #print(x)
    #print(x[1].group())
    s.write("ps aux")
    x = s.expect_prompt(timeout=100)
    #print(x[1].group())

    s = TelnetSession(sid="blm1", host="10.243.14.20", user="admin", password="nep123",
                      login_prompt="user:", password_prompt="pass:", term="vt220", width=120, height=80,
                      prompt=[r"\%"], logfile="blm1.log", login_timeout=5, connect_timeout=5)

    s.session_log.console = True

    s.login()
    time.sleep(5)
    s.write("show pa st")
    x = s.expect_prompt()
    #print (x)
    y = x[2]
    for i in y.split("\r"):
        print(i)



