*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_DHCP_mode_DHCP_Server_without_DNS_setting
    [Documentation]  tc_DHCP_mode_DHCP_Server_without_DNS_setting
    ...   1. Cisco Router configures DHCP server and DHCP Server without DNS server IP setting.
    ...   2. DUT WAN uses DHCP mode connect to Cisco Router.
    ...   3. LAN PC set DNS Server IP manually.  [Down.It's LAN PC default setting.]
    ...   4. Verify LAN PC can not access Internet and DUT without any wrong message.
    ...   5. Setting one non-exist DNS Server IP on Cisco Router.
    ...   6. Verify LAN PC can not access Internet and DUT without any wrong message.
    [Tags]   @TCID=WRTM-326ACN-351    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [teardown]    Restore Networking Configuration

    Cisco Router configures DHCP server and DHCP Server without DNS server IP setting
    DUT WAN uses DHCP mode connect to Cisco Router
    Verify LAN PC can not access Internet and DUT without any wrong message
    Setting one non-exist DNS Server IP on Cisco Router
    Verify LAN PC can not access Internet and DUT without any wrong message

*** Keywords ***
Cisco Router configures DHCP server and DHCP Server without DNS server IP setting
    [Documentation]  Cisco Router configures DHCP server and DHCP Server without DNS server IP setting
    [Tags]   @AUTHOR=Jujung_Chang
    Remove DNS Setting On Cisco Server

DUT WAN uses DHCP mode connect to Cisco Router
    [Documentation]  DUT WAN uses DHCP mode connect to Cisco Router
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client

Verify LAN PC can not access Internet and DUT without any wrong message
    [Documentation]  Verify LAN PC can access Internet (e.g. http://www.google.com) and DUT without any wrong message
    [Tags]   @AUTHOR=Jujung_Chang
    cli   lanhost   echo '${DEVICES.lanhost.password}' | sudo -S sed -i '1i nameserver ${gui_url}' /etc/resolv.conf
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping URL Fail    lanhost    ${DEVICES.wanhost.Domain_Name_URL}

Setting one non-exist DNS Server IP on Cisco Router
    [Documentation]  Setting one non-exist DNS Server IP on Cisco Router
    [Tags]   @AUTHOR=Jujung_Chang
    Adding Fake DNS Setting On Cisco Server    ${g_dut_static_ipaddr}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Adding Default DNS Setting On Cisco Server
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sed -i '/nameserver ${gui_url}/d' /etc/resolv.conf

*** comment ***
2017-12-04     Jujung_Chang
Modified Adding Default DNS Setting On Cisco Server keyword
2017-11-17     Jujung_Chang
Init the script
