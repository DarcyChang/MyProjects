*** Settings ***
Resource    base.robot

*** Variables ***
${Table_Wan_Type} =     xpath=/html/body/div/div[3]/div[2]/div/fieldset[3]/table/tbody/tr[1]/td[2]/table/tbody/tr/td/small/strong[1]
${Table_Wan} =     xpath=/html/body/div/div[3]/div[2]/div/fieldset[3]/table/tbody/tr[1]/td[2]/table
${Table_DHCP_LEASES}  =    xpath=//*[@id="maincontent"]/div/fieldset[4]
${Status_Overview_System_Hostname}    xpath=//*[@id="maincontent"]/div/fieldset[1]/table/tbody/tr[1]/td[2]
${Status_Overview_System_Model}    xpath=//*[@id="maincontent"]/div/fieldset[1]/table/tbody/tr[2]/td[2]
${Status_Overview_System_FirmwareVersion}    xpath=//*[@id="maincontent"]/div/fieldset[1]/table/tbody/tr[3]/td[2]
${Status_Overview_System_KernelVersion}    xpath=//*[@id="maincontent"]/div/fieldset[1]/table/tbody/tr[4]/td[2]
${Status_Overview_System_LocalTime}    xpath=//*[@id="localtime"]
${Status_Overview_System_Uptime}    xpath=//*[@id="uptime"]
${Status_Overview_System_LoadAverage}    xpath=//*[@id="loadavg"]
${Lease_status_table}    xpath=//*[@id="lease_status_table"]
${Memory_Free} =    xpath=//*[@id="memfree"]/div/div/div/small
${Memory_Total} =    xpath=//*[@id="memtotal"]/div/div/div/small
${Buffer} =    xpath=//*[@id="membuff"]/div/div/div/small
${DUTWANIPOnGUI} =    xpath=//*[@id="wan4_s"]/small/text()[2]

*** Keywords ***
DHCP client returns same IP address when LAN host renews
    [Arguments]    ${ip}
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    sleep    5s
    ${result}=    Get Element Text    web    ${Lease_status_table}
    log    ${result}
    Should Contain    ${result}    ${ip}

Get Status->Overview->System->Hostname
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element text    web    ${Status_Overview_System_Hostname}
    log    ${result}
    [Return]    ${result}

Get Status->Overview->System->Model
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =  Get Element text    web    ${Status_Overview_System_Model}
    log    ${result}
    [Return]    ${result}

Get Status->Overview->System->FirmwareVersion
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element text    web    ${Status_Overview_System_FirmwareVersion}
    log    ${result}
    [Return]    ${result}

Get Status->Overview->System->KernelVersion
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element text    web    ${Status_Overview_System_KernelVersion}
    log    ${result}
    [Return]    ${result}

Get Status->Overview->System->LocalTime
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element text    web    ${Status_Overview_System_LocalTime}
    log    ${result}
    [Return]    ${result}

Get Status->Overview->System->Uptime
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element text    web    ${Status_Overview_System_Uptime}
    log    ${result}
    [Return]    ${result}

Get Status->Overview->System->LoadAverage
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element text    web    ${Status_Overview_System_LoadAverage}
    log    ${result}
    [Return]    ${result}

Verify DHCP Wan Type
    [Arguments]
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    Wait Until Keyword Succeeds    5x    2s    Check Wan Type    web   dhcp

Verify Static Wan Type
    [Arguments]
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${result}    Wait Until Keyword Succeeds    5x    2s    Check Wan Type    web    static
    Should Contain    ${result}    ${g_dut_static_ipaddr}

Verify PPPoE Wan Type
    [Arguments]
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${result}    Wait Until Keyword Succeeds    5x    2s    Check Wan Type    web    pppoe

Check Wan Type
    [Arguments]    ${b}    ${type}
    [Documentation]
    [Tags]
    Reload Page    ${b}
    sleep    3
    ${value}    get_element_text    ${b}    ${Table_Wan}
    log    ${value}
    Should Contain    ${value}    ${type}
    [return]    ${value}

Check Address on the IPv4 WAN Status Table Is Valid
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    [return]    ${value}
    Reload Page    ${b}
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status  Overview
    sleep    2
    ${value} =  Wait Until Keyword Succeeds    5x    3s    Retry Get WAN Status    web
    log    ${value}

    ${value} =   Get Line    ${value}    1
    ${value} =   Fetch From Right    ${value}    Address:
    ${value} =   Strip String    ${value}
    @{IP} =  Split String  ${value}    .

    @{IPFromServer}    Split String  ${DEVICES.cisco.gateway}    .
    should be equal    @{IP}[0]    @{IPFromServer}[0]
    should be equal    @{IP}[1]    @{IPFromServer}[1]
    should be equal    @{IP}[2]    @{IPFromServer}[2]
    run keyword if    @{IP}[3] < 0 or @{IP}[3] > 254    Fail    The IP that show from GUI is invalid.

Retry Get WAN Status
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    [return]    ${value}
    ${value} =   get_element_text    ${b}    ${Table_Wan}
    Should Contain    ${value}    Address

Check Netmask on the IPv4 WAN Status Table Is Valid
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    Reload Page    ${b}
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status
    sleep    1
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status  Overview
    ${value} =  get_element_text    ${b}    ${Table_Wan}
    log    ${value}
    ${value} =  Get Line    ${value}    2
    ${value} =  Fetch From Right    ${value}    Netmask:
    ${value} =  Strip String    ${value}
    should be equal    ${value}    ${g_dut_ip_mask}

Check Gateway on the IPv4 WAN Status Table Is Valid
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    Reload Page    ${b}
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status
    sleep    1
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status  Overview
    ${value} =   get_element_text    ${b}    ${Table_Wan}
    log    ${value}
    ${value} =   Get Line    ${value}    3
    ${value} =   Fetch From Right    ${value}    Gateway:
    ${value} =   Strip String    ${value}
    should be equal    ${value}    ${DEVICES.cisco.gateway}

Check DNS on the IPv4 WAN Status Table Is Valid
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    Reload Page    ${b}
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status
    sleep    1
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status  Overview
    ${value} =   get_element_text    ${b}    ${Table_Wan}
    log    ${value}
    ${dns1} =   Get Line    ${value}    4
    ${dns1} =   Fetch From Right    ${dns1}    DNS 1:
    ${dns1} =   Strip String    ${dns1}
    should be equal    ${dns1}    ${g_dut_DNS_from_company}
    ${dns2} =   Get Line    ${value}    5
    ${dns2} =   Fetch From Right    ${dns2}    DNS 2:
    ${dns2} =   Strip String    ${dns2}
    should be equal    ${dns2}    ${DEVICES.cisco.gateway}

Verify DHCP Leases Information
    [Arguments]    ${hostname}
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    page should contain text    web    ${hostname}

After Release DHCP IP, Verify DUT Can Not Show Lease IP Address By GUI
    [Arguments]    ${b}    ${hostname}
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    page should not contain text    web    ${hostname}

Get DUT DHCP WAN IP
    [Tags]   @AUTHOR=Hans_Sun
    ${value}    get_element_text    web    ${Table_Wan}
    ${IP} =    Get Regexp Matches    ${value}    Address: 172.18.19.\\d+
    log    ${IP}
    Should Contain    ${IP}[0]    172.18.19
    ${IP} =    Get Regexp Matches    ${IP}[0]    \\d+.\\d+.\\d+.\\d+
    log    ${IP}[0]
    [Return]    @{IP}[0]