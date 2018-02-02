*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_Internet_Connection_Static_IP
    [Documentation]  tc_Internet_Connection_Static_IP
    ...    1. Go To WebUI Networking/Internet Connection page
    ...    2. Configure Protocol Static IP/Subnet Mask/Gateway/DNS Server
    ...    3. Verify Static IP configuration is configured correct on status page
    [Tags]   @TCID=WRTM-326ACN-170    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go To WebUI Networking/Internet Connection
    Configure Protocol Static IP/Subnet Mask/Gateway/DNS Server
    Verify Static IP configuration is configured correct on status page

*** Keywords ***
Go To WebUI Networking/Internet Connection
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI

Configure Protocol Static IP/Subnet Mask/Gateway/DNS Server
    [Documentation]  Config Static Client
    [Tags]   @AUTHOR=Hans_Sun
    Config Static Client

Verify Static IP configuration is configured correct on status page
    [Documentation]  Verify Static Wan Type and IP
    [Tags]   @AUTHOR=Hans_Sun
    Verify Static Wan Type

*** comment ***
2017-10-17     Hans_Sun
Init the script
