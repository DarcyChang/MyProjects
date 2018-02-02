*** Settings ***
Resource   base.robot


Test Setup   Login Web GUI
Test Teardown  Restore To Previous State


Force Tags    @FEATURE=Web_GUI    @AUTHOR=Johnny_Peng

*** Test Cases ***
tc_Wireless_Guest_Network_Modify_SSID
    [Documentation]   tc_Wireless_Home Network_Hidden SSID
    ...    1. Go to Networking/Wireless_Guest Network page
    ...    2. Select Guest Network On and Change Guest Network SSID and save setting
    ...    3. Refresh page and verify Guest Network SSID is changed accordingly


    [Tags]   @TCID=WRTM-326ACN-172    @DUT=WRTM-326ACN     @AUTHOR=Johnny_Peng     config_test     config_wireless
    [Timeout]

    Go to Networking/Wireless_Guest Network page
    Select Guest Network On and Change Guest Network SSID and save setting
    Refresh page and verify Guest Network SSID is changed accordingly


*** Keywords ***
Go to Networking/Wireless_Guest Network page
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Open Newworking Wireless Page


Select Guest Network On and Change Guest Network SSID and save setting
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Backup Current Guest Network SSID
    kw_Wireless.Turn On Guest Network and Set Guest Network SSID  TEST_GUEST_NETWORK_SSID

Refresh page and verify Guest Network SSID is changed accordingly
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Refresh Networking Wireless Page
    kw_Wireless.Verify Guest Network SSID Value   TEST_GUEST_NETWORK_SSID

Restore To Previous State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Set Guest Network Radio State   off
    kw_Wireless.Restore Guest Network SSID

*** comment ***
2017-10-16     Johnny_Peng
Init the script