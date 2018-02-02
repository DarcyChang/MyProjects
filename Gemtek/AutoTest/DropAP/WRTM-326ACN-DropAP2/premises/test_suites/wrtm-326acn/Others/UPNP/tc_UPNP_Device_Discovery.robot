*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=UPNP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***


*** Test Cases ***
tc_UPNP_Device_Discovery
    [Documentation]    lanhost should correctly receive device upnp information
    [Tags]    @tcid=WRTM-326ACN-144    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Enable UPNP and lanhost should discover this device successfully
    Disable UPNP and lanhost should not discover this device

*** Keywords ***

Enable UPNP and lanhost should discover this device successfully
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    5x    2s    Config UPNP Switch    web    on
    Wait Until Keyword Succeeds    5x    5s    Check UPNP Device Should be Discovered By host    lanhost    ${DEVICES.lanhost.interface}
    
Disable UPNP and lanhost should not discover this device
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Config UPNP Switch    web    off
    Check UPNP Device Should Not be Discovered By host    lanhost    ${DEVICES.lanhost.interface}
    
    
Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
    
    Add Routing On Hosts
    Login Web GUI
    
    
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}

    
Add Routing On Hosts
    [Arguments]
    [Documentation]    Configure routing to lanhost and wanhost
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route add default gw ${g_dut_gw}

Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Delete Routing On Hosts
    
Delete Routing On Hosts
    [Arguments]
    [Documentation]    Unconfigure routing to lanhost and wanhost
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del default gw ${g_dut_gw}

    

*** comment ***
2017-09-10     Gemtek_Thomas_Chen
Init the script
