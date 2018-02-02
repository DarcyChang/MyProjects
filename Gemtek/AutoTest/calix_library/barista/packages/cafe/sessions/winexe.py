__author__ = 'akhanov'

from cafe.sessions.shell import ShellSession
from cafe.sessions.shell import _PROMPT
from cafe.core.signals import SESSION_WINEXE_LOGIN_FAILED
import platform

class WinExeSessionLoginException(Exception):
    """An exception which is raised when a WinExeSession login attempt fails
    """
    def __init__(self, logger, msg=""):
        """Initalizes the exception

        Args:
            logger (CLogger): The logger to log the exception to
            msg (Optional[str]): Defaults to "" (empty string). The message to show.

        """
        logger.exception(msg, signal=SESSION_WINEXE_LOGIN_FAILED)


class WinExeSession(ShellSession):
    """A WinExe session which allows to execute commands on a remote Windows machine
    """
    _WINPROMPT = [r"[a-zA-Z]\:.*\>$"]
    _LOGON_FAIL = "ERROR: Failed to open connection - NT_STATUS_LOGON_FAILURE"

    def __init__(self, winhost, winuser, winpassword, winprompt=_WINPROMPT, winshell="cmd", sid=None,
                 winexe="winexe", host="localhost", port=22, user="cafetest", password="cafetest",
                 prompt=_PROMPT, **kwargs):
        """Initialize a WinExeSession object

        Args:
            winhost (str): The IP address or hostname of the Windows host
            winuser (str): The username of the Windows user to connect to. You may need to use the domain name if the
                user is networked, for example: CALIX/akhanov
            winpassword (str): The password of the Windows user
            winprompt (Optional[str]): Defaults to '[a-zA-Z]\:.*\>$' (The regular expression to match a Windows CMD
                prompt). The regular expression which matches the set prompt.
            winshell (Optional[str]): Defaults to 'cmd'. The command (usually a shell) to execute upon login. Note:
                PowerShell is currently not supported
            sid (Optional[str]): Defaults to None. The Session ID to assign to this session.
            winexe (Optional[str]): Defaults to 'winexe'. The path of the winexe executable.
            host (Optional[str]): Defaults to 'localhost'. The IP address or hostname of the host to connect from. In
                most cases, you will not need to set this parameter and subsequent parameters.
            port (Optional[int]): Defaults to 22. The SSH port of the host to connect from
            user (Optional[str]): Defaults to 'cafetest'. The username of the host to connect from.
            password (Optional[str]): Defaults to 'cafetest'. The password of the host to connect from.
            prompt (Optional[str]): Defaults to '[^\r\n]+((\%)|(\$)|(\#))' (The regular expression to match a linux bash
                prompt). The regular expression which matches the prompt of the host to connect from.
            **kwargs: Any additional arguments to pass to the session initializer

        """
        self.__winhost = winhost
        self.__winuser = winuser
        self.__winpassword = winpassword
        self.__winprompt = winprompt
        self.__winexe = winexe
        self.__other_args = kwargs
        self.__winshell = winshell

        self._logged_in = False

        super(WinExeSession, self).__init__(sid=sid, host=host, port=port, user=user,
                                            password=password, prompt=prompt, **kwargs)

    def login(self):
        """Login into the WinExe session. This method is automatically called by the constructor, so you do not need to
        call it explicitly.

        """
        if not self._logged_in:
            super(WinExeSession, self).login()
            login_str = "%s -U %s%%%s //%s %s" % (self.__winexe, self.__winuser, self.__winpassword,
                                                  self.__winhost, self.__winshell)

            self.session_log.console = True
            self.session_log.set_level("TRACE")

            self.set_prompt(self.__winprompt)
            self.write(login_str)
            result = self.expect_prompt(timeout=10)

            if self._LOGON_FAIL in result[2]:
                raise WinExeSessionLoginException(self.session_log, "Login failed: %s" % self._LOGON_FAIL)

            self._logged_in = True

    def command(self, command="", crlf="\r", timeout=None):
        """Sends a command to the session. The command can be any string accepted by the specified winshell ('cmd' by
        default). Returns the response.

        Args:
            command (Optional[str]): Defaults to "" (empty string). The command to send to the session
            crlf (Optional[str]): Defaults to '\r'. The return character sequence which will be appended to the end of
                the command. Different shells might require different crlf's.
            timeout (Optional[int]): Defaults to 5. Number of seconds to wait for the prompt to appear before moving on.
                If you expect your command to take some time to execute, you should increase this value.

        Returns:
            tuple: (int, re.match, str). The first value of the tuple is an integer specifying the number of prompt
                matches found. Ideally, this should be 1. If it is equal to -1, the prompt has not been found after
                waiting for the specified timeout. The second value (match object) contains strings which were matched
                by the prompt regular expression. Finally, the string contains the text of the response to the command.

        """
        res = super(WinExeSession, self).command(command, crlf, timeout=timeout)
        out = res[2].split(crlf + "\r\n")
        first_line = out[0].split("\r\n")[-1]
        final = (first_line + "\n" + "\n".join(out[1:])).strip()

        return res[0], res[1], final

    def scp(self, remote_file, dest_file, dest_host=None, dest_user=None,
            dest_password=None, timeout=None, scp_tool="c:/cafe/tools/bin/pscp.exe"):
        """Secure copy.
        Secure copy using pscp tool

        To install pscp, please follow the instruction in http://wiki.calix.local/pages/viewpage.action?pageId=45744232

        Args:
            remote_file: remote file name. file in the remote windows env
            dest_file: destination file name.
            dest_host: host of destination file. default: None; it take the hostname of the Cafe VM.
            dest_user: destination host user. default: None; it take the same user value of the winexe session.
            dest_password: destination host user's password None; it take the same password of the winexe sesion
            timeout: scp timeout value
            scp_tool: The windows pscp tool pathname. default is c:/cafe/tools/bin/pscp.exe

        Returns:
            dict of status: "{"status": bool, "error": None or <error description>, "response": <text>}"

        Example:
            >>> c = WinExeSession("192.168.1.100", "cafetest", "cafetest")
            >>> c.login()
            >>> r = c.scp("c:/temp/cap.pcap", "cap.pcap", dest_host="cafe-vm", dest_user="cafeuser",
            >>>      dest_password="calix123", timeout=20)
            >>> print (r)

        """
        if dest_user is None:
            dest_user = self.user

        if dest_password is None:
            dest_password = self.password

        if dest_host is None:
            dest_host = platform.node()

        if timeout is None:
            timeout = self.timeout

        self.write("%s -l %s -pw %s %s %s:%s" % (scp_tool, dest_user, dest_password, remote_file, dest_host, dest_file))

        _expected = self.__winprompt
        _expected.append(r"word:")
        _expected.append(r"Store key in cache\?")

        print (_expected)
        r = self.expect(expected=_expected, timeout=timeout)

        if r[0] == 2:
            self.write("n")
            r = self.expect(expected=_expected, timeout=timeout)

        if r[0] == 0:
            #return {"status": True, "response": r[2]}
            if "No such file or directory" in r[2]:
                return {"status": False, "error": "No such file or directory", "response": r[2]}
            return {"status": True, "error": None, "response": r[2]}
        elif r[0] == 1:
            return {"status": False, "error": "invalid password", "response": r[2]}
        else:
            return {"status": False, "error": "timeout", "response": r[2]}



if __name__ == "__main__":
    # c = WinExeSession("192.168.102.41", "Administrator", "CafeTest123!")
    # c.login()
    #
    # print(c.command("echo HELLO")[2])
    # print(c.command("echo HELLO AGAIN")[2])
    # print(c.command("echo HELLO & echo FROM & echo NEWLINE")[2])
    # c.close()

    c = WinExeSession("192.168.1.100", "cafetest", "Zaq1@wsx")
    c.login()
    #r = c.scp("c:/temp/winexe", "winexe", dest_host="sjclnx-cafe01", dest_user="kelee",
    #      dest_password="calix123", timeout=90)
    r = c.scp("c:/temp/cap.pcap", "cap.pcap", dest_host="sjclnx-cafe01", dest_user="kelee",
         dest_password="calix123", timeout=20)
    print (r)
    c.close()





