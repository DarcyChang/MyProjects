__author__ = 'jcao'

from pyshark.packet.packet import Packet
import pyshark
from pyshark.capture import file_capture
from time import sleep
import random
from cafe.core.logger import CLogger as logger


_module_logger = logger(__name__)

debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

class TsharkSessionException(Exception):

    def __init__(self, msg=""):
        _module_logger.exception(msg)

class tshark(object):
    """
    The procedure used for captured pcap file(packet) analysis
    """
    def __init__(self):
        self.pcap = None
        pass

    def __del__(self):
        if self.pcap:
            self.close_file()

    def load_file(self, filename, filter):
        import time

        self.close_file()

        try:
            self.pcap = pyshark.FileCapture(filename, display_filter=filter)
            self.pcap.load_packets()
            return len(self.pcap)
        except Exception as e:
            print e
            time.sleep(6)
            print 'Retry to load pcap file.'
            self.pcap = pyshark.FileCapture(filename, display_filter=filter)
            self.pcap.load_packets()
            return len(self.pcap)

    def close_file(self):
        if not self.pcap:
            return

        # if we not close the event loop there will be many fd in current process
        # and will raise an exception after reach the file limit
        if not self.pcap.eventloop.is_closed():
            try:
                self.pcap.eventloop.close()
            except RuntimeError as e:
                if e.message.__contains__("Event loop is closed"):
                    pass

        self.pcap.clear()
        self.pcap.close()

    def reset_filter(self, filter):
        '''
        Reset previous filter
        '''

        self.pcap.clear()
        self.pcap.display_filter = filter
        self.pcap.load_packets()
        return len(self.pcap)

    def get_total_packet_count(self):

        # self.cnt = 0
        # for i in self.pcap:
        #     self.cnt += 1
        # return self.cnt
        return len(self.pcap)


    def get_packets_list(self):
        """
        get packets with a list format.

        return:
            packet list

        Example:
            >>> filename = "demo2.pcap"
            >>> filter = "bootp"
            >>> c = tshark(filename,filter)
            >>> y = c.get_packets_list()
            >>> print(y)
            ... [<UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>, <UDP/BOOTP Packet>]

        """
        # self.pkts = []
        # for i in self.pcap:
        #     self.pkts.append(i)
        # return self.pkts
        return self.pcap


    def verify_outer_vlan(self, vlan):

        for i in self.pcap:
            vlans = i.get_multiple_layers('vlan')
            if len(vlans) >= 1 and vlans[0].id == str(vlan):
                continue
            else:
                raise TsharkSessionException('Outer VLAN %s is incorrect!'% vlans[0].id)
        return True

    def verify_inner_vlan(self, vlan):

        for i in self.pcap:
            vlans = i.get_multiple_layers('vlan')
            if len(vlans) > 1 and vlans[1].id == str(vlan):
                continue
            else:
                raise TsharkSessionException('Inner VLAN %s is incorrect!'% vlans[1].id)
        return True

    def verify_ourter_pbit(self, priority):

        for i in self.pcap:
            vlans = i.get_multiple_layers('vlan')
            if len(vlans) >= 1 and vlans[0].priority == str(priority):
                continue
            else:
                raise TsharkSessionException('Outer pbit %s is incorrect!'% vlans[0].priority)
        return True

    def verify_inner_pbit(self, priority):

        for i in self.pcap:
            vlans = i.get_multiple_layers('vlan')
            if len(vlans) > 1 and vlans[1].priority == str(priority):
                continue
            else:
                raise TsharkSessionException('Inner pbit %s is incorrect!'% valns[1].priority)
        return True


    def verify_udp_src_port(self, src_port):

        for i in self.pcap:
            if int(i.udp.srcport) != src_port:
                debug("Not all captured packets source port equal %s, source port %s received also" % (src_port, i.udp.srcport))
                raise TsharkSessionException('UDP src port incorrect!')
        info("All captured source port equal %s" % src_port)
        return True

    def verify_bootp_option(self, option_key, option_value):

        for item in self.pcap:
            if not hasattr(item, 'bootp') \
               or not hasattr(item.bootp, option_key):
                raise ValueError('Option key %s was not contained by all packets.' % (option_key))

        values = map(lambda x: x.bootp.get_field(option_key), self.pcap)

        if (len(set(values))) > 1:
            raise ValueError('Option value was not the same in all packets.')
        if not values[0] == option_value:
            raise ValueError('Option value was not the equal to %s' % (option_value))
        return True

    def verify_udp_dst_port(self, dst_port):

        for i in self.pcap:
            if int(i.udp.dstport) != dst_port:
                debug("Not all captured packets destination port equal %s, destination port %s received also" % (dst_port, i.udp.dstport))
                raise TsharkSessionException('UDP dst incorrect!')
        info("All captured destination port equal %s" % dst_port)
        return True

    def verify_highest_layer(self, layer_name):

        for i in self.pcap:
            if i.highest_layer != layer_name:
                debug("Highest layer is NOT same as expected: %s" % layer_name)
                raise TsharkSessionException('Highest layer incorrect!')
        info("Highest layer is same as expected: %s" % layer_name)
        return True

    def get_dhcp_v4_agent_circuit_id(self):

        c_ids = set(map(lambda x :
                        x.bootp.option_agent_information_option_agent_circuit_id,
                        self.pcap)
                    )
        if len(c_ids) > 1:
            raise ValueError('Not all captured packages have the same circuit id')
        return c_ids.pop().replace(':', '').decode('hex')

    def get_dhcp_v4_agent_remote_id(self):

        r_ids = set(map(lambda x:
                        x.bootp.option_agent_information_option_agent_remote_id,
                        self.pcap))
        if len(r_ids) > 1:
            raise ValueError('Not all captured packages have the same remote id')

        return r_ids.pop().replace(':', '').decode('hex')

    def get_dhcpv6_interface_id(self):

        iids = list()
        for cap in self.pcap:
            shows = filter(lambda x: 'Interface-ID:' in x.show, cap.dhcpv6._get_all_fields_with_alternates())
            if len(shows) != 1:
                raise ValueError('Failed to find interface id.')
            iids.append(shows[0])
        if (len(set(map(lambda x: x.show, iids))) != 1):
            raise ValueError('Faild to find interface id.')

        return iids[0].binary_value

    def get_dhcpv6_remote_id(self):

        rids = list()
        for cap in self.pcap:
            shows = filter(lambda x : 'Remote-ID:' in x.show, cap.dhcpv6._get_all_fields_with_alternates())
            if len(shows) != 1:
                raise ValueError('Faild to find remote id.')
            rids.append(shows[0])

        if (len(set(map(lambda x: x.show, rids))) != 1 ):
            raise ValueError('Faild to find remote id.')
        return rids[0].binary_value

    def get_bootp_option61_raw_value(self):
        opts = set()
        for cap in self.pcap:
            field = filter(lambda x: x.show == '61',
                           cap.bootp.get_field_by_showname('Option').fields)[0]
            opts.add(field.raw_value)
        if len(opts) != 1:
            raise ValueError('Faild to find bootp option 61')
        return opts.pop()

    def should_not_contain_dhcp_option82(self):

        for cap in self.pcap:
            if hasattr(cap, 'bootp'):
                if hasattr(cap.bootp,
                           'option_agent_information_option_agent_circuit_id')\
                           or hasattr(cap.bootp,
                                      'option_agent_information_option_agent_remote_id'):
                    raise ValueError('Contains DHCP v4 Option 82')
            elif hasattr(cap, 'dhcpv6'):
                all_fields = cap.dhcpv6._get_all_fields_with_alternates()
                if len(filter(lambda x: 'Interface-ID:' in x.show \
                              or 'Remote-ID:' in x.show, all_fields)) > 0:
                    raise ValueError('Contains DHCP v6 Option 82')
            else:
                raise ValueError('Invalid DHCP package.')

        return True

    def should_contain_param_requests_in_dhcp_option55(self, *params):

        if len(self.pcap) == 0:
            raise ValueError('There is no packets to check.')
        param_set = set(params)
        missing_set = set()
        for cap in self.pcap:
            option55 = set(map(lambda x: x.show,
                               cap.bootp.option_request_list_item.all_fields))
            if not param_set.issubset(option55):
                #raise ValueError('Not all params in option55 requests list.')
                diff = param_set.difference(set(cap.bootp.option_request_list_item.all_fields))
                missing_set.update(diff)
        else:
            if len(missing_set) == 0:
                return True
            else:
                raise ValueError('Not all params in option55 requestslist: %s'
                                 % (reduce(lambda x, y: str(x)+' '+str(y), missing_set)))

    def get_pppoe_tags_vender_id(self):

        ids = set(map(lambda x: x.pppoed.tags_vendor_id, self.pcap))

        if len(ids) != 1:
            raise ValueError('Not all vendor id are the same.')
        return ids.pop()

    def get_pppoe_tags_circuit_id(self):

        ids = set(map(lambda x:x.pppoed.tags_circuit_id, self.pcap))

        if len(ids) != 1:
            raise ValueError('Not all circuit id are the same.')
        return ids.pop()

    def get_pppoe_tags_remote_id(self):

        ids = set(map(lambda x: x.pppoed.tags_remote_id, self.pcap))

        if len(ids) != 1:
            raise ValueError('Not all remote id are the same.')

        return ids.pop()

    def clear(self):

        self.pcap.clear()
        info("Done!")

    def test(self):

        for i in self.pcap:
            info(i.ip.src)

if __name__ == "__main__":

    #pass


    filename = "demo2.pcap"

    filter = "udp.srcport == 67"

    cap = tshark()

    cap.load_file(filename, filter)

    print cap.verify_ourter_vlan(70)

    # a = cap.get_total_packet_count()
    # print(a)
    #
    # b = cap.get_packets_list()
    # print(b)
    #
    # c = cap.verify_ourter_vlan(20)
    # print(c)
    #
    # d = cap.verify_ourter_pbit(0)
    # print(d)
    #
    # e = cap.verify_ourter_pbit(7)
    # print(e)
    #
    # f = cap.verify_udp_dst_port(68)
    # print(f)
    #
    # g = cap.verify_highest_layer("bootp")
    # print("=========>%s" % g)
