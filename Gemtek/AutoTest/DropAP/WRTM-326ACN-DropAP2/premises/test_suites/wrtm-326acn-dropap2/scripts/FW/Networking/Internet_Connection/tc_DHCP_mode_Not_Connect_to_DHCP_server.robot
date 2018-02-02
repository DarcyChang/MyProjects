*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_DHCP_mode_Not_Connect_to_DHCP_server
    [Documentation]  tc_DHCP_mode_Not_Connect_to_DHCP_server
    ...    1. DUT WAN interface connect to the server that does not have function of DHCP server.
    ...    2. Go to WAN Settings page, and setting DHCP mode.
    ...    3. Verify WAN Port IP information, there is not IP setting on WAN interface.
    [Tags]   @TCID=WRTM-326ACN-349    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [Teardown]    Enable DHCP Server

    DUT WAN interface connect to the server that does not have function of DHCP server
    Go to WAN Settings page, and setting DHCP mode
    Verify WAN Port IP information, there is not IP setting on WAN interface

*** Keywords ***
DUT WAN interface connect to the server that does not have function of DHCP server
    [Documentation]  DUT WAN interface connect to the server that does not have function of DHCP server
    [Tags]   @AUTHOR=Jujung_Chang
    Disable DHCP Server

Go to WAN Settings page, and setting DHCP mode
    [Documentation]  Go to WAN Settings page, and setting DHCP mode
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client

Verify WAN Port IP information, there is not IP setting on WAN interface
    [Documentation]  Verify WAN Port IP information, there is not IP setting on WAN interface
    [Tags]   @AUTHOR=Jujung_Chang

    #workaround for Networking information can not update immidiately
    Config Static Client
    Config DHCP Client
    sleep    5s

    Check Address on the IPv4 WAN Status Table Is Empty    web

Check Address on the IPv4 WAN Status Table Is Empty
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    Reload Page    ${b}
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status  Overview
    sleep    1
    ${value} =   get_element_text    ${b}    ${Table_Wan}
    log    ${value}
    should contain    ${value}    Not connected

*** comment ***
2017-11-27     Jujung_Chang
1. Adding click Status action to prevent Overview is hidden.
2. To extend sleep times from 60s to 70s.To prevent still get IP on GUI after shutdown DHCP server.
2017-11-15     Jujung_Chang
Init the script
