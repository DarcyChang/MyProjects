*** Settings ***

*** Keywords ***
TR69_ccplux_cc_cpe
    [Arguments]    ${801f_sn}   ${linux_shell}
    [Documentation]    [Author:xlai] Description: check if cpe managed by ccplus
    ${result}    cli    ${linux_shell}    curl -X GET "${g_cc_acs_server}/cc/device?orgId=${g_org_id}&serialNumber=${801f_sn}"    \\}    10
    should match regexp    ${result}    id.+${801f_sn}

TR69_ccplus_connected
    [Arguments]    ${801f_sn}    ${linux_shell}
    [Documentation]    [Author:xlai] Description: check if cpe can connected to ccplus after configuration
    ${result2}=    Wait Until Keyword Succeeds    20x    10s    TR69_ccplux_cc_cpe    ${801f_sn}   ${linux_shell}

TR69_ccplus_delete_cpe
    [Arguments]    ${801f_sn}    ${linux_shell}
    [Documentation]    [Author:xlai] Description: delete cpe from ccplus
    ${result}    cli    ${linux_shell}    curl -X DELETE "${g_cc_acs_server}/cc/device?orgId=${g_org_id}&serialNumber=${801f_sn}"

cc_backend_ip
    [Arguments]    ${cc_acs_server}
    [Documentation]    [Author:xlai] Description: retreive backend ip
    ${phy_speed}=   Get Regexp Matches    ${cc_acs_server}     (\\d+\.\\d+\.\\d+\.\\d+)    1
    ${len} =    Get Length    ${phy_speed}
    ${phy_speed} =    Run Keyword If  ${len}    Get From List    ${phy_speed}    0
     [Return]    ${phy_speed}


TR69_ccplus_dwl_image_restful
    [Arguments]    ${801f_image}    ${801f_sn}
    remove ccplus conf    ${801f_image}    ${801f_sn}
    ${cc_ip}    cc_backend_ip    ${g_cc_acs_server}
    ${group_name}    create device group by sn    ${g_ccplus_device}    ${801f_sn}    ${801f_sn}
    should not be equal    ${group_name}    ${NONE}
    should be equal    ${group_name}    ${801f_sn}
    ${image_name}    upload sw fw image    ${g_ccplus_device}    ${g_cc_dwl_ont_load_path}/${801f_image}    ${cc_ip}    ${801f_image}
    should not be equal    ${image_name}    ${NONE}
    should be equal    ${image_name}    ${801f_image}
    ${work_flow_name}    create download image work flow on time window    ${g_ccplus_device}    ${group_name}    ${image_name}    5    ${801f_sn}
    should not be equal    ${work_flow_name}    ${NONE}
    should be equal    ${work_flow_name}    ${801f_sn}
    ${state_name}    wait until work flow to state    ${g_ccplus_device}    ${work_flow_name}    Completed    10    5
    remove ccplus conf    ${801f_image}    ${801f_sn}

TR-069 Provision
    [Arguments]   ${801f_device}   ${801f_sn}   ${gfast_port}
    DPU_clean_gfast_port_svc_role    ${dpu_device}    ${gfast_port}
    DPU_configure_gfast_service    ${dpu_device}    ${g_mgmt_vlan}    ${g_801f_mgmt_vlan}    ${gfast_port}    auto    enabled
    #    ${result}    cli    ${801f_device}    ${g_input_enter}
    801F Restart udhcpc.sh    ${801f_device}
    T801F_login    ${801f_device}    root    superuser
    Sleep    5    #wait for serial popped up words
    TR69_acs_configure    ${801f_device}    ${g_acs_url}    ${g_acs_usr}    ${g_acs_pwd}
    TR69_ccplus_connected   ${801f_sn}    ${linux_shell}

TR-069 Deprovision
    [Arguments]   ${801f_device}   ${801f_sn}   ${gfast_port}
    run keyword and ignore error    TR69_ccplus_delete_cpe    ${801f_sn}   ${linux_shell}
    run keyword and ignore error    TR69_acs_configure    ${801f_device}    ${g_801f_default_acs_url}    ${g_801f_default_acs_user}    ${g_801f_default_acs_pwd}
    T801F_logout    ${801f_device}
    run keyword and ignore error    DPU_recover_gfast_service    ${dpu_device}    ${g_mgmt_vlan}    ${g_801f_mgmt_vlan}    ${gfast_port}

remove ccplus conf
    [Arguments]    ${801f_image}    ${801f_sn}
    run keyword and ignore error    Delete All Test Workflow    ${g_ccplus_device}
    run keyword and ignore error    delete device group    ${g_ccplus_device}    ${801f_sn}
    #run keyword and ignore error    delete config file    ${g_ccplus_device}    test_config_name.conf
    run keyword and ignore error    delete sw fw image    ${g_ccplus_device}    ${801f_image}