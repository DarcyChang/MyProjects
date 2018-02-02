*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Close APP

*** Variables ***
${created_member_name}    KID
${restore_member}    Lanhost
${restore_device}    app-lanhost
${app_home_ssid}    DropAP-0ba9f8
${google_web}    www.google.com
*** Test Cases ***
tc_AndroidAPP_081_MainScreen_Reset_to_default
    [Documentation]  tc_AndroidAPP_081_MainScreen_Reset_to_default
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Reset to Default.
    ...    3. Press reset to default button.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-321    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Reset to Default
    Press reset to default button
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen
    Create some family member

Create some family member
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Create Family Member    ${created_member_name}    ${created_member_name}

Launch main screen > Device settings icon > Reset to Default
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    Swipe To Up

Press reset to default button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Reset to Default
    wait until page contains element    ${default_ok}
    Click Element    ${default_ok}

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait until page contains element    ${add_a_DropAP}    timeout=60
    Sleep    10
    Click Element    ${add_a_DropAP}
    Sleep    25
    Click Element    ${DropAP_is_powered_on}
    Sleep    35
    Click Element    ${plugged_in_the_ethernet_cable}
    wait until keyword succeeds    3x    5s    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${app_home_ssid}    ${DEVICES.wifi_client.int}    ${google_web}
    #Sleep    35
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    app-vm    ${google_web}
    Click Element    ${next_step}
    wait until page contains element    ${OK_btn}    timeout=60
    Click Element    ${OK_btn}
    wait main screen
    touch family member
    Page Should Not Contain Text    ${created_member_name}
    touch left
    Restore Member Device

Restore Member Device
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Trigger Device List
    Create Family Member    ${restore_member}    ADULT    ${restore_device}


*** comment ***
2017-12-25 Gavin_Chang
1. Move "Restore Member Device" to the last step to run teardown only when test case pass

2017-12-18 Gavin_Chang
1. Add Restore Member Device for following data report test.

2017-12-12    Leo_Li
Init the script
