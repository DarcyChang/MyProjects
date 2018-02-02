*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***
${message}    Address 1: 192.168.66.1

*** Test Cases ***
tc_NSLOOKUP
    [Documentation]  tc_NSLOOKUP
    ...    1. Go to web page Networking>Diagnositcs
    ...    2. Input NSLOOKUP Domain name: DropAP.lan
    ...    3. Verify DropAP Gui Can Trigger NSLOOKUP command, page should contains text: Address 1: 192.168.66.1
    [Tags]   @TCID=WRTM-326ACN-326    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Networking>Diagnositcs
    Input NSLOOKUP Domain name: DropAP.lan
    Verify DropAP Gui Can Trigger NSLOOKUP command, page should contains text: Address 1: 192.168.66.1

*** Keywords ***
Go to web page Networking>Diagnositcs
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking  Diagnostics

Input NSLOOKUP Domain name: DropAP.lan
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Input Text    web    ${Input_NSLOOKUP}    DropAP.lan
    cpe click    web    ${Button_NSLOOKUP}

Verify DropAP Gui Can Trigger NSLOOKUP command, page should contains text: Address 1: 192.168.66.1
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result}    Get Element text    web    ${Text_NSLOOKUP}
    should contain    ${result}    ${message}

*** comment ***
2017-10-30     Hans_Sun
Init the script
