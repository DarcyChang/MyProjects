*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***
${upgrade_message}    There is no new version for your device.


*** Test Cases ***
tc_AndroidAPP_099_MainScreen_Device_Settings_Upgrade
    [Documentation]  tc_AndroidAPP_099_MainScreen_Device_Settings_Upgrade
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Upgrade
    ...    3. Check the status
    [Tags]   @TCID=WRTM-326ACN-425    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Upgrade
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Upgrade
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Upgrade

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify upgrade pop message


*** comment ***
2017-11-21    Gavin_Chang
Init the script
