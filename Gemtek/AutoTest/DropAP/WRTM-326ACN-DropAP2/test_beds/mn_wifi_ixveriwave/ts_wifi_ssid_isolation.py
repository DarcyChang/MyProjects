__author__ = 'glivermo'

import cafe
from cafe.core.logger import init_logging
from stp.equipment.calix.e7 import E7ApiClass
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from cafe.sessions.tcl_remote import TCLRemoteShell
from stp.test_cases import tc_wifi_ssid_isolation


# Load config.ini file when not executing from command prompt - default location for Gayle written test suites
if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("config/config.ini")

def open_sessions(params, topology):
    """
    Description:
        Open sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    # TODO: Convert over to using Cafe provided parameter usage
    # TODO: Need to extract returns from calls to verify success
    # Start session manager
    params.session_mgr = session_mgr = cafe.get_session_manager()

    # Open E7 Session(s) - opens sessions to all E7 DUTs in parameter file
    e7_nodename = params['e7']['e7']
    params['e7']['e7_profile'] = topology['nodes'][e7_nodename]['session_profile']['mgmt_vlan']['telnet']
    params['e7']['e7_session'] = E7ApiClass(params.session_mgr.create_session(e7_nodename, 'telnet',
                                                                              **params['e7']['e7_profile']),
                                            eq_type="e7")
    params['e7']['e7_session'].login()

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

def close_sessions(params, topology):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    # Close E7 Session(s) - all that are listed as DUTs in parameter file
    # e7_node_list = params['e7'].keys()
    # for e7_node in e7_node_list:
    #     params.session_mgr.remove_session(params['e7'][e7_node])
    params.session_mgr.remove_session(params['e7']['e7_session'])

    # Close ONT GUI Session(s)
    params['ontgui']['ontgui_session'].close()

    # Close IxVeriwave Managing PC Session
    params['ixvw']['ixvwpcsession'].close()

##########
@cafe.test_suite()
def ts_ssid_isolation():

    # Initialize logging
    init_logging()

    params = cafe.Param({})
    # TODO Modify to take filename directly from cafe config file
    params.load_ini("params/800E/ts_wifi_ssid_isolation_800E_24g.ini")
    # params.load_ini("params/800G/ts_wifi_ssid_isolation_800G_24g.ini")
    # params.load_ini("params/800GH/ts_wifi_ssid_isolation_800GH_24g.ini")
    # params.load_ini("params/800G/ts_wifi_ssid_isolation_854G_5g.ini")
    # params.load_ini("params/800G/ts_wifi_ssid_isolation_844G_5g.ini")
    # print "params : ", params

    # Test bed topology information imported here
    topology = cafe.get_topology()
    topology.load(params.topology.file)
    # print "topology : ", topology

    # Build XConnect
    # TODO: Complete development on building E7 XConnect

    # Open Sessions Needed for Test Suite
    open_sessions(params, topology)

    # TMS Global IDs are made up of <Contour_Global_ID><Contour_User_Interface><EUT>
    idadd = params['testaccounting']['ui'] + params['testaccounting']['eut']

    # If a GPON ONT need to configure WAN uplink through E7
    if str(params['execution']['isdutgponont']).lower() == "yes":
        cafe.register_test_case(tc_wifi_ssid_isolation.gpon_ont_build_e7_provisioning, args=[params])

    # If an Ethernet only ONT need to configure Use Case uplink through E7 for WAN connection
    if str(params['execution']['isdutgponont']).lower() == "no":
        cafe.register_test_case(tc_wifi_ssid_isolation.enet_ont_build_e7_provisioning, args=[params])

    if params['execution']['radiotype'] == "2.4GHz":
        # 2.4GHz Test Case Execution
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546796_24g_primary_ssid_lan_isolation, test_id="546796" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546797_24g_primary_ssid_wan_isolation, test_id="546797" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546798_24g_primary_ssid_intra_isolation, test_id="546798" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546799_24g_primary_ssid_nonprimary_ssid_isolation_nosubnet, test_id="546799" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546800_24g_primary_ssid_nonprimary_ssid_isolation_subnet, test_id="546800" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546801_24g_primary_ssid_nonprimary_ssid_isolation_subnetandintra, test_id="546801" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546803_24g_nonprimary_ssid_lan_isolationdisabled, test_id="546803" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546804_24g_nonprimary_ssid_lan_isolationenabled, test_id="546804" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546805_24g_nonprimary_ssid_wan_isolationenabled, test_id="546805" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546806_24g_nonprimary_ssid_wan_isolationenabled, test_id="546806" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546807_24g_nonprimary_ssid_intra_isolationdisabled, test_id="546807" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546808_24g_nonprimary_ssid_intra_isolationenabled, test_id="546808" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546809_24g_two_nonprimary_ssid_bothinterisolationdisabled, test_id="546809" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546810_24g_two_nonprimary_ssid_bothinterisolationenabled, test_id="546810" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546811_24g_two_nonprimary_ssid_differentinterisolation, test_id="546811" + idadd, args=[params])

    if params['execution']['radiotype'] == "5GHz":
        # 5GHz Test Case Execution
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546775_5g_primary_ssid_lan_isolation, test_id="546775" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546776_5g_primary_ssid_wan_isolation, test_id="546776" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546777_5g_primary_ssid_intra_isolation, test_id="546777" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546778_5g_primary_ssid_nonprimary_ssid_isolation_nosubnet, test_id="546778" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546779_5g_primary_ssid_nonprimary_ssid_isolation_subnet, test_id="546779" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546782_5g_nonprimary_ssid_lan_isolationdisabled, test_id="546782" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546783_5g_nonprimary_ssid_lan_isolationenabled, test_id="546783" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546784_5g_nonprimary_ssid_wan_isolationenabled, test_id="546784" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546785_5g_nonprimary_ssid_wan_isolationenabled, test_id="546785" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546786_5g_nonprimary_ssid_intra_isolationdisabled, test_id="546786" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546787_5g_nonprimary_ssid_intra_isolationenabled, test_id="546787" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546788_5g_two_nonprimary_ssid_bothinterisolationdisabled, test_id="546788" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546789_5g_two_nonprimary_ssid_bothinterisolationenabled, test_id="546789" + idadd, args=[params])
        cafe.register_test_case(tc_wifi_ssid_isolation.tc_546790_5g_two_nonprimary_ssid_differentinterisolation, test_id="546790" + idadd, args=[params])

    if str(params['execution']['isdutgponont']).lower() == "yes":
        cafe.register_test_case(tc_wifi_ssid_isolation.gpon_ont_remove_e7_provisioning, args=[params])

    if str(params['execution']['isdutgponont']).lower() == "no":
        cafe.register_test_case(tc_wifi_ssid_isolation.enet_ont_remove_e7_provisioning, args=[params])

    # Execute test cases
    cafe.run_test_cases()

    # Close Sessions Needed for Test Suite
    close_sessions(params, topology)

if __name__ == "__main__":
    ts_ssid_isolation()
