"""
create a cafetest user in the environment
use ssh for shell
"""

from ssh import _SSHSession
from ssh import _TIMEOUT

_PROMPT = [r"[^\r\n]+((\%)|(\$)|(\#))"]
class _Shell(_SSHSession):
    def __init__(self, sid=None, host="localhost", port=22, user="cafetest", password="cafetest",
            prompt=_PROMPT, **kwargs):

        #fix the input arguments for SSHSession
        d = locals()
        d.pop('self')
        k = d.pop("kwargs")
        d.update(k)

        _SSHSession.__init__(self, **d)
        self.login()

ShellSession = _Shell
# if __name__ == "__main__":
#     from cafe.core.logger import init_logging
#
#     init_logging()
#     s = _Shell(sid="shell", width=400, height=80, logfile="shell.log")
#     print(s.command("pwd"))
#     print(s.command("ls"))
#     print(s.command("ps aux", timeout=10))
#     s.set_prompt()
#     print(s.command("ps aux", timeout=10))
#     print(s.command("tclsh"))
#     s.set_prompt()
#     print(s.command("echo $tcl_version"))
#     print(s.command("set i 1"))
#     print(s.command("puts $i"))




