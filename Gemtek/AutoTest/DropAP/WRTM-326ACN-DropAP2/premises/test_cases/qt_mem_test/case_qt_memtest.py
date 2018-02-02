__author__ = 'alu'
import time

import cafe
from stp.premises.library import Teststeplib_ixia as ixia_lib
from cafe.app import App

from stp.premises.library import Teststeplib_e7 as e7_lib
from stp.premises.library import Teststeplib_ont as ont_lib
import re

@cafe.test_case()
def tc_qtmemtest_onlyrun_rev10unit():
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
                cafe.Checkpoint(ont.ont_get_qtmemtest_executed()).exact(True)
            else:
                cafe.Checkpoint(ont.ont_get_qtmemtest_executed()).exact(False)
        else:
            print("Can't get CLEI from DUT")


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


@cafe.test_case()
def tc_qtmemtest_duration():
    """
    id=5442423

    verify the node1 craft interface name
    """
    ontlist = []
    for key in App().__dict__:
        if re.match(r'DUT3|DUT5',key):
            ontlist.append(ont_lib.calixontbase(getattr(App(),key)))

    for ont in ontlist:
        r = ont.ont_get_ver()
        print "ONT Version is: ",r
        cafe.Checkpoint(r).contains("11")
        result = ont.ont_get_qtmemtest_result()
        print(result)
        stable_result = result
        if stable_result == True:
            sleep_time = 650
        else:
            sleep_time = 300
        errnum = 0
        passnum = 0
        for i in range(1,10):
            ont.ont_del_qtmemtest_result()
            ont.ont_reboot_ont()
            time.sleep(sleep_time)
            result = ont.ont_get_qtmemtest_result()
            print("result:",result)
            print("stable_result:",stable_result)
            if result == stable_result:
                passnum = passnum + 1
                print("Pass counts:",passnum)

            else:
                errnum = errnum +1
                print("error counts:",errnum)
        cafe.Checkpoint(errnum).exact(0)

