__author__ = 'alu'
import time

import cafe
from library import Teststeplib_ixia as Ixia_lib
from cafe.app import App

from library import Teststeplib_e7 as e7_lib


@cafe.test_case()
def UserCases1(CaseConf,**GeneralConf):
    """
    id=5442423

    verify the node1 craft interface name
    """

    e7 = e7_lib.CalixE7Base(App().e7)
    ixia = Ixia_lib.IXIABase(**GeneralConf)
    CaseConf = CaseConf

    if ixia.connect_host():
        if ixia.connect_chassis():

            if not e7.e7_provision_ont(**GeneralConf):
                cafe.Checkpoint().fail("Provision ONT Fail!")

            for key,value in CaseConf.DataConf.items():
                Conf = GeneralConf.copy()
                Conf.update(value)

                if not e7.e7_add_ont_dataservice(**Conf):
                    cafe.Checkpoint().fail("Add Data or Video Service Fail!")
                r = e7.e7_check_ont_dataservice(**Conf)
                cafe.Checkpoint(r).not_contains("fail")

                    #Start IXIA config
                    #Config WAN Server and LAN Clients
                if Conf["Enable"] is "1":

                    #Init the ver

                    ServerHandle = ""
                    clienthandle1 = ""
                    WANClientHandle = ""
                    IGMPSourceHandle = ""
                    IGMPHandler = ""

                    if Conf["WANType"] is "pppoe":
                        ServerHandle = ixia.ixia_config_pppserver(**Conf)
                        if Conf["Bridge"] is not "RG":
                            pass
                        else:
                            dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                            clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**Conf)

                    else:
                        ServerHandle = ixia.ixia_config_dhcps(**Conf)
                        dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                        clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**Conf)


                    cafe.Checkpoint(ServerHandle).not_contains("False")
                    print("ServerHandle: %s" %ServerHandle)
                    cafe.Checkpoint(clienthandle1).not_contains("False")
                    print ("clienthandle1: %s" %clienthandle1)
                    #Config WAN DS Client when RG is enabled
                    if Conf["Bridge"] is "RG":
                        WANClientHandle = ixia.ixia_config_l3_staticintf("WAN",**Conf)
                    else:
                        WANClientHandle = clienthandle1


                    #Config IGMP Service
                    if Conf["McastProfile"] is not "none":
                        IGMPHandler = ixia.ixia_config_igmp(clienthandle1,**Conf)
                        if Conf["MVREnable"] is "1":
                            IGMPSourceHandle = ixia.ixia_config_mvrintf(**Conf)
                        else:
                            IGMPSourceHandle = ServerHandle
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
                        r = ixia.ixia_create_l2_dhcp_traffic_us(ServerHandle,clienthandle1)
                        cafe.Checkpoint(r).not_contains("False")
                        r =ixia.ixia_create_l2_dhcp_traffic_ds(ServerHandle,WANClientHandle)
                        cafe.Checkpoint(r).not_contains("False")
                    #time.sleep(20)
                else:
                    pass

            #Add Iphost SIP service
            for key,value in CaseConf.SIPConf.items():
                Conf = GeneralConf.copy()
                Conf.update(value)
                if not e7.e7_add_ont_sipservice(**Conf):
                    cafe.Checkpoint().fail("Add SIP Service Fail!")
                r = e7.e7_check_ont_sipservice(**Conf)
                cafe.Checkpoint(r).not_contains("fail")


            time.sleep(5)
            r = ixia.ixia_controll_start_traffics()

#                time.sleep(20)
#                ixia.stoptraffic()

