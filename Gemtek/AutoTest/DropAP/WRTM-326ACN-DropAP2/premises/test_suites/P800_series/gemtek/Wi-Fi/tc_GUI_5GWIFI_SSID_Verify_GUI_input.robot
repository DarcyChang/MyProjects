*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun    stable

*** Variables ***
${special_char_ssid}    !@#$%^&*()~
${others_ssid_name}    5GHz_Guest040D1E
*** Test Cases ***
tc_GUI_5GWIFI_SSID_Verify_GUI_input
    [Documentation]    tc_GUI_5GWIFI_SSID_Verify_GUI_input
    ...   1. login DUT web guit, and go to 5GWIFI page
    ...   2. Input special characters SSID name, and click apply button
    ...   3. Check warnings will be generated if choose others SSID and input the same special characters SSID name
    [Tags]    @TCID=STP_DD-TC-10913    @globalid=1526097    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Teardown]    Reset SSID Name

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Change WiFi 2.4G Security Key
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    #Store original SSID for reset SSID name
    ${original_result} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Set Global Variable    ${original_ssid_name}    ${original_result}
    #Input special characters SSID name
    input_text    web    xpath=//input[@id='id_ssid_name']    ${special_char_ssid}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${special_char_ssid}
    ${after_result} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should contain    ${after_result}    ${special_char_ssid}

    #Choose others SSID and Input the same special characters SSID name to check warning message
    Select Others SSID And Check Warning Message
*** Keywords ***
Select Others SSID And Check Warning Message
    [Arguments]
    [Documentation]    Select Others SSID And Check Warning Message
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    ${SSID_Items_List} =   Get List Items    web    xpath=//select[@id='id_ssid']
    log    ${SSID_Items_List}
    ${length} =    Get Length    ${SSID_Items_List}
    log    ${length}
    ${SSID_List} =   Convert To List    ${SSID_Items_List}
    log    ${SSID_List}

    #Use for-loop to get all ssid and check warning message respectively
    : FOR    ${INDEX}    IN RANGE   1    ${length}
    \    ${Slice_Tail_Index} =    Evaluate    ${INDEX} + 1
    \    ${Slice_SSID} =   Get Slice From List    ${SSID_Items_List}    ${INDEX}    ${Slice_Tail_Index}
    \    log    ${Slice_SSID}
    \    ${others_ssid_name} =   Get From List     ${Slice_SSID}    0
    \    log    ${others_ssid_name}
    \    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${others_ssid_name}
#    \    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    \    Wait Until Keyword Succeeds    5x    3s    select radio button    web    ssid_state    1
    \    input_text    web    xpath=//input[@id='id_ssid_name']    ${special_char_ssid}
    \    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    \    page should contain text     web    The assigned SSID Name(${special_char_ssid}) and 1st SSID is the same, please select a new one.


Reset SSID Name
    [Arguments]
    [Documentation]    Reset SSID Name
    [Tags]    @AUTHOR=Gemteks_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Change WiFi 2.4G Security Key
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    input_text    web    xpath=//input[@id='id_ssid_name']    ${original_ssid_name}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
