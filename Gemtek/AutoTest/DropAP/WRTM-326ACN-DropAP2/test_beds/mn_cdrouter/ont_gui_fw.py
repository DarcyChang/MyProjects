__author__ = 'bmelhus'

import csv,re,time,cafe
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from stp.test_beds.mn_cdrouter.loadCmdsToExecute import get_fw_cfg

def open_session_ont_gui(params, topology):
    ont_ip = params['ontgui']['ont_ip']

    # Open ONT Web Gui Session
    params['ont_gui'] = ONTGuiApiClass(sid="ONTMgmt")
    params['ont_gui'].login(ontip=ont_ip, username="support", password="support")

def close_session_ont_gui(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params['ont_gui'].close()

# Load config.ini file when not executing from command prompt - default location for written test suites
if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("config/config.ini")

params = cafe.Param({})
params.load_ini("params/cdrouter.ini")

# Test bed topology information imported here
topology = cafe.get_topology()
topology.load(params.topology.file)

def config_fw(scenario):
    dbglvl = "info"
    open_session_ont_gui(params, topology)
    ont_gui = params['ont_gui']

    fw_svcs_in, fw_svc_state_in = get_fw_cfg("fw_in.csv", scenario)
    for i in range(len(fw_svcs_in)):
        if re.search("Stealth", fw_svcs_in[i], re.S):
            scenario_sm = fw_svc_state_in[i]
        elif re.search("Firewall", fw_svcs_in[i], re.S):
            scenario_fw = fw_svc_state_in[i]
        else:
            if dbglvl == "dbg":
                print("Service In: " + fw_svcs_in[i] + " == " + fw_svc_state_in[i])

    fw_svcs_out, fw_svc_state_out = get_fw_cfg("fw_out.csv", scenario)
    if dbglvl == "dbg":
        for i in range(len(fw_svcs_out)):
            if re.search("Stealth", fw_svcs_out[i], re.S):
                print("Found Stealth Mode!")
            elif re.search("Firewall", fw_svcs_out[i], re.S):
                print("Found Firewall Level!")
            else:
                print("Service Out: " + fw_svcs_out[i] + " == " + fw_svc_state_out[i])

    print("Stealth Mode: " + scenario_sm)
    print("Firewall: " + scenario_fw)
    set_fw = ont_gui.set_ont_fw(ontip=params['ontgui']['ont_ip'], sm=scenario_sm, fw=scenario_fw)
    if not re.search("dflt", scenario, re.S) and not scenario_fw == "off":
        set_fw_svc_in = ont_gui.set_fw_svc_state(ontip=params['ontgui']['ont_ip'], svc_name=fw_svcs_in, svc_state=fw_svc_state_in)
        set_fw_svc_out = ont_gui.set_fw_svc_state(ontip=params['ontgui']['ont_ip'], svc_name=fw_svcs_out, svc_state=fw_svc_state_out)

    close_session_ont_gui(params)