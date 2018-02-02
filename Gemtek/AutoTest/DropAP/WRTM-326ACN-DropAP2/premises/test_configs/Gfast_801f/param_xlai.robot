*** Settings ***

*** Variable ***
# common
${g_mgmt_vlan}
${g_data_vlan}
${g_video_vlan}
${g_voice_vlan}

${g_input_enter}      \x0d
${g_input_ctrl_c}     \x03

#E7
${g_e7_us_port}
${g_e7_gpon_port}
${g_data_vlan}     85
#ONT
${g_ont_id}
${g_ont_type}           GIA
${g_ont_sn}
${g_ont_port}           g1
${g_ont_svc}            Data1
#DPU
${g_dpu_device}         dpu5
${g_dpu_us_port}        g1
${g_dpu_gfast_port}     gfast3
${g_dpu_us_prf}
#801F
${g_801f_device}        801f
${g_801f_mgmt_vlan}     900
${g_801f_image2}     Pre801F_2.0.0.0.oneimage
${g_801f_image}     Pre801F_2.0.1.0.oneimage
${g_801f_sn}        CXNK1C497B27D896
#${g_801f_sn}        CXNK1C497B4EF533

#ACS
${g_acs_url}        http://10.245.250.98:8080/testmin
#${g_acs_url}        http://192.168.33.200:8080
${g_acs_usr}        tr069
${g_acs_pwd}        tr069
${g_acs_req_usr}    admin
${g_acs_req_pwd}    admin
${g_acs_interval}    86400

#CC+
${g_ccplus_device}     ccplus_98
${g_cc_web_url}    http://10.245.250.97:3000/login
${g_cc_usrname}    testmin2
${g_cc_password}    Pitt12me
${g_org_id}    51
${g_cc_acs_server}    http://10.245.250.98:8081
${g_cc_dwl_ont_load_path}   /home/xlai

#TG
${g_tg_device}    tg1
