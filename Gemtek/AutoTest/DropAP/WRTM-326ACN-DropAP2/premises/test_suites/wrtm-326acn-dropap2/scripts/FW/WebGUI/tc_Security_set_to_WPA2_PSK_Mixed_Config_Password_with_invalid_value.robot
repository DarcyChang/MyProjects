*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI

*** Variables ***
${StringLengthThessThan8}    abcdefg
${StringLengthGreateThan64}    abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz0123456789123

*** Test Cases ***
tc_Security_set_to_WPA2_PSK_Mixed_Config_Password_with_invalid_value
    [Documentation]  tc_Security_set_to_WPA2_PSK_Mixed_Config_Password_with_invalid_value
    ...    1. Go to web page Networking>Wireless and set Security to WPA2-PSK Mixed
    ...    2. Input Password beyound the valid value range:character length 8~64 and Verify Gui should display invalid password Value notation: password char turns red
    [Tags]   @TCID=WRTM-326ACN-314    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to web page Networking>Wireless and set Security to WPA2-PSK Mixed
    Input Password beyound the valid value range:character length 8~64 and Verify Gui should display invalid password Value notation: password char turns red

*** Keywords ***
Go to web page Networking>Wireless and set Security to WPA2-PSK Mixed
    [Documentation]  Go to web page Networking>Wireless
    [Tags]   @AUTHOR=Jujung_Chang
    kw_Main_Menu.Open Newworking Wireless Page
    Set Security Value    WPA2-PSK MIXED

Input Password beyound the valid value range:character length 8~64 and Verify Gui should display invalid password Value notation: password char turns red
    [Documentation]  Verify password
    [Tags]   @AUTHOR=Jujung_Chang

    Input a invalid Password checking    ${StringLengthThessThan8}
    Input a invalid Password checking    ${StringLengthGreateThan64}

Input a invalid Password checking
    [Arguments]    ${pwd}
    [Documentation]
    [Tags]
    Set Password For WPA-PSK Security Type    ${pwd}
    page should contain element    web    ${InvalidHtmlMSGForWirelessPassword}

*** comment ***
2017-10-31     Jujung_Chang
Init the script
