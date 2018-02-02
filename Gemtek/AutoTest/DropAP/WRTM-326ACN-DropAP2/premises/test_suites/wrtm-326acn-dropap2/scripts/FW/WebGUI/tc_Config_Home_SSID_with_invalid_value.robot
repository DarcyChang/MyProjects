*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI

*** Variables ***
${EmptyString}
${StringGreaterThan32}    abcdefghijklmnopqrstuvwxyz0123456
${ErrorMSG}    One or more required fields have no value!

*** Test Cases ***
tc_Config_Home_SSID_with_invalid_value
    [Documentation]  tc_Config_Home_SSID_with_invalid_value
    ...    1. Go to web page Networking>Wireless
    ...    2. Input home SSID beyound the valid value range and Verify Gui should display invalid SSID Value notation: password char turns red
    [Tags]   @TCID=WRTM-326ACN-303    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to web page Networking>Wireless
    Input home SSID beyound the valid value range and Verify Gui should display invalid SSID Value notation: password char turns red

*** Keywords ***
Go to web page Networking>Wireless
    [Documentation]  Go to web page Networking>Wireless
    [Tags]   @AUTHOR=Jujung_Chang
    kw_Main_Menu.Open Newworking Wireless Page

Input home SSID beyound the valid value range and Verify Gui should display invalid SSID Value notation: password char turns red
    [Documentation]  Verify Static Wan Type and IP
    [Tags]   @AUTHOR=Jujung_Chang

    Input a invalid SSID checking    ${StringGreaterThan32}
    Input a invalid SSID checking    ${EmptyString}

Input a invalid SSID checking
    [Arguments]    ${ssid}
    [Documentation]
    [Tags]
    input text    web    ${Input_SSID}    ${ssid}
    cpe click       web    ${Button_SAVE}
    ${r}  Get Length    ${ssid}
    run keyword if  ${r} == 0    page should contain text    web    ${ErrorMSG}
    ...   ELSE    page should contain element    web    ${InvalidIPHTMLMSG}

*** comment ***
2017-10-31     Jujung_Chang
Init the script
