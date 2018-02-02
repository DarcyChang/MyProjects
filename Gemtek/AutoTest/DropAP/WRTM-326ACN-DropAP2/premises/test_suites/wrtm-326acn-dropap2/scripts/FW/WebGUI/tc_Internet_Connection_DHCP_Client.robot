*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_Internet_Connection_DHCP_Client
    [Documentation]  tc_Internet_Connection_DHCP_Client
    ...    1. Go To WebUI Networking/Internet Connection
    ...    2. Select Protocol DHCP and Save setting
    ...    3. Verify protocol type is DHCP on the status page
    [Tags]   @TCID=WRTM-326ACN-171    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go To WebUI Networking/Internet Connection
    Select Protocol DHCP and Save setting
    Verify protocol type is DHCP on the status page

*** Keywords ***
Go To WebUI Networking/Internet Connection
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI

Select Protocol DHCP and Save setting
    [Documentation]  Config DHCP Client
    [Tags]   @AUTHOR=Hans_Sun
    Config DHCP Client

Verify protocol type is DHCP on the status page
    [Documentation]  Verify DHCP Wan Type
    [Tags]   @AUTHOR=Hans_Sun
    Verify DHCP Wan Type

*** comment ***
2017-10-16     Hans_Sun
Init the script
