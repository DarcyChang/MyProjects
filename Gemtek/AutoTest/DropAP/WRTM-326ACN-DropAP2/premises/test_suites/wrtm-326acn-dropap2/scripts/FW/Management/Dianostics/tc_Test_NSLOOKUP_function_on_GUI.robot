*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Dianostics    @AUTHOR=Hans_Sun

*** Variables ***
${URL}    www.yahoo.com

*** Test Cases ***
tc_Test_NSLOOKUP_function_on_GUI
    [Documentation]  tc_Test_NSLOOKUP_function_on_GUI
    ...    1. Setup a Networking. LAN host can access to WAN host
    ...    2. Go to web page Networking>Diagnositcs
    ...    3. NSLOOKUP a host Ip or a website URL like "www.yahoo.com" to see information at GUI if it will response
    [Tags]   @TCID=WRTM-326ACN-273    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Setup a Networking. LAN host can access to WAN host
    Go to web page Networking>Diagnositcs
    NSLOOKUP a host Ip or a website URL like "www.yahoo.com" to see information at GUI if it will response

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

NSLOOKUP a host Ip or a website URL like "www.yahoo.com" to see information at GUI if it will response
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    NSLOOKUP Using DropAP GUI    ${URL}
    ${result}    Get Element Text    web    ${Text_NSLOOKUP}
    log    ${result}
    Should Match Regexp    ${result}    yahoo.com

*** comment ***
2017-12-7     Hans_Sun
Init the script
