__author__ = 'jcao'
import inspect
import os, re
import platform
import shutil
import cafe
from cafe.core.logger import CLogger as Logger
from cafe.core.signals import STC_SESSION_ERROR
from cafe.sessions.tcl_remote import TCLRemoteShell
from cafe.sessions.tclsession import TclSession
from cafe.core.exceptions.tg.stc import *

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning


class STCSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=STC_SESSION_ERROR)


class TrafficConfigError(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal="Error code: 6001: traffic generator configuration problem")


class _CSTC(object):
    """
    This is a class for traffic generator Spirent test center control and configuration
    now, the followint functions will be supported:

    1. DHCP function
    2. Static traffic
    3. Bounding traffic
    4. Packet capture

    global var: SUCCESS and ERROR for result verification.
    """
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __init__(self):
        self.logger = _module_logger

    def __shutdown__(self):
        self.cleanup_session(self.__port_list)
        self.close()

    def connect_to_chassis(self, chassis_ip, port_list, xml=""):
        '''
        Initializes one or more Spirent HLTAPI chassis and reserves ports on
        the initialized chassis. All reserved ports will reset any existing traffic
        or port configurations to an initialized startup state.

        Args:
            chassis_ip: IP address of IXIA chassis
            port_list: the ixia ports which will be used in your testing, could be one or multi ports. {<slot>/<port>}
            xml: stc config xml file
        return:
            "SUCCESS" or "ERROR".

        Example:
            >>> chas = "10.245.252.54"
            >>> port_list = "2/1 2/2"
            >>> connect_to_chassis(chas, port_list)
        '''
        self.__port_list = port_list
        print self.__port_list
        self.logger.info("connecting to chassis %s" % chassis_ip)
        if xml == "":
            res = self.tcl.command("CsHLT::connect_to_chas %s \"%s\""
                                   % (chassis_ip, port_list), timeout=300)[2]
        else:
            res = self.tcl.command("CsHLT::connect_to_chas %s \"%s\" \"%s\" "
                                   % (chassis_ip, port_list, xml), timeout=300)[2]

        info_msg = "PASS:Connected to chassis %s" % chassis_ip
        return self._result_check(STCConnectChassisError, info_msg, res)[1]

    def cleanup_session(self, port_list):
        """
        Cleans up the current test by terminating port reservations, disconnecting
        the ports from the chassis, releasing system resources, and removing the
        specified port configurations.

        Args:
            port_list: STC ports you've reserved before.

        return:
            "SUCCESS" or "ERROR".

        Example:
                >>> CSTC.cleanup_session("2/1 2/2")
        """

        self.logger.info("cleanup session...")
        ports = " ".join(port_list)
        res = self.tcl.command("CsHLT::cleanup_session {%s}" % (ports), timeout=120)[2]
        info_msg = "PASS:Cleanup session done!"
        return self._result_check(STCCleanupSessionError, info_msg, res)[1]

    def enable_hlt_log(self, path):
        '''
        Enable Spirent HLTAPI log function to receive hlt log

        Args:
            log_path: Specify the path to save log. like c:/tmp

        return:
            "SUCCESS" or "ERROR".

        Example:
            >>> enable_hlt_log("c:/temp")
        '''
        self.logger.warn(msg="This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        res = self.tcl.command("CsHLT::enable_hltlog %s" % path)[2]
        return self._warning_check("WARNING:Failed to enable log", "PASS: log is enabled", res)

    def enable_test_log(self, log_path):
        '''
        enable test log

        Args:
            log_path: Specify the path to save log, like c:/tmp;

        return:
            "SUCCESS" or "ERROR".

        Example:
            >>> enable_test_log("c:/tmp")
        '''
        self.logger.info("Enable test log to %s." % log_path)
        res = self.tcl.command("CsHLT::logOn %s" % log_path)[2]
        return self._warning_check("WARNING:Failed to enable log",
                                   "PASS: log is enabled, and path is %s" % log_path, res)

    def log(self, msg):
        '''
        used to write log(msg) to file

        Args:
            msg: test log
        return:


        Example:
            >>> log("this is a test msg")
        '''
        self.logger.warn(msg="This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        res = self.tcl.command("CsHLT::log \"%s\"" % msg)[2]
        self._warning_check("WARNING:Failed to write error log to file",
                                   "PASS: write error log to file done!", res)

    def logErr(self, msg):
        '''
        used to write error log(msg) to file.

        Args:
            msg: test log.

        return:
            .

        Example:
            >>> log("this is a test error msg")
        '''
        self.logger.warn(msg="This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        res = self.tcl.command("CsHLT::logErr \"%s\"" % msg)[2]
        self._warning_check("WARNING:Failed to write error log to file",
                                   "PASS: write error log to file done!", res)

    def return_stats(self, key=""):
        """
        User can specify the view name and then API will print out packet statistics with a format.

        Args:
            key: view name.

        return:
            .

        Example:
            >>> dhcp_client_stats("2/1","collect")
            >>> return_stats()
            >>> return_stats("aggregate")
        """
        self.logger.info("return stats...")
        res = self.tcl.command("CsHLT::print_stats %s" % key)[2]
        print("[%s]" % res)
        return res

    def print_stats(self, key=""):
        """
        User can specify the view name and then API will print out packet statistics with a format.

        Args:
            key: view name.

        return:
            .

        Example:
            >>> dhcp_client_stats("2/1","collect")
            >>> print_stats()
            >>> print_stats("aggregate")
        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("print stats...")
        res = self.tcl.command("CsHLT::print_stats %s" % key)[2]
        print("[%s]" % res)
        return self._warning_check("WARNING:Failed to print stats!", "PASS:print stats done!", res)

    def _config_interface(self, port, mode, **kwargs):
        '''
        Creates, modifies, or deletes a port configuration

        Args:
            port: STC testing port
            mode: port configure mode, could be create, modify and delete
            kwargs: other option params, must be a dict.

        return:
            .

        Example:
            >>> option = {
            ...                 "intf_mode":          "ethernet",
            ...                 "phy_mode":           "copper",
            ...                 "speed":              "ether1000",
            ...                 "autonegotiation":    "1",
            ...                 "duplex":             "full",
            ...                 "src_mac_addr":       "00:10:94:00:00:32",
            ...                 "intf_ip_addr":       "10.1.1.3",
            ...                 "gateway":            "10.1.1.1",
            ...                 "netmask":            "255.255.255.0",
            ...                 "arp_send_req":       "1"
            ...                }
            >>> conf_interface("2/1","create",**option)
        '''

        self.logger.info("Configure interface %s is in progress..." % port)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::interface_conf %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS:%s interface %s done!" % (mode, port)
        return self._result_check(STCConfigureInterfaceError, info_msg, res)[0]


    def create_dhcp_server(self, port, version=4, **kwargs):
        '''
        Creates, modifies, or resets an emulated Dynamic Host Configuration Protocol
        (DHCP) server or Dynamic Host Configuration Protocol for IPv6 or Prefix
        delegation (DHCPv6/PD) server for the specified Spirent HLTAPI port or handle.
        A DHCP or DHCPv6/PD server is an Internet host that returns configuration
        parameters to DHCP or DHCPv6/PD clients respectively. DHCP or DHCPv6/PD servers
        can dynamically assign an IP address and deliver configuration parameters to a
        DHCP or DHCPv6/PD client on a TCP/IP network. DHCP allows the reuse of an
        address that is no longer needed by the client to which it was assigned.

        Args:
        port: STC test port.
        kwargs: other option params, must be a dict.

        return:
            .

        Example:
            >>> option ={
            ...                 "count":                      "1",
            ...                 "local_mac":                  "00:10:94:00:00:03",
            ...                 "ip_address":                 "192.0.1.4",
            ...                 "ip_step":                    "0.0.0.1",
            ...                 "ip_gateway":                 "192.0.1.1",
            ...                 "ipaddress_pool":             "192.0.1.5",
            ...                 "ipaddress_increment":        "2",
            ...                 "ipaddress_count":            "30",
            ...                 "lease_time":                 "60"
            ...             }
            ... conf_dhcp_server("2/1","create",**option)
        '''
        # This method is duplicated at the App() driver layer create_dhcp_server method
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("emulation DHCP server is in progress...")
        opt = self.dict2str(kwargs)
        if version == 4:
            res = self.tcl.command("CsHLT::dhcp_server_create %s {%s}" % (port, opt))[2]
        elif version == 6:
            res = self.tcl.command("CsHLT::dhcp_server_create %s {%s} %d" % (port, opt, version))[2]
        else:
            raise ValueError("The version should be 4 or 6.")
        info_msg = "PASS:emulation dhcp server done!"
        return self._result_check(STCConfigureDHCPServerError, info_msg, res)[0]

    def create_dhcp_client_basic(self, port, handle=True, **kwargs):
        '''
        Creates, modifies, or resets an emulated Dynamic Host Configuration Protocol
        (DHCP) clients or Dynamic Host Configuration Protocol for IPv6 or Prefix
        delegation (DHCPv6/PD) clients for the specified Spirent HLTAPI port or handle.
        DHCP is used for IPv4 and IPv6. While both versions serve much the same purpose,
        the details of the protocol for IPv4 and IPv6 are sufficiently different that
        they may be considered separate protocols. You use Spirent HLTAPI to emulate a
        network containing DHCP or DHCPv6/PD clients.
        DHCP uses a client-server model, in which DHCP servers provide network
        addresses and configuration parameters to DHCP clients.
        DHCPv6/PD is intended for delegating a long-lived IPv6 prefix and
        configuration information from a delegating router to a requesting router,
        across an administrative boundary, where the delegating router does not
        require knowledge about the topology of the links in the network to which
        the prefixes will be assigned. Hosts attached to the requesting router can
        auto-configure the IPv6 addresses from the delegated prefix.

        Args:
            port: STC test port.
            handle: if set to False, no handle return, otherwise dhcp handle will be returned.
            kwargs: other option params, must be a dict.

        return:
            .

        Example:
            >>> option = {
            ...         "retry_count":                "20",
            ...         "request_rate":               "1000",
            ...         "outstanding_session_count":  "100",
            ...         "broadcast_bit_flag":         "1"
            ...        }
            ... conf_dhcp_client_basic("2/1","create",handle=True,**option)
        '''
        self.logger.info("Create DHCP client is in progress...")
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::dhcp_client_basic_create %s {%s}" % (port, opt))[2]
        info_msg = "PASS:Create DHCP client done!"
        if handle:
            return self._result_check(STCConfigureDHCPClientError, info_msg, res)[0]
        else:
            return self._result_check(STCConfigureDHCPClientError, info_msg, res)[1]

    def config_dhcp_client_group(self, handle, mode, version=4, **kwargs):
        '''
        Configures, modifies or resets a specified number of DHCP or DHCPv6/PD client
        sessions which belong to a subscriber group with specific Layer 2 network
        settings. Once the subscriber group has been configured, a handle is created,
        which can be used to modify the parameters or reset the sessions for the
        subscriber group or to control the binding, renewal, and release of the DHCP or
        DHCPv6/PD sessions.

        Args:
            handle: the hansdle is returned when dhcp client configure done
            mode: {create|modify|enable|reset}
            kwargs: other option params, must be a dict.

        return:
            .

        Example:
            >>> handle = stc.conf_dhcp_client_basic(client_port,"create",handle=True,**option)
            >>> dhcp_client_handle = handle.split()[-1]
            >>> option ={
            ...              "encap":         "ethernet_ii",
            ...              "protocol":      "dhcpoe",
            ...              "num_sessions":  "20",
            ...              "mac_addr":      "00.00.10.95.11.15"
            ...            }
            ... result = stc.conf_dhcp_client_group(dhcp_client_handle,"create",**option)
        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("%s DHCP client group is in progress..." % mode)
        opt = self.dict2str(kwargs)
        if version == 4:
            res = self.tcl.command("CsHLT::dhcp_client_group_conf %s %s {%s}" % (handle, mode, opt))[2]
        elif version == 6:
            res = self.tcl.command("CsHLT::dhcp_client_group_conf %s %s {%s} %s" % (handle, mode, opt, version))[2]
        else:
            raise ValueError("The version should be 4 or 6.")
        info_msg = "PASS: %s dhcp client group done!" % mode
        return self._result_check(STCConfigureDHCPClientGroupError, info_msg, res)[0]

    def _control_dhcp_server(self, port, mode, **kwargs):
        '''
        Connects, renews, or resets DHCP or DHCPv6/PD server(s) on the specified ports
        or the DHCP or DHCPv6/PD handles/servers respectively.

        Args:
            port: STC test port
            mode: {connect|renew|reset}
            kwargs: other option params, must be a dict.

        return:
            .

        Example:
            >>> stc.control_dhcp_server("2/1","connect")
        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("%s DHCP server is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::dhcp_server_ctrl %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS:%s dhcp server done!" % mode
        return self._result_check(STCControlDHCPServerError, info_msg, res)[1]

    def _control_dhcp_client(self, port, mode, **kwargs):
        '''
        Starts, stops, or restarts the DHCP or DHCPv6/PD subscriber group activity on
        the specified port.

        Args:
            port: Identifies the handle of the port on which DHCP or DHCPv6/PD emulation has been configured. This value is returned by the sth::emulation_dhcp_config function.
            mode: Specifies the action to perform on the port specified by the -port_handle argument. Possible values are bind, release, and renew. You must specify one of these values. The modes are described below:
                bind - Starts the Discover/Request message exchange between the emulated requesting router(s) and the delegating router(s) that is necessary to establish client bindings.
                release - Terminates bindings for all currently bound subscribers.
                renew - Renews the lease for all currently bound subscribers.
            kwargs: other option params, must be a dict.

        return: will print pass or fail info to user.

        Example:
            >>> stc.control_dhcp_client("2/2","bind")
        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("%s DHCP client is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::dhcp_client_ctrl %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS:%s dhcp client done!" % mode
        return self._result_check(STCControlDHCPClientGroupError, info_msg, res)[1]

    def get_dhcp_server_stats(self, port, mode, **kwargs):
        '''
        Returns statistics of the DHCPv6/PD server.

        Args:
            port: Specifies the DHCP or DHCPv6/PD server handle from which to extract the server statistics data. You must specify -dhcp_handle or -port_handle, but not both.
            mode: Specifies the action of the statistics for the specified port or DHCP or DHCPv6/PD server. This argument is mandaotry. Possible values are collect or clear.
                collect - Retrieves the statistics from the specified port or DHCP or DHCPv6/PD server
                clear - Removes the statistics from the specified port or DHCP or DHCPv6/PD server

        return:
            .

        Example:
            >>> stc.dhcp_server_stats("2/1","COLLECT")
        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("%s DHCP server is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::dhcp_server_stats %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS: %s dhcp server stats done!" % mode
        return self._result_check(STCGetDHCPServerStatsError, info_msg, res)[1]

    def get_dhcp_client_stats(self, port, mode, **kwargs):
        '''
        Returns statistics about the DHCP or DHCPv6/PD subscriber group activity on the
        specified port. Statistics include the connection status and number and
        type of messages sent and received from the specified port.

        Args:
            port: Specifies the port upon which emulation is configured. This value is returned by the sth::emulation_dhcp_config function.
            mode: Specifies the kind of information you want to see. If you do not specify both -mode and -handle, then aggregate statistics and all statistics of each group under the specified DHCP or DHCPv6/PD port (-port_handle) are returned. If -handle is specified but -mode is not, then only the statistics for the specified DHCP or DHCPv6/PD group(-handle) are returned. Possible values are:
                aggregate - Returns transmitted and received statistics for the specified DHCP port.
                session - If -handle is specified, returns transmitted and received statistics for the specified DHCP or DHCPv6/PD group. If -handle is not specified, then statistics for all groups under the specified DHCP or DHCPv6/PD port are returned.

        return:
            .

        Example:
            >>> stc.dhcp_client_stats("2/2","collect")
        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("emulation DHCP client stats is in progress...")
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_stats %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS: emulation DHCP client stats done!"
        return self._result_check(STCGetDHCPClientStatsError, info_msg, res)[1]

    def _dhcp_server_stats(self, handle, **kwargs):
        self.logger.info("DHCP server stats is in progress...")
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_server_stats %s {%s}" % (handle, opt))[2]
        info_msg = "PASS: dhcp server stats done!"
        return self._result_check(STCGetDHCPServerStatsError, info_msg, res)[1]

    def _dhcp_client_stats(self, handle, **kwargs):
        self.logger.info(" DHCP client stats is in progress...")
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_stats %s {%s}" % (handle, opt))[2]
        info_msg = "PASS: get dhcp client stats done!"
        return self._result_check(STCGetDHCPClientStatsError, info_msg, res)[1]

    def load_config_file(self, filename):
        '''
        load stc configure from a xml file.

        Args:
            filename: xml file name

        return:
            .

        Examplse:
            >>> load_xml_config("c:/test.xml")
        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        res = self.tcl.command("CsHLT::load_xml_config %s" % filename)[2]
        info_msg = "PASS:load xml configure file done!"
        return self._result_check(STCLoadConfigError, info_msg,res)[1]

    def config_traffic(self, port, mode, **kwargs):
        """
        Creates, modifies, removes, or resets a stream block of network traffic on
        the specified test port(s). A stream is a series of packets that can be
        tracked by Spirent HLTAPI. A stream block is a collection of one or
        more streams represented by a base stream definition plus one or more rules
        that describe how the base definition is modified to produce additional
        streams.

        Args:
            port: stc test port.
            action: {create | modify | remove | enable | disable | reset}
            kwargs: other option params, must be a dict format.

        return:

        Example:
            >>> option = {"-test1":"1", "-test2":"2"}
            >>> config_traffic("2/1", "config", **option)
        """
        self.logger.info("%s traffic is in progress..." % mode)
        self.logger.info("%s traffic is in progress..." % kwargs)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::traffic_conf %s %s {%s}" % (mode, port, opt), timeout=60)[2]
        print "###############################"
        print "res is:", res
        print "###############################"
        info_msg = "PASS:%s traffic on port %s done!" % (mode, port)
        return self._result_check(STCConfigureTrafficError, info_msg, res)[1]

    def _control_traffic(self, port, action, **kwargs):
        """
        Controls traffic generation on the specified test ports.

        Args:
            port: Specifies the handle(s) of the port(s) on which to control traffic.
            action: Specifies the action to take on the specified port handles,This argument is mandatory.
                Possible values are:
                run: Starts traffic on all specified test ports.
                stop: Stops traffic generation on all specified test ports.
                reset: Clears all statistics and deletes all streams.
                destroy: Deletes all streams. (Same as using -traffic_configure -mode remove.)
                clear_stats: Clears all statistics (transmitted and received counters) related to streams.
                poll: Polls the generators to determine whether they are stopped or are running.

            kwargs: other option params, must be a dict format.

        return:
            .

        Example:
            >>> control_traffic("2/1","run")
        """

        self.logger.info("%s traffic is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::traffic_ctrl %s %s {%s}" % (action, port, opt))[2]
        info_msg = "PASS:%s traffic on port %s!" % (action, port)
        return self._result_check(STCControlTrafficError, info_msg, res)[1]

    def _control_traffic_by_name_internal(self, handle, action, **kwargs):

        self.logger.info("%s traffic is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::traffic_ctrl_by_name %s %s {%s}" % (action, handle, opt))[2]
        info_msg = "PASS:%s traffic on port %s!" % (action, handle)
        return self._result_check(STCControlTrafficError, info_msg, res)[1]

    def _apply(self):
        return self.tcl.command("CsHLT::apply ", timeout=300)[2]

    def _start_all_protocol(self):
        return self.tcl.command("CsHLT::startAllProtocol ", timeout=300)[2]

    def _stop_all_protocol(self):
        return self.tcl.command("CsHLT::stopAllProtocol ", timeout=300)[2]

    def _start_all_traffic(self):

        _p = []
        for k in sorted(self.port_list.keys()):
            v = self.port_list[k]
            _p.append(self.get_port_handle(v['port']))
        port_h = " ".join(_p)

        return self.tcl.command("CsHLT::start_all_traffic {%s}" % port_h, timeout=300)[2]

    def _stop_all_traffic(self):

        _p = []
        for k in sorted(self.port_list.keys()):
            v = self.port_list[k]
            _p.append(self.get_port_handle(v['port']))
        port_h = " ".join(_p)

        return self.tcl.command("CsHLT::stop_all_traffic {%s}" % port_h, timeout=300)[2]

    def traffic_stats(self, port, mode, **kwargs):
        """
        Retrieves statistical information about traffic streams.

        Args:
            port: Specifies one or more ports from which to gather transmitted (tx) and received (rx) statistics. This argument is mandatory.
            mode: Specifies the type of statistics to collect:
                aggregate - Collect all transmitted (tx) and received (rx) packets.
                out_of_filter - Collect received (rx) packets that do not match the filter.
                streams - Collect detailed test stream statistics.
                all - Collect all statistics.
                This argument is mandatory.
            kwargs: other option params, must be a dict format.

        return:
            .

        Example:
            >>> traffic_stats("2/1","all")
        """
        self.logger.info("%s traffic stats on port %s is in progress..." % (mode, port))
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::traffic_stats %s %s {%s}" % (mode, port, opt))[2]
        info_msg = "PASS:%s traffic on port %s!" % (mode, port)
        return self._result_check(STCGetTrafficStatsError, info_msg, res)[1]

    def _conf_cap_buffer(self, port, action="stop", **kwargs):
        """
        Defines how Spirent HLTAPI will manage the buffers for packet capturing.

        Args:
            port: Specifies the handle of the port on which buffers will be managed. This argument is mandatory. To apply the sth::packet_config_buffers function to all ports, specify "all" instead of a handle (for example, -port_handle all).
            action: Specifies the action to perform when the buffer is full.
                The only possible value for the Spirent HLTAPI is "wrap",
                This argument is mandatory.

        return:
            "SUCCESS" or "ERROR".

        Example:
            >>> config_cap_buffer("2/1")
        """

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::packetConfigBuffers %s %s {%s}" % (port, action, opt), timeout=20)[2]
        print("[%s]" % res)
        info_msg = "PASS %s capture buffer done!" % action
        return self._result_check(STCConfigurePacketBufferError, info_msg, res)[1]

    def _conf_cap_filter(self, port, mode="create", **kwargs):
        """
        Define the filter for packet capturing

        Args:
            port: spirent port.
            mode: create

        return:
            "SUCCESS" or "ERROR".
        """
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::packetConfigFilter %s %s {%s}" % (port, mode, opt), timeout=20)[2]
        print("[%s]" % res)
        info_msg = "PASS %s capture filter done!" % mode
        return self._result_check(STCConfigurePacketFilterError, info_msg, res)[1]

    def _conf_cap_triggers(self, port, mode="add", **kwargs):
        """
        Define the triggers for packet capturing

        Args:
            port: spirent port.
            mode: create

        return:
            "SUCCESS" or "ERROR".
        """
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::packetConfigTriggers %s %s {%s}" % (port, mode, opt), timeout=20)[2]
        print("[%s]" % res)
        info_msg = "PASS %s capture filter done!" % mode
        return self._result_check(STCConfigurePacketTriggerError, info_msg, res)[1]

    def _control_cap(self, portlist, action):
        """
        Starts or stops packet capturing.

        Args:
            portlist: Identifies the handle of the port on which to start or stop capturing data packets. This argument is mandatory. You can specify "all" to apply this function to all ports (for example, -port_handle all).
            action: Specifies the action to perform. Possible values are start and stop, This argument is mandatory. The actions are described below:
                start - Start capturing packets.
                stop - Stop capturing packets.

        return:
            .
        """
        self.logger.info("%s capture on port %s is in progress..." % (action, portlist))
        res = self.tcl.command("CsHLT::cap_conf_ctrl {%s} %s" % (portlist, action), timeout=300)[2]
        info_msg = "PASS:%s capture on port %s done!" % (action, portlist)
        return self._result_check(STCControlPacketError, info_msg, res)[1]

    def cap_conf_info(self, port):
        """
        Get capture stop status.

        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("get info on port %s is in progress..." % port.handle)
        res = self.tcl.command("CsHLT::cap_conf_info {%s}" % port.handle, timeout=300)[2]
        info_msg = "PASS:get info on port %s done!" % port.handle
        ret = re.findall("ret\:(?P<stopped>[^\s]*)", self._result_check(STCGetPacketStatsError, info_msg, res)[0])
        if ret:
            return ret[0]
        else:
            return None

    def _conf_cap_stats(self, port, filename, format='pcap', **kwargs):
        """
        Returns statistical information about each packet associated with the specified port(s). Statistics include the connection status and number and type of messages sent and received from the specified port.

        Args:
            port: The handle of the port on which to return packet capture information. This argument is mandatory. You can specify "all" to apply this function to all ports (for example, -port_handle all).
            filename: Provide a file name to which to save the captured packets. Specify the file format with the -format argument (for example, "-format pcap"). The default file name and format is Spirent_TestCenter-<timestamp>-<port_handle>.pcap (for example, Spirent_TestCenter-1179466942-port1.pcap).
            kwargs: other option params, must be a dict format.

        return:
            .

        Example:
            >>> config_cap_stats("2/1","c:/tmp/cap")
        """
        self.logger.info("get capture stats on port %s " % port.handle)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::cap_conf_stats %s %s %s {%s}" % (port.handle, filename, format, opt))[2]
        info_msg = "PASS:get capture statistics on port %s done!" % port.handle
        return self._result_check(STCGetPacketStatsError, info_msg, res)[1]

    def _pppoe_client_conf(self, port, mode, **kwargs):

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::pppoe_client_conf %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS: {0} PPPOE client done!".format(mode)
        return self._result_check(STCConfigurePPPoXClientError, info_msg, res)[0]

    def _create_pppoe_client(self, port, **kwargs):
        '''
        Configures PPPoE sessions for the specified Spirent HLTAPI port.
        The Point-to-Point Protocol (PPP) provides a method of transporting
        datagrams over point-to-point links between hosts, switches, and routers.
        Spirent HLTAPI supports Point-to-Point Protocol over Ethernet (PPPoE),
        Point-to-Point Protocol over ATM (PPPoA), and Point-to-Point Protocol over
        Ethernet over ATM (PPPoEoA).

        Args:
        :param port: specified Spirent HLTAPI port
        :param kwargs: other option params, must be a dict format.

        return: will return pppoe handle for further configure or control

        '''
        self.logger.info("Create PPPOE client is in progress...")

        res = self._pppoe_client_conf(port, 'create', **kwargs)
        m = re.search(r'{handle (\w+)}', res)
        return m.group(1)

    def _pppoe_server_conf(self, port, mode, **kw):

        opt = self.dict2str(kw)

        res = self.tcl.command("CsHLT::pppoe_server_conf %s %s {%s}" % (port, mode, opt))[2]

        print '#' * 60
        print res
        print '#' * 60
        info_msg = "PASS: conf PPPoe Server done!"
        return self._result_check(STCConfigurePPPoXServerError, info_msg, res)[0]

    def _create_pppoe_server(self, port, **kwargs):
        """
        Creates PPPoX server session blocks for the specified Spirent HLTAPI port or handle.
        A PPPoX sever is responsible for the dynamic allocation and serving of network addresses to PPPoX clients. It responds to the connection request from the client.

        Args:
        :param port: Spirent test center  port
        :param kwargs: other option params, must be a dict format.

        return: will return pppoe server handle for further configure or control
        """
        self.logger.info("Create PPPOE server is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::pppoe_server_create %s {%s}" % (port, opt))[2]
        print("[%s]" % res)
        info_msg = "PASS: create PPPOE server done!"
        m = re.search(r"{handle (\w+)}", self._result_check(STCConfigurePPPoXServerError,
                                                            info_msg, res)[0])
        return m.group(1)

    def get_pppoe_client_stats(self, handle, mode, **kwargs):
        '''
        Returns PPPoE port statistics associated with the specified port.
        Statistics include the connection status and number and type of messages
        sent and received from the specified port.

        Args:
        :param handle: Specifies the handle of the PPPoE session block for which you want to retrieve PPPoE port statistics. The -handle argument is mandatory.
        :param mode: Specifies the type of statistics to return in the keyed list. The
            -mode argument is mandatory. Possible values are aggregate or session:

            aggregate - retrieves transmitted and received statistics for all
            PPPoE sessions associated with the specified port and a status value (1 for success).

            session - retrieves transmitted and received statistics for only
            the PPPoE sessions specified with -handle.

            Note: Session statistics are only valid after the PPPoE sessions are established. They will not be returned nor accessible until you are connected.

        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        '''
        self.logger.info("Get PPPOE client statistics is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::pppoe_client_stats %s %s {%s}" % (handle, mode, opt))[2]
        info_msg = "PASS: Get PPPOE client statistics done!"
        return self._result_check(STCGetPPPoXStatsError, info_msg, res)[0]

    def get_pppoe_server_stats(self, handle, mode, **kwargs):
        """
        Returns statistics of the PPPoX servers configured on the specified test port.

        Args:
        :param handle: Specifies the handle of the PPPoX server block whose PPPoX statistics you will retrieve.
        :param mode: Specifies the statistics retrieval mode. Possible values are described below:

            aggregate - Aggregates the statistics on all the configured sessions.

            session - Retrieves the statistics on a per session basis.

            Note: Session statistics are only valid after the PPPoX server
            sessions are established. They will not be returned or
            accessible until the sessions are connected.
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """

        self.logger.info("Get PPPOE server statistics is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::pppoe_server_stats %s %s {%s}" % (handle, mode, opt))[2]
        print("[%s]" % res)
        info_msg = "PASS: Get PPPOE server statistics done!"
        return self._result_check(STCGetPPPoXStatsError, info_msg, res)[0]

    def _control_pppoe_server(self, handle, action, **kwargs):
        """
        Controls the pppox server activity on the specified test port.

        Args:
        :param handle: Identifies the server session block on which the actions
            defined by the -action argument will be taken.
            You must specify either -handle or -port_handle, but not both.
        :param action: Specifies the action to perform. Possible values are described below:
            connect - Brings up the configured PPPoX servers.
            disconnect - Tears down connected PPPoX servers
            retry - Attempts to connect PPPoX servers that have
            previously failed to establish
            pause - Pauses the PPPoX servers
            resume - Resumes the PPPoX servers.
            reset - Aborts PPPoX sessions and resets the PPP.
            clear - Clears the status and statistics of the PPP sessions.
            abort - Aborts PPPoX sessions and resets the PPP
            emulation engine (without bringing the sessions back up) on the specified device.
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """
        self.logger.info("%s PPPOE server is in progress..." % action)

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::pppoe_server_ctrl %s %s {%s}" % (handle, action, opt))[2]
        info_msg = "PASS: %s PPPOE server done!" % action
        return self._result_check(STCControlPPPoXError, info_msg, res)[1]

    def _control_pppoe_client(self, handle, action, **kwargs):
        """
        Connects, disconnects, pauses, resumes, retries, or resets the PPPoE sessions for the specified session block.

        Args:
        :param handle: Identifies the session block on which to connect, disconnect, reset, retry, pause, resume, or clear the PPPoX sessions.
        :param action: Specifies the action to perform. Possible values are
            connect, disconnect, reset, retry, pause, resume, and clear.
            You must specify one of these values. The modes are described below:
            connect - Establishes all PPPoX sessions on the specified session block.
            disconnect - Disconnects all established PPPoX sessions from the specified session block.
            retry - Attempts to connect failed PPPoX sessions on the port. You can only use the retry command after the
            sessions have finished attempting to connect (that is the stats show that either aggregate.idle or aggregate.connected is 1).
            reset - Terminates the port. This action does not reset the defaults nor does it attempt to re-connect. To reconnect to the port, you must reconfigure the session block.
            pause - Pause all PPPoX sessions that are connecting or disconnecting.
            resume - Resume PPPoX sessions that were paused with "-action pause" while connecting or disconnecting.
            clear - Clears the PPPoX statistics for the port. You can only use this command after the sessions have been disconnected (that is, aggregate.idle is 1). You cannot clear the PPPoX port statistics while sessions are currently connected (that is aggregate.connected is 1).
            abort - Aborts all PPPoX sessions and resets the PPP emulation engine (without bringing the sessions back up) on the specified device.

        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """
        self.logger.info("%s PPPOE client is in progress..." % action)

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::pppoe_client_ctrl %s %s {%s}" % (handle, action, opt), timeout=60)[2]
        info_msg = "PASS: %s PPPOE client done!" % action
        return self._result_check(STCControlPPPoXError, info_msg, res)[1]

    def config_device(self, port, mode, **kw):
        self.logger.info("%s device is in progress..." % mode)
        opt = self.dict2str(kw)

        res = self.tcl.command("CsHLT::device_conf %s %s {%s}" % (port, mode,
                                                                  opt), timeout=60)[2]
        print res
        info_msg = "PASS %s device is done..." % mode
        return self._result_check(STCConfigureDeviceError, info_msg, res)[0]

    def config_igmp(self, mode, handle, **kwargs):
        """
        Creates, modifies, or deletes Internet Group Management Protocol (IGMP)
        host(s) for the specified Spirent HLTAPI port or handle.

        Args:
        :param mode: Specifies the action to perform. Possible values are create,
            modify, and delete, This argument is mandatory. The modes are
            described below:
            create - Starts emulating IGMP hosts on the specified port
            or handle.

            modify - Changes the configuration parameters for the IGMP
            hosts identified by either the -port_handle or -handle
            argument.

            delete - Stops the IGMP emulation locally without attempting
            to clear the bound addresses from the IGMP server. In
            addition, all IGMP group sessions information on the
            port is cleared and the connection is restarted.

            disable_all - Disables all the IGMP sessions on the specific port.
            If -port_handle is not specified, all IGMP sessions under
            all ports will be disabled.
        :param handle: You must specify -handle when -mode is set to "modify"
            or "delete". When you use -mode create, it is mandatory that
            you specify -port_handle or -handle, but not both.
        :param kwargs: other option params, must be a dict format.

        return: IGMP handle for further configure.
        """
        self.logger.info("%s IGMP is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::igmp_conf %s %s {%s}" % (mode, handle, opt), timeout=60)[2]
        info_msg = "PASS: %s IGMP is done!" % mode
        return str(self._result_check(STCConfigureIGMPError, info_msg, res)[0])

    def add_igmp_host(self, port, ip_addr, mac, vlan=None, count=1, igmp_version="v2",
                      robustness="10", general_query=1, group_query=1, **kwargs):
        option = {}
        if vlan == None:
            pass
        else:
            option["vlan_id"] = str(vlan)
        option["intf_ip_addr"] = str(ip_addr)
        option["source_mac"] = str(mac)
        option["count"] = str(count)
        option["igmp_version"] = str(igmp_version)
        option["robustness"] = str(robustness)
        option["general_query"] = str(general_query)
        option["group_query"] = str(group_query)
        option.update(**kwargs)
        res = self.config_igmp("create", port, **option)
        return res

    def config_igmp_group(self, mode, **kwargs):
        """
        Creates group pools and source pools, and modifies and deletes group and
        source pools from IGMP hosts. This function configures multicast group
        ranges for an emulated IGMP host. You must use the common
        sth::multicast_group_config and sth::multicast_source_config functions with
        this function.

        Args:
        :param mode: Specifies the action to perform. Possible values are create,
            modify, delete, and clear_all. There is no default; you must
            specify a mode. The modes are described below:
            create - Starts emulation on the port specified with
            -handle and associates an existing multicast group
            pool (-group_pool_handle) with the specified IGMP host
            (that is, joins the membership).

            modify - Changes the configuration identified by the -handle
            argument by applying the parameters specified in
            subsequent arguments.
            delete - Remove one group of pools from this session.
            clear_all - Remove all group pools from this session.
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """
        self.logger.info("%s IGMP group is in progress..." % mode)

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::igmp_group_conf %s {%s}" % (mode, opt))[2]
        info_msg = "PASS: %s IGMP group is done!" % mode
        return self._result_check(STCConfigureIGMPGoupError, info_msg, res)[0]

    def control_igmp(self, mode, handle, **kwargs):
        """
        Start, stop, or restart the IGMP host on the
        specified port. Leaves and joins group pools.

        Args:
        :param mode: Specifies the action to perform on the specified handle. If
            you provide a handle (-handle), this argument performs the
            specified action on all groups on this session. If you do
            not provide a handle, this argument performs the specified
            action on all groups on all sessions. Possible values are
            restart, join, and leave. You must specify one of these
            values. The modes are described below:
            restart - Stops and then restarts the groups specified by
            -handle on the specified port. If you do not provide
            a handle, this action stops and restarts all groups
            on all ports.

            join - Joins all groups specified by -handle. If you
            do not provide a handle, this action joins all groups
            on all ports.

            leave - Leave all groups specified by -handle. If you
            do not provide a handle, this action leaves all groups
            on all ports.
            Note: You must send the "leave" actions before
            disconnecting PPPoX sessions. Otherwise, if you
            disconnect a PPPoX session before sending "leaves",
            HLTAPI will not automatically send the "leaves".
        :param handle: Identifies the groups to stop, start, restart, join, or
            leave. If you do not specify a group, the specified action is applied
            to all groups configured on the port specified by -port_handle.
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """
        self.logger.info("%s IGMP is in progress..." % mode)

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::igmp_ctrl %s \"%s\" {%s}" % (mode, handle, opt))[2]
        info_msg = "PASS: %s IGMP is done!" % mode
        return self._result_check(STCControlIGMPGroupError, info_msg, res)[0]

    def get_igmp_stats(self, handle, **kwargs):
        """
        Returns statistics about the IGMP group activity on the specified handle.
        Statistics include the connection status and number and type of messages
        sent and received from the specified port.

        Args:
        :param handle: Specifies the IGMP session handle upon which host
            emulation is configured.
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.

        """
        self.logger.info("getting IGMP statistics is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::igmp_info \"%s\" {%s}" % (handle, opt))[2]
        info_msg = "PASS: get IGMP statistics is done!"
        return self._result_check(STCGetIGMPGroupStatsError, info_msg, res)[0]

    def config_igmp_querier(self, mode, handle, **kwargs):
        """
        The emulation_igmp_querier_config command configures an IGMP router on the
        specified test port.
        Querier is a multicast router that maintains a list of multicast group
        memberships for each attached network. There is normally only one querier per
        physical network. The querier sends out Query messages to determine the multicast
        group memberships for hosts on the attached network.
        The Internet Group Management Protocol (IGMP) is a protocol that provides a way
        for a host computer to report its multicast group membership to adjacent routers.
        A multicast group is configured to receive voice, video, or data traffic sent
        from a multicast server. IGMP is a stateful protocol. The router sends periodic
        queries to the receivers to verify that the hosts want to continue to participate
        in the multicast groups. These queries are transmitted to a well-known multicast
        address (224.0.0.1) that is monitored by all systems. If the receivers are still
        interested in that particular multicast group, they respond with a Membership
        Report message. When the router stops seeing responses to queries, it deletes the
        appropriate group from its forwarding table. For more details on IGMP, please
        refer to the following RFCs:
        RFC 1112 Host Extensions for IP Multicasting
        RFC 2236 Internet Group Management Protocol, Version 2
        RFC 3376 Internet Group Management Protocol, Version 3

        Args:
        :param mode: Specifies the action to perform. Possible values are create,
            modify, and delete. This argument is mandatory. The modes are
            described below:

            create - Starts emulating IGMP routers on the specified port
            or handle.

            modify - Changes the configuration parameters for the IGMP
            router identified by the -handle argument.

            delete - Clears all IGMP group sessions information on the
            port and restarts the connection.
        :param port: Spirent test center port
        :param kwargs: other option params, must be a dict format.

        return: IGMP querier handle for further handle.
        """
        self.logger.info("%s IGMP querier is in progress..." % mode)

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::igmp_querier_conf %s %s {%s}" % (mode, handle, opt))[2]
        info_msg = "PASS: %s IGMP querier is done!" % mode
        return self._result_check(STCConfigureIGMPQuerierError, info_msg, res)[0]

    def add_igmp_querier(self, port, ip_addr, mac, vlan_id=None, count=1, igmp_version="v2", **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        option = {}
        if vlan_id == None:
            pass
        else:
            option["vlan_id"] = str(vlan_id)
        option["source_mac"] = str(mac)
        option["intf_ip_addr"] = str(ip_addr)
        option["count"] = str(count)
        option["igmp_version"] = str(igmp_version)
        option.update(**kwargs)

        self.config_igmp_querier("create", port, **option)

    def control_igmp_querier(self, mode, name, **kwargs):
        """
        Starts or stops sending Query messages from the selected queriers to attached
        hosts on the specified port.

        Args:
        :param mode: Specifies the action to perform on the specified handle. If you
            provide a handle (-handle), this argument performs the specified
            action on all groups on this session. If you do not provide a
            handle, this argument performs the specified action on all groups
            on all sessions. Possible values are start and stop.
            start - Starts sending Query message from the selected queriers
            to attached hosts..

            stop - Stops sending Query message from the selected queriers to
            attached hosts. The queriers also stop responding to Report
            and Leave messages from attached hosts.
            This argument is mandatory.
        :param port: Spirent test center port
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """
        self.logger.info("%s IGMP querier is in progress..." % mode)

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::igmp_querier_ctrl %s %s {%s}" % (mode, name, opt))[2]
        info_msg = "PASS: %s IGMP querier is done!" % mode
        return self._result_check(STCControlIGMPQuerierError, info_msg, res)[0]

    def get_igmp_querier_stats(self, port, **kwargs):
        """
        Retrieves statistics for the IGMP Routers configured on the specified test ports.

        Args:
        :param port: Specifies the port on which to retrieve statistics.
        :param kwargs: other option params, must be a dict format.

        return: return SUCCESS or ERROR.
        """
        self.logger.info("getting IGMP querier statistics is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::igmp_querier_info %s {%s}" % (port, opt))[2]
        info_msg = "PASS: get IGMP querier statistics is done!"
        return self._result_check(STCGetIGMPQuerierStatsError, info_msg, res)[0]

    def check_querier_state(self, querier_handle, key):
        """
        This procedure is used to verify IGMP querier states in statistics.

        Args:
            querier_handle: IGMP querier statistics, it should be a Tcl keyed list.
            key: The key which you'll verify.

        return: return SUCCESS or ERROR.
        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("checking IGMP querier state is in progress...")

        res = self.tcl.command("CsHLT::check_querier_state \"%s\" %s" % (querier_handle, key))[2]
        r = self.verify(res)

        if r == CSTC.ERROR:
            raise STCSessionException("ERROR:Failed to check IGMP querier state!")
        else:
            self.logger.info("PASS: check IGMP querier state is done!")
            return res

    def config_multicast_group(self, mode, **kwargs):
        """
        Creates, modifies, or deletes multicast groups on Spirent HLTAPI. Use
        these multicast functions with the HLTAPI functions for the IGMP (for
        IPv4), MLD (for IPv6), and PIM protocols.

        Args:
        :param mode: Specifies the action to perform. Possible values are create,
            modify, or delete, This argument is mandatory. The modes are
            described below:

            create - Creates a multicast group pool.

            modify - Changes the configuration parameters for the
            multicast group identified by the -handle argument.

            delete - Deletes the multicast group pool specified by
            -handle.
        :param kwargs:

        return:
        """
        self.logger.info("%s multicast group is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::multicast_group_conf %s {%s}" % (mode, opt))[2]
        info_msg = "PASS: %s multicase group is done!"
        return self._result_check(STCConfigureMulticastGroupError, info_msg, res)[0]

    def config_multicast_source(self, mode, **kwargs):
        """
        Creates, modifies, or deletes multicast sources on Spirent HLTAPI. Use
        this procedure with the sth::emulation_igmp_group_config (IGMPv3),
        sth::emulation_mld_group_config (MLD), and
        sth::emulation_pim_group_config (PIM) procedures. Source pool definitions
        might be shared among ports if supported by vendor.

        Args:
        :param mode: Specifies the action to perform. Possible values are create,
            modify, or delete, This argument is mandatory. The modes are
            described below:

            create - Creates a multicast source pool.

            modify - Changes the configuration parameters for the
                     multicast source identified by the -handle argument.

            delete - Deletes the multicast source pool specified by
            -handle.
        :param kwargs:

        return:
        """
        self.logger.info("%s multicast source is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::multicast_source_conf %s {%s}" % (mode, opt))[2]
        info_msg = "PASS: %s multicase source is done!"
        return self._result_check(STCConfigureMulticastSourceError, info_msg, res)[0]

    def create_device(self, port, **kwargs):
        """
        Creates emulated devices

        Args:
            port: Specifies the port on which to create the emulated device.
            kwargs: option parameters.

        return:
            test log info.
        """

        """
        1. There is a duplicate method in the App(0 driver called create device
        2. This method is called by the add_device mthod in this module but, the add device usage
           in only in demo code.
        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("Create device is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::create_device %s {%s}" % (port, opt))[2]
        print("[handle is : %s]" % res)
        print res[-1]
        info_msg = "PASS: Create device is done!"
        return self._result_check(STCConfigureDeviceError, info_msg, res)[0]

    def modify_device(self, device_handle, **kwargs):
        """
        Modify emulated devices

        Args:
            device_handle: Specifies the device handle. This argument is mandatory for -mode
modify.
            kwargs: option parameters.

        return:
            test log info.
        """
        """
        1. This method is duplicated by the modify_device in the App() driver.
        2. The interrnal methods that call this method only show usage in demo code.
        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("Modify device is in progress...")

        opt = self.dict2str(kwargs)

        res = self.tcl.command("CsHLT::modify_device %s {%s}" % (device_handle, opt))[2]
        print("[%s]" % res)
        info_msg = "PASS: Modify device is done!"
        return self._result_check(STCConfigureDeviceError, info_msg, res)[0]

    def modify_device_count(self, device_handle, count, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        d["count"] = str(count)
        d.update(**kwargs)
        self.modify_device(device_handle, **d)

    def modify_device_ipv4(self, device_handle, ip, gateway, step_length="0.0.0.1",
                           gateway_length="0.0.0.1", **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        d["intf_ip_addr"] = str(ip)
        d["intf_ip_addr_step"] = str(step_length)
        d["gateway_ip_addr"] = str(gateway)
        d["gateway_ip_addr_step"] = str(gateway_length)
        d.update(**kwargs)
        self.modify_device(device_handle, **d)

    def add_device(self, port, count, ip_version, ip, mac, vlan=None,
                   priority=None, encapsulation=None, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        if ip_version == "ipv4":
            d["count"] = str(count)
            d["intf_ip_addr"] = str(ip)
            d["ip_version"] = str(ip_version)
            d["mac_addr"] = str(mac)
        elif ip_version == "ipv6":
            d["count"] = str(count)
            d["intf_ipv6_addr"] = str(ip)
            d["ip_version"] = str(ip_version)
            d["mac_addr"] = str(mac)
        if encapsulation:
            en = {"encapsulation": "ethernet_ii_vlan"}
            d.update(en)
        if vlan:
            v = {"vlan_id_step": str(vlan)}
            d.update(v)
        if priority:
            p = {"vlan_user_pri": str(priority)}
            d.update(p)
        res = self.create_device(port, **d)
        return res

    def modify_device_ipv6_global(self, device_handle, ipv6_addr, gateway,
                                  ipv6_addr_step="::1", gateway_step="::", **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        d["intf_ipv6_addr"] = str(ipv6_addr)
        d["intf_ipv6_addr_step"] = str(ipv6_addr_step)
        d["gateway_ipv6_addr"] = str(gateway)
        d["gateway_ipv6_addr_step"] = str(gateway_step)
        d.update(**kwargs)

        self.modify_device(device_handle, **d)

    def modify_device_ipv6_local(self, device_handle, local_ipv6_addr, local_ipv6_addr_step="::1",
                                 local_ipv6_prefix="64", **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")

        d = {}
        d["link_local_ipv6_addr"] = str(local_ipv6_addr)
        d["link_local_ipv6_addr_step"] = str(local_ipv6_addr_step)
        d["link_local_ipv6_prefix_len"] = str(local_ipv6_prefix)
        d.update(**kwargs)
        self.modify_device(device_handle, **d)

    def modify_device_mac(self, device_handle, mac, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        d["mac_addr"] = str(mac)
        d.update(**kwargs)
        self.modify_device(device_handle, **d)

    def modify_device_outer_vlan(self, device_handle, vlan, pbit, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        d["vlan_outer_id"] = str(vlan)
        d["vlan_outer_user_pri"] = str(pbit)
        d.update(**kwargs)
        self.modify_device(device_handle, **d)

    def modify_device_inner_vlan(self, device_handle, vlan, pbit, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        d = {}
        d["vlan_id_step"] = str(vlan)
        d["vlan_user_pri"] = str(pbit)
        d.update(**kwargs)
        self.modify_device(device_handle, **d)

    def modify_loam_device(self):
        raise NotImplementedError

    def modify_rstp_device(self):
        raise NotImplementedError

    def add_dhcp_server(self, port, count, mac, ip,
                        gateway, ip_pool_address,
                        ip_count=100, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        option = {
            "ip_step": "0.0.0.1",
            "ipaddress_increment": "2",
            "lease_time": "60"
        }
        option.update(**kwargs)
        option["count"] = str(count)
        option["local_mac"] = str(mac)
        option["ip_address"] = str(ip)
        option["ip_gateway"] = str(gateway)
        option["ipaddress_pool"] = str(ip_pool_address)
        option["ipaddress_count"] = str(ip_count)
        option.update(**kwargs)
        print option
        self.create_dhcp_server(port, **option)

    def add_dhcp_client(self, port, count, mac, **kwargs):
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        option_basic = {
            "retry_count": "20",
            "request_rate": "1000",
            "outstanding_session_count": "100",
            "broadcast_bit_flag": "1"
        }
        res = self.create_dhcp_client_basic(port, **option_basic)
        print res

        option_group = {
            "encap": "ethernet_ii",
            "protocol": "dhcpoe",
            "num_sessions": "20",
            "mac_addr": "00.00.10.95.11.15"
        }
        option_group["num_sessions"] = str(count)
        option_group["mac_addr"] = str(mac)
        option_group.update(**kwargs)
        print "##################%s###################" % res.split()[-1]
        self.config_dhcp_client_group(res.split()[-1], "create", **option_group)

    def delete_device(self, device_handle):
        # This method is duplicated by the delete_device method in the App() driver
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("Delete device is in progress...")
        res = self.tcl.command("CsHLT::delete_device %s" % device_handle)[2]
        print("[%s]" % res)
        info_msg = "PASS: , delete device is done!"
        return self._result_check(STCConfigureDeviceError, info_msg, res)[0]

    def close(self):
        """
        close tcl remote session


        return: none
        """
        self.tcl.close()

    def get_list_value(self, keylist, key=""):
        """
        get value form tcl keylist

        Args:
        :param keylist: tcl data structure keylist
        :param key: Specify the key to get the corresponding value.

        return: value of the key you've specified.

        Example:
            >>> keylist = "{session {{1/8/5/3400000 {{acks_received 1} {lease_time 1000} {gateway_address 10.10.0.2}}}}} {status 1}"
            >>> get_list_value(keylist, status)
        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        res = self.tcl.command("CsHLT::get_list_value \"%s\" %s" % (keylist, key))[2]
        return res

    def verify(self, response):
        """
        used to check if "SUCCESS" is appeared in response.

        Args:
        :param response: (return) response info

        return: <SUCCESS> or <ERROR>

        Example:
            >>> res = "FAilED, PASS, ERROR, SUCCESS"
            >>> verify(res)
        """
        flag = CSTC.SUCCESS
        if flag not in response:
            flag = CSTC.ERROR
            return flag
        return flag

    def dict2str(self, dict):
        """
        convert dictionary to string

        Args:
            dict: python date structure dictionary

        return: string, format : " -key1 value1 -key2 value2"

        Example:
            >>> dict = {"key1":"1","key2":"2","key3":"3"}
            >>> dict2str(dict)
        """
        strings = ""
        for k, v in dict.iteritems():
            strings = strings + " -{0} {1}".format(str(k), str(v))
        return strings

    def send_tcl_cmd(self, cmd):
        """
        send tcl command to remote shell

        :param cmd: tcl command

        return: return info base on tcl command

        Example:
            >>> send_tcl_cmd("set a 10")
            >>> send_tcl_cmd("puts $a")
        """
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("send tcl command to remote tcksh...")
        res = self.tcl.command("%s" % cmd)[2]
        return res

    def list2str(self, list):
        """
        this procedure is used to convert list to string.

        Args:
        :param list: python list.

        return: string.
        """
        string = ""
        for i in list:
            string = string + " " + str(i)
        return string

    def _emulation_dhcp_server_config(self, port, mode, version, **kwargs):
        self.logger.info("%s DHCP server is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_server_config %s %s %s {%s}" % (port, mode, version, opt))[2]
        info_msg = "PASS:%s dhcp server done!" % mode
        return str(self._result_check(STCConfigureDHCPServerError, info_msg, res)[0]).split()[-1]

    def _emulation_dhcp_client(self, port, mode, **kwargs):
        self.logger.info("%s DHCP client is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_config %s %s {%s}" % (port, mode, opt))[2]
        info_msg = "PASS:%s dhcp client done!" % mode
        return self._result_check(STCConfigureDHCPClientError, info_msg, res)[0]

    def _emulation_dhcp_client_group(self, handle, mode, version, **kwargs):
        self.logger.info("%s DHCP client group is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_group_config %s %s %s {%s}" % (handle, mode, version, opt))[2]
        info_msg = "PASS:%s dhcp client group done!" % mode
        return self._result_check(STCConfigureDHCPClientGroupError, info_msg, res)[0]

    def _reset_dhcp_client(self, handle, **kwargs):
        '''
        '''
        self.logger.info("reset DHCP server is in progress...")
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::resetDhcpClient %s {%s}" % (handle, opt))[2]
        info_msg = "PASS:reset dhcp server done!"
        return self._result_check(STCConfigureDHCPServerError, info_msg, res)[0]

    def _emulation_dhcp_client_stats(self, port, action, **kwargs):
        '''

        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("%s DHCP server is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_server_stats %s {%s}" % (port, opt))[2]
        info_msg = "PASS:%s dhcp server done!" % action
        return self._result_check(STCGetDHCPServerStatsError, info_msg, res)[0]

    def _emulation_dhcp_server_stats(self, port, action, **kwargs):
        '''

        '''
        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")
        self.logger.info("%s DHCP server stats is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_server_stats %s {%s}" % (port, opt))[2]
        info_msg = "PASS:%s dhcp server stats done!" % action
        return self._result_check(STCGetDHCPServerStatsError, info_msg, res)[0]

    def _emulation_dhcp_server_control(self, port, action, **kwargs):

        self.logger.info("%s DHCP server control is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_server_control %s %s {%s}" % (port, action, opt))[2]
        info_msg = "PASS:%s dhcp server control done!" % action
        return self._result_check(STCControlDHCPServerError, info_msg, res)[0]

    def _emulation_dhcp_client_control(self, port, action, **kwargs):
        '''

        '''

        self.logger.info("%s DHCP client control is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_control %s %s {%s}" % (port, action, opt))[2]
        print("====>", res)
        info_msg = "PASS:%s dhcp client control done!" % action
        return self._result_check(STCControlDHCPClientGroupError, info_msg, res)[0]

    def _emulation_dhcp_server_relay_agent_config(self, handle, action, **kwargs):

        self.logger.info("%s DHCP server relay agent is in progress..." % action)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_dhcp_server_relay_agent_config %s %s {%s}" % (handle, action, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCSessionException("ERROR:Failed to %s dhcp server relay agent!" % action)
        else:
            self.logger.info("PASS:%s dhcp server relay agent done!" % action)
            return res

    def _result_check(self, exception_class, info_msg, response_msg):
        ver_flag = self.verify(response_msg)
        if ver_flag == CSTC.ERROR:
            raise exception_class

        self.logger.info(info_msg)
        return response_msg, ver_flag

    def _warning_check(self, warn_msg, info_msg, response_msg):
        ver_flag = self.verify(response_msg)
        if ver_flag == CSTC.ERROR:
            self.logger.warn(warn_msg)
        else:
            self.logger.info(info_msg)
        return ver_flag


    def _emulation_bgp_config(self, mode, **kwargs):

        self.logger.info("%s bgp config is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_bgp_config %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCBGPConfigError
        else:
            self.logger.info ("PASS: %s bgp_config is done!")
            return res

    def _emulation_bgp_route_config(self, mode, **kwargs):

        self.logger.info("%s bgp route config is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_bgp_route_config %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCBGPRouteConfigError
        else:
            self.logger.info ("PASS: %s bgp_route_config is done!")
            return res

    def _emulation_bgp_route_generator(self, mode, **kwargs):

        self.logger.info("%s bgp route generator is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_bgp_route_generator %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCBGPRouteGeneratorError
        else:
            self.logger.info ("PASS: %s bgp_route_generator is done!")
            return res

    def _emulation_bgp_control(self, mode, **kwargs):

        self.logger.info("%s bgp control is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_bgp_control %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCBGPControlError
        else:
            self.logger.info ("PASS: %s bgp_control is done!")
            return res

    def _emulation_bgp_info(self, mode, **kwargs):

        self.logger.info("%s bgp info is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_bgp_info %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCBGPInfoError
        else:
            self.logger.info ("PASS: %s bgp_info is done!")
            return res

    def _emulation_bgp_route_info(self, mode, **kwargs):

        self.logger.info("%s bgp route info is in progress...")

        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_bgp_route_info %s {%s}" % (mode, opt))[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCBGPInfoError
        else:
            self.logger.info ("PASS: %s bgp_route_info is done!")
            return res

    def _emulation_ospf_config(self, handle, mode, **kwargs):
        self.logger.info("%s ospf config is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_ospf_config %s %s {%s}" % (handle, mode, opt), timeout=60)[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCOSPFConfigError
        else:
            self.logger.info("PASS: %s emulation_ospf_config is done!" % mode)
            return res

    def _emulation_ospf_topology_route_config(self, mode, **kwargs):
        self.logger.info("%s ospf_topology_route config is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_ospf_topology_route_config %s {%s}" % (mode, opt), timeout=60)[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCOSPFTopoRouteConfigError
        else:
            self.logger.info("PASS: %s emulation_ospf_topology_route_config is done!" % mode)
            return res

    def _emulation_ospf_lsa_config(self, mode, **kwargs):
        self.logger.info("%s ospf_lsa config is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_ospf_lsa_config %s {%s}" % (mode, opt), timeout=60)[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCOSPFLSAConfigError
        else:
            self.logger.info("PASS: %s emulation_ospf_lsa_config is done!" % mode)
            return res

    def _emulation_ospf_control(self, handle, mode, **kwargs):
        self.logger.info("%s ospf is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::emulation_ospf_control %s %s {%s}" % (handle, mode, opt), timeout=60)[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCOSPFConfigError
        else:
            self.logger.info("PASS: %s emulation_ospf_control is done!" % mode)
            return res

    def _emulation_ospf_info(self, handle, mode, version):
        self.logger.info("ospf %s info is in progress..." % version)
        res = self.tcl.command("CsHLT::emulation_ospf_info %s %s %s" % (handle, mode, version), timeout=60)[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCOSPFConfigError
        else:
            self.logger.info("PASS: %s emulation_ospf_control is done!" % version)
            return res

    def _emulation_ospf_router_info(self, handle):
        self.logger.info("ospf router info is in progress...")
        res = self.tcl.command("CsHLT::emulation_ospf_router_info %s" % handle, timeout=60)[2]
        r = self.verify(res)
        if r == CSTC.ERROR:
            raise STCOSPFConfigError
        else:
            self.logger.info("PASS: %s emulation_ospf_router_control is done!")
            return res

    def _config_isis(self, port, mode, **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CsHLT::isis_config %s %s {%s}"%
                               (port, mode, opts))[2]
        if self.verify(res) == 'ERROR':
            raise  STCConfigureISISError
        return res

    def _control_isis(self, lsp_session_handle, mode, **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CsHLT::isis_control %s %s {%s}" %
                               (lsp_session_handle, mode, opts))[2]

        if self.verify(res) == 'ERROR':
            raise STCControlISISError

        return res

    def _isis_info(self, isis_router_handle, mode="stats"):

        res = self.tcl.command("CsHLT::isis_info %s %s" % (isis_router_handle, mode))[2]

        r = self.verify(res)

        if r == CSTC.ERROR:
            raise STCGetISISInfoError
        else:
            return res

    def _config_isis_topology_route(self, isis_handle, mode , **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CsHLT::isis_topology_route_config %s %s {%s}"%
                               (isis_handle, mode , opts))[2]
        if self.verify(res) == 'ERROR':
            raise STCConfigureISISTopologyRouteError
        return res

    def _config_isis_lsp_generator(self, isis_handle, mode , **kw):

        opts = self.dict2str(kw)

        res = self.tcl.command("CsHLT::isis_lsp_generator_config %s %s {%s}"%
                               (isis_handle, mode , opts))[2]
        if self.verify(res) == 'ERROR':
            raise STCConfigureISISLspGeneratorError
        return res

#CSTC = _CSTC
class CSTC(_CSTC):
    def __init__(self, host=None, user=None, password=None, tcl_shell="tclsh.exe", logger=Logger(__name__),
                 remote=True):
        """
        In init function, will do:
        1.open a session to your Windows machine hosting the Tcl Code.
        2.append tcl path to system env variable.
        3.load tcl package.
        Args:
            host: windows system host ip address.
            user: windows system host login username.
            password: windows system host login password.

        """

        self.logger = logger
        self.remote = remote

        self.logger.warn(msg="WARNING: This method is set for deprecation. Any test cases that are directly accessing "
                             "the session manager should be reworded to use the App() driver. Expected deprecation "
                             "date December 2016")

        if remote:
            if host is None:
                raise STCSessionException("ERROR: host is None")

            if user is None:
                raise STCSessionException("ERROR: user is None")

            if password is None:
                raise STCSessionException("ERROR: password is None")

            self.tcl = TCLRemoteShell(host, user, password, tcl_shell=tcl_shell, logger=logger)
            self.tcl.session_log.console = True

            self.__port_list = None

            self.logger.info("loading package CalixStcHltApi...")
            self.tcl.command("set auto_path [linsert $auto_path 0 c:/Tcl/lib]")
            pkg = self.tcl.command("package req CalixStcHltApi")[2]
            if "Spirent STC HLTAPI has been loaded!" in pkg:
                self.logger.info("PASSED: Tcl package is loaded!")
            else:
                raise STCSessionException("ERROR: Failed to load tcl package!")
        else:

            # check if it is centos
            if not "CENTOS" == platform.dist()[0].upper():
                raise STCSessionException("ERROR: platform (%s) is not supported for the local tcl shell"
                                          % platform.dist()[0])

            logger.warning("For local tcl shell, tclsh is default to /opt/active_tcl/bin/tclsh")
            logger.warning("For local tcl shell, user cafetest is being used")

            logfile = os.path.join(cafe.get_config().cafe_runner.log_path, "cstc.log")
            self.tcl = TclSession(sid="cstc", width=400, height=80, tclsh="/opt/active_tcl/bin/tclsh",
                                  timeout=120, logger=logger, logfile=logfile)
            logger.warning("Tcl shell log: %s" % logfile)
            logger.debug(self.tcl.command("echo $auto_path"))

            ##
            # hack: update stc tcl session with stc tcl lib file in repo
            ##
            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            tcl_lib_pathname = os.path.join(path, "hltapi_stc.tcl")
            print tcl_lib_pathname

            dest_tcl_lib_pathname = os.path.join("/tmp", "hltapi_stc.tcl")
            shutil.copy(tcl_lib_pathname, dest_tcl_lib_pathname)
            r = self.tcl.command("source %s" % dest_tcl_lib_pathname)
            logger.debug(r[2])

            if "Spirent STC HLTAPI has been loaded!" in r[2]:
                self.logger.info("PASSED: Tcl package is loaded!")
            else:
                raise STCSessionException("ERROR: Failed to load tcl package!")
