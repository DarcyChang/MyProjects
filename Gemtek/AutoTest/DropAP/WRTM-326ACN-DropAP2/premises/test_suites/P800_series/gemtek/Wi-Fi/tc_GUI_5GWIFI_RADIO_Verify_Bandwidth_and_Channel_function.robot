*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun

*** Variables ***
@{802.11ac_Bandwith}    20 MHz  40 MHz  80 MHz
@{802.11ac_Channel_20MHz}    Auto  36  40  44  48  52  56  60  64  100  104  108  112  116  120  124  128  132  136  140  144  149  153  157  161  165
@{802.11ac_Channel_40MHz}    Auto  36  44  52  60  100  108  116  124  132  140  149  157
@{802.11ac_Channel_80MHz}    Auto  36  52  100  116  132  149
@{802.11n_Bandwith}    20 MHz  40 MHz
@{802.11n_Channel_20MHz}    Auto  36  40  44  48  52  56  60  64  100  104  108  112  116  120  124  128  132  136  140  144  149  153  157  161  165
@{802.11n_Channel_40MHz}    Auto  36  44  52  60  100  108  116  124  132  140  149  157

*** Test Cases ***
tc_tc_GUI_5GWIFI_RADIO_Verify_Bandwidth_and_Channel_function
    [Documentation]    tc_tc_GUI_5GWIFI_RADIO_Verify_Bandwidth_and_Channel_function
    ...   1. login DUT web gui, and go to 5GWIFI page
    ...   2. Select 802.11ac and 802.11n, and check Default Bandwith and Channel Settings is correct
    ...   3. Select 802.11n, and check Default Bandwith and Channel Settings is correct
    [Tags]   @TCID=STP_DD-TC-10902   @globalid=1526084   @DUT=844FB   @DUT=844F    @AUTHOR=Gemtek_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network

    #Select 802.11ac and 802.11n, and check Default Bandwith Settings is correct
    Get Bandwith Settings and Verify Value Is Same As Original Setttings    ${802.11ac_Bandwith}
    #Select 802.11ac and 802.11n, and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    20
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${802.11ac_Channel_20MHz}
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    40
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${802.11ac_Channel_40MHz}
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    80
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${802.11ac_Channel_80MHz}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Select 802.11n, and check Default Bandwith Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_80211bgn_mode']    n
    Get Bandwith Settings and Verify Value Is Same As Original Setttings    ${802.11n_Bandwith}
    #Select 802.11n, and check Default Channel Settings is correct
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    40
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${802.11n_Channel_40MHz}
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_bandwidth']    20
    Get Channel Settings and Verify Value Is Same As Original Setttings    ${802.11n_Channel_20MHz}
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_80211bgn_mode']    ac
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

*** Keywords ***
Get Bandwith Settings and Verify Value Is Same As Original Setttings
    [Arguments]    ${Default_Bandwith}
    [Documentation]    Get bandwith settings and verify is same as original settings
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${Bandwith_Items_List} =   Get List Items    web    xpath=//select[@id='id_bandwidth']
    ${Bandwith_Items_List} =   Get List Items    web    xpath=//select[@id='id_bandwidth']
    log    ${Bandwith_Items_List}
    ${length} =    Get Length    ${Bandwith_Items_List}
    log    ${length}

    #Use for-loop to get all ssid and check warning message respectively
    : FOR    ${INDEX}    IN RANGE   0    ${length}
    \    ${Slice_Tail_Index} =    Evaluate    ${INDEX} + 1
    \    ${Slice_Bandwith} =   Get Slice From List    ${Bandwith_Items_List}    ${INDEX}    ${Slice_Tail_Index}
    \    log    ${Slice_Bandwith}
    \    ${Bandwith_value} =   Get From List     ${Slice_Bandwith}    0
    \    log    ${Bandwith_value}
    \    Should Be Equal    ${Bandwith_value}    ${Default_Bandwith[${INDEX}]}

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
