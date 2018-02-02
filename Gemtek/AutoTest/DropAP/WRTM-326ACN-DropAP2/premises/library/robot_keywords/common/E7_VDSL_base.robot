*** Settings ***
Resource          caferobot/cafebase.robot
Resource          premises/library/robot_keywords/common/E7_base.robot

*** Keywords ***

E7_check_vdsl_port_status
    [Arguments]    ${device}   ${vdsl_port}
    ${result}    cli    ${device}   show dsl-port ${vdsl_port}
    should contain    ${result}    Showtime
    [Return]    ${result}

E7_create_mcast_map
    [Arguments]    ${device}    ${mcast_map}    ${mcast_group_start}    ${mcast_group_end}
    ${result}    cli    ${device}    create mcast-map ${mcast_map}
    log to console    ${result}
    should contain    ${result}    success
    ${result}    cli    ${device}    add range to-mcast-map ${mcast_map} mcast ${mcast_group_start}-${mcast_group_end}
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}

E7_delete_mcast_map
    [Arguments]    ${device}    ${mcast_map}   ${mcast_range_index}
    ${result}    cli    ${device}    remove range ${mcast_range_index} from-mcast-map ${mcast_map}
    should contain    ${result}    success
    ${result}    cli    ${device}    delete mcast-map ${mcast_map}
    should contain    ${result}    success
    [Return]    ${result}

E7_create_mcast_profile
    [Arguments]    ${device}    ${mcast_profile}   ${mcast_max_strms}    ${mcast_map}
    ${result}   cli    ${device}    create mcast-profile ${mcast_profile} max-strms ${mcast_max_strms} mcast-map ${mcast_map}
    should contain    ${result}    success
    [Return]    ${result}


E7_delete_mcast_profile
    [Arguments]    ${device}    ${mcast_profile}
    ${result}    cli    ${device}   delete mcast-profile ${mcast_profile}
    should contain    ${result}    success
    [Return]    ${result}

E7_create_mcast_vlan
    [Arguments]    ${device}    ${mcast_vlan}
    ${result}    cli    ${device}    create vlan ${mcast_vlan}
    should contain    ${result}    success
    ${result}    cli    ${device}    set vlan ${mcast_vlan} igmp-mode snoop-suppress
    should contain    ${result}    success
    [Return]    ${result}

E7_delete_mcast_vlan
    [Arguments]    ${device}    ${mcast_vlan}
    ${result}    cli    ${device}    delete vlan ${mcast_vlan}
    should contain    ${result}    success
    [Return]    ${result}

E7_prov_uplinkport
    [Arguments]    ${device}   ${mcast_uplinkport}   ${mcast_vlan}
    ${result}    cli    ${device}    set eth-port ${mcast_uplinkport} admin-state enable
    log to console    ${result}
    should contain    ${result}    success

    ${result}    cli    ${device}    set interface ${mcast_uplinkport} role trunk admin-state enable
    log to console    ${result}
    should contain    ${result}    success

    ${result}    cli    ${device}    add interface ${mcast_uplinkport} to-vlan ${mcast_vlan}
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}

E7_depro_uplinkport
    [Arguments]    ${device}   ${mcast_uplinkport}   ${mcast_vlan}
    ${result}    cli    ${device}    remove interface ${mcast_uplinkport} from-vlan ${mcast_vlan}
    log to console    ${result}

    ${result}    cli    ${device}    set interface ${mcast_uplinkport} admin-state disable
    log to console    ${result}
    sleep    5
    #cli    E7    \x0d

    ${result}    cli    ${device}    set eth-port ${mcast_uplinkport} admin-state disable
    log to console    ${result}
    sleep    5
    #cli    E7    \x0d
    [Return]    ${result}


E7_VDSL_add_videoservice
    [Arguments]    ${device}   ${vdsl_svc}   ${vdsl_port}  ${mcast_bw_profile}  ${mcast_profile}
    ${result}    cli    ${device}   add eth-svc ${vdsl_svc} to-interface ${vdsl_port} bw-profile ${mcast_bw_profile} svc-tag-action ${svc_tag_action_name} mcast-profile ${mcast_profile} admin-state enabled
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}


E7_VDSL_remove_videoservice
    [Arguments]    ${device}    ${vdsl_svc}     ${vdsl_port}
    ${result}    cli  ${device}  remove eth-svc ${vdsl_svc} from-interface ${vdsl_port}
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}


VDSL_pro_videoservice

    [Arguments]    ${device}   ${mcast_vlan}  ${mcast_uplinkport}  ${mcast_map}  ${mcast_group_start}  ${mcast_group_end}  ${mcast_profile}  ${mcast_max_strms}   ${mcast_bw_profile}  ${uspir}  ${uscir}  ${dspir}  ${svc_match_name}  ${svc_tag_action_name}  ${tag_action_type}  ${vdsl_svc}

    #check the status of vdsl port
    E7_check_vdsl_port_status  ${device}  ${vdsl_port}

    #create mcast vlan
    E7_create_mcast_vlan  ${device}  ${mcast_vlan}

    #add mcast vlan to the uplink port
    E7_prov_uplinkport  ${device}  ${mcast_uplinkport}  ${mcast_vlan}

    #create mcast-map
    E7_create_mcast_map  ${device}  ${mcast_map}  ${mcast_group_start}  ${mcast_group_end}

    #create mcast-profile
    E7_create_mcast_profile  ${device}   ${mcast_profile}   ${mcast_max_strms}  ${mcast_map}

    # create bandwidth profile
    #${bw_prf}    set variable    ${cfg_prefix}_bw
    E7_create_bw_prf    ${device}    ${mcast_bw_profile}    ${uspir}    ${uscir}    ${dspir}

    # create match-list
    #${match_list}    set variable    ${cfg_prefix}_MatchList_v${mcast_vlan}
    E7_create_match_list   ${device}    ${svc_match_name}   ${mcast_vlan}

    # create svc-tag-action
    #${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${mcast_vlan}
    E7_create_svc_tag_action    ${device}    ${svc_tag_action_name}    ${tag_action_type}    ${svc_match_name}    ${mcast_vlan}

    # bound service to ont port
    E7_VDSL_add_videoservice   ${device}   ${vdsl_svc}   ${vdsl_port}   ${mcast_bw_profile}   ${mcast_profile}

    [Return]


VDSL_depro_videoservice

    [Arguments]    ${device}   ${vdsl_svc}   ${vdsl_port}  ${mcast_profile}   ${mcast_map}  ${mcast_range_index}  ${mcast_bw_profile}  ${svc_tag_action_name}  ${svc_match_name}  ${mcast_uplinkport}   ${mcast_vlan}
    E7_VDSL_remove_videoservice  ${device}    ${vdsl_svc}     ${vdsl_port}

    E7_delete_mcast_profile   ${device}    ${mcast_profile}

    E7_delete_mcast_map  ${device}    ${mcast_map}   ${mcast_range_index}

    E7_delete_profile  ${device}  bw-profile  ${mcast_bw_profile}

    E7_delete_profile  ${device}  svc-tag-action  ${svc_tag_action_name}

    E7_delete_match_list   ${device}   ${svc_match_name}

    E7_depro_uplinkport  ${device}   ${mcast_uplinkport}   ${mcast_vlan}

    E7_delete_mcast_vlan   ${device}    ${mcast_vlan}

    [Return]







