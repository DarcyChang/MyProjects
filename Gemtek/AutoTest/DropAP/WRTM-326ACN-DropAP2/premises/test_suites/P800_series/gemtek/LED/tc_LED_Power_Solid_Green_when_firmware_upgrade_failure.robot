*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Leo_Li    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Exit Shell Mode

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${times}    10
${count_green_on}    0
${count_green_off}    0
${count_red_on}    0
${count_red_off}    0

*** Test Cases ***
tc_LED_Power_Solid_Green_when_firmware_upgrade_failure
    [Documentation]    Verify if the Power LED stay in Solid Green state when  firmware upgrade failure.
    ...    1.When web page choose invalid image file from PC to upload, the gateway device will be not firmware upgrade.
    ...    2.When the gateway device in firmware upgrade failure state, Power LED must be in Solid Green state.

    [Tags]   @TCID=PREMS-TC-7855   @globalid=1597572LED844F    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Firmware Upgrade by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Firmware Upgrade
    Wait Until Keyword Succeeds    5x    3s    click links    web    Upgrade Image

    #execute upload image java script to show file upload dialog
    execute javascript    web    document.getElementById("fileUploadFrameObjId").style.display='block'
    select_frame    web    id=fileUploadFrameObjId
    choose file   web    id=fileObjectID    ${g_844fb_Dummy_Firmware_image}
    unselect_frame    web
    cpe click    web    id=upgrade_button
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Check Power Green and Red LED Register Value bit 27,28 is 0 or 1
    Wait Until Keyword Succeeds    6x    1s    Get Power_LED_Status_Solid_Green Register Value    n1    ${times}

*** Keywords ***
Enter Shell Mode
    [Arguments]
    [Documentation]    Enter shell mode
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    cli    n1    sh

Exit Shell Mode
    [Arguments]
    [Documentation]    Exit shell mode
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    cli    n1    exit

Get Power_LED_Status_Solid_Green Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check Power Green and Red LED Register Value bit 27,28 is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w([\\w]{1})     1    #bit 27
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_green_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_green_on} + 1
        ...    ELSE    Set Variable    ${count_green_on}
    \    ${count_green_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_green_off} + 1
        ...    ELSE    Set Variable    ${count_green_off}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s([\\w]{1})     1    #bit 28
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_red_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_red_on} + 1
        ...    ELSE    Set Variable    ${count_red_on}
    \    ${count_red_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_red_off} + 1
        ...    ELSE    Set Variable    ${count_red_off}
    \    log    ${count_green_on}
    \    log    ${count_green_off}
    \    log    ${count_red_on}
    \    log    ${count_red_off}
    Should not Be Equal    ${count_green_on}    0
    Should Be Equal    ${count_green_off}    0
    Should Be Equal    ${count_red_on}    0
    Should not Be Equal    ${count_red_off}    0

*** comment ***