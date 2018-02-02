__author__ = 'bmelhus'

import time,re,cafe
#from stp.equipment.cdrouter.cdrouter import CdrApiClass
from stp.test_beds.mn_cdrouter.loadCmdsToExecute import get_cmds
from stp.test_beds.mn_cdrouter.cdRouterParser import print2screen
from datetime import datetime
from stp.test_beds.mn_cdrouter.cdr_rslt_compile import add_to_rslt_file

# dbglvl = "info"

#----------------------------------------------------------------------
# Module to verify ONT is in the disabled state after a reset
# If ONT does not reset fallback is to loop 10 times and continue
#
def ont_chk_dis(ont_id, params):
    e72 = params['e7_session']

    ont_disabled = 0
    while ont_disabled <= 6:
        response = e72.ont_send(cmd="show ont " + str(ont_id))
        ont_status = response['response']
        if re.search('disabled', ont_status, re.S):
            ont_disabled = 11
            cont_exec = 1
        else:
            ont_disabled += 1
            time.sleep(10)
            #print("ONT Disabled: " + str(ont_disabled))
    if ont_disabled == 7:
        cont_exec = 1
        print("ONT did not reset!")
    return cont_exec

#----------------------------------------------------------------------
# Module to verify ONT is in the enabled state after a reset
#
def ont_chk_en(ont_id, params):
    e72 = params['e7_session']

    ont_enabled = 0
    while ont_enabled <= 20:
        response = e72.ont_send(cmd="show ont " + str(ont_id))
        ont_status = response['response']
        if re.search('enabled', ont_status, re.S):
            ont_enabled += 1
        else:
            time.sleep(10)
    if ont_enabled >= 20:
        return True
    else:
        return False

#-----------------------------------------------------------------------------------------------------
# 1) Execute CD Router Test based on Scenario and Device Type (Model: (800GH|800GC|800E)
# 2) Compile results and format for Pass/Fail Validation
#
def exec_test(csv, action, rg_scenario, dev_type, cdr_test, params, ont_ver, dbglvl):
    # print("params : ", params)
    cdr = params['cdr_session']
    #-----------------------------------------------------------------------------------------
    # Retrieve commands from CSV
    cmd_lst = get_cmds(csv, action, rg_scenario, dev_type, cdr_test, dbglvl)

    #-----------------------------------------------------------------------------------------
    # 1) Execute CD Router Test based on Scenario and Device Type (Model: (800GH|800GC|800E)
    for i in range(len(cmd_lst)):
        complete = 0
        d = datetime.now()
        # Retrieve command from CMD List
        cmd_exec = cmd_lst[i]
        # Code to substitute Retrieved Version of ONT
        ver_rep = cmd_exec.split()[4]
        ver_rep = ver_rep.split(',')
        ver_rep = ont_ver + "," + ver_rep[1]
        cmd_exec = cmd_exec.replace(cmd_exec.split()[4], ver_rep)
        # Code to create Results File Name
        tmp_info = cmd_lst[i]
        rslt_file = tmp_info.split()
        cdr_tst = rslt_file[2]
        cdr_tst_tags = rslt_file[4].split(',')
        cdr_rslt_file = cdr_tst + "_" + ont_ver.replace('.','-') + "_" + cdr_tst_tags[1] + ".txt"
        # print(cdr_rslt_file)
        add_to_rslt_file(cdr_rslt_file,"#======================================== START OF TEST =========================================")
        add_to_rslt_file(cdr_rslt_file,"# Test Started: " + str(d))
        response = cdr.ont_send(cmd='\r', timeout=10)
        initialize = response['response']
        response = cdr.ont_send(cmd=cmd_exec, timeout=10)
        cmd_response = response['response']
        if dbglvl == 'dbg':
            print["CDR Cmd Response: " + str(cmd_response)]
        infoNew = cmd_response.split('\n')
        if dbglvl == 'dbg':
            print(infoNew)
        jobId = infoNew[1]
        jobId = jobId.strip('\r')
        print("\n#-----------------------------------------------------------------")
        print('{0:20} {1:50}'.format("# Test Suite: ", cmd_exec))
        print('{0:20} {1:50}'.format("# Job ID: ", jobId))
        time.sleep(10)
        print("#-----------------------------------------------------------------")
        cdr_test_running = False
        cdr_test_started = False
        jobIdFound = False
        while complete == False:
            if cdr_test_started == False:
                response = cdr.ont_send(cmd="buddyweb -status " + jobId, timeout=10)
                status = response['response']
                newStatus = status.split('\n')
                jobStatus = newStatus[1]
                jobStatus = jobStatus.strip('\r')
                if re.match(r'.*finished', jobStatus, re.S):
                    print('{0:20} {1:50}'.format("Job Status: ", "Test Completed!"))
                    complete = True
                else:
                    print('{0:20} {1:50}'.format("Job Status: ", jobStatus))
                    if re.match(r'.*running', jobStatus, re.S):
                        complete = False
                        time.sleep(30)
                        jobIdFound = True
                    elif re.match(r'.*starting', jobStatus, re.S):
                        complete = False
                        time.sleep(5)
                    else:
                        print("Received other status: " + jobStatus)
                        otherStatusCmd = "buddyweb -running"
                        response = cdr.ont_send(cmd=otherStatusCmd, timeout=10)
                        otherStatus = response['response']
                        print(otherStatus)
                        print(cdr_test)
                        if re.search(cdr_test, otherStatus, re.S):
                            print("Found Test Running: " + cdr_test)
                            cdr_test_running = True
                            cdr_test_started = True
                        else:
                            cdr_test_running = True
                            cdr_test_started = True
            else:
                while cdr_test_running == True:
                    response = cdr.ont_send(cmd=otherStatusCmd, timeout=10)
                    jobStatus = response['response']
                    if re.search('idle', jobStatus, re.S):
                        complete = True
                        cdr_test_running = False

        #-----------------------------------------------------------------------------------------
        # 2) Compile results and format for Pass/Fail Validation
        #
        if complete == True:
            print("#-----------------------------------------------------------------\n")
            cmd_exec1 = "buddyweb -status " + str(jobId)
            cmd_exec2 = cmd_exec1 + " -show-result-id"
            #print(cmd_exec2)
            rslt_dir_found = False
            if jobIdFound == True:
                while rslt_dir_found == False:
                    response = cdr.ont_send(cmd=cmd_exec2, timeout=10)
                    rslt_dir = response['response']
                    print(rslt_dir)
                    tmp_rslt_dir = rslt_dir.split('\n')
                    if len(tmp_rslt_dir) > 1:
                        rslt_dir = tmp_rslt_dir[1]
                        rslt_dir = rslt_dir.strip('\r')
                        rslt_dir_found = True
            else:
                alt_cmd_exec = "ps -ef | grep buddyweb"
                while rslt_dir_found == False:
                    response = cdr.ont_send(cmd=alt_cmd_exec, timeout=10)
                    cmd_resp = response['response']
                    if re.search('buddyd-id', cmd_resp, re.S):
                        tmp_rslt_dir = cmd_resp.split()
                        rslt_dir_idx = tmp_rslt_dir.index('-buddyd-id') + 1
                        rslt_dir = tmp_rslt_dir[rslt_dir_idx]
                        rslt_dir_found = True

            print('{0:20} {1:50}'.format("Result DIR: ", str(rslt_dir)))
            base_rslt_dir = rslt_dir[0:8]
            print('{0:20} {1:50}'.format("Base Result DIR: ", str(base_rslt_dir)))
            rslt_path = "/mnt/cdrResults/" + str(base_rslt_dir) + "/" + str(rslt_dir) + "/"
            if dbglvl == "dbg":
                rslt_path_cmd = "cd /mnt/cdrResults/" + str(base_rslt_dir) + "/" + str(rslt_dir)
                response = cdr.ont_send(cmd=rslt_path_cmd, timeout=10)
                dir_response = response['response']
                print(dir_response)
                response = cdr.ont_send(cmd="cat final.txt", timeout=20)
                rslt_info = response['response']
                print(rslt_info)
            resultsInfo = print2screen("final.txt", rslt_path, cdr_rslt_file, dbglvl)
            if resultsInfo == False:
                return False
            else:
                return True
        else:
            add_to_rslt_file(cdr_rslt_file,"# Test Failed to Start!")
            print("Test Failed to Complete!")
            return False
    #return resultsInfo

#-----------------------------------------------------------------------------------------------------
# Send command to E7
#
def e7_prov(csv, action, dev_type, scenario, cdr_test, params, dbglvl):
    # print("params : ", params)
    e72 = params['e7_session']
    cfg_rtrv = 0
    ont_check = 0
    ont_enabled = 0
    ont_disabled = 0
    cont_exec = 0
    rtrv_pwd = "bobo"
    rmv_ont_cfg = 0

    #-----------------------------------------------------------------------------------------
    #  Retrieve commands from CSV
    cmd_lst = get_cmds(csv, action, scenario, dev_type, 'null', dbglvl)

    #-----------------------------------------------------------------------------------------
    # Send commands to E7 from list
    for i in range(len(cmd_lst)):
        #--------------------------------------------------------------------
        # Retrieve command from CMD List based on index
        cmd_exec = cmd_lst[i]
        if re.search('native', cmd_exec, re.S):
            chk_ont_dflt = 1
        else:
            chk_ont_dflt = 0
        #--------------------------------------------------------------------
        # If command is retrieve ont-config set cfg_rtrv = 1
        # which is used later to execute the apply ont-config command
        #
        if re.search('retrieve', cmd_exec, re.S):
            cfg_rtrv = True
            print("RTRV Command found!")
        #--------------------------------------------------------------------
        # If command is set ont-port x/G1 instance then set ont_check = 1
        # Must exclude other commands with instance in them
        #
        if re.search('instance', cmd_exec, re.S):
            if not re.search('retrieve', cmd_exec, re.S):
                if not re.search('none', cmd_exec, re.S):
                    ont_check = True
                    ont_id_tmp = cmd_exec.split()
                    ont_id_tmp1 = ont_id_tmp[2]
                    ont_id = ont_id_tmp1[0:3]
                    print("ONT ID: " + str(ont_id))
                    print("ONT Check: " + str(ont_check))

        if re.search('remove', cmd_exec, re.S) and re.search('ont-config', cmd_exec, re.S):
            if re.search('rg-4', cmd_exec, re.S):
                ont_id = "813"
            elif re.search('rg-2', cmd_exec, re.S):
                ont_id = "844"
            else:
                ont_id = "836"
            ont_check = True
            rmv_ont_cfg = True
        #--------------------------------------------------------------------
        # Send command to E7 and place response from shelf in cmd_response
        #
        if cfg_rtrv == True:
            response = e72.ont_send(cmd=cmd_exec, timeout=60)
            cmd_response = response['response']
        else:
            response = e72.ont_send(cmd=cmd_exec, timeout=60)
            cmd_response = response['response']

        if rmv_ont_cfg == True:
            response = e72.ont_send(cmd="reset ont " + str(ont_id) + " rg-restore-defaults", timeout=10)
            cmd_response = response['response']
        #--------------------------------------------------------------------
        # If command is retrieve ont-config and 'Password:' is found in response
        # send password initialized below
        # Else treat command as regular command
        #
        if cfg_rtrv == True and re.search('Password:', cmd_response, re.S):
            response = e72.ont_send(cmd=rtrv_pwd, timeout=60)
            cmd_response = response['response']
        else:
            #--------------------------------------------------------------------
            # Check to see if the command is to remove the ont-config
            if action == "del" and re.search('remove ont-config', cmd_exec, re.I):
                if re.search('Complete', cmd_response, re.S):
                    print("ONT Config Removal Complete")
                else:
                    print("ONT Config Removal Failed")
            elif ont_check == True:
                #--------------------------------------------------------------------
                # Check to make sure ONT reset
                #
                cont_exec = ont_chk_dis(ont_id, params)
            else:
                #--------------------------------------------------------------------
                # Response for regular command
                #
                if re.search('success', cmd_response, re.S):
                    print("Command Executed!")
                else:
                    print("Command Failed!")
        #--------------------------------------------------------------------
        # If command is cfg_rtrv == 1 and action == add
        #
        if cfg_rtrv == True and action == "add":
            complete = False
            response = e72.ont_send(cmd="apply ont-config vendor CXNK", timeout=60)
            cmd_response = response['response']
            while complete == False:
                response = e72.ont_send(cmd="show upgrade", timeout=10)
                cmd_response = response['response']
                if not re.search('ONT Config file download performed', cmd_response, re.S):
                    print("Config Applied!")
                    complete = True
                else:
                    complete = False

        #--------------------------------------------------------------------
        # If ont_check == 1, execute loop to verify ONT reset and is enabled
        #
        if ont_check == True and cont_exec == True:
            time.sleep(10)
            ont_enabled = ont_chk_en(ont_id, params)
        elif ont_check == 1 and rmv_ont_cfg == 1:
            cont_exec = ont_chk_dis(ont_id, params)
            if cont_exec == True:
                ont_enabled = ont_chk_en(ont_id, params)

        if chk_ont_dflt == 1:
            tmp_ont_id = cmd_exec.split()[2]
            ont_id = tmp_ont_id.split('/')[0]
            cont_exec = ont_chk_dis(ont_id, params)
            if cont_exec == True:
                ont_enabled = ont_chk_en(ont_id, params)

    return ont_enabled

#-----------------------------------------------------------------------------------------------------
# Retrieve commands from CSV
def xc3_prov(csv, action, dev_type, scenario, cdr_test, params, dbglvl):
    #print("params : ", params)
    xc3 = params['xc3_session']
    # Retrieve commands from CSV
    cmd_lst = get_cmds(csv, action, scenario, dev_type, 'null', dbglvl)

    for i in range(len(cmd_lst)):
        complete = 0
        # Retrieve command from CMD List
        cmd_exec = cmd_lst[i]
        # print(cmd_exec)
        tmp_cmd_exec = cmd_exec
        tmp_cmd_exec = tmp_cmd_exec.split()
        interface = tmp_cmd_exec[2]
        #print(interface)
        if re.search('delete', cmd_exec, re.S):
            response = xc3.ont_send(cmd="show tag-action")
            cmd_response = response['response']
            # print(cmd_response.split())
            if re.search("No", cmd_response, re.S):
                print("No Tag Actions!")
            else:
                if re.search(interface, cmd_response, re.S):
                    cmd_resp = cmd_response.split()
                    tag_index = cmd_resp.index(interface)
                    tag_index = tag_index - 1
                    # print(cmd_resp[tag_index])
                    response = xc3.ont_send(cmd="delete tag-action " + str(cmd_resp[tag_index]))
                    cmd_response = response['response']
                else:
                    print("Tag Action not found for: " + str(interface))
        else:
            response = xc3.ont_send(cmd=cmd_exec, timeout=10)
            cmd_response = response['response']
        if re.search(r'success', cmd_response, re.S):
            print("Command Executed!")
            return True
        else:
            print("Command Failed!")
            return False