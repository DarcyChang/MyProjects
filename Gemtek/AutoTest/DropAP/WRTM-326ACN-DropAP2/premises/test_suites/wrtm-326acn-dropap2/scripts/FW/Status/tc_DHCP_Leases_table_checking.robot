*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Status    @AUTHOR=Jujung_Chang

*** Variables ***

*** Test Cases ***
tc_DHCP_Leases_table_checking
    [Documentation]  tc_DHCP_Leases_table_checking
    ...    1. Connect PC to LAN of DUT. [Hardware setup]
    ...    2. DUT setup DHCP mode.
    ...    3. Verify the DHCP clients should be display on DHCP leases.
    ...    4. Using sudo dhclient -r eth2 to release client IP.
    ...    5. Verify DUT can't Show lease IP address By GUI.

    [Tags]   @TCID=WRTM-326ACN-326    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    DUT setup DHCP mode
    Verify the DHCP clients should be display on DHCP leases
    LAN Host Release DHCP from DUT Using dhclient Command
    Using sudo dhclient -r eth2 to release client IP
    Verify DUT Can Not Show Lease IP Address By GUI


*** Keywords ***
DUT setup DHCP mode
    [Documentation]  DUT setup DHCP mode
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Verify DHCP Wan Type

Verify the DHCP clients should be display on DHCP leases
    [Documentation]  Verify the DHCP clients should be display on DHCP leases
    [Tags]   @AUTHOR=Jujung_Chang

    LAN Host Request DHCP from DUT

LAN Host Release DHCP from DUT Using dhclient Command
    [Documentation]  LAN Host Release DHCP from DUT Using dhclient Command
    [Tags]   @AUTHOR=Jujung_Chang
    Verify DHCP Leases Information    ${DEVICES.lanhost.hostname}

Using sudo dhclient -r eth2 to release client IP
    [Documentation]  Using sudo dhclient -r eth2 to release client IP
    [Tags]   @AUTHOR=Jujung_Chang
    LAN Host Release DHCP from DUT

Verify DUT Can Not Show Lease IP Address By GUI
    [Documentation]  After Release DHCP IP, Verify DUT Can Not Show Lease IP Address By GUI
    [Tags]   @AUTHOR=Jujung_Chang
    After Release DHCP IP, Verify DUT Can Not Show Lease IP Address By GUI    web    ${DEVICES.lanhost.hostname}

*** comment ***
2017-11-10     Jujung_Chang
Init the script
