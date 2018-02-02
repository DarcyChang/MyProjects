*** Settings ***

*** Variable ***
# common
${g_mgmt_vlan}          900
${g_data_vlan}          700
${g_video_vlan}
${g_voice_vlan}

${g_input_enter}      \x0d
${g_input_ctrl_c}     \x03

# ACS
${g_acs_url}        http://10.245.250.98:8080/testmin
${g_acs_usr}        tr069
${g_acs_pwd}        tr069
${g_acs_req_usr}    admin
${g_acs_req_pwd}    admin
${g_acs_interval}    86400

# CC+
${g_cc_web_url}
${g_cc_usrname}
${g_cc_password}

# 801F common
${g_801f_mgmt_vlan}     85
${g_801f_wan_port}      pon0.85
${g_801f_cli_user}      root
${g_801f_cli_pwd}       superuser
${g_801f_lan_ip}       192.168.1.1
${g_801f_gui_session}   gui
${g_801f_gui_url}       http://192.168.1.1
${g_801f_gui_user}      admin
${g_801f_gui_pwd}       admin
#${g_801f_default_acs_url}    https://gcs.calix.com:8443
#${g_801f_default_acs_user}   ''
#${g_801f_default_acs_pwd}    activate-cxnk
${g_801f_default_acs_url}    http://preview-gcs.calix.com:8080
${g_801f_default_acs_user}   admin
${g_801f_default_acs_pwd}    admin

###################################testbed1#########################################
# E7
${g_e7_device}          e7
${g_e7_gpon_port}       2/4

# ONT
${g_ont_id}             119
${g_ont_type}           GIA
${g_ont_sn}             189894
${g_ont_port}           g1
${g_ont_svc}            Data8

# DPU
${g_dpu_device}         dpu
${g_dpu_us_port}        g1
${g_dpu_us_prf}         lai_test

####################cpe1###########################
${g_e7_us_port}         1/g4
${g_dpu_gfast_port}     gfast11

# 801F
${g_801f_device}        801f
${g_801f_image}
${g_801f_sn}
${g_801f_lan_mac}   1C:49:7B:27:D8:B2
${g_801f_wan_mac}   6E:49:7B:27:D8:B2

# Traffic Generator
${g_tg_device}    tg_stc
${g_tg_uport}    uport
${g_tg_dport}    dport
${g_tg_store_file_path}    /home/cgao/tg_store

#####################cpe2###########################
#${g_e7_us_port}         1/g2
#${g_dpu_gfast_port}     gfast7
#
## 801F
#${g_801f_device}        801f_new
#${g_801f_image}
#${g_801f_sn}
#${g_801f_lan_mac}   1C:49:7B:4E:F4:29
#${g_801f_wan_mac}   6E:49:7B:4E:F4:29
#
## Traffic Generator
#${g_tg_device}    tg_stc
#${g_tg_uport}    uport
#${g_tg_dport}    dport
#${g_tg_store_file_path}    /home/cgao/tg_store

###################################testbed2#########################################
## E7
#${g_e7_device}          e7_p
#${g_e7_us_port}         2/g4
#${g_e7_gpon_port}       2/2
#
## ONT
#${g_ont_id}             2500
#${g_ont_type}           GIA
#${g_ont_sn}
#${g_ont_port}           g1
#${g_ont_svc}            Data6
#
## DPU
#${g_dpu_device}         dpu_p
#${g_dpu_us_port}        g1
#${g_dpu_gfast_port}     gfast5
#${g_dpu_us_prf}         100
#
## 801F
#${g_801f_device}        801f_p
#${g_801f_image}
#${g_801f_sn}
#${g_801f_lan_mac}    1C:49:7B:27:D6:7C
#${g_801f_wan_mac}    6E:49:7B:27:D6:7C
#
## Traffic Generator
#${g_tg_device}    tg_stc
#${g_tg_uport}    uport
#${g_tg_dport}    dport


