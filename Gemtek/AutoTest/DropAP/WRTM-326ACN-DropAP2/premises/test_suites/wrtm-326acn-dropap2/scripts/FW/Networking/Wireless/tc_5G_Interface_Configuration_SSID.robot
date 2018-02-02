*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***
${ssid_test1}    abcdefghijklmnopqrstuvwxyz123
${ssid_test2}    ~!@#$%^&*()_+{}|:" <>?-=[]\;`

*** Test Cases ***
tc_5G_Interface_Configuration_SSID
    [Documentation]  tc_5G_Interface_Configuration_SSID
    ...    1. Setting the SSID filed with 32 characters by all of the ASCII characters
    ...    2. Verify wireless client can associate to DUT or not.
    ...    3. Setting ths SSID filed with ~!@#$%^&*()_+{}|:" <>?-=[]\;`,./
    ...    4. Verify wireless client can associate to DUT or not again
    [Tags]   @TCID=WRTM-326ACN-406    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Setting the SSID filed with 32 characters by all of the ASCII characters
    Verify wireless client can associate to DUT or not
    Setting ths SSID filed with ~!@#$%^&*()_+{}|:" <>?-=[]\;`,./
    Verify wireless client can associate to DUT or not again

*** Keywords ***
Setting the SSID filed with 32 characters by all of the ASCII characters
    [Documentation]  Setting the SSID filed with 32 characters by all of the ASCII characters
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless
    Config Wireless Home Network    web    ${ssid_test1}

Verify wireless client can associate to DUT or not
    [Documentation]  Verify wireless client can associate to DUT or not
    [Tags]   @AUTHOR=Hans_Sun
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${ssid_test1}-5G    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Setting ths SSID filed with ~!@#$%^&*()_+{}|:" <>?-=[]\;`,./
    [Documentation]  Setting ths SSID filed with ~!@#$%^&*()_+{}|:" <>?-=[]\;',./
    [Tags]   @AUTHOR=Hans_Sun
    Config Wireless Home Network    web    ${ssid_test2}

Verify wireless client can associate to DUT or not again
    [Documentation]  Verify wireless client can associate to DUT or not
    [Tags]   @AUTHOR=Hans_Sun
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${ssid_test2}-5G    ${DEVICES.wifi_client.int}    ${g_dut_gw}

*** comment ***
2017-11-08     Hans_Sun
Init the script
