*** Settings ***
Resource          caferobot/cafebase.robot

*** Variables ***
#${svc_vlan}       90
#${mlist_vlan}     100
${dpu_service_prefix}    auto
${dpu_root_prompt}    root.+~#
${dpu_cli_prompt}    [^~]#
#${dpu_device}     dpu5
#${gfast_port}     gfast9

*** Keywords ***
DPU_cli_login
    [Arguments]    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Login to DPU CLI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_cli_login \ \ \ \ dpu
    ${result}    cli    ${dpu_device}    cli    ${dpu_cli_prompt}
    log to console    ${result}

DPU_cli_logout
    [Arguments]    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Logout from DPU CLI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_cli_logout \ \ \ \ dpu
    ${result}    cli    ${dpu_device}    exit    ${dpu_root_prompt}}
    log to console    ${result}

DPU_add_matchlist
    [Arguments]    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Configure match-list on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | mlist_vlan | vlan id in your match-list |
    ...    | dpu_service_prefix | use prefix & vlan to combine your match-list name,it MUST be the same combination of your service-profile,service-instance. e.g. dpu_service_prefix is test, mlist_vlan is 85, match-list name is test_85 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_add_matchlist \ \ \ \ test 85 dpu
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    match-list ${dpu_service_prefix}_${mlist_vlan}    ${mlist_vlan}\\)#
    log to console    ${result}
    #${result}    cli    ${dpu_device}    match-rule 1 match priority-tagged remove-tag    ${mlist_vlan}\\)#
    #log to console    ${result}
    ${result}    cli    ${dpu_device}    match-rule 1 match vlan ${mlist_vlan} remove-tag    ${mlist_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config match-list ${dpu_service_prefix}_${mlist_vlan}    ${mlist_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_add_svcprofile
    [Arguments]    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Configure service-profile on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | svc_vlan | vlan id in your service-profile |
    ...    | dpu_service_prefix | use prefix & svc_vlan to combine your service-profile name,it MUST be the same combination of your match-list,service-instance, e.g. dpu_service_prefix is test, svc_vlan is 85, service-profile name is test_85 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_add_svcprofile \ \ \ \ test 85 dpu
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    service-profile ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config service-profile ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_add_svcinstance
    [Arguments]    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Configure service-instance on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | svc_vlan | vlan id in your service-profile |
    ...    | dpu_service_prefix | use prefix & svc_vlan to combine your service-instance name,it MUST be the same combination of your match-list,service-profile, e.g. dpu_service_prefix is test, vlan is 85, service-instance name is test_85 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_add_svcinstance \ \ \ \ test 85 dpu
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    service-instance ${dpu_service_prefix}_${svc_vlan} ${svc_vlan} ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config service-instance ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_add_gfastsvc
    [Arguments]    ${svc_vlan}    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}    ${gfast_port}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Configure service-instance to gfast port on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | svc_vlan | vlan id in your service-profile & service-instance |
    ...    | mlist_vlan | vlan id in your match-list |
    ...    | dpu_service_prefix | use prefix & vlan to combine your service-instance name,it MUST be the same combination of your match-list,service-profile,service_instance, e.g. dpu_service_prefix is test, svc_vlan is 85,mlist_vlan is 90, service-instance name is test_85;match-list name is test_90 |
    ...    | dpu_device | the one setting in your yaml |
    ...    | gfast_port | gfast port specified |
    ...
    ...    Example:
    ...    DPU_add_gfastsvc \ \ \ \ test 85 90 dpu gfast8
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    interface ethernet ${gfast_port}    ${gfast_port}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    no service-role    ${gfast_port}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    service-role uni    uni\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    service ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    match-list ${dpu_service_prefix}_${mlist_vlan}    ${mlist_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    no shutdown    ${mlist_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config interface ethernet ${gfast_port}    ${mlist_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_check_gfast_port
    [Arguments]    ${device}    ${gfast_port}    ${oper_state}=up    ${fwd_state}=forwarding    ${admin_state}=enable
    [Documentation]    [Author:cgao] Description: check gfast port state
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | gfast_port | gfast port name |  |
	...    | oper_state | operator state | up |
    ...    | fwd_state | forward state | forwarding |
    ...    | admin_state | admin state | enable |
    ...
    ...    Example:
    ...    | DPU_check_gfast_port | dpu | gfast5 |
	...    | DPU_check_gfast_port | dpu | gfast5 | down | blocking | disable |
    # go to config mode
    DPU_CLI_login    ${device}

    # check gfast interface status on dpu
    ${result}    cli    ${device}    show interface summary status
    Should Match Regexp    ${result}    ${gfast_port}.*${admin_state}.*${oper_state}.*${fwd_state}

    ${result}    cli    ${device}    show interface ethernet ${gfast_port} status
    Should Match Regexp    ${result}    port.*${gfast_port}+[\\s\\S]*admin-state.*${admin_state}+[\\s\\S]*oper-state.*${oper_state}+[\\s\\S]*fwd-state.*${fwd_state}
    DPU_CLI_logout    ${device}
    [Return]    ${result}


DPU_delete_matchlist
    [Arguments]    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Delete match-list on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | mlist_vlan | vlan id in your match-list |
    ...    | dpu_service_prefix | use prefix & mlist_vlan to combine your match-list name,it MUST be the same combination of your service-profile,service-instance, e.g. dpu_service_prefix is test, mlist_vlan is 85, match-list name is test_85 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_delete_matchlist \ \ \ \ test 85 dpu
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    no match-list ${dpu_service_prefix}_${mlist_vlan}    ${mlist_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config match-list | begin ${dpu_service_prefix}_${mlist_vlan}    ${mlist_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_delete_svcprofile
    [Arguments]    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Delete service-profile on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | svc_vlan | vlan id in your service-profile |
    ...    | dpu_service_prefix | use prefix & svc_vlan to combine your service-profile name,it MUST be the same combination of your match-list,service-instance, e.g. dpu_service_prefix is test, svc_vlan is 85, service-profile name is test_85 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_delete_svcprofile \ \ \ \ test 85 dpu
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    no service-profile ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config service-profile | begin ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_delete_svcinstance
    [Arguments]    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Delete service-instance on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | svc_vlan | vlan id in your service-profile |
    ...    | dpu_service_prefix | use prefix & svc_vlan to combine your service-instance name,it MUST be the same combination of your match-list,service-profile, e.g. dpu_service_prefix is test, svc_vlan is 85, service-instance name is test_85 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_delete_svcinstance \ \ \ \ test 85 dpu
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    no service-instance ${dpu_service_prefix}_${svc_vlan} ${svc_vlan} ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config service-instance | begin ${dpu_service_prefix}_${svc_vlan}    ${svc_vlan}\\)#
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_delete_gfastsvc
    [Arguments]    ${svc_vlan}    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}    ${gfast_port}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Delete service-instance from gfast port on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | svc_vlan | vlan id in your service-profile & service-instance |
    ...    | mlist_vlan | vlan id in your match-list |
    ...    | dpu_service_prefix | use prefix & vlan to combine your service-instance name,it MUST be the same combination of your match-list,service-profile,service_instance, e.g. dpu_service_prefix is test, svc_vlan is 85,mlist_vlan is 90, service-instance name is test_85;match-list name is test_90 |
    ...    | dpu_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    DPU_delete_gfastsvc \ \ \ \ test 85 90 dpu gfast8
    #DPU_CLI_login
    ${result}    cli    ${dpu_device}    configure    \\(config\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    interface ethernet ${gfast_port}    ${gfast_port}\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    service-role uni    uni\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    no service ${dpu_service_prefix}_${svc_vlan}    uni\\)#
    log to console    ${result}
    ${result}    cli    ${dpu_device}    end
    log to console    ${result}
    ${result}    cli    ${dpu_device}    show running-config interface ethernet ${gfast_port}    ${dpu_cli_prompt}
    log to console    ${result}
    #DPU_CLI_logout
    [Return]    ${result}

DPU_configure_gfast_service
    [Arguments]    ${dpu_device}    ${svc_vlan}    ${mlist_vlan}    ${gfast_port}    ${dpu_service_prefix}=${dpu_service_prefix}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Provision basic L2 service to gfast port on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | dpu_device | the one setting in your yaml |
    ...    | svc_vlan | vlan id in your service-profile & service-instance |
    ...    | mlist_vlan | vlan id in your match-list |
    ...    | gfast_port | gfast port name |
    ...    | dpu_service_prefix | use prefix & vlan to combine your service-instance name,it MUST be the same combination of your match-list,service-profile,service_instance, e.g. dpu_service_prefix is test, svc_vlan is 85,mlist_vlan is 90, service-instance name is test_85;match-list name is test_90 |
        ...
    ...    Example:
    ...    DPU_configure_gfast_service \ \ \ \ test 85 90 dpu gfast8
    DPU_cli_login    ${dpu_device}
    ${ret}    DPU_add_matchlist    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}
    Should Match Regexp    ${ret}    match-list ${dpu_service_prefix}_${mlist_vlan}
    ${ret}    DPU_add_svcprofile    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    Should Match Regexp    ${ret}    service-profile ${dpu_service_prefix}_${svc_vlan}
    ${ret}    DPU_add_svcinstance    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    Should Match Regexp    ${ret}    service-instance ${dpu_service_prefix}_${svc_vlan}
    ${ret}    DPU_add_gfastsvc    ${svc_vlan}    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}    ${gfast_port}
    Should Match Regexp    ${ret}    service ${dpu_service_prefix}_${svc_vlan}
    Should Match Regexp    ${ret}    match-list ${dpu_service_prefix}_${mlist_vlan}
    DPU_cli_logout    ${dpu_device}

DPU_recover_gfast_service
    [Arguments]    ${dpu_device}    ${svc_vlan}    ${mlist_vlan}    ${gfast_port}    ${dpu_service_prefix}=${dpu_service_prefix}
    [Documentation]
    ...    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Remove basic L2 service configured by calling keywords DPU_configure_gfast_service from gfast port on DPU
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | dpu_device | the one setting in your yaml |
    ...    | svc_vlan | vlan id in your service-profile & service-instance |
    ...    | mlist_vlan | vlan id in your match-list |
    ...    | gfast_port | gfast port name |
    ...    | dpu_service_prefix | use prefix & vlan to combine your service-instance name,it MUST be the same combination of your match-list,service-profile,service_instance, e.g. dpu_service_prefix is test, svc_vlan is 85,mlist_vlan is 90, service-instance name is test_85;match-list name is test_90 |
    ...
    ...    Example:
    ...    DPU_recover_gfast_service \ \ \ \ test 85 90 dpu gfast8
    DPU_cli_login    ${dpu_device}
    ${ret}    DPU_delete_gfastsvc    ${svc_vlan}    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}    ${gfast_port}
    Should Not Match Regexp    ${ret}    service ${dpu_service_prefix}_${svc_vlan}
    ${ret}    DPU_delete_svcinstance    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    Should Not Match Regexp    ${ret}    service-instance ${dpu_service_prefix}_${svc_vlan}
    ${ret}    DPU_delete_matchlist    ${mlist_vlan}    ${dpu_service_prefix}    ${dpu_device}
    Should Not Match Regexp    ${ret}    match-list ${dpu_service_prefix}_${mlist_vlan}
    ${ret}    DPU_delete_svcprofile    ${svc_vlan}    ${dpu_service_prefix}    ${dpu_device}
    Should Not Match Regexp    ${ret}    service-profile ${dpu_service_prefix}_${svc_vlan}
    DPU_cli_logout    ${dpu_device}
