#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections

import cafe
from cafe.app.driver.proto.base import DriverBase
from cafe.core.logger import CLogger
from cafe.core.signals import SESSION_SHELL_TIMEOUT

__author__ = 'David Qian'

"""
Created on 01/11/2016
@author: David Qian

"""


_module_logger = CLogger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


class ShellTimeoutException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_SHELL_TIMEOUT)


class ShellDriver(DriverBase):
    default_prompt = collections.OrderedDict(
        [(r"\-\-[Mm][Oo][Rr][Ee]\-\-", ""),
        (r"[^\r\n]+\#", None),
        (r"[^\r\n]+\>", None),
        (r"[^\r\n]+\$", None),
        (r"[^\r\n]+\:\~\$", None),
        (r"[^\r\n]+(\%)", None),
        ]
    )

    def __init__(self, session, name, default_timeout, crlf):
        self._session = session
        self._default_timeout = default_timeout
        self._crlf = crlf
        self._name = name

    def __repr__(self):
        return str(self._name)

    @property
    def crlf(self):
        return self._crlf

    @property
    def default_timeout(self):
        return self._default_timeout

    def session_command(self, *args, **kwargs):
        """compatible with old usage

        Args:
            *args:
            **kwargs:

        Returns:

        """
        raise NotImplementedError()

    def one_time_command(self, *args, **kwargs):
        """compatible with old usage

        Args:
            *args:
            **kwargs:

        Returns:

        """
        raise NotImplementedError()

    def cli(self, *args, **kwargs):
        """compatible with old usage

        Args:
            *args:
            **kwargs:

        Returns:

        """
        raise NotImplementedError()

    def change_credential(self, user_id, user_password, prompt=None):
        self.close_handle()
        self._session.change_credential(user_id, user_password, prompt)

    def login(self):
        self._session.login()

class ShellHandle(object):
    """An entity which created by driver

    """

    def __init__(self, parent, entity):
        self._parent = parent
        self._entity = entity
        self._prompt = []
        self._action = []
        self._default_prompt = parent.default_prompt
        self._default_timeout = parent.default_timeout
        self._crlf = parent.crlf
        self.current_prompt = None
        self.msg = None
        self.buf = None

    def _set_prompt(self, prompt):
        d = {}
        # priority use handle prompt
        if prompt is None:
            prompt = self._entity.prompt

        if prompt is None:
            d = self._default_prompt
        elif isinstance(prompt, (str, unicode)):
            d = {str(prompt): None}
        elif isinstance(prompt, list):
            d = {str(i): None for i in prompt}
        elif isinstance(prompt, dict):
            d = {str(k): v for k, v in prompt.iteritems()}

        self._prompt = d.keys()
        self._action = d.values()
        # default add '--MORE--' action
        self._prompt.append(r'\-\-[Mm][Oo][Rr][Ee]\-\-')
        self._action.append(' ')

        return self._prompt, self._action

    def _fix_timeout(self, timeout):
        if timeout is None:
            timeout = self._entity.timeout

        if timeout is None:
            timeout = self._default_timeout

        return timeout

    def _execute_cmd(self, cmd, timeout, newline):
        """
        send command to session (for internal use only)

        Args:
            cmd (str): message sent to session
            timeout (float): max wait time if prompt is not found

        Returns:
            None: command is executed finish
            not None: the next command need to execute
        """
        debug('command is {}, prompt is {}, action is {}'.format(cmd, self._prompt, self._action))
        crlf = self._crlf
        if newline is not None:
            crlf = newline

        r = self._entity.command(cmd, prompt=self._prompt, timeout=timeout, crlf=crlf)

        self.buf += r[2]
        try:
            self.current_prompt = r[1].group()
        except Exception:
            # does not match any prompt, ignore the exception
            pass

        if r[0] < 0:
            warn('expect prompt timeout(%s)' % (str(timeout),))
            #in case of timeout, wait for a little bit more time to clean up the buffer
            r = self._entity.expect(expected=self._prompt, timeout=0.1)
            self.buf += r[2]
            error("Execute command '%s' timeout" % cmd)

            return None, True
        else:
            debug('recv prompt is {}, action is {}'.format(self._prompt[r[0]], self._action[r[0]]))
            return self._action[r[0]], False

    def _session_cmd(self, msg, prompt=None, timeout=None, newline=None, *args, **kwargs):
        """
        Send message to session.

        This method will try to maintain the
        session connectivity and login status (best effort only)

        Args:
            msg (str): message sent to session
            prompt: regexp of prompt or list of regexp of prompts or dict of prompt,action value pairs
            timeout: max wait time to the prompt to be found

        Return:
            dict of {"prompt": <prompt being found>, "value", <session response>, "content", <session response>}

        Note:
            The return dictionary has key value and content.
            They are duplicate to maintain compatibility of MadMachine script.
        """

        self.msg = msg
        timeout = self._fix_timeout(timeout)

        self.buf = ""
        self._set_prompt(prompt)

        next_cmd = msg
        while next_cmd is not None:
            next_cmd, timeout_status = self._execute_cmd(next_cmd, timeout, newline)

            if timeout_status:
                if float(timeout) != 0:
                    return {"prompt": self.current_prompt, "value": self.buf, "content": self.buf, 'timeout': timeout}
                else:
                    return {"prompt": self.current_prompt, "value": self.buf, "content": self.buf}
            # Customer specified newline just take effect once.
            # That means when we type ? (without newline), then the help page is paging, so we read --MORE--,
            # then we need to send a space to it, so once the command executed, discard customer specified newline.
            newline = ''

        return {"prompt": self.current_prompt, "value": self.buf, "content": self.buf}

    def _one_time_cmd(self, msg, timeout=None):
        self.msg = msg
        timeout = self._fix_timeout(timeout)

        return {'content': self._entity.one_time_command(msg, timeout)}

    @cafe.teststep("send command")
    def session_command(self, *args, **kwargs):
        return self._session_cmd(*args, **kwargs)

    command = session_command

    cli = session_command

    @cafe.teststep("send one-time command")
    def one_time_command(self, *args, **kwargs):
        return self._one_time_cmd(*args, **kwargs)

    def close(self):
        self._entity.close()

    def is_opened(self):
        raise NotImplementedError
