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
                "Enable":                   "1",
                "ServiceName":              "Data1",
                "Bridge":                   "RG",
                "RGMode":                   "native",
                "WANType":                  "dhcp",
                "PPPUsername":              "Calix",
                "PPPPassword":              "password",
                "RGMgmtProfile":            "PITT-CCFG",
                "RGInstance":               "none",
                "ETH":                      "g1",
                "InVlanSwitch":             "41",
                "InVlan":                   "1501",
                "InPbit":                   "0",
                "InDSCP":                   "0",
                "VLANAction":               "C",
                "OutSVLAN":                 "1501",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "1",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none",
                "IXIA_encapsulation":       "ethernet_ii_vlan",
                "IXIAC_mac_addr":           "00.33.22.11.11.11",
                "DHCPSAddress":             "10.20.0.1",
                "DHCPSMAC":                 "0011.0032.2221",
                "DHCPCAddrStart":           "10.20.0.12",
                "DHCPCAddrCount":           "1",
                "STATICADDRESS":            "192.168.1.136",
                "Gateway":                  "192.168.1.1",
                "MVRServerAddress":         "10.210.100.1",
                "MVRMac":                   "00.05.20.11.11.13",
                "StaticMAC1":               "00.25.0a.11.11.11",
                "StaticMAC2":               "00.37.0a.11.11.21",
        },

"Data2":{
                "Enable":         "1",
                "ServiceName":    "Data2",
                "RGMode":         "no",
                "WANType":        "dhcp",
                "Bridge":         "RG",
                "ETH":            "g2",
                "InVlanSwitch":   "42",
                "InVlan":         "1500",
                "InPbit":         "0",
                "InDSCP":         "0",
                "VLANAction":     "C",
                "OutSVLAN":       "1500",
                "OutSpbit":       "4",
                "OutCVLAN":       "0",
                "OutCpbit":       "0",
                "usciroverride":  "10m",
                "dsciroverride":  "20m",
                "BandWidth":                "BWP_CE_10m_2000_2000_2000",
                "MVREnable":                "0",
                "McastProfile":             "multicast",
                "IXIA_encapsulation":       "ethernet_ii_vlan",
                "IXIAC_mac_addr":           "00.35.22.11.11.13",
                "DHCPSAddress":             "10.21.0.1",
                "DHCPSMAC":                 "0000.0032.2221",
                "STATICADDRESS":            "192.168.1.126",
                "Gateway":                  "192.168.1.1",
                "DHCPCAddrStart":           "10.21.0.12",
                "StaticMac":                "00.38.22.11.10.13",
                "DHCPCAddrCount":           "1",
                "MVR_VLAN":                 "2000",
                "MVRServerAddress":         "10.210.100.1",
                "MVRMac":                   "00.0a.20.11.11.13"
        },
"Data3":{
                "Enable":         "0",
                "ServiceName":    "Data1",
                "Bridge":         "HB",
                "ETH":            "g1",
                "InVlan":         "0",
                "InPbit":         "0",
                "InDSCP":         "0",
                "VLANAction":     "A2",
                "OutSVLAN":       "1503",
                "OutSpbit":       "1",
                "OutCVLAN":       "503",
                "OutCpbit":       "1",
                "usciroverride":  "0",
                "dsciroverride":  "0",
                "BandWidth":      "BWP_BE_1000m_2000_2000_2000",
                "McastProfile":   "none"
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
                "SIPURI":        "6123401122",
                "SIPUsername":   "6123401122",
                "SIPPassword":   "password"
        },
"SIP2":{
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
                "SIPURI":        "6123401123",
                "SIPUsername":   "6123401123",
                "SIPPassword":   "password"
        }
}



