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
tc_Verify_led_demo
   [Documentation]    To demostrate the usage of CLI automation
   [Tags]   @DUT=844FB  @DUT=844F
   [Timeout]
   cli    n1    ledctl Power on
   ${result} =   Get Power Green LED Register Value    n1
   log    Power Green LED register value is ${result}
   ${result} =   Get Power Red LED Register Value    n1
   log    Power Green Red register value is ${result}

   cli    n1    ledctl Power off
   ${result} =   Get Power Green LED Register Value    n1
   log    Power Green LED register value is ${result}
   ${result} =   Get Power Red LED Register Value    n1
   log    Power Green Red register value is ${result}

   cli    n1    ledctl Power red
   ${result} =   Get Power Green LED Register Value    n1
   log    Power Green LED register value is ${result}
   ${result} =   Get Power Red LED Register Value    n1
   log    Power Green Red register value is ${result}

   cli    n1    ledctl Power amber
   ${result} =   Get Power Green LED Register Value    n1
   log    Power Green LED register value is ${result}
   ${result} =   Get Power Red LED Register Value    n1
   log    Power Green Red register value is ${result}

*** Keywords ***
Get Power Green LED Register Value
    [Arguments]    ${device}
    [Documentation]

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w([\\w]{1})     1   #bit 27    0xFFFE8114 : 17eaefaf  => should retrive second hex: 7->0111, bit 27 is 0
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 10101111
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0

    log to console    ${ret}
    [Return]    ${ret}

Get Power Red LED Register Value
    [Arguments]    ${device}
    [Documentation]

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s([\\w]{1})     1    #bit 28   0xFFFE8114 : 17eaefaf  => should retrive first hex: 1->0001, bit 28 is 1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 10101111
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0

    log to console    ${ret}
    [Return]    ${ret}


*** comment ***






