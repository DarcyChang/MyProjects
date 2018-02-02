*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_Static_mode_The_Second_DNS_Server
    [Documentation]  tc_Static_mode_The_Second_DNS_Server
    ...   1. Setting static mode on DUT, to Connect WAN interface to router or ISP.
    ...   2. DUT set the two DNS servers.
    ...   3. Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 1st DNS).
    [Tags]   @TCID=WRTM-326ACN-362    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [teardown]    Restore Networking Configuration
    Setting static mode on DUT, to Connect WAN interface to router or ISP
    DUT set the two DNS servers
    Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 1st DNS)

*** Keywords ***
Setting static mode on DUT, to Connect WAN interface to router or ISP
    [Documentation]  Setting static mode on DUT, to Connect WAN interface to router or ISP
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config Static Client

DUT set the two DNS servers
    [Documentation]  DUT connect to WAN host and setting DUT is DHCP mode.
    [Tags]   @AUTHOR=Jujung_Chang
    Adding DNS Candidate At GUI    ${gui_url}

Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 1st DNS)
    [Documentation]  Verify LAN-PCs and smart mobile devices can access Internet (e.g. http://www.google.com) (using the 1st DNS)
    [Tags]   @AUTHOR=Jujung_Chang
    [timeout]  30s
    cli   lanhost   echo '${DEVICES.lanhost.password}' | sudo -S sed -i '1i nameserver ${gui_url}' /etc/resolv.conf
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.Domain_Name_URL}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Config DHCP Client
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sed -i '/nameserver ${gui_url}/d' /etc/resolv.conf

*** comment ***
2017-11-17     Jujung_Chang
Init the script
