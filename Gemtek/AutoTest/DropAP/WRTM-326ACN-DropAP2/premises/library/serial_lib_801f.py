import cafe
from cafe.sessions.telnet import *
from cafe.core.logger import init_logging


class SerialConsoleTelnetSession(TelnetSession):
    def pre_actions(self):
        init_logging()
        cafe.Checkpoint(str(self.is_connected())).verify_contains("True")
        self.command("\n")
        self.command("exit")
        self.command("\n")
        self.login()

    def post_actions(self):
        self.command("exit")
        result = self.command("\n")
        result = re.search('com login: $', result[2])
        cafe.Checkpoint(str(result.group())).verify_regex(exp="login: $", pos_msg="re found!", neg_msg="re not found")
        self.close()
