*** Settings ***
Resource   base.robot



Test Setup   Login Web GUI
Test Teardown  Restore To Previous State
Force Tags  @FEATURE=Web_GUI    @AUTHOR=Johnny_Peng

*** Test Cases ***
tc_Wireless_Home Network_Hidden SSID
    [Documentation]   tc_Wireless_Home Network_Hidden SSID
    ...    1. Go to Networking/Wireless page
    ...    2. Click on Hidden SSID checkbox
    ...    3. Refresh page and verify Hidden SSID check box is checked.


    [Tags]   @TCID=WRTM-326ACN-178    @DUT=WRTM-326ACN     @AUTHOR=Johnny_Peng    config_test     config_wireless
    [Timeout]
    Go to Networking/Wireless page
    Click on Hidden SSID checkbox
    Refresh page and verify Hidden SSID check box is checked.



*** Keywords ***
Go to Networking/Wireless page
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Open Newworking Wireless Page

Click on Hidden SSID checkbox
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
#    kw_Wireless.Backup Current Checkbox Hidden SSID State
    kw_Wireless.Set Hidden SSID Checkbox to Checked

Refresh page and verify Hidden SSID check box is checked.
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Refresh Networking Wireless Page
    kw_Wireless.Verify Hidden SSID Checkbox is Checked

Restore To Previous State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Reset To Default Checkbox Hidden SSID State

*** comment ***
2017-10-16     Johnny_Peng
Init the script