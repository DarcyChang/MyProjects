*** Settings ***

*** Variable ***
# common
${g_mgmt_vlan}      666
${g_data_vlan}      666
${g_video_vlan}
${g_voice_vlan}
${g_input_enter}      \x0d
${g_input_ctrl_c}     \x03
${g_ip_format}    \\d+\\.\\d+\\.\\d+\\.\\d+

# E7
${g_e7_device}          e7
${g_e7_us_port}         1/g6
${g_e7_eth_port}
${g_e7_gpon_port}       1/1
${uscir}          0
${uspir}          200m
${dspir}          800m
${cfg_prefix}     844G


# ONT

${g_ont_id}             800
${g_ont_type}           844G
${g_ont_sn}            2BAC6F
${g_ont_port}           G1
${g_ont_svc}            Data1
${EUT}            fam-800GE-AE
${ontip}          http://192.168.1.1
${browser}        firefox
${username}       support
${password}       support
${dmzhost}        192.168.1.253
${g_ont_pppoe_username}    qacafe
${g_ont_pppoe_password}    admin


#CD-Router package

${cdrouter_rf}    cdrouter_rf
${cdr_ip}         10.245.10.205

#tms
${tms}            tms
${assignee}       sashi
${FixVersion}     P-R11.2.3
${Buildtest}      11.2.3.57
${filter_800E}    project = "Premises ONT" and fixVersion = REGRESSION and "Sub Feature" ~ "DNS" and "Sub Feature" !~ "DNS-TCP" and EUT ~ 800E and "Group Ownership" = ST
${filter_800E_tr69}    Grouping ~ "Scope1" and assignee =blwang AND Feature ~"TR-069" and EUT ~ 800E
${filter_800G_tr69}    Grouping ~ "Scope1" and assignee =blwang AND Feature ~"TR-069" and EUT ~ 800G and fixVersion = REGRESSION
${User_Interface}    CLIRGGUI
#${User_Interface_tr069}    CD-Router
${User_Interface_tr069}    CLIRGGUI
#${EUT_800G}            800G
#${EUT_800E}            800E