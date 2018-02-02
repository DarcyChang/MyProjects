__author__ = 'akhanov'

import winexe
from winexe import _PROMPT


class TCLRemoteShell(winexe.WinExeSession):
    """A session to allow TCL interaction over a WinExe Session
    """
    _TCLPROMPT = [r"[\r\n]%"]

    def __init__(self, winhost, winuser, winpassword, tcl_prompt=_TCLPROMPT, tcl_shell="tclsh85.exe", sid=None,
                 winexe="winexe", host="localhost", port=22, user="cafetest", password="cafetest",
                 prompt=_PROMPT, timeout=120, **kwargs):
        """Initialize a WinExeSession object

        Args:
            winhost (str): The IP address or hostname of the Windows host
            winuser (str): The username of the Windows user to connect to. You may need to use the domain name if the
                user is networked, for example: CALIX/akhanov
            winpassword (str): The password of the Windows user
            tcl_prompt (Optional[str]): Defaults to '%\s+$' (The regular expression to match the TCL shell prompt). The
                regular expression which matches the set prompt.
            tcl_shell (Optional[str]): Defaults to 'tclsh85.exe'. The path of the TCL shell to use. Override this if you
                want a shell different from 'tclsh85.exe', for example, 'tclsh84.exe'
            sid (Optional[str]): Defaults to None. The Session ID to assign to this session.
            winexe (Optional[str]): Defaults to 'winexe'. The path of the winexe executable.
            host (Optional[str]): Defaults to 'localhost'. The IP address or hostname of the host to connect from. In
                most cases, you will not need to set this parameter and subsequent parameters.
            port (Optional[int]): Defaults to 22. The SSH port of the host to connect from
            user (Optional[str]): Defaults to 'cafetest'. The username of the host to connect from.
            password (Optional[str]): Defaults to 'cafetest'. The password of the host to connect from.
            prompt (Optional[str]): Defaults to '[^\r\n]+((\%)|(\$)|(\#))' (The regular expression to match a linux bash
                prompt). The regular expression which matches the prompt of the host to connect from.
            timeout (Optional[int]): Defaults to 60. The default number of seconds to wait for the prompt before moving
                on.
            **kwargs: Any additional arguments to pass to the session initializer

        """
        super(TCLRemoteShell, self).__init__(winhost, winuser, winpassword, tcl_prompt, tcl_shell, sid, winexe,
                                             host, port, user, password, prompt, **kwargs)

        self.__timeout = timeout

        self.write("set tcl_interactive 1", crlf="\r")
        self.expect_prompt()

    def command(self, cmd="", crlf="\r", timeout=None, status_only=True):
        """Sends a command to the session. The command can be any string accepted by the specified winshell ('cmd' by
        default). Returns the response.

        Args:
            command (Optional[str]): Defaults to "" (empty string). The command to send to the session
            crlf (Optional[str]): Defaults to '\r'. The return character sequence which will be appended to the end of
                the command. Different shells might require different crlf's.
            timeout (Optional[int]): Defaults to None. Number of seconds to wait for the prompt to appear before moving
                on. If you expect your command to take some time to execute, you should increase this value. If this
                argument is set to None, the default timeout (specified in the class constructor) will be used.

        Returns:
            tuple: (int, re.match, str). The first value of the tuple is an integer specifying the number of prompt
                matches found. Ideally, this should be 1. If it is equal to -1, the prompt has not been found after
                waiting for the specified timeout. The second value (match object) contains strings which were matched
                by the prompt regular expression. Finally, the string contains the text of the response to the command.

        """
        if timeout is None:
            timeout = self.__timeout

        self.write(cmd, crlf)
        ret = self.expect_prompt(timeout=timeout)
        out = ret[2].split(crlf + "\r\n")
        first_line = out[0].split("\r\n")[-1]
        if status_only == True:
            final = (first_line + "\n" + "\n".join(out[1:])).strip()
            return ret[0], ret[1], final
        else:
            return ret[0], ret[1], ret[2]


if __name__ == "__main__":
    tcl = TCLRemoteShell("192.168.102.103", "cafetest", "Zaq1@wsx")

    print(tcl.command("puts {HELLO WORLD FROM TCL}"))
    print(tcl.command("puts {ANOTHER HELLO}"))
    #print(tcl.command("puts {DONE WAITING}"))
    x = tcl.command("puts {%%% %% %% }")
    print x[1].groups()
    print x[1].group(0)
    print(tcl.command("puts {prompt}"))