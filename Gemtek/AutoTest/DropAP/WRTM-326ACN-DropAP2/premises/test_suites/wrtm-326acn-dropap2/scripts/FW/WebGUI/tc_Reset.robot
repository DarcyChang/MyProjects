*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun
Suite Teardown    Run keywords    Config Setup DropAP

*** Variables ***

*** Test Cases ***
tc_Reset
    [Documentation]  tc_Reset
    ...    1. Go to DeviceManager Reboot/Reset page
    ...    2. Click Perform Reset and wait for loading page is finished and return to homepage
    [Tags]   @TCID=WRTM-326ACN-175    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]
    [setup]    Setting Company DNS Only on Cisco Server    ${g_dut_DNS_from_company}
    [teardown]    Adding Default DNS Setting On Cisco Server

    Go to DeviceManager Reboot/Reset page
    Click Perform Reset and wait for loading page is finished and return to homepage

*** Keywords ***
Go to DeviceManager Reboot/Reset page
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI

Click Perform Reset and wait for loading page is finished and return to homepage
    [Documentation]  Click Reset Button And Verify Function Is Work
    [Tags]   @AUTHOR=Hans_Sun
    Click Reset Button And Verify Function Is Work

*** comment ***
2017-12-04     Jujung_Chang
Adding setup to config Company DNS only on Cisco server.
Adding teardown to config Default DNS Setting On Cisco Server.
2017-10-11     Hans_Sun
Init the script
