__author__ = 'kelvin'
"""
create a cafetest user in the environment
use ssh for tcl session
"""
from ssh import _SSHSession
from ssh import _TIMEOUT
from cafe.core.logger import CLogger as Logger
from cafe.core.signals import SESSION_TCL_ERROR

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error

class TclSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_TCL_ERROR)

_PROMPT = [r"[^\r\n]+(\%)"]
class _TclSession(_SSHSession):
    """
    Tcl Session
    """
    def __init__(self, sid=None, host="localhost", port=22, user="cafetest", password="cafetest",
            prompt=None, shell="bash", tclsh="/usr/bin/tclsh", logger=Logger(__name__), tcl_lib_path="", **kwargs):

        self.shell = shell
        self.tclsh = tclsh
        self.tcl_lib_path = tcl_lib_path

        _SSHSession.__init__(self, sid=sid, host=host, port=port, user=user, password=password, prompt=prompt,
                             logger=logger, **kwargs)
        self.login()
        self.open_entity()
        # self.set_prompt()
        self.command(self.shell)
        # self.set_prompt()
        self.command(self._get_tcl_lib_path())

        if kwargs.has_key('hlt_version'):
            self.command('export IXIA_VERSION={}'.format(kwargs['hlt_version']))

        self.command("mkdir -p ~/traffic/working")
        self.command("cd ~/traffic/working")

        self.command(self.tclsh)
        self.set_prompt()
        self.command('set tcl_interactive 1')

        #this should ensure the prompt appears
        self.command('set tcl_interactive 1', timeout=1)
        self.set_prompt()

    def command(self, cmd='', prompt=None, timeout=None, newline=None):
        res = super(_TclSession, self).command(cmd, prompt, timeout, newline)
        if res[0] == -1:
            raise TclSessionException('TCL Session Timeout.')
        return res

    def _get_tcl_lib_path(self):
        if self.shell == "bash":
            return "export TCLLIBPATH=%s" % self.tcl_lib_path
        else:
            raise TclSessionException("tcl lib path setting for %s not implemented" % self.shell)


TclSession = _TclSession
if __name__ == "__main__":
    from cafe.core.logger import init_logging

    init_logging()
    s = TclSession(sid="tcl", tclsh='/opt/active_tcl/bin/tclsh', width=400, height=80)
    s.logger.enable_file_logging("tcl.log")
    print(s.command("echo $tcl_version"))
    print(s.command("set i 1"))
    #print(s.command("puts $i"))
    r = s.command("puts $i")
    print(r[1].group())
    print s.command("echo $auto_path")
    print s.command("package req SpirentHltApi", timeout=30)
