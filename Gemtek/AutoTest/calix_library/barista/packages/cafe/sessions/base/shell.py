#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading

import time

import re

from cafe.core.utils import create_folder, static_vars
from cafe.core.logger import CLogger
import cafe
_logger = CLogger(__name__)
info = _logger.info

__author__ = 'David Qian'

"""
Created on 01/12/2016
@author: David Qian

"""


class ShellSession(object):
    default_prompt = [
        r'[^\r\n]+\#',
        r'[^\r\n]+\>',
        r'[^\r\n]+\$',
        r'[^\r\n]+\:\~\$',
        r'[^\r\n]*(\%)',
    ]

    def __init__(self, sid, host, port, user, password, prompt, connect_timeout, timeout, term, width, height,
                 session_log_file, logger, session_log_level=None):
        self.logger = logger
        self.sid = sid
        self._session = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connect_timeout = connect_timeout
        self._timeout = timeout
        self.term = term
        self.width = width
        self.height = height
        self.session_log = self.logger.get_child("session_log")
        self.session_log.console = False    # disable propagate
        self._logfile = None
        self._lock = threading.RLock()
        self._session = None
        self._entity = None
        self.session_log_level = session_log_level

        if self.session_log_level is None:
            self.session_log_level = cafe.get_config().logger.level
        self.logger.debug("session log level is: %s" % self.session_log_level)
        self.logger.debug('prompt=%s, type is %s' % (prompt, type(prompt)))
        if prompt is None:
            self._prompt = self.default_prompt
        else:
            self.prompt = prompt

        self.logfile = session_log_file
        self._line_buffer = []

    # def __del__(self):
    #     if self.is_connected():
    #         self.close()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout_):
        self._timeout = timeout_
        if self._entity is not None:
            self._entity.timeout = timeout_

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, f):
        if f is None:
            self.session_log.disable_file_logging()
            return
        if create_folder(f):
            self.logger.info("create folder for %s successful" % f)
        else:
            self.logger.info("create folder for %s failed" % f)
            return
        self._logfile = f
        self.session_log.enable_file_logging(log_file=f)
        self.session_log.set_level(self.session_log_level)

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, p):
        if isinstance(p, (list, tuple)):
            self._prompt = p
        elif isinstance(p, str):
            self._prompt = [re.escape(p)]
        else:
            raise RuntimeError("prompt must be list or tuple or str")

        if self._entity is not None:
            self._entity.set_prompt(self.prompt)

    def write_session_log(self, s):
        if self.session_log:
            output = self._parse_log(s)
            for _s in output:
                self.session_log.debug(_s)

    def login(self):
        raise NotImplementedError()

    def is_connected(self):
        raise NotImplementedError()

    def open_entity(self, auto_login=True):
        raise NotImplementedError()

    def close_entity(self):
        raise NotImplementedError()

    def one_time_command(self, cmd='', tiFmeout=None):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def change_credential(self, user_id, user_password, prompt):
        self.user = user_id
        self.password = user_password
        if prompt:
            self.prompt = prompt

        self.close()

    def __shutdown__(self):
        if self.is_connected():
            self.close()

    def _parse_log(self, s):
        """Output log by line buffering

        Args:
            s: log message

        Returns: output log message

        """
        line_buffer = self._line_buffer
        lines = s.splitlines()
        if s and (s[-1] == '\r' or s[-1] == '\n'):
            # output all
            line_buffer.append(lines[0])
            lines[0] = ''.join(line_buffer)
            del line_buffer[:]
            return lines
        elif len(lines) > 1:
            # output all except the last line
            line_buffer.append(lines[0])
            lines[0] = ''.join(line_buffer)
            del line_buffer[:]
            line_buffer.append(lines.pop())
            return lines
        elif len(lines) == 1:
            # buffer all
            line_buffer.append(lines[0])
            return []
        else:
            return []


class ShellEntity(object):
    def __init__(self, session, channel, prompt, timeout):
        self._session = session
        self._channel = channel
        self._prompt = prompt
        self._timeout = timeout
        self._lock = threading.RLock()

    def __del__(self):
        self.close()

    def set_prompt(self, prompt):
        self._prompt = prompt

    @property
    def crlf(self):
        return self._session.crlf

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout_):
        self._timeout = timeout_

    @property
    def logger(self):
        return self._session.logger

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, prompt_):
        self._prompt = prompt_

    def read(self, timeout=None):
        raise NotImplementedError()

    def command(self, cmd='', prompt=None, timeout=None, crlf=None):
        if crlf is None:
            crlf = self.crlf
        self.logger.debug('send command: %s' % cmd)
        with self._lock:
            self.write(cmd, crlf)
            if prompt is None:
                s = self.expect_prompt(timeout)
            else:
                s = self.expect(prompt, timeout)
        return s

    def write(self, cmd="", crlf=None):
        raise NotImplementedError()

    def expect_prompt(self, timeout=None):
        return self.expect(self._prompt, timeout)

    def expect(self, expected, timeout=None):
        """

        Args:
            expected: should be None or list, if it's None, this method will read until timeout
            timeout: wait time

        Returns:
            @succ: (prompt index, match object, output before prompt)
            @fail: (-1, None, all output)
        """
        if expected and not isinstance(expected, (list,)):
            raise RuntimeError("'expected' should be a list")

        if timeout is None:
            _timeout = float(self._timeout)
        else:
            _timeout = float(timeout)

        max_time = time.time() + _timeout
        rest_timeout = _timeout
        output = ''
        while True:
            _o = self.read(rest_timeout)
            if _o == '':
                # time.sleep(random.uniform(0.01, 0.05))
                # time.sleep(0.01)
                pass
            else:
                output += _o

            if expected:
                for i in range(0, len(expected)):
                    _exp = expected[i]
                    m = re.search(_exp, output)
                    if m:
                        # if match is found, process the output
                        # determine the prompt, string before the prompt
                        # _prompt = m.group()
                        # self.logger.debug('output is: %s' % output)
                        _out = re.split(_exp, output, maxsplit=1)
                        _output = _out[0]
                        self.logger.debug("output match prompt '%s', output is: %s" % (_exp, _output))
                        return i, m, _output

            rest_timeout = max_time - time.time()

            if rest_timeout <= 0:
                self.logger.debug('wait prompt timeout, wait time = %s, prompt = %s, output is: %s' % (str(_timeout), expected, output))
                break

        return -1, None, output

    def one_time_command(self, cmd='', timeout=None):
        return self._session.one_time_command(cmd, timeout)

    def close(self):
        raise NotImplementedError()
