*** Settings ***

*** Variable ***
# common
${g_mgmt_vlan}      900
${g_data_vlan}      1100
${g_video_vlan}
${g_voice_vlan}

${g_input_enter}      \x0d
${g_input_ctrl_c}     \x03

${g_ip_format}    \\d+\\.\\d+\\.\\d+\\.\\d+

# E7
${g_e7_device}          e7
${g_e7_us_port}         1/g3
${g_e7_gpon_port}       1/3

# ONT
${g_ont_id}             119
${g_ont_type}           GIA
${g_ont_sn}             166E4A
${g_ont_port}           g1
${g_ont_svc}            Data3

# DPU
${g_dpu_device}         dpu
${g_dpu_us_port}        g1
${g_dpu_gfast_port}     gfast2
${g_dpu_us_prf}         auto_upstream

# 801F
${g_801f_device}        801f
${g_801f_mgmt_vlan}     85
${g_801f_wan_port}      pon0.85
${g_801f_cli_user}      root
${g_801f_cli_pwd}       superuser
${g_801f_cli_exit}      exit
${g_801f_lan_ip}       192.168.1.1
${g_801f_lan_mac}
${g_801f_wan_mac}
${g_801f_gui_session}   gui
${g_801f_gui_url}       http://192.168.1.1
${g_801f_gui_user}      admin
${g_801f_gui_pwd}       admin
${g_801f_image}
${g_801f_sn}
${g_801f_show_version}   cat /root/version
${g_801f_prompt}        ~ #
${g_801f_tftp_update}    tftp_update.sh
#${g_801f_default_acs_url}    https://gcs.calix.com:8443
#${g_801f_default_acs_user}   ''
#${g_801f_default_acs_pwd}    activate-cxnk
${g_801f_default_acs_url}    http://preview-gcs.calix.com:8080
${g_801f_default_acs_user}   admin
${g_801f_default_acs_pwd}    admin

# ACS
${g_acs_url}        http://10.245.250.98:8080/testmin
${g_acs_usr}        tr069
${g_acs_pwd}        tr069
${g_acs_req_usr}    admin
${g_acs_req_pwd}    admin
${g_acs_interval}    86400

# CC+
${g_ccplus_device}
${g_cc_web_url}
${g_cc_usrname}
${g_cc_password}
${g_org_id}
${g_cc_acs_server}
${g_cc_dwl_ont_load_path}

# Traffic Generator
${g_tg_device}    tg
${g_tg_uport}    uport
${g_tg_dport}    dport
${g_tg_store_file_path}
