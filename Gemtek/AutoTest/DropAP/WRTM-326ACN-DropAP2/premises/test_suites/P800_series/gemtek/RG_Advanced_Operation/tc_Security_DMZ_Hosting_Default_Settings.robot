*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${modified_DMZ_Device_IP Address}    192.168.1.200
${Restore_times}    150
${Original_DMZ_Hosting_settings}    true

*** Test Cases ***
tc_Security_DMZ_Hosting_Default_Settings
    [Documentation]    Verify Restore Defaults the device gateway, default settings should be restoring to factory defaults.
    ...    1.When web page choose Restore Defaults, the gateway device DMZ Hosting settings must be Restore default values.
    [Tags]   @TCID=STP_DD-TC-10501   @globalid=1506091    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to DMZ Hosting Settings by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    DMZ Hosting

    #Modified DMZ state settings by web page
    Wait Until Element Is Visible    web    id=dmz_on
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    dmz_on    1

    #Modified DMZ Device settings by web page
    Wait Until Element Is Visible    web    id=deviceTypeRadio2
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    deviceTypeRadio2    1
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address"]    ${modified_DMZ_Device_IP Address}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Choose Restore Defaults by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Restore Defaults
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Restore')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Restore')]    ${Restore_times}    #After Restore finish, web page will display Restore button.

    #Go to DMZ Hosting Settings by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    DMZ Hosting

    #Check default values of DMZ Hosting settings by web Page
    ${get_DMZ_Hosting_settings_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="deviceTypeRadio1"]@disabled
    Should Contain    ${get_DMZ_Hosting_settings_result}    ${Original_DMZ_Hosting_settings}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='dmz_table']    2    1    No Entries Defined

*** Keywords ***
Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

*** comment ***