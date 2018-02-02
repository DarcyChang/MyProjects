__author__ = 'alu'

from cafe.equipment.ixia.cixia import CIXIA
from caferobot.trafficgen.trafficgen import TrafficGenerator as tg
from cafe.core.signals import IXIA_SESSION_ERROR
from cafe.app.driver.ixia import IXIADriver
from cafe.core.logger import CLogger as Logger
import cafe
from time import sleep
import re

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

class IXIAException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=IXIA_SESSION_ERROR)


class IXIABase(object):

    def __init__(self,session):

        self.tg = tg()
        self.tg_session = session
        self.logger=Logger()
        pass

    # def connect_host(self):
    #     Result = True
    #     r = self.ixia.enable_test_log(self.log_path)
    #     self.logger.info("Connect to host:%s" % r)
    #     if r is "ERROR":
    #         Result = False
    #     return Result
    #
    # def connect_chassis(self):
    #     Result = True
    #     portlist = "%s %s" %(self.client_port,self.server_port)
    #     r = self.ixia.connect_to_chassis(self.chassis_ip,portlist)
    #     self.logger.info("Connect to chassis:%s" % r)
    #     if r is "ERROR":
    #         Result = False
    #     return Result

    def ixia_config_l3_staticintf(self,name,port,mode,**data):

        option ={
                "vlan":           "1",
                "vlan_id":              "1"
        }
        if mode == "WAN":
            intf_ip_addr = data["DHCPCAddrStart"]
            src_mac_addr = data["StaticMAC1"]
        else:
            if data.has_key("STATICADDRESS"):
                intf_ip_addr=data["STATICADDRESS"]
            src_mac_addr = data["StaticMAC2"]
            gateway = data["Gateway"]
            option["vlan"] = "1"
            option["vlan_id"] = data["InVlanSwitch"]

        #handle = self.ixia.conf_interface(self.client_port,**option)
        handle=self.tg.tg_create_static_host_on_port(self.tg_session, name, port,
                                      src_mac_addr, intf_ip_addr, "255.255.255.0",
                                      gateway, **option)
        if "ERROR" in handle:
            return False
        else:
            # interfacehandle = handle.split()[-1]
            # self.logger.info("Static Interface handle: %s" %interfacehandle)
            # return interfacehandle
            return True

    def ixia_config_mvrintf(self,name, port,
                                      src_mac_addr, intf_ip_addr, net_mask,
                                      gateway,**data):

        option ={
                "vlan_id":              "40",
                "vlan":                 "1"
        }
        if data.has_key("MVREnable"):
            if data["MVREnable"] == "1":
                option["vlan_id"] = data["MVR_VLAN"]

            #handle = self.ixia.conf_interface(self.server_port,**option)
            Handle = self.tg.tg_create_static_host_on_port(self.tg_session, name, port,
                                      data["src_mac_addr"], data["intf_ip_addr"], data["netmask"],
                                      data["gateway"],**option)
            if "ERROR" in Handle:
                return False
            else:
                # interfacehandle = handle.split()[-1]
                # self.logger.info("Interface handle: %s" %interfacehandle)
                # return interfacehandle
                return True
        else:
            return True

    def ixia_config_dhcps(self,name,port,**data):
        option ={
                "encapsulation":        "ethernet_ii_vlan",
                "ip_address":           "10.20.100.1",
                "vlan_id":              "40",
                "vlan_id_repeat":       "0",
                "ip_version":           "4",
                "local_mac":            "0000.0022.2221",
                "ipaddress_pool":       "10.20.100.2",
                "ipaddress_pool_step":  "0.0.0.1",
                "ipaddress_count":      "1",
                "ip_gateway":           "10.20.100.1"
        }
        option["encapsulation"] = data["IXIA_encapsulation"]
        option["vlan_id"] = data["OutSVLAN"]
        option["vlan_user_priority"] = data["OutSpbit"]
        option["ip_address"] = data["DHCPSAddress"]
        option["ipaddress_pool"] = data["DHCPCAddrStart"]
        option["ipaddress_count"] = data["DHCPCAddrCount"]
        option["ip_gateway"] = data["DHCPSAddress"]
        option["local_mac"] = data["DHCPSMAC"]

        if option.has_key("encapsulation"):
            if option["encapsulation"]== "ethernet_ii_qinq":
                option["vlan_id_inner"] = data["OutCVLAN"]
                option["vlan_user_priority_inner"] = data["OutCpbit"]

        handle = self.tg.tg_create_dhcp_server_on_port(self.tg_session, name, port, **option)
        # if "ERROR" in handle:
        #     return False
        # else:
        #     # dhcp_server_handle = handle.split()[-1]
        #     # self.logger.info("Dhcp Server handle: %s" %dhcp_server_handle)
        #     return True

    def ixia_control_dhcp_server(self,name,action):
        res=self.tg.tg_control_dhcp_server(self.tg_session,name,action)
        # if "ERROR" in res:
        #     return False
        # else:
        #     return True

    def ixia_control_dhcp_client(self,name,action):
        res=self.tg.tg_control_dhcp_client(self.tg_session,name,action)
        # if "ERROR" in res:
        #     return False
        # else:
        #     return True

    def ixia_control_pppox_by_name(self,name,action):
        res=self.tg.tg_control_pppox_by_name(self.tg_session,name,action)
        # if "ERROR" in res:
        #     return False
        # else:
        #     return True

    def ixia_control_igmp(self,name,action):
        res=self.tg.tg_control_igmp(self.tg_session,name,action)
        # if "ERROR" in res:
        #     return False
        # else:
        #     return True

    def ixia_control_traffic(self,portname,action):
        res=self.tg.tg_control_traffic(self.tg_session,portname,action)
        # if "ERROR" in res:
        #     return False
        # else:
        #     return True

    def ixia_config_dhcpc_basic(self):
        optionBasic = {
                "lease_time": "300",
                "version": "ixnetwork",
                "reset": ""
             }
        handle = self.tg.conf_dhcp_client_basic(self.client_port,"create", **optionBasic)
        if "ERROR" in handle:
            return False
        else:
            handle= handle.split()[-1]
            self.logger.info("DHCP client basic handle: %s" %handle)
            return handle

    def ixia_config_dhcpc(self,name, port,**data):

        optionGroup = {
              "mac_addr":      "00.00.22.15.11.11",
              "mac_addr_step": "00.00.00.00.00.01",
              "encap":         "ethernet_ii_vlan",
              "vlan_id":       "40",
              "vlan_id_step":  "0",
              "vlan_id_count": "1",
              "version":       "ixnetwork",
              "dhcp_range_param_request_list": "{1 3 58 59}"
             }

              # "num_sessions":  "1",
        optionGroup["vlan_id"] = data["InVlanSwitch"]
        optionGroup["mac_addr"] = data["IXIAC_mac_addr"]

        #r = self.ixia.conf_dhcp_client_group(handle,"create",**optionGroup)
        res=self.tg.tg_create_dhcp_client_on_port(self.tg_session, name, port, **optionGroup)
        if "ERROR" in res:
            return False
        else:
            # dhcp_client_group_handle = r.split()[-1]
            # self.logger.info("DHCP client group handle: %s" %dhcp_client_group_handle)
            # return  dhcp_client_group_handle
            return True

    def ixia_config_pppserver(self,name,port,**data):

        option = {
              "vlan_id":       "40",
              "vlan_id_step":  "0",
              "vlan_id_count": "1",
              "ppp_local_ip":  "172.225.10.1",
              "ppp_peer_ip":   "172.225.20.1",
              "auth_mode":     "pap_or_chap",
              "username":      "calix",
              "password":      "password"
             }

        option["mac_addr"] = data["DHCPSMAC"]
        option["vlan_user_priority"] = data ["OutSpbit"]
        option["username"]= data["PPPUsername"]
        option["password"] =data["PPPPassword"]
        option["ppp_local_ip"]=data["DHCPSAddress"]
        option["ppp_peer_ip"]=data["DHCPCAddrStart"]
        if data.has_key("IXIA_encapsulation"):
            if data["IXIA_encapsulation"]== "ethernet_ii_vlan":
                option["encap"] = data["IXIA_encapsulation"]
                option["vlan_id"] = data["OutSVLAN"]
            else:
                option["encap"]= "ethernet_ii_qinq"
                option["vlan_id_outer"] = data["OutSVLAN"]
                option["vlan_id"] = data["OutCVLAN"]

        self.logger.info("start to create the PPPOE SERVER Session")
        res=self.tg.tg_create_pppoe_server_on_port(self.tg_session, name, port, **option)
        # opt = self.ixia.dict2str(option)
        # res = self.ixia.tcl.command("CiHLT::pppoxConfig %s add {%s}" %(self.server_port,opt),timeout=20)[2]
        # self.logger.info("config PPPServer return:%s" %res)
        # result = res.split()[0]
        # self.logger.debug("Config PPPServer : %s" %result)
        # if "ERROR" in res:
        #     return False
        # else:
        #     # handle = res.split()[-1]
        #     # self.logger.info("PPPOE Server handle: %s" %handle)
        #     return  True

    def ixia_config_pppclient(self,name,port,**data):

        option = {
              "vlan_id":       "40",
              "auth_mode":     "pap_or_chap",
              "username":      "calix",
              "password":      "password"
             }
        option["vlan_id"] = data["InVlanSwitch"]
        option["mac_addr"] = data["StaticMAC2"]
        option["vlan_user_priority"] = data ["InPbit"]
        option["username"]= data["PPPUsername"]
        option["password"] =data["PPPPassword"]

        self.logger.info("start to create the PPPOE Client Session")
        # opt = self.ixia.dict2str(option)
        # res = self.ixia.tcl.command("CiHLT::pppoxConfig %s add {%s}" %(self.client_port,opt),timeout=20)[2]
        res=self.tg.tg_create_pppoe_client_on_port(self.tg_session, name, port, **option)
        # self.logger.info("config PPP Client return:%s" %res)
        # result = res.split()[0]
        # self.logger.debug("Config PPP Client : %s" %result)
        if "ERROR" in res:
            return False
        else:
            # handle = res.split()[-1]
            # self.logger.info("PPPOE Client handle: %s" %handle)
            # return  handle
            return True


    def ixia_create_l2_dhcp_traffic_us(self,dhcpserverhandle,dhcpclienthandle):
        option = {
                    "traffic_generator": 				"ixnetwork_540",
                    "circuit_endpoint_type": 			"ipv4",
                    "track_by": 					    "{dest_ip source_ip}",
                    "emulation_src_handle": 			"",
                    "emulation_dst_handle": 		    "",
                    "name": 						    "US_Traffic_UDP",
                    "endpointset_count": 			    "1",
                    "src_dest_mesh": 				    "one_to_one",
                    "route_mesh": 					    "one_to_one",
                    "rate_percent": 					"20",
                    "frame_size": 					    "512",
                    "tx_mode": 					        "advanced",
                    "transmit_mode": 				    "continuous",
                    "convert_to_raw": 				    "1",
                    "l4_protocol":                      "udp",
                    "udp_dst_port":                     "27000",
                    "udp_src_port":                     "28000"
                }
        option["emulation_src_handle"]= dhcpclienthandle
        option["emulation_dst_handle"]= dhcpserverhandle
        # r = self.ixia.conf_traffic("create",**option)
        # if "ERROR" in r:
        #     return False
        # else:
        #     return True
        self.logger.info("create traffic is in progress")
        #return self._ixia_send_tclcmd("CiHLT::trafficConfig","create",**option)
        r = False
        for i in range(1,5):
            r = self._ixia_send_tclcmd("CiHLT::trafficConfig","create",1,**option)
            if r:
                break
            else:
                #self.ixia_controll_start_allprotocols()
                sleep(30)
        return r

    def ixia_create_bound_tagged_stream(self,stream_name,port,stream_to_bounder,stream_from_bounder,mode,**data):
        option = {
                    "circuit_endpoint_type": 			"ipv4",
                    "endpointset_count": 			    "1",
                    "src_dest_mesh": 				    "one_to_one",
                    "route_mesh": 					    "one_to_one",
                    "rate_percent": 					"20",
                    "frame_size": 					    "512",
                    "tx_mode": 					        "advanced",
                    "transmit_mode": 				    "continuous",
                    "convert_to_raw": 				    "1",
                    "l4_protocol":                      "udp",
                    "udp_dst_port":                     "27000",
                    "udp_src_port":                     "28000"
                }
        if mode == "us":
            vlan_id =data["InVlanSwitch"]
            vlan_user_priority=data["InPbit"]
            #option["encapsulation"] = data["IXIA_encapsulation"]
        else:
            vlan_id =data["OutSVLAN"]
            vlan_user_priority=data["OutSpbit"]
        if data.has_key("OutCVLAN"):
            if data["OutCVLAN"]!= "0" and mode == "ds":
                    vlan_id =data["OutCVLAN"]
                    vlan_user_priority=data["OutCpbit"]
                    vlan_id_outer =data["OutSVLAN"]
                    vlan_outer_user_priority=data["OutSpbit"]
                    res=self.tg.tg_create_bound_double_tagged_stream_on_port(self.tg_session,stream_name, port,stream_to_bounder,stream_from_bounder,vlan_id,vlan_user_priority,vlan_id_outer,vlan_outer_user_priority,l2_encap='ethernet_ii',**option)

            else:
                res=self.tg.tg_create_bound_single_tagged_stream_on_port(self.tg_session,stream_name,port,stream_to_bounder, stream_from_bounder,vlan_id, vlan_user_priority,**option)
        else:
            res=self.tg.tg_create_bound_single_tagged_stream_on_port(self.tg_session,stream_name,port,stream_to_bounder, stream_from_bounder,vlan_id, vlan_user_priority,**option)
        if "ERROR" in res:
            return False
        else:
            return True

    def ixia_create_l2_dhcp_traffic_ds(self,dhcpserverhandle,dhcpclienthandle):
        option = {
                    "traffic_generator": 				"ixnetwork_540",
                    "circuit_endpoint_type": 			"ipv4",
                    "track_by": 					    "{dest_ip source_ip}",
                    "emulation_src_handle": 			"",
                    "emulation_dst_handle": 		    "",
                    "name": 						    "DS_Traffic_UDP",
                    "endpointset_count": 			    "1",
                    "src_dest_mesh": 				    "one_to_one",
                    "route_mesh": 					    "one_to_one",
                    "rate_percent": 					"20",
                    "frame_size": 					    "256",
                    "tx_mode": 					        "advanced",
                    "transmit_mode": 				    "continuous",
                    "convert_to_raw": 				    "0",
                    "l4_protocol":                      "udp",
                    "udp_dst_port":                     "28000",
                    "udp_src_port":                     "27000"
                }
        option["emulation_src_handle"]= dhcpserverhandle
        option["emulation_dst_handle"]= dhcpclienthandle
        r = False
        for i in range(1,5):
            r = self._ixia_send_tclcmd("CiHLT::trafficConfig","create",1,**option)
            if r:
                break
            else:
                self.ixia_controll_start_allprotocols()
                sleep(30)
        return r

    def ixia_create_igmp_port(self,hostname,hostport,queriername="querier",querierport="p1",**Data):
        option = {
                    "msg_interval": 			        "79",
                    "unsolicited_report_interval":      "81"
                }
        option["vlan_id"]= Data["InVlanSwitch"]
        option["intf_ip_addr"] = Data["STATICADDRESS"]
        option["mac_address_init"] = Data["StaticMac"]
        #option["gateway"] =Data["Gateway"]
        option2 = {
            "vlan_id": 			        "79",
            "intf_ip_addr":      "",
            "query_interval":   "60"
        }
        if Data["MVREnable"] is "1":
            option2["vlan_id"] = Data["MVR_VLAN"]
            option2["intf_ip_addr"] = Data["MVRServerAddress"]
            option2["mac_address_init"] = Data["MVRMac"]
        else:
            option2["vlan_id"] = Data["OutSVLAN"]
            option2["intf_ip_addr"] = Data["DHCPCAddrStart"]
            option2["mac_address_init"] = Data["StaticMAC2"]

        self.logger.info("start to create the IGMP Session")
        #opt = self.ixia.dict2str(option)
        #res = self.ixia.tcl.command("CiHLT::igmpConfig 1/%s create {%s}" %(self.client_port,opt),timeout=20)[2]
        self.tg.tg_create_igmp_on_port(self.tg_session,hostname,hostport,"v2",**option)
        self.tg.tg_create_igmp_querier_on_port(self.tg_session,queriername,querierport,"v2",**option2)
        self.tg.tg_control_igmp_querier_by_name(self.tg_session,queriername,"start")
        #res = self.ixia.tcl.command("CiHLT::igmpConfig create {%s}" %opt,timeout=20)[2]
        #result = res.split()[0]
        #self.logger.debug("CreateIGMPSession : %s" %result)
        # if "ERROR" in Handle:
        #     return False
        # else:
        #     return True

    def ixia_create_mcast_group(self,client_name,source_name,session_name,**Data):
        option = {
            "num_groups":     "30",
            "ip_addr_start":  "228.0.1.1",
            "ip_prefix_len":  "24"
        }
        option2 = {
            "num_sources":     "3",
            "ip_addr_step":   "0.0.0.1",
            "ip_prefix_len":  "24"
        }
        option2["ip_addr_start"]=Data["DHCPCAddrStart"]
        self.logger.info("Start to create the multicast group")
        #opt = self.ixia.dict2str(option)
        self.tg.tg_create_multicast_group(self.tg_session, client_name,**option)
        self.tg.tg_create_multicast_source(self.tg_session, source_name,**option2)
        source_pool_name_list=[]
        source_pool_name_list.append(source_name)
        self.tg.tg_create_igmp_group(self.tg_session,"igmp_group",session_name,client_name,
                          source_pool_name_list,g_filter_mode="include")
        #GroupHandle = self.ixia.tcl.command("CiHLT::mcastGroupConfig create {%s}" %opt,timeout=20)[2]
        #result = GroupHandle.split()[0]
        #self.logger.debug("CreateMcastGroup)
        # if "ERROR" in result:
        #     return False
        # else:
        #     # McastGroupHandle = GroupHandle.split()[-1]
        #     # self.logger.debug("CreateMcastGroup return: %s" %McastGroupHandle)
        #     # return McastGroupHandle
        #     return True
        return "client_group"

    def ixia_config_igmp(self,session_name,querier_name,client_port,**Data):

        # option = {
        #     "group_pool_handle":     ""
        # }
        self.ixia_create_igmp_port(session_name,client_port,queriername=querier_name,**Data)
        #if result_createsession:
        result_create_group= self.ixia_create_mcast_group("client_group","source_group",session_name,**Data)
        return result_create_group
            #option["group_pool_handle"] = self.ixia_create_mcast_group(tg_session,"igmp_group",session_name,"igmp_pool")
            #if option["group_pool_handle"]:
        # if result_create_group:
        #         # self.logger.info("start to config the IGMP Host")
        #         # # opt = self.ixia.dict2str(option)
        #         # # Handle = self.ixia.tcl.command("CiHLT::igmpGroupConfig %s create {%s}" %(IGMPSessionHandle,opt),timeout=20)[2]
        #         # Handle = self.ixia.tg_create_igmp_on_port(tg_session,name,port,igmp_version,**option)
        #         # self.logger.debug("Config IGMP Group return: %s" %Handle)
        #         # # IGMPGroupHandle = Handle.split()[-1]
        #         # # self.logger.debug("Config IGMP Group return handle: %s" %IGMPGroupHandle)
        #         # # res = Handle.split()[0]
        #         # # self.logger.debug("Config IGMP Group return status: %s" %res)
        #         # if "ERROR" in Handle:
        #         #     return False
        #         # else:
        # #         return True
        # #     else:
        #     return True
        # else:
        #     return False

    def ixia_create_l2_igmp_traffic(self,stream_name,dport,sport,**data):
        option = {
                    "circuit_endpoint_type": 			"ipv4",
                    "track_by": 					    "{dest_ip source_ip}",
                    "endpointset_count": 			    "1",
                    "src_dest_mesh": 				    "one_to_one",
                    "route_mesh": 					    "one_to_one",
                    "rate_percent": 					"18",
                    "frame_size": 					    "512",
                    "tx_mode": 					        "advanced",
                    "transmit_mode": 				    "continuous",
                    "convert_to_raw": 				    "1",
                    "l4_protocol":                      "udp",
                    "udp_dst_port":                     "38000",
                    "udp_src_port":                     "37000"
                }
        if data.has_key("IXIA_encapsulation"):
            if data["IXIA_encapsulation"]== "ethernet_ii_vlan":
                #option["encap"] = data["IXIA_encapsulation"]
                vlan_id = data["OutSVLAN"]
                vlan_user_priority = data["OutSpbit"]
            else:
                #option["encap"]= "ethernet_ii_qinq"
                vlan_id = data["OutSVLAN"]
                vlan_user_priority = data["OutCpbit"]
        # option["emulation_src_handle"]= sourcehandle
        # option["emulation_dst_handle"]= desthandle
        # r = self.ixia.conf_traffic("create",**option)
        self.tg.tg_create_single_tagged_stream_on_port(self.tg_session,
                                                     stream_name,
                                                     dport,sport,
                                                     vlan_id, vlan_user_priority,
                                                     ip_dst_addr="228.0.1.1",ip_src_addr=data["DHCPSAddress"],
                                                     mac_dst="01:00:5e:01:01:01",mac_src=data["DHCPSMAC"],
                                                     **option)
        # self.logger.info("Fail after retry cmd : %s, please check your config!" %r)
        # if "ERROR" in r:
        #     return False
        # else:
        #     return True


    def ixia_controll_start_traffics(self):
        self.tg.control_traffic("run")

    def ixia_controll_stop_traffics(self):
        self.ixia.control_traffic("stop")

    def ixia_controll_start_allprotocols(self):

        result = False
        for i in range(0,10):
            r = self.ixia.tcl.command("CiHLT::testControl start_all_protocols", timeout=30)[2]
            res = self.ixia.verify(r)
            if "ERROR" in res:
                if i > 9:
                    raise IXIAException("Fail to start protocol, please check your configurations")
                else:
                    self.logger.warn("FAIL: start protocl fail!")
                    sleep(20)
            else:
                break
                self.logger.info("PASS: start protocl done!")
                result = True
        return result
    def ixia_controll_stop_allprotocols(self):

        # Result = True
        # r = self.ixia.test_control("stop_all_protocols")
        # if "ERROR" in r:
        #     Result = False
        # else:
        #     Result = r.split()[-1]
        # return Result
        result = False
        for i in range(0,10):
            r = self.ixia.tcl.command("CiHLT::testControl stop_all_protocols", timeout=30)[2]
            res = self.ixia.verify(r)
            if "ERROR" in res:
                if i > 9:
                    raise IXIAException("Fail to stop protocol, please check your configurations")
                else:
                    self.logger.warn("FAIL: stop protocl fail!")
                    sleep(20)
            else:
                break
                self.logger.info("PASS: stop protocl done!")
                result = True
        return result

    def ixia_get_traffic_stats(self,mode):
        #opt = self.ixia.dict2str()
        origin_data = self.ixia.tcl.command("CiHLT::trafficStat %s " % mode,timeout=20)[2]

        #origin_data = self.ixia.traffic_stats("traffic_item")
        dict_result = self._ixia_parser_result(origin_data)
        return dict_result
    def _ixia_parser_result(self,origin_data):
        str = origin_data
        i = 0
        n = 0
        content = ""
        res = {}
        keylist = []
        keylist.append("res")
        names = locals()

        for i in range(0,int(len(str))):
            if str[i] == "{" :
                n =n +1
                if n>= 1 and content is not "" and not re.match(r'\s',content):
                    keylist.append(content.strip())
                    names[keylist[len(keylist)-1]] = {}
                content = ""
            elif str[i] == "}":
                n = n-1
                if n%2 == 0:
                    if content is not "" and not re.match(r'\s',content):
                        names[keylist[len(keylist)-1]][content.split( )[0]]=content.split()[-1]
                else:
                    names[keylist[len(keylist)-2]][keylist[len(keylist)-1]] = names[keylist[len(keylist)-1]]
                    keylist.pop()
                content = ""
                #print "res:",res
            else:
                if n >0:
                    content = content + str[i]
        return res

    def _ixia_send_tclcmd(self,cmd,mode,retry = 5,timeout = 20,**kwargs):
        result = False
        opt = self.ixia.dict2str(kwargs)
        for i in range(0,retry):
            r = self.ixia.tcl.command("%s %s {%s}" %(cmd,mode, opt),timeout=timeout)[2]
            res = self.ixia.verify(r)
            if "ERROR" in res:
                if i == retry:
                    raise IXIAException("Fail after retry cmd : %s, please check your config!" %cmd)
                else:
                    self.logger.warn("FAIL: try again!")
                    sleep(20)
            else:
                self.logger.info("PASS:%s!" %cmd)
                result = True
                break

        return result