#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cafe.core.logger import CLogger
from cafe.resp.response_map import ResponseMap
from Teststeplib_e7 import CalixE7Base as testlib_e7
from Teststeplib_ont import calixontbase as testlib_800ont
from Teststeplib_ixia import IXIABase as testlib_ixia
from caferobot.util.forward import caller_transfer
from cafe.app import App

__author__ = 'alu'

class adapter_e7(object):

    def __init__(self):
        pass

    @staticmethod
    def build_e7_testlib(connection_name):
        session = getattr(App(),connection_name)
        return testlib_e7(session)

    @staticmethod
    @caller_transfer()
    def e7_sendcmd(e7,cmd):
        pass

    @staticmethod
    @caller_transfer()
    def e7_check_ont_status(e7,ontid):
        pass

    @staticmethod
    @caller_transfer()
    def e7_provision_ont(e7,**conf):
        pass

    @staticmethod
    @caller_transfer()
    def e7_remove_ontcfg(e7,instance,vendor="CXNK"):
        pass

    @staticmethod
    @caller_transfer()
    def e7_set_ont_rgmode(e7,ontid,rgmode="external"):
        pass

    @staticmethod
    @caller_transfer()
    def e7_retrieve_ontcfg(e7,server,location,version,instance,vendor="CXNK"):
        pass

    @staticmethod
    @caller_transfer()
    def e7_check_ontcfg(e7,instance,version):
        pass

    @staticmethod
    @caller_transfer()
    def e7_set_ont_rginstance(e7,ontid,instance):
        pass

    @staticmethod
    @caller_transfer()
    def e7_set_ont_mgmt_profile(e7,ontid,mgmt_profile):
        pass

    @staticmethod
    @caller_transfer()
    def e7_get_ontcfg_version(e7,ontid):
        pass


    @staticmethod
    def e7_add_ont_rg_service(e7,ontid,InVlan,OutSVLAN,VLANAction="C",*args,**dict):

        config = {
                "ontid":   ontid,
                "VLANAction":VLANAction,
                "InVlan":InVlan,
                "OutSVLAN":OutSVLAN,
                "ServiceName":"Data1",
                "RGMode":"native",
                "WANType":"dhcp",
                "Bridge":"RG",
                "OutSpbit":                 "6",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "0",
                "usciroverride":            "100m",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none"
            }
        if dict:
            config = config.update(dict)

        result = e7.e7_add_ont_dataservice(**config)
        return result

    @staticmethod
    def e7_add_ont_2ndrg_service(e7,ontid,InVlan,OutSVLAN,VLANAction="C",*args,**dict):

        config = {
                "ontid":   ontid,
                "VLANAction":VLANAction,
                "InVlan":InVlan,
                "OutSVLAN":OutSVLAN,
                "ServiceName":"Data2",
                "RGMode":"native",
                "WANType":"dhcp",
                "Bridge":"RG",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "0",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none"
            }
        if dict:
            config = config.update(dict)

        result = e7.e7_add_ont_dataservice(**config)
        return result

    @staticmethod
    def e7_add_ont_l2_service(e7,ontid,InVlan,OutSVLAN,ETH,VLANAction="A",*args,**dict):

        config = {
                "ontid":   ontid,
                "VLANAction":VLANAction,
                "InVlan":InVlan,
                "OutSVLAN":OutSVLAN,
                "ETH":ETH,
                "ServiceName":"Data1",
                "RGMode":"no",
                "WANType":"dhcp",
                "Bridge":"HB",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "0",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none"
            }
        if dict:
            config = config.update(dict)

        result = e7.e7_add_ont_dataservice(**config)
        return result

    @staticmethod
    def e7_add_ont_l2_ctag_service(e7,ontid,InVlan,OutSVLAN,ETH,ServiceName,VLANAction="C",*args,**dict):

        config = {
                "ontid":   ontid,
                "VLANAction":VLANAction,
                "InVlan":InVlan,
                "OutSVLAN":OutSVLAN,
                "ETH":ETH,
                "ServiceName":ServiceName,
                "RGMode":"no",
                "WANType":"dhcp",
                "Bridge":"HB",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "0",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none"
            }
        if dict:
            config = config.update(dict)

        result = e7.e7_add_ont_dataservice(**config)
        return result

class adapter_800ont(object):

    def __init__(self):
        pass

    @staticmethod
    def build_800ont_testlib(connection_name):
        session = getattr(App(),connection_name)
        return testlib_800ont(session)

    @staticmethod
    def combine_string(str1,str2):
        combined_str = str1 + str2

    @staticmethod
    @caller_transfer()
    def set_800ont_climode(ont,climode = "sh"):
        pass

    @staticmethod
    @caller_transfer()
    def ont_get_ver(ont):
        pass

    @staticmethod
    @caller_transfer()
    def ont_restore_default(ont):
        pass

    @staticmethod
    @caller_transfer()
    def ont_send(ont,cmd):
        pass

    @staticmethod
    @caller_transfer()
    def ont_gen_url(ont,br0_ip,url):
        pass

    @staticmethod
    @caller_transfer()
    def ont_getvalue_by_name(ont,name,cmd,climode="sh"):
        """Returns the value of the specific parameter name.

        cli is default as sh. if need to use bcm shell, please set climode as "bcm"
        for example, need to get version by cmd "ver"":
        ~ # ver
        Calix ONT 813G-2
            GigEth ports:    4
            POTS ports:      2       Slic:LE9540
            RF ports:        0
            Wireless-1:      MFG:BCM, FREQ:2.4GHz, Firmware:V1.2
            Wireless-2:      MFG:QNT, FREQ:5.0GHz, Firmware:v37.3.0.50(acR3.2.1)
            MFG S/N:         261508000141
            FSAN S/N:        CXNK0028B4AA
            SW Release Ver:  11.1.110.5
            Kernel Version:  Linux 3.4.11-rt19 Feb 24 2016 mips GNU/Linux
        Running    : 11.1.110.5
        ~ #
        so the name is "Running", cmd is "ver", climode is default"sh"
        """
        pass

    @staticmethod
    @caller_transfer()
    def ont_format_string(ont,origin_mac,symbol):
        pass

    @staticmethod
    @caller_transfer()
    def ont_get_intf_mac(ont,intf_name):
        pass

    @staticmethod
    @caller_transfer()
    def ont_check_by_tablematch(ont,reg,cmd,climode="sh"):
        pass

    @staticmethod
    @caller_transfer()
    def ont_get_ipaddress(ont,interface):
        pass

    @staticmethod
    @caller_transfer()
    def ont_set_mdm_pv(ont,param,value):
        pass


    @staticmethod
    @caller_transfer()
    def ont_get_mdm_pv(ont,param):
        pass

    @staticmethod
    @caller_transfer()
    def ont_get_br0_member(ont):
        pass

class adapter_ixia(object):

    def __init__(self):
        pass

    @staticmethod
    def build_ixia_testlib(tg_session):
        session = getattr(App(),tg_session)
        return testlib_ixia(session)