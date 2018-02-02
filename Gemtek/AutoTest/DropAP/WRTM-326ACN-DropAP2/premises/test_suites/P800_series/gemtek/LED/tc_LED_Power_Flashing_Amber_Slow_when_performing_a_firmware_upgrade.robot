*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Leo_Li    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Exit Shell Mode

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${times}    5
${Reboot_times}    150
${count_green_on}    0
${count_green_off}    0
${count_red_on}    0
${count_red_off}    0

*** Test Cases ***
tc_LED_Power_Flashing_Amber_Slow_when_performing_a_firmware_upgrade
    [Documentation]    Verify if the Power LED stay in Flashing Amber Slow state when the ONT is performing a firmware upgrade.
    ...    1.When web page choose image file from PC to upload, the gateway device must be firmware upgrade.
    ...    2.When the gateway device is performing a firmware upgrade, Power LED is Flashing Amber Slow state.
    [Tags]   @TCID=PREMS-TC-7854   @globalid=1597571LED844F    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
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
    choose file   web    id=fileObjectID    ${g_844fb_Firmware_image}
    unselect_frame    web
    cpe click    web   id=upgrade_button

    #Check Power Green and Red LED Register Value bit 27,28 is 0 or 1
    Wait Until Keyword Succeeds    6x    1s    Get Power_LED_Status_Flashing_Amber Register Value    n1    ${times}
    Wait Until Element Is Not Visible    web    xpath=//button[contains(., 'Upgrade')]    ${Reboot_times}    #After upload and reboot finish, web page upgrade button will disappear.

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

Get Power_LED_Status_Flashing_Amber Register Value
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
    sleep    1    # We need to add a sleep cycle here to prevent multiple dw command to cause CPE crash while it is doing fw upgrade
    Should not Be Equal    ${count_green_on}    0
    Should not Be Equal    ${count_green_off}    0
    Should not Be Equal    ${count_red_on}    0
    Should not Be Equal    ${count_red_off}    0

*** comment ***