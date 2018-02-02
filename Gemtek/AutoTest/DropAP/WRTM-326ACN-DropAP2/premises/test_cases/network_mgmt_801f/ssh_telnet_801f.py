import cafe
import cafe.sessions.session_manager
from cafe.sessions.ssh import *
from cafe.sessions.telnet import *
from premises.test_configs.Gfast_801f.ssh_telnet_801f import *
from time import sleep

__author__ = 'wywang'


@cafe.test_case()
def verify_801f_only_one_ssh_writable():
    """
    @id = 10004NetworkMgmt801F
    test_case 801F/GP-274
    Refactory needed
    """
    sshs1 = SSHSession(SSHConfig["sid"], SSHConfig["host"], SSHConfig["port"],
                                      SSHConfig["user"], SSHConfig["password"])
    sshs1.login()
    sshs1.command("sudo -i")
    result = sshs1.command("ssh " + str(CPEConfig["ip"]))
    cafe.Checkpoint(str(result[2])).verify_contains(exp="password", pos_msg="re found!", neg_msg="re not found")
    result = sshs1.command(str(CPEConfig["password"]))
    cafe.Checkpoint(str(result[2])).verify_regex(exp="BusyBox v\d\.\d\d\.\d", pos_msg="re found!", neg_msg="re not found")
    result = sshs1.command("echo aaa >> 1")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="aaa", pos_msg="re found!", neg_msg="re not found")

    sshs2 = SSHSession(SSHConfig["sid"], SSHConfig["host"], SSHConfig["port"],
                                      SSHConfig["user"], SSHConfig["password"])
    sshs2.login()
    sshs2.command("sudo -i")
    result = sshs2.command("ssh " + str(CPEConfig["ip"]))
    cafe.Checkpoint(str(result[2])).verify_contains(exp="password", pos_msg="re found!", neg_msg="re not found")
    result = sshs2.command(str(CPEConfig["password"]))
    cafe.Checkpoint(str(result[2])).verify_regex(exp="BusyBox v\d\.\d\d\.\d", pos_msg="re found!", neg_msg="re not found")
    result = sshs2.command("echo aaa >> 2")
    result = sshs2.command("cat 2")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="can't open \'2\'", pos_msg="re found!", neg_msg="re not found")

    sshs2.command("rm -rf 1 2")

    sshs1.close()
    sshs2.close()


@cafe.test_case()
def verify_801f_only_one_telnet_writable():
    """
    @id = 10005NetworkMgmt801F
    test_case 801F/GP-274
    Refactory needed
    """
    sshs1 = SSHSession(SSHConfig["sid"], SSHConfig["host"], SSHConfig["port"],
                                      SSHConfig["user"], SSHConfig["password"])
    sshs1.login()
    sshs1.command("sudo -i")
    result = sshs1.command("telnet 192.168.1.1")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="login:", pos_msg="re found!", neg_msg="re not found")
    result = sshs1.command("root")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="assword", pos_msg="re found!", neg_msg="re not found")
    result = sshs1.command("superuser")
    cafe.Checkpoint(str(result[2])).verify_regex(exp="BusyBox v\d\.\d\d\.\d", pos_msg="re found!", neg_msg="re not found")
    result = sshs1.command("echo aaa >> 1")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="aaa", pos_msg="re found!", neg_msg="re not found")

    sshs2 = SSHSession(SSHConfig["sid"], SSHConfig["host"], SSHConfig["port"],
                                      SSHConfig["user"], SSHConfig["password"])
    sshs2.login()
    sshs2.command("sudo -i")
    result = sshs2.command("telnet 192.168.1.1")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="login:", pos_msg="re found!", neg_msg="re not found")
    result = sshs2.command("root")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="assword", pos_msg="re found!", neg_msg="re not found")
    result = sshs2.command("superuser")
    cafe.Checkpoint(str(result[2])).verify_regex(exp="BusyBox v\d\.\d\d\.\d", pos_msg="re found!", neg_msg="re not found")
    result = sshs2.command("echo aaa >> 2")
    cafe.Checkpoint(str(result[2])).verify_contains(exp="can't open \'2\'", pos_msg="re found!", neg_msg="re not found")

    sshs2.command("rm -rf 1 2")

    sshs1.close()
    sshs2.close()

'''@cafe.test_case()
def verify_801f_only_one_telnet_writable():
    """
    @id = 10005NetworkMgmt801F
    test_case 801F/GP-137
    """
    tels1 = TelnetSession(SSHConfig["sid"], SSHConfig["host"], SSHConfig["port"],
                                      SSHConfig["user"], SSHConfig["password"])
    tels1.login()
    tels1.command("telnet 192.168.1.1")
'''