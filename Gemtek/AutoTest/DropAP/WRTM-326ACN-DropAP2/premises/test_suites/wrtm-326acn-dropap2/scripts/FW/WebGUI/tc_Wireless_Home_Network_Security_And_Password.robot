*** Settings ***
Resource   base.robot


Test Setup   Login Web GUI
Test Teardown  Restore To Previous State
Force Tags  @FEATURE=Web_GUI    @AUTHOR=Johnny_Peng

*** Test Cases ***
tc_Wireless_Home Network_Security_And_Password
    [Documentation]   tc_Wireless_Home Network_Security_And_Password
    ...    1. Go to Networking/Wireless Page
    ...    2. Change 2.4g wifi and 5g wifi Security/Password and save setting
    ...    3. Refresh page and verify Security/Password is changed accordingly.


    [Tags]   @TCID=WRTM-326ACN-177    @DUT=WRTM-326ACN     @AUTHOR=Johnny_Peng    config_test     config_wireless
    [Timeout]
    Go to Networking/Wireless Page
    Change 2.4g wifi and 5g wifi Security/Password and save setting
    Refresh Page and verify Security/Password is changed accordingly


*** Keywords ***
Go to Networking/Wireless Page
    [Documentation]    Go to target gui page
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Open Newworking Wireless Page

Change 2.4g wifi and 5g wifi Security/Password and save setting
    [Documentation]    backup current state and set security and password value
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Backup Current Security And Password State
    kw_Wireless.Set Security And Password   WEP    qwert

Refresh Page and verify Security/Password is changed accordingly
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Refresh Networking Wireless Page
    kw_Wireless.Verify Security And Password Were Set   WEP    qwert

Restore To Previous State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Restore To Previous Security State

*** comment ***
2017-10-16     Johnny_Peng
Init the script
