*** Settings ***
Resource    base.robot

*** Variables ***
${main_screen_device_name}    com.dropap.dropap:id/deviceNameTxt
${router_Offline_icon}    com.dropap.dropap:id/routerOfflineImg

*** Keywords ***
verify main screen device name
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${main_screen_device_name}

wait main screen
    Wait Until Page Contains Element    ${main_screen_device_name}    timeout=50

show router Offline icon
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${router_Offline_icon}    timeout=30

verify the device status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Does Not Contain Element    ${router_Offline_icon}    timeout=110

*** comment ***
2017-12-11 Gavin_Chang
1. Add check keyowrd about reboot.

2017-11-10     Leo_Li
Init the script
