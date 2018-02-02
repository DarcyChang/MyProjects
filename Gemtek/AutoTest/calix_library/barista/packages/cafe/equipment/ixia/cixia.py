__author__ = 'jcao'
import re
import sys
from time import sleep

from cafe.core.logger import CLogger as Logger
from cafe.core.signals import IXIA_SESSION_ERROR
from cafe.sessions.tcl_remote import TCLRemoteShell
from cafe.core.exceptions.tg.ixia import *

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning

class IXIASessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=IXIA_SESSION_ERROR)

class TrafficConfigError(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal="Error code: 6001: traffic generator configuration problem")

class _CIXIA (object):
    """
    this is a class for traffic generator IXIA control and configuration
    global var: (For the return info verification)
    1. SUCCESS
    2. ERROR
    """
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    # def __init__(self, host, user, password,
    #              ixia_env="{C:/Program Files (x86)/Ixia/hltapi/4.30.65.37/TclScripts/bin/hlt_init.tcl}",
    #              tcl_shell="tclsh84.exe",
    #              logger=Logger(__name__)):
    #
    #     '''
    #     In init function, will do:
    #         1.open a session to your Windows machine hosting the TCL Code.
    #         2.append tcl path to system env variable.
    #         3.load tcl package.
    #     Args:
    #         host(str): windows system host ip address
    #         user(str): windows system host login username
    #         password(str): windows system host login password
    #         ixia_env(str): ixia env scripts, default path is "C:/Program Files (x86)/Ixia/IxOS/6.20-EA/TclScripts/bin/IxiaWish.tcl"
    #
    #     return:
    #         "SUCCESS" or "ERROR".
    #
    #     '''
    #     self.logger = logger
    #     self.tcl = TCLRemoteShell(host, user, password, timeout=60, tcl_shell=tcl_shell)
    #     #self.tcl.session_log.set_level("TRACE")
    #     #self.tcl.session_log.console = True
    #     self.tcl.command("source %s" % ixia_env)
    #     self.tcl.command("set auto_path [linsert $auto_path 0 c:/Tcl/lib]")
    #     self.logger.info("loading package CalixIxiaHltApi...")
    #     pkg = self.tcl.command("package req CalixIxiaHltApi")[2]
    #     if "package HLTAPI for IxNetwork has been loaded" in pkg:
    #         self.logger.info("PASSED: Tcl package is loaded!")
    #     else:
    #         raise IXIASessionException("ERROR: Failed to load tcl package!")
    def connect_to_chassis(self, chassis_ip, port_list,
                           ixNetworkTclServer="localhost:8009",
                           tcl_server=""):
        '''
        This procedure connects to the Ixia Chassis, takes ownership of selected ports, and optionally
        loads a configuration on the chassis or resets the targeted ports to factory defaults

        Args:
            chassis_ip(str): IP address or chassis name
            port_list(str): the ixia ports which will be used in your testing, could be one or multi ports.

        Returns:
            "SUCCESS" or "ERROR".

        Raises:
            None
        '''

        self.logger.info("connecting to chassis %s" % chassis_ip)
        res= self.tcl.command("CiHLT::connect_to_chas %s \"%s\" %s %s" % (chassis_ip, port_list, ixNetworkTclServer,tcl_server), timeout=300)[2]
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to connect to chassis %s" % chassis_ip)
            raise IXIAConnectChassisError

        elif r == self.SUCCESS:
            self.logger.info("PASS:Connected to chassis %s" % chassis_ip)
            return r

    def cleanup_session(self):
        """
        This procedure disconnects from chassis, IxNetwork Tcl Server and Tcl Server,resets to
        factory defaults, and removes ownership from a list of ports. This command can be used
        after a script is run.

        return:
            "SUCCESS" or "ERROR".

        Raises:
            None

        """

        self.logger.info("cleanup session...")
        res = self.tcl.command("CiHLT::cleanupSession %s" % (1))[2]
        print res
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to cleanup session")
            raise IXIACleanupSessionError

        elif r == self.SUCCESS:
            self.logger.info("PASS:Cleanup session done!")
            return r

    def _debug(self, var):
        print '====> %s' % var

    def _load_config_file(self, path, config_file, **kwargs):

        self.logger.info("load configure file is in progress...")
        opt = {}
        opt.update(**kwargs)
        res = self.tcl.command("IxNC::ixNetLoadconfigure {%s} %s" % (path, config_file),
                               timeout=180)[2]
        #print '====>', res
        if res.split()[-1] != 'SUCCESS':
            raise IXIASessionException("ERROR:Failed to load configure %s/%s!" % (path, config_file))
        else:
            self.logger.info("PASS: Load configuration file is successful! %s/%s.ixncfg!" % (path, config_file))

        self._check_ixia_port_up()

    def _check_ixia_port_up(self):

        self.logger.info("check ixia port status")

        res = self.tcl.command("IxNC::ixNetCheckPortUp", timeout=180)[2]

        if res.split()[-1] != 'SUCCESS':

            raise IXIASessionException("ERROR: Ixia port is not up!")

    def _start_all_protocol(self, check_sum=False):

        self.logger.info("start all protocol is in progress...")
        if check_sum:
            res = self.tcl.command("IxNC::ixNetStartAllProtocols_uncheckSession")
        else:
            res = self.tcl.command("IxNC::ixNetStartAllProtocols", timeout=180)
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            #raise IXIASessionException("ERROR:Failed to start all protocol!")
            raise IXIAControlAllProtocolError
        else:
            self.logger.info("PASS: start all protocol is Done!")

    def _start_all_traffic(self):
        self.logger.info("start all traffic is in progress...")

        res = self.tcl.command("IxNC::ixNetStartTraffic")
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            raise IXIASessionException("ERROR:Failed to start all traffic!")
        else:
            self.logger.info("PASS: start all traffic is Done!")

    def _stop_all_protocol(self):
        self.logger.info("stop all protocol is in progress...")

        res = self.tcl.command("IxNC::ixNetStopAllProtocols")
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            #raise IXIASessionException("ERROR:Failed to stop all protocol!")
            raise IXIAControlAllProtocolError
        else:
            self.logger.info("PASS: stop all protocol is Done!")

    def _stop_all_traffic(self):

        self.logger.info("stop all traffic is in progress...")

        res = self.tcl.command("IxNC::ixNetStopTraffic")
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            #raise IXIASessionException("ERROR:Failed to stop all traffic!")
            raise IXIAControlTrafficError
        else:
            self.logger.info("PASS: stop all traffic is Done!")

    def _apply_traffic(self):

        self.logger.info("apply traffic is in progress...")

        res = self.tcl.command("IxNC::ixNetApplyTraffic")
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            raise IXIASessionException("ERROR:Failed to apply traffic!")
        else:
            self.logger.info("PASS: apply traffic is Done!")

    def _clear_traffic_stats(self):

        self.logger.info("clear traffic stats is in progress...")

        res = self.tcl.command("IxNC::ixNetClearStatistic")
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            raise IXIASessionException("ERROR:Failed to clear traffic stats!")
        else:
            self.logger.info("PASS: clear traffic stats is Done!")

    def _get_traffic_stats_traffic_item(self, row, colum):

        self.logger.info("get traffic stats is in progress...")

        res = self.tcl.command("IxNC::ixNetChecktrafficItemStatFull %s %s" % (row, colum))
        #print '====>', res
        #print '====>', res[2].split()[-2]
        if res[2].split()[-1] != 'SUCCESS':
            raise IXIASessionException("ERROR:Failed to get traffic stats!")
        else:
            self.logger.info("PASS: get traffic stats is Done!")


    def _check_protocol_sum(self):

        self.logger.info("check protocol summary is in progress...")

        res = self.tcl.command("IxNC::ixNetCheckProtocolSum")
        #print '====>', res
        if res[2].split()[-1] != 'SUCCESS':
            raise IXIASessionException("ERROR:Failed to check protocol summary!")
        else:
            self.logger.info("PASS: check protocol summary is done!")

    def enable_test_log(self, log_path):

        '''
        enable test log

        Args:

            param log_path(str): Specify the path to save log, like c:/tmp;

        return:
            "SUCCESS" or "ERROR".

        Raises:
            None

        Example:
            >>> enable_test_log("c:/tmp")
        '''

        res = self.tcl.command("CiHLT::enable_log %s" % log_path)[2]
        self.logger.info("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to enable test log")
            raise IXIAEnableTestLogError

        elif r == self.SUCCESS:
            self.logger.info("PASS: enable log done!")
            return r

        #result = self.verify(res, "PASS")
        # if not result:
        #     print("Failed to enable log")

    def log(self, msg):
        '''
        used to write log(msg) to file

        Args:

            :param msg: test log
            :return: print result pass or fail

        Example:
            >>> log("this is a test msg")
        '''

        res = self.tcl.command("CiHLT::log \"%s\"" % msg)[2]
        if self.ERROR in res:
            self.logger.warn("WARNING:Failed to write log to file")
            return
        elif r == self.SUCCESS:
            self.logger.info("PASS: write log done!")

    def logErr(self, msg):
        '''
        enable test log

        Args:
            :param log_path: Specify the path to save log, like c:/tmp;
            :return: will print info to user for pass or fail and return SUCCESS or ERROR.

        Example:
            >>> enable_test_log("c:/tmp")
        '''

        res = self.tcl.command("CiHLT::logErr \"%s\"" % msg)[2]
        #print("[%s]" % res)
        if self.ERROR in res:
            self.logger.warn("WARNING:Failed to write error log to file")

        elif self.SUCCESS in res:
            self.logger.info("PASS: write error log to file done!")

    def print_stats(self, key=""):
        """
        User can specify the view name and then API will print out packet statistics with a format.

        Args:
            :param key: view name.

        return:
            "SUCCESS" or "ERROR".

        Example:
            >>> dhcp_client_stats("2/1","collect")
            >>> print_stats()
            >>> print_stats("aggregate")
        """

        self.logger.info("print stats...")
        res = self.tcl.command("::CiHLT::printStats %s" % key)[2]
        print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            self.logger.warn("WARNING:Failed to print stats!")
            return r
        elif r == self.SUCCESS:
            self.logger.info("PASS:Print stats done!")
            return r

    def return_stats(self, key=""):
        """
        User can specify the view name and then API will print out packet statistics with a format.

        Args:
            :param key: view name.

        return:
            "SUCCESS" or "ERROR".

        Example:
            >>> dhcp_client_stats("2/1","collect")
            >>> print_stats()
            >>> print_stats("aggregate")
        """

        self.logger.info("print stats...")
        res = self.tcl.command("::CiHLT::printStats %s" % key)[2]
        print("[%s]" % res)
        return res

    def conf_interface(self, port, **kwargs):
        """
        This procedure configures an interface on an Ixia Load Module. It provides the
        means for managing the Ixia Chassis Test Interface options. Depending on whether
        the port is a SONET, Ethernet or ATM type, you have access to the appropriate
        protocol properties

        Args:
            port: ixia ports
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".

        """
        self.logger.info("Configure interface %s is in progress..." % port)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::interfaceConfig %s {%s}" % (port, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to configure interface %s!" % port)
            raise IXIAConfigureInterfaceError

        elif r == self.SUCCESS:
            self.logger.info("PASS: configure interface %s done!" % port)
            #sleep(10)
            return res

    def _conf_interface(self, port, mode, **kwargs):
        """
        This procedure configures an interface on an Ixia Load Module. It provides the
        means for managing the Ixia Chassis Test Interface options. Depending on whether
        the port is a SONET, Ethernet or ATM type, you have access to the appropriate
        protocol properties

        Args:
            port: ixia ports
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".

        """
        self.logger.info("Configure interface %s is in progress..." % port)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::_interfaceConfig %s %s {%s}" % (port, mode, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to configure interface %s!" % port)
            raise IXIAConfigureInterfaceError

        elif r == self.SUCCESS:
            self.logger.info("PASS: configure interface %s done!" % port)
            #sleep(10)
            return res

    def emulation_dhcp_server(self, **kwargs):

        self.logger.info("emulating DHCP client is in progress...")
        opt = {}
        opt.update(**kwargs)
        port_handle = self.tcl.command("set port_handle [eval CiHLT::getVPortHandle %s]" % opt.pop('port'))[2].split()[-1]
        opt['port_handle'] = port_handle
        opt['version'] = 'ixnetwork'
        ops = self.dict2str(opt)
        r1 = self.tcl.command("set res [::ixia::emulation_dhcp_config %s]" % ops)[2].split()[-1]
        r2 = self.tcl.command("keylget res status")[2].split()[-1]

        if r2 != 1:
            #raise IXIASessionException("ERROR:Failed to configure dhcp basic!")
            raise IXIAConfigureDHCPClientError
        else:
            self.logger.info("PASS: emulating dhcp basic is done!")
            if hasattr(opt, 'mode') and opt['mode'] == 'create':
                res = self.tcl.command("keylget res handle")
                return res

    def emulation_dhcp_client(self, **kwargs):

        self.logger.info("emulating DHCP client is in progress...")
        opt = {}
        opt.update(**kwargs)
        port_handle = self.tcl.command("set port_handle [eval CiHLT::getVPortHandle %s]" % opt.pop('port'))[2].split()[-1]
        opt['port_handle'] = port_handle
        opt['version'] = 'ixnetwork'
        ops = self.dict2str(opt)
        r1 = self.tcl.command("set res [::ixia::emulation_dhcp_config %s]" % ops)[2]
        r2 = self.tcl.command("keylget res status")[2].split()[-1]

        if r2 != '1':
            #raise IXIASessionException("ERROR:Failed to configure dhcp basic!")
            raise IXIAConfigureDHCPClientError
        else:
            self.logger.info("PASS: emulating dhcp basic is done!")
            if opt.has_key('mode') and opt['mode'] == 'create':
                res = self.tcl.command("keylget res handle")
                return res[2].split()[-1]

    def emulation_dhcp_client_group(self, **kwargs):
        self.logger.info("emulating DHCP client is in progress...")
        opt = {}
        opt.update(**kwargs)
        port_handle = self.tcl.command("set port_handle [eval CiHLT::getVPortHandle %s]" % opt.pop('port'))[2].split()[-1]
        opt['port_handle'] = port_handle
        opt['version'] = 'ixnetwork'
        ops = self.dict2str(opt)
        r1 = self.tcl.command("set res [::ixia::emulation_dhcp_config %s]" % ops)[2]
        r2 = self.tcl.command("keylget res status")

        if r2 != 1:
            #raise IXIASessionException("ERROR:Failed to configure dhcp basic!")
            raise IXIAConfigureDHCPClientError
        else:
            self.logger.info("PASS: emulating dhcp basic is done!")
            if hasattr(opt, 'mode') and opt['mode'] == 'create':
                res = self.tcl.command("keylget res handle")
                return res

    def conf_dhcp_server(self, port, mode, **kwargs):
        """
        This procedure will configure DHCP Server on an Ixia port

        Args:
            port: ixia ports
            mode: CHOICES: create, modify, reset. DEFAULT: create
            kwargs: other option params, must be a dict.

        return:
            DHCP server handle.

        """
        self.logger.info("%s DHCP server is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::dhcpServerConfig %s %s {%s}" % (port, mode, opt))[2]
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp server!" % mode)
            raise IXIAConfigureDHCPServerError

        elif r == self.SUCCESS:
            self.logger.info("PASS: configure dhcp server done!")
            return res.split()[-1]

    def conf_dhcp_client(self, port, mode, **kwargs):
        """
        Configures DHCP emulation for the specified test port or handle.

        Args:
            port: ixia ports
            mode: CHOICES: create, modify, reset. DEFAULT: create
            handle: ANY
            kwargs: other option params, must be a dict.

        return:
            DHCP basic configure handle.

        """

        self.logger.info("%s DHCP client is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::dhcpClientConfig %s %s {%s}" % (port, mode, opt))[2]
        print '====>res:', res
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp basic!" % mode)
            raise IXIAConfigureDHCPClientError
        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp basic done!" % mode)
        return res.split()[-1]

    def conf_dhcp_client_group(self, handle, mode, **kwargs):

        """
        Configures and modifies a group of DHCP subscribers where each group share a set of common
        characteristics.
        This proc can be invoked multiple times to create multiple groups of subscribers on a port
        with characteristics different from other groups or for independent control purposes.
        This proc allows the user to configure a specified number of DHCP client sessions which belong
        to a subscriber group with specific Layer 2 network settings. Once the subscriber group has
        been configured a handle is created, which can be used to modify the parameters or reset
        sessions for the subscriber.
        :param handle: Specifies the port and group upon which emulation is configured. If the -mode
        is "modify", -handle specifies the group upon which emulation is configured, otherwise
        it specifies the session upon which emulation is configured. Valid for IxTclHal and IxTclNetwork.
        :param mode: Action to take on the port specified the handle argument.
        Create starts emulation on the port.
        Modify applies the parameters specified in subsequent arguments.
        Reset stops the emulation locally without attempting to clear the bound addresses from the
        DHCP server.

        Args:
            kwargs: other option params, must be a dict.

        return:
            DHCP client group handle.
        """
        self.logger.info("%s DHCP client group is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::dhcpClientGroupConfig %s %s {%s}" % (handle, mode, opt))[2]
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp client group!" % mode)
            raise IXIAConfigureDHCPClientGroupError

        elif r == self.SUCCESS:
            self.logger.info("PASS: configure dhcp client group done!")
            return res.split()[-1]

    def _modify_dhcp_client(self, **kwargs):

        self.logger.info("modify dhcp client is in progress...")
        opt = {}
        opt.update(**kwargs)
        port = None
        return self.conf_dhcp_client(port, 'modify', **opt)


    def _reset_dhcp_client(self, port, **kwargs):

        self.logger.info("reset dhcp client is in progress...")
        opt = {}
        opt.update(**kwargs)
        return self.conf_dhcp_client(port, 'reset', **opt)

    def _reset_dhcp_client_group(self, handle, **kwargs):

        self.logger.info("reset dhcp client is in progress...")
        opt = {}
        opt.update(**kwargs)
        port = None
        return self.conf_dhcp_client_group(handle, 'reset', **opt)

    def _reset_dhcp_server(self, **kwargs):

        self.logger.info("modify dhcp client is in progress...")
        opt = {}
        opt.update(**kwargs)
        port = None
        return self.conf_dhcp_server(port, 'reset', **opt)

    def _modify_dhcp_client_group(self, handle, **kwargs):

        self.logger.info("modifing dhcp client group is in progress...")
        opt = {}
        opt.update(**kwargs)

        return self.conf_dhcp_client_group(handle, 'modify', **opt)

    def _modify_dhcp_server(self, **kwargs):

        self.logger.info("modifing dhcp server is in progress...")
        opt = {}
        opt.update(**kwargs)
        port = None
        return self.conf_dhcp_server(port, 'modify', **opt)

    def test_control(self, action):
        """
        test control - used to control protocol here.

        Args:
            action: Specifies the action to take on the specified port handles. like "start all protocol"

        return:
            "SUCCESS" or "ERROR".
        """
        self.logger.info("test control is running: %s" % action)
        res = self.tcl.command("CiHLT::testControl %s" % action)[2]
        #print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            raise IXIASessionException("ERROR:Failed to start protocol")

        elif r == self.SUCCESS:
            self.logger.info("PASS: start protocl done!")
            return r

    def _control_dhcp_server(self, port, action, **kwargs):
        """
        This procedure controls DHCP Server actions.

        Args:
            port_handle: The port handle to perform action for. This parameter is supported using
                the following APIs: IxTclNetwork.
            action: This is a mandatory argument. Used to select the task to perform. This parameter
                is supported using the following APIs: IxTclNetwork. Valid choices are: abort abort_async
                renew reset collect.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """
        self.logger.info("%s DHCP server is in progress..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpServerControl %s %s" % (port, action))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpServerControl %s %s {%s}" % (port, action, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp server!" % action)
            raise IXIAControlDHCPServerError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp server done!" % action)
            return r


    def _control_dhcp_server_by_name(self, handle, action, **kwargs):
        """
        This procedure controls DHCP Server actions.

        Args:
            port_handle: The port handle to perform action for. This parameter is supported using
                the following APIs: IxTclNetwork.
            action: This is a mandatory argument. Used to select the task to perform. This parameter
                is supported using the following APIs: IxTclNetwork. Valid choices are: abort abort_async
                renew reset collect.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """
        self.logger.info("%s DHCP server is in progress..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpServerControlByHandle %s %s" % (handle, action))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpServerControlByHandle %s %s {%s}" % (handle, action, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp server!" % action)
            raise IXIAControlDHCPServerError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp server done!" % action)
            return r

    def _control_dhcp_client(self, port, action, **kwargs):
        """
        Controls DHCP sessions.

        Args:
            port: STC test port.
            action: Action to take on the port specified by the port_handle argument. The
                parameters specified in the emulation_dhcp_group_config proc are used to control the
                bind/renew/release rates. Valid choices are:

                abort: aborts the DHCP sessions for a DHCP emulation. The command returns when the
                    operation is completed. This option is valid only using IxTclNetwork.

                abort_async: aborts the DHCP sessions for a DHCP emulation. The command returns
                    immediately and the operation is executed in the backgronud. This option is valid only
                    using IxTclNetwork.

                bind: starts the discover/request message transmission.

                release: causes the system to issue release message for all currently bound subscribers.

                renew: issues a renew request for all currently bound subscribers. This option is a Cisco option.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """

        self.logger.info("%s DHCP client is in progress..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpClientControl %s %s" % (port, action))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpClientControl %s %s {%s}" % (port, action, opt))[2]
        print("[%s]" % res)
        #result = self.verify(res, "PASS")

        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp client!" % action)
            raise IXIAControlDHCPClientGroupError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp client done!" % action)
            return r


    def _control_dhcp_client_by_name(self, handle, action, **kwargs):

        self.logger.info("%s DHCP client is in progress..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpClientControlByHandle %s %s" % (handle, action))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpClientControlByHandle %s %s {%s}" % (handle, action, opt))[2]
        print("[%s]" % res)
        #result = self.verify(res, "PASS")

        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp client!" % action)
            raise IXIAControlDHCPClientGroupError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp client done!" % action)
            return r


    def _control_dhcp(self, handle, action, **kwargs):
        """
        This procedure controls DHCP Server actions.

        Args:
            port_handle: The port handle to perform action for. This parameter is supported using
                the following APIs: IxTclNetwork.
            action: This is a mandatory argument. Used to select the task to perform. This parameter
                is supported using the following APIs: IxTclNetwork. Valid choices are: abort abort_async
                renew reset collect.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """

        self.logger.info("%s DHCP control is in progress..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpControlByHandle %s %s" % (handle, action))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpControlByHandle {%s} %s {%s}" % (handle, action, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp!" % action)
            raise IXIAControlDHCPClientGroupError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp %s done!" % action)
            return r


    def _dhcp_server_stats(self, port, action, **kwargs):
        """
        This procedure retrieves DHCP Server stats.

        Args:
            port: ixia ports.
            mode: This is a mandatory argument. Used to select the task to perform. This parameter
                is supported using the following APIs: IxTclNetwork. Valid choices are: clear collect.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """

        self.logger.info("%s DHCP server stats is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::dhcpServerStat %s %s {%s}" % (port, action, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")

        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp server stats!" % action)
            raise IXIAGetDHCPServerStatsError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp server stats done!" % action)
            #print '====> -2', res.split('\n')[-2]

            return res.split('\n')[-2]
        else:
            raise RuntimeError('Abnormal return captured!', sys._getframe().f_code.co_name)

    def _dhcp_server_stats_by_handle(self, handle, action, **kwargs):

        self.logger.info("%s DHCP server is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::dhcpServerStatByHandle %s %s {%s}" % (handle, action, opt))[2]
        #print("[%s]" % res)
        #result = self.verify(res, "PASS")

        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp server stats!" % action)
            raise IXIAGetDHCPServerStatsError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp server stats done!" % action)
            #print '====> -2', res.split('\n')[-2]

            return res.split('\n')[-2]
        else:
            raise RuntimeError('Abnormal return captured!', sys._getframe().f_code.co_name)

    def _dhcp_client_stats(self, port, mode,  **kwargs):
        """
        Controls DHCP subscriber group activity.

        Args:
            port: ixia ports.
            mode: session - retrieves session statistics for configured DHCP v4/v6 clients.
                Supported with IxTclNetwork.
                aggregate_stats - retrieves aggregate statistics for the selected port with configured
                DHCP v4/v6 clients.
                Supported with IxTclnetwork and IxTclHal.
            handle: Allows the user to optionally select the groups to which the specified action
                is to be applied. If this parameter is not specified, then the specified action is applied to
                all groups configured on the port specified by the -port_handle command. The handle is obtained
                from the keyed list returned in the call to emulation_dhcp_group_config proc.
                The port handle parameter must have been initialized and dhcp group emulation must have been
                configured prior to calling this function.
                This option is not supported with IxTclAccess and will be ignored if it is used. For
                IxTclNetwork the statistics will be aggregated at port level (the port on which this handle has
                been configured). The stats aggregate.<stat key> will represent the aggregated port stats for
                the first port if multiple handles are provided.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """

        self.logger.info("%s DHCP client stats is in progress..." % mode)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpClientStat %s %s" % (port, mode))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpClientStat %s %s {%s}" % (port, mode, opt))[2]

        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp client stats!" % mode)
            raise IXIAGetDHCPClientStatsError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp client stats done!" % mode)
            print '====>', res
            print '====>', res.split()[-1]
            return res.split()[-1]
        raise RuntimeError('Abnormal return captured!', sys._getframe().f_code.co_name)

    def _dhcp_client_stats_by_handle(self, handle, mode,  **kwargs):

        self.logger.info("%s DHCP client stats is in progress..." % mode)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::dhcpClientStatByHandle %s %s" % (handle, mode))[2]
        else:
            res = self.tcl.command("CiHLT::dhcpClientStatByHandle %s %s {%s}" % (handle, mode, opt))[2]

        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s dhcp client stats!" % mode)
            raise IXIAGetDHCPClientStatsError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s dhcp client stats done!" % mode)
            print '====>', res
            print '====>', res.split()[-1]
            return res.split()[-1]
        raise RuntimeError('Abnormal return captured!', sys._getframe().f_code.co_name)

    def conf_traffic(self, mode, **kwargs):
        """
        This proc configures traffic streams on the specified port with the specified options.

        Args:
            mode: What specific action is taken. Valid choices are:

                create: Create only one stream/traffic item. Dependencies: When traffic_generator must is ixos,\
                    the port_handle must also be provided when mode is create.

                modify: Modify only one existing stream/traffic item. Dependencies: traffic_generator must be
                    ixos/ixnetwork/ixnetwork_540 and stream_id must be provided. NOTE: modify mode is not supported
                    for streams originating in PPPoX endpoints when -traffic_generator is ixos. When
                    traffic_generator ixnetwork_540 is used stream_id can also be a header handle.

                remove: Remove/disable an existing stream/traffic item. Dependencies: traffic_generator
                    must be ixos/ixnetwork/ixnetwork_540 and stream_id must be provided. When traffic_generator
                    is ixos, it disables the stream, when traffic_generator is ixnetwork it removes the
                    traffic item. When traffic_generator is ixnetwork_540: if stream_id is a traffic_item
                    it removes it; if stream_id is a high level stream it suspends it; if stream_id is a
                    header handle it removes it.

                reset: Remove all existing traffic setups.
                    enable: Enables an existing stream. Dependencies:traffic_generator must be\
                    ixos/ixnetwork/ixnetwork_540 and stream_id must be provided.

                disable: Disables an existing stream/traffic item.Dependencies: traffic_generator must be
                    ixnetwork/ixnetwork_540 and stream_id must be provided.

                append_header: Append headers. Dependencies: traffic_generator must be ixnetwork_540 and
                    stream_id must be a header handle.

                prepend_header: Prepend headers. Dependencies: traffic_generator must be ixnetwork_540 and
                    stream_id must be a header handle.

                replace_header: Replace a header. Dependencies: traffic_generator must be ixnetwork_540 and
                    stream_id must be a header handle.

                dynamic_update: With traffic_generator 'ixnetwork_540' some rate and framesize parameters can
                    be changed while the traffic is running. To do this use -mode 'dynamic_update' and -stream_id
                    <traffic_item_handle>. The parameters that will be used for this mode are: frame_size,
                    frame_size_max, frame_size_min, length_mode (only fixed or random), rate_bps, rate_kbps,
                    rate_mbps, rate_byteps, rate_kbyteps, rate_mbyteps, rate_percent, rate_pps,
                    inter_frame_gap, inter_frame_gap_unit and enforce_min_gap. Any other parameters will
                    be silently ignored.

                Dependencies: traffic_generator must be ixnetwork_540 and stream_id must be a traffic item
                    handle. get_available_protocol_templates: Returns a list of all available protocol
                    templates in a user-friendly format. The elements from the list (or the entire list)
                    can be used as pt_handle object(s). Returns key "pt_handle".

                Dependencies: traffic_generator must be ixnetwork_540.
                    get_available_fields: Returns a list of all available fields specific to the provided
                    header handle (in user friendly format). The "header_handle" must be a stack object
                    over a high level stream or a config element. Returns key "handle". Dependencies:
                    traffic_generator must be ixnetwork_540.

                get_field_values: Returns the values for the provided field handle. The field handle can be
                    obtained using mode "get_available_fields". The header handle must also be provided.

                set_field_values: Sets the specified values for the given field handle. Not all values
                    provided by "get_field_values" are available for set. Some of them are read-only. Valid fields:
                    field_activeField-Choice field_auto field_countValue field_fieldValue field_fullMesh
                    field_optionalEnabled field_singleValue field_startValue field_stepValue field_trackingEnabled
                    field_valueList field_valueType Dependencies: traffic_generator must be ixnetwork_540.

                add_field_level: Adds a new field level for the specified header if multiple levels are
                    supported.The "header_handle" and the "field_handle" must be provided. Returns the new field
                    handlers associated with the new level (key: handle). Dependencies: traffic_generator must be
                    ixnetwork_540.

                remove_field_level: Removed the specified field level on the given header. The
                    "header_handle" and the "field_handle" must be provided. Dependencies: traffic_generator
                    must be ixnetwork_540.
            kwargs: other option params, must be a dict.

        return:
            return traffic id

        """
        self.logger.info("%s traffic is in progress" % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::trafficConfig %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s traffic!" % mode)
            raise IXIAConfigureTrafficError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s traffic done!" % mode)
            return res

    def control_traffic(self, port, action, use_low_api=0, **kwargs):
        """
        This proc starts or stops traffic on a given port list.

        Args:
            action: Action to take. Valid choices are:

                sync_run: Hardware synchronizes the generators and all defined traffic. This means that performs
                    the following operations: clears statistics, clears timestamps, starts packet group and latency
                    statistics retrieval for the ports that have the receive mode set to packet group or wide packet
                    group mode, starts capture for the ports that have the receive mode set to capture, and finally,
                    starts traffic. This option should be used specially if you want to retrieve per stream stats or
                    packet group stats(using traffic_stats with -mode stream or with -packet_group_id option). Option
                    -action sync_run performs both actions: clear_stats and start traffic. This option should be used,
                    when per stream stats or packet group stats need to be retrieved. If this option is used with
                    large IxNetwork configs, it takes some time to configure the traffic and apply the traffic to the
                    Ixia port. In this case, the sync_run option should be used with -max_wait_timer (usually takes
                    less than 120 seconds)

                run: Starts the generators and all configured traffic sources (starts traffic). If this option is
                    used with large IxNetwork configs, it takes some time to configure the traffic and apply the
                    traffic to the Ixia port. In this case, the run option should be used with -max_wait_timer (usually
                    takes less than 120 seconds).
                    manual_trigger: triggers a manually triggered traffic sequence on the specified traffic source.
                    (NOT IMPLEMENTED)

                stop: Stops the generators. This choice is valid when -traffic_generator is set to ixos/ixnetwork.
                NOTE: Add a time delay after the traffic stop call, before doing other things such as cleanup or
                modify configuration. Stopping a legacy protocol usually takes less than 10 seconds; stopping
                traffic takes about 30 seconds.

                poll: Polls the generators to determine whether they are stopped or running. This choice is valid
                    when -traffic_generator is set to ixos/ixnetwork. Note: If action -poll is issued immediately
                    after action -start, then the poll action may return stopped 1 when the correct status should be
                    stopped 0. This happens when the chassis is very busy. Adding a little delay (one second) between
                    -action start and -action poll call should resolve this problem.

                reset: Clears generators to power up state and clears all traffic sources. This choice is valid
                    when -traffic_generator is set to ixos/ixnetwork.

                destroy: Destroys the generators. This choice is valid when -traffic_generator is set to
                    xos/ixnetwork.

                clear_stats: Clears all stats and timestamps. Starts packet group and latency statistics retrieval
                    for ports that have the receive mode set to packet group or wide packet group mode. Also starts the
                    capture for the ports that have receive mode set to capture. This option should be used specially
                    if you want to retrieve per stream stats or packet group stats (using traffic_stats with -mode
                    stream or with -packet_group_id option). If using this option, then -action start can be used to
                    start traffic. Option -action sync_run performs both actions: clear_stats and start traffic. This
                    choice is valid when -traffic_generator is set to ixos/ixnetwork.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """

        self.logger.info("%s traffic is in progress ..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::trafficControl %s %s %s" %
                                   (port, action, use_low_api))[2]
        else:
            res = self.tcl.command("CiHLT::trafficControl %s %s %s {%s}" %
                                   (port, action, use_low_api,opt))[2]

        self.logger.info("[===========>>>>%s]" % res)
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s traffic !" % action)
            raise IXIAControlTrafficError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s traffic done!" % action)
            return r

    def _control_traffic(self, action, **kwargs):
        """
        This proc starts or stops traffic on a given port list.

        Args:
            action: Action to take. Valid choices are:

                sync_run: Hardware synchronizes the generators and all defined traffic. This means that performs
                    the following operations: clears statistics, clears timestamps, starts packet group and latency
                    statistics retrieval for the ports that have the receive mode set to packet group or wide packet
                    group mode, starts capture for the ports that have the receive mode set to capture, and finally,
                    starts traffic. This option should be used specially if you want to retrieve per stream stats or
                    packet group stats(using traffic_stats with -mode stream or with -packet_group_id option). Option
                    -action sync_run performs both actions: clear_stats and start traffic. This option should be used,
                    when per stream stats or packet group stats need to be retrieved. If this option is used with
                    large IxNetwork configs, it takes some time to configure the traffic and apply the traffic to the
                    Ixia port. In this case, the sync_run option should be used with -max_wait_timer (usually takes
                    less than 120 seconds)

                run: Starts the generators and all configured traffic sources (starts traffic). If this option is
                    used with large IxNetwork configs, it takes some time to configure the traffic and apply the
                    traffic to the Ixia port. In this case, the run option should be used with -max_wait_timer (usually
                    takes less than 120 seconds).
                    manual_trigger: triggers a manually triggered traffic sequence on the specified traffic source.
                    (NOT IMPLEMENTED)

                stop: Stops the generators. This choice is valid when -traffic_generator is set to ixos/ixnetwork.
                NOTE: Add a time delay after the traffic stop call, before doing other things such as cleanup or
                modify configuration. Stopping a legacy protocol usually takes less than 10 seconds; stopping
                traffic takes about 30 seconds.

                poll: Polls the generators to determine whether they are stopped or running. This choice is valid
                    when -traffic_generator is set to ixos/ixnetwork. Note: If action -poll is issued immediately
                    after action -start, then the poll action may return stopped 1 when the correct status should be
                    stopped 0. This happens when the chassis is very busy. Adding a little delay (one second) between
                    -action start and -action poll call should resolve this problem.

                reset: Clears generators to power up state and clears all traffic sources. This choice is valid
                    when -traffic_generator is set to ixos/ixnetwork.

                destroy: Destroys the generators. This choice is valid when -traffic_generator is set to
                    xos/ixnetwork.

                clear_stats: Clears all stats and timestamps. Starts packet group and latency statistics retrieval
                    for ports that have the receive mode set to packet group or wide packet group mode. Also starts the
                    capture for the ports that have receive mode set to capture. This option should be used specially
                    if you want to retrieve per stream stats or packet group stats (using traffic_stats with -mode
                    stream or with -packet_group_id option). If using this option, then -action start can be used to
                    start traffic. Option -action sync_run performs both actions: clear_stats and start traffic. This
                    choice is valid when -traffic_generator is set to ixos/ixnetwork.
            kwargs: other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """
        self.logger.info("%s traffic is in progress ..." % action)
        opt = self.dict2str(kwargs)
        if opt == "":
            res = self.tcl.command("CiHLT::trafficControl %s" % action)[2]
        else:
            res = self.tcl.command("CiHLT::trafficControl %s {%s}" % (action, opt))[2]

            self.logger.info("[===========>>>>%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s traffic !" % action)
            raise IXIAControlTrafficError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s traffic done!" % action)
            return r

    def _config_traffic(self, mode, **kwargs):

        self.logger.info("%s traffic is in progress" % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::trafficConfig %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s traffic!" % mode)
            raise IXIAConfigureTrafficError

        elif r == self.SUCCESS:
            self.logger.info("PASS: %s traffic done!" % mode)
            if mode not in ["create"]:
                return
            m = re.search(r"(^TI\d+-.+)\r\r", res, re.M)
            #print m.groups()[0]
            return m.groups()[0]

    def traffic_stats(self, mode, **kwargs):
        """
        This proc gathers statistics by port.

        Args:
            port: ixia ports
            mode: Type of statistics to collect. Valid choices are:

                add_atm_stats: Adds the vpi/vci pair to gather both rx and tx statistics. The number of
                    tx stats that can be tracked is less than the number of rx stats that can be tracked.
                    This option is valid only if -traffic_generator is set to ixos.

                add_atm_stats_rx: Adds the vpi/vci pair to gather rx statistics.
                    The number of tx stats that can be tracked is less than the number of rx stats
                    that can be tracked. This option is valid only if -traffic_generator is set to ixos.

                add_atm_stats_tx: Adds the vpi/vci pair to gather tx statistics. The number of tx
                    stats that can be tracked is less than the number of rx stats that can be tracked.
                    This option is valid only if -traffic_generator is set to ixos.

                aggregate: Gathers per port aggregated stats. This option is valid only
                    if -traffic_generator is set to ixos or ixnetwork or ixnetwork_540 and streams
                    where generated either with IxOS/IxNetwork.

                all: Gathers all the statistics available for the specific -traffic_generator option.

                flow: Gathers per flow stats. This option is valid only if -traffic_generator is set
                    to ixnetwork or ixnetwork_540 and streams were generated with IxNetwork.
                    per_port_flows: Ability to retrieve per flow information using HLTAPI. Valid only for
                    traffic generator ixnetwork or ixnetwork_540.

                stream: Gathers per stream stats. This option is valid only if -traffic_generator is
                    set to ixos and streams were generated with IxOS or parameter -traffic_generator is
                    set to ixnetwork or ixnetwork_540 and streams were generated with IxNetwork.

                streams: This is the same as stream option. Deprecated.

                egress_by_port: Available only for IxNetwork TCL API. Parameter port_handle is mandatory
                    for this mode. If egress tracking was configured on the port_handle port this mode
                    retrieves egress tracking statistics for this port. This is available with -traffic_generator
                    ixnetwork and ixnetwork_540.

                egress_by_flow: Available only for IxNetwork TCL API. Parameter port_handle is mandatory
                    for this mode. If egress tracking was configured on the port_handle port this mode retrieves
                    egress tracking statistics for the flows on port_handle port. This is available with
                    -traffic_generator ixnetwork and ixnetwork_540.

                data_plane_port: Available only for IxNetwork TCL API with traffic_generator ixnetwork_540.
                    Retrieve per port data plane statistics.

                traffic_item: Available only for IxNetwork TCL API with traffic_generator ixnetwork_540.
                    Retrieve statistics per traffic item. The statistics can be filtered using parameter
                    -stream with one or a list of values. The values must be traffic_items returned by procedure
                    ::ixia::traffic_config.

                user_defined_stats: Available only for IxNetwork TCL API with traffic_generator ixnetwork_540.
                    Retrieve user defined statitics. The statistics can be filtered using parameters starting
                    with -uds_* with one or a list of values. Available starting with HLT API 3.80.

            kwargs:
                other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """
        self.logger.info("%s traffic statistics is in progress..." % mode)
        opt = self.dict2str(kwargs)
        #print("opt=%s" % opt)
        if opt == "":
            res = self.tcl.command("CiHLT::trafficStat %s " % mode)[2]
        else:
            res = self.tcl.command("CiHLT::trafficStat %s {%s}" % (mode, opt))[2]
        #print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s traffic stats!" % mode )
            raise IXIAGetTrafficStatsError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s traffic stats done!" % mode )
            return r

    def _traffic_stats(self, mode, port, **kwargs):
        """
        This proc gathers statistics by port.

        Args:
            port: ixia ports
            mode: Type of statistics to collect. Valid choices are:

                add_atm_stats: Adds the vpi/vci pair to gather both rx and tx statistics. The number of
                    tx stats that can be tracked is less than the number of rx stats that can be tracked.
                    This option is valid only if -traffic_generator is set to ixos.

                add_atm_stats_rx: Adds the vpi/vci pair to gather rx statistics.
                    The number of tx stats that can be tracked is less than the number of rx stats
                    that can be tracked. This option is valid only if -traffic_generator is set to ixos.

                add_atm_stats_tx: Adds the vpi/vci pair to gather tx statistics. The number of tx
                    stats that can be tracked is less than the number of rx stats that can be tracked.
                    This option is valid only if -traffic_generator is set to ixos.

                aggregate: Gathers per port aggregated stats. This option is valid only
                    if -traffic_generator is set to ixos or ixnetwork or ixnetwork_540 and streams
                    where generated either with IxOS/IxNetwork.

                all: Gathers all the statistics available for the specific -traffic_generator option.

                flow: Gathers per flow stats. This option is valid only if -traffic_generator is set
                    to ixnetwork or ixnetwork_540 and streams were generated with IxNetwork.
                    per_port_flows: Ability to retrieve per flow information using HLTAPI. Valid only for
                    traffic generator ixnetwork or ixnetwork_540.

                stream: Gathers per stream stats. This option is valid only if -traffic_generator is
                    set to ixos and streams were generated with IxOS or parameter -traffic_generator is
                    set to ixnetwork or ixnetwork_540 and streams were generated with IxNetwork.

                streams: This is the same as stream option. Deprecated.

                egress_by_port: Available only for IxNetwork TCL API. Parameter port_handle is mandatory
                    for this mode. If egress tracking was configured on the port_handle port this mode
                    retrieves egress tracking statistics for this port. This is available with -traffic_generator
                    ixnetwork and ixnetwork_540.

                egress_by_flow: Available only for IxNetwork TCL API. Parameter port_handle is mandatory
                    for this mode. If egress tracking was configured on the port_handle port this mode retrieves
                    egress tracking statistics for the flows on port_handle port. This is available with
                    -traffic_generator ixnetwork and ixnetwork_540.

                data_plane_port: Available only for IxNetwork TCL API with traffic_generator ixnetwork_540.
                    Retrieve per port data plane statistics.

                traffic_item: Available only for IxNetwork TCL API with traffic_generator ixnetwork_540.
                    Retrieve statistics per traffic item. The statistics can be filtered using parameter
                    -stream with one or a list of values. The values must be traffic_items returned by procedure
                    ::ixia::traffic_config.

                user_defined_stats: Available only for IxNetwork TCL API with traffic_generator ixnetwork_540.
                    Retrieve user defined statitics. The statistics can be filtered using parameters starting
                    with -uds_* with one or a list of values. Available starting with HLT API 3.80.

            kwargs:
                other option params, must be a dict.

        return:
            "SUCCESS" or "ERROR".
        """
        self.logger.info("%s traffic statistics is in progress..." % mode)
        opt = self.dict2str(kwargs)
        #print("opt=%s" % opt)
        if opt == "":
            res = self.tcl.command("CiHLT::trafficStatOnPort %s %s" % mode, port)[2]
        else:
            res = self.tcl.command("CiHLT::trafficStat %s %s {%s}" % (mode, port, opt))[2]
        #print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s traffic stats!" % mode )
            raise IXIAGetTrafficStatsError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s traffic stats done!" % mode )
            return r

    def _conf_cap_stats(self, port, stop, filename, pkt_mode='data', **kwargs):
        """
        Returns the information related to the packet capture. It is also required that each
        captured packet is returned with a timestamp per packet

        return:
            "SUCCESS" or "ERROR"

        """

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::packetStats %s %s %s %s {%s}" % (port, filename, stop, pkt_mode, opt))[2]
        print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to capture stats!" )
            raise IXIAGetPacketStatsError
        elif r == self.SUCCESS:
            return r

    def _conf_cap_filter(self, port, mode="create", **kwargs):
        """
        Define the filter for packet capturing

        Args:
            port: ixia port.
            mode: create

        return:
            "SUCCESS" or "ERROR".
        """
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::packetConfigFilter %s %s {%s}" % (port, mode, opt))[2]
        print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s capture filter!" % mode)
            raise IXIAConfigurePacketFilterError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s capture filter done!" % mode)
            return r

    def _conf_cap_triggers(self, port, mode="create", **kwargs):
        """
        Define the triggers for packet capturing

        Args:
            port: ixia port.
            mode: create

        return:
            "SUCCESS" or "ERROR".
        """
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::packetConfigTriggers %s %s {%s}" % (port, mode, opt))[2]
        print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s capture filter!" % mode)
            raise IXIAConfigurePacketTriggerError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s capture filter done!" % mode)
            return r


    def _conf_cap_buffer(self, port, action="stop", **kwargs):
        """
        Define how the buffers will be managed for packet capturing

        Args:
            port: ixia port.
            action: Supported with IxTclHal. Controls the action of the buffer when it reaches the full status.
                Not supported with IxTclNetwork and warning will be printed on stdout if this parameter is used.
                DEFAULT: wrap

        return:
            "SUCCESS" or "ERROR".
        """
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::packetConfigBuffers %s %s {%s}" % (port, action, opt))[2]
        print("[%s]" % res)
        r = self.verify(res)

        if r == self.ERROR:
            #raise IXIASessionException("ERROR:Failed to %s capture buffer!" % action )
            raise IXIAConfigurePacketBufferError

        elif r == self.SUCCESS:
            self.logger.info("PASS %s capture buffer done!" % action )
            return r

    def _control_cap(self, port, action, **kwargs):
        """
        Define the beginning and end of packet capturing. The type of capturing performed is
        provided by the packet_config commands. If these commands have not be defined correctly,
        the capturing will not start and an error message will be returned. Fully supported with
        IxTclHal and IxTclNetwork.

        Args:
            port: ixia port
            action: Perform the actions as defined by the values. Valid choices are:
                start: start packet capturing
                stop : stop packet capturing
        return:
            "SUCCESS" or "ERROR".
        """
        res = self.tcl.command("CiHLT::packetControl {%s} %s" % (port, action))[2]
        print("[%s]" % res)
        result = self.verify(res)
        if not result:
            #raise IXIASessionException("ERROR:Failed to %s capture." % action)
            raise IXIAControlPacketError
        return result

    ### Start igmp api definition
    def _conf_igmp_querier(self, handle, mode, **kwargs):
        opts = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::igmpQuerierConfig"
                               " %s %s {%s}" % (handle, mode, opts))[2]
        self.logger.debug("IGMP querier configuration result [{}].".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {}'
            #                           ' igmp session'.format(mode))
            raise IXIAConfigureIGMPQuerierError
        return res

    def _conf_igmp(self, handle, mode, **kwargs):
        opts = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::igmpConfig"
                               " %s %s {%s}" % (handle, mode, opts))[2]
        self.logger.debug("IGMP configuration result [{}].".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {}'
            #                           ' igmp session'.format(mode))
            raise IXIAConfigureIGMPError
        return res

    def _control_igmp(self, handle, mode):
        res = self.tcl.command("CiHLT::igmpControl"
                               " %s %s " % (handle, mode))[2]
        self.logger.debug("IGMP control result [{}].".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {}'
            #                           ' igmp control'.format(mode))
            raise IXIAControlIGMPGroupError
        return res

    def _group_conf_igmp(self, handle, mode, **kwargs):
        opts = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::igmpGroupConfig"
                               " %s %s {%s}" % (handle, mode, opts))[2]
        self.logger.debug("IGMP config group result [{}].".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {}'
            #                           ' igmp group config'.format(mode))
            raise IXIAConfigureIGMPGoupError
        return res

    def _igmp_info(self, port_handle, mode):
        res = self.tcl.command("CiHLT::igmpInfo {} {}".format(port_handle, mode))[2]
        self.logger.debug("IGMP statistic result [{}].".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {}'
            #                           ' igmp info' % (mode))
            raise IXIAGetIGMPGroupStatsError
        return res
    ### End igmp api definition

    ### Start multicast api definition
    def _group_conf_mutilcast(self, handle, mode, **kwargs):
        opts = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::multcastGroupConfig %s %s {%s}" % (handle, mode, opts))[2]
        self.logger.debug("Configures multicast groups result [{}]".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {} multicast group'.format(mode))
            raise IXIAConfigureMulticastGroupError
        return res

    def _source_conf_mutilcast(self, handle, mode, **kwargs):
        opts = self.dict2str(kwargs)
        res = self.tcl.command("CiHLT::multcastSourceConfig %s %s {%s}" % (handle, mode, opts))[2]
        self.logger.debug("Configures multicast sources result [{}]".format(res))
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException('ERROR: Failed to {} multicast source'.format(mode))
            raise IXIAConfigureMulticastSourceError
        return res
    ### End multicast api definition

    def _conf_pppox(self, port, mode, **kwargs):

        opts = self.dict2str(kwargs)

        res = self.tcl.command("CiHLT::pppoxConfig %s %s {%s}" % (port, mode, opts))[2]

        result = self.verify(res)

        if result == 'ERROR':
            raise IXIASessionException('ERROR: Failed to %s pppox' % (mode))
        return res

    def _control_pppox(self, port_handle, action , **kwargs):

        opts = self.dict2str(kwargs)

        res = self.tcl.command("CiHLT::pppoxControl %s %s {%s}" % (port_handle,
                                                                   action,
                                                                   opts))[2]
        result = self.verify(res)

        if result == 'ERROR' :
            #raise IXIASessionException('ERROR:Failed to control pppox')
            raise IXIAControlPPPoXError

        return res


    def _pppox_stats(self, port_handle, handle, mode):

        res = self.tcl.command("CiHLT::pppoxStats %s %s %s" % (port_handle,
                                                              handle ,
                                                              mode))[2]

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException("ERROR:Failed to get pppox stats.")
            raise IXIAGetPPPoXStatsError

        return res

    def _pppox_stats_by_port(self, port_handle, mode):

        res = self.tcl.command("CiHLT::pppoxStatsByPort %s %s" % (port_handle,
                                                                     mode))[2]
        print res
        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException("ERROR:Failed to get pppox stats.")
            raise IXIAGetPPPoXStatsError
        return res

    def _config_cfm_bridge(self, port, mode, **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CiHLT::cfmConfig %s %s {%s}"%
                               (port, mode, opts))[2]
        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to config CFM bridge')
            raise IXIAConfigureCFMBridgeError
        return res

    def _control_cfm_bridge(self, port, action):

        res = self.tcl.command("CiHLT::cfmControl %s %s"%
                               (port, action))[2]
        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to control CFM bridge')
            raise IXIAControlCFMBridgeError

    def _config_cfm_vlan(self, bridge_handle, mode, **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CiHLT::cfmVlanConfig %s %s {%s}"%
                               (bridge_handle, mode, opts))[2]

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to config CFM Vlan')
            raise IXIAConfigureCFMVlanError
        return res

    def _config_cfm_links(self, bridge_handle, mode, **kw):

        opts = self.dict2str(kw)
        res = self.tcl.command("CiHLT::cfmLinksConfig %s %s {%s}"%
                               (bridge_handle, mode, opts))[2]

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to config CFM Links')
            raise IXIAConfigureCFMLinksError
        return res

    def _config_cfm_md_meg(self, bridge_handle, mode, **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CiHLT::cfmMdMegConfig %s %s {%s}"%
                               (bridge_handle, mode, opts))[2]

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to config CFM Md Meg')
            raise IXIAConfigureCFMMdMegError
        return res

    def _config_cfm_mip_mep(self, bridge_handle, mode, **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CiHLT::cfmMipMepConfig %s %s {%s}"%
                               (bridge_handle, mode, opts))[2]

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to config CFM Mip Mep')
            raise IXIAConfigureCFMMipMepError
        return res

    def close(self):
        self.tcl.close()

    def get_list_value(self, list, flag=False, key=""):
        """
        Not ready for use.

        Args:
         list:
         flag:
         key:

        return:

        """
        if flag:
            res = self.tcl.command("puts [CiHLT::get_keylist_value %s %s]" % (list, key))[2]
            print("[%s]" % res)
        else:
            res = self.tcl.command("CiHLT::get_keylist_value %s %s" % (list, key))[2]
            print("[%s]" % res)
            #result = self.verify(res, "PASS")
            if "PASS" not in res:
                raise IXIASessionException("ERROR:Failed to get value!")
            else:
                self.logger.info("PASS: get value done!")

    def verify(self, response):
        """
        used to check if "SUCCESS" is appeared in response.

        Args:
            response: (return) response info

        return:
            "SUCCESS" or "ERROR"

        Example:
            >>> res = "FAilED, PASS, ERROR, SUCCESS"
            >>> verify(res)
        """
        flag = CIXIA.SUCCESS
        if flag not in response:
            flag = CIXIA.ERROR
            return flag
        return flag

    def dict2str(self, dict):
        """
        convert dictionary to string

        Args:
            dict: python date structure dictionary

        return: string, format : " -key1 value1 -key2 -value2"

        Example:
            >>> dict = {"key1":"1","key2":"2","key3":"3"}
            >>> dict2str(dict)
        """

        strings = ""
        for k, v in dict.iteritems():
            if isinstance(v, list):
                v = self.list_convertion(v)
            strings = strings+" "+"-"+str(k)+" "+str(v)
        return strings

    def list_convertion(self, l):
        new = ""
        if isinstance(l, list):
            for i in l:
                new = new + str(i) +" "
        last = "{" + new + "}"
        return last

    def get_keylist_value(self, keylist, key=""):
        """
        get value form tcl keylist

        Args:
            keylist: tcl data structure keylist
            key: Specify the key to get the corresponding value.
        return:
            value of the key you've specified.

        Example:
            >>> keylist = "{session {{1/8/5/3400000 {{acks_received 1} {lease_time 1000} {gateway_address 10.10.0.2}}}}} {status 1}"
            >>> get_list_value(keylist, status)
        """
        res = self.tcl.command("CiHLT::get_list_value \"%s\" %s" % (keylist,key))[2]
        return res

    def send_tcl_cmd(self, cmd):
        """
        send tcl command to remote shell

        Args:
            cmd: tcl command

        return:
            return info base on tcl command

        Example:
            >>> send_tcl_cmd("set a 10")
            >>> send_tcl_cmd("puts $a")
        """
        self.logger.info("send tcl command %s remote tcksh..." % cmd)
        return self.tcl.command("%s" % cmd)[2]

class CIXIA(_CIXIA):
    def __init__(self, host, user, password,
                 ixia_env="{C:/Program Files (x86)/Ixia/hltapi/4.30.65.37/TclScripts/bin/hlt_init.tcl}",
                 tcl_shell="tclsh.exe", logger=Logger(__name__)):


        '''
        In init function, will do:
            1.open a session to your Windows machine hosting the TCL Code.
            2.append tcl path to system env variable.
            3.load tcl package.
        Args:
            host(str): windows system host ip address
            user(str): windows system host login username
            password(str): windows system host login password
            ixia_env(str): ixia env scripts, default path is "C:/Program Files (x86)/Ixia/IxOS/6.20-EA/TclScripts/bin/IxiaWish.tcl"

        return:
            "SUCCESS" or "ERROR".

        '''
        self.logger = logger
        self.tcl = TCLRemoteShell(host, user, password, tcl_shell=tcl_shell)
        # self.tcl.session_log.set_level("TRACE")
        # self.tcl.session_log.console = True
        self.tcl.command("source %s" % ixia_env)
        self.tcl.command("set auto_path [linsert $auto_path 0 c:/Tcl/lib]")
        self.logger.info("loading package CalixIxiaHltApi...")
        pkg = self.tcl.command("package req CalixIxiaHltApi")[2]
        if "package HLTAPI for IxNetwork has been loaded" in pkg:
            self.logger.info("PASSED: Tcl package is loaded!")
        else:
            raise IXIASessionException("ERROR: Failed to load tcl package!")

if __name__ == "__main__":
    pass
