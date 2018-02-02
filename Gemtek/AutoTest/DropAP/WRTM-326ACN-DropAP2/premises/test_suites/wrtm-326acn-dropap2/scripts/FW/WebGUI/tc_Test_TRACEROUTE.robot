*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI

*** Variables ***

*** Test Cases ***
tc_Test_TRACEROUTE
    [Documentation]  tc_Test_TRACEROUTE
    ...    1. Go to web page Networking>Diagnositcs
    ...    2. tranceroute DropAP GUI IP: 192.168.66.1
    ...    3. Verify DropAP Gui Can Trigger TRACEROUTE command, page should contains text: traceroute to 192.168.66.1
    [Tags]   @TCID=WRTM-326ACN-322    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to web page Networking>Diagnositcs
    tranceroute DropAP GUI IP: 192.168.66.1
    Verify DropAP Gui Can Trigger TRACEROUTE command, page should contains text: traceroute to 192.168.66.1

*** Keywords ***
Go to web page Networking>Diagnositcs
    [Documentation]  Go to web page Networking>Diagnositcs
    [Tags]   @AUTHOR=Jujung_Chang
    Go to Diagnostics

tranceroute DropAP GUI IP: 192.168.66.1
    [Documentation]  ping DropAP GUI IP: 192.168.66.1
    [Tags]   @AUTHOR=Jujung_Chang
    Traceroute Using DropAP GUI    ${gui_url}
    #wait for ping is successfully
    sleep   3s

Verify DropAP Gui Can Trigger TRACEROUTE command, page should contains text: traceroute to 192.168.66.1
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Should Be Contain Text At Diagnostics Page    ${gui_url}

*** comment ***
2017-10-31     Jujung_Chang
Init the script
