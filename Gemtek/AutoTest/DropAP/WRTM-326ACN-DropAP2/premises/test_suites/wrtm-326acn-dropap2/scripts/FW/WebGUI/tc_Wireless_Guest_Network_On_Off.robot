*** Settings ***
Resource   base.robot




Test Setup   Login Web GUI
Test Teardown  Restore Guest Network Radio To Default
Force Tags    @FEATURE=Web_GUI    @AUTHOR=Johnny_Peng


*** Test Cases ***
tc_Wireless_Guest Network_On_Off
    [Documentation]   tc_Wireless_Home Network_Hidden SSID
    ...    1. Go to Networking/Wireless_Guest Network page
    ...    2. Select Guest Network is selected on
    ...    3. Refresh page and verify guest network is selected on.


    [Tags]   @TCID=WRTM-326ACN-179    @DUT=WRTM-326ACN     @AUTHOR=Johnny_Peng     config_test     config_wireless
    [Timeout]
    Go to Networking/Wireless_Guest Network page
    Select Guest Network is selected on
    Refresh page and verify guest network is selected on


*** Keywords ***
Go to Networking/Wireless_Guest Network page
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Open Newworking Wireless Page

Select Guest Network is selected on
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Set Guest Network Radio State   on

Refresh page and verify guest network is selected on
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Main_Menu.Refresh Networking Wireless Page
    kw_Wireless.Verify Guest Network Radio Is on or off   on

Restore Guest Network Radio To Default
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    kw_Wireless.Set Guest Network Radio State   off

*** comment ***
2017-10-16     Johnny_Peng
Init the script