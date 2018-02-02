__author__ = 'glivermo'

import cafe
from cafe.core.logger import init_logging
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from cafe.sessions.tcl_remote import TCLRemoteShell
from stp.test_cases import tc_wifi_radio


# Load config.ini file when not executing from command prompt - default location for Gayle written test suites
if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("config/config.ini")

def open_sessions(params):
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

def close_sessions(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
    Returns:
    """

    # Close ONT GUI Session(s)
    params['ontgui']['ontgui_session'].close()

    # Close IxVeriwave Managing PC Session
    params['ixvw']['ixvwpcsession'].close()

##########
@cafe.test_suite()
def ts_wifi_radio():

    # Initialize logging
    init_logging()

    params = cafe.Param({})
    # TODO Modify to take filename directly from cafe config file
    params.load_ini("params/800E/ts_wifi_security_800E_24g.ini")
    # params.load_ini("params/800GH/ts_wifi_security_800GH_24g.ini")
    # params.load_ini("params/800G/ts_wifi_radio_854G_5g.ini")
    # params.load_ini("params/800G/ts_wifi_radio_844G_5g.ini")
    # print "params : ", params

    # Test bed topology information imported here (No topology needed at this time)
#    topology = cafe.get_topology()
#    topology.load(params.topology.file)
#    print "topology : ", topology

    # Open Sessions Needed for Test Suite
    open_sessions(params)

    # TMS Global IDs are made up of <Contour_Global_ID><Contour_User_Interface><EUT>
    idadd = params['testaccounting']['ui'] + params['testaccounting']['eut']

    if params['execution']['radiotype'] == "2.4GHz":
        # 2.4GHz Test Case Execution
        cafe.register_test_case(tc_wifi_radio.tc_1052807_24g_radio_toggle, test_id="1052807" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1052808_24g_80211n_bandwidth_toggle, test_id="1052808" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665920_24g_80211bgn_client_phy, test_id="665920" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665921_24g_80211gn_client_phy, test_id="665921" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665922_24g_80211n_client_phy, test_id="665922" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665923_24g_80211bg_client_phy, test_id="665923" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665924_24g_80211g_client_phy, test_id="665924" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665925_24g_80211b_client_phy, test_id="665925" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1052810_24g_20mhz_channels, test_id="1052810" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1052811_24g_40mhz_channels, test_id="1052811" + idadd, args=[params])

    if params['execution']['radiotype'] == "5GHz":
        # 5GHz Test Case Execution - Country Code United States
        cafe.register_test_case(tc_wifi_radio.tc_1043401_5g_80211ac_bandwidth_toggle, test_id="1043401" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047001_5g_radio_toggle, test_id="1047001" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665928_5g_80211ac_client_phy, test_id="665928" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_665929_5g_80211n_client_phy, test_id="665929" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047203_5g_80mhz_nondfs_channels, test_id="1047203" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047204_5g_80mhz_dfs_channels, test_id="1047204" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047205_5g_40mhz_nondfs_channels, test_id="1047205" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047206_5g_40mhz_dfs_channels, test_id="1047206" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047207_5g_20mhz_nondfs_channels, test_id="1047207" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047208_5g_20mhz_dfs_channels, test_id="1047208" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_radio.tc_1047701_5g_80mhz_toggle_channels, test_id="1047701" + idadd, args=[params])

    # Execute test cases
    cafe.run_test_cases()

    # Close Sessions Needed for Test Suite
    close_sessions(params)

if __name__ == "__main__":
    ts_wifi_radio()
