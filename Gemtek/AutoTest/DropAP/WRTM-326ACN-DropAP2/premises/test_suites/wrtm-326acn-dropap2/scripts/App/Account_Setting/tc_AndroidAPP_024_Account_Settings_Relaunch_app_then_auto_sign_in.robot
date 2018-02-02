*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${app_REMOTE_URL}    http://localhost:4727/wd/hub
${appium_port}    4727

*** Test Cases ***
tc_AndroidAPP_024_Account_Settings_Relaunch_app_then_auto_sign_in
    [Documentation]  tc_AndroidAPP_024_Account_Settings_Relaunch_app_then_auto_sign_in
    ...    1. Launch the app and go to the login page.
    ...    2. Input the username or email, password.
    ...    3. Press Sign in button.
    ...    4. Press HW home key to leave Drop AP app.
    ...    5. Delete the process then launch Drop AP app again.
    ...    6. Check the status.
    [Tags]   @TCID=WRTM-326ACN-372    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Input the username or email, password
    Press Sign in button
    Press HW home key to leave Drop AP app
    Delete the process then launch Drop AP app again
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    #prepare for auto login
    cli    app-vm    appium -p ${appium_port} --no-reset &

Input the username or email, password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    input username
    input password

Press Sign in button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch sign in
    wait main screen
    verify main screen device name

Press HW home key to leave Drop AP app
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Close APP    #Change appium port --no-reset

Delete the process then launch Drop AP app again
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Open Application    ${app_REMOTE_URL}    platformName=${g_app_PLATFORM_NAME}    platformVersion = ${g_app_PLATFORM_VERSION}    deviceName=${g_app_device_name}    app=${g_APP_APK}    appPackage=${g_APP_PACKAGE_NAME}    appActivity=${g_APP_ACTIVITY}
    wait main screen

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify main screen device name

*** comment ***
2018-01-10 Gavin_Chang
1. Open another appium port for auto login in the beginning of script.

2017-11-27    Leo_Li
Init the script