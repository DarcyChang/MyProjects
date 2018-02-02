*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${getIP}
*** Test Cases ***
tc_Static_mode_Setting_and_Connection
    [Documentation]  tc_Static_mode_Setting_and_Connection
    ...  1. Go to WAN setting page, setting the DUT with Static mode.
    ...  2. Setting of WAN IP address, Mask, default gateway and DNS information to WAN interface [Down by step1.]
    ...  3. To connect WAN interface to router or ISP.  [Hardware Setup]
    ...  4. Move on Settings page, Verify WAN Port IP information.
    ...  5. Verify IP information on the console (command: ifstatus wan).
    ...  6. Verify LAN-PCs and smart mobile devices can access Internet when WAN interface connect to ISP.
    [Tags]   @TCID=WRTM-326ACN-358    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [teardown]  Restore Networking Configuration

    Go to WAN setting page, setting the DUT with Static mode
    Move on Settings page, Verify WAN Port IP information
    Verify IP information on the console (command: ifstatus wan)
    Verify LAN-PCs and smart mobile devices can access Internet when WAN interface connect to ISP

*** Keywords ***
Go to WAN setting page, setting the DUT with Static mode
    [Documentation]  Go to WAN setting page, setting the DUT with Static mode
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config Static Client
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts

Move on Settings page, Verify WAN Port IP information
    [Documentation]  Move on Settings page, Verify WAN Port IP information
    [Tags]   @AUTHOR=Jujung_Chang
    ${getIP} =  Check Address on the IPv4 WAN Status Table Is Valid    web

Verify IP information on the console (command: ifstatus wan)
    [Documentation]  Verify IP information on the console (command: ifstatus wan)
    [Tags]   @AUTHOR=Jujung_Chang

    ${r} =    Wait Until Keyword Succeeds    10x    3s      cli    dut1    ifstatus wan | grep address
    should contain    ${r}    ${getIP}

Verify LAN-PCs and smart mobile devices can access Internet when WAN interface connect to ISP
    [Documentation]  Verify LAN-PCs and smart mobile devices can access Internet when WAN interface connect to ISP
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Config DHCP Client

*** comment ***
2017-12-18     Jujung_Chang
Move "cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts" on first keyword.
2017-11-16     Jujung_Chang
Init the script
