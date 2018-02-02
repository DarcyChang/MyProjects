*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI
Test teardown    Restore Networking Configuration
*** Variables ***
${AllzeroIP}    0.0.0.0
${FivezeroIP}    0.0.0.0.0
${muticastIP}   224.0.0.1
${illegalrangeIP}    266.355.7766.43
${illegalrangeIP_2}    256.1.1.1
${wrongformatIP_1}    12.4.5.6.3.5
${wrongformatIP_2}    13.4
${wrongformatIP_3}    avbe.eed.###.4
${ErrorMSG}    One or more fields contain invalid values!

*** Test Cases ***
tc_Config_Static_IP_with_invalid_IP_Value
    [Documentation]  tc_Config_Static_IP_with_invalid_IP_Value
    ...    1. Go to web page Networking>Internet Connection, and select protocol to Static IP
    ...    2. Input a invalid Subnet Static IP Value and save and Verify prompt alert should show and the input string should turn red
    [Tags]   @TCID=WRTM-326ACN-292    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to web page Networking>Internet Connection, and select protocol to Static IP
    Input a invalid Subnet Static IP Value and save and Verify prompt alert should show and the input string should turn red

*** Keywords ***
Go to web page Networking>Internet Connection, and select protocol to Static IP
    [Documentation]  Login Web GUI and using static IP
    [Tags]   @AUTHOR=Jujung_Chang
    Config Static Client

Input a invalid Subnet Static IP Value and save and Verify prompt alert should show and the input string should turn red
    [Documentation]  Verify Static Wan Type and IP
    [Tags]   @AUTHOR=Jujung_Chang
    Config Static Client for Input invalid Static IP checking    ${AllzeroIP}
    Config Static Client for Input invalid Static IP checking    ${FivezeroIP}
    Config Static Client for Input invalid Static IP checking    ${muticastIP}
    Config Static Client for Input invalid Static IP checking    ${illegalrangeIP}
    Config Static Client for Input invalid Static IP checking    ${illegalrangeIP_2}
    Config Static Client for Input invalid Static IP checking    ${wrongformatIP_1}
    Config Static Client for Input invalid Static IP checking    ${wrongformatIP_2}
    Config Static Client for Input invalid Static IP checking    ${wrongformatIP_3}

Config Static Client for Input invalid Static IP checking
    [Arguments]    ${IP}
    [Documentation]
    [Tags]
    Input Text    web    ${Input_Static_IP}    ${IP}
    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    sleep    2s
    ${status} =  run keyword and return status    page should contain element    web    ${InvalidIPHTMLMSG}
    return from keyword if    ${status}==True
    page should contain text    web    ${ErrorMSG}

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
