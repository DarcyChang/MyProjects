import threading
import sys
import os
import string
from types import TypeType
import rpyc
from cafe import get_config
from rpyc.utils.registry import TCPRegistryServer
from rpyc.utils.factory import _get_free_port


from cafe.sessions.ssh import SSHSession
from cafe.sessions.snmp import SnmpSession
from cafe.core.logger import CLogger as Logger, DEFAULT_LOGGER_CONFIG
from cafe.core.signals import SESSION_SERVER_ERROR
from telnet import TelnetSession
from webgui import WebGuiSession
from shell import ShellSession
from ncsession import NetConfSession
from tclsession import TclSession
from restapi import RestfulSession
from cafe.core.decorators import mem_debug
import cafe

__author__ = 'kelvin'

_logger = Logger(__name__)
info = _logger.info
debug = _logger.debug

# _logger.add_robot_logger_handler()

class SessionException(Exception):
    def __init__(self, msg=""):
        _logger.exception(msg, signal=SESSION_SERVER_ERROR)


class SessionPool(object):
    """Class/object to hold the session objects of session server
    """

    def __init__(self):
        self.sessions = {}
        self.lock = threading.RLock()

    def add(self, name, obj):
        """Add session in sessions dictionary

        Args:
            name (str): name reference of session object
            obj (object): session object
        """
        if name in self.sessions:
            raise SessionException("name (%s) already exist" % name)
        with self.lock:
            self.sessions[name] = obj

    def remove(self, name):
        """remove session object
        Args:
            name (str): name reference of session object
        Return
            session object
        """
        with self.lock:
            s = self.sessions.pop(name)
        return s

    def get(self):
        """return the sessions dictionary structure
        """
        return self.sessions


class CafeSessionService(rpyc.Service):
    """Base class for rpyc service

    """
    _session_log_base_path = "/tmp"

    @mem_debug()
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        info("session server connected!!!")
        self.session_pool = SessionPool()
        pass

    def on_disconnect(self):
        # code that runs when disconnect
        self.remove_sessions()
        self.session_pool = None

    #@mem_debug()
    def remove_session(self, sid):
        """Remove session by sid/name
        """
        session_pool = self.session_pool
        sids = session_pool.sessions.keys()[:]
        if sid in sids:
            s = session_pool.remove(sid)
            # close the session
            s.close()


    @mem_debug()
    def remove_sessions(self):
        """Remove all sessions
        """
        session_pool = self.session_pool
        sids = session_pool.sessions.keys()[:]
        for sid in sids:
            s = session_pool.remove(sid)
            # close the session
            s.close()


    def getsockname(self):
        """return tuple of (host, ip port) of Networked RPYC service
        """
        host, port = self._conn._channel.stream.sock.getsockname()
        info("getsockname %s" % str((host, port)))
        return (host, port)


    def get_sessions(self):
        session_pool = self.session_pool
        return session_pool.sessions

    # def exposed_thread_count(self):
    #     return threading.active_count()


    def set_session_log_base_path(self, path):
        """set the log base path for the server
        """
        self._session_log_base_path = os.path.expanduser(path)

    def _get_session_log_path(self, session_name):
        return os.path.join(self._session_log_base_path, "%s.log" % session_name)

    def get_ssh_session(self, sid=None, term="vt100", width=400, height=80, logfile=None, log_level=None, **kwargs):
        t = SSHSession(sid=sid, term=term, width=width, height=height, logfile=logfile,
                       logger=_logger.get_child(sid), log_level=log_level, **kwargs)

        session_pool = self.session_pool
        session_pool.add(sid, t)
        return t

    def get_webgui_session(self, sid=None, logfile=None, webdriver_log=None, **kwargs):
        t = WebGuiSession(sid=sid, logfile=logfile, logger=_logger.get_child(sid), **kwargs)
        session_pool = self.session_pool
        session_pool.add(sid, t)
        t.set_webdriver_log(webdriver_log)
        return t

    def get_netconf_session(self, sid=None, host=None, port=830, user=None,
                                    password=None, timeout=30, logfile=None, **kwargs):
        t = NetConfSession(sid=sid, host=host, port=port, user=user, password=password, timeout=timeout,
                           logfile=logfile, **kwargs)
        # print "====>", sid
        session_pool = self.session_pool
        session_pool.add(sid, t)
        return t

    def get_telnet_session(self, sid=None, logfile=None, log_level=None, **kwargs):
        t = TelnetSession(sid=sid, logfile=logfile,
                          logger=_logger.get_child(sid), log_level=log_level, **kwargs)
        session_pool = self.session_pool
        session_pool.add(sid, t)
        return t

    def get_tcl_session(self, sid=None, logfile=None, **kwargs):
        t = TclSession(sid=sid, logfile=logfile, logger=_logger.get_child(sid), **kwargs)
        session_pool = self.session_pool
        session_pool.add(sid, t)
        return t

    def get_restful_session(self, sid=None, user="", password="", timeout=3.0, logfile=None, **kwargs):
        d = locals()
        d.pop("self")
        t = RestfulSession(**d)
        session_pool = self.session_pool
        session_pool.add(sid, t)
        return t

    def get_snmp_session(self, sid=None, host="", port=161, version="2c", **kwargs):
        s = SnmpSession(sid=sid, host=host, port=port, version=str(version), **kwargs)
        self.session_pool.add(sid, s)
        return s

    def get_shell_session(self, sid=None, host='localhost', port=22, user='cafetest', password='cafetest',
                                  prompt=[r"[^\r\n]+(\$|\>|\#)"], connect_timeout=3.0, timeout=3.0, term="vt100",
                                  width=400, height=80,
                                  enable_log=True, logfile=None, ssh_tool_log=None, **kwargs):

        d = locals()
        d.pop("self")
        t = ShellSession(**d)
        t.open_entity()
        t.set_prompt()
        session_pool = self.session_pool
        session_pool.add(sid, t)
        return t

    def create_session(self, session_name=None, session_type=None, device_type=None, **kwargs):
        info("create_session: %s, %s, %s" % (session_name, session_type, str(kwargs)))

        session_name = str(session_name).lower()
        session_type = str(session_type).lower()

        session_log = self._get_session_log_path(session_name)
        session = None
        self.__update_session_timeout_by_type(session_name, session_type, kwargs)

        if session_type == "telnet":
            # self, sid=None, host=None, port=_PORT, user=None, password=None,
            #  prompt=_PROMPT, login_prompt="ogin:", password_prompt="word:", connect_timeout=_CONNECT_TIMEOUT,
            #  login_timeout=2, term=_TERM, width=_WIDTH, height=_HEIGHT, enable_log=True, logfile=None, **kwargs
            if device_type is None:
                pass
            elif device_type == "e7":
                if "login_prompt" not in kwargs: kwargs["login_prompt"] = "Username:"
                if "prompt" not in kwargs: kwargs["prompt"] = [r"[^\r\n]+(\>)"]
            session = self.get_telnet_session(sid=session_name, logfile=session_log, **kwargs)

        if session_type == "ssh":
            session = self.get_ssh_session(sid=session_name, logfile=session_log, **kwargs)

        if session_type == "webgui":
            webdriver_log = self._get_session_log_path("webdriver")
            session = self.get_webgui_session(sid=session_name, logfile=session_log, webdriver_log=webdriver_log,
                                              **kwargs)

        if session_type == "shell":
            session = self.get_shell_session(sid=session_name, logfile=session_log, **kwargs)

        if session_type == "tcl":
            session = self.get_tcl_session(sid=session_name, logfile=session_log, **kwargs)

        if session_type == "netconf":
            session = self.get_netconf_session(sid=session_name, logfile=session_log, **kwargs)

        if session_type == "restful":
            session = self.get_restful_session(sid=session_name, logfile=session_log, **kwargs)
        
        if session_type == "snmp":
            session = self.get_snmp_session(sid=session_name, logfile=session_log, **kwargs)

        if session:
            return session
        else:
            raise SessionException("session server not able to create session (%s)" % session_name)

    def __update_session_timeout_by_type(self, session_name, session_type, params):
        config = get_config()
        _session_timeout_map = {
            'telnet': config.timeout.cli_timeout,
            'ssh': config.timeout.cli_timeout,
            'shell': config.timeout.cli_timeout,
            'netconf': config.timeout.netconf_timeout,
            'snmp': config.timeout.snmp_timeout,
            'tcl': config.timeout.trafficgen_timeout,
            'webgui': config.timeout.webgui_timeout,
            'restful': config.timeout.restful_timeout,
        }

        new_timeout = None

        if _session_timeout_map[session_type] != -1:
            new_timeout = _session_timeout_map[session_type]
        elif config.timeout.default_global_timeout != -1:
            new_timeout = config.timeout.default_global_timeout

        if new_timeout is not None:
            params['timeout'] = new_timeout
            debug("update session '%s' timeout to %d seconds" % (session_name, new_timeout))


class NetworkSessionService(CafeSessionService):
    """Implementation of rpyc Session Service. It is intended to be used by Networked RPYC server
    """

    #create aliases to expose methods via rpyc
    exposed_remove_session = CafeSessionService.remove_session
    exposed_remove_sessions = CafeSessionService.remove_sessions
    exposed_getsockname = CafeSessionService.getsockname
    exposed_get_sessions = CafeSessionService.get_sessions
    exposed_set_session_log_base_path = CafeSessionService.set_session_log_base_path
    exposed_get_ssh_session = CafeSessionService.get_ssh_session
    exposed_get_webgui_session = CafeSessionService.get_webgui_session
    exposed_get_netconf_session = CafeSessionService.get_netconf_session
    exposed_get_telnet_session = CafeSessionService.get_telnet_session
    exposed_get_tcl_session = CafeSessionService.get_tcl_session
    exposed_get_restful_session = CafeSessionService.get_restful_session
    exposed_get_shell_session = CafeSessionService.get_shell_session
    exposed_create_session = CafeSessionService.create_session

class LocalSessionService(CafeSessionService):
    """Implementation of Non-networked Session Server
    """

    # override the parent's constructor & getsockname
    def __init__(self):
        print self
        self.on_connect()

    def getsockname(self):
        """return tuple of (host, ip port) of Networked RPYC service
        """
        info("getsockname %s" % str((None, None)))
        return (None, None)

    #alias
    disconnect = CafeSessionService.on_disconnect

class CafeSessionServer(object):
    """Base Cafe session server
    """

    @staticmethod
    def is_server_type(server_type):
        """
        Note: used by CafeSessionServerFactory to determine what type of Session Server object should be created.
        """
        return False

    def get_server_name(self):
        raise NotImplementedError()

    def create_session(self, session_name="", session_type="", device_type="", **kwargs):
        raise NotImplementedError()

    def remove_session(self, session_name):
        raise NotImplementedError()

    def getsockname(self):
        """return tuple of (host, ip port) of session server
        """
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class RemoteNetworkSessionServer(CafeSessionServer):
    """ RPYC Session Server for remote host(s)
    """
    @staticmethod
    def is_server_type(server_type):
        return str(server_type).lower() in [CafeSessionServerFactory.REMOTE_NETWORK_SERVER]

    def __init__(self, host='0.0.0.0', port=0):
        pid = start_session_server(host, port)
        import time
        time.sleep(2)
        self._conn = rpyc.connect(host, port)
        self.service = self._conn.root

    def create_session(self, session_name="", session_type="", device_type="", **kwargs):
        _session_name = str(session_name).lower()
        _session_type = str(session_type).lower()
        _device_type = str(device_type).lower()
        return self.service.create_session(_session_name, _session_type, _device_type, **kwargs)

    def getsockname(self):
        return self.service.getsockname()

    def remove_session(self, session_name):
        self.service.remove_session(session_name)

    def get_server_name(self):
        return "%s_%s" % self.getsockname()

    def close(self):
        info("session server (%s) is closed" % self.get_server_name())
        self.service.remove_sessions()
        self._conn.close()


class LocalNetworkSessionServer(RemoteNetworkSessionServer):
    """ RPYC Session Server for local host
    """
    @staticmethod
    def is_server_type(server_type):
        return str(server_type).lower() in [CafeSessionServerFactory.LOCAL_NETWORK_SERVER]


class LocalSessionServer(CafeSessionServer):
    """ Non-RPYC Session Server for cafe main/runner interpreter.
    """
    @staticmethod
    def is_server_type(server_type):
        return str(server_type).lower() in [CafeSessionServerFactory.LOCAL_SERVER]

    def __init__(self, host="0.0.0.0", port=0):
        """
        Note:
        host and port are here for make the interface consistence with others
        They are not used
        """
        self.service = LocalSessionService()

    def create_session(self, session_name="", session_type="", device_type="", **kwargs):
        _session_name = str(session_name).lower()
        _session_type = str(session_type).lower()
        _device_type = str(device_type).lower()
        return self.service.create_session(_session_name, _session_type, _device_type, **kwargs)

    def getsockname(self):
        return self.service.getsockname()

    def remove_session(self, session_name):
        self.service.remove_session(session_name)

    def get_server_name(self):
        return CafeSessionServerFactory.LOCAL_SERVER

    def close(self):
        self.service.disconnect()
        info("session server (%s) is closed" % self.get_server_name())


class CafeSessionServerFactory(object):
    """Session Server Factory

    Example:
        >>> local_server = CafeSessionServerFactory.create(CafeSessionServerFactory.LOCAL_SERVER)
        >>> local_net_server = CafeSessionServerFactory.create(CafeSessionServerFactory.LOCAL_NETWORK_SERVER)
        >>> remote_net_server = CafeSessionServerFactory.create(CafeSessionServerFactory.REMOTE_NETWORK_SERVER, host="myhost")

    Note:
        remote_net_server is not tested.

    """
    LOCAL_SERVER = "local_server"
    LOCAL_NETWORK_SERVER = "local_network_server"
    REMOTE_NETWORK_SERVER = "remote_network_server"

    # registry server attributes
    reg_srv = None
    reg_srv_thread = None
    reg_srv_port = 0
    reg_srv_host = '0.0.0.0'

    @staticmethod
    def create(server_type, host=None, port=None, **kwargs):
        """Create Session server by type

        Args:
            server_type (str): one of LOCAL_SERVER, LOCAL_NETWORK_SERVER, REMOTE_NETWORK_SERVER
            host (str): host of session server. For LOCAL_SERVER, LOCAL_NETWORK_SERVER, this value is ignored
            port (int): port of session server. For LOCAL_SERVER, LOCAL_NETWORK_SERVER, this value is ignored

        Return
        """

        #get all classes which are subclass from CafeSessionServer
        klasses = [j for (i, j) in globals().iteritems() if
                   isinstance(j, TypeType) and issubclass(j, CafeSessionServer)]

        for klass in klasses:
            if klass.is_server_type(server_type):
                if port is None or port == 0:
                    _port = _get_free_port()
                else:
                    _port = port
                return klass(host, _port)

        raise SessionException('No server type is "%s".' % server_type)

    @classmethod
    def start_registry_server(cls):
        """Start a rpyc registry server
        """
        if cls.reg_srv is None:
            cls.reg_srv_port = _get_free_port()
            cls.reg_srv = TCPRegistryServer(port=cls.reg_srv_port, logger=_logger.logger)
            t = threading.Thread(name="registry_srv_thread", target=cls.reg_srv.start)
            t.setDaemon(True)
            t.start()
            cls.reg_srv_thread = t
            info("registry server is started (%s)" % str((cls.reg_srv_host, cls.reg_srv_port)))
        else:
            info("registry server is already started (%s)" % str((cls.reg_srv_host, cls.reg_srv_port)))

    @classmethod
    def stop_registry_server(cls):
        """stop a rpyc registry server
        """
        cls.reg_srv.close()
        cls.reg_srv_thread.join(2)
        cls.reg_srv_thread = None
        cls.reg_srv = None
        cls.reg_srv_host = None
        cls.reg_srv_port = 0


def start_session_server(host='0.0.0.0', port=0, server_klass=LocalNetworkSessionServer,
                         logger_config=DEFAULT_LOGGER_CONFIG):
    """Launch a session server as a separate process
    """
    from multiprocessing import Process
    from rpyc.utils.server import OneShotServer
    from cafe.core.logger import init_logging

    def w(host, port):
        # print logger_config
        init_logging()
        _logger = Logger("session_srv%s_%s" % (host, port))
        _logger.set_console(True)
        _logger.set_level("DEBUG")
        _logger.debug("logger config:" + str(logger_config))

        # TODO: get log server host/port info from config.ini
        # from cafe.core.logger import NetworkLogging
        # NetworkLogging.enable(host)

        # Change from ThreadedServer to OneTimeServer
        # OneTimeServer is terminated automatically one the client is disconnected,
        # no need to kill it separately.
        t = OneShotServer(NetworkSessionService, hostname=host, port=port, logger=_logger.logger,
                          protocol_config={"allow_all_attrs": True,
                                           "allow_public_attrs": True,
                                           "allow_setattr": True,
                                           "allow_getattr": True,
                                           "allow_delattr": True,
                                           "allow_pickle": True,
                                           "instantiate_custom_exceptions": True,
                                           "import_custom_exceptions": True,
                                           "propagate_SystemExit_locally": True})
        t.start()

    p = Process(target=w, args=(host, port))
    p.daemon = True
    p.start()
    return p


class Launch(object):
    """A command-line program that runs a set of tests; this is primarily
       for making test modules conveniently executable.
    """
    USAGE = """\
Usage: session_srv [options]

Options:
  -h, --help       Show this message
  -p, --port       port number of server

Examples:
  session_srv                           - run cafe session manger server
"""

    def __init__(self, module='__main__', port=18890, argv=None):
        if type(module) == type(''):
            self.module = __import__(module)
            for part in string.split(module, '.')[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.verbosity = 1
        self.port = port
        self.prog_name = os.path.basename(argv[0])
        self.parse_args(argv)
        self.run_server()

    def usage_exit(self, msg=None):
        if msg: print msg
        print (self.USAGE % self.__dict__)
        sys.exit(2)

    def parse_args(self, argv):
        import getopt

        try:
            # print argv[1:]
            options, args = getopt.getopt(argv[1:], 'hH:p:',
                                          ['help', 'port='])
            for opt, value in options:
                if opt in ('-h', '-H', '--help'):
                    self.usage_exit()
                if opt in ('-p', '--port'):
                    self.port = int(value)

        except getopt.error, msg:
            self.usage_exit(msg)

    def run_server(self):
        from rpyc.utils.server import OneShotServer
        import logging
        FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        logging.basicConfig(format=FORMAT)
        logger = logging.getLogger("server")
        logger.setLevel("DEBUG")
        t = OneShotServer(NetworkSessionService, port=self.port, logger=logger,
                          protocol_config={"allow_all_attrs": True,
                                           "allow_public_attrs": True,
                                           "allow_setattr": True,
                                           "allow_getattr": True,
                                           "allow_delattr": True,
                                           "allow_pickle": True,
                                           "instantiate_custom_exceptions": True,
                                           "import_custom_exceptions": True,
                                           "propagate_SystemExit_locally": True})
        t.start()

        # import time
        # time.sleep(5)
        # t.close()


main = Launch

if __name__ == "__main__":
    pass
    main(module=None)
    # import time
    # s = start_session_server()
    # print (s.pid)
    # time.sleep(5)
    # s.terminate()
