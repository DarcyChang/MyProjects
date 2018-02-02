*** Settings ***
Resource    base.robot


Force Tags    @FEATURE=Web_GUI    @AUTHOR=Jujung_Chang

*** Variables ***

*** Test Cases ***
tc_Verify_mobile_android_app_download_website_link
    [Documentation]  tc_Verify_mobile_android_app_download_website_link
    ...    1. Link to DropAP2 Website 192.168.66.1
    ...    2. Checking Google Play Image Can Link to Google Play website
    [Tags]   @TCID=WRTM-326ACN-290    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Link to DropAP2 Website 192.168.66.1
    Checking Google Play Image Can Link to Google Play website

*** Keywords ***
Link to DropAP2 Website 192.168.66.1
    [Documentation]  Login Web GUI
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    cpe logout    web    ${Menu_Logout}

Checking Google Play Image Can Link to Google Play website
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Verify Google Play Link


*** comment ***
2017-11-07    Jujung_Chang
Modified Checking image button way using get element attribute.

2017-10-30     Jujung_Chang
Init the script
