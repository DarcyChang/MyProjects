import collections
import re
import os
import time

import cafe
from cafe.core.logger import CLogger as Logger
from cafe.core.utils import Param
from cafe.equipment.ixia.cixia import _CIXIA, TrafficConfigError, IXIASessionException, IXIA_SESSION_ERROR
from cafe.core.exceptions.tg.ixia import *
from handle import Handle

_module_logger = Logger(__name__)


class IXIADriver(_CIXIA):

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    default_prompt = collections.OrderedDict(
        {r"[^\r\n].+\#": None,
         r"[^\r\n].+\>": None,
         r"[^\r\n].+\$": None,
         r"[^\r\n].+\:\~\$": None,
         r"[^\r\n]+(\%)": None,
         }
    )
    error_response = r"error"

    def __init__(self, session=None, name=None, default_timeout=5, crlf="\n", app=None):

        super(_CIXIA, self).__init__()
        self.session = session
        self.current_prompt = None
        self._set_prompt(self.default_prompt)
        self.default_timeout = default_timeout
        self.crlf = crlf
        self.buf = ""
        self.msg = ""

        #name of driver
        self.name = name

        #reference to app module
        self.app = app

        self.stats = {}
        self.handles = []
        #create atrributes which is compatible with base class
        self.logger = self.session.logger
        self.tcl = self.session
        self.chassis_ip = None
        self.port_list = None
        self.ix_network_tcl_server = None

    def __debug_print(self, var):
        print "#"*80
        print var
        print "#"*80

    def _update_app_result(self, stats):
        """
        update the app module result data structure

        Args:
            stats (dict) - stats result of traffic generator
        """

        if self.app:
            d = {}
            d["session"] = self.name
            d["prompt"] = None
            d["content"] = str(stats)
            d["stats"] = stats

            #import pprint; pprint.pprint(d)
            self.app.update_result(d)

    def _set_handle(self, ref, name, handle, htype, neg=None):
        """
        set handle and create a attribute into traffic gen object.
        """

        if not hasattr(self, ref):
            h = Handle(ref, name, handle, htype, neg)
            self.handles.append(h)
            setattr(self, ref, h)
        else:
            raise TrafficConfigError("reference %s already exist in traffic gen data structure." % ref)

    def _get_handle(self, ref, htype):
        """
        Obtain handle from traffic gen object.
        """
        handle_instance = filter(lambda x: x.ref == ref and x.handle_type == htype, self.handles)
        if not handle_instance:
            raise ValueError("Obtain handle failed, [{}] not found".format(ref))
        return handle_instance[0].handle

    def _del_handle(self, ref, htype):
        """
        Delete handle from traffic gen object.
        """
        handle_instance = filter(lambda x: x.ref == ref and x.handle_type == htype, self.handles)
        if not handle_instance:
            raise ValueError("Delete handle failed, [{}] not found".format(ref))
        self.handles.remove(handle_instance[0])
        delattr(self, ref)

    def _from_handle_to_ref(self, handle):
        """
        Translate handle value to ref value
        If handle is not find in self.handle return handle itself
        """
        for h in self.handles:
            if handle == h.handle:
                return h.ref
        return handle

    def _check_name(self, name, has_attr=False):

        if not isinstance(name, (str, unicode)):
            raise TypeError('name should be a string format!')

        if has_attr and not hasattr(self, name):
            raise TypeError('invalid name to obtain the corresponding handle!')

    def _check_port(self, port):

        ports = self.get_handles('port')
        self.p = []
        map(lambda x: self.p.append(x.value), [y for y in ports])
        if str(port) not in self.p:
            raise ValueError('port %s not found' % port)

    def _check_stream(self, stream):

        s = self.get_handles('stream')
        ss = []
        for i in s:
            ss.append(i.value)
        if stream not in ss:
            raise ValueError('Stream %s not found!'% stream)

    def _flatten_and_translate(self, d, parent_key='', sep='.'):
        """
        flatten nested dictionary and translate value to traffic specific key values

        """
        items = []
        for k, v in d.items():
            #k is traffic gen object handle
            _k = self._from_handle_to_ref(k)
            new_key = parent_key + sep + _k if parent_key else _k
            if isinstance(v, collections.MutableMapping):
                items.extend(self._flatten_and_translate(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def get_handles(self, htype):
        """
        return a list of handle of same handle type
        """
        ret = []
        #print self.handles
        for h in self.handles:
            if h.handle_type == htype.lower():
                ret.append(h)
        return ret

    def del_handles(self):
        """
        del handles related IXIA handles, including port handles
        """
        for h in self.handles:

            if hasattr(self, h.ref) is True:
                delattr(self, h.ref)

        self.handles = []

    def clear_session(self, *args, **kwargs):
        '''
        Purpose:
            Cleans up the current test by terminating port reservations, disconnecting
            the ports from the chassis, releasing system resources, and removing the
            specified port configurations.
        Args:
        '''
        self.del_handles()

        res = self.tcl.command("CiHLT::cleanupSession", timeout=120)[2]
        r = self.verify(res)
        if r == "ERROR":
            #raise IXIASessionException("ERROR:Failed to cleanup session")
            raise IXIACleanupSessionError
        else:
            self.logger.info("PASS:Cleanup session done!")
            return r

    def set_session(self, session):
        self.session = session

    def _set_prompt(self, d):
        self.prompt = d.keys()
        self.action = d.values()

    def cmd(self, *args, **kwargs):
        r = self.session.command(*args, **kwargs)
        return {"prompt": r[1], "value": r[2], "content": r[2]}

    @cafe.teststep("send command")
    def command(self, *args, **kwargs):
        return self.cmd(*args, **kwargs)

    @cafe.teststep("send command")
    def cli(self, *args, **kwargs):
        return self.cmd(*args, **kwargs)

    def get_port_handle(self, port):

        self.logger.info("get port handle for port %s" % port)
        res= self.session.command("CiHLT::getPortHandle %s" % port, timeout=60)
        if res[0] > -1:
            m = re.search(r"(\d/\d{1,2}/\d{1,2})", res[2])
            if m:
                return m.group(1)
            else:
               raise TrafficConfigError("cannot get port handle for %s." % port)
        else:
            raise TrafficConfigError("cannot get port handle for %s. reason: command timeout" % port)

    def _process_stats(self, s):
        """
        extract the tcl result into python dictionary
        """
        if not self.SUCCESS in s:
            return Param({"status": -2})

        #parse the ret and convert into dictionary
        m = re.search(r"\#\#\#([^\#]+)\#\#\#", s)
        if m:
            x = m.group(1)
            p = Param()
            try:
                p.load_yaml_string(x)
                return p
            except TypeError:
                raise TypeError('invalid yaml file!')
        else:
            return Param({"status": -1})

    @cafe.teststep("get stats into buffer")
    def get_stats(self, reset=True):
        """
        Purpose:
            read the traffic gen stats and put them into traffic gen stats dictionary in flatten form.
        return:
            all of the stats stored
            Examples: ret.last.stats['p1.stream.streamblock1.rx.avg_delay'] will get the avg_delay info
        Note:
            it is deprecated to use the return value directly, instead you should call
            get_stats_by_key_regex to get the stat info after this call

        """

        if reset:
            self.stats = {}
        ret = self.return_stats().replace('gateway_address: ::', "gateway_address: '::'")
        p = self._process_stats(ret)
        _p = self._flatten_and_translate(p)
        self.stats.update(_p)
        print self.stats
        for k, v in sorted(self.stats.items()):
            self.logger.debug(k + ":" + str(v))
        self._update_app_result(_p)
        return _p

    @cafe.teststep("get traffic gen stats by key regex")
    def get_stats_by_key_regex(self, key):
        print key
        print self.stats
        ret = {}
        for k, v in self.stats.items():
            m = re.search(key, k)
            if m:
                ret[k] = v
        if ret:
            return ret
        else:
            raise RuntimeError("key %s found!" % key)

    def _get_traffic_stats(self):
        """
        :return:
        """
        ports = self.get_handles("port")
        self.logger.debug("port handles " + str(ports))

        #reset stats
        self.stats = {}
        self.traffic_stats('streams')
        self.get_stats()
        self._update_app_result(self.stats)
        return self.app.result

    def open(self, chassis_ip, equipment_type="ix_network", ports={},
             ixNetworkTclServer="10.245.44.201.8009", tcl_server=""):
        if equipment_type != 'ix_network':
            raise ValueError('Invalide Device Type')
        self.chassis_ip = chassis_ip
        self.port_list = ports
        self.ix_network_tcl_server = ixNetworkTclServer
        self.tcl_server=tcl_server

        #self.connect_to_chassis()

    #def open(self, chassis_ip, equipment_type="ix_network", ports={}, ixNetworkTclServer="10.245.44.201:8009"):

    @cafe.teststep('connect to ixia chassis!')
    def connect_to_chassis(self):
        '''
        Purpose:
            open a session to traffic generator and initialized the ports.
            Register the session object into the App() object

        Args:
            chassis_ip: ip address of test equipment
            equipment_type: {stc|ix_network}
            ports: dictionary of ports and their attributes for initialization.
            ix_network_ip: if equipment_type is ix_network, ixNetwork TCL server ix_network_ip need to be specified
            ix_network_port: tcp port of ixNetwork TCL server. default 8890

        Returns:
            session: test equipment session object

        Raises:
            EqptNotConnected: not able to connected to test equipment
            EqptPortNotAvailable: not able to reserved test equipment port or initialize the port.
        '''


        if True:
            # The port has to be sorted in order to get the same test execution sequence
            self.enable_test_log('/tmp/')
            _p = []
            for k in sorted(self.port_list.keys()):
                v = self.port_list[k]
                _p.append(v['port'])
            port_list = " ".join(_p)
            super(IXIADriver, self).connect_to_chassis(self.chassis_ip, port_list,
                                                       ixNetworkTclServer=self.ix_network_tcl_server,
                                                       tcl_server=self.tcl_server)

            for k in sorted(self.port_list.keys()):
                v = self.port_list[k]
                port = v['port']
                handle = self.get_port_handle(port)
                self._set_handle(k, port, handle, 'port')

    @cafe.teststep('configure ixia interfaces!')
    def config_interfaces(self):
        if True:
            cnt = 0
            for k in sorted(self.port_list.keys()):
                v = self.port_list[k]
                cnt += 1
                port = v['port']
                medium  = v["medium"]
                speed   = v["speed"]
                option  = {
#                    "intf_mode":          "ethernet",
                    "phy_mode":           medium,
                    'auto_detect_instrumentation_type': 'floating',
                    "speed":              speed,
#                    "autonegotiation":    "1",
#                    "duplex":             "full",
#                    "src_mac_addr":       "00:10:94:00:00:3%d" % cnt,
#                    "intf_ip_addr":       "10.1.%d.2" % cnt,
#                    "gateway":            "10.1.%d.1" % cnt,
#                    "netmask":            "255.255.255.0",
#                    "arp_send_req":       "1"
                 }
                self._conf_interface(port, "config", **option)

    def get_discovered_neighbor_ip(self, port):

        self._check_port(port)

        res = self.tcl.command("CiHLT::getDiscoveredNeighborIp %s" % (port))[2]

        return res.split('\r\n')[1].replace('\r', '').split()

    def get_arp_table(self, port):
        self._check_port(port)
        res = self.tcl.command("CiHLT::getArpTable %s" % (port))[2]
        return res.split('\r\n')[1].replace('\r', '').split()

    def clear_arp_table(self, port):
        self._check_port(port)
        res = self.tcl.command("CiHLT::ClearArpTable %s" % (port))[2]
        if not self.verify(res) == self.SUCCESS:
            #raise ValueError('Failed to send Arp Command')
            raise IXIAHostSendCommandError
        return res

    def create_static_host_on_port(self, name, port, src_mac_addr, intf_ip_addr, net_mask, gateway, **kw):

        self._check_name(name)
        self._check_port(port)

        v = self.port_list[port.ref]

        opts = {'src_mac_addr': src_mac_addr,
                'arp_send_req': 1,
                'intf_ip_addr': intf_ip_addr,
                'netmask': net_mask,
                'gateway': gateway,
                'speed': v['speed'],
                'phy_mode': v['medium'],
                'auto_detect_instrumentation_type': 'floating'
        }

        opts.update(**kw)

        res = self._conf_interface(port, 'config', **opts)
        interface = res.split()[-1]
        self._set_handle(name, name, interface, 'device')


    def create_static_hostv6_on_port(self, name, port, src_mac_addr,
                                     ipv6_intf_addr, ipv6_prefix_length,
                                     ipv6_gateway, **kw):

        self._check_name(name)
        self._check_port(port)

        v = self.port_list[port.ref]

        opts = {'src_mac_addr': src_mac_addr,
                'arp_send_req': 1,
                'ipv6_intf_addr': ipv6_intf_addr,
                'ipv6_prefix_length': ipv6_prefix_length,
                'ipv6_gateway': ipv6_gateway,
                'speed': v['speed'],
                'phy_mode': v['medium'],
                'auto_detect_instrumentation_type': 'floating'
        }

        opts.update(**kw)

        res = self._conf_interface(port, 'config', **opts)
        interface = res.split()[-1]
        self._set_handle(name, name, interface, 'device')


    def create_dynamic_host_on_port(self, name, port, src_mac_addr, **kw):

        self._check_name(name)
        self._check_port(port)

        v = self.port_list[port.ref]

        opts = {'src_mac_addr': src_mac_addr,
                'arp_send_req': 1,
                'speed': v['speed'],
                'phy_mode': v['medium'],
                'auto_detect_instrumentation_type': 'floating'
        }

        opts.update(**kw)
        res = self._conf_interface(port, 'config', **opts)
        interface = res.split()[-1]
        res = self.tcl.command("CiHLT::interfaceEnableDHCPv4 %s" % (interface))[2]
        if not self.verify(res) == self.SUCCESS :
            #raise ValueError('Failed to create dynamic host.')
            raise IXIAConfigureHostError

        #wait for DHCP resolve
        time.sleep(4)
        res = self.tcl.command("CiHLT::interfaceGetDHCPV4IpAddress %s" % ( interface))[2]

        if not self.verify(res) == self.SUCCESS:
            self.logger.debug('Have not get the DHCP ip yet')
        self._set_handle(name, name, interface, 'device')

    def create_dynamic_hostv6_on_port(self, name, port, src_mac_addr, **kw):

        self._check_name(name)
        self._check_port(port)

        v = self.port_list[port.ref]

        opts = {'src_mac_addr': src_mac_addr,
                'arp_send_req': 1,
                'speed': v['speed'],
                'phy_mode': v['medium'],
                'auto_detect_instrumentation_type': 'floating'
        }

        opts.update(**kw)
        res = self._conf_interface(port, 'config', **opts)
        interface = res.split()[-1]
        res = self.tcl.command("CiHLT::interfaceEnableDHCPv6 %s" % (interface))[2]
        if not self.verify(res) == self.SUCCESS:
            raise ValueError('Failed to create dynamic host.')

        #wait for DHCP resolve
        time.sleep(4)
        res = self.tcl.command("CiHLT::interfaceGetDHCPV6IpAddress %s" % (interface))[2]

        if not self.verify(res) == self.SUCCESS:
            self.logger.debug('Have not get the DHCP ip yet')
        self._set_handle(name, name, interface, 'device')

    def get_host_dynamic_discovered_info(self, name):

        self._check_name(name, has_attr=True)

        valid_fields = ['gateway', 'ipv4Address', 'ipv4Mask',
                        'isDhcpV4LearnedInfoRefreshed',
                        'leaseDuration', 'protocolInterface',
                        'tlv']

        values = {}
        interface = getattr(self, name).handle

        for field in valid_fields:
            res = self.tcl.command("CiHLT::interfaceGetDHCPV4DiscoveredInfo %s %s" % (interface, field))[2]
            values[field] = res.split('\r\n')[-2].replace('\r','')
        return values

    def get_hostv6_dynamic_discovered_info(self, name):

        self._check_name(name, has_attr=True)

        valid_fields = ['iaRebindTime', 'iaRenewTime',
                        'ipv6Address', 'isDhcpV6LearnedInfoRefreshed',
                        'protocolInterface', 'tlvs']

        values = {}
        interface = getattr(self, name).handle

        for field in valid_fields:
            res = self.tcl.command("CiHLT::interfaceGetDHCPV6DiscoveredInfo %s %s" % (interface, field))[2]
            values[field] = res.split('\r\n')[-2].replace('\r', '')
        return values

    def host_send_ping(self, name, dst_ip):

        self._check_name(name, has_attr=True)

        interface = getattr(self, name).handle

        res = self.tcl.command("CiHLT::interfaceSendPing  %s %s " %(interface, dst_ip))[2]
        if self.verify(res) == self.SUCCESS:
            res = res.replace('\r\n','').replace('\r','')
            return re.search('{(.*)}',res).group(1).split(',')[1]
        else:
            raise ValueError('Faild to send Ping Command')

    def host_send_arp(self, name):

        self._check_name(name, has_attr=True)
        interface = getattr(self, name).handle
        res = self.tcl.command("CiHLT::interfaceSendArp %s" % (interface))[2]
        print res
        if not self.verify(res) == self.SUCCESS:
            raise ValueError('Failed to send Arp Command')

    def host_send_ns(self, name):
        self._check_name(name)
        interface = getattr(self, name).handle

        res = self.tcl.command("CiHLT::interfaceSendNs %s" % (interface))[2]
        print res

        if not self.verify(res) == self.SUCCESS:
            raise ValueError('Failed to send ns command')

    def host_send_rs(self, name):

        self._check_name(name)
        interface = getattr(self, name).handle
        res = self.tcl.command("CiHLT::interfaceSendRs %s" % (interface))[2]
        print res

        if not self.verify(res) == self.SUCCESS:
            raise ValueError('Failed to send rs command')

    @cafe.teststep('modify specified interface!')
    # def modify_host(self, name, service, attr, value, **kwargs):

    #     self._check_name(name)
    #     interface = getattr(self, name).handle
    #     res = self.tcl.command("CiHLT::interfaceModify %s %s %s %s"%
    #                            (interface, service , attr, value))[2]
    #     if not self.verify(res) == self.SUCCESS:
    #         raise ValueError('Failed to modify interface attribute')

    def modify_host( self, name, port, **kw):

        self._check_name(name)
        self._check_port(port)
        handle = getattr(self, name).handle
        opts = {}
        opts.update(kw)
        s = self.dict2str(opts)
        res = self.tcl.command("CiHLT::interfaceModify %s %s {%s}" % (handle,
                                                                      port, s))[2]

        if not self.verify(res) == self.SUCCESS:
            raise ValueError('Failed to modify interface')

    @cafe.teststep('close STC session!')
    def close_session(self):
        '''
        close ixia session and release all ixia resources.

        Returns:

        '''

        #TODO: NOT IMPLEMENTED YET.

        # clean handles
        # relase ports

        raise NotImplementedError('Not implemented yet!')

    def _pass(self, title):
        cafe.Checkpoint().pass_test(title)

    def _fail(self, title):
        cafe.Checkpoint().fail(title)

    def _get_stats_by_key(self, key):
        ret = {}
        for k, v in self.stats.items():
            m = re.search(key, k)
            if m:
                ret[k] = v
        return ret

    def clear_traffic_stats(self):
        self.stats = {}
        ports = self.get_handles("port")
        for p in ports:
            self.control_traffic(p.value, "clear_stats")

    def _get_traffic_on_port(self, port, key, mode="traffic_item"):

        port_handles = self.get_handles("port")
        for p in port_handles:
            if p == port:
                opt = {}
                opt["port_handle"] = p.handle
                self.traffic_stats(mode, **opt)
                self.get_stats()
                self._update_app_result(self.stats)
                return self._get_stats_by_key(key)
        else:
            raise ValueError('port handle not found!')
        #return False

    def _get_stream_stats_by_key(self, key, mode="stream", **kwargs):
        opt = {}
        opt.update(**kwargs)
        self.traffic_stats(mode, **opt)
        self.get_stats()
        self._update_app_result(self.stats)
        return self.get_stats_by_key_regex(key)

    def _create_untag_traffic(self, name, tx_port, rx_port, **kwargs):

        self._check_name(name)
        option = {}
        option["name"] = str(name)
        option["traffic_generator"] = "ixnetwork_540"
        option["emulation_src_handle"] = str(tx_port)
        option["emulation_dst_handle"] = str(rx_port)
        option["circuit_type"] = "raw"
        option["track_by"] = "trackingenabled0"
        option['frame_size'] = '128'
        option.update(**kwargs)
        return self._config_traffic("create", **option)

    def _create_single_tag_traffic(self, name, tx_port, rx_port, vlan_id, vlan_user_priority, **kwargs):

        self._check_name(name)
        option = {}
        option["name"] = str(name)
        option['l2_encap'] = 'ethernet_ii_vlan'
        option["vlan_id"] = str(vlan_id)
        option["vlan_user_priority"] = str(vlan_user_priority)
        option["traffic_generator"] = "ixnetwork_540"
        option["emulation_src_handle"] = str(tx_port)
        option["emulation_dst_handle"] = str(rx_port)
        option["circuit_type"] = "raw"
        option["track_by"] = "trackingenabled0"
        option['frame_size'] = '128'
        option["vlan"] = "enable"
        option.update(**kwargs)
        return self._config_traffic("create", **option)

    def _create_double_tag_traffic(self, name, tx_port, rx_port, vlan_id, vlan_user_priority, **kwargs):

        option = {}
        option["name"] = str(name)
        option['l2_encap'] = 'ethernet_ii_vlan'
        option["vlan_id"] = vlan_id
        option["vlan_user_priority"] = vlan_user_priority
        option["traffic_generator"] = "ixnetwork_540"
        option["emulation_src_handle"] = str(tx_port)
        option["emulation_dst_handle"] = str(rx_port)
        option["circuit_type"] = "raw"
        option["track_by"] = "trackingenabled0"
        option["vlan"] = "enable"
        option['frame_size'] ='128'
        option.update(**kwargs)
        return self._config_traffic("create", **option)

    def _traffic_enable_all(self):
        streams = self.get_handles("stream")
        opt = {}
        for i in streams:
            opt["stream_id"] = i.handle
            self._config_traffic("enable", **opt)

    def _traffic_disable_all(self):
        streams = self.get_handles("stream")
        opt = {}
        for i in streams:
            opt["stream_id"] = i.handle
            self._config_traffic("disable", **opt)

    def _traffic_enable(self, name):

        self._check_name(name)
        streams = self.get_handles("stream")
        opt = {}
        for i in streams:
            # print type(i)
            # print i.handle
            # print i.vlaue
            if name == i.value:
                opt["stream_id"] = i.handle
                return self._config_traffic("enable", **opt)
        else:
            raise ValueError('%s is not found' % name)
        #return False

    def _traffic_disable(self, name):

        self._check_name(name)
        streams = self.get_handles("stream")
        opt = {}
        for i in streams:
            if name == i.value:
                opt["stream_id"] = i.handle
                return self._config_traffic("disable", **opt)
        else:
            raise ValueError('%s is not found' % name)
        #return False

    def _verify_traffic_no_loss(self):

        # ports = self.get_port_handle("port")
        # self.logger.debug("port handles " + str(ports))
        self.stats = {}
        self.traffic_stats("traffic_item")
        self.get_stats()
        self._update_app_result(self.stats)
        print "#"*80
        print self.stats
        print "#"*80
        values = self.get_stats_by_key_regex(r"rx\.loss_pkts.sum")
        for k, v in values.items():
            self.logger.debug("verify_no_traffic_loss:" + k + ":" + str(v))
            if float(v) != 0:
                self._fail("session(%s): verify no traffic loss. failed (%s=%s)" % (self.name, k, str(v)))
                return False
            elif float(v) == 0:
                self._pass("session(%s): verify no traffic loss." % self.name)
                return True
        self._fail("no dropped pkgs count found!")
        return False

    def verify_traffic_loss_on_port_within_expect_count(self, port, count):
        '''
        Purpose:
            verify the traffic loss within expect count(exclusive)

        Args:
            count: the max loss count permitted , exclusive

        Returns:
            bool: True traffic lost within "count"; False otherwise
        '''

        p = []
        ports = self.get_handles("port")
        for i in ports:
            print type(i)
            p.append(i.value)
        if str(port) not in p or not isinstance(count, int):
            raise Exception("Your input is invalid!")
        loss = self._get_traffic_on_port(port, "rx\.loss_pkts.sum").values()[0]
        if loss >= count:
            self._fail("session(%s): verify no traffic loss. failed (loss = %s)" % (self.name, loss))
            return False
        else:
            self._pass("session(%s): verify traffic loss pass." % self.name)
            return True

    def _verify_traffic_loss_within(self, percent=0.001):

        if not isinstance(percent, (int, float, unicode)):
            raise TypeError('Invalid input, %s should be int or float' % percent)
        self.stats = {}
        self.traffic_stats("traffic_item")
        self.get_stats()
        self._update_app_result(self.stats)

        print "====>", self.stats
        values = self.get_stats_by_key_regex(r"rx\.loss_pkts.sum")
        total = self.get_stats_by_key_regex(r"rx\.total_pkts.sum").values()[0]
        for k, v in values.items():
            self.logger.debug("verify_no_traffic_loss:" + k + ":" + str(v))
            if float(total) == 0:
                raise RuntimeError("Traffic stats error, total_pkts.sum = 0")
            loss_rate = abs(float(v))/float(total)
            if float(loss_rate) > float(str(percent)):
                self._fail("session(%s): verify no traffic loss. failed (%s=%s)" % (self.name, k, str(v)))
                return False
            else:
                self._pass("session(%s): verify no traffic loss." % self.name)
                return True
        self._fail("no dropped pkgs count found!")
        return False

    def _verify_traffic_no_loss_on_port(self, port):

        p = []
        ports = self.get_handles("port")
        for i in ports:
            print type(i)
            p.append(i.value)
        if str(port) not in p:
            raise ValueError("Port %s not found!" % p)
        loss = self._get_traffic_on_port(port, "rx\.loss_pkts.sum").values()[0]
        if float(loss) != 0:
            self._fail("session(%s): verify no traffic loss. failed (loss = %s)" % (self.name, loss))
            return False
        elif float(loss) == 0:
            self._pass("session(%s): verify no traffic loss." % self.name)
            return True

    def _verify_traffic_loss_on_port_within(self, port, percent):

        p = []
        ports = self.get_handles("port")
        for i in ports:
            print type(i)
            p.append(i.value)
        if str(port) not in p or not isinstance(percent, (int, float, unicode)):
            raise Exception("Your input is invalid!")
        loss = self._get_traffic_on_port(port, "rx\.loss_pkts.sum").values()[0]
        total = self.get_stats_by_key_regex(r"rx\.total_pkts.sum").values()[0]
        if total == 0:
            raise RuntimeError("Traffic stats error, total_pkts.sum = 0")
        num = abs(float(loss)) / total
        # print num
        if float(num) > float(str(percent)):
            self._fail("session(%s): verify no traffic loss. failed (loss = %s)" % (self.name, loss))
            return False
        else:
            self._pass("session(%s): verify no traffic loss." % self.name)
            return True

    def _verify_traffic_no_loss_on_stream(self, stream):

        try:
            strs = self.get_handles('stream')
            ports = self.get_handles('port')
            for s in strs:
                if s.value == stream:
                    opt = {"streams": s.handle}
                    sn = s.handle.replace("-", "_")
                    loss = self._get_stream_stats_by_key("%s.rx.loss_pkts" % sn, **opt)
                    for k, v in loss.items():
                        print loss
                        print k, v
                        if float(v) != 0:
                            self._fail("session(%s): verify no traffic loss on stream %s. failed (%s=%s)" % (self.name, stream, k, str(v)))
                            return False
                        self._pass("session(%s): verify no traffic loss." % self.name)
                        return True
            else:
                raise RuntimeError('Stream name not found!')
        except RuntimeError:
            self.logErr("")

    def _verify_traffic_loss_on_stream_within(self, stream, percent):

        if not isinstance(percent, (int, float, unicode)):
            raise TypeError('invalid input %s!' % percent)
        try:
            strs = self.get_handles('stream')
            for s in strs:
                if s.value == stream:
                    opt = {"streams": s.handle}
                    sn = s.handle.replace("-", "_")
                    # loss = self._get_stream_stats_by_key("%s.rx.loss_pkts" % sn, **opt).values()[0]
                    # total = self._get_stream_stats_by_key("%s.rx.total_pkts" % sn, **opt).values()[0]
                    # if total == 0:
                    #     raise RuntimeError('Traffic stats error, total_pkts.sum = 0')
                    # res = abs(float(loss)) / total
                    loss = self._get_stream_stats_by_key("%s.rx.loss_percent" % sn, **opt).values()[0]
                    if loss > percent:
                        self._fail('session(%s): verify no traffic loss on stream %s. failed (loss=%s)' % (self.name, stream, loss))
                        return False
                    elif float(loss) <= float(str(percent)):
                        self._pass('session(%s): verify no traffic loss.' % self.name)
                        return True
            else:
                raise RuntimeError('Stream name not found!')
        except:
            self.logErr("Unexpected exception captured!")

    def _get_traffic_stats_cnt(self, key):

        summ =[]
        strs = self.get_handles('stream')
        for s in strs:
            opt = {"streams": s.handle}
            summ.extend(self._get_stream_stats_by_key(key, mode="traffic_item", **opt).values())
        # print summ
        return summ

    def _verify_stats_eq(self, key, expected_value):

        if not isinstance(expected_value, (int, float, unicode)):
            raise TypeError("Type error: value type is incorrect!")
        res = self._get_traffic_stats_cnt(key)
        if len(res) == 0:
            raise RuntimeError("Key %s does NOT exist!" % key)
        for i in res:
            if float(i) != float(str(expected_value)):
                self._fail("traffic stats: %s is %s, NOT same as %s" % (key, i, expected_value))
                return False
            else:
                self._pass('traffic stats: %s is same as expected %s' % (key, expected_value))
                return True
        return False

    def _verify_stats_less_than(self, key, value):

        if not isinstance(value, (int, float, unicode)):
            raise TypeError("Type error: value type is incorrect!")
        res = self._get_traffic_stats_cnt(key)
        if len(res) == 0:
            raise RuntimeError("Key %s does NOT exist!" % key)
        for i in res:
            if float(i) >= float(str(value)):
                self._fail("traffic stats: %s is %s, NOT same as %s" % (key, i, value))
                return False
            else:
                self._pass('traffic stats: %s is same as expected %s' % (key, value))
                return True
        return False

    def _verify_stats_greater_than(self, key, value):

        if not isinstance(value, (int, float, unicode)):
            raise TypeError("Type error: value type is incorrect!")
        res = self._get_traffic_stats_cnt(key)
        if len(res) == 0:
            raise RuntimeError("Key %s does NOT exist!" % key)
        for i in res:
            if float(i) <= float(str(value)):
                self._fail("traffic stats: %s is %s, NOT greater than %s" % (key, i, value))
                return False
            else:
                self._pass('traffic stats: %s is greater than expected %s' % (key, value))
                return True
        return False

    @cafe.teststep('verify traffic stats no packet loss!')
    def verify_traffic_no_loss(self):
        '''
        Purpose:
            Verify no data traffic lost for all test equipment's ports

        Returns:
            bool: True no traffic lost; False otherwise
        '''
        return self._verify_traffic_no_loss()

    @cafe.teststep('verify traffic stats packet loss within expected range!')
    def verify_traffic_loss_within(self, percent=0.001):
        '''
        Purpose:
            Verify data traffic lost for test equipment's ports is within "percentage" tolerance

        Args:
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True traffic lost within "percent"; False otherwise
        '''
        return self._verify_traffic_loss_within(percent)

    @cafe.teststep('verify traffic stats and not packet loss on port')
    def verify_traffic_no_loss_on_port(self, port):
        '''
        Purpose:
            Verify no data traffic lost for test equipment's port
        Args:
            port

        Returns:
            bool: True if No traffic lost; False otherwise
        '''
        self._check_port(port)
        return self._verify_traffic_no_loss_on_port(port)

    @cafe.teststep('verify traffic stats on port within expected range!')
    def verify_traffic_loss_on_port_within(self, port, percent):
        '''
        Purpose:
            Verify data traffic lost for test equipment's port is within "percentage" tolerance

        Args:
            port
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True traffic lost within "percent"; False otherwise
        '''
        self._check_port(port)
        return self._verify_traffic_loss_on_port_within(port, percent)

    @cafe.teststep('verify traffic loss on stream!')
    def verify_traffic_no_loss_on_stream(self, stream):
        """
        Purpose:
            Verify no data traffic lost for test equipment's data stream object
        Args:
            stream: data stream name reference
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True if No traffic lost; False otherwise
        """

        self._check_stream(stream)
        return self._verify_traffic_no_loss_on_stream(stream)

    @cafe.teststep('verify traffic loss on stream!')
    def verify_traffic_loss_on_stream_within(self, stream, percent):
        '''
        Purpose:
            Verify data traffic lost for test equipment's data stream object is within "percentage" tolerance

        Args:
            stream: data stream name reference
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True traffic lost within "percent"; False otherwise
        '''

        self._check_stream(stream)
        return self._verify_traffic_loss_on_stream_within(stream, percent)

    @cafe.teststep('verify traffic stats equal!')
    def verify_stats_eq(self, key, value):
        '''
        Purpose:
            verify the statistic figure referenced by key is equal to the value
            The statistic figures are cached whenever a *_stat API is called.
            The comparison result will log into result database
        Args:
            key: key of the statistic figure
            value: value fo comparison

        Returns:
            bool: True if value to is equal to statistic figure referenced by key; False otherwise
        '''
        return self._verify_stats_eq(key, value)

    @cafe.teststep('verify traffic stats less than!')
    def verify_stats_less_than(self, key, value):
        '''
        Purpose:
            verify the statistic figure referenced by key is less than the value
            The statistic figures are cached whenever a *_stat API is called.
            The comparison result will log into result database
        Args:
            key: key of the statistic figure
            value: value fo comparison

        Returns:
            bool: True if statistic figure referenced by key is less than value; False otherwise
        '''
        return self._verify_stats_less_than(key, value)

    @cafe.teststep('verify traffic stats greater than!')
    def verify_stats_greater_than(self, key, value):
        '''
        Purpose:
            verify the statistic figure referenced by key is larger than the value
            The statistic figures are cached whenever a *_stat API is called.
            The comparison result will log into result database
        Args:
            key: key of the statistic figure
            value: value fo comparison

        Returns:
            bool: True if statistic figure referenced by key is larger than value; False otherwise
        '''
        return self._verify_stats_greater_than(key, value)

    @cafe.teststep('traffic configure untag!')
    def traffic_config_untag(self, name, tx_port, rx_port, **kwargs):

        '''
        Purpose:
            helper function to create an untag traffic.
            layer 2 default to ethernet
            layer 3 default to ipv4

        Args:
            name: data stream name reference
            port: traffic generator port
            src_mac: source mac address
            dst_mac: destination mac address
            src_ip: source ipv4 address
            dst_ip: destination ipv4 address
            framesize: packet length
            rate_percent: the transmit speed w.r.t to the max capacity of the port
            length_mode: The packet size length mode. default is fixed.
            transmit_mode: default is "continuous"

        Raises:
            TrafficConfigError - error in config the traffic stream
        '''
        self._check_port(tx_port)
        self._check_port(rx_port)
        self._check_name(name)
        tx = self.get_port_handle(tx_port)
        rx = self.get_port_handle(rx_port)

        h = self._create_untag_traffic(name=name, tx_port=tx, rx_port=rx,  **kwargs)

        self._set_handle(name, name, h, "stream")
        return h

    @cafe.teststep('traffic configure bound untag')
    def bound_traffic_config_untag(self, name, port, t_handle, f_handle,
                                   **kw):

        self._check_port(port)
        self._check_name(name)

        opts = {'name': str(name),
                'traffic_generator': 'ixnetwork_540',
                'emulation_src_handle': f_handle,
                'emulation_dst_handle': t_handle,
                'frame_size': '128',
                'track_by': 'traffic_item',
        }
        opts.update(**kw)

        h = self._config_traffic("create", **opts)
        self._set_handle(name, name, h, 'stream')

    @cafe.teststep('traffic configure single tag!')
    def traffic_config_single_tag(self, name, tx_port, rx_port, vlan_id=100, vlan_user_priority=7, **kwargs):

        '''
        Purpose:
            helper function to create an single tag traffic. layer 2 default to ethernet
            layer 3 default to ipv4
        Args:
            name: data stream name reference
            port: traffic generator port
            src_mac: source mac address
            dst_mac: destination mac address
            src_ip: source ipv4 address
            dst_ip: destination ipv4 address
            vlan_id: default to 100
            framesize: packet length
            rate_percent: the transmit speed w.r.t to the max capacity of the port
            length_mode: The packet size length mode. default is fixed.
            transmit_mode: default is "continuous"

        Raises:
            TrafficConfigError - error in config the traffic stream
        '''

        self._check_port(tx_port)
        self._check_port(rx_port)
        self._check_name(name)
        tx = self.get_port_handle(tx_port)
        rx = self.get_port_handle(rx_port)

        h = self._create_single_tag_traffic(name=name, tx_port=tx, rx_port=rx,
                                            vlan_id=vlan_id, vlan_user_priority=vlan_user_priority,
                                            **kwargs)

        self._set_handle(name, name, h, "stream")
        return h

    @cafe.teststep('traffic configure bound single tag')
    def bound_traffic_config_single_tag(self, name, port, t_handle, f_handle,
                                        vlan_id, vlan_user_priority,
                                        **kw):

        self._check_port(port)
        self._check_name(name)

        opts = {'name':str(name),
                'traffic_generator':'ixnetwork_540',
                'emulation_src_handle': f_handle,
                'emulation_dst_handle': t_handle,
                'l2_encap' : 'ethernet_ii_vlan',
                'vlan_id': str(vlan_id),
                'vlan_user_priority': str(vlan_user_priority),
                'track_by':'traffic_item',
                'frame_size':'128',
                'vlan':'enable'
        }
        opts.update(**kw)

        h = self._config_traffic("create", **opts)
        self._set_handle(name, name, h, 'stream')


    @cafe.teststep('traffic configure double tag!')
    def traffic_config_double_tag(self, name, tx_port, rx_port,
                                  vlan_id=[100, 10], vlan_user_priority=[1, 5],
                                  **kwargs):

        '''
        Purpose:
            helper function to create an double tag traffic.
            layer 2 default to ethernet, layer 3 default to ipv4

        Args:
            name: data stream name reference
            port: traffic generator port
            src_mac: source mac address
            dst_mac: destination mac address
            src_ip: source ipv4 address
            dst_ip: destination ipv4 address
            cvlan_id: default to 100
            svlan_id: default to 100
            framesize: packet length
            rate_percent: the transmit speed w.r.t to the max capacity of the port
            length_mode: The packet size length mode. default is fixed.
            transmit_mode: default is "continuous"

        Raises:
            TrafficConfigError - error in config the traffic stream
        '''
        if not isinstance(vlan_id, list) or not isinstance(vlan_user_priority, list):
            raise IXIASessionException('vlan and vlan user priority should be list format in double tag func.')

        self._check_port(tx_port)
        self._check_port(rx_port)
        self._check_name(name)

        tx = self.get_port_handle(tx_port)
        rx = self.get_port_handle(rx_port)

        h = self._create_double_tag_traffic(name=name, tx_port=tx, rx_port=rx, vlan_id=vlan_id,
                                            vlan_user_priority=vlan_user_priority, **kwargs)
        self._set_handle(name, name, h, "stream")
        return h

    @cafe.teststep('traffic configure bound double tag')
    def bound_traffic_config_double_tag(self, name, port, t_handle, f_handle,
                                        vlan_id, vlan_user_priority,
                                        **kw):

        self._check_port(port)
        self._check_name(name)

        opts = {'name':str(name),
                'traffic_generator':'ixnetwork_540',
                'emulation_src_handle': f_handle,
                'emulation_dst_handle': t_handle,
                'l2_encap' : 'ethernet_ii_vlan',
                'vlan_id': vlan_id,
                'vlan_user_priority': vlan_user_priority,
                'track_by':'traffic_item',
                'frame_size':'128',
                'vlan':'enable'
        }
        opts.update(**kw)

        h = self._config_traffic("create", **opts)
        self._set_handle(name, name, h, 'stream')

    def traffic_modify(self, name, **kw):
        self._check_name(name)
        stream_id = getattr(self, name).handle
        opts = {'traffic_generator': 'ixnetwork_540',
                'stream_id': stream_id}
        opts.update(**kw)
        mode = 'modify' if 'mode' not in opts else opts['mode']
        if 'mode' in opts: del opts['mode']
        self._config_traffic(mode, **opts)

    @cafe.teststep('traffic enable all!')
    def traffic_enable_all(self):
        '''
        Purpose:
            to enable all traffic streams in configuration

        '''
        return self._traffic_enable_all()

    @cafe.teststep('traffic disable all!')
    def traffic_disable_all(self):
        '''
        Purpose:
            to disable all traffic streams in configuration

        '''
        return self._traffic_disable_all()

    @cafe.teststep('traffic enable!')
    def traffic_enable(self, name):
        '''
        Purpose:
            to enable traffic stream referenced by "stream" in configuration

        Args:
            stream: name reference of traffic stream
        '''
        self._check_name(name)
        return self._traffic_enable(name)

    @cafe.teststep('traffic disable!')
    def traffic_disable(self, name):
        '''
        Purpose:
            to disable traffic stream referenced by "stream" in configuration

        Args:
            stream: name reference of traffic stream
        '''
        self._check_name(name)
        return self._traffic_disable(name)

    @cafe.teststep("delete traffic stream")
    def traffic_delete(self, stream):
        stream_handle = self._get_handle(stream, "stream")
        opt = {"stream_id" : stream_handle}
        self._config_traffic('remove', **opt)
        self._del_handle(stream, "stream")
        return True

    @cafe.teststep("delete all traffic stream")
    def traffic_delete_all(self):
        self._config_traffic('reset')
        stream_handles = self.get_handles('stream')
        for handle in stream_handles:
            delattr(self, handle.ref)
            self.handles.remove(handle)
        return True

    def _create_dhcp_client(self, name, port, **kwargs):

        self._check_name(name)
        opt = {}
        opt.update(**kwargs)
        mode = 'create'
        self.h = self.conf_dhcp_client(port, mode, **opt)
        return self.h

    def _create_dhcp_client_group(self, name, handle, **kwargs):

        self._check_name(name)
        opt = {}
        opt['mode'] = 'create'
        opt.update(**kwargs)
        h = self.conf_dhcp_client_group(handle, **opt)
        #self._set_handle(name, name, h, 'dhcp_client_group')
        return h

    def delete_dhcp_client_group(self, name):

        self._check_name(name)
        handles = filter(lambda x: x.ref == name, self.handles)

        if len(handles) != 1:
            raise ValueError('handle: %s not found' % name)
        res = self.tcl.command("CiHLT::delete_dhcp_client -group_handle %s" % handles[0].handle)[2]
        if self.verify(res) != self.SUCCESS:
            raise ValueError('Fail to delete dhcp client group')
        self.handles.remove(handles[0])
        delattr(self, name)

    def delete_dhcp_client(self, name):
        self._check_name(name)
        handles = filter(lambda x: x.ref == name, self.handles)
        if len(handles) != 1:
            raise ValueError('handle: %s not found' % name)
        res = self.tcl.command("CiHLT::delete_dhcp_client -port_handle %s" % handles[0].handle)[2]
        if self.verify(res) != self.SUCCESS:
            raise ValueError('Failed to delete dhcp client')
        self.handles.remove(handles[0])
        delattr(self, name)

    def _create_dhcp_server(self, name, port, **kwargs ):

        self._check_name(name)
        opt = {}
        opt.update(**kwargs)
        return self.conf_dhcp_server(port, mode='create', **opt)

    def _delete_dhcp_server(self):
        pass

    def _get_dhcp_client_stats(self, port, key, mode, **kwargs):

        opt = {}
        opt.update(**kwargs)

        self._dhcp_client_stats(port, mode, **opt)
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    def _get_dhcp_client_stats_by_name(self, name, key, mode, **kwargs):

        opt = {}
        opt.update(**kwargs)
        h = self.get_handles('dhcp_client_group')
        for i in h:
            if i.value == name:
                self._dhcp_client_stats_by_handle(i.handle, mode, **opt)
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    def _get_dhcp_server_stats(self, port, key, mode, **kwargs):

        opt = {}
        opt.update(**kwargs)

        self._dhcp_server_stats(port, mode, **opt)
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    def _get_dhcp_server_stats_by_name(self, name, key, mode, **kwargs):

        opt = {}
        opt.update(**kwargs)
        h = self.get_handles('dhcp_server')
        for i in h:
            if i.value == name:
                self._dhcp_server_stats_by_handle(i.handle, mode, **opt)
        self.get_stats()
        return self.get_stats_by_key_regex(key)


    @cafe.teststep('create dhco client!')
    def create_dhcp_client(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        ports = self.get_handles('port')
        p = []
        map(lambda x: p.append(x.value), [y for y in ports])
        if port.value not in p:
            raise ValueError('port %s not found!' % port)
        else:
            opt = {}
            opt['lease_time'] = '300'
            opt['version'] = 'ixnetwork'
            opt['reset'] = ""
            opt.update(**kwargs)
            self.h =  self._create_dhcp_client(name=name, port=port, **opt)
            return self._set_handle(name, name, self.h, 'dhcp_client')

        #self._set_handle(name, name, h, 'dhcp_client')

    @cafe.teststep('create dhco client v6!')
    def create_dhcp_client_v6(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        ports = self.get_handles('port')
        p = []
        map(lambda x: p.append(x.value), [y for y in ports])
        if port.value not in p:
            raise ValueError('port %s not found!' % port)
        else:
            opt = {}
            opt['dhcp6_echo_ia_info'] = '1'
            opt['dhcp6_req_max_rt'] = '30'
            opt['dhcp6_req_timeout'] = '1'
            opt['dhcp6_rel_timeout'] = '1'
            opt['dhcp6_ren_max_rt'] = '600'
            opt['dhcp6_ren_timeout'] = '10'
            opt['outstanding_releases_count'] = '500'
            opt['dhcp6_req_timeout'] = '1'
            opt['dhcp6_sol_max_rc'] = '3'
            opt['dhcp6_reb_max_rt'] = '600'
            opt['dhcp6_sol_timeout'] = '4'
            opt['dhcp6_rel_max_rc'] = '5'
            opt['msg_timeout_factor'] = '1'
            #opt[''] = ''
            opt['lease_time'] = '300'
            opt['version'] = 'ixnetwork'
            opt['reset'] = ""
            opt.update(**kwargs)
            self.h = self._create_dhcp_client(name=name, port=port, **opt)
            return self._set_handle(name, name, self.h, 'dhcp_client')

    @cafe.teststep('create dhcp client group!')
    def create_dhcp_client_group(self, name, dhcp_client_name, **kwargs):

        self._check_name(name)
        self._check_name(dhcp_client_name)
        hs = self.get_handles('dhcp_client')
        for i in hs:
            if i.value == dhcp_client_name:
                opt = {}
                opt['mode'] = 'create'
                opt['encap'] = 'ethernet_ii'
                opt['mac_addr'] = '00.00.00.11.11.11'
                opt['num_sessions'] = 1
                opt['version'] = 'ixnetwork'
                opt['mac_addr_step'] = '00.00.00.00.00.01'
                opt.update(**kwargs)
                self.h = self._create_dhcp_client_group(name=name, handle=i.handle, **opt)
                return self._set_handle(name, name, self.h, 'dhcp_client_group', dhcp_client_name)
        else:
            raise ValueError('%s not found!' % dhcp_client_name)

    @cafe.teststep('create dhcp client group v6!')
    def create_dhcp_client_group_v6(self, name, dhcp_client_name, **kwargs):

        self._check_name(name)
        self._check_name(dhcp_client_name)
        hs = self.get_handles('dhcp_client')
        for i in hs:
            if i.value == dhcp_client_name:
                opt = {}
                opt['dhcp_range_ip_type'] = 'ipv6'
                opt['encap'] = 'ethernet_ii'
                opt['mac_addr'] = '00.00.00.11.11.11'
                opt['num_sessions'] = '1'
                opt['version'] = 'ixnetwork'
                opt['mac_addr_step'] = '00.00.00.00.00.01'
                opt.update(**kwargs)
                self.h = self._create_dhcp_client_group(name=name, handle=i.handle, **opt)
                return self._set_handle(name, name, self.h, 'dhcp_client_group', dhcp_client_name)
        else:
            raise ValueError('%s not found!' % dhcp_client_name)

    @cafe.teststep('reset dhcp client!')
    def reset_dhcp_client(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        opt.update(**kwargs)

        handles = filter(lambda x: x.ref == name, self.handles)
        if len(handles) != 1:
            raise  ValueError('%s not found!' % name)
        opt['handle'] = handles[0].handle
        self._reset_dhcp_client(None, **opt)
        self.handles.remove(handles[0])
        delattr(self, name)
        '''
        h = self.get_handles('dhcp_client')
        for i in h:
            if i.value == name:
                opt['handle'] = i.handle
                opt['version'] = 'ixnetwork'
                port = None
                self._reset_dhcp_client(port, **opt)
                self.del_handles()
                return
        else:
            raise ValueError('%s not found!' % name)
        '''

    @cafe.teststep('reset dhcp client v6!')
    def reset_dhcp_client_v6(self, name, **kwargs):
        pass
        # self._check_name(name)
        # opt = {}
        # opt.update(**kwargs)
        # h = self.get_handles('dhcp_client')
        # for i in h:
        #     if i.value == name:
        #         opt['handle'] = i.handle
        #         opt['version'] = 'ixnetwork'
        #         port = None
        #         self._reset_dhcp_client(port, **opt)
        #         self.del_handles()
        #         return
        # else:
        #     raise ValueError('%s not found!' % name)

    @cafe.teststep('reset dhcp group!')
    def reset_dhcp_client_group(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        opt.update(**kwargs)
        handles = filter(lambda x: x.ref == name, self.handles)

        if len(handles) != 1:
            raise ValueError('% handle not found!' % name)

        self._reset_dhcp_client_group(handles[0].handle, **opt)
        self.handles.remove(handles[0])
        delattr(self, name)

        '''
        h = self.get_handles('dhcp_client_group')
        for i in h:
            if i.value == name:
                #opt['handle'] = i.handle
                opt['version'] = 'ixnetwork'
                self._reset_dhcp_client_group(i.handle, **opt)
                self.del_handles()
                return
        else:
            raise ValueError('%s not found!' % name)
        '''

    @cafe.teststep('reset dhcp group v6!')
    def reset_dhcp_client_group_v6(self, name, **kwargs):

        pass

        # self._check_name(name)
        # #self._check_port(port)
        # opt = {}
        # opt.update(**kwargs)
        # h = self.get_handles('dhcp_client_group')
        # for i in h:
        #     if i.value == name:
        #         #opt['handle'] = i.handle
        #         opt['version'] = 'ixnetwork'
        #         self._reset_dhcp_client_group(i.handle, **opt)
        #         self.del_handles()
        #         return
        # else:
        #     raise ValueError('%s not found!' % name)

    @cafe.teststep('create dhcp server!')
    def create_dhcp_server(self, name, port, **kwargs):

        self._check_name(name)
        self._check_port(port)
        opt = {'ip_version': 4}
        opt.update(**kwargs)
        h = self._create_dhcp_server(name=name, port=port,  **opt)
        self._set_handle(name, name, h, 'dhcp_server')


    @cafe.teststep('create dhcp server!')
    def create_dhcp_server_v6(self, name, port, **kwargs):

        self._check_name(name)
        self._check_port(port)
        opt = {}
        opt['ip_version'] = '6'
        opt['ipaddress_pool'] = 'A0A::102'
        opt['ip_prefix_length'] = '112'
        opt['ipaddress_count'] = '15'
        opt['dhcp6_ia_type'] = 'iana'
        opt['ip_address'] = 'A0A::002'
        opt['ipv6_gateway'] = 'A0A::001'
        opt['encapsulation'] = 'ETHERNET_II'
        opt.update(kwargs)
        h = self._create_dhcp_server(name=name, port=port,  **opt)
        self._set_handle(name, name, h, 'dhcp_server')


    @cafe.teststep('reset dhcp server!')
    def reset_dhcp_server(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        opt.update(**kwargs)

        handle = filter(lambda x: x.ref == name, self.handles)
        if len(handle) != 1:
            raise ValueError('% handle not found!' % name)
        opt['handle'] = handle[0].handle
        self._reset_dhcp_server(**opt)
        self.handles.remove(handle[0])
        delattr(self, name)

    @cafe.teststep('reset dhcp server v6!')
    def reset_dhcp_server_v6(self, name, **kwargs):

        pass

        # self._check_name(name)
        # opt = {}
        # opt.update(**kwargs)
        # h = self.get_handles('dhcp_server')
        # for i in h:
        #     if i.value == name:
        #         opt['handle'] = i.handle
        #         #opt['version'] = 'ixnetwork'
        #         opt.update(**kwargs)
        #         self._reset_dhcp_server(**opt)
        #         self.del_handles()
        #         return
        # else:
        #     raise ValueError('%s not found!' % name)

    @cafe.teststep('modify dhcp client!')
    def modify_dhcp_client(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        opt.update(**kwargs)
        h = self.get_handles('dhcp_client')
        for i in h:
            if i.value == name:
                opt['handle'] = i.handle
                opt['version'] = 'ixnetwork'
                return self._modify_dhcp_client(**opt)
        else:
            raise ValueError('%s not found!' % name)

    @cafe.teststep('modify dhcp client v6!')
    def modify_dhcp_client_v6(self, name, **kwargs):

        pass

        # self._check_name(name)
        # opt = {}
        # opt.update(**kwargs)
        # h = self.get_handles('dhcp_client')
        # for i in h:
        #     if i.value == name:
        #         opt['handle'] = i.handle
        #         opt['version'] = 'ixnetwork'
        #         return self._modify_dhcp_client(**opt)
        # else:
        #     raise ValueError('%s not found!' % name)

    @cafe.teststep('modify dhcp client group!')
    def modify_dhcp_client_group(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        opt['version'] = 'ixnetwork'
        opt.update(**kwargs)
        g = self.get_handles('dhcp_client_group')
        for i in g:
            if i.value == name:
                return self._modify_dhcp_client_group(i.handle, **opt)
        else:
            raise ValueError('%s not found!' % name)

    @cafe.teststep('modify dhcp client group v6!')
    def modify_dhcp_client_group_v6(self, name, **kwargs):

        pass

        # self._check_name(name)
        # opt = {}
        # opt['version'] = 'ixnetwork'
        # opt.update(**kwargs)
        # g = self.get_handles('dhcp_client_group')
        # for i in g:
        #     if i.value == name:
        #         return self._modify_dhcp_client_group(i.handle, **opt)
        # else:
        #     raise ValueError('%s not found!' % name)

    @cafe.teststep('modify dhcp server!')
    def modify_dhcp_server(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        h = self.get_handles('dhcp_server')
        for i in h:
            if i.value == name:
                opt['handle'] = i.handle
                opt['ip_version'] = 4
                opt.update(**kwargs)
                return self._modify_dhcp_server(**opt)
        else:
            raise ValueError('%s not found!' % name)

    @cafe.teststep('modify dhcp server v6!')
    def modify_dhcp_server_v6(self, name, **kwargs):

        self._check_name(name)
        opt = {}
        h = self.get_handles('dhcp_server_v6')
        for i in h:
            if i.value == name:
                opt['handle'] = i.handle
                opt['ip_version'] = 4
                opt.update(**kwargs)
                return self._modify_dhcp_server(**opt)
        else:
            raise ValueError('%s not found!' % name)

    @cafe.teststep('control dhcp client!')
    def control_dhcp_client(self, port, action, **kwargs):

        self._check_port(port)
        if action not in ['bind', 'release', 'renew', 'abort', 'abort_async']:
            raise KeyError('Invalid value for action, allowed value should be bind, release, renew, abort, abort_async')
        ports = self.get_handles('port')
        p = []
        map(lambda x: p.append(x.value), [y for y in ports])
        if port.value not in p:
            raise KeyError('port does not exist!')
        # print port
        return self._control_dhcp_client(port, action=action, **kwargs)


    @cafe.teststep('control dhcp client by name!')
    def control_dhcp_client_by_name(self, name, action, **kwargs):

        self._check_name(name)
        if action not in ['bind', 'release', 'renew', 'abort', 'abort_async']:
            raise KeyError('Invalid value for action, allowed value should be bind, release, renew, abort, abort_async')
        ch = self.get_handles('dhcp_client_group')

        for i in ch:
            if i.value == name:
                return self._control_dhcp_client_by_name(i.handle, action=action, **kwargs)

    @cafe.teststep('control dhcp server!')
    def control_dhcp_server(self, port, action, **kwargs):

        self._check_port(port)
        if action not in ['abort', 'abort_async', 'renew', 'reset', 'collect']:
            raise KeyError('Invalid value for action, allowed value should be abort abort_async renew reset collect')
        ports = self.get_handles('port')
        p = []
        map(lambda x: p.append(x.value), [y for y in ports])
        if port.value not in p:
            raise ValueError('port %s does not exist!' % port)
        return self._control_dhcp_server(port, action=action, **kwargs)

    @cafe.teststep('control dhcp server by name!')
    def control_dhcp_server_by_name(self, name, action, **kwargs):

        self._check_name(name)
        if action not in ['abort', 'abort_async', 'renew', 'reset', 'collect']:
            raise KeyError('Invalid value for action, allowed value should be abort abort_async renew reset collect')
        ch = self.get_handles('dhcp_server')
        for i in ch:
            if i.value == name:
                return self._control_dhcp_server_by_name(i.handle, action=action, **kwargs)

    @cafe.teststep('verify dhcp client stats!')
    def get_dhcp_client_stats_by_key(self, port, key, mode='session', **kwargs):
        self._check_port(port)

        if mode == 'session':
            res = self.tcl.command("CiHLT::_getDHCPClientHandlesByPort %s" % port)[2]
            handles = re.findall(r'(::ixNet::OBJ-/vport:\d+/protocolStack/ethernet:\S+)', res)
            if not handles:
                raise ValueError('No DHCP client handle were found to bind on port.')
            for item in handles:
                self._dhcp_client_stats_by_handle(item, mode, **kwargs)
                self.get_stats(reset=False)
            return self.get_stats_by_key_regex(key)
        else:
            return self._get_dhcp_client_stats(port, key, mode, **kwargs)

    @cafe.teststep('verify dhcp client stats!')
    def get_dhcp_client_stats_by_key_by_name(self, name, key, mode='session', **kwargs):

        self._check_name(name)
        return self._get_dhcp_client_stats_by_name(name, key, mode, **kwargs)

    @cafe.teststep('verify dhcp server stats!')
    def get_dhcp_server_stats_by_key(self, port, key, action='collect', **kwargs):

        self._check_port(port)
        return self._get_dhcp_server_stats(port, key, action, **kwargs)

    @cafe.teststep('verify dhcp server stats!')
    def get_dhcp_server_stats_by_key_by_name(self, name, key, action='collect', **kwargs):

        #raise NotImplementedError('NOT ready for use yet!')

        self._check_name(name)
        return self._get_dhcp_server_stats_by_name(name, key, action, **kwargs)

    @cafe.teststep('create pppoe server!')
    def create_pppoe_v6_server(self, name, port, **kwargs):
        opts = {'encap':'ethernet_ii',
                'protocol':'pppoe','num_sessions':5,
                'port_role':'network',
                'ip_cp':'ipv6_cp'
                }
        opts.update(kwargs)
        return self.create_pppoe_server(name, port, **opts)

    @cafe.teststep('create pppoe server!')
    def create_pppoe_server(self, name, port, **kwargs):

        self._check_name(name)
        self._check_port(port)
        opts = {'encap':'ethernet_ii',
                'protocol':'pppoe','num_sessions':5,
                'port_role':'network'}

        opts.update(kwargs)

        res = self._conf_pppox(port = port, mode = 'add', **opts)
        print res
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException("ERROR:Failed to create PPPoE server.")
            raise IXIAConfigurePPPoXServerError

        m = re.search(r'{handle (.*)}', res)
        h = m.group(1)

        self._set_handle(name, name, h, "pppoe_server")
        return h

    @cafe.teststep('create pppoe v6 client!')
    def create_pppoe_v6_client(self, name, port, **kwargs):
        opts = {'encap':'ethernet_ii',
                'protocol':'pppoe','num_sessions':5,
                'port_role':'access',
                'ip_cp':'ipv6_cp'
                }

        opts.update(kwargs)
        return self.create_pppoe_client(name, port, **opts)

    @cafe.teststep('create pppoe client!')
    def create_pppoe_client(self, name, port, **kwargs):

        self._check_name(name)
        self._check_port(port)
        opts = {'encap':'ethernet_ii',
                'protocol':'pppoe','num_sessions':5,
                'port_role':'access'}

        opts.update(kwargs)

        res = self._conf_pppox(port = port, mode = 'add', **opts)
        result = self.verify(res)
        if result == 'ERROR':
            #raise IXIASessionException("ERROR:Failed to create PPPoE client.")
            raise IXIAConfigurePPPoXClientError

        m = re.search(r'{handle (.*)}', res)
        h = m.group(1)

        self._set_handle(name, name, h, "pppoe_client")
        return h

    @cafe.teststep('delete pppoe server!')
    def delete_pppoe_server(self, name, port, **kwargs):


        self._check_name(name)
        self._check_port(port)
        opts = {'encap' : 'ethernet_ii',
                'protocol': 'pppoe',
                'num_sessions': 5
        }

        opts.update(kwargs)

        handle = filter(lambda x: x.ref == name, self.handles)
        if len(handle) == 0:
            raise ValueError('Invalid pppox name %s'%(name))
        opts['handle'] = handle[0].handle
        res = self._conf_pppox(port=port, mode='remove', **opts)

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException("ERROR:Falied to delete PPPoE server.")
            raise IXIAConfigurePPPoXServerError

        self.handles.remove(handle[0])
        delattr(self, name)

    @cafe.teststep('delete pppoe client!')
    def delete_pppoe_client(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        opts = {'encap' : 'ethernet_ii',
                'protocol': 'pppoe',
                'num_sessions': 5,
        }

        opts.update(kwargs)

        handle = filter(lambda x: x.ref == name, self.get_handles('pppoe_client'))
        if len(handle) == 0:
            raise ValueError('Invalid pppox name %s'%(name))
        opts['handle'] = handle[0].handle
        res = self._conf_pppox(port = port, mode = 'remove', **opts)

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException("ERROR:Falied to delete PPPoE client.")
            raise IXIAConfigurePPPoXClientError

        self.handles.remove(handle[0])
        delattr(self, name)

    @cafe.teststep('modify pppoe server!')
    def modify_pppoe_server(self, name, port, **kwargs):


        self._check_name(name)
        self._check_port(port)
        opts = {'encap':'ethernet_ii',
                'protocol':'pppoe','num_sessions':5}

        handle = filter(lambda x: x.ref == name, self.get_handles('pppoe_server'))
        if len(handle) == 0:
            raise ValueError('Invalid pppox name %s' % (name))
        opts['handle'] = handle[0].handle

        opts.update(kwargs)

        res = self._conf_pppox(port=port, mode='modify', **opts)

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to modify PPPoE server.')
            raise IXIAConfigurePPPoXServerError

    @cafe.teststep('modify pppoe client!')
    def modify_pppoe_client(self, name, port, **kwargs):

        self._check_name(name)
        self._check_port(port)
        opts = {'encap':'ethernet_ii',
                'protocol':'pppoe',
                'num_sessions':5
        }

        handle = filter(lambda x: x.ref == name, self.get_handles('pppoe_client'))
        if len(handle) ==0:
            raise ValueError('Invalid pppox name %s' % (name))

        opts['handle'] = handle[0].handle

        opts.update(kwargs)

        res = self._conf_pppox(port = port, mode = 'modify', ** opts)

        result = self.verify(res)

        if result == 'ERROR':
            #raise IXIASessionException('ERROR:Failed to modify PPPoE server.')
            raise IXIAConfigurePPPoXServerError

    @cafe.teststep('control pppoe!')
    def control_pppox(self, name, mode, **kwargs):

        self._check_name(name)
        handle = filter(lambda x: x.ref == name , self.handles)

        if len(handle)==0:
            raise ValueError('Invalid pppox name %s' % (name))

        res = self._control_pppox(handle[0].handle, mode)
        return res

    @cafe.teststep('get pppoe stats by key!')
    def get_pppox_stats_by_key_regex(self, name, port, mode, key):

        self._check_name(name)
        self._check_port(port)
        handle = filter(lambda x: x.ref == name, self.handles)
        if len(handle) == 0:
            raise ValueError('Invalid pppox name %s' % (name))

        self._pppox_stats(port, handle[0].handle, mode)
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    def get_pppox_stats_on_port_by_key_regex(self, port, mode, key):

        self._check_port(port)
        self._pppox_stats_by_port(port, mode)
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    @cafe.teststep('create igmp querier!')
    def create_igmp_querier(self, name, port, igmp_version, **kwargs):
        self._check_name(name)
        self._check_port(port)
        port_handle = self._get_handle(ref=port.ref, htype="port")
        if igmp_version not in ('v1','v2','v3'):
            raise ValueError("Only support IGMP version:[v1/v2/v3]")
        opts = {
            'intf_ip_addr':'10.41.1.1',
            'neighbor_intf_ip_addr':'10.41.1.2',
            'vlan_id':10,
            'vlan_user_priority':4,
        }
        opts.update(kwargs)
        res = self._conf_igmp_querier(handle = port_handle, mode = 'create',
                              igmp_version = igmp_version, **opts)
        m = re.search(r'(::ixNet::OBJ-/vport:\d+/protocols/igmp/querier:\d+)',
                      res)
        if m:
            ret_handle = m.group(1)
        else:
            IXIASessionException("Create IGMP session fail, "
                                 "Can't get handle!")
        self.logger.debug('Create igmp session success, '
                          'handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "igmp_querier")
        return ret_handle

    def get_igmp_querier_interface(self, name):

        self._check_name(name)
        handle = self._get_handle(ref=name, htype='igmp_querier')
        res = self.tcl.command("CiHLT::getIGMPQuerierInterface %s"%(handle))[2]

        m = re.search(r'(::ixNet::OBJ-/vport:\d+/interface:\d+)', res)

        if m :
            return m.group(1)
        else:
            IXIASessionException('Get IGMP Querier Interface Fail.')

    @cafe.teststep('modify igmp querier!')
    def modify_igmp_querier(self, name, igmp_version, **kwargs):
        self._check_name(name)
        querier_handle = self._get_handle(ref=name, htype="igmp_querier")

        if igmp_version not in ('v1','v2','v3'):
            raise ValueError("Only support IGMP version:[v1/v2/v3]")

        opts={'igmp_version':igmp_version}
        opts.update(kwargs)
        return self._conf_igmp_querier(handle = querier_handle, mode = 'modify', **opts)

    @cafe.teststep('delete igmp querier!')
    def delete_igmp_querier(self, name, **kwargs):
        self._check_name(name)
        querier_handle = self._get_handle(ref=name, htype="igmp_querier")

        opts = {}
        opts.update(kwargs)
        self._conf_igmp_querier(handle = querier_handle, mode = 'delete', **opts)
        self._del_handle(ref=name, htype="igmp_querier")

    @cafe.teststep('create igmp session!')
    def create_igmp(self, name, port, igmp_version, **kwargs):
        self._check_name(name)
        self._check_port(port)
        port_handle = self._get_handle(ref=port.ref, htype="port")
        if igmp_version not in ('v1','v2','v3'):
            raise ValueError("Only support IGMP version:[v1/v2/v3]")
        opts = {
            'intf_ip_addr':'10.41.1.2',
            'neighbor_intf_ip_addr':'10.41.1.1',
            'vlan_id':10,
            'vlan_user_priority':4,
        }
        opts.update(kwargs)
        res = self._conf_igmp(handle = port_handle, mode = 'create',
                              igmp_version = igmp_version, **opts)
        m = re.search(r'(::ixNet::OBJ-/vport:\d+/protocols/igmp/host:\d+)',
                      res)
        if m:
            ret_handle = m.group(1)
        else:
            IXIASessionException("Create IGMP session fail, "
                                 "Can't get handle!")
        self.logger.debug('Create igmp session success, '
                          'handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "igmp_session")
        return ret_handle

    @cafe.teststep('modify igmp session!')
    def modify_igmp(self, name, **kwargs):
        self._check_name(name)
        session_handle = self._get_handle(ref=name, htype="igmp_session")

        opts = {}
        opts.update(kwargs)
        return self._conf_igmp(handle = session_handle, mode = 'modify', **opts)

    @cafe.teststep('delete igmp session!')
    def delete_igmp(self, name, **kwargs):
        self._check_name(name)
        session_handle = self._get_handle(ref=name, htype="igmp_session")

        opts = {}
        opts.update(kwargs)
        self._conf_igmp(handle = session_handle, mode = 'delete', **opts)
        self._del_handle(ref=name, htype="igmp_session")

    @cafe.teststep('enable igmp session!')
    def enable_igmp(self, name, **kwargs):
        self._check_name(name)
        session_handle = self._get_handle(ref=name, htype="igmp_session")

        opts = {}
        opts.update(kwargs)
        self._conf_igmp(handle = session_handle, mode = 'enable', **opts)

    @cafe.teststep('disable igmp session!')
    def disable_igmp(self, name, **kwargs):
        self._check_name(name)
        session_handle = self._get_handle(ref=name, htype="igmp_session")

        opts = {}
        opts.update(kwargs)
        self._conf_igmp(handle = session_handle, mode = 'disable', **opts)

    @cafe.teststep('disble all igmp session!')
    def disable_all_igmp(self, port, **kwargs):
        port_handle = self._get_handle(ref=port.ref, htype="port")
        return self._conf_igmp(handle=port_handle, mode="disable_all", **kwargs)

    @cafe.teststep('create igmp group member!')
    def create_igmp_group(self, name, session_name,
                          group_pool_name,
                          source_pool_name_list=None, **kwargs):
        self._check_name(name)
        self._check_name(session_name)
        self._check_name(group_pool_name)
        session_handle = self._get_handle(ref=session_name,
                                          htype="igmp_session")
        group_pool_handle = self._get_handle(ref=group_pool_name,
                                             htype='multicast_group')
        opts = {
            'session_handle' : session_handle,
            'group_pool_handle'  : group_pool_handle,
        }
        if source_pool_name_list:
            if not isinstance(source_pool_name_list, list):
                raise ValueError('multicast source name must be list')
            source_pool_handles = []
            for source_pool_name in source_pool_name_list:
                source_pool_handles.append(self._get_handle(ref=source_pool_name, htype='multicast_source'))
            opts.update({'source_pool_handle' : source_pool_handles})
        else:
            raise ValueError('Lack of the mandatory option [source_pool_name_list].')

        opts.update(kwargs)
        res = self._group_conf_igmp(mode = 'create', handle=None, **opts)
        m = re.search(r'(::ixNet::OBJ-/vport:\d+/protocols/igmp/host:\d+/group:\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            IXIASessionException("Create IGMP group fail, Can't get handle!")

        self.logger.debug('Create igmp session success, '
                          'handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "igmp_group")
        return ret_handle

    @cafe.teststep('modify igmp group!')
    def modify_igmp_group(self, name, session_name=None, group_pool_name=None,
                          source_pool_name_list=None, **kwargs):
        handle = self._get_handle(ref=name, htype='igmp_group')
        opts = {'handle' : handle}
        if session_name:
            session_handle = self._get_handle(ref=session_name,
                                              htype='igmp_session')
            opts.update({'session_handle' : session_handle})

        if group_pool_name:
            group_pool_handle = self._get_handle(ref=group_pool_name,
                                                 htype='multicast_group')
            opts.update({'group_pool_handle' : group_pool_handle})

        if source_pool_name_list:
            if not isinstance(source_pool_name_list, list):
                raise ValueError('multicast source name must be list')

            source_pool_handles = []
            for source_pool_name in source_pool_name_list:
                source_pool_handles.append(self._get_handle(ref=source_pool_name,
                                                            htype='multicast_source'))
            opts.update({'source_pool_handle' : source_pool_handles})

        opts.update(kwargs)
        return self._group_conf_igmp(mode = 'modify', **opts)

    @cafe.teststep('delete igmp group!')
    def delete_igmp_group(self, name):
        handle= self._get_handle(ref=name, htype='igmp_group')
        self._group_conf_igmp(mode = 'delete', handle=handle)
        self._del_handle(ref=name, htype='igmp_group')

    @cafe.teststep('create multicast group pool!')
    def create_multicast_group(self, name, **kwargs):
        self._check_name(name)
        opts = {
            'num_groups' : 2,
            'ip_addr_start' : '225.0.1.1',
            'ip_addr_step' : '0.0.1.0',
            'ip_prefix_len' : 24,
        }
        opts.update(kwargs)
        res = self._group_conf_mutilcast(mode = 'create', handle=None, **opts)
        m = re.search(r'(group\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            IXIASessionException("Create Multicast group fail, "
                                 "Can't get handle!")
        self.logger.debug('Create multicast group success, '
                          'handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "multicast_group")
        return ret_handle

    @cafe.teststep('modify multicast group pool!')
    def modify_multicast_group(self, name, **kwargs):

        handle = self._get_handle(ref=name, htype='multicast_group')
        opts = {}
        opts.update(kwargs)

        return self._group_conf_mutilcast(mode = 'modify',
                                          handle=handle, **opts)

    @cafe.teststep('delete multicast group pool!')
    def delete_multicast_group(self, name):
        handle= self._get_handle(ref=name, htype='multicast_group')
        self._group_conf_mutilcast(mode = 'delete', handle=handle)
        self._del_handle(ref=name, htype='multicast_group')

    @cafe.teststep('create multicast source pool!')
    def create_multicast_source(self, name, **kwargs):
        self._check_name(name)
        opts = {
            'num_sources' : 2,
            'ip_addr_start' : '101.0.1.1',
            'ip_addr_step' : '0.0.0.1',
            'ip_prefix_len' : 24,
        }
        opts.update(kwargs)
        res = self._source_conf_mutilcast(mode = 'create', handle=None, **opts)
        m = re.search(r'(source\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            IXIASessionException("Create Multicast source fail,"
                                 " Can't get handle!")

        self.logger.debug('Create multicast source success,'
                          ' handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "multicast_source")
        return ret_handle

    @cafe.teststep('modify multicast source pool!')
    def modify_multicast_source(self, name, **kwargs):
        handle = self._get_handle(ref=name, htype='multicast_source')
        opts = {}
        opts.update(kwargs)
        return self._source_conf_mutilcast(mode = 'modify',
                                           handle=handle, **opts)

    @cafe.teststep('delete multicast source pool!')
    def delete_multicast_source(self, name):
        handle= self._get_handle(ref=name, htype='multicast_source')
        self._source_conf_mutilcast(mode = 'delete', handle=handle)
        self._del_handle(ref=name, htype='multicast_source')

    @cafe.teststep('control igmp querier!')
    def control_igmp_querier(self, mode, name, **kwargs):
        handle = self._get_handle(ref=name, htype='igmp_querier')
        self._control_igmp(mode = mode, handle=handle)

    @cafe.teststep('control igmp!')
    def control_igmp(self,name, mode, **kwargs):
        handle = self._get_handle(ref=name, htype='igmp_session')
        self._control_igmp(mode = mode, handle=handle)

    @cafe.teststep('get igmp statistic!')
    def get_igmp_stats_by_key_regx(self, port, key):
        port_handle = self._get_handle(ref=port.ref, htype="port")
        self._igmp_info(port_handle=port_handle, mode='aggregate')
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    def packet_control(self, port_handle, action):
        '''
        Purpose:
            Starts or stops packet capturing.
        Args:
            port_handle:<(handle,handle,handel)>
            action:{start|stop}
        '''
        port_h=""

        if isinstance(port_handle, (tuple, list)):
            for p in port_handle:
                p_h = self.get_port_handle(p)
                port_h += " "+p_h
        else:
            port_h = self.get_port_handle(port_handle)

        return self._control_cap(port_h, action)

    def packet_config_buffers(self, port_handle, action='stop', **kwargs):
        '''
        Purpose:
            Defines how Spirent HLTAPI will manage the buffers for packet
            capturing.
        Args:
            port_handle:<handle>
            action:{wrap|stop}
            Note:action not supported with IxTclNetwork and warning will be printed on stdout
if this parameter is used
        '''

        port_h = self.get_port_handle(port_handle)
        option = {}

        option.update(**kwargs)

        return self._conf_cap_buffer(port_h, action, **option)

    def packet_config_filter(self, port_handle, mode='create', **kwargs):
        '''
        Purpose:
            Defines how Spirent HLTAPI will filter the captured data. If you do not
            define any filters, Spirent HLTAPI captures all data.
        Args:
            port_handle:<handle>
            mode  (optional):{create}
        '''

        port_h = self.get_port_handle(port_handle)
        option = {}

        option.update(**kwargs)

        return self._conf_cap_filter(port_h, mode, **option)

    def packet_config_triggers(self, port_handle, mode='create', **kwargs):
        '''
        Purpose:
            Defines the condition (trigger) that will start or stop packet capturing.
            By default, Spirent HLTAPI captures all data and control plane packets
            that it sends and all data plane packets that it receives.
        Args:
            port_handle:<handle>
            mode  (optional):{create}
        '''

        port_h = self.get_port_handle(port_handle)
        option = {}

        option.update(**kwargs)

        return self._conf_cap_triggers(port_h, mode, **option)

    def packet_stats(self, port_handle, stop=1, filename = '/tmp/default.pcap', pkt_mode='data', **kwargs):
        '''
        Purpose:
            Returns statistical information about each packet associated with the specified
            port(s). Statistics include the connection status and number and type of messages
            sent and received from the specified port.
            Packet Capture Functions
        Args:
            port_handle:<handle>
            stop  (optional):{0|1}
            format  (optional):{pcap | var}
            filename  (optional):<filename>
        '''

        port_h = self.get_port_handle(port_handle)
        option = {}
        # if filename:
        #     option['filename'] = filename

        option.update(**kwargs)
        return self._conf_cap_stats(port_h, stop, filename, pkt_mode, **option)

    def create_cfm_bridge(self, name, port, **kw):

        self._check_port(port)
        self._check_name(name)

        opts = {}
        opts.update(kw)

        res = self._config_cfm_bridge(port, 'create', **opts)

        m = re.search(r'{handle (.*)}', res)
        handles = m.group(1).split(' ')
        self._set_handle(name, name, handles, 'cfm_bridge')

        return handles

    def modify_cfm_bridge_by_index(self, name, index=0, **kw):
        self._check_name(name)

        bridge_handle = getattr(self, name).handle[int(index)]
        opts = {'handle': bridge_handle}
        opts.update(kw)
        self._config_cfm_bridge(None, 'modify', **opts)

    def delete_cfm_bridge_by_index(self, name, index=0):

        self._check_name(name)
        handle = getattr(self, name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_bridge(None, 'remove', **opts)

        getattr(self, name).handle[int(index)] = None

        if len(filter(lambda x: x != None, getattr(self, name).handle)) == 0:
            self._del_handle(name, 'cfm_bridge')

    def enable_cfm_bridge_by_index(self, bridge_name, index):

        self._check_name(bridge_name)

        handle = getattr(self, bridge_name).handle[int(index)]

        opts = {'handle': handle}

        self._config_cfm_bridge(None, 'enable', **opts)

    def disable_cfm_bridge_by_index(self, bridge_name, index):

        self._check_name(bridge_name)
        handle = getattr(self, bridge_name).handle[int(index)]
        opts = {'handle': handle}

        self._config_cfm_bridge(None, 'disable', **opts)

    def control_cfm_bridge_by_port(self, port, action):

        self._check_port(port)
        if action not in ['start', 'stop']:
            raise ValueError('Invalid action Type')
        self._control_cfm_bridge(port, action)

    def create_cfm_vlan(self, name, bridge_name, index=0, **kw):

        self._check_name(name)

        handle = getattr(self, bridge_name).handle[int(index)]

        res = self._config_cfm_vlan(handle, 'create', **kw)

        print res

        m = re.search(r'{handle (.*)}', res)
        handles = m.group(1).split(' ')
        self._set_handle(name, name, handles, 'cfm_vlan')

        return handles

    def modify_cfm_vlan_by_index(self, vlan_name, index=0 , **kw):

        self._check_name(vlan_name)

        handle = getattr(self, vlan_name).handle[int(index)]
        opts = {'handle': handle}
        opts.update(kw)
        self._config_cfm_vlan(None, 'modify', **opts)

    def delete_cfm_vlan_by_index(self, vlan_name, index):

        self._check_name(vlan_name)

        handle = getattr(self, vlan_name).handle[int(index)]
        opts = {'handle': handle}

        self._config_cfm_vlan(None, 'remove', **opts)

        getattr(self, vlan_name).handle[int(index)] = None

        if len(filter(lambda x: x != None, getattr(self, vlan_name).handle)) == 0:
            self._del_handle(vlan_name, 'cfm_vlan')

    def enable_cfm_vlan_by_index(self, vlan_name, index):
        self._check_name(vlan_name)

        handle = getattr(self, vlan_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_vlan(None, 'enable', **opts)

    def disable_cfm_vlan_by_index(self, vlan_name, index):
        self._check_name(vlan_name)

        handle = getattr(self, vlan_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_vlan(None, 'disable', **opts)

    def create_cfm_links(self, links_name, bridge_handle, index=0 , **kw):

        self._check_name(links_name)

        handle = getattr(self, bridge_handle).handle[int(index)]
        res = self._config_cfm_links(handle, 'create', **kw)
        m = re.search(r'{handle (.*)}', res)
        handles = m.group(1).split(' ')
        self._set_handle(links_name, links_name, handles, 'cfm_links')

        return handles

    def modify_cfm_links_by_index(self, links_name, index=0, **kw):
        handle = getattr(self, links_name).handle[int(index)]
        opts = {'handle': handle}
        opts.update(kw)
        self._config_cfm_links(None, 'modify', **opts)

    def delete_cfm_links_by_index(self, links_name, index):

        self._check_name(links_name)

        handle = getattr(self, links_name).handle[int(index)]
        opts = {'handle': handle}

        self._config_cfm_links(None, 'remove', **opts)

        getattr(self, links_name).handle[int(index)] = None

        if len(filter(lambda x: x != None, getattr(self, links_name).handle)) == 0:
            self._del_handle(md_meg_name, 'cfm_md_meg')

    def enable_cfm_links_by_index(self, links_name, index):
        self._check_name(links_name)

        handle = getattr(self, links_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_links(None, 'enable', **opts)

    def disable_cfm_links_by_index(self, links_name, index):
        self._check_name(links_name)

        handle = getattr(self, links_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_links(None, 'disable', **opts)

    def create_cfm_md_meg(self, md_meg_name, bridge_handle, index=0, **kw):

        self._check_name(md_meg_name)

        handle = getattr(self, bridge_handle).handle[int(index)]

        res = self._config_cfm_md_meg(handle, 'create', **kw)

        print res

        m = re.search(r'{handle (.*)}', res)
        handles = m.group(1).split(' ')
        self._set_handle(md_meg_name, md_meg_name, handles, 'cfm_md_meg')

        return handles

    def modify_cfm_md_meg_by_index(self, md_meg_name, index=0, **kw):

        handle = getattr(self, md_meg_name).handle[int(index)]
        opts = {'handle': handle}
        opts.update(kw)
        self._config_cfm_md_meg(None, 'modify', **opts)

    def delete_cfm_md_meg_by_index(self, md_meg_name, index):

        self._check_name(md_meg_name)

        handle = getattr(self, md_meg_name).handle[int(index)]
        opts = {'handle': handle}

        self._config_cfm_md_meg(None, 'remove', **opts)

        getattr(self, md_meg_name).handle[int(index)] = None

        if len(filter(lambda x: x != None, getattr(self, md_meg_name).handle)) == 0:
            self._del_handle(md_meg_name, 'cfm_md_meg')

    def enable_cfm_md_meg_by_index(self, md_meg_name, index):
        self._check_name(md_meg_name)

        handle = getattr(self, md_meg_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_md_meg(None, 'enable', **opts)

    def disable_cfm_md_meg_by_index(self, md_meg_name, index):
        self._check_name(md_meg_name)

        handle = getattr(self, md_meg_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_md_meg(None, 'disable', **opts)

    def create_cfm_mip_mep(self, mip_mep_name, bridge_handle, index=0, **kw):

        self._check_name(mip_mep_name)

        handle = getattr(self, bridge_handle).handle[int(index)]

        res = self._config_cfm_mip_mep(handle, 'create', **kw)

        m = re.search(r'{handle (.*)}', res)
        handles = m.group(1).split(' ')
        self._set_handle(mip_mep_name, mip_mep_name, handles, 'cfm_mip_mep')

        return handles

    def modify_cfm_mip_mep_by_index(self, mip_mep_name, index=0, **kw):

        handle = getattr(self, mip_mep_name).handle[int(index)]
        opts = {'handle': handle}
        opts.update(kw)
        self._config_cfm_mip_mep(None, 'modify', **opts)

    def delete_cfm_mip_mep_by_index(self, mip_mep_name, index):

        self._check_name(mip_mep_name)

        handle = getattr(self, mip_mep_name).handle[int(index)]
        opts = {'handle': handle}

        self._config_cfm_mip_mep(None, 'remove', **opts)

        getattr(self, mip_mep_name).handle[int(index)] = None

        if len(filter(lambda x: x != None, getattr(self, mip_mep_name).handle)) == 0:
            self._del_handle(mip_mep_name, 'cfm_mip_mep')

    def enable_cfm_mip_mep_by_index(self, mip_mep_name, index):
        self._check_name(mip_mep_name)

        handle = getattr(self, mip_mep_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_mip_mep(None, 'enable', **opts)

    def disable_cfm_mip_mep_by_index(self, mip_mep_name, index):
        self._check_name(mip_mep_name)

        handle = getattr(self, mip_mep_name).handle[int(index)]
        opts = {'handle': handle}
        self._config_cfm_mip_mep(None, 'disable', **opts)

    @cafe.teststep('load config file.')
    def load_config_file(self, config_path, **kwargs):
        if not os.path.exists(config_path):
            raise RuntimeError('{} is not exist.'.format(config_path))

        (path, config_file) = os.path.split(config_path)
        config_file_without_extension = os.path.splitext(config_file)[0]
        self._load_config_file(path, config_file_without_extension, **kwargs)

    @cafe.teststep('start all protocol!')
    def start_all_protocol(self, check_sum=False):
        return self._start_all_protocol(check_sum)

    @cafe.teststep('check protocol summary!')
    def check_protocol_sum(self):
        return self._check_protocol_sum()

    @cafe.teststep('apply traffic!')
    def apply_traffic(self):
        return self._apply_traffic()

    @cafe.teststep('clear traffic stats!')
    def clear_traffic_stats(self):
        return self._clear_traffic_stats()

    @cafe.teststep('get_traffic_stats!')
    def get_traffic_stats_traffic_iterm(self, row, colum):
        return self._get_traffic_stats_traffic_item(row, colum)

    @cafe.teststep('start all traffic!')
    def start_all_traffic(self):
        return self._start_all_traffic()

    @cafe.teststep('stop all traffic!')
    def stop_all_traffic(self):
        return self._stop_all_traffic()

    @cafe.teststep('stop all protocol!')
    def stop_all_protocol(self):
        return self._stop_all_protocol()



if __name__ == "__main__":
    res = """
    ################################################################################
    status: 1
    waiting_for_stats: 1
    1/8/5:
        aggregate:
            tx:
                pkt_count: 328831
                control_frames: 0
                pkt_byte_count: 42090368
                pkt_kbit_rate: 0.000
                total_pkt_rate: 0
                total_pkts: 328831
                pkt_byte_rate: 0
                pkt_bit_rate: 0.000
                tx_aal5_scheduled_frames_count: 328831
                tx_aal5_scheduled_frames_rate: 0
                elapsed_time: 3893348160
                pkt_rate: 0.000
                scheduled_pkt_rate: 0
                pkt_mbit_rate: 0.000
                raw_pkt_count: 328831
                line_speed: 1000 Mbps
                scheduled_pkt_count: 328831
            rx:
                uds1_frame_rate: 0
                control_frames: 0
                data_int_errors_count: 0
                pkt_byte_count: 42090371
                uds2_frame_rate: 0
                pkt_mbit_rate: 0.000
                pkt_rate: 0.000
                raw_pkt_count: 328828
                collisions_count: 0
                total_pkts: 328828
                data_int_frames_count: 328828
                pkt_kbit_rate: 0.000
                uds2_frame_count: 328831
                pkt_byte_rate: 0
                raw_pkt_rate: 0
                pkt_count: 328828
                uds1_frame_count: 328831
                pkt_bit_rate: 0.000
            duplex_mode: Full
    aggregate:
        tx:
            pkt_byte_rate:
                avg: 0
                count: 2
                max: 0
                min: 0
                sum: 0
            pkt_count:
                sum: 657662
                count: 2
                avg: 328831
                max: 328831
                min: 328831
            tx_aal5_scheduled_frames_count:
                count: 2
                sum: 657662
                avg: 328831
                max: 328831
                min: 328831
            total_pkts:
                count: 2
                max: 328831
                min: 328831
                sum: 657662
                avg: 328831
            total_pkt_rate:
                min: 0
                count: 2
                sum: 0
                avg: 0
                max: 0
            elapsed_time:
                sum: 7786696340
                avg: 3893348170
                max: 3893348180
                count: 2
                min: 3893348160
            pkt_rate:
                count: 2
                sum: 0.0
                avg: 0.0
                max: 0.000
                min: 0.000
            scheduled_pkt_count:
                min: 328831
                sum: 657662
                avg: 328831
                max: 328831
                count: 2
            pkt_mbit_rate:
                count: 2
                sum: 0.0
                avg: 0.0
                max: 0.000
                min: 0.000
            pkt_kbit_rate:
                min: 0.000
                sum: 0.0
                count: 2
                avg: 0.0
                max: 0.000
            scheduled_pkt_rate:
                max: 0
                count: 2
                min: 0
                sum: 0
                avg: 0
            tx_aal5_scheduled_frames_rate:
                min: 0
                count: 2
                sum: 0
                avg: 0
                max: 0
            pkt_bit_rate:
                min: 0.000
                sum: 0.0
                avg: 0.0
                count: 2
                max: 0.000
            pkt_byte_count:
                min: 42090368
                count: 2
                sum: 84180736
                avg: 42090368
                max: 42090368
            raw_pkt_count:
                sum: 657662
                avg: 328831
                max: 328831
                min: 328831
                count: 2
            control_frames:
                avg: 0
                max: 0
                min: 0
                count: 2
                sum: 0
            line_speed:
                count: 2
        rx:
            pkt_count:
                max: 328828
                min: 328827
                sum: 657655
                avg: 328827
                count: 2
            pkt_rate:
                avg: 0.0
                count: 2
                max: 0.000
                min: 0.000
                sum: 1315324.0
            uds2_frame_rate:
                sum: 0
                avg: 0
                max: 0
                count: 2
                min: 0
            raw_pkt_rate:
                max: 0
                count: 2
                min: 0
                sum: 0
                avg: 0
            pkt_kbit_rate:
                avg: 0.0
                max: 0.000
                count: 2
                min: 0.000
                sum: 0.0
            data_int_errors_count:
                avg: 0
                max: 0
                min: 0
                sum: 0
                count: 2
            total_pkts:
                max: 328828
                min: 328827
                count: 2
                sum: 657655
                avg: 328827
            control_frames:
                max: 0
                min: 0
                sum: 0
                count: 2
                avg: 0
            uds2_frame_count:
                min: 328831
                count: 2
                avg: 328831
                max: 328831
            uds1_frame_rate:
                count: 2
                sum: 0
                avg: 0
                max: 0
                min: 0
            pkt_bit_rate:
                avg: 0.0
                max: 0.000
                min: 0.000
                count: 2
                sum: 0.0
            pkt_mbit_rate:
                min: 0.000
                sum: 0.0
                count: 2
                avg: 0.0
                max: 0.000
            collisions_count:
                min: 0
                count: 2
                sum: 0
                avg: 0
                max: 0
            raw_pkt_count:
                min: 328827
                sum: 657655
                count: 2
                avg: 328827
                max: 328828
            pkt_byte_count:
                sum: 84180742
                avg: 42090371
                count: 2
                max: 42090371
                min: 42090371
            uds1_frame_count:
                avg: 328831
                max: 328831
                min: 328831
                count: 2
            data_int_frames_count:
                avg: 328827
                max: 328828
                min: 328827
                sum: 657655
                count: 2
            pkt_byte_rate:
                avg: 0
                max: 0
                min: 0
                count: 2
                sum: 0
        duplex_mode:
            count: 2
    1/8/4:
        aggregate:
            rx:
                uds2_frame_count: 328831
                pkt_kbit_rate: 0.000
                pkt_byte_rate: 0
                uds1_frame_count: 328831
                data_int_errors_count: 0
                pkt_mbit_rate: 0.000
                uds1_frame_rate: 0
                total_pkts: 328827
                control_frames: 0
                raw_pkt_rate: 0
                collisions_count: 0
                uds2_frame_rate: 0
                raw_pkt_count: 328827
                pkt_byte_count: 42090371
                pkt_bit_rate: 0.000
                pkt_rate: 0.000
                pkt_count: 328827
                data_int_frames_count: 328827
            tx:
                pkt_count: 328831
                pkt_mbit_rate: 0.000
                line_speed: 1000 Mbps
                pkt_bit_rate: 0.000
                raw_pkt_count: 328831
                tx_aal5_scheduled_frames_rate: 0
                elapsed_time: 3893348180
                tx_aal5_scheduled_frames_count: 328831
                total_pkts: 328831
                pkt_kbit_rate: 0.000
                pkt_byte_rate: 0
                scheduled_pkt_rate: 0
                control_frames: 0
                pkt_byte_count: 42090368
                total_pkt_rate: 0
                scheduled_pkt_count: 328831
                pkt_rate: 0.000
            duplex_mode: Full

    ################################################################################
    """
