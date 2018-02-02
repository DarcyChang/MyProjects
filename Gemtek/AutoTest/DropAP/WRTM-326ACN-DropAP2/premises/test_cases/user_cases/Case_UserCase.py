#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'alu'
import time
import sys
import cafe
from stp.premises.library import Teststeplib_ixia as ixia_lib
from stp.premises.library import Teststeplib_ont as ont_lib
from cafe.app import App
from caferobot.trafficgen.trafficgen import TrafficGenerator as tg
from stp.premises.library import Teststeplib_e7 as e7_lib
#from caferobot.util.forward import caller_transfer

# class usercases_adapter(object):
#     def __init__(self):
#         pass
#     @staticmethod
#     def build_usercases():
#         return usercases()
#


class usercases(object):

    def __init__(self):
        pass

    @staticmethod
    #@cafe.test_case()
    def tc_usercases_1(case_conf,**GeneralConf):
        """
        id=5442423

        verify the node1 craft interface name
        """

        e7 = e7_lib.CalixE7Base(App().e7)
        ixia = ixia_lib.IXIABase(**GeneralConf)
        case_conf = case_conf
        #import CaseConf as CaseConf

        if ixia.connect_host():
            if ixia.connect_chassis():

                if not e7.e7_provision_ont(**GeneralConf):
                    cafe.Checkpoint().fail("Provision ONT Fail!")

                #add Data or Video Service
                Datalist = [case_conf.Data1,case_conf.Data2,case_conf.Data3]
                Siplist = [case_conf.SIP1,case_conf.SIP2]

                for dict in Datalist:
                    Conf = GeneralConf.copy()
                    Conf.update(dict)

                    if not e7.e7_add_ont_dataservice(**Conf):
                        cafe.Checkpoint().fail("Add Data or Video Service Fail!")
                    r = e7.e7_check_ont_dataservice(**Conf)
                    cafe.Checkpoint(r).not_contains("fail")

                        #Start IXIA config
                        #Config WAN Server and LAN Clients
                    if Conf["Enable"] is "1":

                        #Init the ver

                        serverhandle = ""
                        clienthandle1 = ""
                        wanclienthandle = ""
                        IGMPSourceHandle = ""
                        IGMPHandler = ""

                        if dict.has_key("WANType"):
                            if dict["WANType"] is "pppoe":
                                serverhandle = ixia.ixia_config_pppserver(**dict)
                                if dict["Bridge"] is not "RG":
                                    pass
                                else:
                                    dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                                    clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**dict)

                            else:
                                serverhandle = ixia.ixia_config_dhcps(**dict)
                                dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                                clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**dict)


                        cafe.Checkpoint(serverhandle).not_contains("False")
                        print("serverhandle: %s" %serverhandle)
                        cafe.Checkpoint(clienthandle1).not_contains("False")
                        print ("clienthandle1: %s" %clienthandle1)
                        #Config WAN DS Client when RG is enabled
                        if dict["Bridge"] is "RG":
                            wanclienthandle = ixia.ixia_config_l3_staticintf("WAN",**dict)
                        else:
                            wanclienthandle = clienthandle1


                        #Config IGMP Service
                        if dict["McastProfile"] is not "none":
                            IGMPHandler = ixia.ixia_config_igmp(**dict)
                            if dict["MVREnable"] is "1":
                                IGMPSourceHandle = ixia.ixia_config_mvrintf(**dict)
                            else:
                                IGMPSourceHandle = serverhandle
                            cafe.Checkpoint(IGMPHandler).not_contains("False")
                            cafe.Checkpoint(IGMPSourceHandle).not_contains("False")
                            time.sleep(2)
                            #Start Protocols
                            r = ixia.ixia_controll_start_allprotocols()
                            time.sleep(40)
                            r = ixia.ixia_create_l2_igmp_traffic(IGMPSourceHandle,IGMPHandler)
                            cafe.Checkpoint(r).not_contains("False")
                            r = ixia.ixia_controll_start_allprotocols()

                        else:
                        #Config Data Service
                            r = ixia.ixia_controll_start_allprotocols()
                            time.sleep(20)
                            r = ixia.ixia_create_l2_dhcp_traffic_us(serverhandle,clienthandle1)
                            cafe.Checkpoint(r).not_contains("False")
                            r =ixia.ixia_create_l2_dhcp_traffic_ds(serverhandle,wanclienthandle)
                            cafe.Checkpoint(r).not_contains("False")
                        #time.sleep(20)
                    else:
                        pass

                #Add Iphost SIP service
                for dict in Siplist:
                    Conf = GeneralConf.copy()
                    Conf.update(dict)
                    if not e7.e7_add_ont_sipservice(**Conf):
                        cafe.Checkpoint().fail("Add SIP Service Fail!")
                    r = e7.e7_check_ont_sipservice(**Conf)
                    cafe.Checkpoint(r).not_contains("fail")


                time.sleep(5)
                r = ixia.ixia_controll_start_traffics()

    @staticmethod
    #@cafe.test_case()
    def tc_usercases_2(CaseConf,**GeneralConf):
        """

        verify the node1 craft interface name
        """

        e7 = e7_lib.CalixE7Base(getattr(App(),GeneralConf["e7"]))
        ont =ont_lib.calixontbase(getattr(App(),GeneralConf["ont_topo"]))
        tg2_session=GeneralConf["ixia_session"]
        #ixia = ixia_lib.IXIABase(getattr(App(),GeneralConf["ixia_session"]))
        ixia = ixia_lib.IXIABase(GeneralConf["ixia_session"])
        CaseConf = CaseConf
        test_result=True

        # if ixia.connect_host():
        #     if ixia.connect_chassis():

        cafe.Checkpoint(e7.e7_provision_ont(**GeneralConf)).exact(True)
        i = 0
#       ixia.connect_chassis()
        for key,value in CaseConf.DataConf.items():
            Conf = GeneralConf.copy()
            Conf.update(value)

            if Conf["Enable"] is "1":
                print("Start to add data service")
                cafe.Checkpoint(e7.e7_add_ont_dataservice(**Conf)).exact(True)
                cafe.Checkpoint(e7.e7_check_ont_dataservice(**Conf)).exact(True)

                #Start IXIA config
                #Config WAN Server and LAN Clients
                #config server

                if Conf["WANType"] is "pppoe":
                    ixia.ixia_config_pppserver("tg_Server","p1",**Conf)
                    ixia.ixia_control_pppox_by_name("tg_Server","connect")
                elif Conf["WANType"] is "dhcp":
                    ixia.ixia_config_dhcps("tg_Server","p1",**Conf)
                    ixia.ixia_control_dhcp_server("tg_Server","start")
                else:
                    pass
                ServerHandle = 'tg_Server'

                #config client
                #config IGMP client
                if Conf["McastProfile"] is not "none":
                    print("start to config IGMP on IXIA")
                    #clienthandle1 = ixia.ixia_config_l3_staticintf("LAN",**Conf)
                    IGMPHandler = ixia.ixia_config_igmp("igmp_session","igmp_source","p2",**Conf)
                    # IGMPHandler = ixia.tg_create_igmp_on_port(GeneralConf["ixia_session"])
                    # if Conf["MVREnable"] is "1":
                    #     ixia.ixia_config_mvrintf("Mvr_intf","p1",**Conf)
                    #     IGMPSourceHandle = "Mvr_intf"
                    # else:
                    #     IGMPSourceHandle = "tg_Server"
                    # if not IGMPSourceHandle or not IGMPHandler:
                    #     cafe.Checkpoint().fail("Get IGMP handle Fail!")
                    #     test_result=False
                    #     print("Get IGMP handle Fail!")
                    # time.sleep(2)
                    # #Start Protocols
                    #r = ixia.ixia_controll_start_allprotocols()
                    ixia.ixia_control_igmp("igmp_session","start")
                    time.sleep(40)
                    if Conf["Bridge"] is "RG" :
                        i = i +1
                        if Conf["WANType"]:
                            if Conf["WANType"] is "pppoe":
                                usercases.subtc_verify_rg_ip(ont,i,"pppoe")
                            else:
                                usercases.subtc_verify_rg_ip(ont,i)
                        else:
                            usercases.subtc_verify_rg_ip(ont,i)
                    ixia.ixia_create_l2_igmp_traffic("igmp_traffic","p2","p1",**Conf)
                    #cafe.Checkpoint().fail("Create IGMP Traffic fail!")
                    #test_result=False
                    print("Create IGMP Traffic")
                    time.sleep(10)
                    #r = ixia.ixia_controll_start_allprotocols()

                else:
                    if Conf["Bridge"] is "RG" :
                        print("Start to config RG service on IXIA")
                        ixia.ixia_config_l3_staticintf("wan_static","p1","WAN",**Conf)
                        WANClientHandle = "wan_static"
                        ixia.ixia_config_l3_staticintf("lan_static","p2","LAN",**Conf)
                        clienthandle1 = "lan_static"
                        i = i+1
                    else:
                        if Conf["WANType"] is "pppoe":
                            clienthandle1 = ixia.ixia_config_pppclient("lanclient","p2",**Conf)
                            ixia.ixia_control_pppox_by_name('lanclient','connect')
                        else:
                            # dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                            clienthandle1 = ixia.ixia_config_dhcpc("lanclient","p2",**Conf)
                            ixia.ixia_control_dhcp_client("lanclient","start")
                        WANClientHandle = clienthandle1


                    if "False" in ServerHandle or "False" in clienthandle1:
                        cafe.Checkpoint().fail("Get Data Traffic handle Fail!")
                    #add data traffic
                    time.sleep(2)
                    #r = ixia.ixia_controll_start_allprotocols()
                    time.sleep(40)
                    if Conf["Bridge"] is "RG":
                        if Conf["WANType"]:
                            if Conf["WANType"] is "pppoe":
                                usercases.subtc_verify_rg_ip(ont,i,"pppoe")
                            else:
                                usercases.subtc_verify_rg_ip(ont,i)
                        else:
                            usercases.subtc_verify_rg_ip(ont,i)
                    if not ixia.ixia_create_bound_tagged_stream("us_traffic","p1",ServerHandle,WANClientHandle,"us",**Conf):
                        cafe.Checkpoint().fail("Create up stream traffic fail!")
                        test_result=False
                    time.sleep(5)
                    if not ixia.ixia_create_bound_tagged_stream("ds_traffic","p2",WANClientHandle,ServerHandle,"ds",**Conf):
                        cafe.Checkpoint().fail("create down stream traffic fail")
                        test_result=False

            else:
                pass

        #Add Iphost SIP service
        for key,value in CaseConf.SIPConf.items():
            Conf = GeneralConf.copy()
            Conf.update(value)
            if not e7.e7_add_ont_sipservice(**Conf):
                cafe.Checkpoint().fail("Add SIP Service Fail!")
                print("add SIP service fail!")
            r = e7.e7_check_ont_sipservice(**Conf)

        time.sleep(10)
        # ixia.ixia_controll_start_allprotocols()
        # print("IXIA:start all protocols......")
        # time.sleep(10)
        # r = ixia.ixia_controll_start_traffics()
        ixia.ixia_control_traffic("p1","run")
        print("IXIA:start all traffics......")
        time.sleep(72)
        ixia.ixia_control_traffic("p1","stop")
        print("IXIA:stop all traffics......")
        time.sleep(5)
        #dict_result = ixia.ixia_get_traffic_stats("traffic_item")

        #lossrate = dict_result['traffic_item']['aggregate']['rx']['loss_percent']["avg"]
        # print("first test lossrate:",lossrate)
        # if float(lossrate) > 10.0:
        #     cafe.Checkpoint().fail("Loss rate is more than 10%!")
        #     test_result=False

        #diable/enable gpon port
        gponport = e7.e7_get_ont_gponport(Conf["ontid"])
        if gponport:
            print("start to disable GPON port")
            if not e7.e7_set_gponport_status(gponport,"disabled"):
                cafe.Checkpoint().fail("Disable gponport %s fail!" %gponport)
            else:
                time.sleep(10)
                print("Enable GPON port....")
                if not e7.e7_set_gponport_status(gponport,"enabled"):
                    cafe.Checkpoint().fail(("Enable gpon port %s fail!" %gponport))
                else:
                    time.sleep(150)
            print("Start traffic verify.....")
            if not usercases.subtc_verify_traffic(ixia):
                cafe.Checkpoint().fail("Traffic verify fail!")
                test_result=False
            else:
                cafe.Checkpoint().pass_step("test pass")
        else:
            pass
        return test_result


    #@cafe.test_case()
    @staticmethod
    def tc_auxilialy_usercases_1(CaseConf,**GeneralConf):
        """
        id=5442423

        verify the node1 craft interface name
        """

        e7 = e7_lib.CalixE7Base(App().e7)
    #    ixia = Ixia_lib.IXIABase(**GeneralConf)
        CaseConf = CaseConf
        #import CaseConf as CaseConf
        #
        # if ixia.connect_host():
        #     if ixia.connect_chassis():

        if not e7.e7_provision_ont(**GeneralConf):
            cafe.Checkpoint().fail("Provision ONT Fail!")

        #add Data or Video Service

        for key,value in CaseConf.DataConf.items():
            print value
            Conf = GeneralConf.copy()
            Conf.update(value)

            EthList = ["g1","g2","g3","g4"]
            for eth in EthList:
                Conf["ETH"] = eth
                if not e7.e7_add_ont_dataservice(**Conf):
                    cafe.Checkpoint().fail("Add Data or Video Service Fail!")
                r = e7.e7_check_ont_dataservice(**Conf)
                cafe.Checkpoint(r).not_contains("fail")

                #Add Iphost SIP service
        for key,value in CaseConf.SIPConf.items():
            Conf = GeneralConf.copy()
            Conf.update(value)
            if not e7.e7_add_ont_sipservice(**Conf):
                cafe.Checkpoint().fail("Add SIP Service Fail!")
            r = e7.e7_check_ont_sipservice(**Conf)
            cafe.Checkpoint(r).not_contains("fail")

    #@cafe.test_case()
    @staticmethod
    def tc_usercases_800e(CaseConf,**GeneralConf):
        """
        id=5442423

        verify the node1 craft interface name
        """

        e7 = e7_lib.CalixE7Base(App().e7)
        ont =ont_lib.calixontbase(getattr(App(),GeneralConf["ont_topo"]))
        ixia = ixia_lib.IXIABase(**GeneralConf)
        CaseConf = CaseConf

        if ixia.connect_host():
            if ixia.connect_chassis():
                cafe.Checkpoint(e7.e7_provision_ont(**GeneralConf)).exact(True)
                i = 0
                for key,value in CaseConf.DataConf.items():
                    Conf = GeneralConf.copy()
                    Conf.update(value)

                    if Conf["Enable"] is "1":
                        if e7.e7_check_ont_dataservice(**Conf):
                            pass
                        else:
                            cafe.Checkpoint(e7.e7_add_ont_dataservice(**Conf)).exact(True)
                            cafe.Checkpoint(e7.e7_check_ont_dataservice(**Conf)).exact(True)

                        #Start IXIA config
                        #Config WAN Server and LAN Clients
                        #config server
                        if not "noTraffic" in Conf.keys():
                            if Conf["WANType"] is "pppoe":
                                ServerHandle = ixia.ixia_config_pppserver(**Conf)
                            elif Conf["WANType"] is "dhcp":
                                ServerHandle = ixia.ixia_config_dhcps(**Conf)
                            else:
                                pass

                            #config client
                            #config IGMP client
                            if Conf["McastProfile"] is not "none":
                                #clienthandle1 = ixia.ixia_config_l3_staticintf("LAN",**Conf)
                                IGMPHandler = ixia.ixia_config_igmp(**Conf)
                                if Conf["MVREnable"] is "1":
                                    IGMPSourceHandle = ixia.ixia_config_mvrintf(**Conf)
                                else:
                                    IGMPSourceHandle = ServerHandle
                                if not IGMPSourceHandle or not IGMPHandler:
                                    cafe.Checkpoint().fail("Get IGMP handle Fail!")
                                time.sleep(2)
                                #Start Protocols
                                r = ixia.ixia_controll_stop_allprotocols()
                                time.sleep(5)
                                r = ixia.ixia_controll_start_allprotocols()
                                time.sleep(40)
                                if Conf["Bridge"] is "RG" :
                                    i = i +1
                                    if Conf["WANType"]:
                                        if Conf["WANType"] is "pppoe":
                                            usercases.subtc_verify_rg_ip(ont,i,"pppoe")
                                        else:
                                            usercases.subtc_verify_rg_ip(ont,i)
                                    else:
                                        usercases.subtc_verify_rg_ip(ont,i)
                                if not ixia.ixia_create_l2_igmp_traffic(IGMPSourceHandle,IGMPHandler):
                                    cafe.Checkpoint().fail("Create IGMP Traffic fail!")
                                time.sleep(10)
                                r = ixia.ixia_controll_start_allprotocols()

                            else:
                                if Conf["Bridge"] is "RG" or Conf.has_key("800EConnect"):
                                    WANClientHandle = ixia.ixia_config_l3_staticintf("WAN",**Conf)
                                    clienthandle1 = ixia.ixia_config_l3_staticintf("LAN",**Conf)
                                    i = i+1
                                else:
                                    if Conf["WANType"] is "pppoe":
                                        clienthandle1 = ixia.ixia_config_pppclient(**Conf)
                                    else:
                                        dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                                        clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**Conf)
                                    WANClientHandle = clienthandle1

                                if "False" in ServerHandle or "False" in clienthandle1:
                                    cafe.Checkpoint().fail("Get Data Traffic handle Fail!")
                                #add data traffic
                                r = ixia.ixia_controll_stop_allprotocols()
                                time.sleep(10)
                                r = ixia.ixia_controll_start_allprotocols()
                                time.sleep(40)
                                if Conf["Bridge"] is "RG":
                                    if Conf["WANType"]:
                                        if Conf["WANType"] is "pppoe":
                                            usercases.subtc_verify_rg_ip(ont,i,"pppoe")
                                        else:
                                            usercases.subtc_verify_rg_ip(ont,i)
                                    else:
                                        usercases.subtc_verify_rg_ip(ont,i)
                                if not ixia.ixia_create_l2_dhcp_traffic_us(ServerHandle,clienthandle1):
                                    cafe.Checkpoint().fail("Create up stream traffic fail!")
                                time.sleep(5)
                                if not ixia.ixia_create_l2_dhcp_traffic_ds(ServerHandle,WANClientHandle):
                                    cafe.Checkpoint().fail("create down stream traffic fail")

                    else:
                        pass

                #Add Iphost SIP service
                for key,value in CaseConf.SIPConf.items():
                    Conf = GeneralConf.copy()
                    Conf.update(value)
                    if not e7.e7_add_ont_sipservice(**Conf):
                        cafe.Checkpoint().fail("Add SIP Service Fail!")
                    r = e7.e7_check_ont_sipservice(**Conf)

                r = ixia.ixia_controll_stop_allprotocols()
                time.sleep(10)
                r = ixia.ixia_controll_start_allprotocols()
                time.sleep(10)
                r = ixia.ixia_controll_start_traffics()
                time.sleep(120)
                r = ixia.ixia_controll_stop_traffics()
                time.sleep(5)
                dict_result = ixia.ixia_get_traffic_stats("traffic_item")

                lossrate = dict_result['traffic_item']['aggregate']['rx']['loss_percent']["avg"]
                print("lossrate:",lossrate)
                if float(lossrate) > 0.2:
                    cafe.Checkpoint().fail("Loss rate is more than 0.2%!")

                #diable/enable gpon port
                # gponport = e7.e7_get_ont_gponport(Conf["ontid"])
                # if gponport:
                #     if not e7.e7_set_gponport_status(gponport,"disabled"):
                #         cafe.Checkpoint().fail("Disable gponport %s fail!" %gponport)
                #     else:
                #         time.sleep(10)
                #         if not e7.e7_set_gponport_status(gponport,"enabled"):
                #             cafe.Checkpoint().fail(("Enable gpon port %s fail!" %gponport))
                #         else:
                #             time.sleep(100)
                #     if not subtc_verify_traffic(ixia):
                #         cafe.Checkpoint().fail("Traffic verify fail!")
                #     else:
                #         cafe.Checkpoint().pass_step("test pass")
                else:
                    pass

    @staticmethod
    def subtc_verify_traffic(ixia):
        r = ixia.ixia_controll_start_allprotocols()
        time.sleep(30)
        r = ixia.ixia_controll_start_traffics()
        time.sleep(120)
        r = ixia.ixia_controll_stop_traffics()
        time.sleep(10)
        dict_result = ixia.ixia_get_traffic_stats("traffic_item")

        lossrate = dict_result['traffic_item']['aggregate']['rx']['loss_percent']["avg"]
        print("lossrate:",lossrate)
        if float(lossrate) > 10.0:
            r = False
            cafe.Checkpoint().fail("Loss rate is %f,more than 10 !" %float(lossrate))
        return r

    @staticmethod
    def subtc_verify_rg_ip(ont,intf_number,intf_type = "dhcp"):
        if intf_type == "dhcp":
            interface = "veip0." + str(intf_number)
        else:
            interface = "ppp0." + str(intf_number)
        for m in range(0,10):
            if ont.ont_get_ipaddress(interface):
                break
            else:
                if m < 10:
                    time.sleep(20)
                else:
                    cafe.Checkpoint.fail("ONT RG port %s can't get IP address!" %interface)