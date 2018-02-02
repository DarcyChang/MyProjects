#!/usr/bin/env python
# Author: Me
# Purpose: SSH into list of devices and run list of commands

__author__ = 'bmelhus'

import csv,re

def get_fw_cfg(csv_filename, scenario):
    command_file = csv_filename
    #----------------------------------------
    # Opens files in read mode
    #----------------------------------------
    cmd_file = open('/opt/home/bmelhus/stp/test_beds/mn_cdrouter/data/' + command_file, "r")
    csv_f = csv.reader(cmd_file)
    if csv_f != "":
        print("Command File Opened: " + command_file)
    else:
        print("Command File not Found.")
    fw_service = []
    fw_svc_state = []
    for row in csv_f:
        row_scenario = row[0]
        #print(row_scenario)
        #print(row)
        if re.search("Scenario", row_scenario, re.S):
            service_len = len(row)
            #print("Number of Services: " + str(service_len))
            for i in range(1,service_len,1):
                fw_service.append(row[i])
        if re.search(scenario, row_scenario, re.S):
            service_len = len(row)
            #print("Number of Services: " + str(service_len))
            for i in range(1,service_len,1):
                fw_svc_state.append(row[i])
    # for i in range(len(fw_service)):
    #     print("Service: " + fw_service[i] + " State: " + fw_svc_state[i])
    cmd_file.close()
    return fw_service, fw_svc_state


def get_cmds(csv_filename, cmd_action, rg_scenario, dev_type, cdr_test, dbglvl):
    command_file = csv_filename
    action = cmd_action
    #print("CDR Test Scenario: " + str(cdr_test))
    if cdr_test != "null":
        tmp_scenario = cdr_test.split('_')
        #print("Tmp Scenario: " + str(tmp_scenario[1]))
        match_scenario = tmp_scenario[1]
    #----------------------------------------
    # Opens files in read mode
    #----------------------------------------
    cmd_file = open('/opt/home/bmelhus/stp/test_beds/mn_cdrouter/data/' + command_file, "r")
    csv_f = csv.reader(cmd_file)
    if csv_f != "":
        print("Command File Opened: " + command_file)
    else:
        print("Command File not Found.")

    e7_add_cmds = []
    e7_del_cmds = []
    issue_cmd = []
    cdrFile = 0

    # Row[0] == Execute CMD (y|n) (ALL CSVs)
    # Row[1] == Add CMD (ALL CSVs)
    # Row[2] == Del CMD (ALL CSVs except for CD Router)
    # Row[3] == MATCH to scenario
        # CD Router CSV      ==     Scenario
        # Eth Svc CSV        ==     ONT Type_(multi|cdr)
        # ONT Config Load    ==     Scenario
        # X-CONN CSV         ==     ONT-Type_(multi|cdr)
        # RG Instance        ==     ONT-Type_(multi|cdr)
        # RG Mgmt Prof       ==     ONT-Type_(multi|cdr)

    for row in csv_f:
        exec_row = row[0]
        match_value = row[3]
        if cmd_action == "add":
            add_cmd = row[1]
            del_cmd = row[5]
        elif cmd_action == "del":
            add_cmd = row[5]
            del_cmd = row[2]
        #print("match value: " + str(match_value))
        #print("device type: " + str(dev_type))
        if re.search('cdr', command_file, re.S):
            cdrFile = 1
        if dbglvl == "dbg" and exec_row == "y":
            print("This is row:\n" + str(row[2]))
        if dbglvl == "dbg":
            print('#######################################')
            print('{0:20} {1:50}'.format('# Execute Command: ', row[0]))
            print('{0:20} {1:50}'.format('# Add Command: ', row[1]))
            print('{0:20} {1:50}'.format('# Delete Command: ', row[2]))
            print('#######################################\n')
        if exec_row == "y" and match_value == dev_type:
            print("Basic E7/XCONN Config")
            issue_cmd.append(exec_row)
            e7_add_cmds.append(add_cmd)
            e7_del_cmds.append(del_cmd)
        elif exec_row == "y" and cdrFile == 1:
            tmp_add_cmd = add_cmd
            tmp_add_cmd1 = tmp_add_cmd.split()
            tmp_add_cmd2 = tmp_add_cmd1[2]
            tmp_add_cmd3 = tmp_add_cmd2.split('_')
            #print("Scenario: " + tmp_add_cmd3[1])
            cdr_scenario = tmp_add_cmd3[1]
            #print("Match scenario: " + match_scenario)
            if dev_type == row[5] and cdr_test == match_value:
                if re.search(cdr_scenario, match_scenario, re.IGNORECASE):
                    issue_cmd.append(exec_row)
                    e7_add_cmds.append(add_cmd)
                    e7_del_cmds.append(del_cmd)
            elif dev_type == row[5] and re.search('all', cdr_test, re.I):
                #print("CD Router Config with Match Criteria - ALL")
                #print(tmp_add_cmd)
                #print(match_scenario)
                if re.search(cdr_scenario, match_scenario, re.IGNORECASE):
                    issue_cmd.append(exec_row)
                    e7_add_cmds.append(add_cmd)
                    e7_del_cmds.append(del_cmd)

    #----------------------------------------
    # Creates list based on f1 and f2
    #----------------------------------------
    cmds = []
    cmd_exec = []

    #----------------------------------------------------------------------------------------
    # This function loops through devices. No real need for a function here, just doing it.
    #----------------------------------------------------------------------------------------
    if action == 'add':
        cmds = e7_add_cmds
        cmd_exec = issue_cmd
    elif action == 'del':
        cmds = list(reversed(e7_del_cmds))
        cmd_exec = list(reversed(issue_cmd))
    else:
        print('No Commands!')

    for i in range(len(cmds)):
        run_cmd = cmd_exec[i]
        if run_cmd == 'y':
            #--------------------------------------------------------------------
            # This strips \n from end of each command (line) in the commands list
            command = cmds[i]
            if command != "" and dbglvl == "info":
                print('{0:20} {1:50}'.format('Execute Command: ', command))
    return cmds

    cmd_file.close()

def get_cfg_info(csv_filename, rg_scenario, dev_type, dbglvl):
    command_file = csv_filename
    #print("CDR Test Scenario: " + str(cdr_test))
    #----------------------------------------
    # Opens files in read mode
    #----------------------------------------
    cmd_file = open('/opt/home/bmelhus/stp/test_beds/mn_cdrouter/data/' + command_file, "r")
    csv_f = csv.reader(cmd_file)
    if csv_f != "":
        print("Command File Opened: " + command_file)
    else:
        print("Command File not Found.")

    cfg_file_names = []
    dev_type_names = []
    issue_cmd = []

    # Row[0] == Execute CMD (y|n) (ALL CSVs)
    # Row[1] == cfg_file_names
    # Row[2] == dev_type_names
    # Row[3] == rg_scenario

    for row in csv_f:
        exec_row = row[0]
        match_value = row[3]
        cfg_file_csv = row[1]
        dev_type_csv = row[2]
        if dbglvl == "dbg" and exec_row == "y":
            print("This is row:\n" + str(row[2]))
        if dbglvl == "dbg":
            print('#######################################')
            print('{0:20} {1:50}'.format('# Execute Command: ', row[0]))
            print('{0:20} {1:50}'.format('# Config File: ', row[1]))
            print('{0:20} {1:50}'.format('# ONT Type: ', row[2]))
            print('{0:20} {1:50}'.format('# RG Scenario: ', row[3]))
            print('#######################################\n')
        if exec_row == "y" and match_value == rg_scenario and dev_type == dev_type_csv:
            issue_cmd.append(exec_row)
            cfg_file_names.append(cfg_file_csv)
            dev_type_names.append(dev_type_csv)

    return cfg_file_names,dev_type_names

    cmd_file.close()
# END
