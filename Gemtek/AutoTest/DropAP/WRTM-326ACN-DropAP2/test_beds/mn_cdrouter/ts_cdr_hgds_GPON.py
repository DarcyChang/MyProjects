__author__ = 'bmelhus'

import csv,re,time,cafe
from stp.test_beds.mn_cdrouter.testCdRouter import xc3_prov
from stp.test_beds.mn_cdrouter.testCdRouter import e7_prov
from stp.test_beds.mn_cdrouter.testCdRouter import exec_test
from stp.equipment.cdrouter.cdrouter import CdrApiClass
from stp.equipment.calix.ccfg_gui import CCFGGuiApiClass
from stp.equipment.calix.ont_gui import ONTGuiApiClass
from stp.equipment.calix.ont_terminal import OntApiClass
from stp.test_beds.mn_cdrouter.ont_gui_fw import config_fw


# dbglvl = "info"

def open_session_cdr(params, topology):
    #-----------------------------------------------------------------------------------------------------
    # CD Router SSH
    # print(topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh'])
    params['cdr_profile'] = topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh']
    params['cdr_session'] = CdrApiClass(params.session_mgr.create_session("cdr", 'ssh', **params['cdr_profile']), eq_type="cdr")

    # print(params['cdr_profile'])
    params['cdr_session'].login()
    # cdr = params['cdr_session']

def open_session_xc(params, topology):
    #-----------------------------------------------------------------------------------------------------
    # XCONN Telnet
    # print(topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh'])
    params['xc3_profile'] = topology['nodes']['xc3']['session_profile']['mgmt_vlan']['telnet']
    params['xc3_session'] = CdrApiClass(params.session_mgr.create_session("xc3", 'telnet', **params['xc3_profile']), eq_type="e72")

    # print(params['cdr_profile'])
    params['xc3_session'].login()
    # xc3 = params['xc3_session']

def open_session_e7(params, topology):
    #-----------------------------------------------------------------------------------------------------
    # E7 DUT Telnet
    # print(topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh'])
    params['e7_profile'] = topology['nodes']['e72']['session_profile']['mgmt_vlan']['telnet']
    params['e7_session'] = CdrApiClass(params.session_mgr.create_session("e72", 'telnet', **params['e7_profile']), eq_type="e72")

    # print(params['cdr_profile'])
    params['e7_session'].login()
    # e72 = params['e7_session']

def open_session_ccfg(params, topology):
    # Open CCFG Session
    params['ccfg_gui'] = CCFGGuiApiClass(sid="CCFG")
    params['ccfg_gui'].login(ccfg_ip=params.ccfg.ccfg_ip, username=params.ccfg.ccfg_uname, password=params.ccfg.ccfg_pwrd)

def open_session_ont_gui(params, topology):
    ont_ip = params['ontgui']['ont_ip']

    # Open ONT Web Gui Session
    params['ont_gui'] = ONTGuiApiClass(sid="ONTMgmt")
    params['ont_gui'].login(ontip=ont_ip, username="support", password="support")

def open_session_ont_serial(params, topology):
    #-----------------------------------------------------------------------------------------------------
    # Conn to ONT Serial Port via Terminal Server
    params['ont_profile'] = topology['nodes']['844E_Drei']['session_profile']['terminal']['telnet']
    params['ont_session'] = OntApiClass(params.session_mgr.create_session("844E_Drei", 'telnet', **params['ont_profile']), eq_type="ONT")

def close_session_cdr(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params.session_mgr.remove_session(params['cdr_profile'])

def close_session_xc(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params.session_mgr.remove_session(params['xc3_profile'])

def close_session_e7(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params.session_mgr.remove_session(params['e7_profile'])

def close_session_ccfg(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params['ccfg_gui'].close()

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
# print("params : ", params)

# Test bed topology information imported here
topology = cafe.get_topology()
topology.load(params.topology.file)
#print("topology : ", topology)

params.session_mgr = session_mgr = cafe.get_session_manager()

open_session_xc(params, topology)

open_session_e7(params, topology)

open_session_cdr(params, topology)

# dev_type     ==     ONT/Location_(multi|cdr)
# eut          ==     ONT Model (813G|844G|854G|etc...)
# scenario     ==     IPv6 SVC Model/Index (ds-1|dsl-1|6rd-1)
# cdr_test     ==     IPv6 SVC Model/Index (ds-1|dsl-1|6rd-1)_subIdx
# dbglvl       ==     (info|dbg|etc...)

# Note: etc...  is yet to be determined when specified

def hgds_test_case(dev_type, eut, rg_scenario, cdr_test, cfg_step, params, dbglvl):

    execute_steps = cfg_step.split()
    execute_config = execute_steps[0]
    execute_cdr = execute_steps[1]
    deconfig_config = execute_steps[2]
    fw_scenario = rg_scenario
    if re.search("fw", rg_scenario, re.S):
        rg_scenario = "fw-1"

    if dbglvl == "dbg":
        print("Execute steps: " + str(execute_steps))
        print("Execute Config: " + str(execute_config))
        print("Execute CDR: " + str(execute_cdr))
        print("Deconfigure Config: " + str(deconfig_config))

    #===========================================================================================
    # Get ONT Version for Results Reporting

    if execute_cdr == "1":
        #---------------------------------------------------
        # Delete tag action if exists
        if not execute_config == "1":
            xconn = xc3_prov("xc_cmds.csv", "del", dev_type, eut, "null", params, dbglvl)

        #---------------------------------------------------
        # Create tag action for ONT GUI
        xconn = xc3_prov("xc_cmds_ont-gui.csv", "add", dev_type, eut, "null", params, dbglvl)

        #---------------------------------------------------
        # Get ONT Version
        open_session_ont_gui(params, topology)
        ont_gui = params['ont_gui']
        ont_ver = ont_gui.get_ont_version(ontip=params['ontgui']['ont_ip'])
        print("ONT Version: " + str(ont_ver))
        close_session_ont_gui(params)

        #---------------------------------------------------
        # Delete tag action for ONT GUI
        xconn = xc3_prov("xc_cmds_ont-gui.csv", "del", dev_type, eut, "null", params, dbglvl)

    if execute_config != "0":
        xconn = xc3_prov("xc_cmds.csv", "add", dev_type, eut, "null", params, dbglvl)

    if execute_config != "0":
        #===========================================================================================
        # Config XCONN
        # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
        # xc3_prov(csv, add, dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1,  dbglvl=info)
        xconn = xc3_prov("xc_cmds.csv", "add", dev_type, eut, "null", params, dbglvl)

        #===========================================================================================
        # Configure ONT
        # 1) ontRgPortProv.csv
        # 2) cdRouterSvcCmds_<v6_type>.csv
        # 3) <ont_type>_ontConfigs.csv
        # 4) ontRgCfgProv.csv
        # 5) ontTr69CfgProv_<tr69_type>.csv

        if not eut == "844E":
            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 1) Set ONT RG Port mgmt-mode to external
            rg_port_cfg = e7_prov("ontRgPortProv.csv", "add", dev_type, eut, "null", params, dbglvl)

        # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
        # 2) Configure Eth-Svc on RG Port
        if eut == "844E":
            from stp.test_beds.mn_cdrouter.cmdCtr import load_cfg_file
            open_session_ccfg(params, topology)

            # Configure service for Access to TR-069
            svc_prov = e7_prov("cdRouterSvcCmds_tr069.csv", "add", dev_type, eut, "null", params, dbglvl)

            #---------------------------------------------------
            #  Configure RG for TR-069
            # Delete tag action for CDR
            xconn = xc3_prov("xc_cmds.csv", "del", dev_type, eut, "null", params, dbglvl)
            #---------------------------------------------------
            # Create tag action for ONT GUI
            xconn = xc3_prov("xc_cmds_ont-gui.csv", "add", dev_type, eut, "null", params, dbglvl)

            from stp.test_beds.mn_cdrouter.ontgui_config import rstr_dflts
            from stp.test_beds.mn_cdrouter.ontgui_config import conf_tr069
            from stp.test_beds.mn_cdrouter.ontgui_config import chk_cfg_dld_cmplt

            #---------------------------------------------------
            # Configure TR-069 via ONT GUI
            #tr069_setup = conf_tr069(params)

            #---------------------------------------------------
            # Download Config File via CCFG
            dld_cfg_file = load_cfg_file("e_ontConfigs.csv", rg_scenario, dev_type, params, dbglvl)

            #---------------------------------------------------
            # Verify Dld of config file
            dld_ont = False
            while dld_ont == False:
                rst_ont = False
                #---------------------------------------------------
                # Reset ONT Factory Default
                while rst_ont == False:
                    open_session_ont_gui(params, topology)
                    rst_ont = rstr_dflts(params)
                time.sleep(10)
                dld_ont = chk_cfg_dld_cmplt(eut, rg_scenario, params)

            #---------------------------------------------------
            # Delete tag action for ONT GUI
            xconn = xc3_prov("xc_cmds_ont-gui.csv", "del", dev_type, eut, "null", params, dbglvl)
            #---------------------------------------------------
            # Create tag action for CDR
            xconn = xc3_prov("xc_cmds.csv", "add", dev_type, eut, "null", params, dbglvl)

            #---------------------------------------------------
            # Remove service for Access to TR-069
            svc_prov = e7_prov("cdRouterSvcCmds_tr069.csv", "del", dev_type, eut, "null", params, dbglvl)
            close_session_ccfg(params)
            close_session_ont_gui(params)


        if re.search('dsl', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_dsl.csv", "add", dev_type, eut, "null", params, dbglvl)
        elif re.search('ds', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_ds.csv", "add", dev_type, eut, "null", params, dbglvl)
        elif re.search('6rd', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_6rd.csv", "add", dev_type, eut, "null", params, dbglvl)
        elif re.search('pppoe', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_pppoe.csv", "add", dev_type, eut, "null", params, dbglvl)
        elif re.search('fw', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_ds.csv", "add", dev_type, eut, "null", params, dbglvl)

        if not eut == "844E":
            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 3) Add ONT-Config to System
            if re.search('GH', eut, re.S):
                ont_cfg = e7_prov("gh_ontConfigs.csv", "add", rg_scenario, eut, "null", params, dbglvl)
            elif re.search('GE', eut, re.S):
                ont_cfg = e7_prov("ge_ontConfigs.csv", "add", rg_scenario, eut, "null", params, dbglvl)
            else:
                ont_cfg = e7_prov("gc_ontConfigs.csv", "add", rg_scenario, eut, "null", params, dbglvl)

        if not eut == "844E":
            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 4) Set ONT RG Port instance
            rg_cfg = e7_prov("ontRgCfgProv.csv", "add", dev_type, eut, "null", params, dbglvl)

            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 5) Set ONT RG Port TR-69 profile
            # tr69_cfg = e7_prov("ontTr69CfgProv_ib.csv", "add", dev_type, eut, "null", dbglvl)

    if re.search("fw", fw_scenario, re.S) and execute_cdr == "1":
        #---------------------------------------------------
        # Delete tag action if exists
        xconn = xc3_prov("xc_cmds.csv", "del", dev_type, eut, "null", params, dbglvl)

        #---------------------------------------------------
        # Create tag action for ONT GUI
        xconn = xc3_prov("xc_cmds_ont-gui.csv", "add", dev_type, eut, "null", params, dbglvl)

        #---------------------------------------------------
        # Configure RG Firewall
        fw_config= config_fw(scenario=fw_scenario)

        #---------------------------------------------------
        # Delete tag action for ONT GUI
        xconn = xc3_prov("xc_cmds_ont-gui.csv", "del", dev_type, eut, "null", params, dbglvl)

        #---------------------------------------------------
        # Create tag action for CDR
        xconn = xc3_prov("xc_cmds.csv", "add", dev_type, eut, "null", params, dbglvl)

    if execute_cdr != "0":
        #===========================================================================================
        # Execute CD Router
        # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)

        if execute_config == "0":
            #time.sleep(180)
            time.sleep(60)
        else:
            time.sleep(30)
        cdr_complete = False
        cdr_count = 1
        while cdr_complete == False:
            cdr_rslts = exec_test("cdrAutoCmds.csv", "add", rg_scenario, eut, cdr_test, params, ont_ver, dbglvl)
            if cdr_rslts == True:
                cdr_complete = True
            else:
                time.sleep(20)
                cdr_complete = False
                cdr_count += 1
            if cdr_count == 3:
                cdr_complete = True
                print("CDR Test Failed to Execute!")

    if deconfig_config != "0":
        #===========================================================================================
        # Configure ONT
        # 1) cdRouterSvcCmds_<v6_type>.csv
        # 2) ontTr69CfgProv_<tr69_type>.csv
        # 3) ontRgCfgProv.csv
        # 4) <ont_type>_ontConfigs.csv
        # 5) ontRgPortProv.csv

        # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
        # 1) Configure Eth-Svc on RG Port
        if re.search('dsl', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_dsl.csv", "del", dev_type, eut, "null", params, dbglvl)
        elif re.search('ds', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_ds.csv", "del", dev_type, eut, "null", params, dbglvl)
        elif re.search('6rd', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_6rd.csv", "del", dev_type, eut, "null", params, dbglvl)
        elif re.search('pppoe', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_pppoe.csv", "del", dev_type, eut, "null", params, dbglvl)
        elif re.search('fw', rg_scenario, re.S):
            svc_prov = e7_prov("cdRouterSvcCmds_ds.csv", "del", dev_type, eut, "null", params, dbglvl)

        if not eut == "844E":
            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 2) Set ONT RG Port TR-69 profile
            # tr69_cfg = e7_prov("ontTr69CfgProv_ib.csv", "del", dev_type, eut, "null", dbglvl)

            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 3) Set ONT RG Port instance
            rg_cfg = e7_prov("ontRgCfgProv.csv", "del", dev_type, eut, "null", params, dbglvl)

            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 4) Add ONT-Config to System
            if re.search('GH', eut, re.S):
                ont_cfg = e7_prov("gh_ontConfigs.csv", "del", rg_scenario, eut, "null", params, dbglvl)
            elif re.search('GE', eut, re.S):
                ont_cfg = e7_prov("ge_ontConfigs.csv", "del", rg_scenario, eut, "null", params, dbglvl)
            else:
                ont_cfg = e7_prov("gc_ontConfigs.csv", "del", rg_scenario, eut, "null", params, dbglvl)

            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            # 5) Set ONT RG Port mgmt-mode to external
            rg_port_cfg = e7_prov("ontRgPortProv.csv", "del", dev_type, eut, "null", params, dbglvl)

        #===========================================================================================
        # Config XCONN

        # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, rg_scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
        xconn = xc3_prov("xc_cmds.csv", "del", dev_type, eut, "null", params, dbglvl)

        # if eut == "844E":
        #     rst_ont = False
        #     while rst_ont == False:
        #         # Reset ONT Factory Defaults
        #         rst_ont = ont_rstr_dflt(eut)

#---------------------------------------------------------------------------
# Execute tests
#---------------------------------------------------------------------------

def get_test_info(csv_filename, dbglvl):
    command_file = csv_filename
    #----------------------------------------
    # Opens files in read mode
    #----------------------------------------
    cmd_file = open('/opt/home/bmelhus/stp/test_beds/mn_cdrouter/data/' + command_file, "r")
    csv_f = csv.reader(cmd_file)

    for row in csv_f:
        exec_row = row[0]

        # row[1]    ==    dev_type   :  813G-D_cdr
        # row[2]    ==    eut        :  800GH
        # row[3]    ==    scenario   :  6rd-1
        # row[4]    ==    cdr_test   :  all or 4a_6rd_l-dyn_subnet8
        # row[5]    ==    cfg_step   :  1 1 1
        # row[6]    ==    dbglvl     :  info

        if dbglvl == "dbg" and exec_row == "y":
            if dbglvl == "dbg":
                print("This is row:\n" + str(row))
                print('#######################################')
                print('{0:20} {1:50}'.format('# Execute Command: ', row[0]))
                print('{0:20} {1:50}'.format('# Device Type: ', row[1]))
                print('{0:20} {1:50}'.format('# EUT: ', row[2]))
                print('{0:20} {1:50}'.format('# HGDS Scenario: ', row[3]))
                print('{0:20} {1:50}'.format('# CDR Test Suite: ', row[4]))
                print('{0:20} {1:50}'.format('# Execute Values: ', row[5]))
                print('{0:20} {1:50}'.format('# Debug Level: ', row[6]))
                print('#######################################\n')
        if exec_row == "y":
            dev_type = row[1]
            eut = row[2]
            scenario = row[3]
            cdr_test = row[4]
            cfg_step = row[5]
            dbglvl = row[6]
            # hgds_test_case(dev_type=813G-D_cdr, eut=800GH, scenario=6rd-1, cdr_test=all, cfg_step=1 1 1, dbglvl=info)
            hgds_test_case(dev_type, eut, scenario, cdr_test, cfg_step, params, dbglvl)

    cmd_file.close()

# End

#-----------------------------------------------------------------------------
# Execute test suites in CSV
#
get_test_info("hgds_cdr_test_suites.csv", "dbg")
close_session_cdr(params)
close_session_e7(params)
close_session_xc(params)
