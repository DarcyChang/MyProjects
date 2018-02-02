__author__ = 'alu'
import cafe
import time
from library import Teststeplib_e7 as e7_lib
from library import Teststeplib_ixia as Ixia_lib




@cafe.test_case()
def UserCases1(CaseConf,**GeneralConf):
    """
    id=5442423

    verify the node1 craft interface name
    """

    param = cafe.get_test_param()
    e7 = e7_lib.CalixE7Base(param.e7_sess)
#    ixia = Ixia_lib.IXIABase(**GeneralConf)
    CaseConf = CaseConf
    #import CaseConf as CaseConf

#    if ixia.connect_host():
#        if ixia.connect_chassis():

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



