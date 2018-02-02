*** Settings ***
Documentation     800 serials cli keywords
Resource          caferobot/cafebase.robot

*** Keywords ***
set ip for device
    [Arguments]    ${local_connection}    ${password}    ${device}    ${ip}
    [Documentation]    set ip address for local device
    cli    ${local_connection}    sudo -k ifconfig ${device} down
    cli    ${local_connection}    ${password}
    cli    ${local_connection}    sudo -k ifconfig ${device} up
    cli    ${local_connection}    ${password}
    cli    ${local_connection}    sudo -k ifconfig ${device} ${ip}
    cli    ${local_connection}    ${password}
    ${info}    cli    ${local_connection}    ifconfig ${device}
    should contain    ${info}    ${ip}

restore default for device
    [Arguments]    ${connection}
    [Documentation]    restore default for the device, it can only use with broadcom shell.
    cli    ${connection}    restoredefault    retry=0    timeout_exception=0

reset device to normal status
    set ip for device    local_ssh    cafetest    ${nc_844E}    192.168.2.100
    set ip for device    local_ssh    cafetest    ${nc_844GE}    192.168.1.100
    restore default for device    ${ONT_E_TRUNK}
    restore default for device    ${ONT_G_TRUNK}
    sleep    180
    wait_trunk_able_to_execute_command    ${ONT_E_TRUNK}
    wait_trunk_able_to_execute_command    ${ONT_G_TRUNK}
    teardown
