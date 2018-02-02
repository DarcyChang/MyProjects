from docutils.nodes import sidebar

__author__ = 'akhanov'

from cafe.sessions.telnet import TelnetSession
from cafe.sessions.ssh import SSHSession


class MRV_PLS(object):
    """Equipment library for the MRV Physical Layer Switch
    """
    def __init__(self, chassis_ip, port=22, user=None, password=None, sid=None):
        """Constructor of the MRV_PLS class

        Args:
            chassis_ip (str): The IP address or hostname of the MRV Switch chassis
            port (Optional[int]): Default: 22. The SSH port of the MRV Switch chassis
            user (Optional[str]): Default: None. The username to log in as
            password (Optional[str]): Default: None. The password of the user
            sid (Optional[str]): Default: None. The session name to give to the SSH session

        """
        self._session = SSHSession(sid=sid, host=chassis_ip, port=port, user=user, password=password)

        """
        self._session.session_log.set_level("TRACE")
        self._session.session_log.console = True
        """

        self._session.login()

    def map_port_pair(self, port1, port2):
        self.command("config term")

        self.__clear_connections([port1, port2])

        self.command("map %s with %s" % (port1, port2))

        self.command("port %s" % port1)
        self.command("no shutdown")
        self.command("lin")
        self.command("exit")

        self.command("port %s" % port2)
        self.command("no shutdown")
        self.command("lin")
        self.command("exit")

        self.command("exit")

    def clear_connections(self, ports):
        self.command("config term")
        self.__clear_connections(ports)
        self.command("exit")

    def __clear_connections(self, ports):
        for port in ports:
            self.command("map %s clear-all" % port)

    def command(self, comm):
        return self._session.command(comm)

    def close(self):
        self.command("exit")
        self._session.close()


if __name__ == "__main__":
    mrv = MRV_PLS("10.243.66.103", user="admin", password="admin")
    mrv.map_port_pair("1.1.28", "1.1.31")
    mrv.clear_connections(["1.1.28", "1.1.31"])
    mrv.close()


