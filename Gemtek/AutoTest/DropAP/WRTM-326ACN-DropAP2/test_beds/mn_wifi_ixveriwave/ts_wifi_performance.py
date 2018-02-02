__author__ = 'glivermo'

import cafe
from cafe.core.logger import init_logging
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from cafe.sessions.tcl_remote import TCLRemoteShell
from stp.test_cases import tc_wifi_performance


# Load config.ini file when not executing from command prompt - default location for Gayle written test suites
if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("config/config.ini")

def open_sessions(params, iscalix):
    """
    Description:
        Open sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
    Returns:
    """
    # TODO: Convert over to using Cafe provided parameter usage
    # TODO: Need to extract returns from calls to verify success

    # Open ONT GUI Session(s)
    if iscalix:
        params['ontgui']['ontgui_session'] = ONTGuiApiClass(sid="ONTMgmt")
        params['ontgui']['ontgui_session'].login(ontip=params.ontgui.ontgui, username="support", password="support")

    # Open remote TCL shell session to IxVeriwave Managing PC
    # TODO: Look at reducing timeout to low value
    params['ixvw']['ixvwpcsession'] = TCLRemoteShell(winhost=params['ixvw']['ixvwpcip'],
                                                     winuser=params['ixvw']['ixvwpclogin'],
                                                     winpassword=params['ixvw']['ixvwpcpassword'],
                                                     timeout=300,
                                                     tcl_shell="tclsh.exe")
    params['ixvw']['ixvwpcsession'].login()

# ######################################################################################################################
# Close sessions for test execution
# ######################################################################################################################

def close_sessions(params, iscalix):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
    Returns:
    """

    # Close ONT GUI Session(s)
    if iscalix:
        params['ontgui']['ontgui_session'].close()

    # Close IxVeriwave Managing PC Session
    params['ixvw']['ixvwpcsession'].close()

##########
@cafe.test_suite()
def ts_wifi_performance():

    # Initialize logging
    init_logging()

    params = cafe.Param({})
    # TODO Modify to take filename directly from cafe config file
    #params.load_ini("params/800E/ts_wifi_performance_800E_24g.ini")
    #params.load_ini("params/noncalix/buffalo_performance_24g.ini")
    #params.load_ini("params/noncalix/bcomreference_performance_24g.ini")
    #params.load_ini("params/noncalix/bcomreference_performance_5g.ini")
    #params.load_ini("params/800G/ts_wifi_performance_854G_5g.ini")
    params.load_ini("params/800G/ts_wifi_performance_844G_5g.ini")
    # print "params : ", params

    # Test bed topology information imported here (No topology needed at this time)
#    topology = cafe.get_topology()
#    topology.load(params.topology.file)
#    print "topology : ", topology

    if 'iscalix' in params['globalsettings']:
        if str(params['globalsettings']['iscalix']).lower() == 'false':
            iscalix = False
        else:
            iscalix = True
    else:
        iscalix = True

    # Open Sessions Needed for Test Suite
    open_sessions(params, iscalix)

    # TMS Global IDs are made up of <Contour_Global_ID><Contour_User_Interface><EUT>
    idadd = params['testaccounting']['ui'] + params['testaccounting']['eut']

    if params['globalsettings']['radiotype'] == "2.4GHz":
        # 2.4GHz Test Case Execution
        if iscalix:
            cafe.register_test_case(tc_wifi_performance.tc_1041201_24g_centurylink_frsize_lan2wifi, test_id="1041201" + idadd, args=[params])
            #cafe.register_test_case(tc_wifi_performance.tc_1041204_24g_centurylink_frsize_wifi2lan(, test_id="1041204" + idadd, args=[params])
            #cafe.register_test_case(tc_wifi_performance.tc_1041203_24g_centurylink_frsize_wifilanbidirectional, test_id="1041203" + idadd, args=[params])
        else:
            cafe.register_test_case(tc_wifi_performance.tc_noncalix_24g_centurylink_frsize_lan2wifi, test_id="noncalix" + idadd, args=[params])

    if params['globalsettings']['radiotype'] == "5GHz":
        # 5GHz Test Case Execution
        if iscalix:
            cafe.register_test_case(tc_wifi_performance.tc_1041311_5g_centurylink_frsize_lan2wifi, test_id="1041311" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1041312_5g_centurylink_frsize_wifi2lan, test_id="1041312" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1041313_5g_centurylink_frsize_wifilanbidirectional, test_id="1041313" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1065801_5g_centurylink_multiclients_lan2wifi, test_id="1065801" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1065901_5g_centurylink_multiclients_wifi2lan, test_id="1065901" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1065802_5g_centurylink_multiclientsssids_lan2wifi, test_id="1065802" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1065904_5g_centurylink_multiclientsssids_wifi2lan, test_id="1065904" + idadd, args=[params])
            cafe.register_test_case(tc_wifi_performance.tc_1065902_5g_centurylink_multiclientsssids_wifilanbidirectional, test_id="1065902" + idadd, args=[params])
            # cafe.register_test_case(tc_wifi_performance.tc_777_5g_maxclientscapacity, test_id="777" + idadd, args=[params])
        else:
            cafe.register_test_case(tc_wifi_performance.tc_noncalix_5g_centurylink_frsize_lan2wifi, test_id="noncalix" + idadd, args=[params])

    # Execute test cases
    cafe.run_test_cases()

    # Close Sessions Needed for Test Suite
    close_sessions(params, iscalix)

if __name__ == "__main__":
    ts_wifi_performance()
