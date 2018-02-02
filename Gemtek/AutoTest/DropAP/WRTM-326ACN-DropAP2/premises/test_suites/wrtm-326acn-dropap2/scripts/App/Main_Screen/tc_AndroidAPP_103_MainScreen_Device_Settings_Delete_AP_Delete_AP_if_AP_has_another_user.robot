*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_103_MainScreen_Device_Settings_Delete_AP_Delete_AP_if_AP_has_another_user
    [Documentation]  tc_AndroidAPP_103_MainScreen_Device_Settings_Delete_AP_Delete_AP_if_AP_has_another_user
    ...    1. Launch the app and login the user account.
    ...    2. [User 1]Add a Drop AP device then bind it.
    ...    3. [User 2]Use another email to bind the device.
    ...    4. Enable performance function.
    ...    5. Login the user 1 account.
    ...    6. [User 1]Launch main screen > Dashboard > Delete AP.
    ...    7. Try to login the 2 accounts and check the status.

    [Tags]   @TCID=WRTM-326ACN-424    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and login the user account
    [User 1]Add a Drop AP device then bind it
    [User 2]Use another email to bind the device
    Enable performance function
    Login the user 1 account
    [User 1]Launch main screen > Dashboard > Delete AP
    Try to login the 2 accounts and check the status

*** Keywords ***
Launch the app and login the user account
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

[User 1]Add a Drop AP device then bind it
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${device_name}    Get Text    ${main_screen_device_name}
    touch Device Settings
    touch Authorization Code
    Wait Until Page Contains Element    ${master_code}
    ${master_code_value}    Get Text    ${master_code}
    log    ${master_code_value}
    set test variable    ${master_code_value}    ${master_code_value}
    Page Should Contain Text    ${master_code_value}
    touch left
    touch left
    touch account menu
    touch sign out
    wait sign out web
    Clear Text    ${username}
    Input Text    ${username}    ${second_username}
    Input Text    ${password}    ${second_password}
    touch sign in
    Wait Until Page Contains Element    ${add_a_DropAP}    timeout=60
    touch add a DropAP
    touch DropAP is powered on
    touch plugged in the ethernet cable
    touch next step
    Wait Until Page Contains Element    ${Input_Authorization_Code}    timeout=60
    Input Text    ${Input_Authorization_Code}    ${master_code_value}
    touch Enter
    Wait Until Page Contains Element    ${successful_info}    timeout=60
    Page Should Contain Text    &quot;${device_name}&quot; has been added to your account. Now, you can control it.
    Click Element    ${successful_info}
    wait main screen

[User 2]Use another email to bind the device
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    touch sign out
    wait sign out web
    Clear Text    ${username}
    Input Text    ${username}    ${g_app_email}
    Input Text    ${password}    ${g_app_password}
    touch sign in
    wait main screen

Enable performance function
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    touch Performance Control
    Check the original Performance status
    Click Element    ${performance_control_switch}
    Wait Until Page Contains Element    ${performance_control_switch}    timeout=30
    Check the Enable Performance status

Check the original Performance status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${original_performance_status}    Get Element Attribute    ${performance_control_switch}    checked
    log    ${original_performance_status}
    set test variable    ${original_performance_status}    ${original_performance_status}

Check the Enable Performance status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${Enable_performance_status}    Get Element Attribute    ${performance_control_switch}    checked
    log    ${Enable_performance_status}
    Should Not Contain    ${Enable_performance_status}    ${original_performance_status}
    set test variable    ${Enable_performance_status}    ${Enable_performance_status}

Login the user 1 account
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch left
    touch left
    touch account menu
    touch sign out
    wait sign out web
    Clear Text    ${username}
    Input Text    ${username}    ${second_username}
    Input Text    ${password}    ${second_password}
    touch sign in
    wait main screen

[User 1]Launch main screen > Dashboard > Delete AP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    Swipe To Up
    touch Remove DropAP
    Wait Until Page Contains Element    ${remove_info}    timeout=60
    touch Remove OK button
    Wait Until Page Contains Element    ${Bind_the_Existing_DropAP_Router_btn_slave}    timeout=20

Try to login the 2 accounts and check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    touch sign out
    wait sign out web
    Clear Text    ${username}
    Input Text    ${username}    ${g_app_email}
    Input Text    ${password}    ${g_app_password}
    touch sign in
    wait main screen
    touch Device Settings
    touch Performance Control
    Check the seconnd user Enable Performance status

Check the seconnd user Enable Performance status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${seconnd_Enable_performance_status}    Get Element Attribute    ${performance_control_switch}    checked
    log    ${seconnd_Enable_performance_status}
    Should Contain    ${seconnd_Enable_performance_status}    ${Enable_performance_status}
    Click Element    ${performance_control_switch}
    Wait Until Page Contains Element    ${performance_control_switch}    timeout=30
*** comment ***
2017-12-29 Gavin_Chang
1. Move second account to parameter.
2. Add Get device name info.
3. Correct the judgment about del second account.


2017-12-26    Leo_Li
Init the script