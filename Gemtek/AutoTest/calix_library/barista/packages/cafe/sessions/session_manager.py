from collections import namedtuple
import sys
import weakref
import cafe
from cafe.core.logger import CLogger as Logger
from cafe.core.signals import SESSION_MANAGER_ERROR
from cafe.core.decorators import SingletonClass
from session_srv import CafeSessionServerFactory

__author__ = 'kelvin'

_logger = Logger(__name__)
debug = _logger.debug
info = _logger.debug
error = _logger.error
warn = _logger.warning


class SessionManagerError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(SessionManagerError, self).__init__(message)
        # Now for your custom code..
        if sys.exc_info()[0]:
            debug(sys.exc_info()[:2])
        error("- " + message, signal=SESSION_MANAGER_ERROR)


SessionRecord = namedtuple("SessionRecord", "session, session_type, server_name")


# ServerRecord = namedtuple("SessionRecord", "session_conn, host, port")

class PolicyBase(object):
    """Base class of session creation policy
    """

    def __init__(self, mgr):
        """
        Args:
            mgr: session manager object
        """
        self.mgr = mgr

    def get_session_srv(self):
        """method to determine which session server to be used
        Note:
            1.create new session servers if needed
            2.return name of the session server
        """
        raise NotImplemented()


class SimpleLocalOnlyPolicy(PolicyBase):
    def get_session_name(self):
        return CafeSessionServerFactory.LOCAL_SERVER


class LocalDistributedPolicy(PolicyBase):
    _THREADSHOLD = 50
    _MAX = 200

    def _get_session_count_local(self):
        return len(self.mgr.servers[CafeSessionServerFactory.LOCAL_SERVER].service.get_sessions())

    def _get_local_network_name(self):
        keys = self.mgr.servers.keys()[:]
        keys.remove(CafeSessionServerFactory.LOCAL_SERVER)

        for k in keys:
            if len(self.mgr.servers[k].service.get_sessions()) < self._THREADSHOLD:
                return k

        # since there is no existing local network server is found initialize a new one
        return self.mgr.create_local_network_server()

    def get_session_name(self):
        if self._get_session_count_local() < self._THREADSHOLD:
            return CafeSessionServerFactory.LOCAL_SERVER

        if len(self.mgr.get_sessions()) > self._MAX:
            raise SessionManagerError("cannot create session - max sessions reached (%d)" % self._MAX)

        return self._get_local_network_name()


class _SessionManager(object):
    """Session Manager.
    Single point of contact for Cafe session creation/removal
    """

    def __init__(self, policy_class=SimpleLocalOnlyPolicy, server_params=None, local_log_path="", remote_log_path=""):
        """
        Args:
            policy_class:   must be subclass of PolicyBase.
                            it is used internally to which server to be used to create a new session
            server_params:  TBD
        """

        self.sessions = {}
        self.servers = {}
        self.server_params = server_params
        self.local_log_path = local_log_path
        self.remote_log_path = remote_log_path

        if not issubclass(policy_class, PolicyBase):
            raise SessionManagerError("policy (%s)is not derived from %s" % (policy_class, PolicyBase))

        self.policy = policy_class(weakref.proxy(self))

        # initialize local server
        self.create_local_server()

    def get_sessions(self):
        """
        """
        l = {}
        for k, r in self.sessions.items():
            l[k] = weakref.proxy(r.session)
        return l

    def create_local_server(self):
        """to create a local session server.
        Note: it is run on cafe python interpreter
        """
        if CafeSessionServerFactory.LOCAL_SERVER not in self.servers.keys():
            server = CafeSessionServerFactory.create(CafeSessionServerFactory.LOCAL_SERVER)
            server.service.set_session_log_base_path(self.local_log_path)
            self.servers[CafeSessionServerFactory.LOCAL_SERVER] = server
        return CafeSessionServerFactory.LOCAL_SERVER

    def create_local_network_server(self):
        """to create a local networked session server.
        Note: create a rypc server in the localhost
        """
        server = CafeSessionServerFactory.create(CafeSessionServerFactory.LOCAL_NETWORK_SERVER,
                                                 host='0.0.0.0', port=0)
        server.service.set_session_log_base_path(self.local_log_path)
        name = server.get_server_name()
        self.servers[name] = server

        return name

    def get_server_by_name(self, name):
        return self.servers[name]

    def get_session(self, name):
        try:
            r = self.sessions[str(name).lower()]
            return weakref.proxy(r.session)
        except KeyError:
            return None

    def create_session(self, session_name="", session_type="", device_type="", **kwargs):
        """Create a new session
        Args:
            session_name (str): session name (unique identifier of a session)
            session_type (str): session type
            device_type (str):  device type
            **kwargs:
        """
        info("create_session: %s, %s, %s, %s" % (session_name, session_type, device_type, str(kwargs)))

        # decide which server to be used for new session creation.
        server_name = self.policy.get_session_name()
        server = self.servers[server_name]

        session_name = str(session_name).lower()

        if self.get_session(session_name):
            raise SessionManagerError("session (%s) is already created" % session_name)

        session = server.create_session(session_name, session_type, device_type, **kwargs)

        if session:
            self.sessions[session_name] = SessionRecord(session, session_type, server_name)
            return weakref.proxy(session)
        else:
            raise SessionManagerError("create session failed - session (%s)" % session_name)

    def remove_session(self, name):
        """remove a session by name
        """
        keys = self.sessions.keys()
        _name = str(name).lower()

        if _name not in keys:
            # raise SessionManagerError("remove session failed - session (%s) not found" % _name)
            warn('remove session failed - session (%s) not found' % _name)
            return

        record = self.sessions.pop(_name)
        server = self.servers[record.server_name]
        server.remove_session(_name)

    def remove_sessions(self):
        """remove all sessions
        """
        keys = self.sessions.keys()
        for k in keys:
            self.remove_session(k)

    def close(self):
        self.remove_sessions()
        for n, obj in self.servers.items():
            info("closing server %s" % n)
            obj.close()

    # make code backward compatible
    def _stop_session_server(self):
        import inspect
        frame, filename, line_number, function_name, lines, index = inspect.stack()[1]
        warn("_stop_session_server is deprecated %s" % str((filename, line_number, function_name, lines, index)))
        self.close()

    # make code backward compatible
    terminate_server = _stop_session_server


@SingletonClass
class SessionManager(_SessionManager):
    pass


def get_session_manager(host=None, port=None, server_params=None, local_log_path=None):
    """return a singleton session manager object
        host: deprecated
        port: deprecated
        server_params: TBD
        local_log_path: where session logs are being saved

    """
    if host is not None:
        warn("get_session_manager 'host' argument is depreciated")
    if port is not None:
        warn("get_session_manager 'port' argument is depreciated")

    if local_log_path is None:
        local_log_path = cafe.get_config().cafe_runner.log_path

    # TODO: implement other policies when needed.
    try:
        klass = cafe.get_config().session_server.policy
        if klass == "SIMPLE":
            policy_class = SimpleLocalOnlyPolicy
        else:
            warn("non supported session server policy value (%s)" % klass)
            policy_class = SimpleLocalOnlyPolicy
    except Exception:
        warn("problem in getting session server policy")
        policy_class = SimpleLocalOnlyPolicy

    debug("session policy class chosen (%s)" % str(policy_class))

    return SessionManager(policy_class=policy_class, local_log_path=local_log_path)


if __name__ == "__main__":
    pass
