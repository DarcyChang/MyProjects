*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun

Suite Teardown    Run keywords    Recover To Original Setting
*** Variables ***
@{United_States_Channel}    Auto  36  52  100  116  132  149
@{European_Union_Channel}    Auto  36  52  100  116  132  149
${Reboot_times}    150

*** Test Cases ***
tc_GUI_5GWIFI_RADIO_Verify_Country_function_5G
    [Documentation]    tc_GUI_5GWIFI_RADIO_Verify_Country_function_5G
    ...   1. login DUT web gui, and go to 5GWIFI page
    ...   2. Configure Country setting is United States, and reboot for this setting to take effect
    ...   3. Check 5G WiFi default channel is correct
    [Tags]    @TCID=STP_DD-TC-10903    @globalid=1526085    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced Radio Setup

    #Configure Country setting is United States, and reboot for this setting to take effect
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_country']    US
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Go to Reboot Device by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Reboot
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Reboot')]
    cpe click    web    xpath=//button[contains(., 'Reboot')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Reboot')]    ${Reboot_times}

    #After select country configuration, Check 5G WiFi default channel is correct
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    80
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${United_States_Channel}

*** Keywords ***
Get Channel Settings and Verify Value Is Same As Original Setttings
    [Arguments]    ${Default_Channel}
    [Documentation]    Get channel settings and verify is same as original settings
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${Channel_Items_List} =   Get List Items    web    xpath=//select[@id='channel_obj_id']
    ${Channel_Items_List} =   Get List Items    web    xpath=//select[@id='channel_obj_id']
    log    ${Channel_Items_List}
    ${length} =    Get Length    ${Channel_Items_List}
    log    ${length}

    #Use for-loop to get all channel and check settings respectively
    : FOR    ${INDEX}    IN RANGE   0    ${length}
    \    ${Slice_Tail_Index} =    Evaluate    ${INDEX} + 1
    \    ${Slice_Channel} =   Get Slice From List    ${Channel_Items_List}    ${INDEX}    ${Slice_Tail_Index}
    \    log    ${Slice_Channel}
    \    ${Channel_value} =   Get From List     ${Slice_Channel}    0
    \    log    ${Channel_value}
    \    Should Be Equal    ${Channel_value}    ${Default_Channel[${INDEX}]}

Recover To Original Setting
    [Arguments]
    [Documentation]    Recover channel to original setting
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    #Restore Country setting is Europe Union, and reboot for this setting to take effect
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced Radio Setup
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_country']    EU
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Go to Reboot Device by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Reboot
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Reboot')]
    cpe click    web    xpath=//button[contains(., 'Reboot')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Reboot')]    ${Reboot_times}
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    80
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${European_Union_Channel}