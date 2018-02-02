import collections
import re
import cafe
from cafe.core.logger import CLogger as Logger
from cafe.core.utils import Param
from cafe.equipment.spirent.stc.cstc import _CSTC, STCSessionException, TrafficConfigError
from cafe.core.exceptions.tg.stc import *
from handle import Handle

_module_logger = Logger(__name__)
debug = _module_logger.debug


class STCDriver(_CSTC):

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    default_prompt = collections.OrderedDict(
        {r"[^\r\n].+\#": None,
         r"[^\r\n].+\>": None,
         r"[^\r\n].+\$": None,
         r"[^\r\n].+\:\~\$": None,
         r"[^\r\n]+(\%)": None,
         r"\-\-More\-\-": " ",
         }
    )
    error_response = r"error"

    def __init__(self, session=None, name=None, default_timeout=5, crlf="\n", app=None):

        super(_CSTC, self).__init__()
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
        self.port_list = []
        self.topology_route_info = {}
        self.topo_route_handle_reg = {
            'router': 'routerlsa',
            'summary_routes': 'summarylsablock',
            'grid': 'ospfGrid',
            'ext_routes': 'externallsablock',
            'nssa_routes': 'externallsablock',
            'network': 'networklsa',
        }

        self.lsa_handle_reg = {
            'router': 'routerlsa',
            'network': 'networklsa',
            'summary_pool': 'summarylsablock',
            'asbr_summary': 'asbrsummarylsa',
            'ext_pool': 'externallsablock',
            'nssa_ext_pool': 'externallsablock',
            'opaque_type_10': 'telsa',
            'extended_prefix': 'extendedprefixlsa',
            'extended_link': 'extendedlinklsa',
            'router_info': 'routerinfolsa',
        }

    # def __del__(self):
    #     self.del_handles()
    #     self.cleanup_session(self.port_list)
    #     self.close()

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

    def _set_handle(self, ref, name, handle, htype):
        """
        set handle and create a attribute into traffic gen object.
        """
        if hasattr(self, ref) is False:
            h = Handle(ref, name, handle, htype)
            self.handles.append(h)
            setattr(self, ref, h)
        else:
            #stc has bug for load config multi times(redundant ports will be created
            # for each load)
            self._del_handle(ref,htype)
            h = Handle(ref, name, handle, htype)
            self.handles.append(h)
            setattr(self, ref, h)
            # raise TrafficConfigError("reference %s already exist in traffic gen data structure." % ref)

    def _get_handle(self, name):
        """
        Obtain handle from traffic gen object.
        """

        try:
            handles = getattr(self, name).handle
            return handles
        except AttributeError:
            raise AttributeError('%s not found!' % name)
        # handle_instance = filter(lambda x: x.ref == ref and x.handle_type == htype, self.handles)
        # if not handle_instance:
        #     raise ValueError("Obtain handle failed, [{}] not found".format(ref))
        # return handle_instance[0].handle

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
        If handle is not found in self.handle return handle itself
        """
        for h in self.handles:
            if handle == h.handle:
                return h.ref
        return handle

    def _flatten_and_translate(self, d, parent_key='', sep='.'):
        """
        flatten nested dictionary and translate value to traffic specific key values

        """
        items = []
        for k, v in d.items():
            #k is traffic gen object handle
            _k = self._from_handle_to_ref(k)
            new_key = '%s%s%s' % (parent_key, sep, _k) if parent_key else _k
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

        for h in self.handles:
            if h.handle_type == htype.lower():
                ret.append(h)
        return ret

    def del_handles(self):
        """
        return a list of handle of same handle type
        """
        for h in self.handles:
            if hasattr(self, h.ref):
                delattr(self, h.ref)
        self.handles = []

    # def set_session(self, session):
    #     self.session = session
    #
    def _set_prompt(self, d):
        self.prompt = d.keys()
        self.action = d.values()
    #
    # def _cmd(self, *args, **kwargs):
    #     r = self.session.command(*args, **kwargs)
    #     return {"prompt": r[1], "value": r[2], "content": r[2]}
    #
    # @cafe.teststep("send command")
    # def command(self, *args, **kwargs):
    #     return self._cmd(*args, **kwargs)
    #
    # @cafe.teststep("send command")
    # def cli(self, *args, **kwargs):
    #     return self._cmd(*args, **kwargs)

    def get_stream_handle(self, sname):
        res = self.tcl.command("CsHLT::get_stream_handle {%s}" % sname, timeout=20)[2]
        pat = "ret\:(?P<streamname>[^\s]*)"
        ret = re.findall(pat, res)
        if ret:
            return ret[0]
        else:
            return None

    def get_port_handle(self, port):
        self.logger.info("get port handle for port %s" % port)
        res = self.session.command("CsHLT::get_port_handle %s" % port, timeout=60)
        if res[0] > -1:
            m = re.search(r"(port\d+)", res[2])
            if m:
                return m.group(1)
            else:
                raise TrafficConfigError("cannot get port handle for %s." % port)
        else:
            raise TrafficConfigError("cannot get port handle for %s. reason: command timeout" % port)

    def load_all_stream_names_and_handles(self):

        self.logger.info("get all traffic names and handles")
        res = self.session.command("CsHLT::get_all_stream_names_and_handles", timeout=120)[2]
        value = res.split('\r\n')[1]
        l = value.split('#')[1:-1]
        if len(l)>0:
            it = iter(l)
            d = dict(zip(it,it))
            for k in d:
                self._set_handle(k, k, d[k], "stream")
        else:
            self.logger.warn("No stream found in STC config file.")

    def _process_stats(self , s):
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

    def _check_name(self, name):

        if not isinstance(name, (str, unicode)):
            raise TypeError('name should be a string format!')

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
            raise ValueError('Stream %s not found!' % stream)

    @cafe.teststep("get traffic gen stats into buffer")
    def get_stats(self, reset=False):
        """
        read the traffic gen stats and put them into traffic gen stats dictionary in flatten form.
        """

        if reset:
            self.stats = {}

        ret = self.return_stats().replace('-', 'NA')
        p = self._process_stats(ret)
        _p = self._flatten_and_translate(p)
        self.stats.update(_p)

        for k, v in sorted(self.stats.items()):
            self.logger.debug(k + ":" + str(v))

        self._update_app_result(_p)
        return _p

    @cafe.teststep("get traffic gen stats by key")
    def get_stats_key(self, key):
        return self.stats[key]

    @cafe.teststep("get traffic gen stats by key regex")
    def get_stats_by_key_regx(self, key):
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

    def _get_traffic_stats(self, mode="streams"):
        """
        Args:
            mode: Specifies the type of statistics to collect
                possible values:
                    - aggregate - Collect all transmitted (tx) and received (rx) packets
                    - out_of_filter - Collect received (rx) packets that do not match the filter
                    - detailed_streams - Collect detailed statistics for individual streams
                    - streams - Collect detailed test stream statistics
                    - all - Collect all statistics

        Purpose:
            read the traffic gen stats and put them into traffic gen stats dictionary in flatten form.
        return:
            all of the stats stored
            Examples: ret.last.stats['p1.stream.streamblock1.rx.avg_delay'] will get the avg_delay info
        Note:
            it is deprecated to use the return value directly, instead you should call
            get_stats_by_key_regex to get the stat info after this call

        """
        ports = self.get_handles("port")
        self.logger.debug("port handles " + str(ports))

        #reset stats
        self.stats = {}

        for p in ports:
            self.traffic_stats(p.value, mode)
            self.get_stats()
        self._update_app_result(self.stats)
        return self.app.result

    def get_stats_by_key_regex(self, key):
        ret = {}
        for k, v in self.stats.items():
            m = re.search(key, k)
            if m:
                ret[k] = v
        if ret:
            return ret
        else:
            raise RuntimeError("key %s not found!" % key)

    def _open(self, chassis_ip, equipment_type="stc", ports={}, ix_network_ip=None, ix_network_port=8009):
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

        if equipment_type == "stc":
            self.enable_test_log("/tmp")
            #self.enable_hlt_log("/tmp")
            self.chassis_ip = chassis_ip
            self.port_list = ports

    @cafe.teststep('connect stc chassis!')
    def connect_to_chassis(self, xml=""):
        if True:
            _p = []
            for k in sorted(self.port_list.keys()):
                v = self.port_list[k]
                _p.append(v['port'])
                #handle = self.get_port_handle(port)
                #self._set_handle(k, port, handle, "port")
            port_list = " ".join(_p)
            super(STCDriver, self).connect_to_chassis(self.chassis_ip,
                                                      port_list, xml)
            if xml:
                self.load_all_stream_names_and_handles()

            for k in sorted(self.port_list.keys()):
                v = self.port_list[k]
                handle = self.get_port_handle(v['port'])
                self._set_handle(k, v['port'], handle, "port")

    def apply(self):
        super(STCDriver, self)._apply()

    def start_all_protocol(self):
        super(STCDriver, self)._start_all_protocol()

    def stop_all_protocol(self):
        super(STCDriver, self)._stop_all_protocol()

    def start_all_traffic(self):

        super(STCDriver, self)._start_all_traffic()

    def stop_all_traffic(self):

        super(STCDriver, self)._stop_all_traffic()

    @cafe.teststep('configure interface!')
    def config_interfaces(self, **kwargs):

        if True:
            cnt = 0
            for k in sorted(self.port_list.keys()):
                v = self.port_list[k]
                cnt += 1
                port = v['port']
                medium  = v["medium"]
                speed   = v["speed"]
                option = {
                    # "intf_mode":          "ethernet",
                    "phy_mode":           medium,
                    "speed":              speed,
                    # "autonegotiation":    "1",
                    # "duplex":             "full",
                    # "src_mac_addr":       "00:10:94:00:00:3%d" % cnt,
                    # "intf_ip_addr":       "10.1.%d.2" % cnt,
                    # "gateway":            "10.1.%d.1" % cnt,
                    # "netmask":            "255.255.255.0",
                    # "arp_send_req":       "1"
                 }
                option.update(**kwargs)
                self._config_interface(port, "config", **option)
                #handle = self.get_port_handle(port)
                #create handle for port
                #self._set_handle(k, port, handle, "port")

    @cafe.teststep('configure specified interface!')
    def config_interface(self, port, **kwargs):

        option = {}
        option.update(**kwargs)
        self._config_interface(port, 'config', **option)
        handle = self.get_port_handle(port)
        self._set_handle(port, port, handle, "port")

    @cafe.teststep('modify specified interface!')
    def modify_interface(self, port, **kwargs):

        option = {}
        option.update(**kwargs)
        self._config_interface(port, 'modify', **option)


    def _config_traffic(self, port, mode, **kwargs):
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
            >>> option = {"test1":"1", "test2":"2"}
            >>> config_traffic("2/1", "config", **option)
        """
        self.logger.info("%s traffic is in progress..." % mode)
        opt = self.dict2str(kwargs)
        res = self.tcl.command("CsHLT::traffic_conf %s %s {%s}" % (mode, port, opt), timeout=60)[2]
        r = self.verify(res)
        if r == "ERROR":
            print res
            #raise TrafficConfigError("ERROR:Failed to %s traffic on %s!" % (mode, port))
            raise STCConfigureTrafficError
        else:
            self.logger.info ("PASS:%s traffic on port %s done!" % (mode, port))
            print res
            m = re.search(r"(streamblock\d+)", res)
            #print(m)
            #print m.group(1)
            return m.group(1)

    def _modify_traffic(self, port, mode, **kwargs):
        opt = {}
        opt.update(**kwargs)
        return self._config_traffic(port, mode, **opt)

    def _verify_traffic_loss_on_stream_within(self, stream, percent):
        '''
        Purpose:
            Verify data traffic lost for test equipment's data stream object is within "percentage" tolerance

        Args:
            stream: data stream name reference
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True traffic lost within "percent"; False otherwise
        '''
        if not isinstance(percent, (int, float)):
            raise TypeError('percent should be a int or float type!')
        strs = self.get_handles('stream')
        ports = self.get_handles('port')
        for p in ports:
            for i in strs:
                if i.value == stream:
                    opt ={"streams": i.handle}
                    loss = self._get_traffic_stats_on_port(p, "dropped_pkts", **opt).values()[0]
                    total_pkts = self._get_traffic_stats_on_port(p, "total_pkts").values()[0]
                    if total_pkts == 0:
                        raise ZeroDivisionError('No packets received!')
                    if abs(loss) / abs(total_pkts) > percent:
                        self._fail('session(%s): verify no traffic loss on stream %s. failed (loss percent is %s)' % (self.name, stream,percent))
                        return False
                    self._pass('session(%s): verify no traffic loss.' % self.name)
                    return True

        raise RuntimeError('stream not found!')

    def _get_traffic_stats_key_on_all_ports(self, key):
        ports = self.get_handles("port")
        self.logger.debug("port handles " + str(ports))
        s = {}
        for p in ports:
            s.update(self._get_traffic_stats_on_port(p, key))
        return s

    def _get_traffic_stats_on_port(self, port, key, **kwargs):
        opt = {}
        opt.update(**kwargs)
        self.traffic_stats(port, "streams", **opt)
        self.get_stats()
        self._update_app_result(self.stats)
        return self.get_stats_by_key_regx(r"rx\.%s" % key)

    def _traffic_loss_within(self, allowed_loss):

        self._get_traffic_stats()
        if not isinstance(allowed_loss, (int, float)):
            raise KeyError("allowed_loss should be a int or float type!")
        dropped = self.get_stats_by_key_regx(r"rx\.dropped_pkts")
        v1 = dropped.values()
        total_pkts = self.get_stats_by_key_regx(r"rx\.total_pkts")
        v2 = total_pkts.values()
        for i in range(len(dropped)):
            self.logger.debug("verify_traffic_loss:" + dropped.keys()[i] + ":" + str(dropped.values()[i]))
            if v2[i] == 0:
                raise ZeroDivisionError('No packets received!')
            if abs(v1[i])/abs(v2[i]) > allowed_loss:
                self._fail("session(%s): verify traffic loss. failed (%s!=%d)" % (self.name, dropped.keys()[i], dropped.values()[i]))
                return False
        self._pass("session(%s): verify traffic loss is same as expected." % self.name)
        return True

    def _verify_traffic_loss_within_count_range(self, allowed_loss):
        """
        Purpose:
            Verify no data traffic lost tolerance for all test equipment's ports
        Args:
            allowed_loss: allow packet loss within expected count range.
        Returns:
            bool: True no traffic lost; False otherwise
        """
        self._get_traffic_stats()
        if not isinstance(allowed_loss, int):
            raise KeyError("allowed_loss should be a int type!")
        dropped = self.get_stats_by_key_regx(r"rx\.dropped_pkts")
        for k, v in dropped.items():
            self.logger.debug("verify_traffic_loss:" + k + ":" + str(v))
            if abs(float(v)) > allowed_loss:
                self._fail("session(%s): verify traffic loss. failed (%s=%s)" % (self.name, k, str(v)))
                return False
        self._pass("session(%s): verify traffic loss is same as expected." % self.name)
        return True

    def _verify_traffic_no_loss_on_stream(self, stream):
        '''
        Purpose:
            Verify no data traffic lost for test equipment's data stream object
        Args:
            stream: data stream name reference
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True if No traffic lost; False otherwise
        '''
        strs = self.get_handles("stream")
        ports = self.get_handles("port")
        for p in ports:
            for i in strs:
                if i.value == stream:
                    opt ={"streams": i.handle}
                    rx = self._get_traffic_stats_on_port(p, 'total_pkts', **opt)
                    for x, y in rx.items():
                        if float(y) != 0:
                            loss = self._get_traffic_stats_on_port(p, "dropped_pkts", **opt)
                            for k, v in loss.items():
                                #print loss
                                #print k, v
                                if float(v) != 0:
                                    self._fail("session(%s): verify no traffic loss on stream %s. failed (%s=%s)" % (self.name, stream, k, str(v)))
                                    return False
                            self._pass("session(%s): verify no traffic loss." % self.name)
                            return True
                        else:
                            #raise STCSessionException('NO packets received!')
                            raise STCGetTrafficStatsError
        raise RuntimeError('Stream not found!')

    def _verify_stats_greater_than(self, key, value):
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
        s = self._get_traffic_stats_key_on_all_ports(key)
        for k, v in s.items():
            self.logger.debug("verify traffic stats:" + k + ":" + str(v))
            if float(v) <= value:
                self._fail("session(%s): verify traffic stats. failed (%s=%s)" % (self.name, k, str(v)))
                return False
        self._pass("session(%s): verify traffic stats." % self.name)
        return True

    def _verify_stats_eq(self, key, value):
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
        s = self._get_traffic_stats_key_on_all_ports(key)
        for k, v in s.items():
            self.logger.debug("verify traffic stats:" + k + ":" + str(v))
            if float(v) != value:
                self._fail("session(%s): verify traffic stats. failed (%s=%s)" % (self.name, k, str(v)))
                return False
        self._pass("session(%s): verify traffic stats." % self.name)
        return True

    def _verify_stats_less_than(self, key, value):
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
        s = self._get_traffic_stats_key_on_all_ports(key)
        for k, v in s.items():
            self.logger.debug("verify traffic stats:" + k + ":" + str(v))
            if float(v) >= value:
                self._fail("session(%s): verify traffic stats. failed (%s=%s)" % (self.name, k, str(v)))
                return False
        self._pass("session(%s): verify traffic stats." % self.name)
        return True

    def _get_stream_stats_by_key(self, key, mode="streams", **kwargs):
        opt = {}
        opt.update(**kwargs)

        self._get_traffic_stats(mode)
        self._update_app_result(self.stats)
        return self.get_stats_by_key_regex(key)

    def _create_untag_traffic(self, port, name, **kwargs):
        option = {}
        option["name"] = str(name)
        option.update(**kwargs)
        s = self._config_traffic(port, "create", **option)
        # print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        # print s
        # print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        return s

    def _create_single_tag_traffic(self, name, port, vlan_id, vlan_user_priority, **kwargs):

            option = {}
            option["name"] = str(name)
            option["vlan_id"] = str(vlan_id)
            option["vlan_user_priority"] = str(vlan_user_priority)
            option['l2_encap'] = 'ethernet_ii_vlan'
            option.update(**kwargs)
            # print "#" * 80
            # print "[%s]" % option
            # print "#" * 80
            return self._config_traffic(port, "create", **option)

    def _create_double_tag_traffic(self, name, port, vlan_id, vlan_user_priority,
                                   vlan_id_outer, vlan_outer_user_priority, **kwargs):
        option = {}
        option["name"] = str(name)
        option["l2_encap"] = 'l3_protocol'
        option["vlan_id"] = str(vlan_id)
        option["vlan_user_priority"] = str(vlan_user_priority)
        option["vlan_id_outer"] = str(vlan_id_outer)
        option["vlan_outer_user_priority"] = str(vlan_outer_user_priority)
        option.update(**kwargs)
        # print "#" * 80
        # print "[%s]" % option
        # print "#" * 80
        return self._config_traffic(port, "create", **option)

    def _control_traffic_by_name(self, name, action, **kwargs):

        self._check_name(name)
        handle = filter(lambda x: x.ref == name, self.handles)
        print '====>', handle[0].handle
        opt = {}
        opt.update(**kwargs)
        return self._control_traffic_by_name_internal(handle[0].handle, action, **opt)

    @cafe.teststep("delete traffic stream")
    def traffic_delete(self, stream):
        stream_handle = self._get_handle(stream)
        opt = {'stream_id': stream_handle}
        self.config_traffic(None, 'remove', **opt)
        self._del_handle(stream, "stream")
        return True

    @cafe.teststep("delete all traffic stream")
    def traffic_delete_all(self):
        self.config_traffic(None, 'reset')
        stream_handles = self.get_handles('stream')
        for handle in stream_handles:
            delattr(self, handle.ref)
            self.handles.remove(handle)
        return True

    def _fail(self, msg):
        cafe.Checkpoint().fail(msg)

    def _pass(self, msg):
        cafe.Checkpoint().pass_test(msg)

    @cafe.teststep("create untag traffic stream")
    def traffic_config_untag(self, name, port, **kwargs):
        """
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
            length: pack length
            bidirectional: True is bidirectional False: uni-directional

        Raises:
            TrafficConfigError - error in config the traffic stream
        """

        x = self._create_untag_traffic(port=port, name=name, **kwargs)

        self._set_handle(name, name, x, "stream")
        return x

    def control_traffic(self, port, action, **kwargs):
        return self._control_traffic(port, action, **kwargs)

    def control_traffic_by_name(self, name, action, **kwargs):
        return self._control_traffic_by_name(name, action, **kwargs)

    @cafe.teststep("create sigle tag traffic stream")
    def traffic_config_single_tag(self, name, port, vlan_id, vlan_user_priority, **kwargs):
        """
        Purpose:
            helper function to create an untag traffic.
            layer 2 default to ethernet
            layer 3 default to ipv4

        Args:
            port: traffic generator port
            name: data stream name reference
            src_mac: source mac address
            dst_mac: destination mac address
            src_ip: source ipv4 address
            dst_ip: destination ipv4 address
            framesize: packet length
            bidirectional: True is bidirectional False: uni-directional
            rate_percent
            l2_encap: mandatory to set the -l2_encap to ethernet_ii_vlan when using vlan_id
            l3_protocol: mandatory to set the -l3_protocol to ipv4 when using ip_src_addr


        Raises:
            TrafficConfigError - error in config the traffic stream
        """
        option = {}
        option.update(**kwargs)
        x = self._create_single_tag_traffic(name, port, vlan_id, vlan_user_priority, **option)
        self._set_handle(name, name, x, "stream")
        return x

    @cafe.teststep("create double tag traffic stream")
    def traffic_config_double_tag(self, name, port, vlan_id=100, vlan_user_priority=0,
                                  vlan_id_outer=100, vlan_outer_user_priority=0,
                                   l2_encap='ethernet_ii_vlan', **kwargs):
        """
        """
        x = self._create_double_tag_traffic(name=name, port=port, vlan_id=vlan_id,
                                            vlan_user_priority=vlan_user_priority,
                                            vlan_id_outer=vlan_id_outer,
                                            vlan_outer_user_priority=vlan_outer_user_priority,
                                            l2_encap=l2_encap, **kwargs)
        self._set_handle(name, name, x, "stream")
        return x

    @cafe.teststep("create untag bound traffic stream")
    def bound_traffic_config_untag(self, name, port, rx_handle, tx_handle, **kwargs):
        """
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
            length: pack length
            bidirectional: True is bidirectional False: uni-directional

        Raises:
            TrafficConfigError - error in config the traffic stream
        """
        options = {'name': str(name),
                   'emulation_dst_handle': rx_handle,
                   'emulation_src_handle': tx_handle}
        options.update(**kwargs)
        x = self._config_traffic(port=port, mode='create', **options)
        self._set_handle(name, name, x, "stream")
        return x

    @cafe.teststep("create single tag bound traffic stream")
    def bound_traffic_config_single_tag(self, name, port, rx_handle, tx_handle,
                                        vlan_id=100, pbit=0, **kwargs):
        """
        Purpose:
            helper function to create an untag traffic.
            layer 2 default to ethernet
            layer 3 default to ipv4

        Args:
            port: traffic generator port
            name: data stream name reference
            src_mac: source mac address
            dst_mac: destination mac address
            src_ip: source ipv4 address
            dst_ip: destination ipv4 address
            framesize: packet length
            bidirectional: True is bidirectional False: uni-directional
            rate_percent
            l2_encap: mandatory to set the -l2_encap to ethernet_ii_vlan when using vlan_id
            l3_protocol: mandatory to set the -l3_protocol to ipv4 when using ip_src_addr


        Raises:
            TrafficConfigError - error in config the traffic stream
        """
        options = {'name': str(name),
                   'emulation_dst_handle': rx_handle,
                   'emulation_src_handle': tx_handle,
                   'l2_encap':'ethernet_ii_vlan'}

        options['vlan_id'] = str(vlan_id)
        options['vlan_user_priority'] = str(pbit)
        options.update(**kwargs)
        x = self._config_traffic(port, 'create', **options)
        self._set_handle(name, name, x, "stream")
        return x

    @cafe.teststep("create double tag bound traffic stream")
    def bound_traffic_config_double_tag(self, name, port, rx_handle, tx_handle,
                                        cvlan_id=100, cpbit=0, svlan_id=100, spbit=0,
                                        l2_encap='ethernet_ii_pppoe', **kwargs):
        """
        """
        options = {'name': name, 'emulation_dst_handle': rx_handle,
                   'emulation_src_handle': tx_handle,
                   'l2_encap':l2_encap,
                   'vlan_id': cvlan_id, 'vlan_user_priority':cpbit,
                   'vlan_id_outer': svlan_id, 'vlan_outer_user_priority':spbit}

        options.update(**kwargs)

        x = self._config_traffic(port, 'create', **options)
        self._set_handle(name, name, x, "stream")
        return x

    @cafe.teststep("verify no traffic loss on all ports")
    def verify_traffic_no_loss_old(self):
        """
        Purpose:
            Verify no data traffic lost for all test equipment's ports

        Returns:
            bool: True no traffic lost; False otherwise
        """
        ports = self.get_handles("port")
        self.logger.debug("port handles " + str(ports))

        #reset stats
        self.stats = {}

        for p in ports:
            self.traffic_stats(p.value, "streams")
            self.get_stats()
        self._update_app_result(self.stats)

        values = self.get_stats_by_key_regx(r"rx\.dropped_pkts")
        for k, v in values.items():
            self.logger.debug("verify_no_traffic_loss:" + k + ":" + str(v))
            if float(v) != 0:
                self._fail("session(%s): verify no traffic loss. failed (%s=%s)", (self.name, k, str(v)))
                return False
        self._pass("session(%s): verify no traffic loss." % self.name)
        return True

    @cafe.teststep("verify no traffic loss on all ports")
    def verify_traffic_no_loss(self):
        """
        Purpose:
            Verify no data traffic lost for all test equipment's ports

        Returns:
            bool: True no traffic lost; False otherwise
        """
        ports = self.get_handles("port")
        self.logger.debug("port handles " + str(ports))
        loss = {}
        for p in ports:
            _x = self._get_traffic_stats_on_port(p, 'total_pkts').values()
            try:
                rx_total_pkts = _x[0]
            except IndexError:
                self.logger.warn("There is no streamblock associated with the port {}".format(p))
                continue

            if rx_total_pkts == 0:
                self.logger.error("Traffic stats error, no packets received!")
                #raise STCSessionException("Traffic stats error, no packets received!")
                raise STCGetTrafficStatsError
            loss.update(self._get_traffic_stats_on_port(p, "dropped_pkts"))

        for k, v in loss.items():
            self.logger.debug("verify_no_traffic_loss:" + k + ":" + str(v))
            if float(v) != 0:
                self._fail("session(%s): verify no traffic loss. failed (%s=%s)" % (self.name, k, str(v)))
                return False
        self._pass("session(%s): verify no traffic loss." % self.name)
        return True

    @cafe.teststep("verify traffic loss within expected range")
    def verify_traffic_loss_within(self, allowed_loss):
        '''
        Purpose:
            Verify data traffic lost for test equipment's ports is within "percentage" tolerance

        Args:
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True traffic lost within "percent"; False otherwise
        '''
        return self._traffic_loss_within(allowed_loss)

    @cafe.teststep("verify no traffic loss on port")
    def verify_traffic_no_loss_on_port(self, port):
        '''
        Purpose:
            Verify no data traffic lost for test equipment's port
        Args:
            port

        Returns:
            bool: True if No traffic lost; False otherwise
        '''
        rx = self._get_traffic_stats_on_port(port, 'total_pkts')
        if not rx:
            self.logger.warn("There is no streamblock associated with the port {}".format(port))
            return

        for x, y in rx.items():
            if float(y) != 0:
                loss = self._get_traffic_stats_on_port(port, "dropped_pkts")
                for k, v in loss.items():
                    self.logger.debug("verify_no_traffic_loss:" + k + ":" + str(v))
                    if float(v) != 0:
                        self._fail("session(%s): verify no traffic loss. failed (%s=%s)" % (self.name, k, str(v)))
                        return False
                self._pass("session(%s): verify no traffic loss." % self.name)
                return True
            else:
                #raise STCSessionException('no packets received!')
                raise STCGetTrafficStatsError

    @cafe.teststep("verify traffic loss on port within expected range")
    def verify_traffic_loss_on_port_within(self, port, allowed_loss):
        '''
        Purpose:
            Verify data traffic lost for test equipment's port is within "percentage" tolerance

        Args:
            port
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True traffic lost within "percent"; False otherwise
        '''
        _x = self._get_traffic_stats_on_port(port, 'total_pkts').values()
        try:
            total_pkts = _x[0]
        except IndexError:
            self.logger.warn("There is no streamblock associated with the port {}".format(port))
            return

        loss = self._get_traffic_stats_on_port(port, "dropped_pkts").values()[0]
        if not isinstance(allowed_loss, (int, float)):
            raise TypeError("allowed_loss should be a int or float type!")
        self.logger.debug("verify_traffic_loss_on_port:" + "dropped" + "=" + str(loss) + "and total_pkts" +":" + str(total_pkts))
        if total_pkts == 0:
            raise ZeroDivisionError("No packets received!")
        actual = abs(loss)/abs(total_pkts)
        if actual > allowed_loss:
            self._fail("session(%s): verify traffic loss. failed ('loss:'%s / 'total:'%s = %s)" % (self.name, str(loss), str(total_pkts), str(actual)))
            return False
        self._pass("session(%s): verify traffic loss is same as expected. loss is %s" % (self.name, str(actual)))
        return True

    @cafe.teststep("verify traffic stats eaque expected.")
    def verify_stats_eq(self, key, value):
        if not (isinstance(key, str) or isinstance(key, unicode)) or not isinstance(value, int):
            raise TypeError("key or value is not valid! key should be str type and value should be int type.")
        return self._verify_stats_eq(key, value)

    @cafe.teststep("verify traffic stats less than expected!")
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
        if not (isinstance(key, str) or isinstance(key, unicode)) or not isinstance(value, int):
            raise TypeError("key or value is not valid! key should be str type and value should be int type.")
        return self._verify_stats_less_than(key, value)

    @cafe.teststep("verify traffic stats greater than expected!")
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
        if not (isinstance(key, str) or isinstance(key, unicode)) or not isinstance(value, int):
            raise TypeError("key or value is not valid! key should be str type and value should be int type.")
        return self._verify_stats_greater_than(key, value)

    @cafe.teststep('verify traffic no loss on stream!')
    def verify_traffic_no_loss_on_stream(self, stream):
        '''
        Purpose:
            Verify no data traffic lost for test equipment's data stream object
        Args:
            stream: data stream name reference
            percent: percentage tolerance of traffic lost

        Returns:
            bool: True if No traffic lost; False otherwise
        '''

        return self._verify_traffic_no_loss_on_stream(stream)

    @cafe.teststep("verify traffic loss on stream within expected percent.")
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
        return self._verify_traffic_loss_on_stream_within(stream, percent)

    @cafe.teststep('disable traffic!')
    def traffic_disable(self, name, **kwargs):
        '''
        Purpose:
            to disable traffic stream referenced by "stream" in configuration

        Args:
            stream: name reference of traffic stream
        '''

        self._check_name(name)
        #self._check_port(port)
        port = None
        h = self.get_handles('stream')
        for i in h:
            if i.value == name:
                mode = "disable"
                opt = {}
                opt["stream_id"] = i.handle
                opt.update(**kwargs)
                # self.__debug_print(opt)
                return self._modify_traffic(port, mode, **opt)
        else:
            raise STCSessionException('name %s not found!' % name)

    @cafe.teststep('Modify traffic')
    def traffic_modify(self, stream_name, **kw):
        if not hasattr(self, stream_name):
            raise RuntimeError('Invalid Stream Name')
        handle =  getattr(self, stream_name).handle
        options = {'stream_id': handle}
        options.update(**kw)
        return self._config_traffic(None, 'modify', **options)

    @cafe.teststep('Disable all traffic')
    def traffic_disable_all(self):
        '''
        Purpose:
            to disable all traffic streams in configuration

        '''

        streams = self.get_handles("stream")
        self.logger.debug("disable all streams!")
        try:
            for s in streams:
                #print s
                self.traffic_disable(s.value)
        except Exception as e:
            raise Exception(e)
        return True

    @cafe.teststep('Enable traffic')
    def traffic_enable(self, name, **kwargs):
        '''
        Purpose:
            to enable traffic stream referenced by "stream" in configuration

        Args:
            stream: name reference of traffic stream
        '''
        self._check_name(name)
        port = None
        #self._check_port(port)

        h = self.get_handles('stream')
        for i in h:
            if i.value == name:
                mode = "enable"
                opt = {}
                opt["stream_id"] = i.handle
                opt.update(**kwargs)
                # self.__debug_print(opt)
                return self._modify_traffic(port, mode, **opt)
        else:
            raise STCSessionException('name %s not found!' % name)

    @cafe.teststep('Enable all traffic')
    def traffic_enable_all(self):
        '''
        Purpose:
            to enable all traffic streams in configuration

        '''

        streams = self.get_handles("stream")
        self.logger.debug("enable all streams!")
        try:
            for s in streams:
                #print s.value
                self.traffic_enable(s.value)
        except Exception as e:
            raise Exception(e)
        return True

    @cafe.teststep('create pppoe v6 client!')
    def create_pppoe_v6_client(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        opts = {'protocol': 'pppoe','ip_cp':'ipv6_cp'}
        opts.update(kw)
        x = super(STCDriver, self)._create_pppoe_client(port, **opts)
        self._set_handle(name, name, x, "pppoe_client")
        return x

    @cafe.teststep('create pppoe client!')
    def create_pppoe_client(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        opts = {'protocol': 'pppoe'}
        opts.update(kw)
        x = super(STCDriver, self)._create_pppoe_client(port, **opts)
        self._set_handle(name, name, x, "pppoe_client")
        return x

    @cafe.teststep('modify pppoe client!')
    def modify_pppoe_client(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        handle = getattr(self, name).handle
        opt = {'handle': handle}
        opt.update(kw)
        return self._pppoe_client_conf(port, 'modify', **opt)

    @cafe.teststep('delete pppoe client!')
    def delete_pppoe_client(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        handles = filter(lambda x: x.ref == name, self.handles)
        if len(handles) == 0:
            raise ValueError('Invalid PPPoE name')
        opt = {'handle': handles[0].handle}
        opt.update(kw)

        self._pppoe_client_conf(port, 'reset', **opt)

        self.handles.remove(handles[0])
        delattr(self, name)

    @cafe.teststep('create pppoe v6 server!')
    def create_pppoe_v6_server(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        opts = {'protocol': 'pppoe','ip_cp':'ipv6_cp'}
        opts.update(kw)
        x = super(STCDriver, self)._create_pppoe_server(port, **opts)
        self._set_handle(name, name, x, "pppoe_server")
        return x

    @cafe.teststep('create pppoe server!')
    def create_pppoe_server(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        opts = {'protocol': 'pppoe'}
        opts.update(kw)
        x = super(STCDriver, self)._create_pppoe_server(port, **opts)
        self._set_handle(name, name, x, "pppoe_server")
        return x

    @cafe.teststep('modify pppoe server!')
    def modify_pppoe_server(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)
        handle = getattr(self, name).handle
        opts = {'handle': handle}
        opts.update(kw)
        return self._pppoe_server_conf(port, 'modify', **opts)

    @cafe.teststep('delete pppoe server!')
    def delete_pppoe_server(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        handles = filter(lambda x: x.ref == name, self.handles)
        if len(handles) == 0:
            raise ValueError('Invalid PPPoE Name')
        opts = {'handle': handles[0].handle}
        opts.update(kw)
        self._pppoe_server_conf(port, 'reset', **opts)
        self.handles.remove(handles[0])
        delattr(self, name)

    @cafe.teststep('control pppoe server!')
    def control_pppoe_server(self, name,  action, **kw):
        self._check_name(name)
        handle = getattr(self, name).handle
        x = super(STCDriver, self)._control_pppoe_server(handle, action, **kw)
        return x

    @cafe.teststep('control pppoe client!')
    def control_pppoe_client(self, name, action, **kw):
        self._check_name(name)
        handle = getattr(self, name).handle
        x = super(STCDriver, self)._control_pppoe_client(handle, action, **kw)
        return x

    @cafe.teststep('get pppox stats by key!')
    def get_pppox_stats_by_key_regex(self, name, mode, key):

        self._check_name(name)

        handles = filter(lambda x: x.ref == name , self.handles)
        if len(handles) == 0:
            raise ValueError('Invalid PPPoE name')

        pppox_type = handles[0].handle_type

        if pppox_type == 'pppoe_server':
            self.get_pppoe_server_stats(handles[0].handle, mode)
        elif pppox_type == 'pppoe_client':
            self.get_pppoe_client_stats(handles[0].handle, mode)
        else:
            raise ValueError('Invalid pppox type')
        self.get_stats()

        return self.get_stats_by_key_regx(key)

    def get_pppox_stats_on_port_by_key_regex(self, port,
                                             mode,
                                             key,
                                             **kw ):
        self._check_port(port)
        opts = {}
        opts.update(kw)
        handles = reduce(lambda x,y:x + ' ' + y ,
                         map(lambda x: x.handle,
                             self.get_handles('pppoe_client')))

        self.get_pppoe_client_stats('{'+ handles + '}', mode)
        self.get_stats()

        return self.get_stats_by_key_regx(key)

    @cafe.teststep('create dhcp server!')
    def create_dhcp_server(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        opt = {}
        opt.update(kwargs)
        mode = 'create'
        # opt['mode'] = mode
        res = self._emulation_dhcp_server_config(port, mode, 4, **opt)
        return self._set_handle(name, name, res, 'dhcp_server')

    @cafe.teststep('create option on dhcp server!')
    def create_dhcp_server_option(self, name, option_type, payload, **kwargs):

        self._check_name(name)
        handle = getattr(self, name).handle
        print '****'*30
        print handle
        if kwargs.has_key('MsgType'):
            msg_type = kwargs.get('MsgType')
        else:
            msg_type = 'ACK'

        if kwargs.has_key('EnableWildcards'):
            enable_wildcards = kwargs.get('EnableWildcards')
        else:
            enable_wildcards = 'TRUE'

        if kwargs.has_key('HexValue'):
            hex_value = kwargs.get('HexValue')
        else:
            hex_value = 'TRUE'

        res = self.tcl.command("CsHLT::create_dhcp_server_option %s %s %s %s %s %s"
                               % (handle, option_type, msg_type, enable_wildcards, hex_value, payload))[2]
        print '==='*30
        print res
        m=re.search(r'dhcpv[4|6]servermsgoption\d+',res)
        print m.group(0)
        print '==='*40
        if self.verify(res) == self.SUCCESS:
            return m.group(0)
        else:
            raise ValueError('Failed to set option on DHCP server')
            return res

    @cafe.teststep('create dhcp server v6!')
    def create_dhcp_server_v6(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        mode = 'create'
        opt = {}
        opt['ip_version'] = '6'
        opt['addr_pool_start_addr'] = '2008::2'
        opt['server_emulation_mode'] = 'DHCPV6'
        opt['encapsulation'] = 'ethernet_ii'
        opt['local_ipv6_addr'] = '2001::2'
        opt['gateway_ipv6_addr'] = '2001::1'
        opt['mac_addr'] = '00:10:94:00:00:03'
        #opt['version'] = 6
        # opt[''] = ''
        # opt[''] = ''
        opt.update(kwargs)
        res = self._emulation_dhcp_server_config(port, mode, 6, **opt)
        return self._set_handle(name, name, res, 'dhcp_server')

    @cafe.teststep('modify DHCP server!')
    def modify_dhcp_server(self, name, **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_server')
        for i in handles:
            if i.value == name:
                opt = {}
                opt['handle'] = i.handle
                opt.update(kwargs)
                mode = 'modify'
                # opt['mode'] = mode
                port = None
                res = self._emulation_dhcp_server_config(port, mode, 4, **opt)
                return res
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('modify DHCP server v6!')
    def modify_dhcp_server_v6(self, name, **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_server')
        for i in handles:
            if i.value == name:
                opt = {}
                opt['handle'] = i.handle
                opt.update(kwargs)
                mode = 'modify'
                # opt['mode'] = mode
                port = None
                res = self._emulation_dhcp_server_config(port, mode, 6, **opt)
                return res
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('reset dhcp server!')
    def reset_dhcp_server(self, name, **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_server')
        for i in handles:
            if i.value == name:
                opt = {}
                opt['handle'] = i.handle
                opt.update(kwargs)
                mode = 'reset'
                # opt['mode'] = mode
                port = None
                res = self._emulation_dhcp_server_config(port, mode, 4, **opt)
                self.handles.remove(i)
                delattr(self, name)
                return res
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('dhcp server relay agent config!')
    def dhcp_server_relay_agent_config(self, name, server_name, **kwargs):

        self._check_name(server_name)
        self._check_name(name)
        handles = self.get_handles('dhcp_server')
        for i in handles:
            if i.value == server_name:
                opt = {}
                opt.update(kwargs)
                mode = 'create'
                # opt['mode'] = mode
                res = self._emulation_dhcp_server_relay_agent_config(i.handle, mode, **opt)
                return self._set_handle(name, name, res, 'dhcp_client_relay_agent')
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('create dhcp client!')
    def create_dhcp_client(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        opt = {}
        opt.update(kwargs)
        mode = 'create'
        # opt['mode'] = mode
        res = self._emulation_dhcp_client(port, mode, **opt)
        print "====>", res.split()[-1]
        return self._set_handle(name, name, res.split()[-1], 'dhcp_client')

    @cafe.teststep('create dhcp client v6!')
    def create_dhcp_client_v6(self, name, port, **kwargs):

        self._check_port(port)
        self._check_name(name)
        opt = {}
        opt['ip_version'] = '6'
        # opt[''] = ''
        # opt[''] = ''
        opt.update(kwargs)
        mode = 'create'
        # opt['mode'] = mode
        res = self._emulation_dhcp_client(port, mode, **opt)
        print "====>", res.split()[-1]
        return self._set_handle(name, name, res.split()[-1], 'dhcp_client')


    @cafe.teststep('modify dhcp client!')
    def modify_dhcp_client(self, name, **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_client')
        for i in handles:
            if i.value == name:
                opt = {}
                opt['handle'] = i.handle
                print i.handle
                opt.update(kwargs)
                mode = 'modify'
                # opt['mode'] = mode
                port = None
                return self._emulation_dhcp_client(port, mode, **opt)
                #return res
        else:
            raise STCSessionException('handle not found!')
        # self._check_name(name)
        # opt = {}
        # opt['handle'] = port.value
        # opt.update(kwargs)
        # mode = 'modify'
        # # opt['mode'] = mode
        # _port = None
        # res = self._emulation_dhcp_client(_port, mode, **opt)
        # return res

    @cafe.teststep('reset dhcp client!')
    def reset_dhcp_client(self, name, **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_client')
        for i in handles:
            if i.value == name:
                opt = {}
                opt.update(kwargs)
                res = self._reset_dhcp_client(i.handle, **opt)
                self.handles.remove(i)
                delattr(self, name)
                return res
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('create dhcp client group!')
    def create_dhcp_client_group(self, name, dhcp_client_name, **kwargs):

        #self._check_port(port)
        self._check_name(name)
        self._check_name(dhcp_client_name)
        handles = self.get_handles("dhcp_client")
        for i in handles:
            if i.value == dhcp_client_name:
                opt = {}
                opt['encap'] = 'ethernet_ii'
                opt['num_sessions'] = '1'
                opt.update(kwargs)
                mode = 'create'
                # opt['mode'] = mode
                res = self._emulation_dhcp_client_group(i.handle, mode, 4, **opt)
                return self._set_handle(name, name, res.split()[-1], 'dhcp_client_group')
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('create dhcp client group!')
    def create_dhcp_client_group_v6(self, name, dhcp_client_name, **kwargs):

        #self._check_port(port)
        self._check_name(name)
        self._check_name(dhcp_client_name)
        handles = self.get_handles("dhcp_client")
        for i in handles:
            if i.value == dhcp_client_name:
                opt = {}
                opt['encap'] = 'ethernet_ii'
                #opt['create_dhcp_client_group_v6'] = 'DHCPV6'
                opt['local_ipv6_addr'] = '2001::3'
                #opt['gateway_ipv6_addr'] = '2001::1'
                opt['dhcp_range_ip_type'] = '6'
                opt['mac_addr'] = '00:10:94:00:00:04'
                opt.update(kwargs)
                mode = 'create'
                # opt['mode'] = mode
                res = self._emulation_dhcp_client_group(i.handle, mode, 6, **opt)
                return self._set_handle(name, name, res.split()[-1], 'dhcp_client_group')
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('modify dhcp client group!')
    def modify_dhcp_client_group(self, name, **kwargs):
        #self._check_port(port)
        self._check_name(name)
        #self._check_name(dhcp_client_name)
        handles = self.get_handles("dhcp_client_group")
        for i in handles:
            if i.value == name:
                opt = {}
                opt['encap'] = 'ethernet_ii'
                opt.update(kwargs)
                mode = 'modify'
                # opt['mode'] = mode
                res = self._emulation_dhcp_client_group(i.handle, mode, 4, **opt)
                return
                #return self._set_handle(name, name, res.split()[-1], 'dhcp_client_group')
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('enable dhcp client group!')
    def enable_dhcp_client_group(self, name, port, **kw):
        pass

    @cafe.teststep('reset dhcp client group!')
    def reset_dhcp_client_group(self, name, **kwargs):
        self._check_name(name)
        handles = filter(lambda x: x.value == name, self.get_handles('dhcp_client_group'))
        for i in handles:
            res = self._reset_dhcp_client_group(i.handle, **kwargs)
            self.handles.remove(i)
            delattr(self, name)
            return res
        else:
            raise STCSessionException('handle not found!')

    @cafe.teststep('control dhcp client!')
    def control_dhcp_client(self, name, mode, **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_client_group')
        for i in handles:
            if i.value == name:
                opt = {}
                opt.update(kwargs)
                return self._emulation_dhcp_client_control(i.handle, mode, **opt)

        else:
            raise STCSessionException('dhcp client not exist!')

    @cafe.teststep('control dhcp server!')
    def control_dhcp_server(self, name, mode, **kwargs):

        self._check_name(name)
        # handles = self.get_handles('dhcp_server')
        #
        # for i in handles:
        #     if i.value == name:
        #         opt = {}
        #         opt.update(kwargs)
        handle = getattr(self, name).handle
        debug('handle is ===== > %s'% handle)
        opt = {}
        opt.update(**kwargs)
        return self._emulation_dhcp_server_control(handle, mode, **opt)

    @cafe.teststep('get dhcp client stats!')
    def get_dhcp_client_stats_by_key(self, name, key, action='collect', **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_client_group')
        for i in handles:
            if i.value == name:
                opt = {}
                opt['action'] = action
                opt.update(**kwargs)
                super(STCDriver,self)._dhcp_client_stats(i.handle, **opt)
                self.get_stats()
                return self.get_stats_by_key_regex(key)

    def get_dhcp_client_stats_by_key_on_port(self,
                                             port,
                                             key,
                                             mode='session',
                                             **kw):

        self._check_port(port)
        opts = {'mode': mode}
        opts.update(**kw)
        self.tcl.command("CsHLT::dhcp_client_stats %s %s {%s}"%
                         (port, 'collect', self.dict2str(opts)))[2]
        self.get_stats()
        return self.get_stats_by_key_regex(key)

    @cafe.teststep('get dhcp sevrer stats!')
    def get_dhcp_server_stats_by_key(self, name, key, action='COLLECT', **kwargs):

        self._check_name(name)
        handles = self.get_handles('dhcp_server')
        for i in handles:
            if i.value == name:
                opt = {}
                #opt['mode'] = ''
                opt['action'] = action
                opt.update(**kwargs)
                super(STCDriver,self)._dhcp_server_stats(i.handle, **opt)
                self.get_stats()
                res = self.get_stats_by_key_regex(key)
                return res

    @cafe.teststep('')
    def example(self):
        pass

    def create_device(self, name, port, **kw):

        self._check_name(name)
        self._check_port(port)
        res = self.config_device(port, 'create', **kw)

        device_handle = re.search(r"{handle : (.*)}", res).group(1)
        self._set_handle(name, name, device_handle, 'device')
        return device_handle

    def modify_device(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)
        handle = getattr(self, name)
        opt = {'handle': handle.handle}
        opt.update(kw)
        res = self.config_device(port, 'modify', **opt)
        return res

    def delete_device(self, name, port, **kw):
        self._check_name(name)
        self._check_port(port)

        handles = filter(lambda x: x.ref == name, self.handles)
        if len(handles) == 0:
            raise ValueError('Invalid device name')
        opt = {'handle': handles[0].handle}

        self.config_device(port, 'delete', **opt)

        self.handles.remove(handles[0])
        delattr(self, name)

    def device_send_ping(self, name, dst_ip):
        self._check_name(name)

        handle = getattr(self, name).handle
        res = self.tcl.command("CsHLT::device_send_ping %s %s" % (handle, dst_ip))[2]
        print res
        if self.verify(res) == self.SUCCESS:
            pass
        else:
            raise ValueError('Failed to send ping command')
        return res

    def device_send_arp(self, name):
        self._check_name(name)
        handle = getattr(self, name).handle

        res = self.tcl.command("CsHLT::device_send_arp %s " % handle)[2]
        if self.verify(res) == self.ERROR:
            raise ValueError('Faild to send arp command')
        else:
            return res

    def start_arp_nd_on_all_devices(self):

        res = self.tcl.command("CsHLT::start_arp_nd_on_all_devices")[2]

        if self.verify(res) == self.ERROR:
            raise ValueError('Failed to start Arp Nd command on all devices')

    def start_all_devices(self):

        res = self.tcl.command("CsHLT::DevicesStartAllCommand")[2]

        if self.verify(res) == self.ERROR:
            raise ValueError('Failed to start all the STC devices')

    def stop_all_devices(self):

        res = self.tcl.command("CsHLT::DevicesStopAllCommand")[2]

        if self.verify(res) == self.ERROR:
            raise ValueError('Failed to stop all the STC devices')

    @cafe.teststep('Save configure file as XML')
    def save_config_as_xml(self, filename, project="project1"):
        '''
        save stc configure as xml file.

        Args:
            filename: xml file name.
            project: default is project1

        return:
            .

        Example:
            >>> save_config_as_xml("c:/test.xml")
        '''
        res = self.tcl.command("CsHLT::save_as_xml %s %s" % (filename, project), timeout=20)[2]
        r = self.verify(res)
        if r == "ERROR":
            raise STCSessionException("ERROR:Failed to save xml configure file (%s)" % filename)

        else:
            self.logger.info ("PASS: save xml configure file (%s) done!" % filename)
            return r

    @cafe.teststep('Cleanup STC Session')
    def close_stc_session(self, name, *args, **kwargs):
        '''
        Purpose:
            Cleans up the current test by terminating port reservations, disconnecting
            the ports from the chassis, releasing system resources, and removing the
            specified port configurations.
        Args:
            maintain_lock  (optional):{1|0}
            port_list  (optional):{list of port handles} | port_handle {list of porthandles}
            clean_dbfile  (optional):{1|0}
            clean_labserver_session  (optional):{1|0}
        '''
        port_list = []
        #self.del_handles()
        if name == self.name:
            self.logger.info("cleanup session...")
            for i in self.get_handles("port"):
                port_list.append(i.value)
            res = self.tcl.command("CsHLT::cleanup_session \"%s\"" % port_list, timeout=120)[2]
            r = self.verify(res)
            if r == "ERROR":
                #raise STCSessionException("ERROR:Failed to cleanup session")
                raise STCCleanupSessionError
            else:
                self.logger.info("PASS:Cleanup session done!")
                return r
        else:
            raise STCSessionException("Session %s not found!" % name)

    def clear_session(self):

        port_list = [x.value for x in self.get_handles('port')]
        if len(port_list) > 0:
            super(STCDriver, self).cleanup_session(port_list)
        self.del_handles()

    @cafe.teststep('create igmp session!')
    def create_igmp(self, name, port, igmp_version, **kwargs):

        self._check_name(name)
        self._check_port(port)

        port_handle = self._get_handle(port.ref)

        if igmp_version not in ('v2','v3'):
            raise ValueError("Only support IGMP version:[v2/v3]")

        opts = {
            'igmp_version' : igmp_version,
            'intf_ip_addr':'10.41.1.2',
            'neighbor_intf_ip_addr':'10.41.1.1',
        }
        opts.update(kwargs)

        res = self.config_igmp(handle = port_handle, mode = 'create', **opts)
        m = re.search(r'(host\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create IGMP session fail, Can't get handle!")

        self.logger.debug('Create igmp session success, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "igmp_session")
        return ret_handle

    @cafe.teststep('modify igmp session!')
    def modify_igmp(self, name, **kwargs):

        self._check_name(name)

        session_handle = self._get_handle(name)

        opts = {}
        opts.update(kwargs)

        return self.config_igmp(handle = session_handle, mode = 'modify', **opts)

    @cafe.teststep('delete igmp session!')
    def delete_igmp(self, name, **kwargs):

        self._check_name(name)
        session_handle = self._get_handle(name)
        opts = {}
        opts.update(kwargs)

        self.config_igmp(handle = session_handle, mode = 'delete', **opts)
        self._del_handle(ref=name, htype="igmp_session")

    @cafe.teststep('disble all igmp session!')
    def disable_all_igmp(self, port, **kwargs):
        # self._check_port(port)
        port_handle = self._get_handle(port.ref)

        return self.config_igmp(handle=port_handle, mode="disable_all", **kwargs)


    @cafe.teststep('create igmp querier!')
    def create_igmp_querier(self, name, port, igmp_version, **kwargs):
        self._check_name(name)
        self._check_port(port)
        port_handle = self._get_handle(port.ref)
        if igmp_version not in ('v2','v3'):
            raise ValueError("Only support IGMP version:[v2/v3]")

        opts = {
            'igmp_version' : igmp_version,
            'intf_ip_addr':'192.58.1.2',
            'neighbor_intf_ip_addr':'192.58.1.1',
        }
        opts.update(kwargs)

        res = self.config_igmp_querier(handle = port_handle, mode = 'create', **opts)
        m = re.search(r'(router\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create IGMP querier fail, Can't get handle!")

        self.logger.debug('Create IGMP querier success, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "igmp_querier")
        return ret_handle

    @cafe.teststep('modify igmp querier!')
    def modify_igmp_querier(self, name, **kwargs):
        self._check_name(name)
        querier_handle = self._get_handle(name)
        opts = {}
        opts.update(kwargs)

        return self.config_igmp_querier(handle = querier_handle, mode = 'modify', **opts)

    @cafe.teststep('delete igmp querier!')
    def delete_igmp_querier(self, name, **kwargs):
        self._check_name(name)
        querier_handle = self._get_handle(name)
        opts = {}
        opts.update(kwargs)
        self.config_igmp_querier(handle = querier_handle, mode = 'delete', **opts)
        self._del_handle(ref=name, htype="igmp_querier")

    @cafe.teststep('create multicast group!')
    def create_multicast_group(self, name, **kwargs):
        self._check_name(name)

        opts = {
            'num_groups' : 2,
            'ip_addr_start' : '228.0.1.0',
            'ip_addr_step' : '1',
            'ip_prefix_len' : 24,
        }
        opts.update(kwargs)

        res = self.config_multicast_group(mode = 'create', **opts)
        m = re.search(r'(ipv[46]group\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create Multicast group fail, Can't get handle!")

        self.logger.debug('Create multicast group success, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "multicast_group")
        return ret_handle

    @cafe.teststep('modify multicast group!')
    def modify_multicast_group(self, name, **kwargs):
        handle = self._get_handle(name)
        opts = {'handle' : handle}
        opts.update(kwargs)

        return self.config_multicast_group(mode = 'modify', **opts)

    @cafe.teststep('delete multicast group!')
    def delete_multicast_group(self, name):
        handle= self._get_handle(name)
        self.config_multicast_group(mode = 'delete', handle=handle)
        self._del_handle(ref=name, htype='multicast_group')

    @cafe.teststep('create multicast source!')
    def create_multicast_source(self, name, **kwargs):
        self._check_name(name)

        opts = {
            'num_sources' : 2,
            'ip_addr_start' : '128.0.1.0',
            'ip_addr_step' : '1',
            'ip_prefix_len' : 24,
        }
        opts.update(kwargs)

        res = self.config_multicast_source(mode = 'create', **opts)
        m = re.search(r'(multicastSourcePool\(\d+\))', res)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create Multicast source fail, Can't get handle!")

        self.logger.debug('Create multicast source success, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "multicast_source")
        return ret_handle

    @cafe.teststep('modify multicast source!')
    def modify_multicast_source(self, name, **kwargs):
        handle = self._get_handle(name)
        opts = {'handle' : handle}
        opts.update(kwargs)

        return self.config_multicast_source(mode = 'modify', **opts)

    @cafe.teststep('delete multicast source!')
    def delete_multicast_source(self, name):
        handle= self._get_handle(name)
        self.config_multicast_source(mode = 'delete', handle=handle)
        self._del_handle(ref=name, htype='multicast_source')

    @cafe.teststep('create igmp group!')
    def create_igmp_group(self, name, session_name, group_pool_name, source_pool_name=None, **kwargs):
        self._check_name(name)
        self._check_name(session_name)
        self._check_name(group_pool_name)

        session_handle = self._get_handle(session_name)
        group_pool_handle = self._get_handle(group_pool_name)

        opts = {
            'session_handle' : session_handle,
            'group_pool_handle'  : group_pool_handle,
        }

        if source_pool_name:
            self._check_name(source_pool_name)
            source_pool_handle = self._get_handle(source_pool_name)
            opts.update({'source_pool_handle' : source_pool_handle})

        opts.update(kwargs)

        res = self.config_igmp_group(mode = 'create', **opts)
        m = re.search(r'(igmpgroupmembership\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create IGMP group fail, Can't get handle!")

        self.logger.debug('Create multicast source success, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "igmp_group")
        return ret_handle

    @cafe.teststep('modify igmp group!')
    def modify_igmp_group(self, name, session_name=None, group_pool_name=None, source_pool_name=None, **kwargs):
        handle = self._get_handle(name)
        opts = {'handle' : handle}
        if session_name:
            session_handle = self._get_handle(session_name)
            opts.update({'session_handle' : session_handle})

        if group_pool_name:
            group_pool_handle = self._get_handle(group_pool_name)
            opts.update({'group_pool_handle' : group_pool_handle})

        if source_pool_name:
            source_pool_handle = self._get_handle(source_pool_name)
            opts.update({'source_pool_handle' : source_pool_handle})

        opts.update(kwargs)
        return self.config_igmp_group(mode = 'modify', **opts)

    @cafe.teststep('delete igmp group!')
    def delete_igmp_group(self, name):
        handle= self._get_handle(name)
        self.config_igmp_group(mode = 'delete', handle=handle)
        self._del_handle(ref=name, htype='igmp_group')

    @cafe.teststep('control igmp!')
    def control_igmp(self, mode, name, **kwargs):
        session_handle= self._get_handle(name)
        return super(STCDriver, self).control_igmp(mode,
                                                   session_handle, **kwargs)

    @cafe.teststep('get igmp hosts stats!')
    def get_igmp_stats_by_key_regx(self, port, key):
        port_handle= self._get_handle(port.ref)
        super(STCDriver, self).get_igmp_stats(port_handle)
        self.get_stats()
        self._update_app_result(self.stats)
        return self.get_stats_by_key_regx(key)

    @cafe.teststep('control igmp querier!')
    def control_igmp_querier(self, mode, name, **kwargs):
        handle= self._get_handle(name)
        return super(STCDriver, self).control_igmp_querier(mode,
                                                    handle, **kwargs)

    @cafe.teststep('get igmp querier stats!')
    def get_igmp_querier_stats_by_key_regx(self, port, key):
        port_handle= self._get_handle(port.ref)
        super(STCDriver, self).get_igmp_querier_stats(port_handle)
        self.get_stats()
        self._update_app_result(self.stats)
        return self.get_stats_by_key_regx(key)

    def packet_config_buffers(self, port_handle, action='stop', **kwargs):
        '''
        Purpose:
            Defines how Spirent HLTAPI will manage the buffers for packet
            capturing.
        Args:
            port_handle:<handle>
            action:{wrap|stop}
            Note:action not supported with IxTclNetwork and warning will be printed on stdout if this parameter is used
        '''

        port_h = self.get_port_handle(port_handle)
        option = {}

        option.update(**kwargs)

        return self._conf_cap_buffer(port_h, action, **option)

    def packet_config_filter(self, port_handle, mode='add', **kwargs):
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

    def packet_config_triggers(self, port_handle, mode, **kwargs):
        '''
        Purpose:
            Defines the condition (trigger) that will start or stop packet capturing.
            By default, Spirent HLTAPI captures all data and control plane packets
            that it sends and all data plane packets that it receives.
        Args:
            port_handle:<handle>
            mode  (optional):{add | remove}
        '''

        port_h = self.get_port_handle(port_handle)
        option = {'exec' : 'start'
                  }
        option.update(**kwargs)

        return self._conf_cap_triggers(port_h, mode, **option)

    def packet_control(self, portlist, action):
        '''
        Purpose:
            Starts or stops packet capturing.
        Args:
            portlist:<(port,port,port)>
            action:{start|stop}
        '''
        p_list=""

        if isinstance(portlist, (tuple, list)):
            for p in portlist:
                p_list += p.handle+" "
        else:
            p_list = portlist.handle

        return self._control_cap(p_list, action)

    def _check_index(self, index, router_handles):
        if int(index) >= len(router_handles):
            raise STCSessionException("Handle index is out of range, "
                                      "the range is [0-{}]".format(len(router_handles)-1))

    @cafe.teststep('create ospf router!')
    def create_ospf(self, name, port, **kwargs):

        self._check_name(name)
        self._check_port(port)

        port_handle = self._get_handle(port.ref)
        opts = {'session_type': 'ospfv2'}
        opts.update(kwargs)
        res = self._emulation_ospf_config(mode='create', handle=port_handle, **opts)
        m = re.search(r'return_handle: (.+)', res)
        if m:
            ret_handle = m.group(1).split()
            print ret_handle
        else:
            STCSessionException("Create OSPF router failed, Can't get handle!")

        self.logger.debug('Create OSPF router successfully, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "ospf")
        return ret_handle

    @cafe.teststep('modify ospf router!')
    def modify_ospf(self, name, index=0, **kwargs):
        self._check_name(name)
        router_handles = self._get_handle(name)
        self._check_index(index, router_handles)
        opts = {}
        opts.update(kwargs)
        return self._emulation_ospf_config(handle=router_handles[int(index)], mode='modify', **opts)

    @cafe.teststep('delete ospf router!')
    def delete_ospf(self, name, index=None):
        self._check_name(name)
        router_handles = self._get_handle(name)

        if index:
            self._check_index(index, router_handles)
            handle = router_handles.pop(int(index))
            self._emulation_ospf_config(handle=handle, mode='delete')
        else:
            while router_handles:
                handle = router_handles.pop()
                self._emulation_ospf_config(handle=handle, mode='delete')

        if not router_handles:
            self._del_handle(ref=name, htype="ospf")


    @cafe.teststep('create ospf_topology_route!')
    def create_ospf_topology_route(self, name, router_name, topo_type, index=0, lsa_name=None, **kwargs):
        self._check_name(name)
        self._check_name(router_name)
        router_handles = self._get_handle(router_name)
        self._check_index(index, router_handles)
        self.topology_route_info[name] = [router_handles[int(index)], topo_type]
        opts = {
                'type': topo_type,
                'handle': self.topology_route_info[name][0]
               }
        opts.update(kwargs)

        if topo_type == 'network':
            self._check_name(lsa_name)
            lsa_handle = self._get_handle(lsa_name)
            opts.update({'net_dr': lsa_handle})

        res = self._emulation_ospf_topology_route_config(mode='create', **opts)
        m = re.search(r'return_handle: ({}\d+)'.format(self.topo_route_handle_reg[topo_type]), res, re.I)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create OSPF topology router failed, Can't get handle!")

        self.logger.debug('Create OSPF topology router successfully, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "ospf_topology_route")
        return ret_handle

    @cafe.teststep('modify ospf_topology_route!')
    def modify_ospf_topology_route(self, name, **kwargs):
        self._check_name(name)
        opts = {
               'handle': self.topology_route_info[name][0],
               'elem_handle': self._get_handle(name),
               'type': self.topology_route_info[name][1],
               }
        opts.update(kwargs)
        return self._emulation_ospf_topology_route_config(mode='modify', **opts)

    @cafe.teststep('delete ospf_topology_route!')
    def delete_ospf_topology_route(self, name):
        self._check_name(name)
        opts = {
            'handle': self.topology_route_info[name][0],
            'elem_handle': self._get_handle(name),
            'type': self.topology_route_info[name][1],
        }
        self._emulation_ospf_topology_route_config(mode='delete', **opts)
        self._del_handle(ref=name, htype="ospf_topology_route")
        del self.topology_route_info[name]

    @cafe.teststep('create ospf_lsa!')
    def create_ospf_lsa(self, name, router_name, type, index=0, **kwargs):
        self._check_name(name)
        self._check_name(router_name)
        router_handles = self._get_handle(router_name)
        self._check_index(index, router_handles)
        opts = {
            'type': type,
            'handle': router_handles[int(index)]
        }
        opts.update(kwargs)
        res = self._emulation_ospf_lsa_config(mode='create', **opts)
        m = re.search(r'return_handle: ({}\d+)'.format(self.lsa_handle_reg[type]), res, re.I)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create OSPF topology router failed, Can't get handle!")

        self.logger.debug('Create OSPF topology router successfully, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "ospf_lsa")
        return ret_handle

    @cafe.teststep('modify ospf_lsa!')
    def modify_ospf_lsa(self, name, **kwargs):
        self._check_name(name)
        opts = {
            'lsa_handle': self._get_handle(name),
        }
        opts.update(kwargs)
        return self._emulation_ospf_lsa_config(mode='modify', **opts)

    @cafe.teststep('delete ospf_lsa!')
    def delete_ospf_lsa(self, name):
        self._check_name(name)
        opts = {
            'lsa_handle': self._get_handle(name),
        }
        self._emulation_ospf_lsa_config(mode='delete', **opts)
        self._del_handle(ref=name, htype="ospf_lsa")

    @cafe.teststep('control ospf router!')
    def control_ospf(self, name, mode, index=None, **kwargs):
        self._check_name(name)
        router_handles = self._get_handle(name)
        if index:
            self._check_index(index, router_handles)
            router_handle = router_handles[int(index)]
            self._emulation_ospf_control(handle=router_handle, mode=mode, **kwargs)
        else:
            for handle in router_handles:
                self._emulation_ospf_control(handle=handle, mode=mode, **kwargs)

    @cafe.teststep('get ospf info!')
    def get_ospf_info(self, name, key_or_key_list, version='ospfv2', index=0):
        self._check_name(name)
        router_handles = self._get_handle(name)
        self._check_index(index, router_handles)
        router_handle = router_handles[int(index)]
        res = self._emulation_ospf_info(handle=router_handle, mode='stats', version=version)
        self.logger.debug('%s' % res)

        r = re.findall(r'{(.*?)\s+(.*?)}', res)
        stats = {l[0]: l[1] for l in r if l[0] != 'status'}

        if key_or_key_list is None:
            return stats
        elif isinstance(key_or_key_list, (str, unicode)):
            key = str(key_or_key_list)
            return {key: stats[str(key)]}
        elif isinstance(key_or_key_list, list):
            return {str(key): stats[str(key)] for key in key_or_key_list}
        else:
            raise ValueError('invalid key %s' % key_or_key_list)

    @cafe.teststep('get ospf router info!')
    def get_ospf_router_info(self, name, key_or_key_list, index=0):
        self._check_name(name)
        router_handles = self._get_handle(name)
        self._check_index(index, router_handles)
        router_handle = router_handles[int(index)]
        self._emulation_ospf_router_info(handle=router_handle)
        self.get_stats(reset=True)

        if key_or_key_list is None:
            return self.stats
        elif isinstance(key_or_key_list, (str, unicode)):
            return self.get_stats_by_key_regex(str(key_or_key_list))
        elif isinstance(key_or_key_list, list):
            ret = {}
            for key in key_or_key_list:
                ret.update(self.get_stats_by_key_regex(str(key)))
            return ret
        else:
            raise ValueError('invalid key %s' % key_or_key_list)

    def check_all_neighboring_routers_fully_adjacent(self, name_list):
        for name in name_list:
            count = len(self._get_handle(name))
            for i in range(count):
                info = self.get_ospf_info(name, 'adjacency_status', index=i)
                status = info.get('adjacency_status', 'None')
                self.logger.debug('router name is %s, index is %s(%s), adjacency_status is %s'
                                  % (name, i, count, status))
                if status != 'FULL':
                    return False

        return True

    def packet_stats(self, port,filename='default',format='pcap', **kwargs):
        '''
        Purpose:
            Returns statistical information about each packet associated with the specified
            port(s). Statistics include the connection status and number and type of messages
            sent and received from the specified port.
            Packet Capture Functions
        Args:
            port:<port>
            format  (optional):{pcap | var}
            filename  (optional):<filename>
        '''

        option = {}
        # if filename:
        #     option['filename'] = filename

        option.update(**kwargs)

        return self._conf_cap_stats(port,  filename, format, **option)


    @cafe.teststep('create bgp config!')
    def create_bgp_config(self, name, port, **kwargs):
        self._check_name(name)
        self._check_port(port)

        opts = {
            'count': '1',
            'port_handle': port.handle
        }
        opts.update(kwargs)

        res = self._emulation_bgp_config(mode = 'enable', **opts)
        m=re.search(r"ret\:([\w\s]+)\:",res)
        if m:
            ret_handle = m.group(1).split()
        else:
            STCSessionException("Create BGP config failed, Can't get handle!")

        self.logger.debug('Create BGP config success, handle [{}]'.format(ret_handle))
        index=0
        for h in ret_handle:
            n=name+str(index)
            index=index+1
            self._set_handle(n, n, h, "bgp")

        return ret_handle

    @cafe.teststep('modify bgp config!')
    def modify_bgp_config(self, name, index=0, **kwargs):
        name=name+str(index)
        self._check_name(name)
        router_handle = self._get_handle(name)
        opts = {'handle' : router_handle}
        opts.update(kwargs)

        self._emulation_bgp_config(mode = 'modify', **opts)
        return True

    @cafe.teststep('delete bgp config!')
    def delete_bgp_config(self, name, index=0, **kwargs):
        name=name+str(index)
        self._check_name(name)
        router_handle = self._get_handle(name)
        opts = {'handle' : router_handle}
        opts.update(kwargs)

        self._emulation_bgp_config(mode = 'reset', **opts)
        self._del_handle(name,'bgp')
        return True

    @cafe.teststep('create create bgp route config!')
    def create_bgp_route_config(self, name, router_name, index=0, **kwargs):
        self._check_name(name)
        router_name=router_name+str(index)
        self._check_name(router_name)
        router_handle = self._get_handle(router_name)

        opts = {
            'handle' : router_handle
        }
        opts.update(kwargs)

        res = self._emulation_bgp_route_config(mode = 'add', **opts)
        m=re.search(r"ret\:([\w\s]+)\:",res)
        if m:
            ret_handle = m.group(1).split()
        else:
            STCSessionException("Create BGP route config failed, Can't get handle!")

        self.logger.debug('Create BGP route config success, handle [{}]'.format(ret_handle))
        index=0
        for h in ret_handle:
            n=name+str(index)
            index=index+1
            self._set_handle(n, n, h, "bgp_route")

        return ret_handle

    @cafe.teststep('modify bgp route config!')
    def modify_bgp_route_config(self, name, index=0,**kwargs):
        name=name+str(index)
        self._check_name(name)
        route_handle = self._get_handle(name)
        opts = {'route_handle' : route_handle}
        opts.update(kwargs)

        self._emulation_bgp_route_config(mode = 'modify', **opts)
        return True

    @cafe.teststep('delete bgp route config!')
    def delete_bgp_route_config(self, name, index=0,**kwargs):
        name=name+str(index)
        self._check_name(name)
        route_handle = self._get_handle(name)
        opts = {'route_handle' : route_handle}
        opts.update(kwargs)

        self._emulation_bgp_route_config(mode = 'remove', **opts)
        self._del_handle(name,'bgp_route')
        return True

    @cafe.teststep('get bgp route info by key!')
    def get_bgp_info_by_key(self, name, mode, key, index=0, **kwargs):
        name=name+str(index)
        self._check_name(name)
        router_handle = self._get_handle(name)
        opts = {'handle' : router_handle}
        opts.update(kwargs)

        self._emulation_bgp_info(mode, **opts)
        self.get_stats()
        res = self.get_stats_by_key_regex(key)
        return res

    @cafe.teststep('get bgp info by key!')
    def get_bgp_route_info_by_key(self, name, mode, key, index=0, **kwargs):
        name=name+str(index)
        self._check_name(name)
        router_handle = self._get_handle(name)
        opts = {'handle' : router_handle}
        opts.update(kwargs)

        self._emulation_bgp_route_info(mode, **opts)
        self.get_stats()
        res = self.get_stats_by_key_regex(key)
        return res

    @cafe.teststep('control bgp!')
    def control_bgp(self,port,mode,route_name=None,index=0, **kwargs):
        opts = {
                'handle' : port.handle
                }
        opts.update(kwargs)
        if route_name:
            route_name=route_name+str(index)
            self._check_name(route_name)
            route_handle = self._get_handle(route_name)
            opts['route_handle']=route_handle

        self._emulation_bgp_control(mode = mode, **opts)
        return True

    @cafe.teststep('create bgp route generator!')
    def create_bgp_route_generator(self, name, router_name, index=0, **kwargs):
        self._check_name(name)
        router_name=router_name+str(index)
        self._check_name(router_name)
        router_handle = self._get_handle(router_name)

        opts = {
            'handle' : router_handle
        }
        opts.update(kwargs)

        res = self._emulation_bgp_route_generator(mode = 'create', **opts)
        m = re.search(r'(bgproutegenparams\d+)', res)
        if m:
            ret_handle = m.group(1)
        else:
            STCSessionException("Create BGP route generator failed, Can't get handle!")

        self.logger.debug('Create BGP route generator success, handle [{}]'.format(ret_handle))
        self._set_handle(name, name, ret_handle, "bgp_route_generator")
        return ret_handle

    @cafe.teststep('modify bgp route generator!')
    def modify_bgp_route_generator(self, name, **kwargs):
        self._check_name(name)
        elem_handle = self._get_handle(name)
        opts = {'elem_handle' : elem_handle}
        opts.update(kwargs)

        self._emulation_bgp_route_generator(mode = 'modify', **opts)
        return True

    @cafe.teststep('delete bgp route generator!')
    def delete_bgp_route_generator(self, name, **kwargs):
        self._check_name(name)
        elem_handle = self._get_handle(name)
        opts = {'elem_handle' : elem_handle}
        opts.update(kwargs)

        self._emulation_bgp_route_generator(mode = 'delete', **opts)
        self._del_handle(name,'bgp_route_generator')
        return True

    def create_isis_router(self, name, port, area_id, system_id,
                           router_id, routing_level='L2', **kw):
        self._check_name(name)
        options = {'area_id': area_id,
                   'system_id': system_id,
                   'router_id': router_id,
                   'routing_level': routing_level}

        options.update(**kw)

        res = self._config_isis(port, 'create', **options)
        print res
        m = re.search(r"{handles :(.*)}", res)
        if m :
            handles = m.group(1).split()
            self._set_handle(name, name, handles, 'isis_router')
        else:
            raise STCConfigureISISError

    def modify_isis_router_by_index(self, name, index=0, **kw):

        self._check_name(name)
        handle = getattr(self, name).handle[int(index)]
        options = {'handle': handle}
        options.update(**kw)
        self._config_isis(None, 'modify', **options)

    def delete_isis_router_by_index(self, name, index=0):
        self._check_name(name)
        handle = getattr(self, name).handle[int(index)]
        options = {'handle': handle}
        self._config_isis(None, 'delete', **options)
        getattr(self, name).handle[int(index)] = None
        if len(filter(lambda x: x != None, getattr(self, name).handle)) == 0:
            self._del_handle(name, 'isis_router')

    def create_isis_topology_route(self, name, isis_name, index,
                                   topo_type, router_id, router_system_id,
                                   router_routing_level, **kw):
        self._check_name(name)

        isis_handle = getattr(self, isis_name).handle[int(index)]

        options = {'type': topo_type,
                   'router_id': router_id,
                   'router_system_id': router_system_id,
                   'router_routing_level': router_routing_level}

        options.update(**kw)
        res = self._config_isis_topology_route(isis_handle, 'create', **options)

        m = re.search(r"{handle :(isisRouteHandle\d+)}", res)
        if m:
            handle = m.group(1)
            self._set_handle(name, name, handle, 'isis_topology_route')
        else:
            raise STCConfigureISISTopologyRouteError

    def modify_isis_topology_route(self, name, **kw):

        self._check_name(name)
        topo_handle = getattr(self, name).handle

        options = {'elem_handle': topo_handle}

        options.update(**kw)
        self._config_isis_topology_route(None, 'modify', **options)

    def delete_isis_topology_route(self, name):

        self._check_name(name)
        topo_handle = getattr(self, name).handle

        options = {'elem_handle': topo_handle}

        self._config_isis_topology_route(None, 'delete', **options)
        self._del_handle(name, 'isis_topology_route')

    def create_isis_lsp_generator(self, name, isis_name, index, **kw):

        self._check_name(name)
        options = {}
        options.update(**kw)
        isis_handle = getattr(self, isis_name).handle[int(index)]
        res = self._config_isis_lsp_generator(isis_handle, 'create', **options)

        m = re.search(r"{handle :(isislspgenparams\d+)}", res)
        if m:
            handle = m.group(1)
            self._set_handle(name, name, handle, 'isis_lsp_generator')
        else:
            raise STCConfigureISISLspGeneratorError

    def modify_isis_lsp_generator(self, name, **kw):

        self._check_name(name)
        lsp_handle = getattr(self, name).handle

        options = {'elem_handle': lsp_handle}

        options.update(**kw)
        self._config_isis_lsp_generator(None, 'modify', **options)

    def delete_isis_lsp_generator(self, name):

        self._check_name(name)
        lsp_handle = getattr(self, name).handle

        options = {'elem_handle': lsp_handle}

        self._config_isis_lsp_generator(None, 'delete', **options)
        self._del_handle(name, 'isis_lsp_generator')

    def control_isis(self, name, index, mode, **kwargs):
        self._check_name(name)
        lsp_handle = getattr(self, name).handle[int(index)]

        return self._control_isis(lsp_handle, mode, **kwargs)

    def get_isis_info_by_key(self, router_name, index, key):

        self._check_name(router_name)
        isis_router_handle = getattr(self, router_name).handle[int(index)]

        self._isis_info(isis_router_handle)
        self.get_stats()
        res = self.get_stats_by_key_regex(key=key)

        return res

if __name__ == "__main__":
    pass
