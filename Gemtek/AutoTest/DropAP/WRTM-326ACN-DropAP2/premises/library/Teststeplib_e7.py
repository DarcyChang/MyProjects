#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cafe.core.logger import CLogger as Logger
from cafe.core.signals import E7_SESSION_ERROR
from cafe.resp.response_map import ResponseMap

import collections
import time

__author__ = 'alu'

#import cafe
#from cafe.resp.response_map import ResponseMap
#from cafe.core.db import TestStep
#from cafe.core.utils import Param
#import re

logger = Logger(__name__)
debug = logger.debug
error = logger.error
debug("importing module %s" % __name__)


class E7Exception(Exception):
    def __init__(self, msg=""):
        logger.exception(msg, signal=E7_SESSION_ERROR)

class CalixE7Base(object):
    """
    base class of E7 interfaces
    """
    def __init__(self, session, session_type=None, e7_type=None, release=None):
        """
        """
        #self.name = name
        self.session = session
        self.session_type = session_type
        self.e7_type = e7_type
        # self.release = release
        self.login()
        self.logger = logger

#    @teststep("send")
    @staticmethod
    def convert_uni_str(data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(CalixE7Base.convert_uni_str, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(CalixE7Base.convert_uni_str, data))
        else:
            return data

    def send(self, cmd="",prompt=None,timeout =3):
        # self.session.write(cmd)
        # r = self.session.expect_prompt(timeout=timeout)
        # return r[2]
        r = self.session.session_command(cmd)
        return r["content"]

    def login(self):
        #self.session.login()
        self.send("set session timeout disable")
        self.send("set session event disable")
        self.send("set session alarm disable")

    def switch_controller(self):
        self.session.write(cmd="switch controller")
        time.sleep(5)

    def show_alarm(self):
        r = self.send("show alarm")
        return r

    #@teststep("checkontstatus")
    def e7_check_ont_status(self, ontid):
        """
        get ont status on e7.

        e7 is the e7 instance of the the testlib
        ontid  is the ont provisioned ID on E7.

        if the ont is enabled, it returns True,else it returns false

        Example:
        | e7_check_ont_status | e7_ins | 203 |

        """

        r = self.send("show ont %s" %ontid)
        if "enable" not in r:
            return False
        else:
            return True


    def e7_sendcmd(self,cmd,prompt=None,timeout =3):
        """
        send cmd and get response
        """
#        param = cafe.get_test_param()
        r = self.send(cmd,prompt=prompt,timeout =timeout)
        if "fail" in r:
            return False
        else:
            return True


    def e7_get_ont_gponport(self,ontid):
        """
        get ont status on e7.

        ontid  is the ont provisioned ID on E7.

        if the ont is
        """
        res = ResponseMap(self.send("show ont %s" %ontid))
        patten = r"(.+Location:\s+)(\d+\S\d+)"
        m = res.table_match(patten)
        if m:
            return m[0][1]
        else:
            return False

    def e7_set_gponport_status(self,gponport,status):
        """
        set gpon port enable or disable
        """
        if self.e7_sendcmd("set gpon-port %s admin-state %s" %(gponport,status)):
            return True
        else:
            return False

    def e7_get_ont_rg_ip(self,ontid):
        """
        get ont rg ip
        """
        res = ResponseMap(self.send("show ont %s" %ontid))
        patten = r"(.+Location:\s+)(\d+\S\d+)"
        m = res.table_match(patten)
        if m:
            return m[0][1]
        else:
            return False

    def e7_retrieve_ontcfg(self,server,location,version,instance,vendor="CXNK"):
        r = self.send("retrieve ont-config server %s user anonymous file-path %s vendor %s version %s instance %s" %(server,location,vendor,version,instance),prompt='\\S')
        #if "ass" in r:
        if r:
            self.e7_sendcmd("password")
            time.sleep(60)
            if self.e7_sendcmd("apply ont-config vendor %s" %(vendor)):
                return True
            else:
                return False
        else:
            return False

    def e7_check_ontcfg(self,instance,version):
        r = self.send("show ont-config instance %s" %(instance))
        if version in r:
            return True
        else:
            return False

    def e7_get_ontcfg_version(self,ontid):
        version = False
        for i in range(0,10):
            res = ResponseMap(self.send("show ont %s detail" %(ontid)))
            patten = r"(.+File\s+Vers\s+:\s+)(\S+)"
            m=res.table_match(patten)
            #patten = r"(.+File\s+Vers\s+:\s+)(\S+)"
            if m:
                version = m[0][1]
                break
            else:
                time.sleep(20)
                print("can't get ont cfg version, try again")
        return version

    def e7_get_ont_rgmode(self,ontid):
        res = ResponseMap(self.send("show ont-port %s/G1 detail" %(ontid)))
        patten = r"(.+nagement\s+Mode\s+:\s+)(\S+)"
        m = res.table_match(patten)
        if m:
            return m[0][1]
        else:
            return False

    def e7_remove_ontcfg(self,instance,vendor="CXNK"):
        if self.e7_sendcmd("remove ont-config vendor %s instance %s" %(vendor,instance)):
            time.sleep(5)
            return True
        else:
            return False

    def e7_set_ont_rgmode(self,ontid,rgmode="external"):
        origin_rgmode = self.e7_get_ont_rgmode(ontid)
        print ("original RG mode is %s" %origin_rgmode)
        if self.e7_sendcmd("set ont-port %s/G1 mgmt-mode %s" %(ontid,rgmode)):
            if rgmode is not origin_rgmode:
                time.sleep(200)
            return True
        else:
            return False

    def e7_set_ont_rginstance(self,ontid,instance):
        if self.e7_sendcmd("set ont-port %s/G1 instance %s" %(ontid,instance)):
            #time.sleep(240)
            return True
        else:
            return False

    def e7_set_ont_mgmt_profile(self,ontid,mgmt_profile):
        if self.e7_sendcmd("set ont-port %s/G1 rg-mgmt-profile %s" %(ontid,mgmt_profile)):
            return True
        else:
            return False


    def e7_provision_ont(self,**ont):
        """
        author:alex lu
        return the provision result. **ont is a dictionary.
        Do actions below:
        1. delete the ONT profile, re-create the ont profile.
        2. provision ont on E7.
        3. return bull value "True" is success, else return "False"

        Dictionary should include values as sample:

        ont ={
                "ontid":          "205",
                "vendor":         "CXNK",
                "ProvisionType":  "SN",
                "SerialNumber":   "28B4AA",
                "Model":           "813G-2",
                "Pots_ports":      "2",
                "FEPorts":         "0",
                "GEPorts":         "4",
                "RG":              "1",
                "FB":              "1",
                "RGdefault":       "y",
                "regid":           "",
        }
        """

#        param = cafe.get_test_param()
#        print id(param.e7_sess)
        Result = True
        if self.e7_sendcmd("show ont-profile %(Model)s" % ont):
            self.e7_sendcmd("delete ont %(ontid)s force" % ont)
            self.e7_sendcmd("delete ont-profile %(Model)s" % ont)
            self.e7_sendcmd("create ont-profile %(Model)s vendor-id %(vendor)s pots-ports %(Pots_ports)s fast-eth-ports %(FEPorts)s "
                       "gig-eth-ports %(GEPorts)s residential-gw-ports %(RG)s full-bridge-ports %(FB)s default-to-rg-mode %(RGdefault)s" % ont)
        for i in range(10):
            r = self.send("show ont discovered serial-number %(SerialNumber)s" % ont)
            if "Serial" in r:
                break
            elif i == 9:
                self.logger.error("Can't discover ONT")
                Result = False
            else:
                time.sleep(10)
        if ont["ProvisionType"] == "SN":
            if not self.e7_sendcmd("create ont %(ontid)s profile %(Model)s serial-number %(SerialNumber)s" % ont):
                self.logger.error("Provision ONT by SerialNumber Fail!")
                Result = False
        else:
            if not self.e7_sendcmd("create ont %(ontid)s profile %(Model)s reg-id %(regid)s" % ont):
                self.logger.error("Provision ONT by regid Fail!")
                time.sleep(10)
        r = self.send("show ont %(ontid)s" % ont)
        if "enable" not in r:
            Result = False
        return Result

    def e7_preparebw(self,bw):
        Result = True
        r = self.send("show bw-profile %s" %bw)
        if "fail" in r:
            bwlist = bw.split('_')
            if bwlist[1] == "BE":
                if not self.e7_sendcmd("create bw-profile %s upstream-pir %s downstream-pir %s upstream-cbs %s upstream-pbs %s downstream-pbs %s" %
                          (bw,bwlist[2],bwlist[2],bwlist[3],bwlist[4],bwlist[5])):
                    Result = False
            else:
                if not self.e7_sendcmd("create bw-profile %s upstream-cir %s upstream-cbs %s upstream-pbs %s downstream-pbs %s" %
                          (bw,bwlist[2],bwlist[3],bwlist[4],bwlist[5])):
                    Result = False
        return Result

    def e7_prepare_tagaction(self,**data):
        Result = True
        r = self.send("show svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s" %data)
        if "fail" in r:
            matchlist = data["InVlan"]
            matchpbit = data["InPbit"]
            if data["InVlan"] == "0":
                if data.has_key("untagmatchlist"):
                    matchlist = data["untagmatchlist"]
                else:
                    matchlist = "all_untag"
            else:
                if data["InPbit"] == "0":
                    matchpbit = "any"
                    matchlist = "%(InVlan)s" %data

                else:
                    matchlist = "%(InVlan)s_%(InPbit)s" %data

            data["matchpbit"] = matchpbit
            data["matchlist"] = matchlist
            if not self.e7_sendcmd("show vlan %(InVlan)s" %data):
                if not self.e7_sendcmd("create vlan %(InVlan)s" %data):
                    Result = False
            if not self.e7_sendcmd("show svc-match-list %s" %matchlist):
                if not self.e7_sendcmd("create svc-match-list %s" %matchlist):
                    Result = False
                if not self.e7_sendcmd("add tagged-rule to-svc-match-list %(matchlist)s vlan %(InVlan)s p-bit %(matchpbit)s" %data):
                    Result = False

            if data["VLANAction"] == "C":
                if not self.e7_sendcmd("create svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s "
                                        "type change-tag outer use-svc-vlan svc-match-list %(matchlist)s use-p-bit %(OutSpbit)s" %data):
                    Result = False
            elif data["VLANAction"] == "A":
                if not self.e7_sendcmd("create svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s "
                                        "type add-tag outer use-svc-vlan svc-match-list %(matchlist)s use-p-bit %(OutSpbit)s" %data):
                    Result = False
            elif data["VLANAction"] == "A2":
                if not self.e7_sendcmd("create svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s type add-2-tag outer use-svc-vlan inner use-svc-vlan"
                                        " svc-match-list %(matchlist)s use-p-bit %(OutSpbit)s use-inner-p-bit %(OutCpbit)s" %data):
                    Result= False
            elif data["VLANAction"] == "AnC":
                if not self.e7_sendcmd("create svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s type add-and-change outer use-svc-vlan inner use-svc-vlan"
                                        " svc-match-list %(matchlist)s use-p-bit %(OutSpbit)s use-inner-p-bit %(OutCpbit)s" %data):
                    Result = False

        return Result


    def e7_add_ont_dataservice(self,**conf):
        """
        author:alex lu
        Add L2 or L3 Data or viedo Service on ONT.
        Do actions below:
        1. Check ONT status
        2. Check if the service is enabled/disabled
        3.Check bandwidth profile.If no, add profile.
        4.Check tag action profile.if no, add profile.
        5.Check if it is RG service of L2 service.
        6.Rerurns True if success, else return False.

        The dictionary should at least include:

        Data1={
                "Enable":                   "1",   -----if "0",do not add the data service
                "ServiceName":              "Data1",
                "Bridge":                   "HB",  -----"HB","RG" or "FB"
                "RGMode":                   "no",  -----"no" means not in RG. if in RG, it should be "native" or "external"
                "WANType":                  "dhcp",-----Only work in RG mode."dhcp" or "pppoe"
                "PPPUsername":              "Calix",----Only works in pppoe mode
                "PPPPassword":              "password",
                "RGMgmtProfile":            "PITT-CCFG",-----Only works in RG mode.
                "RGInstance":               "none", -----Only works in RG mode
                "ETH":                      "g3",   -----uplink eth port
                "VLANAction":               "C",    -----C: change tag.Anc:Add and change tag.A2: Add 2 tags A:Add tag
                "InVlan":                   "13",
                "InPbit":                   "0",
                "InDSCP":                   "0",
                "untagmatchlist":           "all_untag",
                "OutSVLAN":                 "1503",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "0",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none",------"none" means multicast is disabled. if enable multicast, input a valid multicast profile

        },
        """
        Result = True
        dict ={
            "ontid":                    "",
            "Enable":                   "1",
            "ServiceName":              "Data1",
            "Bridge":                   "HB",
            "RGMode":                   "no",
            "WANType":                  "dhcp",
            "PPPUsername":              "Calix",
            "PPPPassword":              "password",
            "RGMgmtProfile":            "PITT-CCFG",
            "RGInstance":               "none",
            "ETH":                      "g3",
            "VLANAction":               "C",
            "InVlan":                   "13",
            "InPbit":                   "0",
            "InDSCP":                   "0",
            "untagmatchlist":           "all_untag",
            "OutSVLAN":                 "1503",
            "OutSpbit":                 "1",
            "OutCVLAN":                 "0",
            "OutCpbit":                 "0",
            "usciroverride":            "0",
            "dsciroverride":            "0",
            "BandWidth":                "BWP_BE_1000m_none_none_none",
            "McastProfile":             "none"
        }
#        dict = conf.copy()
        dict.update(conf)
        dict = CalixE7Base.convert_uni_str(dict)
        if self.e7_check_ont_status(dict["ontid"]):
            if dict["Enable"]is not "1":
                self.logger.info("this data service is disabled")
            else:
                if not self.e7_preparebw(dict["BandWidth"]):
                    Result = False
                elif not self.e7_prepare_tagaction(**dict):
                    Result = False
                else:
                    if dict["Bridge"] is not "RG":
                        if not self.e7_sendcmd("remove ont-port %(ontid)s/%(ETH)s from-res-gw %(ontid)s/G1" %dict):
                            pass
                            #Result = False
                        elif dict["Bridge"] is "FB":
                            if self.e7_sendcmd("add ont-port %(ontid)s/%(ETH)s to-full-bridge %(ontid)s/F1" %dict):
                                dict["ETH"] = "F1"
                                Result = True
                    else:
                        dict["ETH"] = "G1"
                        if dict["RGMode"] is "native" or dict["RGMode"] is "external":
                            self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s mgmt-mode %(RGMode)s" %dict)
                            if dict["RGMode"]is "native":
                                if dict["WANType"] is "pppoe":
                                    self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s wan-protocol pppoe pppoe-username %(PPPUsername)s pppoe-password %(PPPPassword)s" %dict)
                                else:
                                    self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s wan-protocol dhcp" %dict)

                            self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s rg-mgmt-profile %(RGMgmtProfile)s" %dict)
                            self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s instance %(RGInstance)s" %dict)

                    if dict["VLANAction"] is "A" or dict["VLANAction"] is "C":
                        if not self.e7_sendcmd("add eth-svc %(ServiceName)s to-ont-port %(ontid)s/%(ETH)s bw-profile %(BandWidth)s svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s outer-vlan %(OutSVLAN)s mcast-profile %(McastProfile)s us-cir-override %(usciroverride)s us-pir-override %(dsciroverride)s" %dict):
                            Result = False
                    else:
                        if not self.e7_sendcmd("add eth-svc %(ServiceName)s to-ont-port %(ontid)s/%(ETH)s bw-profile %(BandWidth)s svc-tag-action "
                                            "%(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s outer-vlan %(OutSVLAN)s "
                                            "us-cir-override %(usciroverride)s us-pir-override %(dsciroverride)s inner-vlan %(OutCVLAN)s mcast-profile %(McastProfile)s" %dict):
                            Result = False
        else:
            Result = False
        return Result

    def e7_del_ont_dataservice(self,**dict):
        """
        author:alex lu
        Add L2 or L3 Data or viedo Service on ONT.
        Do actions below:
        1. Check ONT status
        2. Check if the service is enabled/disabled
        3.Check bandwidth profile.If no, add profile.
        4.Check tag action profile.if no, add profile.
        5.Check if it is RG service of L2 service.
        6.Rerurns True if success, else return False.

        The dictionary should at least include:

        Data1={
                "Enable":                   "1",   -----if "0",do not add the data service
                "ServiceName":              "Data1",
                "Bridge":                   "HB",  -----"HB","RG" or "FB"
                "RGMode":                   "no",  -----"no" means not in RG. if in RG, it should be "native" or "external"
                "WANType":                  "dhcp",-----Only work in RG mode."dhcp" or "pppoe"
                "PPPUsername":              "Calix",----Only works in pppoe mode
                "PPPPassword":              "password",
                "RGMgmtProfile":            "PITT-CCFG",-----Only works in RG mode.
                "RGInstance":               "none", -----Only works in RG mode
                "ETH":                      "g3",   -----uplink eth port
                "VLANAction":               "C",    -----C: change tag.Anc:Add and change tag.A2: Add 2 tags A:Add tag
                "InVlan":                   "13",
                "InPbit":                   "0",
                "InDSCP":                   "0",
                "untagmatchlist":           "all_untag",
                "OutSVLAN":                 "1503",
                "OutSpbit":                 "1",
                "OutCVLAN":                 "0",
                "OutCpbit":                 "0",
                "usciroverride":            "0",
                "dsciroverride":            "0",
                "BandWidth":                "BWP_BE_1000m_none_none_none",
                "McastProfile":             "none",------"none" means multicast is disabled. if enable multicast, input a valid multicast profile

        },
        """
        Result = True
#        dict = ont.copy()
#        dict.update(data)
        if self.e7_check_ont_status(dict["ontid"]):
            if dict["Enable"]is not "1":
                self.logger.info("this data service is disabled")
            else:
                if not self.e7_preparebw(dict["BandWidth"]):
                    Result = False
                elif not self.e7_prepare_tagaction(**dict):
                    Result = False
                else:
                    if dict["Bridge"] is not "RG":
                        if not self.e7_sendcmd("remove ont-port %(ontid)s/%(ETH)s from-res-gw %(ontid)s/G1" %dict):
                            Result = False
                        elif dict["Bridge"] is "FB":
                            if self.e7_sendcmd("add ont-port %(ontid)s/%(ETH)s to-full-bridge %(ontid)s/F1" %dict):
                                dict["ETH"] = "F1"
                                Result = True
                    else:
                        dict["ETH"] = "G1"
                        if dict["RGMode"] is "native" or dict["RGMode"] is "external":
                            self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s mgmt-mode %(RGMode)s" %dict)
                            if dict["RGMode"]is "native":
                                if dict["WANType"] is "pppoe":
                                    self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s wan-protocol pppoe pppoe-username %(PPPUsername)s pppoe-password %(PPPPassword)s" %dict)
                                else:
                                    self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s wan-protocol dhcp" %dict)

                            self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s rg-mgmt-profile %(RGMgmtProfile)s" %dict)
                            self.e7_sendcmd("set ont-port %(ontid)s/%(ETH)s instance %(RGInstance)s" %dict)

                    if dict["VLANAction"] is "A" or dict["VLANAction"] is "C":
                        if not self.e7_sendcmd("add eth-svc %(ServiceName)s to-ont-port %(ontid)s/%(ETH)s bw-profile %(BandWidth)s svc-tag-action "
                                            "%(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s outer-vlan %(OutSVLAN)s mcast-profile %(McastProfile)s "
                                            "us-cir-override %(usciroverride)s us-pir-override %(dsciroverride)s" %dict):
                            Result = False
                    else:
                        if not self.e7_sendcmd("add eth-svc %(ServiceName)s to-ont-port %(ontid)s/%(ETH)s bw-profile %(BandWidth)s svc-tag-action "
                                            "%(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s outer-vlan %(OutSVLAN)s "
                                            "us-cir-override %(usciroverride)s us-pir-override %(dsciroverride)s inner-vlan %(OutCVLAN)s mcast-profile %(McastProfile)s" %dict):
                            Result = False
        else:
            Result = False
        return Result

    def e7_add_ont_sipservice(self,**dict):
        """
        author:alex lu
        Add L2 SIP Service on ONT
        dict sample:
        SIP ={
                "Enable":         "1",,
                "ETH":            "p1",
                "VLANAction":     "A2",
                "OutSVLAN":       "1503",
                "OutSpbit":       "1",
                "OutCVLAN":       "503",
                "OutCpbit":       "1",
                "SIPInstance":   "none",
                "SIPProfile":    "PITT-SIP",
                "DialPlan":      "ST-PREM",
                "SIPURI":        "6123401122",
                "SIPUsername":   "6123401122",
                "SIPPassword":   "password"
        }
        """
        Result = True
        if self.e7_check_ont_status(dict["ontid"]):
            if dict["Enable"]== "1":
                if not self.e7_prepare_tagaction(**dict):
                    Result = False
                else:
                    if dict["VLANAction"] is "A" or dict["VLANAction"] is "C":
                        if not self.e7_sendcmd("set ont %(ontid)s ip-host sip svc-tag-action "
                                            "%(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s outer-vlan %(OutSVLAN)s config-file-instance %(SIPInstance)s" %dict):
                            Result = False
                    else:
                        if not self.e7_sendcmd("set ont %(ontid)s ip-host sip svc-tag-action %(VLANAction)s_Sp%(OutSpbit)s_Cp%(OutCpbit)s_M%(InVlan)sp%(InPbit)s "
                                                "outer-vlan %(OutSVLAN)s inner-vlan %(OutCVLAN)s config-file-instance %(SIPInstance)s" %dict):
                            Result = False
                    if not self.e7_sendcmd("add sip-svc to-ont-port %(ontid)s/%(ETH)s sip-gw-profile %(SIPGWProfile)s user %(SIPUsername)s password %(SIPPassword)s uri %(SIPURI)s dial-plan %(DialPlan)s admin-state enabled" %dict):
                        Result = False
        else:
            Result = False
        return Result



    def e7_check_ont_dataservice(self,**dict):
        if dict["Enable"] is "1":
            if dict["Bridge"] is "FB":
                dict["ETH"] = "F1"
            elif dict["Bridge"] is "RG":
                dict["ETH"] = "G1"
            r = self.e7_sendcmd("show ont-port %(ontid)s/%(ETH)s eth-svc %(ServiceName)s" %dict)

        else:
            r = True
        return r


    def e7_check_ont_sipservice(self,**dict):
        r = self.e7_sendcmd("show ont-port %(ontid)s/%(ETH)s sip-svc" %dict)
        return r
