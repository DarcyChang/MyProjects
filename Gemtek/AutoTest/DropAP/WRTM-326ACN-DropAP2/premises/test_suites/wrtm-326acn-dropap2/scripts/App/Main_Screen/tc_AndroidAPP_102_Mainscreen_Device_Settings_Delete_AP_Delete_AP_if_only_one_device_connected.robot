*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_102_Mainscreen_Device_Settings_Delete_AP_Delete_AP_if_only_one_device_connected
    [Documentation]  tc_AndroidAPP_102_Mainscreen_Device_Settings_Delete_AP_Delete_AP_if_only_one_device_connected
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Remove AP.
    ...    3. Press OK button to check confirm dialog.
    ...    4. Re-login again and check the status.
    [Tags]   @TCID=WRTM-326ACN-423    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Remove AP
    Press OK button to check confirm dialog
    Re login again and check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Remove AP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    Swipe To Up
    touch Remove DropAP

Press OK button to check confirm dialog
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${remove_info}    timeout=60
    touch Remove OK button

Re login again and check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${Bind_the_Existing_DropAP_Router_btn_master}    timeout=20
    Click Element    ${Bind_the_Existing_DropAP_Router_btn_master}
    Wait Until Page Contains Element    ${OK_btn}    timeout=10
    Click Element    ${OK_btn}
    wait main screen

*** comment ***
2017-12-12    Leo_Li
Init the script