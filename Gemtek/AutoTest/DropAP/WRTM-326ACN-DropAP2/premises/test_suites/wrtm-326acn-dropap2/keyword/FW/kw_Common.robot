*** Settings ***
Resource    base.robot

*** Variables ***
${Loading_Block} =      css=div[class="Loading"]
${Sign_Config_Is_Applying}=    css=img[alt="Loading"]
${DropAP_Setup} =      xpath=//*[@id="btn-setup"]
${DropAP_Ok} =      xpath=//*[@id="btn-ok"]

*** Keywords ***

Login Web GUI
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    login ont    web    ${g_dut_gui_url}

End Test
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Close Browser   web

Wait Until Config Has Applied Completely
    [Documentation]  Wait until config is applying animated sign has disapear
    [Tags]   @AUTHOR=Johnny_Peng
    Wait until element is not visible    web    ${Sign_Config_Is_Applying}
    sleep   1s

Set Checkbox State
    [Documentation]     If current state is not equal to assigned state, click checkbox once to make it consist to assigned state
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${checkbox_locator}     ${set_checkbox_state}
    ${checkbox_state} =     Assert Checkbox is checked      ${checkbox_locator}
    #if checkbox state is not equal, then click check box
    run keyword Unless      ${checkbox_state}==${set_checkbox_state}      cpe click     web   ${checkbox_locator}

Assert Element is visible
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${locator}
    ${is_visible}=    run keyword and return status   element should be visible   web    ${locator}
    [Return]  ${is_visible}

Assert Checkbox is checked
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]  ${checkbox_locator}
    ${checkbox_state} =     run keyword and return status   Checkbox Should Be Selected    web     ${checkbox_locator}
    [Return]  ${checkbox_state}

Config Setup DropAP
    Wait Until Keyword Succeeds    10x    2s    cpe click    web    ${DropAP_Setup}
    Wait Until Keyword Succeeds    10x    10s    cpe click    web    ${DropAP_OK}
    Wait Until Keyword Succeeds    10x    10s    cpe click    web    ${DropAP_OK}
    page should contain text    web    Status
    sleep   1s

linuxhost cli
    [Arguments]  ${d}  @{args}
    [Return]  ${result}
    # workaroud for cafe get last output bugs
    ${result} =   cli    ${d}     ${EMPTY}
    ${result} =   cli  ${d}   @{args}  timeout=200
    ${r} =   cli  ${d}  echo $?   timeout=20
    ${tmp} =   get lines matching regexp  ${r}   \\\d
    @{r} =   split to lines  ${tmp}
    should be equal as integers  @{r}[0]  0

wificlient cli
    [Arguments]  ${d}  @{args}
    [Return]  ${r}
    ${r} =   linuxhost cli  ${d}  @{args}

*** comment ***
2017-10-18  Hans_SUn
Add Config Setup DropAP keyword
2017-10-17  Johnny_Peng
Fix Keyword Function:Wait Until Config Has Applied Completely
    Cannot distinguish Configuration is applied properly
2017-10-16     Johnny_Peng
Init the script

