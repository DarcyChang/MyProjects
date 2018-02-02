__author__ = 'alu'
import cafe
import time

# Data1 is a template for 1 data service configuration.
# when configure the test config file ,all the parameters in the data conf template should be included.
# no parameter in template should be missing, or the test execution will report error.
# "Data1":{
#                 "Enable":                   "1",               --------If not 1, this data config and traffic test will be ignored
#                 "ServiceName":              "Data1",           --------Service name on E7
#                 "Bridge":                   "RG",              --------RG,HB,FB. HB is halfbridge,FB is full bridge.
#                 "RGMode":                   "native",          --------native or external. none means not in RG model.
#                 "WANType":                  "dhcp",            --------dhcp or pppoe.
#                 "PPPUsername":              "Calix",
#                 "PPPPassword":              "password",
#                 "RGMgmtProfile":            "PITT-CCFG",
#                 "RGInstance":               "none",
#                 "ETH":                      "g1",              --------The eth port which connect to ixia.g1 means eth1
#                 "InVlanSwitch":             "11",              --------For IXIA traffic generate. "0" means no vlan
#                 "InVlan":                   "1503",            --------For service provision on E7.
#                 "InPbit":                   "0",               --------0 means all pbit.
#                 "InDSCP":                   "0",
#                 "VLANAction":               "C",               --------C: change tag.Anc:Add and change tag.A2: Add 2 tags A:Add tag
#                 "UntagMatchlist":           "all_untag"        --------The untag matchlist name
#                 "OutSVLAN":                 "1503",            --------For service provision on E7
#                 "OutSpbit":                 "0",               --------For service provision on E7
#                 "OutCVLAN":                 "0",
#                 "OutCpbit":                 "1",
#                 "usciroverride":            "0",               --------E7 Qos. If OutSpbit in [0,2], us and ds should be 0.
#                                                                                If OutSpbit in [3,4], Us and Ds should != 0.
#                                                                                If OutSpbit in [5,7], Us should !=0 and Ds should =0
#                 "dsciroverride":            "0",
#                 "BandWidth":                "BWP_BE_1000m_none_none_none",
#                 "McastProfile":             "none",            ---------"none" means no IPTV service enabled in this service.
#                 "MVREnable":                "0",               ---------If enabled MVR, fill in 1.
#                 "IXIA_encapsulation":       "ethernet_ii_vlan",---------"ethernet_ii_vlan" : single vlan enabled
#                                                                         "ethernet_ii_qinq" : double vlan enabled
#                 "IXIAC_mac_addr":           "00.05.2e.11.11.11",
#                 "DHCPSAddress":             "10.30.0.1",       ----------DHCP server address, when Config the DHCP server on IXIA
#                 "DHCPSMAC":                 "0012.0032.2221",  ----------DHCP server mac
#                 "DHCPCAddrStart":           "10.30.0.22",      ----------DHCP client address pool start address.
#                 "DHCPCAddrCount":           "1",               ----------DHCP client pool size.
#                 "STATICADDRESS":            "192.168.1.136",   ----------Only for IPTV service. Config IPTV client on IXIA.
#                 "Gateway":                  "192.168.1.1",     ----------IPTV client gateway.
#                 "StaticMac":                "00.43.22.11.10.13",
#                 "MVR_VLAN":                 "2000",            ----------Only for the MVR service. The MVR IPTV server vlan on IXIA.
#                 "MVRServerAddress":         "10.210.100.1",    ----------only for the MVR service. The MVR IPTV server address on IXIA.
#                 "MVRMac":                   "00.05.20.11.11.13",---------Only for the MVR service. The MVR server mac on IXIA.
#                 "StaticMAC1":               "00.35.0a.11.11.11",---------In case for static address need to be added on IXIA
#                 "StaticMAC2":               "00.47.0a.11.11.21"
#         },
#####################################################################
#NOTE:
#Please confirm the E7 Configurations before test:
#     1. multicast profiles.
#     2. SIP gateway profile, dial plan
#     3. untag matchlist;
#     4.The VLANS will be used in service provision.
#
###################################################################

DataConf = {
"Data1":{
                "Enable":         "1",
                "ServiceName":    "Data1",
                "RGMode":         "no",
                "Bridge":         "HB",
                "WANType":        "dhcp",
                "ETH":            "g1",
                "InVlanSwitch":   "11",
                "InVlan":         "0",
                "InPbit":         "0",
                "InDSCP":         "0",
                "VLANAction":     "A2",
                "OutSVLAN":       "1503",
                "OutSpbit":       "1",
                "OutCVLAN":       "503",
                "OutCpbit":       "1",
                "usciroverride":  "0",
                "dsciroverride":  "1000m",
                "BandWidth":                "BWP_CE_1000m_none_none_none",
                "MVREnable":                "0",
                "McastProfile":             "none",
                "IXIA_encapsulation":       "ethernet_ii_qinq",
                "IXIAC_mac_addr":           "00.35.22.11.11.13",
                "DHCPSAddress":             "10.54.0.1",
                "DHCPSMAC":                 "0011.0032.2221",
                "DHCPCAddrStart":           "10.54.0.22",
                "STATICADDRESS":            "192.168.1.136",
                "Gateway":                  "192.168.1.1",
                "StaticMac":                "00.83.22.11.10.13",
                "DHCPCAddrCount":           "1",
                "MVR_VLAN":                 "2000",
                "MVRServerAddress":         "10.220.100.1",
                "MVRMac":                   "00.38.20.11.11.13",
                "StaticMAC1":               "00.38.0a.11.11.11",
                "StaticMAC2":               "00.37.0a.11.11.21"

        },
"Data2":{
                "Enable":                   "1",
                "MVREnable":                "1",
                "ServiceName":              "Video1",
                "Bridge":                   "HB",
                "RGMode":                   "no",
                "WANType":                  "dhcp",
                "PPPUsername":              "Calix",
                "PPPPassword":              "password",
                "RGMgmtProfile":            "PITT-CCFG",
                "RGInstance":               "none",
                "ETH":                      "g2",
                "InVlanSwitch":             "12",
                "InVlan":                   "0",
                "InPbit":                   "0",
                "InDSCP":                   "0",
                "VLANAction":               "A2",
                "OutSVLAN":                 "1502",
                "OutSpbit":                 "4",
                "OutCVLAN":                 "502",
                "OutCpbit":                 "4",
                "usciroverride":            "10m",
                "dsciroverride":            "20m",
                "BandWidth":                "BWP_BE_20m_none_none_none",
                "McastProfile":             "Mcast-IXIA-MVR",
                "MVR_VLAN":                 "2000",
                "MVRServerAddress":         "10.220.100.1",
                "MVRMac":                   "00.3e.20.11.11.13",
                "STATICADDRESS":            "10.64.0.36",
                "StaticMac":                "00.a3.2c.11.10.13",
                "IXIAC_mac_addr":           "00.39.2f.11.11.11",
                "IXIA_encapsulation":       "ethernet_ii_qinq",
                "DHCPSAddress":             "10.64.0.1",
                "DHCPSMAC":                 "0036.0035.2221",
                "DHCPCAddrStart":           "10.64.0.22",
                "DHCPCAddrCount":           "1",
                "StaticMAC1":               "00.37.0c.11.11.11",
                "StaticMAC2":               "00.4c.0c.11.11.21",
                "Gateway":                  "192.168.1.1"
        },
"Data3":{
                "Enable":                   "0",
                "ServiceName":              "Data1",
                "Bridge":                   "RG",
                "RGMode":                   "native",
                "WANType":                  "pppoe",
                "PPPUsername":              "Calix",
                "PPPPassword":              "password",
                "RGMgmtProfile":            "PITT-CCFG",
                "RGInstance":               "none",
                "ETH":                      "g1",
                "InVlanSwitch":             "11",
                "InVlan":                   "1513",
                "InPbit":                   "0",
                "InDSCP":                   "0",
                "VLANAction":               "AnC",
                "OutSVLAN":                 "1513",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "513",
                "OutCpbit":                 "1",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none",
                "IXIA_encapsulation":       "ethernet_ii_qinq",
                "IXIAC_mac_addr":           "00.09.2e.11.11.11",
                "DHCPSAddress":             "10.40.0.1",
                "DHCPSMAC":                 "0016.0035.2221",
                "DHCPCAddrStart":           "10.40.0.22",
                "DHCPCAddrCount":           "1",
                "StaticMAC1":               "00.2b.0a.11.11.11",
                "StaticMAC2":               "00.3c.0a.11.11.21",
                "Gateway":                  "192.168.1.1",
                "MVREnable":                "0"

        }
}
SIPConf = {
"SIP1":{
                "Enable":         "1",
                "ETH":            "p1",
                "VLANAction":     "A",
                "InVlan":         "0",
                "InPbit":         "0",
                "InDSCP":         "0",
                "OutSVLAN":       "4001",
                "OutSpbit":       "7",
                "OutCVLAN":       "0",
                "OutCpbit":       "0",
                "SIPInstance":   "none",
                "SIPGWProfile":  "PITT-SIP",
                "DialPlan":      "ST-PREM",
                "SIPURI":        "6123401120",
                "SIPUsername":   "6123401120",
                "SIPPassword":   "password"
        },
"SIP2" :{
                "Enable":         "1",
                "ETH":            "p2",
                "VLANAction":     "A",
                "InVlan":         "0",
                "InPbit":         "0",
                "InDSCP":         "0",
                "OutSVLAN":       "4001",
                "OutSpbit":       "7",
                "OutCVLAN":       "0",
                "OutCpbit":       "0",
                "SIPInstance":   "none",
                "SIPGWProfile":  "PITT-SIP",
                "DialPlan":      "ST-PREM",
                "SIPURI":        "6123401121",
                "SIPUsername":   "6123401121",
                "SIPPassword":   "password"
        }
}


@cafe.test_case()
def UserCases1(**GeneralConf):
    """
    id=5442423

    verify the node1 craft interface name
    """

    param = cafe.get_test_param()
    e7 = e7_lib.CalixE7Base(param.e7_sess)
    ixia = Ixia_lib.IXIABase(**GeneralConf)


    if ixia.connect_host():
        if ixia.connect_chassis():

            if not e7.e7_provision_ont(**GeneralConf):
                cafe.Checkpoint().fail("Provision ONT Fail!")

            #add Data or Video Service
            Datalist = [Data1,Data2,Data3]
            Siplist = [SIP1,SIP2]

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

                    ServerHandle = ""
                    clienthandle1 = ""
                    WANClientHandle = ""
                    IGMPSourceHandle = ""
                    IGMPHandler = ""

                    if dict["WANType"] is "pppoe":
                        ServerHandle = ixia.ixia_config_pppserver(**dict)
                        if dict["Bridge"] is not "RG":
                            pass
                        else:
                            dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                            clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**dict)

                    else:
                        ServerHandle = ixia.ixia_config_dhcps(**dict)
                        dhcpchandlebasic1 = ixia.ixia_config_dhcpc_basic()
                        clienthandle1 = ixia.ixia_config_dhcpc(dhcpchandlebasic1,**dict)


                    cafe.Checkpoint(ServerHandle).not_contains("False")
                    print("ServerHandle: %s" %ServerHandle)
                    cafe.Checkpoint(clienthandle1).not_contains("False")
                    print ("clienthandle1: %s" %clienthandle1)
                    #Config WAN DS Client when RG is enabled
                    if dict["Bridge"] is "RG":
                        WANClientHandle = ixia.ixia_config_l3_staticintf("WAN",**dict)
                    else:
                        WANClientHandle = clienthandle1


                    #Config IGMP Service
                    if dict["McastProfile"] is not "none":
                        IGMPHandler = ixia.ixia_config_igmp(clienthandle1,**dict)
                        if dict["MVREnable"] is "1":
                            IGMPSourceHandle = ixia.ixia_config_mvrintf(**dict)
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
            for dict in Siplist:
                Conf = GeneralConf.copy()
                Conf.update(dict)
                if not e7.e7_add_ont_sipservice(**Conf):
                    cafe.Checkpoint().fail("Add SIP Service Fail!")
                r = e7.e7_check_ont_sipservice(**Conf)
                cafe.Checkpoint(r).not_contains("fail")


            time.sleep(5)
            r = ixia.ixia_controll_start_traffics()

#                time.sleep(20)
#                ixia.stoptraffic()

