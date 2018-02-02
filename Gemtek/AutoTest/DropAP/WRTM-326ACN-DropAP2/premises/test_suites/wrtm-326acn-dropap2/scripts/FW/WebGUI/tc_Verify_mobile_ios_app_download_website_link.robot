*** Settings ***
Resource    base.robot


Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang

*** Variables ***

*** Test Cases ***
tc_Verify_mobile_ios_app_download_website_link
    [Documentation]  tc_Verify_mobile_ios_app_download_website_link
    ...    1. Go to DropAP2 Website 192.168.66.1 Front Page
    ...    2. Click App Store website link
    [Tags]   @TCID=WRTM-326ACN-289    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to DropAP2 Website 192.168.66.1 Front Page
    Checking App Store Image Can Link to App Store website

*** Keywords ***
Go to DropAP2 Website 192.168.66.1 Front Page
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    cpe logout    web    ${Menu_Logout}

Checking App Store Image Can Link to App Store website
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Verify App Store Link

*** comment ***
2017-11-07    Jujung_Chang
Modified Checking image button way using get element attribute.

2017-10-30     Jujung_Chang
Init the script
