*** Settings ***
Resource   base.robot

Test Setup   Login Web GUI
Test Teardown  Restore ssid to previous state
Force Tags  @FEATURE=Web_GUI    @AUTHOR=Johnny_Peng

*** Test Cases ***
tc_Wireless_Home_Network_Modify_SSID
    [Documentation]   tc_Wireless_Home_Network_Modify_SSID
    ...    1. Go to Networking/Wireless page
    ...    2. Change 2.4 wifi, 5g wifi SSID and Save setting
    ...    3. Refresh page and verify SSID is changed accordingly.

    [Tags]   @TCID=WRTM-326ACN-176    @DUT=WRTM-326ACN     @AUTHOR=Johnny_Peng    config_test     config_wireless
    [Timeout]
    Go to Networking/Wireless page
    Change 2.4g wifi, 5g wifi SSID and Save Setting
    Refresh page and verify SSID is changed accordingly

*** Keywords ***
Go to Networking/Wireless page
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Open Newworking Wireless Page

Change 2.4g wifi, 5g wifi SSID and Save Setting
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Backup Previous SSID Value
    kw_Wireless.Set SSID Value      SSID_SET_TEST_1

Refresh page and verify SSID is changed accordingly
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Refresh Networking Wireless Page
    kw_Wireless.Verify SSID Value    SSID_SET_TEST_1

Restore ssid to previous state
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Restore To Previous SSID Value

*** comment ***
2017-10-16     Johnny_Peng
Init the script