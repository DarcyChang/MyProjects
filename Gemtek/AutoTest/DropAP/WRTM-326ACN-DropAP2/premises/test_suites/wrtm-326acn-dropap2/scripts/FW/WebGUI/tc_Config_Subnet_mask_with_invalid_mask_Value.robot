*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang
Test Setup   Login Web GUI
Test teardown    Restore Networking Configuration

*** Variables ***
${wrongformatIP_1}    12.4.5.6.3.5
${wrongformatIP_2}    13.4
${wrongformatIP_3}    avbe.eed.###.4
${invalidsubnet_1}    255.255.255.251
${invalidsubnet_2}    255.255.255.247
${invalidsubnet_3}    255.255.255.239
${invalidsubnet_4}    255.255.0.224
${invalidsubnet_5}    255.0.255.192
${invalidsubnet_6}    0.255.255.128
${invalidsubnet_7}    0.0.254.0
${invalidsubnet_8}    0.0.0.0
${invalidsubnet_9}    0.255.0.0
${invalidsubnet_10}    0.0.0.255
${invalidsubnet_11}    0.255.224.0
${invalidsubnet_12}    255.255.192.255
${invalidsubnet_13}    0.255.192.255
${ErrorMSG}    One or more fields contain invalid values!

*** Test Cases ***
tc_Config_Subnet_mask_with_invalid_mask_Value
    [Documentation]  tc_Config_Subnet_mask_with_invalid_mask_Value
    ...    1. Go to web page Networking>Internet Connection, and select protocol to Static IP
    ...    2. Input a invalid Static IP Value and Save and Verify prompt alert should show and the input string should turn red
    [Tags]   @TCID=WRTM-326ACN-295    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
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

    Config Static Client for Input invalid mask IP checking    ${wrongformatIP_1}
    Config Static Client for Input invalid mask IP checking    ${wrongformatIP_2}
    Config Static Client for Input invalid mask IP checking    ${wrongformatIP_3}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_1}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_2}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_3}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_4}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_5}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_6}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_7}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_8}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_9}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_10}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_11}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_12}
    Config Static Client for Input invalid mask IP checking    ${invalidsubnet_13}

Config Static Client for Input invalid mask IP checking
    [Arguments]    ${IP}
    [Documentation]
    [Tags]
    Input Text    web    ${Input_Subnet_Mask}    ${IP}
    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
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
