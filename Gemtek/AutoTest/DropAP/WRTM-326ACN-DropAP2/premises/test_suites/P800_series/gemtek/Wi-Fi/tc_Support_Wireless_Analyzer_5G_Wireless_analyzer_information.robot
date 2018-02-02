*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang

*** Variables ***
${g_ssid_name}    CXNK-gavin-5G
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${security_type}    WPA - WPA2-Personal
${encryption_type}    AES


*** Test Cases ***
tc_Support_Wireless_Analyzer_5G_Wireless_analyzer_information
    [Documentation]    tc_Support_Wireless_Analyzer_5G_Wireless_analyzer_information
    ...   1. After the configuration is applied, GUI page should show according to your setting.
    ...   2. Use one laptop to get IP from ONT via wireless with your setting.
    [Tags]    @TCID=STP_DD-TC-10921   @globalid=1526115    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 5GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Disable WiFi 5GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    Select Radio Button    web    wireless_onoff    0
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    wireless_onoff    0
    #Go to Wireless Network Analyzer Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless Analyzer
    Select From List By Label    web    xpath=//select[@id='id_ssid']    5 GHz
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Be Equal    web    xpath=//table[@style='display:inline-block']    2    2    Off
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Be Equal    web    xpath=//table[@style='display:inline-block']    9    2    0%
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Be Equal    web    xpath=//table[@style='display:inline-block']    10    2    0%
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Be Equal    web    xpath=//table[@style='display:inline-block']    11    2   0
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Be Equal    web    xpath=//table[@style='display:inline-block']    12    2   0
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Contain   web    xpath=//table[@id='deviceTabObjID']    2    1   No device attached

    #Enable WiFi 5GHz
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Element Is Visible    web    name=wireless_onoff
    Select Radio Button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    wireless_onoff    1

    #Select the first WiFi 5G SSID and rename
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${g_ssid_name}

    #Select security type to WPA-WPA2
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    ${security_type}
    #Select Default Security Key
    Wait Until Keyword Succeeds    5x    3s    Click Element    web    xpath=//input[@id='lshxq01']
    #Read Wi-Fi Password
    ${matched_wifi_pwd} =    get_element_value    web    defaultPskKeyInput
    #Select encryption type to AES
    Select Encryption Type    ${encryption_type}
    #Verify wireless connection
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key    wifi_client    ${g_ssid_name}    ${matched_wifi_pwd}

    #Go to Wireless Network Analyzer Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless Analyzer
    Select From List By Label    web    xpath=//select[@id='id_ssid']    5 GHz
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Be Equal    web    xpath=//table[@style='display:inline-block']    2    2    On
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Not Be Equal    web    xpath=//table[@style='display:inline-block']    9    2    0%
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Not Be Equal    web    xpath=//table[@style='display:inline-block']    10    2    0%
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Not Be Equal    web    xpath=//table[@style='display:inline-block']    11    2   0
    Wait Until Keyword Succeeds    5x    2s    Cell Data Should Not Be Equal    web    xpath=//table[@style='display:inline-block']    12    2   0
    #Check IP address and SSID
    ${result} =    Get Element Text    web    xpath=//tr[@class='deviceTableRemovableRow']
    Should Contain    ${result}    ${g_844_wifi_client_ip}
    Should Contain    ${result}    ${g_ssid_name}

*** Keywords ***
Select Security Type
    [Arguments]    ${security_type}
    [Documentation]    Select security type(WPA-WPA2-Personal, WPA2-Personal, Security Off)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Select From List By Label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    Get Selected List Label    web    xpath=//select[@id='security_type']
    Should Be Equal   ${items}    ${security_type}

Select Encryption Type
    [Arguments]    ${encryption_type}
    [Documentation]    Select encryption type(AES)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Select From List By Label    web    xpath=//select[@id='id_wpa_cipher']    ${encryption_type}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    ${items} =    Get Selected List Label    web    xpath=//select[@id='id_wpa_cipher']
    Should Be Equal   ${items}    ${encryption _type}


Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key
    [Arguments]    ${device}    ${g_ssid_name}    ${secruity_key}
    [Documentation]    Connect to DUT 5g ssid with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${secruity_key} > wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    10x   10s    Is Ping Successful    wifi_client    ${dut_gw}

Is Ping Successful
    [Arguments]    ${device}    ${gw_ip}
    [Documentation]    To check ping ${gw_ip} is successful
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c 3
    log    ${result}
    Should Not Contain    ${result}    100% packet loss

Is WIFI Interface Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

Cell Data Should Be Equal
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should be equal ${included_string}
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${cell1} =    Run Webgui Keyword With Timeout    1    Get Table Cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Be Equal    ${cell1}    ${included_string}

Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${cell1} =    Run Webgui Keyword With Timeout    1    Get Table Cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

Cell Data Should Not Be Equal
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should not be equal ${included_string}
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${cell1} =    Run Webgui Keyword With Timeout    1    Get Table Cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Equal    ${cell1}    ${included_string}

*** comment ***