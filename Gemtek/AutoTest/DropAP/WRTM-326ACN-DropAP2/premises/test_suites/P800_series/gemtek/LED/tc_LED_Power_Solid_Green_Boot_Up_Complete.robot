*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Leo_Li    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Exit Shell Mode

*** Variables ***
${Reboot_times}    150
${844fb_dump_led_register}     dw fffe8114

*** Test Cases ***
tc_LED_Power_Solid_Green_Boot_Up_Complete
    [Documentation]    Verify if the Power LED  stay in Solid Green state when ONT boot-up is complete successful.
    ...    1.When web page select Reboot button, the gateway device must be reboot.
    ...    2.When the gateway device boot-up is complete, Power LED is Solid Green state.
    [Tags]   @TCID=PREMS-TC-7849   @globalid=1597566LED844F    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Check Power Green LED Register Value 27 bit is 0
    ${result} =   Wait Until Keyword Succeeds    5x    2s    Get Power_LED_Status_Solid_Green Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    0

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Reboot Device by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Reboot
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Reboot')]
    cpe click    web    xpath=//button[contains(., 'Reboot')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Reboot')]    ${Reboot_times}    #After reboot finish, web page Reboot button will display.

    #Check Power Green LED Register Value 27 bit is 0
    cli    n1    sh
    ${result} =   Wait Until Keyword Succeeds    5x    2s    Get Power_LED_Status_Solid_Green Register Value    n1
    cli    n1    exit
    log    ${result}
    Should Be Equal     ${result}    0

*** Keywords ***
Enter Shell Mode
    [Arguments]
    [Documentation]    Enter shell mode
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Keyword Succeeds    5x    3s    cli    n1    sh    ~ #

Exit Shell Mode
    [Arguments]
    [Documentation]    Exit shell mode
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    cli    n1    exit

Get Power_LED_Status_Solid_Green Register Value
    [Arguments]    ${device}
    [Documentation]    when Power LED solid Green state Register Value is 17eafbef => should retrive twenty-seventh hex: 7->0111, bit 27 is 0
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

*** comment ***