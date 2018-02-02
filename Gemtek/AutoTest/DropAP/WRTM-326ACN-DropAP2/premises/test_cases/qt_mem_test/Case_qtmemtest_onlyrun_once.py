__author__ = 'alu'
import time

import cafe
from stp.premises.library import Teststeplib_ixia as ixia_lib
from cafe.app import App

from stp.premises.library import Teststeplib_e7 as e7_lib
from stp.premises.library import Teststeplib_ont as ont_lib
import re


@cafe.test_case()
def tc_qtmemtest_onlyrun_once():
    """
    id=5442423

    verify the node1 craft interface name
    """
    ontlist = []
    rev10_list = ["BVMCJ00ARA","BVMCH00ARA","BVMCL00ARA","BVMCK00ARA","BVMCK844E1","BVMCK844E2"]
    for key in App().__dict__:
        if re.match(r'DUT\d',key):
            ontlist.append(ont_lib.calixontbase(getattr(App(),key)))

    for ont in ontlist:
        r = ont.ont_get_clei()
        if r:
            print "ONT CLEI is: ",r
            if r in rev10_list:
                for i in range(0,10):
                    result = ont.ont_get_qtmemtest_result
                    ont.ont_reboot_ont()
                    time.sleep(300)
                    cafe.Checkpoint(ont.ont_get_qtmemtest_executed()).exact(True)
                    cafe.Checkpoint(result == ont.ont_get_qtmemtest_result).exact(True)

            else:
                print("This is not a Rev10 unit")
        else:
            print("Can't get CLEI from DUT")

