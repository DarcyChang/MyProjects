*** Settings ***
Resource    base.robot

*** Variables ***
${popup_dropap_offline}    com.dropap.dropap:id/infoTxt
${popup_ok}    com.dropap.dropap:id/positiveBtn
${check_keyboard}    adb shell dumpsys window InputMethod | grep "mHasSurface"
${congratulation_btn}    0
*** Keywords ***
Launch APP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    set suite variable    ${congratulation_btn}    0
    Set Library Search Order    AppiumLibrary
    Open Application    ${g_app_REMOTE_URL}    platformName=${g_app_PLATFORM_NAME}    platformVersion = ${g_app_PLATFORM_VERSION}    deviceName=${g_app_device_name}    app=${g_APP_APK}    appPackage=${g_APP_PACKAGE_NAME}    appActivity=${g_APP_ACTIVITY}
    ${status}    run keyword and return status    wait sign in
    return from keyword if    ${status}==True
    set suite variable    ${congratulation_btn}    1
    ${status}    run keyword and return status    Click Element    ${Bind_the_Existing_DropAP_Router_btn_master}
    return from keyword if    ${status}==True
    Set Up Your DropAP


First Launch
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Set Library Search Order    AppiumLibrary
    Open Application    ${g_app_REMOTE_URL}    platformName=${g_app_PLATFORM_NAME}    platformVersion = ${g_app_PLATFORM_VERSION}    deviceName=${g_app_device_name}    app=${g_APP_APK}    appPackage=${g_APP_PACKAGE_NAME}    appActivity=${g_APP_ACTIVITY}

Close APP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${adb_status}    run keyword and ignore error     cli    app-vm    ps -aux | grep adb
    run keyword and ignore error    Close All Applications
    ${adb_status}    run keyword and ignore error     cli    app-vm    ps -aux | grep adb


Sign In
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    input username
    input password
    touch sign in

    run keyword if    ${congratulation_btn} == 1
    ...    Run keywords
    ...    Wait Until Page Contains Element    ${OK_btn}    timeout=30
    ...    AND
    ...    Click Element    ${OK_btn}

Swipe To Left
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe By Percent    90    50    10   50
    sleep    3s

Swipe To Right
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe By Percent    10    50    90   50
    sleep    3s

Swipe To Up
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe By Percent    50    70    50   30
    sleep    3s

Swipe To Down
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe By Percent    50    30    50   70
    sleep    3s

Detect Keyboard Status Is Visible
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${keyboard_status}    cli    app-vm    ${check_keyboard}
    ${visible}    run keyword and return status    Should Contain    ${keyboard_status}    true
    [Return]    ${visible}

Set Up Your DropAP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Set_Up_Your_DropAP}
    Click Element    ${plugged_in_the_ethernet_cable}
    Click Element    ${next_step}
    Wait Until Page Contains    ${OK_btn}    timeout=30
    Click Element    ${Ok_btn}

*** comment ***
2017-11-15 Gavin_Chang
Init basic AP common keyword


