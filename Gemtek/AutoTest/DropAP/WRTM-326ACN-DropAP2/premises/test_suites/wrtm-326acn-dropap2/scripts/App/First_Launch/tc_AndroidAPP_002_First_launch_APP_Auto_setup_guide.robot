*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=First_Launch    @AUTHOR=Leo_Li

Test Teardown      Close APP

*** Variables ***
${Ethernet_connect_title}    Plug Ethernet Cable
${Wi_Fi_connect_title}    Please Connect to Your DropAP
${connect_success_title}    Congratulations

*** Test Cases ***
tc_AndroidAPP_002_First_launch_APP_Auto_setup_guide
    [Documentation]  tc_AndroidAPP_002_First_launch_APP_Auto_setup_guide
    ...    1. Launch the app.
    ...    2. Login the DropAP account.
    ...    3. Go to Setup Guide 1, then press OK, I’ve Powered DropAP On.
    ...    4. Go to Setup Guide 2, Ensure your Ethernet cable connect to DropAP AP wan port.
    ...    5. Press OK, I’ve Plugged in the Ethernet Cable.
    ...    6. Go to Setup Guide 3, Ensure your mobile connect to DropAP SSID.
    ...    7. Press Next button.
    ...    8. Wait for Device setup, and show Congratulation Page.
    [Tags]   @TCID=WRTM-326ACN-199    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app
    Login the DropAP account
    Go to Setup Guide 1, then press OK, I’ve Powered DropAP On
    Go to Setup Guide 2, Ensure your Ethernet cable connect to DropAP AP wan port
    Press OK, I’ve Plugged in the Ethernet Cable
    Go to Setup Guide 3, Ensure your mobile connect to DropAP SSID
    Press Next button
    Wait for Device setup, and show Congratulation Page

*** Keywords ***
Launch the app
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Login the DropAP account
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Sign In
    wait main screen
    touch account menu
    touch add dropap

Go to Setup Guide 1, then press OK, I’ve Powered DropAP On
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${DropAP_is_powered_on}

Go to Setup Guide 2, Ensure your Ethernet cable connect to DropAP AP wan port
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Text    ${Ethernet_connect_title}

Press OK, I’ve Plugged in the Ethernet Cable
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${plugged_in_the_ethernet_cable}

Go to Setup Guide 3, Ensure your mobile connect to DropAP SSID
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Text    ${Wi_Fi_connect_title}

Press Next button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${next_step}

Wait for Device setup, and show Congratulation Page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait until page contains element    ${OK_btn}    timeout=60
    Page Should Contain Text    ${connect_success_title}
    Click Element    ${OK_btn}
    wait main screen


*** comment ***
2017-12-18 Gavin_Chang
1. Remove Reset to default due to duplicate case

2017-12-12    Leo_Li
Init the script
