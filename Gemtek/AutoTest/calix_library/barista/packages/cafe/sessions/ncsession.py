import logging
import re
from lxml import etree

from ncclient import NCClientError
from ncclient import manager
from ncclient import transport
from ncclient.operations import RaiseMode
from ncclient.operations.retrieve import GetReply
from ncclient.manager import make_device_handler
from ncclient.operations.rpc import RPC
from ncclient.xml_ import to_xml

from cafe.core.logger import CLogger as Logger
from cafe.core.utils import create_folder
from cafe.core.signals import SESSION_NETCONF_ERROR

"""
wiki page: http://wiki.calix.local/display/DVT/Cafe+automated+test+case%28s%29+with+Netconf+interface

Sample netconf data structure in topo.yaml file:
    >>> connection:
    >>>   n1:
    >>>     ip: 10.243.19.213
    >>>     type: exa
    >>>     protocol: netconf_ssh
    >>>     netconf_params:
    >>>       name: axos
    >>>       version: 1.0
    >>>       additional_capabilities:
    >>>         - 'urn:ietf:params:netconf:capability:xpath:1.0'
    >>>       log_level: DEBUG
    >>>      user: root
    >>>      password: root
    >>>      ports:
    >>>        p1:
    >>>          port: g1
    >>>        p2:
    >>>          port: g2

    key netconf_params is used to specify what handler to be used.
    The key itself is optional.

        sub-key in netconf_params
        - name:                     supported values "axos", "default" (ncclient default handler) and other vendors which specified in ncclient source code.
        - version:                  supported values 1.0 or 1.1. it is in effect when name is "axos"
        - additional_capabilites:   List of urn to specific additional client capabilities.
                                    It is in effect when name is "axos"
        - log_level:                Default is "ERROR".
                                    It is used for changing the nnclient tool log message display filtering.
                                    It is in effect when name is "axos"
"""
__author__ = 'kelvin'

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error

from ncclient.devices.default import DefaultDeviceHandler

class CalixE7DeviceHandler(DefaultDeviceHandler):

    def __init__(self, device_params=None):
        super(CalixE7DeviceHandler, self).__init__(device_params)

        if device_params is not None and "additional_capabilities" in device_params:
            self._additional_capabilities = device_params["additional_capabilities"]
        else:
            self._additional_capabilities = []

        self._capabilities = [
            'urn:ietf:params:netconf:capability:writable-running:1.0',
            'urn:ietf:params:netconf:base:1.0'
        ]

        self._capabilities.extend(self._additional_capabilities)

    def perform_qualify_check(self):
        """
        During RPC operations, ncclient, by default, perform some initial sanity checks on the responses.
        This check will fail on E7
        To disable this check, return False in this function.
        """
        return False

    def get_capabilities(self):
        """
        Return the client capability list.
        """
        return self._capabilities

class CalixAxosDeviceHandler(DefaultDeviceHandler):
    """Customized Calix AXOS Device handler
    """
    def __init__(self, device_params=None):
        super(CalixAxosDeviceHandler, self).__init__(device_params)

        #processing device_param
        if device_params is not None and "version" in device_params:
            self._version = str(device_params["version"])
        else:
            self._version = "1.1"

        if self._version not in ("1.0", "1.1"):
            raise NetConfSessionException("unsupported netconf version %s" % self._version)

        if device_params is not None and "additional_capabilities" in device_params:
            self._additional_capabilities = device_params["additional_capabilities"]
        else:
            self._additional_capabilities = []

        if self._version == "1.1":
            debug("axos v1.1 is configured")
            self._capabilities = ["urn:ietf:params:netconf:base:1.1"]
        else:
            debug("axos v1.0 is configured")
            self._capabilities = ["urn:ietf:params:netconf:base:1.0"]

        self._capabilities.extend(self._additional_capabilities)


    def get_capabilities(self):
        """
        Return the client capability list.
        """
        return self._capabilities

def connect_ssh(*args, **kwds):
    """Select which ncclient device handler to be used based on device_params:name

    Note:
        code are based on ncclient manager.connect_ssh
    """

    if "device_params" in kwds:
        device_params = kwds["device_params"]
    else:
        device_params = None

    if device_params is None:
        #if device_params is None; then use the ncclient "default"
        device_handler = make_device_handler(device_params)
        debug("default device handler is being used")

    elif "name" in device_params and device_params["name"].lower() == "axos":
        #when device name is "axos"
        device_handler = CalixAxosDeviceHandler(device_params)
        debug("axos device handler is being used")

    elif "name" in device_params and device_params["name"].lower() == "e7":
        # when device name is "e7"
        device_handler = CalixE7DeviceHandler(device_params)
        debug("e7 device handler is being used")

    else:
        #other device name
        debug("other device handler is being used")
        device_handler = make_device_handler(device_params)

    # to make the ncclient internal logger only send message level >= INFO
    logging.getLogger("ncclient").setLevel("ERROR")

    try:
        if device_params is not None and "log_level" in device_params:
            logging.getLogger("ncclient").setLevel(device_params["log_level"].upper())
    except ValueError:
        #in case log level is not supported
        pass

    device_handler.add_additional_ssh_connect_params(kwds)

    from ncclient.manager import VENDOR_OPERATIONS

    #global VENDOR_OPERATIONS
    VENDOR_OPERATIONS.update(device_handler.add_additional_operations())
    session = transport.SSHSession(device_handler)

    if "hostkey_verify" not in kwds or kwds["hostkey_verify"]:
        session.load_known_hosts()

    # device_params is not a supported argument for session.connect
    # remove it before calling session.connect
    kwds.pop("device_params")

    try:
        session.connect(*args, **kwds)
    except NCClientError as ex:
        if session.transport:
            session.close()
        raise
    return manager.Manager(session, device_handler, **kwds)


class Raw(RPC):
    """Custom netconf operation for sending Raw netconf RPC
    """
    REPLY_CLS = GetReply
    """See :class:`GetReply`."""

    def request(self, xml):
        """
            xml (str):  xml string of netconf rpc
        """
        # replace XML decorator string and netconf delimiter with <empty> space
        _xml = re.sub(r"\<\?xml.+\?\>", "", xml)
        _xml = re.sub(r"\]\]\>\]\]\>", "", _xml)
        node = etree.fromstring(_xml)

        # hack the parent class code
        # the parent class has the message id and listener created in the constructor.
        # The listen is waiting for rpc-reply with the matching message id
        # if the xml already contains message id, then we used it
        # if not, the we use the message id generated by the parent class
        if "message-id" in node.attrib:
            # re-register message id into the listener
            with self._listener._lock:
                self._listener._id2rpc.pop(self._id)
                self._id = node.attrib["message-id"]
                self._listener._id2rpc[self._id] = self

        else:
            # xml does not has message id, use the default one generated.
            node.attrib["message-id"] = self._id
        return self._request(node)

    # override the parent class method.
    # the parent will add rpc message id and other headers
    # we do not need these id and headers
    def _wrap(self, ele):
        return to_xml(ele)


class NetConfSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_NETCONF_ERROR)


class NetConfSession(object):
    """netconfig APIs class

    """

    def __init__(self, sid=None, host=None, port=830, user="", password="",
                 timeout=120, logfile=None, netconf_params=None, **kwargs):

        self.sid = sid

        self.session = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

        self.session_log = Logger(self.sid)
        self.session_log.console = False
        self.logfile = logfile
        self.netconf_params = netconf_params

    def login(self):
        """login to netconf session

        """

        # self.session = manager.connect_ssh(host=self.host, port=self.port,
        #                                    username=self.user, password=self.password,
        #                                    timeout=self.timeout, hostkey_verify=False)

        self.session = connect_ssh(host=self.host, port=self.port,
                                   username=self.user, password=self.password,
                                   timeout=self.timeout, hostkey_verify=False,
                                   device_params=self.netconf_params)

        # change: not to raise RPCError
        self.session.raise_mode = RaiseMode.NONE

        if self.session:
            self._write_log("login successful. session(%s)" % self.sid)

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, f):
        if f is None:
            self.session_log.disable_file_logging()
            return
        if create_folder(f):
            debug("create folder for %s successful" % f)
        else:
            debug("create folder for %s failed" % f)
            return
        self._logfile = f
        self.session_log.enable_file_logging(log_file=f)
        self.session_log.set_level("DEBUG")


    def get_server_capabilities(self):
        """get server of the connected device netconf capabilites

        Return:
            list
        """
        return self.session.server_capabilities

    def get_client_capabilities(self):
        """get netconf client capabilites

        Return:
            list
        """
        return self.session.client_capabilities

    def _write_log(self, s):
        if self.session_log:
            try:
                root = etree.XML(s)
                self.session_log.debug(etree.tostring(root, pretty_print=True))
            except etree.XMLSyntaxError:
                self.session_log.warn(">>> etree.XMLSyntaxError <<<")
                self.session_log.warn(s)

    def close(self):
        if self.session:
            try:
                self.session.close_session()
            except NCClientError:
                # when close fail, ncsession will raise exception, ignore it.
                pass
            self.session = None
            self._write_log("close successful. session(%s)" % self.sid)

    def __del__(self):
        self.close()

    def is_connected(self):
        """return True is Session is connected; false otherwise
        """

        # TODO: code and test different disconnect suituation
        if self.session:
            return self.session.connected
        else:
            return False

    def _get_filter(self, filter_type, filter_criteria):
        """
        To construct the filter tuple required by ncclients specification

        Args:
            filter_type (str): "xpath" or "subtree"
            filter_criteria (str or lxml element object): if filter_type is str, this should be sting;
                                                          if filter_type is substree, using element
        Return:
            None or a tuple of (type, criteria). None is when filter_type is neither xpath or subtree

        Note:
            For xpath the criteria should be a string containing the XPath expression.
            For subtree the criteria should be an XML string or an Element object containing the criteria.
        """

        if filter_type is None:
            return None

        if not filter_type in ["xpath", "subtree"]:
            self.session_log.warning("filter_type %s is not supported" % str(filter_type))
            return None

        return (filter_type, filter_criteria)

    def _raw(self, xml):

        self._write_log("_raw == %s" % str(xml))

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        ret = self.session.execute(Raw, xml=xml)

        self._write_log("_raw - return ==")
        self._write_log(str(ret))

        return ret

    def raw(self, xml):
        """Send RPC as Raw XML and get the RPC reply

        Args:
            xml (string): Netconf RPC in form of XML string
        Returns:
            ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest

        Example:
            >>> raw = '''
            >>> <?xml version="1.0" encoding="UTF-8"?>
            >>> <rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            >>>  <get>
            >>>    <filter xmlns="http://www.calix.com/ns/exa/base">
            >>>        <config xmlns="http://www.calix.com/ns/exa/base">
            >>>            <profile/>
            >>>        </config>
            >>>    </filter>
            >>>  </get>
            >>> </rpc>
            >>> '''
            >>> nc = self.session_mgr.create_session("nc_simple", session_type="netconf", timeout=5,
            >>>                                     host="10.243.19.213", user="root", password="root")
            >>> nc.login()
            >>> c = nc.session.raw()
            >>> print(c.data_xml); # print the config messages
            >>> self.session_mgr.remove_session(nc.sid)
        """
        return self._raw(xml)

    def get(self, filter_type=None, filter_criteria=None):
        """Retrieve all or part of a specified configuration.

        Args:
            source (string): name of the configuration datastore being queried. default is "running"
            filter_type (str): "xpath" or "subtree"
            filter_criteria (str or lxml element object): if filter_type is str, this should be sting;
                                                          if filter_type is substree, using element
        Returns:
            ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest

        Example:
            >>> nc = self.session_mgr.create_session("nc_simple", session_type="netconf", timeout=5,
            >>>                                     host="10.243.19.213", user="root", password="root")
            >>> nc.login()
            >>> c = nc.session.get(filter_type="xpath", filter_criteria="//craft"))
            >>> print(c.data_xml); # print the config messages
            >>> self.session_mgr.remove_session(nc.sid)

        """

        filter = self._get_filter(filter_type, filter_criteria)
        return self._get(filter=filter)

    def _get(self, filter=None):
        """Retrieve all or part of a specified configuration. it is an internal call

        Args:
            source (string): name of the configuration datastore being queried. default is "running"
            filter: specifies the portion of the configuration to retrieve (by default entire configuration is retrieved)
        Returns:
            ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest

        """
        self._write_log("_get - filter == %s" % str(filter))

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        ret = self.session.get(filter)

        self._write_log("_get - return ==")
        self._write_log(str(ret))

        return ret

    def get_config(self, source="running", filter_type=None, filter_criteria=None):
        """Retrieve all or part of a specified configuration. it is an internal call

        Args:
            source (string): name of the configuration datastore being queried. default is "running"
            filter_type (str): "xpath" or "subtree"
            filter_criteria (str or lxml element object): if filter_type is str, this should be sting;
                                                          if filter_type is substree, using element
        Returns:
            ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest

        Example:
            >>> nc = self.session_mgr.create_session("nc_simple", session_type="netconf", timeout=5,
            >>>                                     host="10.243.19.213", user="root", password="root")
            >>> nc.login()
            >>> c = nc.session.get_config(source='running', filter_type="xpath", filter_criteria="//craft")
            >>> print(c.data_xml); # print the config messages
            >>> self.session_mgr.remove_session(nc.sid
        """
        filter = self._get_filter(filter_type, filter_criteria)
        return self._get_config(source=source, filter=filter)

    def _get_config(self, source="running", filter=None):
        """Retrieve all or part of a specified configuration. it is an internal call

        Args:
            source (string): name of the configuration datastore being queried. default is "running"
            filter: specifies the portion of the configuration to retrieve (by default entire configuration is retrieved)
        Returns:
            ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest

        """

        self._write_log("get_config - source == %s" % source)
        self._write_log("get_config - filter == %s" % str(filter))

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        ret = self.session.get_config(source, filter)

        self._write_log("get_config - return ==")
        self._write_log(str(ret))

        return ret

    def edit_config(self, config, target="running", error_option=None):
        """edit device configruation.

        Args:
            config (xml string): xml rpc message to configure device attributes.
            target (string): netconfig target device configuration datastore. default "running".
            error_option (string): if specified must be one of "stop-on-error", "continue-on-error"m "rollback-on-error"
        Returns:
            ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest

        Examples:
            >>> x = '''
            >>>     <config>
            >>>         <config xmlns="http://www.calix.com/ns/exa/base">
            >>>         <interface>
            >>>            <ethernet>
            >>>              <port>g1</port>
            >>>               <shutdown>false</shutdown>
            >>>            </ethernet>
            >>>         </interface>
            >>>         </config>
            >>>     </config>
            >>> '''
            >>> cx = self.session_mgr.create_session("netconf_1", session_type="netconf", timeout=4,
            >>>                                  host="10.243.19.213", user="root", password="root")
            >>> cx.login()
            >>> try:
            >>>     r = cx.session.edit_config(target="running", config=x)
            >>>     print(r.ok)
            >>> finally:
            >>>     self.session_mgr.remove_session(cx.sid)

        """

        self._write_log("edit_config - target == %s" % target)
        self._write_log("edit_config - config ==")
        self._write_log(str(config))

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        if config is None:
            raise NetConfSessionException("edit_config: invalid config value: session (%s)" % self.sid)

        ret = self.session.edit_config(target=target, config=config, error_option=error_option)

        self._write_log("edit_config - return ==")
        self._write_log(str(ret))

        return ret

    def copy_config(self, source, target):
        """
        Create or replace an entire configuration datastore with the contents of another complete configuration datastore.

        Args:
            source (str): the name of the configuration datastore to use as the source of the copy operation or config element containing the configuration subtree to copy
            target (str): the name of the configuration datastore to use as the destination of the copy operation

        Note:
            To be tested
        """

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        ret = self.session.edit_config(source=source, target=target)

        self._write_log("copy_config - return ==")
        self._write_log(str(ret))

        return ret

    def delete_config(self, target):
        """
        Delete a configuration datastore.

        Args:
            target (str): the name or URL of configuration datastore to delete

        Note:
            To be tested
        """

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        ret = self.session.delete_config(target=target)

        self._write_log("delete_config - return ==")
        self._write_log(str(ret))

        return ret

    def dispatch(self, rpc_command, source=None, filter_type=None, filter_criteria=None):
        """

        Args:
            rpc_command (str or lxml elem object): specifies rpc command to be dispatched
                        either in plain text or in xml element format (depending on command)
            source (str): name of the configuration datastore being queried
            filter_type (str): "xpath" or "subtree"
            filter_criteria (str or lxml element object): if filter_type is str, this should be sting;
                                                          if filter_type is substree, using element
        Note:
            To be tested
        """

        if not self.is_connected():
            raise NetConfSessionException("not connected: session (%s)" % self.sid)

        # import sys
        # rpc_command.__class__
        # sys.__stderr__.write("\n%s\n" % (type(rpc_command)))
        # sys.__stderr__.write("\n%s\n" % rpc_command.__class__)

        if isinstance(rpc_command, etree._Element):
            self._write_log(
                "dispatch - rpc_command(etree._Element) == %s" % etree.tostring(rpc_command, pretty_print=True))
        else:
            self._write_log("dispatch - rpc_command(str) == %s" % str(rpc_command))

        filter = self._get_filter(filter_type, filter_criteria)
        ret = self.session.dispatch(rpc_command, source, filter)

        self._write_log("dispatch - return ==")
        self._write_log(str(ret))

        return ret


if __name__ == "__main__":
    pass
    from lxml import etree
    from cafe.core.logger import init_logging
    from cafe.runner.parameters.options import options

    options.apply()

    init_logging()
    nc = NetConfSession(sid="1222", host="10.243.19.214", user="root", password="root")
    nc.session_log.set_console(True)
    nc.login()

    c = nc.session.get_config(source='running', filter=("xpath", "//craft"))
    print(c.data_xml)
    print(nc)
    print(nc.session)

    root = etree.XML(c.data_xml)
    print(etree.tostring(root, pretty_print=True))
    nc.close()
