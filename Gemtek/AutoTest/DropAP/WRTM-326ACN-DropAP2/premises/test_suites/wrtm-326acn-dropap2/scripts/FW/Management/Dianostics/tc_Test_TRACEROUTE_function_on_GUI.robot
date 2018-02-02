*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Dianostics    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_Test_TRACEROUTE_function_on_GUI
    [Documentation]  tc_Test_TRACEROUTE_function_on_GUI
    ...    1. Setup a Networking. LAN host can access to WAN host
    ...    2. Go to web page Networking>Diagnositcs
    ...    3. TRACEROUTE a host Ip to see information at GUI if it will response
    [Tags]   @TCID=WRTM-326ACN-272    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Setup a Networking. LAN host can access to WAN host
    Go to web page Networking>Diagnositcs
    TRACEROUTE a host Ip to see information at GUI if it will response

*** Keywords ***
Setup a Networking. LAN host can access to WAN host
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Config DHCP Client
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

Go to web page Networking>Diagnositcs
    [Documentation]  Config DHCP Client
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    1s    click links    web    Diagnostics

TRACEROUTE a host Ip to see information at GUI if it will response
    [Documentation]  Verify DHCP Wan Type
    [Tags]   @AUTHOR=Hans_Sun
    Traceroute Using DropAP GUI    ${DEVICES.wanhost.traffic_ip}
    Should Be Contain Text At Diagnostics Page    ${DEVICES.cisco.gateway}
    Should Be Contain Text At Diagnostics Page    ${DEVICES.wanhost.traffic_ip}

*** comment ***
2017-12-4     Hans_Sun
Init the script
