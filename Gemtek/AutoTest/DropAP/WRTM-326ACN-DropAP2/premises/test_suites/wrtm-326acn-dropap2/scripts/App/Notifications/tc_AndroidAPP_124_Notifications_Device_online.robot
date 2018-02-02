*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=Notifications    @AUTHOR=Leo_Li

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_124_Notifications_Device_online
    [Documentation]  tc_AndroidAPP_124_Notifications_Device_online
    ...    1. launch the DropAP and go to main page.
    ...    2. Check the notifications.
    [Tags]   @TCID=WRTM-326ACN-380    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    launch the DropAP and go to main page
    Check the notifications

*** Keywords ***
launch the DropAP and go to main page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch App
    Sign In

Check the notifications
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait main screen
    verify notifications info num

*** comment ***
2017-12-12    Leo_Li
Init the script