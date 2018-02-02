*** Settings ***
Resource   base.robot

Test Setup   Login Web GUI
Test teardown    Restore Networking Configuration
Force Tags  @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang

*** Variables ***
${blank_username}
${blank_password}
${Over64_username}    abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz1234567890123
${Over64_password}    abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz1234567890123

*** Test Cases ***
tc_Config_PPPoE_with_invalid_idpw
    [Documentation]   tc_Config_PPPoE_with_invalid_idpw
    ...    1. Go to web page Networking>Internet Connection, and select protocol to PPPoE
    ...    2. input invalid ID/pw and save And Verify prompt alert should show and the input string should turn red

    [Tags]   @TCID=WRTM-326ACN-291    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    Go to web page Networking>Internet Connection, and select protocol to PPPoE
    input invalid ID/pw and save And Verify prompt alert should show and the input string should turn red

*** Keywords ***
Go to web page Networking>Internet Connection, and select protocol to PPPoE
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Config PPPoE Client    ${g_dut_pppoe_username}    ${g_dut_pppoe_password}

input invalid ID/pw and save And Verify prompt alert should show and the input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Config PPPoE Client    ${blank_username}    ${blank_password}
    Config PPPoE Client    ${Over64_username}    ${Over64_password}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking
    Config DHCP Client

*** comment ***
2017-11-20     Jujung_Chang
Adding click Networking button to prevent Interface button is hidden.
2017-10-30     Jujung_Chang
Init the script
