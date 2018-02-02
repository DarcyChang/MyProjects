import cafe
import re
from premises.library.serial_lib_801f import *
from premises.test_configs.Gfast_801f.serial_801f import *
from time import sleep

__author__ = 'wywang'


@cafe.test_case()
def verify_801f_log_timestamp_format():
    """
    @id = 10001NetworkMgmt801F
    test_case 801F/GP-142
    """
    tels = SerialConsoleTelnetSession(SerialConfig["sid"], SerialConfig["host"], SerialConfig["port"],
                                      SerialConfig["user"], SerialConfig["password"])
    tels.pre_actions()

    # ================case logic========================

    result = tels.command("tail -n 1 /tmp/log/messages")
    result = re.search("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", result[2])
    check = cafe.Checkpoint(str(result.group())).verify_regex(exp="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", pos_msg="re found!",
                                                      neg_msg="re not found")
    if check:
        pass
    else:
        cafe.print_console("check result is: " + str(check) + " " + str(result.group()))
    # ==================================================

    tels.post_actions()


@cafe.test_case()
def verify_801f_version_format():
    """
    @id = 10002NetworkMgmt801F
    test_case 801F/GP-244
    """
    tels = SerialConsoleTelnetSession(SerialConfig["sid"], SerialConfig["host"], SerialConfig["port"],
                                      SerialConfig["user"], SerialConfig["password"])
    tels.pre_actions()

    # ================case logic========================

    result = tels.command("cat /root/version")
    result = re.search("\d\.\d\.\d", result[2])
    cafe.Checkpoint(str(result.group())).verify_regex(exp="\d\.\d\.\d", pos_msg="re found!", neg_msg="re not found")

    # ==================================================

    tels.post_actions()


@cafe.test_case()
def verify_801f_cold_restart_in_60s():
    """
    @id = 10003Performance801F
    test_case 801F/GP-249
    """
    tels = SerialConsoleTelnetSession(SerialConfig["sid"], SerialConfig["host"], SerialConfig["port"],
                                      SerialConfig["user"], SerialConfig["password"])
    tels.pre_actions()

    # ================case logic========================
    result = tels.command("reboot")
    result = re.search("Shutdown network interface", result[2])
    cafe.Checkpoint(str(result.group())).verify_contains(exp="Shutdown network interface", pos_msg="re found!",
                                                         neg_msg="re not found")
    tels.close()
    sleep(30)
    tels = SerialConsoleTelnetSession(SerialConfig["sid"], SerialConfig["host"], SerialConfig["port"],
                                      SerialConfig["user"], SerialConfig["password"])
    cafe.Checkpoint(str(tels)).verify_contains("object at")
    tels.login()
    # ==================================================

    tels.post_actions()
