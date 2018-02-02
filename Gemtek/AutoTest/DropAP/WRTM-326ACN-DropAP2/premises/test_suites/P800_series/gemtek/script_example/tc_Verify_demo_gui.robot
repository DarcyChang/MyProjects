*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=WebGUI    @AUTHOR=thomas_chen    norun

*** Variables ***
${844fb_gui_session}    web
${844fb_dump_led_register}     dw fffe8114
${844fb_power_led_off_hex}    1f     #ex: 1feaefef
${844fb_power_led_on_hex}    17     #ex: 17eaefef
${844fb_power_led_red_hex}    0f     #ex: 0feaefef
${844fb_power_led_amber_hex}    07  #ex: 07eaefe


*** Test Cases ***
tc_Verify_Demo scripts
    [Documentation]    tc_Verify_Demo scripts
    [Tags]    @DUT=844F    @DUT=844FB

    login ont    ${844fb_gui_session}    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    click links    ${844fb_gui_session}    Advanced
    click links    ${844fb_gui_session}    LED Suppress Control
    select radio button    ${844fb_gui_session}    ledSuppressMode    2
    select radio button    ${844fb_gui_session}    LedPower    1
    radio_button_should_be_set_to    ${844fb_gui_session}    LedPower    1

*** comment ***






