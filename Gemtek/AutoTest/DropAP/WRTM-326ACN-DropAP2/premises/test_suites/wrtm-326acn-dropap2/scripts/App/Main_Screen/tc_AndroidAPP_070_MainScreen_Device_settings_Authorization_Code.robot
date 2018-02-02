*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_070_MainScreen_Device_settings_Authorization_Code
    [Documentation]  tc_AndroidAPP_070_MainScreen_Device_settings_Authorization_Code
    ...    1. Launch the DropAP app into main screen.
    ...    2. Press device settings button.
    ...    3. Press Authorization.
    ...    4. Check the Authorization code.
    ...    5. Check the status.
    [Tags]   @TCID=WRTM-326ACN-252    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Press device settings button
    Press Authorization
    Check the Authorization code
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen
    Check device name

Check device name
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${device_name}    Get Text    ${main_screen_device_name}
    log    ${device_name}
    set test variable    ${device_name}    ${device_name}

Press device settings button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings

Press Authorization
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Authorization Code

Check the Authorization code
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${master_code}
    ${master_code_value}    Get Text    ${master_code}
    log    ${master_code_value}
    set test variable    ${master_code_value}    ${master_code_value}
    Page Should Contain Text    ${master_code_value}

Check the status
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
    touch Device Settings
    Page Should Not Contain Element    ${authorization_code}
    Restore Device status

Restore Device status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Remove DropAP
    Wait Until Page Contains Element    ${remove_info}    timeout=20
    touch Remove OK button
    Wait Until Page Contains Element    ${add_a_DropAP}    timeout=20


*** comment ***
2018-01-02 Gavin_Chang
1. Move second account to parameters.
2. Teardown only when test case pass.

2017-12-19    Leo_Li
Init the script