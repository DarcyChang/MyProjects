__author__ = 'glivermo'

import cafe
# from selenium.webdriver.common.keys import Keys
from cafe.core.logger import init_logging
from stp.equipment.calix.e7 import E7ApiClass
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from stp.equipment.ixia.OLD_ixveriwave import IxVeriwaveClass
from cafe.sessions.winexe import WinExeSession
import time
import stp.api.e7.e7_lib

# Load config.ini file when not executing from command prompt - default location for Gayle written test suites
if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("../config/config.ini")


# ######################################################################################################################
# Build topology connections via XConnect structure
# ######################################################################################################################


def build_topology(params, topology):
    """
    Description:
        Build topology connections required for test suite. All session control within function.
        Making the assumption that all XConns are via mgmt_vlan IP and session type is telnet.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
        NA
    """
    # Get a list of all XConn nodes
    xconn_node_list = []
    keyvalues = params.keys()
    for key in keyvalues:
        if key[0] == "X":
            # Add end point A XConnect to node list if not already there
            if params[key]['xconna'] not in xconn_node_list:
                xconn_node_list.append(params[key]['xconna'])

            # Add end point B XConnect to node list if not already there
            if params[key]['xconnb'] not in xconn_node_list:
                xconn_node_list.append(params[key]['xconnb'])
    # print("xconn_node_list : ", xconn_node_list)

    # Extract session information, create session, and login to each XConn node
    xconn_info = {}
    for xconn in xconn_node_list:
        xconn_info[xconn] = {'profile': topology.nodes[xconn]['session_profile']['mgmt_vlan']['telnet']}
        xconn_info[xconn] = {'session': E7ApiClass(params.session_mgr.create_session(xconn, 'telnet',
                                                                                     **xconn_info[xconn]['profile']),
                                                   eq_type="E7")}
        # TODO error checking needed for when session cannot be started
        xconn_info[xconn]['session'].login()
        # TODO error checking needed for when login fails

    # Build XConnects
    # x1 = params['X1']
    # print("x1: ", x1)
    # checkpoint = stp.api.e7.e7_lib.lib_create_nl2nlringxconn(p_description="x1",
    #                                             p_xconna_sess=xconn_info[x1['xconna']]['session'],
    #                                             p_xconna_int=x1['xconnaint'],
    #                                             p_xconnb_sess=xconn_info[x1['xconnb']]['session'],
    #                                             p_xconnb_int=x1['xconnbint'],
    #                                             p_tlsvlan=x1['tlsvlan'],
    #                                             p_nativevlan=x1['nativevlan'])

    # p_xconna_sess=xconn_info[x1['xconna']]['session'].show_tag_actions()

    # print("Status of building xconn pipe: ", checkpoint)

    # TODO error checking to verify if removal needed
    # Remove each session
    for xconn in xconn_node_list:
        params.session_mgr.remove_session(xconn)


# ######################################################################################################################
# Remove topology connections via XConnect structure
# ######################################################################################################################


def remove_topology():
    """
    Description: Remove topology connections required for test suite. All session control within function.

    Args:

    Returns:
    """
    # Obtain parameter file information
    param = cafe.Param({})
    # TODO Modify to take filename directly from cafe config file
    param.load_ini("/opt/home/glivermo/stp/stp/test_beds/sandbox/ts_xconn_demo_parms.ini")
    print("param :", param)


# ######################################################################################################################
# Open sessions for test execution
# ######################################################################################################################

def open_sessions(params, topology):
    """
    Description:
    Args:
    Returns:
    """
    # Open E7 Session(s) - opens sessions to all E7 DUTs in parameter file
    # e7_node_list = params.e7.keys()
    # for e7_node in e7_node_list:
    #     params['e7'][e7_node + '_profile'] = \
    #         topology['nodes'][params['e7'][e7_node]]['session_profile']['mgmt_vlan']['telnet']
    #     params['e7'][e7_node + '_session'] = \
    #         E7ApiClass(params.session_mgr.create_session(params['e7'][e7_node], 'telnet',
    #                                                      **params['e7'][e7_node + '_profile']),
    #                    eq_type="e7")
    #     params['e7'][e7_node + '_session'].login()

    # Open ONT GUI Session(s)
    params['ontgui']['ontgui_session'] = ONTGuiApiClass(sid="ONTMgmt", logfile="web.log")
    params['ontgui']['ontgui_session'].login(ontip=params.ontgui.ontgui, username="support", password="support")

    # # Open IxVeriwave Managing PC Session
    # params['ixvw']['ixvwpcsession'] = IxVeriwaveClass(winhost=params['ixvw']['ixvwpcip'],
    #                                                   winuser=params['ixvw']['ixvwpclogin'],
    #                                                   winpassword=params['ixvw']['ixvwpcpassword'],
    #                                                   timeout=60,
    #                                                   tcl_shell="tclsh.exe")
    #
    # # OLD Way of Logging in
    # params['ixvw']['ixvwpcsession'].login()

# ######################################################################################################################
# Close sessions for test execution
# ######################################################################################################################

def close_sessions(params, topology):
    """
    Description:
    Args:
    Returns:
    """
    # Close E7 Session(s) - all that are listed as DUTs in parameter file
    # e7_node_list = params['e7'].keys()
    # for e7_node in e7_node_list:
    #     # params.session_manager.remove_session(session_name=[params['E7'][e7]])
    #     params.session_mgr.remove_session(params['e7'][e7_node])
    #     # params['E7'][e7]['session'].remove_session()

    # Close ONT GUI Session(s)
    params['ontgui']['ontgui_session'].close()

    # Close IxVeriwave Managing PC Session
    # params['ixvw']['ixvwpcsession'].close()

# ######################################################################################################################
# Test Cases
# ######################################################################################################################


@cafe.test_case()
def e7_test_case(dut):

    print("Hello! I am a test case!")
    cafe.Checkpoint("Pass me please").verify_exact("Pass me please")

    # Simple display of system version
    # v1 = session1.command("show version")[2]
    # dut1_ver = stp.api.e7.e7_lib.show_version(dut1)
    resp = dut.show_version()
    print("dut_ver: ", resp)
    resp = dut.show_system()
    print("show system: ", resp)
    # print("response type: ",type(dut_ver))
    # version = v1
    # cp_version = cafe.Checkpoint(version)
    # cp_version.contains(title="e7 version:",
    #                     exp="2.4.3.9"
    #                     )


@cafe.test_case()
def e7gui_test_case(params):

    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan1']

    print("Hello! I am a test case!")
    cafe.Checkpoint("Pass me please").verify_exact("Pass me please")

    ontgui.wireless_radiosetup(ontip=ontip, radiotype="2.4GHz", radio="off", mode="802.11b")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype="2.4GHz", radio="on", mode="802.11g and 802.11n")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype="5GHz", radio="on", mode="802.11n", dfs="disabled",
                                  channel="36")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype="5GHz", radio="on", mode="802.11n", dfs="enabled",
                                  channel="60")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="5GHz", ssid="5GHz_Operator_5", ssidstate="enabled",
                               renamessid="YodaWasHere!")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="5GHz", ssid="YodaWasHere!", ssidisolate="enabled",
                              gw="192.168.100.1",
                              startip="192.168.100.10", stopip="192.168.100.100", mask="255.255.255.0")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="5GHz", ssid="YodaWasHere!", renamessid="5GHz_Operator_5")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="5GHz", ssid="5GHz_Operator_5", ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid="2.4GHz_Operator_1", ssidstate="enabled",
                              renamessid="NakedMoleRat")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid="NakedMoleRat", ssidisolate="enabled",
                              gw="192.168.99.1",
                              startip="192.168.99.10", stopip="192.168.99.100", mask="255.255.255.0")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid="NakedMoleRat", l2wansvc="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid="NakedMoleRat", l2wansvc="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid="NakedMoleRat", renamessid="2.4GHz_Operator_1")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid="2.4GHz_Operator_1", ssidstate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype="2.4GHz", ssid=fsan, securitytype="WPA2-Personal",
                                  passphrase="YodaLivesHere")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype="5GHz", ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase="Livernet")

@cafe.test_case()
def e7guifailure_test_case(params):

    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan1']

    print("Hello! I am a test case!")
    cafe.Checkpoint("Pass me please").verify_exact("Pass me please")

    ontgui.wireless_radiosetup(ontip=ontip, radiotype="5GHz", radio="on", mode="802.11n", dfs="disabled",
                                  channel="22")


@cafe.test_case()
def ixveriwave_test_case(params):

    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan1']

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype="2.4GHz", radio="on", mode="802.11b, 802.11g, and 802.11n",
                               bandwidth="20 MHz", channel="6", powerlevel="100%")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssidstate="enabled", broadcast="enabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype="2.4GHz", ssid=fsan, securitytype="Security Off")

    # Create file to execute IxVeriwave Test
    ixvw.buildsimplebenchtest(chassisname="10.83.2.199", wifichannel="6",
                              srcint="2:1", srcinttype="802.11n", srcgrouptype="802.11abgn", srcchanbw="40",
                              srcssid=fsan, srcphyinterface="802.11n", srcmac="00:01:01:01:01:01",
                              destint="2:1", destinttype="802.11n", destgrouptype="802.11abgn", destchanbw="40",
                              destssid=fsan, destphyinterface="802.11n", destmac="00:02:02:02:02:02",
                              framesize="500", srcpercentrate="20", debug=3, tclshpath="c:/Tcl")


    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype="2.4GHz", channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype="2.4GHz", ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

    print("Hello! I am a test case!")
    cafe.Checkpoint("Pass me please").verify_exact("Pass me please")

@cafe.test_case()
def ixveriwave_buildfile(params):

    # Obtain required parameters
    ixvw =  params['ixvw']['ixvwpcsession']
    fsan = params['execution']['ontfsan1']

    # Create file to execute IxVeriwave Test
    ixvw.simplebenchtest(chassisname="10.83.2.199", wifichannel="6",
                              srcint="2:1", srcinttype="802.11n", srcgrouptype="802.11abgn", srcchanbw="40",
                              srcssid=fsan, srcphyinterface="802.11n", srcmac="00:01:01:01:01:01",
                              destint="2:1", destinttype="802.11n", destgrouptype="802.11abgn", destchanbw="40",
                              destssid=fsan, destphyinterface="802.11n", destmac="00:02:02:02:02:02",
                              framesize="500", srcpercentrate="20", debug=3, tclshpath="c:/Tcl")

    print("Hello! I am a test case!")
    cafe.Checkpoint("Pass me please").verify_exact("Pass me please")

# ##########
# @cafe.test_case()
# def e7_test_case(dut):
#
#
#
#     stp.api.e7.e7_lib.lib_create_NL2NLRingXConn(p_description="x1",
#                                                 p_xconna_sess=xconna, p_xconna_int="2/g1",
#                                                 p_xconn_sess=xconnb, p_xconnb_int="2/g1",
#                                                 p_tlsvlan=2001,
#                                                 p_nativevlan=3001)
#
#
#

##########
@cafe.test_suite()
def xconn_demo_test_suite():

    # Initialize logging
    init_logging()

    # Start session manager
    # sm = cafe.get_session_manager()

    # Obtain test suite parameter file information
    # params = cafe.get_test_param()
    # params.reset()
    # cafe.load_ts_config(cafe.get_cfs().abspath("params/ts_xconn_demo_parms.ini"))

    params = cafe.Param({})
    # TODO Modify to take filename directly from cafe config file
    params.load_ini("params/ts_xconn_demo_parms.ini")
    print("params : ", params)

    # Test bed topology information imported here
    topology = cafe.get_topology()
    # print("topo file : ",params['Topology'])
    topology.load(params.topology.file)

    # Start session manager
    params.session_mgr = session_mgr = cafe.get_session_manager()

    # Open Sessions Needed for Test Suite
    open_sessions(params, topology)


    # Register Test cases
    # cafe.register_test_case(e7gui_test_case, args=[params])
    cafe.register_test_case(e7guifailure_test_case, args=[params])
    # cafe.register_test_case(ixveriwave_test_case, args=[params])
    # cafe.register_test_case(ixveriwave_buildfile, args=[params])
    # cafe.register_test_case(e7_test_case, args=[dut2])

    # Execute test cases
    cafe.run_test_cases()

    # Close Sessions Needed for Test Suite
    close_sessions(params, topology)

    # Extract session information for DUTs
    # dut1_info = topology.nodes['e72_mc']['session_profile']['mgmt_vlan']['telnet']
    # dut2_info = topology.nodes['e348c']['session_profile']['mgmt_vlan']['telnet']

    # get E7 Communication class - E7 equipment lib
    # dut1 = E7ApiClass(sm.create_session('dut1', 'telnet', **dut1_info), eq_type=topology.nodes['e72_mc']['eq_type'])
    # dut2 = E7ApiClass(sm.create_session('dut2', 'telnet', **dut2_info), eq_type=topology.nodes['e348c']['eq_type'])

    # dut1.login()
    # dut2.login()

    # Register test cases
    # cafe.register_test_case(e7_test_case, args=[dut1])
    # cafe.register_test_case(e7_test_case, args=[dut2])
    # Execute test cases
    # cafe.run_test_cases()
    #
    # Close sessions after execution
    # sm.remove_session(session_name="dut1")
    # sm.remove_session(session_name="dut2")


if __name__ == "__main__":
    xconn_demo_test_suite()
