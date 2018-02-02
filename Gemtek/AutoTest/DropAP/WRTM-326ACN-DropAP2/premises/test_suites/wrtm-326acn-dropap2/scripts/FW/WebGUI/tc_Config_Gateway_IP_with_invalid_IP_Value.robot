*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI
*** Variables ***
${wrongformatIP_1}    12.4.5.6.3.5
${wrongformatIP_2}    13.4
${wrongformatIP_3}    avbe.eed.###.4
${nonnumber}    ave.eee.ss
${illegalnumber}    266.355.7766.43
${muticastIP}    224.0.0.1
${Allzeor}    0.0.0.0
${ErrorMSG}    One or more fields contain invalid values!

*** Test Cases ***
tc_Config_Gateway_IP_with_invalid_IP_Value
    [Documentation]  tc_Config_Gateway_IP_with_invalid_IP_Value
    ...    1. Go to web page Networking>Internet Connection, and select protocol to Static IP
    ...    2. Input a invalid Static IP Value and Save and Verify prompt alert should show and the input string should turn red
    [Tags]   @TCID=WRTM-326ACN-299    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to web page Networking>Internet Connection, and select protocol to Static IP
    Input a invalid Static IP Value and Save and Verify prompt alert should show and the input string should turn red

*** Keywords ***
Go to web page Networking>Internet Connection, and select protocol to Static IP
    [Documentation]  Login Web GUI and using static IP
    [Tags]   @AUTHOR=Jujung_Chang
    Config Static Client

Input a invalid Static IP Value and Save and Verify prompt alert should show and the input string should turn red
    [Documentation]  Verify Static Wan Type and IP
    [Tags]   @AUTHOR=Jujung_Chang

    Config Static Client for Input invalid gateway IP checking    ${wrongformatIP_1}
    Config Static Client for Input invalid gateway IP checking    ${wrongformatIP_2}
    Config Static Client for Input invalid gateway IP checking    ${wrongformatIP_3}
    Config Static Client for Input invalid gateway IP checking    ${nonnumber}
    Config Static Client for Input invalid gateway IP checking    ${illegalnumber}
    Config Static Client for Input invalid gateway IP checking    ${muticastIP}
    Config Static Client for Input invalid gateway IP checking    ${Allzeor}

Config Static Client for Input invalid gateway IP checking
    [Arguments]    ${IP}
    [Documentation]
    [Tags]
    Input Text    web    ${Input_Static_Gateway}    ${IP}
    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    ${status} =  run keyword and return status    page should contain element    web    ${InvalidIPHTMLMSG}
    return from keyword if    ${status}==True
    page should contain text    web    ${ErrorMSG}

*** comment ***
2017-10-31     Jujung_Chang
Init the script
