*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI

*** Variables ***
${StringLength3}    abc
${StringLength7}    abcdefg
${StringLength11}    abcdefghijk
${HEX_Length10}    aaaaaaaaaa
${HEX_Length26}    aaaaaaaaaaaaaaaaaaaaaaaaaa
${ASCII_Length5}    !!!!!
${ASCII_Length13}    !!!!!!!!!!!!!

*** Test Cases ***
tc_Security_set_to_WEP_Config_Password_with_invalid_value_and_another_valid_value_testing
    [Documentation]  tc_Security_set_to_WEP_Config_Password_with_invalid_value_and_another_valid_value_testing
    ...    1. Go to web page Networking>Wireless and set Security to WEP
    ...    2. Input Password beyound the valid value range:character length 5, 10, 13 and Verify Gui should display invalid password Value notation: password char turns red
    [Tags]   @TCID=WRTM-326ACN-305    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to web page Networking>Wireless and set Security to WEP
    Input Password beyound the valid value range:character length 5, 10, 13 and Verify Gui should display invalid password Value notation: password char turns red
    Using ASCII And HEX to test Password is allowed

*** Keywords ***
Go to web page Networking>Wireless and set Security to WEP
    [Documentation]  Go to web page Networking>Wireless and set Security to WEP
    [Tags]   @AUTHOR=Jujung_Chang
    kw_Main_Menu.Open Newworking Wireless Page
    Set Security Value    WEP

Input Password beyound the valid value range:character length 5, 10, 13 and Verify Gui should display invalid password Value notation: password char turns red
    [Documentation]  Verify password
    [Tags]   @AUTHOR=Jujung_Chang

    Input a invalid Password checking    ${StringLength3}
    Input a invalid Password checking    ${StringLength7}
    Input a invalid Password checking    ${StringLength11}

Input a invalid Password checking
    [Arguments]    ${pwd}
    [Documentation]
    [Tags]
    Set Password    ${pwd}
    page should contain element    web    ${InvalidHtmlMSGForWirelessPassword}

Using ASCII And HEX to test Password is allowed
    [Arguments]
    [Documentation]
    [Tags]
    Input a valid Password checking    ${HEX_Length10}
    Input a valid Password checking    ${HEX_Length26}
    Input a valid Password checking    ${ASCII_Length5}
    Input a valid Password checking    ${ASCII_Length13}

Input a valid Password checking
    [Arguments]    ${pwd}
    [Documentation]
    [Tags]
    Set Password    ${pwd}
    page should not contain element    web    ${InvalidHtmlMSGForWirelessPassword}

*** comment ***
2017-10-31     Jujung_Chang
Init the script
