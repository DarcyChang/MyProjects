from cafe.core.logger import CLogger as Logger
from cafe.core.signals import SESSION_TELNET_ERROR
from cafe.resp.response_map import ResponseMap

import re
import time

__author__ = 'alu'
#import cafe
#from cafe.core.db import TestStep
#from cafe.core.utils import Param

logger = Logger(__name__)
debug = logger.debug
error = logger.error
debug("importing module %s" % __name__)



class ontexception(Exception):
    def __init__(self, msg=""):
        logger.exception(msg, signal=SESSION_TELNET_ERROR)



class calixontbase(object):
    """
    base class of ont interfaces
    """
    def __init__(self, session, session_type=None, ont_type=None):
        """
        """
        #self.name = name
        self.session = session
        self.session_type = session_type
        self.ont_type = ont_type
        self.logger = logger

    def ont_send(self, cmd="", timeout=3):
        # self.session.write(cmd)
        # # return tuple (prompt index, <prompt re match object>, text)
        # r = self.session.expect_prompt(timeout=timeout)
        r = self.session.cli(cmd,timeout=timeout)
        return r["value"]

    # def send(self,cmd,prompt=None,timeout=None, newline=None, action=None):
    #     p = None
    #     if prompt is not None:
    #         p = {prompt: action}
    #
    #     result = self.session.session_command(cmd, p, timeout, newline)
    #     return result['content']

    def set_800ont_climode(self, climode ="sh"):
        """set the cli into specific mode. default climode is "sh"
        if need to switch to bcm mode, set climode to "bcm"
        """
        repeat = True
        if climode == "sh":
            if "Version" in self.ont_send("ver"):
                repeat = False
            while repeat == True:
                r = self.ont_send("sh")
                if "BusyBox" in r:
                    repeat = True
                    break
                time.sleep(1)
        else:
            if "error" in self.ont_send("ver"):
                repeat = False
            while repeat == True:
                r = self.ont_send("exit")
                if "restart" in r:
                    repeat = True
                    break
                time.sleep(1)

    def ont_get_ver(self):
        self.set_800ont_climode("sh")
        r = ResponseMap(self.ont_send("ver"))
        patten = r"(.+Ver:\s+)(\d+\.\d+\.\d+\.\d+)"
        m = r.table_match(patten)
        return m[0][1]
        if m:
            return m[0][1]
        else:
            return False

    def ont_restore_default(self):
        self.set_800ont_climode("bcm")
        r = self.ont_send("restoredefault",timeout=20)
        return True


    def ont_get_clei(self):
        self.set_800ont_climode("sh")
        r = ResponseMap(self.ont_send("dtshell_900 bdinfo"))
        patten = r"(.+CLEI:\s+)(\S+)"
        m = r.table_match(patten)
        if m:
            return m[0][1]
        else:
            return False

    def ont_get_ipaddress(self, interface):
        self.set_800ont_climode("sh")
        r = ResponseMap(self.ont_send("ifconfig %s" % interface))
        patten = r"(.+net\s+addr:\s*)(\d+\.\d+\.\d+\.\d+)(.*)"
        m = r.table_match(patten)
        if m:
            return m[0][1]
        else:
            return False

    def ont_get_qtmemtest_executed(self):
        self.set_800ont_climode()
        if "memtestresult" in self.ont_send("ls /calix/sys/qtn"):
            return True
        else:
            return False

    def ont_get_qtmemtest_result(self):
        self.set_800ont_climode("bcm")
        res = self.ont_send("calixdebug qtmemtest")
        if "memtestresult:pass" in res:
            if "QUANTENNA_MEMTEST_PASSED" in res:
                result = True
            else:
                result = None
        elif "memtestresult:fail" in res:
            result = False
        else:
            result = None
        return result
        # res = ResponseMap(res)
        # patten = r"(memtestresult:)(\D+)"
        # m = res.table_match(patten)
        # return m

    def ont_reboot_ont(self):
        self.ont_send("reboot")

    def ont_del_qtmemtest_result(self):
        """delete the QT memory test result.

        """
        self.set_800ont_climode()
        if "memtestresult" in self.ont_send("ls /calix/sys/qtn"):
            self.ont_send("rm /calix/sys/qtn/memtestresult.txt")

    def ont_gen_url(self,br0_ip,url):
        gen_url = "http://"+ br0_ip +"/" +url
        return gen_url

    def ont_getvalue_by_name(self,name,cmd,climode="sh"):
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
        self.set_800ont_climode(climode)
        r = self.ont_send(cmd)
        self.logger.info("output:%s" %r)
        r = ResponseMap(self.ont_send(cmd))
        self.logger.info("output:%s" %r)
        #patten = r"(\s*%s[=:.\s]+)(\S+)" %name
        patten = r"(\s*%s[=:.\s]+)(\S+)" %name
        self.logger.info("patten:%s" %patten)
        m = r.table_match(patten)
        self.logger.info("m:%s" %m)
        if m:
            return m[0][1]
        else:
            return False

    def ont_format_string(self,origin_value,symbol):
        new_value = origin_value.replace(symbol,'')
        return new_value

    def ont_get_intf_mac(self,intf_name):
        """Returns the MAC value of the specific interface.

        """
        self.set_800ont_climode("sh")
        r = ResponseMap(self.ont_send("ifconfig %s" % intf_name))
        patten = {"hwaddress": {"regex":r"HWaddr (\S+)(\s+)","group": 1}}
        m = r.pattern_match(patten)
        print m
        if m:
            return m["hwaddress"]
        else:
            return False

    def ont_check_by_tablematch(self,reg,cmd,climode="sh"):
        """if match, return True, else return False.

        """
        self.set_800ont_climode(climode)
        r = ResponseMap(self.ont_send(cmd))
        patten = r"(%s)" %reg
        m = r.table_match(patten)
        if m:
            return True
        else:
            return False

    def ont_set_mdm_pv(self,pv,value):
        """if match, return True, else return False.

        """
        self.set_800ont_climode("bcm")
        result = self.ont_send("mdm setpv %s %s" %(pv,value))
        time.sleep(2)
        r = self.ont_send("mdm getpv %s" %(pv))
        if value in r:
            return True
        else:
            return False

    def ont_get_mdm_pv(self,pv):
        """if get value, return value, else return False.

        """
        r = self.ont_getvalue_by_name("Param value","mdm getpv %s" %pv,"bcm")
        return r

    def ont_get_br0_member(self):
        self.set_800ont_climode("sh")
        r = ResponseMap(self.ont_send("brctl show"))
        patten = r"(.*\s+eth.+)"
        m = r.table_match(patten)
        list = []
        for item in m:
            re_result = re.match(r'(br0\s+.+\s+.+\s+)(eth.+)',item[0])
            if re_result:
                list.append(re_result.group(2))
            else:
                re_result = re.match(r'(\s+)(eth.+)',item[0])
                if re_result:
                    list.append(re_result.group(2))

        return list