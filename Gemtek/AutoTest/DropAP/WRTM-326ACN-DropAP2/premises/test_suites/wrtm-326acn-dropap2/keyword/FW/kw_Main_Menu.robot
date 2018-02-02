*** Settings ***
Resource      ./base.robot


*** Variables ***
${Link_Configure_DropAP} =      xpath=/html/body/section/div[1]/div/a[2]
${Menu_Status} =       xpath=/html/body/div/div[2]/ul/li[1]/a
${Menu_Networking} =     xpath=/html/body/div/div[2]/ul/li[2]/a
${Link_Wireless} =      xpath=/html/body/div/div[2]/ul/li[2]/ul/li[3]/a
${Menu_Device_Management} =    xpath=/html/body/div/div[2]/ul/li[3]/a
${Link_Setup_DropAP} =      xpath=//*[@id="btn-setup"]
${Menu_Logout} =       xpath=/html/body/div/div[2]/ul/li[4]/a
${AppstoreImage_Link} =      xpath=//html/body/section/div[2]/div/a[1]
${AppstoreURL} =    https://itunes.apple.com/app/id1024442276
${GooglePlayImage_Link} =      xpath=/html/body/section/div[2]/div/a[2]
${GooglePlayURL} =    https://play.google.com/store/apps/details?id=com.dropap.dropap


*** Keywords ***


Open Newworking Wireless Page
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Wait Until Keyword Succeeds    10x    1s    click links    web     Networking    Wireless


Refresh Networking Wireless Page
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Wait Until Keyword Succeeds    10x    1s    click links    web    Wireless

Verify App Store Link
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    wait_until_element_is_visible     web    ${AppstoreImage_Link}
    ${ret}=    Get Element Attribute    web    ${AppstoreImage_Link}@href
    log    ${ret}
    Should be equal    ${ret}    ${AppstoreURL}

Verify Google Play Link
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    wait_until_element_is_visible     web    ${GooglePlayImage_Link}
    ${ret}=    Get Element Attribute    web    ${GooglePlayImage_Link}@href
    log    ${ret}
    Should be equal    ${ret}    ${GooglePlayURL}

*** comment ***
2017-10-30    Jujung_Chang
Adding keyword: Click App Store Link
Adding keyword: Click Google Play Link

2017-10-18  Johnny_Peng
add key word:Refresh Networking Wireless Page

2017-10-16     Johnny_Peng
Init the script
