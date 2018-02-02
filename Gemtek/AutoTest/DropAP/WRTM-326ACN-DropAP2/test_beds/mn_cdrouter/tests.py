__author__ = 'bmelhus'

import re
from stp.test_beds.mn_cdrouter.ontgui_config import conf_tr069
from stp.test_beds.mn_cdrouter.ontgui_config import rstr_dflts
from stp.test_beds.mn_cdrouter.ontgui_config import chk_cfg_dld_cmplt
from stp.test_beds.mn_cdrouter.ont_gui_fw import config_fw
from stp.test_beds.mn_cdrouter.cdRouterParser import print2screen

# cmd_exec = 'set ont-port 836/G1 mgmt-mode native'
#
# if re.search('native', cmd_exec, re.S):
#     tmp_ont_id = cmd_exec.split()[2]
#     ont_id = tmp_ont_id.split('/')[0]
#     print(ont_id)
#
# rstr_dflts()
# #conf_tr069()
# dld_ont = chk_cfg_dld_cmplt(eut="844E", rg_scenario="6rd")

# cmd_exec = 'buddyweb -package 1f_DS_v4-6_dns -tags P11.1M7,800GH -jobid'
# ont_ver = '11-1-80-10'
#
# ver_rep = cmd_exec.split()[4]
# ver_rep = ver_rep.split(',')
# ver_rep = ont_ver + "," + ver_rep[1]
# cmd_exec = cmd_exec.replace(cmd_exec.split()[4], ver_rep)
# print(cmd_exec)

# fw_svcs, fw_svc_state = get_fw_cfg(csv_filename="fw_in.csv", scenario="test_1")
# for i in range(len(fw_svcs)):
#         print("Service: " + fw_svcs[i] + " == " + fw_svc_state[i])

#configure_fw = config_fw(csv_filename="fw_in.csv", scneario="test_1")

print2screen(resultfile="final.txt", rslt_path="/mnt/cdrResults/20151204/20151204070918/", cdr_rslt_file="1f_DS_bogus_bogus_11-1-90-2_800GH.txt", dbglvl="dbg")