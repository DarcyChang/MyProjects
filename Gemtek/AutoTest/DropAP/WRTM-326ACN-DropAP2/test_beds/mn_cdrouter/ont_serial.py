__author__ = 'bmelhus'

import re,time

#-----------------------------------------------------------------------------------------------
#
#
def ont_rstr_dflt(eut, params):
    ont = params['ont_session']

    ont_conn = False
    while ont_conn == False:
        response = ont.ont_send(cmd="wan show", timeout=20)
        cmd_response = response['response']
        #print("CMD Response: " + str(cmd_response))
        if re.search('ipoe', cmd_response, re.S):
            ont.ont_send(cmd='\r')
            time.sleep(1)
            response = ont.ont_send(cmd="restoredefault", timeout=10)
        elif re.search(eut, cmd_response, re.S):
            ont.ont_send(cmd='\r')
            time.sleep(1)
            response = ont.ont_send(cmd="restoredefault", timeout=10)
        time.sleep(1)
        rst_response = response['response']

        if re.search('The system shell is being reset', rst_response, re.S):
            print("ONT was reset!")
            ont_conn = True
    if ont_conn == True:
        return True
    else:
        return False

#-----------------------------------------------------------------------------------------------
#
#
def rg_chk(eut, rg_scenario, params):
    ont = params['ont_session']

    print("Checking Download Status!")
    scenario = rg_scenario.split('-')[0]
    wan_not = 0
    time_sleep = 5
    while wan_not <= 20:
        response = ont.ont_send(cmd="wan show", timeout=30)
        cmd_response = response['response']
        #print("RG Check CMD Response: " + cmd_response)
        if re.search(eut, cmd_response, re.S) and re.search(scenario, cmd_response, re.S):
            return True
        else:
            wan_not += 1
            time.sleep(time_sleep)
            time_sleep += 5
    return False

def ont_conn_status(eut):
    ont = params['ont_session']
    ont_conn = False
    while ont_conn == False:
        response = ont.ont_send(cmd="wan show", timeout=10)
        cmd_response = response['response']
        if re.search('ipoe', cmd_response, re.S):
            return True
        elif re.search(eut, cmd_response, re.S):
            return True