__author__ = 'glivermo'

import cafe
from cafe.core.logger import init_logging
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from cafe.sessions.tcl_remote import TCLRemoteShell
from stp.test_cases import tc_wifi_security


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
def ts_wifi_security():

    # Initialize logging
    init_logging()

    params = cafe.Param({})
    # TODO Modify to take filename directly from cafe config file
    params.load_ini("params/800E/ts_wifi_security_800E_24g.ini")
    # params.load_ini("params/800GH/ts_wifi_security_800GH_24g.ini")
    #params.load_ini("params/800G/ts_wifi_security_854G_5g.ini")
    #params.load_ini("params/800G/ts_wifi_security_844G_5g.ini")
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
        cafe.register_test_case(tc_wifi_security.tc_675201_24g_base_ssid_default_security, test_id="675201" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675202_24g_base_ssid_custom_key, test_id="675202" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675203_24g_guest_opertor_ssid_default_security_key, test_id="675203" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675204_24g_base_guest_ssid_custom_security_key, test_id="675204" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675209_24g_base_guest_ssid_security_off, test_id="675209" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675210_24g_base_guest_ssid_security_wpawpa2_enc_both, test_id="675210" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675211_24g_base_guest_ssid_security_wpawpa2_enc_aes, test_id="675211" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_675212_24g_base_guest_ssid_security_wpawpa2_enc_tkip, test_id="675212" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_1019101_24g_base_guest_ssid_security_wpa2_enc_aes, test_id="1019101" + idadd, args=[params])

    if params['execution']['radiotype'] == "5GHz":
        # 5GHz Test Case Execution
        cafe.register_test_case(tc_wifi_security.tc_981722_5g_base_ssid_default_security, test_id="981722" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_981707_5g_base_ssid_custom_key, test_id="981707" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_981708_5g_guest_opertor_ssid_default_security_key, test_id="981708" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_981709_5g_base_guest_ssid_custom_security_key, test_id="981709" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_981711_5g_base_guest_ssid_security_off, test_id="981711" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_981713_5g_base_guest_ssid_security_wpawpa2_enc_aes, test_id="981713" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_security.tc_1020703_5g_base_guest_ssid_security_wpa2_enc_aes, test_id="1020703" + idadd, args=[params])

    # Execute test cases
    cafe.run_test_cases()

    # Close Sessions Needed for Test Suite
    close_sessions(params)

if __name__ == "__main__":
    ts_wifi_security()
