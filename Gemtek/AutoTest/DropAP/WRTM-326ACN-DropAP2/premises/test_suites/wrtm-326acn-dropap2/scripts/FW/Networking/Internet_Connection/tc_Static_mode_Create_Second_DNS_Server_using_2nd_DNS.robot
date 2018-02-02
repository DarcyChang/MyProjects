*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${dummy_dns1}    172.18.19.10
*** Test Cases ***
tc_Static_mode_Create_Second_DNS_Server_using_2nd_DNS
    [Documentation]  tc_Static_mode_Create_Second_DNS_Server_using_2nd_DNS
    ...   1. Setting static mode on DUT, to Connect WAN interface to router or ISP and Setting the 1st DNS is fake.
    ...   2. DUT set the two DNS servers.
    ...   3. Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 2nd DNS).
    [Tags]   @TCID=WRTM-326ACN-396    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [teardown]    Restore Networking Configuration
    Setting static mode on DUT, to Connect WAN interface to router or ISP
    DUT set the second DNS servers
    Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 2nd DNS)

*** Keywords ***
Setting static mode on DUT, to Connect WAN interface to router or ISP
    [Documentation]  Setting static mode on DUT, to Connect WAN interface to router or ISP
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config Static Client    ${dummy_dns1}

DUT set the second DNS servers
    [Documentation]  DUT connect to WAN host and setting DUT is DHCP mode.
    [Tags]   @AUTHOR=Jujung_Chang
    Adding DNS Candidate At GUI    ${g_dut_static_dns1}

Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 2nd DNS)
    [Documentation]  Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 1st DNS)
    [Tags]   @AUTHOR=Jujung_Chang
    [timeout]  30s
    cli   lanhost   echo '${DEVICES.lanhost.password}' | sudo -S sed -i '1i nameserver ${gui_url}' /etc/resolv.conf
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.Domain_Name_URL}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking
    Config DHCP Client
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sed -i '/nameserver ${gui_url}/d' /etc/resolv.conf
    Adding Default DNS Setting On Cisco Server

*** comment ***
2017-12-04     Jujung_Chang
Modified Adding Default DNS Setting On Cisco Server keyword
Mdified Config Static Client using dummy DNS for fist DNS
Modified keyword name
2017-11-17     Jujung_Chang
Init the script
