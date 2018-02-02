*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Status    @AUTHOR=Jujung_Chang

*** Variables ***

*** Test Cases ***
tc_Verify_Network_Status_if_connection_is_work_well
    [Documentation]  tc_Verify_Network_Status_if_connection_is_work_well
    ...    1.  To prepare DHCP server(cisco) and connect DUT WAN port  [Hardware Setup]
    ...    2.  DUT will obtain IP from DHCP server(cisco)
    ...    3.  Go to Stattus-> Overview -> Network table and see the DUT WAN IP、 MASK、Gateway 、 DNS is valid
    [Tags]   @TCID=WRTM-326ACN-285    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    DUT will obtain IP from DHCP server(cisco)
    Go to Stattus-> Overview -> Network table and see the DUT WAN IP、 MASK、Gateway 、 DNS is valid

*** Keywords ***
DUT will obtain IP from DHCP server(cisco)
    [Documentation]  DUT will obtain IP from DHCP server(cisco)
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    #Verify DHCP Wan Type

Go to Stattus-> Overview -> Network table and see the DUT WAN IP、 MASK、Gateway 、 DNS is valid
    [Documentation]  Go to Stattus-> Overview -> Network table and see the DUT WAN IP、 MASK、Gateway 、 DNS is valid
    [Tags]   @AUTHOR=Jujung_Chang
    Check Address on the IPv4 WAN Status Table Is Valid    web
    Check Netmask on the IPv4 WAN Status Table Is Valid    web
    Check Gateway on the IPv4 WAN Status Table Is Valid    web
    Check DNS on the IPv4 WAN Status Table Is Valid    web

Get Real Time on Device Management>System page
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${after_time} =   Get Real Time
    log    ${after_time}
    @{after_times}  Split String  ${after_time}
    log  ${after_times}
    ${RealTime} =   Set Variable    @{after_times}[3]
    @{RealTime} =   Split String  ${RealTime}    :
    [Return]    @{RealTime}[0]

*** comment ***
2017-11-13     Jujung_Chang
Init the script
