*** Settings ***
Documentation     E7 basic provision Library

Resource    caferobot/cafebase.robot
#Resource    premises/test_configs/Gfast_801f/param.robot

*** Variables ***
${cfg_prefix}       auto
#${uscir}            0
#${uspir}            50m
#${dspir}            100m
#${tag_action_type}  change-tag



*** Keywords ***
E7_create_ont
    [Arguments]    ${device}    ${ont_id}    ${ont_type}=${g_ont_type}    ${ont_sn}=${g_ont_sn}
    [Documentation]    [Author:cgao] Description: create ont by ont id, ont type and ont serial number
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | ont_id | ONT logical ID |  |
	...    | ont_type | ONT profile name | ${ont_type} setting in global parameter file |
    ...    | ont_sn | ONT serial number | ${ont_sn} setting in global parameter file |
    ...
    ...    Example:
    ...    | E7_create_ont | E7 | 100 |
	...    | E7_create_ont | E7 | 100 | 844G | 16684E |
    # create ont
    ${result}    cli    ${device}    create ont ${ont_id} profile ${ont_type} serial-number ${ont_sn}
    Run Keyword And Ignore Error     should contain    ${result}    success
    ${result}    cli    ${device}    show ont ${ont_id}
    should not contain    ${result}    not found
    [Return]    ${result}

E7_delete_ont
    [Arguments]    ${device}    ${ont_id}
    [Documentation]    [Author:cgao] Description: delete ont by ont id
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ONT logical ID |
    ...
    ...    Example:
    ...    | E7_delete_ont | E7 | 100 |
    # delete ont
    ${result}    cli    ${device}    delete ont ${ont_id} force
    should contain    ${result}    success
    [Return]    ${result}

E7_create_vlan
    [Arguments]    ${device}    ${vlan_id}
    [Documentation]    [Author:cgao] Description: create vlan by vlan id
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | vlan_id | VLAN ID |
    ...
    ...    Example:
    ...    | E7_create_vlan | E7 | 1000 |
    # create vlan
    ${result}    cli    ${device}    create vlan ${vlan_id}
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    show vlan ${vlan_id}
    should not contain    ${result}    not found
    [Return]    ${result}

E7_delete_vlan
    [Arguments]    ${device}    ${vlan_id}
    [Documentation]    [Author:cgao] Description: delete vlan by vlan id
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | vlan_id | VLAN ID |
    ...
    ...    Example:
    ...    | E7_delete_vlan | E7 | 1000 |
    # delete vlan
    ${result}    cli    ${device}    delete vlan ${vlan_id}
    [Return]    ${result}

E7_create_mcast_map
    [Arguments]    ${device}    ${mcast_map}    ${mcast_group_start}    ${mcast_group_end}
    ${result}    cli    ${device}    create mcast-map ${mcast_map}
    Run Keyword And Ignore Error     should contain    ${result}    success
    ${result}    cli    ${device}    add range to-mcast-map ${mcast_map} mcast ${mcast_group_start}-${mcast_group_end}
    Run Keyword And Ignore Error     should contain    ${result}    success
    ${result}    cli    ${device}    show mcast-map ${mcast_map}
    should not contain    ${result}    not found
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
    Run Keyword And Ignore Error     should contain    ${result}    success
    ${result}    cli    ${device}    show mcast-profile ${mcast_profile}
    should not contain    ${result}    not found
    [Return]    ${result}

E7_delete_mcast_profile
    [Arguments]    ${device}    ${mcast_profile}
    ${result}    cli    ${device}   delete mcast-profile ${mcast_profile}
    should contain    ${result}    success
    [Return]    ${result}

E7_add_ont_video_svc
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${mcast_profile}    ${svc_tag_action}
    [Documentation]    [Author:blwang] Description: add eth-video-svc to ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
    ...    | ont_svc | Name of Ethernet service |
	...    | bw_prf | Name of bandwidth profile |
    ...    | svc_tag_action | Name of service tag-action |
    ...
    ...    Example:
    ...    | E7_add_ont_video_svc | E7 | 100 | g1 | Data1 | test_bw_prf | test_tag_action |
    # bound service to ont port
    ${result}    cli    ${device}    add eth-svc ${ont_svc} to-ont-port ${ont_id}/${ont_port} bw-profile ${bw_prf} svc-tag-action ${svc_tag_action} mcast-profile ${mcast_profile} admin-state enabled
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} eth-svc ${ont_svc}
    Should Match Regexp    ${result}    ${ont_svc}+[\\s\\S]*${ont_id}/${ont_port}+[\\s\\S]*${bw_prf}+[\\s\\S]*${svc_tag_action}
    [Return]    ${result}

E7_remove_ont_video_svc
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}
    [Documentation]    [Author:blwang] Description: remove eth-video-svc from ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
    ...    | ont_svc | Name of Ethernet service |
    ...
    ...    Example:
    ...    | E7_remove_ont_video_svc | E7 | 100 | g1 | Data1 |
    # bound service to ont port
    ${result}    cli    ${device}    remove eth-svc ${ont_svc} from-ont-port ${ont_id}/${ont_port}

    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} eth-svc ${ont_svc}
    Should contain    ${result}    not found
    [Return]    ${result}

E7_prov_port
    [Arguments]    ${device}    ${port}    ${vlan_id}    ${role}=trunk
    [Documentation]    [Author:cgao] Description: enable interface, set role and add port to vlan
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | port | interface name <card/port> |  |
	...    | vlan_id | vlan id that you want to add to port |  |
    ...    | role | Role of this interface | trunk |
    ...
    ...    Example:
    ...    | E7_prov_port | E7 | 1/g1 | 100 |
	...    | E7_prov_port | E7 | 1/g1 | 100 | edge |
    # enable port and add vlan to upstream port
    ${result}    cli    ${device}    set eth-port ${port} admin-state enable
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    set interface ${port} role ${role} admin-state enable
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    add interface ${port} to-vlan ${vlan_id}
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    show vlan ${vlan_id} members
    Should Match Regexp    ${result}    ${vlan_id}.*${port}
    [Return]    ${result}

E7_deprov_port
    [Arguments]    ${device}    ${port}    ${vlan_id}
    [Documentation]    [Author:cgao] Description: remove port from vlan and disable interface
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | port | interface name <card/port> |
	...    | vlan_id | vlan id that you want to add to port |
    ...
    ...    Example:
    ...    | E7_deprov_port | E7 | 1/g1 | 100 |
    # remove interface from vlan
    ${result}    cli    ${device}    remove interface ${port} from-vlan ${vlan_id}

#    ${result}    cli    ${device}    set interface ${port} admin-state disable
#    sleep    5
#    cli    ${device}    \x0d
#
#    ${result}    cli    ${device}    set eth-port ${port} admin-state disable
#    sleep    5
#    cli    ${device}    \x0d
    [Return]    ${result}

E7_create_match_list
    [Arguments]    ${device}    ${name}    ${vlan}    ${pbit}=any
    [Documentation]    [Author:cgao] Description: create svc-match-list and add rule to it
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | name | Name of service match-list |  |
	...    | vlan | VLAN ID of outer tag |  |
    ...    | pbit | p-bit value of outer tag | any |
    ...
    ...    Example:
    ...    | E7_create_match_list | E7 | matchlist | 100 |
	...    | E7_create_match_list | E7 | matchlist | 100 | 3 |
    # create match-list
    ${result}    cli    ${device}    create svc-match-list ${name}
    Run Keyword And Ignore Error     should contain    ${result}    success
    # add tag rule to match-list
    ${result}    cli    ${device}    add tagged-rule to-svc-match-list ${name} vlan ${vlan} p-bit ${pbit}
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    show svc-match-list ${name}
    should not contain    ${result}    not found
    should contain    ${result}    VLAN ${vlan}
    [Return]    ${result}

E7_delete_match_list
    [Arguments]    ${device}    ${name}    ${rule_index}=1
    [Documentation]    [Author:cgao] Description: delete svc-match-list and remove rule
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | name | Name of service match-list |  |
	...    | rule_index | Index of rule in service match-list <1-12> | 1 |
    ...
    ...    Example:
    ...    | E7_delete_match_list | E7 | matchlist |
	...    | E7_delete_match_list | E7 | matchlist | 2 |
    # remove tag-rule from match-list
    ${result}    cli    ${device}    remove tagged-rule ${rule_index} from-svc-match-list ${name}
    # delete match-list
    ${result}    cli    ${device}    delete svc-match-list ${name}

    ${result}    cli    ${device}    show svc-match-list ${name}
    should contain    ${result}    not found
    [Return]    ${result}


E7_create_bw_prf
    [Arguments]    ${device}    ${name}    ${uspir}=none    ${uscir}=none    ${dspir}=none
    [Documentation]    [Author:cgao] Description: create bw-profile
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
    ...    | name | Name of bandwidth profile | |
	...    | uspir | upstream-pir | none |
	...    | uscir | upstream-cir | none |
    ...    | dspir | downstream-pir | none |
    ...
    ...    Example:
    ...    | E7_create_bw_prf | E7 | test_bw_prf | 10m |
	...    | E7_create_bw_prf | E7 | test_bw_prf | 100m | 10m | 200m |
    # create bandwidth profile
    ${result}    cli    ${device}    create bw-profile ${name} upstream-cir ${uscir} upstream-pir ${uspir} downstream-pir ${dspir}
    Run Keyword And Ignore Error     should contain    ${result}    success
    ${result}    cli    ${device}    show bw-profile ${name}
    should not contain    ${result}    not found
    [Return]    ${result}

E7_create_svc_tag_action
    [Arguments]    ${device}    ${name}    ${tag_action_type}    ${match_list_name}    ${vlan}
    [Documentation]    [Author:cgao] Description: create svc-tag-action
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | name | Name of service tag-action |
	...    | tag_action_type | type of service tag-action to create |
    ...    | match_list_name | Name of service match-list |
	...    | vlan | VLAN name or ID for existing outer tag |
    ...
    ...    Example:
    ...    | E7_create_svc_tag_action | E7 | test_tag_action | change-tag | matchlist | 100 |
    # create svc-tag-action
    ${result}    cli    ${device}    create svc-tag-action ${name} type ${tag_action_type} outer ${vlan} svc-match-list ${match_list_name}
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    show svc-tag-action ${name}
    should not contain    ${result}    not found
    [Return]    ${result}

E7_delete_profile
    [Arguments]    ${device}    ${prf_type}    ${prf_name}
    [Documentation]    [Author:cgao] Description: delete different profile by type and name
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | prf_type | Type of profile to delete, <bw-profile/svc-tag-action> |
	...    | prf_name | Name of profile to delete |
    ...
    ...    Example:
    ...    | E7_delete_profile | E7 | bw-profile| test_bw_prf |
	...    | E7_delete_profile | E7 | svc-tag-action | test_tag_action |
    # delete profile by type and name, ${prf_type} should be bw-profile or svc-tag-action
    ${result}    cli    ${device}    delete ${prf_type} ${prf_name}

    ${result}    cli    ${device}    show ${prf_type} ${prf_name}
    should contain    ${result}    not found
    [Return]    ${result}

E7_set_wanprotocol_pppoe
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${pppoe_username}=${g_ont_pppoe_username}   ${pppoe_password}=${g_ont_pppoe_password}
    [Documentation]    [Author:blwang] Description: set wan protocol of ont port to pppoe
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
	...    | pppoe_username | pppoe username |
	...    | pppoe_password | pppoe password |
    ...
    ...    Example:
    ...    | E7_set_wanprotocol_pppoe | 100 | g1 | qacafe | cdrouter |

    # delete profile by type and name, ${prf_type} should be bw-profile or svc-tag-action
    ${result}    cli    ${device}    set ont-port ${ont_id}/${ont_port} wan-protocol pppoe pppoe-username ${pppoe_username} pppoe-password ${pppoe_password}
    Run Keyword And Ignore Error    should contain    ${result}    success
    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} detail
    should contain    ${result}    pppoe
    [Return]    ${result}

E7_set_wanprotocol_dhcp
    [Arguments]    ${device}    ${ont_id}    ${ont_port}
    [Documentation]    [Author:blwang] Description: set wan protocol of ont port to pppoe
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
    ...
    ...    Example:
    ...    | E7_set_wanprotocol_dhcp | 100 | g1 |

    # delete profile by type and name, ${prf_type} should be bw-profile or svc-tag-action
    ${result}    cli    ${device}    set ont-port ${ont_id}/${ont_port} wan-protocol dhcp
    Run Keyword And Ignore Error    should contain    ${result}    success
    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} detail
    should contain    ${result}    dhcp
    [Return]    ${result}

E7_add_ont_svc
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
    [Documentation]    [Author:cgao] Description: add eth-svc to ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
    ...    | ont_svc | Name of Ethernet service |
	...    | bw_prf | Name of bandwidth profile |
    ...    | svc_tag_action | Name of service tag-action |
    ...
    ...    Example:
    ...    | E7_add_ont_svc | E7 | 100 | g1 | Data1 | test_bw_prf | test_tag_action |
    # bound service to ont port
    ${result}    cli    ${device}    add eth-svc ${ont_svc} to-ont-port ${ont_id}/${ont_port} bw-profile ${bw_prf} svc-tag-action ${svc_tag_action}
    Run Keyword And Ignore Error     should contain    ${result}    success

    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} eth-svc ${ont_svc}
    Should Match Regexp    ${result}    ${ont_svc}+[\\s\\S]*${ont_id}/${ont_port}+[\\s\\S]*${bw_prf}+[\\s\\S]*${svc_tag_action}
    [Return]    ${result}

E7_remove_ont_svc
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}
    [Documentation]    [Author:cgao] Description: remove eth-svc from ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
    ...    | ont_svc | Name of Ethernet service |
    ...
    ...    Example:
    ...    | E7_remove_ont_svc | E7 | 100 | g1 | Data1 |
    # bound service to ont port
    ${result}    cli    ${device}    remove eth-svc ${ont_svc} from-ont-port ${ont_id}/${ont_port}

    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} eth-svc ${ont_svc}
    Should contain    ${result}    not found
    [Return]    ${result}

E7_check_ont_svc
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
    [Documentation]    [Author:cgao] Description: check eth-svc of ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | ont_id | ont id |
	...    | ont_port | ont port name |
    ...    | ont_svc | Name of Ethernet service |
	...    | bw_prf | Name of bandwidth profile |
    ...    | svc_tag_action | Name of service tag-action |
    ...
    ...    Example:
    ...    | E7_check_ont_svc | E7 | 100 | g1 | Data1 | test_bw_prf | test_tag_action |
    ${result}    cli    ${device}    show ont-port ${ont_id}/${ont_port} eth-svc ${ont_svc}
    Should Match Regexp    ${result}    ${ont_svc}+[\\s\\S]*${ont_id}/${ont_port}+[\\s\\S]*${bw_prf}+[\\s\\S]*${svc_tag_action}
    [Return]    ${result}


E7_basic_provision
    [Arguments]    ${device}    ${svc_vlan}    ${match_vlan}    ${ont_id}=${g_ont_id}    ${ont_port}=${g_ont_port}    ${ont_svc}=${g_ont_svc}    ${e7_us_port}=${g_e7_us_port}    ${tag_action_type}=change-tag    ${uspir}=50m    ${uscir}=0    ${dspir}=100m    ${cfg_prefix}=${cfg_prefix}
    [Documentation]    [Author:cgao] Description: E7 basic provision as create ont, create vlan, add upstream port to vlan, create bw-profile, create svc-match-list, create svc-tag-action and bound them to ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
    ...    | svc_vlan | VLAN ID for svc-tag-action | |
    ...    | match_vlan | VLAN ID for svc-match list | |
    ...    | ont_id | ont id | ${ont_id} setting in global parameter file |
    ...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
    ...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
    ...    | uspir | upstream-pir |  ${uspir} setting in file |
    ...    | uscir | upstream-cir |  ${uscir} setting in file |
    ...    | dspir | downstream-pir | ${dspir} setting in file |
    ...    | cfg_prefix | a string as configuration prefix | ${cfg_prefix} setting in file |
    ...
    ...    Example:
    ...    | E7_basic_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
    ...    | E7_basic_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | 100m | 10m | 500m | automation |
    # create ont
    E7_create_ont    ${device}    ${ont_id}

    # create vlan
    E7_create_vlan    ${device}    ${svc_vlan}

    # enable port and add vlan to upstream port
    E7_prov_port    ${device}    ${e7_us_port}    ${svc_vlan}    trunk

    # create bandwidth profile
    ${bw_prf}    set variable    ${cfg_prefix}_bw_v${svc_vlan}
    E7_create_bw_prf    ${device}    ${bw_prf}    ${uspir}    ${uscir}    ${dspir}

    # create match-list
    ${match_list}    Set Variable If
    ...    ${match_vlan}==0    all-untagged
    ...    ${match_vlan}>0     ${cfg_prefix}_MatchList_v${match_vlan}
    Run Keyword If    ${match_vlan}>0    E7_create_match_list    ${device}    ${match_list}    ${match_vlan}

#    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${match_vlan}
#    E7_create_match_list    ${device}    ${match_list}    ${match_vlan}

    # create svc-tag-action
    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${svc_vlan}
    E7_create_svc_tag_action    ${device}    ${svc_tag_action}    ${tag_action_type}    ${match_list}    ${svc_vlan}
    cli    ${device}    hello2
    # bound service to ont port
    E7_add_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
#    E7_check_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}

#    E7_check_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}


E7_basic_deprovision
    [Arguments]    ${device}    ${svc_vlan}    ${match_vlan}    ${ont_id}=${g_ont_id}    ${ont_port}=${g_ont_port}    ${ont_svc}=${g_ont_svc}    ${e7_us_port}=${g_e7_us_port}    ${cfg_prefix}=${cfg_prefix}
    [Documentation]    [Author:cgao] Description: E7 basic de-provision as delete ont, delete svc-tag-action, delete svc-match-list, delete bw-profile, remove port from vlan, and delete vlan
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
    ...    | svc_vlan | VLAN ID for svc-tag-action | |
    ...    | match_vlan | VLAN ID for svc-match list | |
    ...    | ont_id | ont id | ${ont_id} setting in global parameter file |
    ...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
    ...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
    ...    | cfg_prefix | a string as configuration prefix, must be the same as used in E7_basic_provision | ${cfg_prefix} setting in file |
    ...
    ...    Example:
    ...    | E7_basic_deprovision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
    ...    | E7_basic_deprovision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | automation |
    # remove service from ont port
    E7_remove_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}

    # delete ont
    E7_delete_ont    ${device}    ${ont_id}

    # delete profile
    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${svc_vlan}
    E7_delete_profile    ${device}    svc-tag-action    ${svc_tag_action}

    # delete match-list
    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${match_vlan}
    Run Keyword If    ${match_vlan}>0    E7_delete_match_list    ${device}    ${match_list}

    # delete bandwidth profile
    ${bw_prf}    set variable    ${cfg_prefix}_bw_v${svc_vlan}
    E7_delete_profile    ${device}    bw-profile    ${bw_prf}

    # recover port and add vlan to upstream port
    E7_deprov_port    ${device}    ${e7_us_port}    ${svc_vlan}

    # delete vlan
    E7_delete_vlan    ${device}    ${svc_vlan}
    [Return]

E7_videoservice_provision
    [Arguments]    ${device}       ${svc_vlan}    ${match_vlan}    ${ont_id}=${g_ont_id}    ${ont_port}=${g_ont_port}    ${ont_svc}=${g_ont_svc}    ${e7_us_port}=${g_e7_us_port}    ${tag_action_type}=change-tag    ${uspir}=50m    ${uscir}=0    ${dspir}=100m    ${cfg_prefix}=${cfg_prefix}    ${mcast_group_start}=224.0.0.0  ${mcast_group_end}=239.255.255.255     ${mcast_max_strms}=32
    [Documentation]    [Author:blwang] Description: E7 basic provision as create ont, create vlan, add upstream port to vlan, create bw-profile, create svc-match-list, create svc-tag-action and bound them to ont-port
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
    ...    | svc_vlan | VLAN ID for svc-tag-action | |
    ...    | match_vlan | VLAN ID for svc-match list | |
    ...    | ont_id | ont id | ${ont_id} setting in global parameter file |
    ...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
    ...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
    ...    | uspir | upstream-pir |  ${uspir} setting in file |
    ...    | uscir | upstream-cir |  ${uscir} setting in file |
    ...    | dspir | downstream-pir | ${dspir} setting in file |
    ...    | cfg_prefix | a string as configuration prefix | ${cfg_prefix} setting in file |
    ...
    ...    Example:
    ...    | E7_videoservice_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
    ...    | E7_videoservice_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | 100m | 10m | 500m | automation |
    # create ont
    E7_create_ont    ${device}    ${ont_id}

   # create vlan
    E7_create_vlan    ${device}    ${svc_vlan}

    #add  vlan to the uplink port
    E7_prov_port     ${device}  ${e7_us_port}  ${svc_vlan}    trunk

    #create mcast-map
    ${mcast_map}    set variable    mcast-map
    E7_create_mcast_map  ${device}  ${mcast_map}  ${mcast_group_start}  ${mcast_group_end}

    #create mcast-profile
    ${mcast_profile}    set variable    mcast-profile
    E7_create_mcast_profile  ${device}   ${mcast_profile}   ${mcast_max_strms}  ${mcast_map}

    #create bandwidth profile
    ${bw_prf}    set variable    ${cfg_prefix}_bw_v${svc_vlan}
    E7_create_bw_prf    ${device}    ${bw_prf}    ${uspir}    ${uscir}    ${dspir}

    # create match-list
    ${match_list}    Set Variable If
    ...    ${match_vlan}==0    all-untagged
    ...    ${match_vlan}>0     ${cfg_prefix}_MatchList_v${match_vlan}
    Run Keyword If    ${match_vlan}>0    E7_create_match_list    ${device}    ${match_list}    ${match_vlan}

    # create svc-tag-action
    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${svc_vlan}
    E7_create_svc_tag_action    ${device}    ${svc_tag_action}    ${tag_action_type}    ${match_list}    ${svc_vlan}

    # bound service to ont port
    E7_add_ont_video_svc     ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${mcast_profile}    ${svc_tag_action}

E7_videoservice_deprovision
    [Arguments]    ${device}    ${svc_vlan}    ${match_vlan}    ${ont_id}=${g_ont_id}    ${ont_port}=${g_ont_port}    ${ont_svc}=${g_ont_svc}    ${e7_us_port}=${g_e7_us_port}    ${cfg_prefix}=${cfg_prefix}
    [Documentation]    [Author:blwang] Description: E7 basic de-provision as delete ont, delete svc-tag-action, delete svc-match-list, delete bw-profile, remove port from vlan, and delete vlan
 	# remove video service from ont port
    E7_remove_ont_video_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}

	# delete ont
    E7_delete_ont    ${device}    ${ont_id}

	# delete mcast profilemc
	${mcast_profile}    set variable    mcast-profile
	E7_delete_mcast_profile   ${device}    ${mcast_profile}

	# delete mcast map
	${mcast_map}    set variable    mcast-map
    E7_delete_mcast_map  ${device}    ${mcast_map}    1

	# delete svc-tag-action profile
    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${svc_vlan}
    E7_delete_profile    ${device}    svc-tag-action    ${svc_tag_action}

	# delete match-list
    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${match_vlan}
    Run Keyword If    ${match_vlan}>0    E7_delete_match_list    ${device}    ${match_list}

    # delete bandwidth profile
    ${bw_prf}    set variable    ${cfg_prefix}_bw_v${svc_vlan}
    E7_delete_profile    ${device}    bw-profile    ${bw_prf}

    # recover port and add vlan to upstream port
    E7_deprov_port    ${device}    ${e7_us_port}    ${svc_vlan}

    # delete vlan
    E7_delete_vlan    ${device}    ${svc_vlan}
    [Return]


#E7_basic_provision
#    [Arguments]    ${device}    ${match_vlan}    ${svc_vlan}     ${ont_id}=${ont_id}    ${ont_port}=${ont_port}    ${ont_svc}=${ont_svc}    ${e7_us_port}=${e7_us_port}    ${uspir}=${uspir}    ${uscir}=${uscir}    ${dspir}=${dspir}    ${cfg_prefix}=${cfg_prefix}
#    [Documentation]    [Author:cgao] Description: E7 basic provision as create ont, create vlan, add upstream port to vlan, create bw-profile, create svc-match-list, create svc-tag-action and bound them to ont-port
#    ...
#    ...    Arguments:
#    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
#    ...    | device | device name setting in your yaml |  |
#    ...    | vlan_id | VLAN ID | |
#    ...    | ont_id | ont id | ${ont_id} setting in global parameter file |
#    ...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
#    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
#    ...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
#    ...    | uspir | upstream-pir |  ${uspir} setting in file |
#    ...    | uscir | upstream-cir |  ${uscir} setting in file |
#    ...    | dspir | downstream-pir | ${dspir} setting in file |
#    ...    | cfg_prefix | a string as configuration prefix | ${cfg_prefix} setting in file |
#    ...
#    ...    Example:
#    ...    | E7_basic_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
#    ...    | E7_basic_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | 100m | 10m | 500m | automation |
#    # create ont
#    #E7_create_ont    ${device}    ${ont_id}    ${ont_type}    ${ont_sn}
#
#    # create vlan
#    E7_create_vlan    ${device}    ${svc_vlan}
#
#    # enable port and add vlan to upstream port
#    E7_prov_port    ${device}    ${e7_us_port}    ${svc_vlan}    trunk
#
#    # create bandwidth profile
#    ${bw_prf}    set variable    ${cfg_prefix}_bw_v${svc_vlan}
#    E7_create_bw_prf    ${device}    ${bw_prf}    ${uspir}    ${uscir}    ${dspir}
#
#    # create match-list
#    ${match_list}    Set Variable If
#    ...    ${match_vlan}==0    all-untagged
#    ...    ${match_vlan}>0     ${cfg_prefix}_MatchList_v${match_vlan}
#    Run Keyword If    ${match_vlan}>0    E7_create_match_list    ${device}    ${match_list}    ${match_vlan}
#
##    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${match_vlan}
##    E7_create_match_list    ${device}    ${match_list}    ${match_vlan}
#
#    # create svc-tag-action
#    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${svc_vlan}
#    E7_create_svc_tag_action    ${device}    ${svc_tag_action}    ${tag_action_type}    ${match_list}    ${svc_vlan}
#
#    # bound service to ont port
#    E7_add_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
##    E7_check_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
#
#    [Return]
#
#
#E7_basic_deprovision
#    [Arguments]    ${device}    ${match_vlan}    ${svc_vlan}    ${ont_id}=${ont_id}    ${ont_port}=${ont_port}    ${ont_svc}=${ont_svc}    ${e7_us_port}=${e7_us_port}    ${cfg_prefix}=${cfg_prefix}
#    [Documentation]    [Author:cgao] Description: E7 basic de-provision as delete ont, delete svc-tag-action, delete svc-match-list, delete bw-profile, remove port from vlan, and delete vlan
#    ...
#    ...    Arguments:
#    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
#    ...    | device | device name setting in your yaml |  |
#    ...    | vlan_id | VLAN ID | |
#    ...    | ont_id | ont id | ${ont_id} setting in global parameter file |
#    ...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
#    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
#    ...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
#    ...    | cfg_prefix | a string as configuration prefix, must be the same as used in E7_basic_provision | ${cfg_prefix} setting in file |
#    ...
#    ...    Example:
#    ...    | E7_basic_deprovision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
#    ...    | E7_basic_deprovision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | automation |
#    # remove service from ont port
#    E7_remove_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}
#
#    # delete ont
#    #E7_delete_ont    ${device}    ${ont_id}
#
#    # delete profile
#    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${svc_vlan}
#    E7_delete_profile    ${device}    svc-tag-action    ${svc_tag_action}
#
#    # delete match-list
#    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${match_vlan}
#    Run Keyword If    ${match_vlan}>0    E7_delete_match_list    ${device}    ${match_list}
#
#    # delete bandwidth profile
#    ${bw_prf}    set variable    ${cfg_prefix}_bw_v${svc_vlan}
#    E7_delete_profile    ${device}    bw-profile    ${bw_prf}
#
#    # recover port and add vlan to upstream port
#    E7_deprov_port    ${device}    ${e7_us_port}    ${svc_vlan}
#
#    # delete vlan
#    E7_delete_vlan    ${device}    ${svc_vlan}
#    [Return]

E7_remove_ont_port_from_res
    [Arguments]    ${device}    ${ont_id}    ${ont_port}
    ${result}    cli    ${device}    remove ont-port ${ont_id}/${ont_port} from-res-gw
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}

E7_create_eth_sec_profile
    [Arguments]    ${device}    ${name}    ${src_mac_vlaue}    ${mac_age}
    ${result}    cli    ${device}    creat eth-sec-profile ${name} src-mac-limit ${src_mac_vlaue} src-mac-age ${mac_age}
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}

E7_set_eth_sec_profile
    [Arguments]    ${device}    ${name}    ${ont_id}    ${ont_port}    ${src_mac_value}    ${mac_age}
    ${result}    cli    ${device}    creat eth-sec-profile ${name} src-mac-limit ${src_mac_value} src-mac-age ${mac_age}
    log to console    ${result}
    should contain    ${result}    success
    ${result}    cli    ${device}    set ont-port ${ont_id}/${ont_port} eth-sec-profile ${name}
    should contain    ${result}    success
    [Return]    ${result}

E7_delete_eth_sec_profile
    [Arguments]    ${device}    ${name}
    ${result}    cli    ${device}    delete eth-sec-profile ${name}
    log to console    ${result}
    should contain    ${result}    success
    [Return]    ${result}

E7_check_mac_lmt
    [Arguments]    ${device}    ${ont_id}    ${ont_port}    ${src_mac_value}
    ${result}    cli    ${device}    show mac on-ont-port ${ont_id}/${ont_port}
    log to console    ${result}
    should contain    ${result}    ${src_mac_value} MAC addresses found
    [Return]    ${result}


E7_check_ont_status
    [Arguments]    ${device}    ${ont_id}
    ${result}=    Wait Until Keyword Succeeds    5x    5s    cli    ${device}    show ont ${ont_id} detail     Operational status.*enabled
    log to console    ${result}
    [Return]    ${result}

#E7_basic_provision
#    [Arguments]    ${device}    ${vlan_id}    ${ont_id}=${ont_id}    ${ont_port}=${ont_port}    ${ont_svc}=${ont_svc}    ${e7_us_port}=${e7_us_port}    ${uspir}=${uspir}    ${uscir}=${uscir}    ${dspir}=${dspir}    ${cfg_prefix}=${cfg_prefix}
#    [Documentation]    Description: E7 basic provision as create ont, create vlan, add upstream port to vlan, create bw-profile, create svc-match-list, create svc-tag-action and bound them to ont-port
#    ...
#    ...    Arguments:
#    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
#    ...    | device | device name setting in your yaml |  |
#    ...    | vlan_id | VLAN ID | |
#	...    | ont_id | ont id | ${ont_id} setting in global parameter file |
#	...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
#    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
#	...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
#    ...    | uspir | upstream-pir |  ${uspir} setting in file |
#	...    | uscir | upstream-cir |  ${uscir} setting in file |
#    ...    | dspir | downstream-pir | ${dspir} setting in file |
#	...    | cfg_prefix | a string as configuration prefix | ${cfg_prefix} setting in file |
#    ...
#    ...    Example:
#    ...    | E7_basic_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
#	...    | E7_basic_provision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | 100m | 10m | 500m | automation |
#    # create ont
#    #E7_create_ont    ${device}    ${ont_id}    ${ont_type}    ${ont_sn}
#
#    # create vlan
#    E7_create_vlan    ${device}    ${vlan_id}
#
#    # enable port and add vlan to upstream port
#    E7_prov_port    ${device}    ${e7_us_port}    ${vlan_id}    trunk
#
#    # create bandwidth profile
#    ${bw_prf}    set variable    ${cfg_prefix}_bw
#    E7_create_bw_prf    ${device}    ${bw_prf}    ${uspir}    ${uscir}    ${dspir}
#
#    # create match-list
#    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${vlan_id}
#    E7_create_match_list    ${device}    ${match_list}    ${vlan_id}
#
#    # create svc-tag-action
#    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${vlan_id}
#    E7_create_svc_tag_action    ${device}    ${svc_tag_action}    ${tag_action_type}    ${match_list}    ${vlan_id}
#
#    # bound service to ont port
#    E7_add_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
#    E7_check_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}    ${bw_prf}    ${svc_tag_action}
#
#    [Return]
#
#
#E7_basic_deprovision
#    [Arguments]    ${device}    ${vlan_id}    ${ont_id}=${ont_id}    ${ont_port}=${ont_port}    ${ont_svc}=${ont_svc}    ${e7_us_port}=${e7_us_port}    ${cfg_prefix}=${cfg_prefix}
#    [Documentation]    Description: E7 basic de-provision as delete ont, delete svc-tag-action, delete svc-match-list, delete bw-profile, remove port from vlan, and delete vlan
#    ...
#    ...    Arguments:
#    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
#    ...    | device | device name setting in your yaml |  |
#    ...    | vlan_id | VLAN ID | |
#	...    | ont_id | ont id | ${ont_id} setting in global parameter file |
#	...    | ont_port | ont port name | ${ont_port} setting in global parameter file |
#    ...    | ont_svc | Name of Ethernet service | ${ont_svc} setting in global parameter file |
#	...    | e7_us_port | upstream port on e7 | ${e7_us_port} setting in global parameter file |
#    ...    | cfg_prefix | a string as configuration prefix, must be the same as used in E7_basic_provision | ${cfg_prefix} setting in file |
#    ...
#    ...    Example:
#    ...    | E7_basic_deprovision | E7 | 85 | 100 | g1 | Data1 | 2/g1 |
#	...    | E7_basic_deprovision | E7 | 85 | 100 | g1 | Data1 | 2/g1 | automation |
#    # remove service from ont port
#    E7_remove_ont_svc    ${device}    ${ont_id}    ${ont_port}    ${ont_svc}
#
#    # delete ont
#    #E7_delete_ont    ${device}    ${ont_id}
#
#    # delete profile
#    ${svc_tag_action}    set variable    ${cfg_prefix}_TagAction_v${vlan_id}
#    E7_delete_profile    ${device}    svc-tag-action    ${svc_tag_action}
#
#    # delete match-list
#    ${match_list}    set variable    ${cfg_prefix}_MatchList_v${vlan_id}
#    E7_delete_match_list    ${device}    ${match_list}
#
#    # delete bandwidth profile
#    ${bw_prf}    set variable    ${cfg_prefix}_bw
#    E7_delete_profile    ${device}    bw-profile    ${bw_prf}
#
#    # recover port and add vlan to upstream port
#    E7_deprov_port    ${device}    ${e7_us_port}    ${vlan_id}
#
#    # delete vlan
#    E7_delete_vlan    ${device}    ${vlan_id}
#    [Return]
