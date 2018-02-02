from cafe.core.logger import CLogger
from ssh import SSHDriver, SSHHandle
import collections
import re
from cafe.app import App

_module_logger = CLogger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

class EXASSHDriver(SSHDriver):
    default_prompt = collections.OrderedDict(
        [(r"\-\-[Mm][Oo][Rr][Ee]\-\-", ""),
         (r"[^\r\n\(\)\:\~]+\#", None),
         (r"[^\r\n]+\)\:", None),
         (r"[^\r\n]+\#", None),
         ]
    )

    top_prompt = r"[^\r\n\(\)\:\~]+\#"
    keywords = ['config']
    error_response = r"error\:"

    def open_handle(self):
        if self._is_handle_opened():
            return

        super(EXASSHDriver, self)._open_handle()

        info('open exa_ssh in ssh handle')
        self._handle.session_command('')
        if 'root' in self._handle.current_prompt:
            self._handle.session_command('cli')

    def cmd(self, msg, prompt=None, timeout=None, newline=None, *args, **kwargs):
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
        resp = self._handle.session_command(msg, prompt, timeout, newline, *args, **kwargs)
        self._error_response_hook(resp['value'])
        return resp

    def _error_response_hook(self, buf):
        m = re.search(self.error_response, buf)
        if m:
            App().logger.debug("\n")
            App().logger.debug("Response contain %s" % self.error_response)
            for b in buf.splitlines():
                App().logger.debug(b)
            App().logger.debug("\n")

    def top(self):
        self.open_handle()
        self._handle.session_command('')
        if not re.search(self.top_prompt, self._handle.current_prompt, flags=re.I):
            self._handle.session_command('end')

    def session_command(self, *args, **kwargs):
        self.open_handle()
        c = str(args[0]).strip().lower()
        if any(c in s for s in self.keywords):
            self.top()
        return self.cmd(*args, **kwargs)

    cli = session_command

    command = session_command

