*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun    stable

*** Variables ***
@{DFS_Channel_20MHz}    Auto  36  40  44  48  52  56  60  64  100  104  108  112  116  120  124  128  132  136  140  144  149  153  157  161  165
@{DFS_Channel_40MHz}    Auto  36  44  52  60  100  108  116  124  132  140  149  157
@{DFS_Channel_80MHz}    Auto  36  52  100  116  132  149
@{No_DFS_Channel_20MHz}    Auto  36  40  44  48  149  153  157  161  165
@{No_DFS_Channel_40MHz}    Auto  36  44  149  157
@{No_DFS_Channel_80MHz}    Auto  36  149

*** Test Cases ***
tc_GUI_5GWIFI_RADIO_Verify_DFS_function
    [Documentation]    tc_GUI_5GWIFI_RADIO_Verify_DFS_function
    ...   1. login DUT web gui, and go to 5GWIFI page
    ...   2. Enable DFS with 20 / 40 / 80 MHz, check channel default settings if is correct
    ...   3. Disable DFS with 20 / 40 / 80 MHz, check channel default settings if is correct
    [Tags]    @TCID=STP_DD-TC-10902    @globalid= 1526084    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network

    #Select DFS checkbox enabled with Select bandwith 20 MHz, and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    20
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${DFS_Channel_20MHz}

    #Select bandwith 40 MHz and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    40
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${DFS_Channel_40MHz}

    #Select bandwith 80 MHz and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    80
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${DFS_Channel_80MHz}

    #Select DFS checkbox disabled with Select bandwith 80 MHz, and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    unselect_checkbox    web    xpath=//input[@id='dfs_check_obj_id']
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${No_DFS_Channel_80MHz}

    #Select bandwith 40 MHz and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    40
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${No_DFS_Channel_40MHz}

    #Select bandwith 20 MHz and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    20
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${No_DFS_Channel_20MHz}
    Wait Until Keyword Succeeds    5x    3s    select_checkbox    web    xpath=//input[@id='dfs_check_obj_id']
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]


*** Keywords ***
Get Channel Settings and Verify Value Is Same As Original Setttings
    [Arguments]    ${Default_Channel}
    [Documentation]    Get channel settings and verify is same as original settings
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${Channel_Items_List} =   Get List Items    web    xpath=//select[@id='channel_obj_id']
    log    ${Channel_Items_List}
    ${length} =    Get Length    ${Channel_Items_List}
    log    ${length}

    #Use for-loop to get all ssid and check warning message respectively
    : FOR    ${INDEX}    IN RANGE   0    ${length}
    \    ${Slice_Tail_Index} =    Evaluate    ${INDEX} + 1
    \    ${Slice_Channel} =   Get Slice From List    ${Channel_Items_List}    ${INDEX}    ${Slice_Tail_Index}
    \    log    ${Slice_Channel}
    \    ${Channel_value} =   Get From List     ${Slice_Channel}    0
    \    log    ${Channel_value}
    \    Should Be Equal    ${Channel_value}    ${Default_Channel[${INDEX}]}