__author__ = 'bmelhus'

from stp.test_beds.mn_cdrouter.loadCmdsToExecute import get_cfg_info

#-----------------------------------------------------------------------------------------------
#
#
def load_cfg_file(csv, rg_scenario, dev_type, params_ccfg, dbglvl):
    ccfg_gui = params_ccfg['ccfg_gui']

    cfg_file_name,dev_type_name = get_cfg_info(csv, rg_scenario, dev_type, dbglvl)
    print(cfg_file_name)
    print(dev_type_name)
    complete = False

    for i in range(len(cfg_file_name)):
        #-----------------------------------------------------------------------------------------------
        # Workflow to apply config file to 844E
        #
        # Browse to Web Page for Workflow
        cfg_file_page = 'netop-workflows/wizard'
        #----------------------------------------------------------------------------------------------
        # Enter values
        # 1) Name of Operation
        # 2) Description of Operation
        # 3) Click Next
        wf_name_val = str(dev_type_name[i]) + " CFG DLD"
        wf_desc_val = "DLD Config File for Testing"
        #----------------------------------------------------------------------------------------------
        # Check box for EUT based on ont_type
        ont_type = dev_type_name[i]
        #----------------------------------------------------------------------------------------------
        # Select Work Flow Operation
        # Work Flow Operations:
        # 1) Configuration File Download
        # 2) Download SW/FW Image
        # 3) Apply Configuration Profile
        wf_oper_val = "Configuration File Download"
        #----------------------------------------------------------------------------------------------
        # Click Radio button for Config file
        # Note: Config files must have been loaded previous to this operation
        cfg_file = cfg_file_name[i]
        print(cfg_file)
        #----------------------------------------------------------------------------------------------
        # Work Flow Execution type
        # 1) On Discovery
        # 2) Time Scheduler
        wf_type = "On Discovery"
        #----------------------------------------------------------------------------------------------
        # Input value = time in minutes
        wf_exec_wndw_val = "10"

        ccfg_ip = params_ccfg.ccfg.ccfg_ip

        dld_cfg = ccfg_gui.dld_cfg_file(ccfg_ip, cfg_file_page, wf_name_val, wf_desc_val, ont_type, wf_oper_val, cfg_file, wf_type, wf_exec_wndw_val)

        if dld_cfg == True:
            print("# ONT Config File DLD Started for: " + ont_type)
        else:
            print("# ONT Config File DLD Failed!")
        if not dev_type == "844E":
            chk_page = cfg_file_page.split('/')[0]
            complete = ccfg_gui.chk_dld_status(params_ccfg.ccfg.ccfg_ip, chk_page, wf_name_val)

        if complete == True:
            print("Download Complete for Workflow: " + wf_name_val)
        else:
            print("Download Not Completed for Workflow: " + wf_name_val)
        return complete