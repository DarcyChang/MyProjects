*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***
${times}    10

*** Test Cases ***
tc_Test_Logout
    [Documentation]  tc_Test_Logout
    ...    1. Go to DropAP2 Website 192.168.66.1 Front Page and click "Configure DropAP" button to Main Page
    ...    2. Click Logout Button on main menu
    ...    3. Verify the page can return to front page, page should contains "Configure DropAP" button
    ...    4. Repeat 10 times for Step 1.~ Step3. Verify is work well.
    [Tags]   @TCID=WRTM-326ACN-348    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to DropAP2 Website 192.168.66.1 Front Page and click "Configure DropAP" button to Main Page
    Click Logout Button on main menu
    Verify the page can return to front page, page should contains "Configure DropAP" button
    Repeat 10 times for Step 1.~ Step3. Verify is work well

*** Keywords ***
Go to DropAP2 Website 192.168.66.1 Front Page and click "Configure DropAP" button to Main Page
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI

Click Logout Button on main menu
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cpe logout    web    ${Menu_Logout}

Verify the page can return to front page, page should contains "Configure DropAP" button
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    page should contain element    web    ${Link_Configure_DropAP}

Repeat 10 times for Step 1.~ Step3. Verify is work well
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    : FOR    ${INDEX}    IN RANGE    0    ${times}
    \    Go to DropAP2 Website 192.168.66.1 Front Page and click "Configure DropAP" button to Main Page
    \    Click Logout Button on main menu
    \    Verify the page can return to front page, page should contains "Configure DropAP" button

*** comment ***
2017-11-02     Hans_Sun
Init the script
