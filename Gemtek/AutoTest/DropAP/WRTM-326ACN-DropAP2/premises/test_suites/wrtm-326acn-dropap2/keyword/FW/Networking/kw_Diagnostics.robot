*** Settings ***
Resource    base.robot

*** Variables ***
${Input_NSLOOKUP} =    xpath=//*[@id="maincontent"]/div/form/div/fieldset/div[3]/input[1]
${Button_NSLOOKUP} =    xpath=//*[@id="maincontent"]/div/form/div/fieldset/div[3]/input[2]
${Text_NSLOOKUP} =    xpath=//*[@id="diag-rc-output"]/pre
${Input_IP}    xpath=//*[@id="maincontent"]/div/form/div/fieldset/div[1]/input[1]
${PingButton}    xpath=//*[@id="maincontent"]/div/form/div/fieldset/div[1]/input[2]
${TracerouteInput}    xpath=//*[@id="maincontent"]/div/form/div/fieldset/div[2]/input[1]
${TracerouteButton}    xpath=//*[@id="maincontent"]/div/form/div/fieldset/div[2]/input[2]

*** Keywords ***
Go to Diagnostics
    [Documentation]   ping test
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking  Diagnostics

Ping Using DropAP GUI
    [Documentation]   ping test
    [Tags]   @AUTHOR=Jujung_Chang
    [Arguments]  ${IP}
    input text    web    ${Input_IP}    ${IP}
    cpe click       web    ${PingButton}
    Wait Until Config Has Applied Completely

Traceroute Using DropAP GUI
    [Documentation]   ping test
    [Tags]   @AUTHOR=Jujung_Chang
    [Arguments]  ${IP}
    input text    web    ${TracerouteInput}    ${IP}
    cpe click       web    ${TracerouteButton}

NSLOOKUP Using DropAP GUI
    [Documentation]   NSLOOKUP test
    [Tags]   @AUTHOR=Jujung_Chang
    [Arguments]  ${IP}
    input text    web    ${Input_NSLOOKUP}    ${IP}
    cpe click       web    ${Button_NSLOOKUP}

Should Be Contain Text At Diagnostics Page
    [Arguments]    ${text}
    [Documentation]
    [Tags]
    page should contain text    web    ${text}

*** comment ***
2017-10-31     Jujung_Chang
Init the script