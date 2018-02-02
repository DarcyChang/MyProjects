*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_Reboot
    [Documentation]  tc_Reboot
    ...    1. Go to DeviceManager Reboot/Reset page
    ...    2. Click Perform Reboot and wait for loading page is finished and return to homepage
    [Tags]   @TCID=WRTM-326ACN-174    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to DeviceManager Reboot/Reset page
    Click Perform Reboot and wait for loading page is finished and return to homepage

*** Keywords ***
Go to DeviceManager Reboot/Reset page
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI

Click Perform Reboot and wait for loading page is finished and return to homepage
    [Documentation]  Click Reboot Button And Verify Function Is Work
    [Tags]   @AUTHOR=Hans_Sun
    Click Reboot Button And Verify Function Is Work

*** comment ***
2017-10-11     Hans_Sun
Init the script
