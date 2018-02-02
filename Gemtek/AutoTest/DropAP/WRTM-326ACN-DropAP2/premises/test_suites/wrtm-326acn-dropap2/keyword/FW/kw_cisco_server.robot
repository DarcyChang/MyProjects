*** Settings ***

*** Variables ***

*** Keywords ***
Change PPPoE Server Authentication On Cisco Server
    [Arguments]    ${SecurityType}
    [Documentation]    Security type is support pap,chap and both.
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    cli    ${DEVICES.cisco.vendor}    interface ${DEVICES.cisco.ppoe_interface}
    run keyword if  '${SecurityType}' == 'both'    cli    ${DEVICES.cisco.vendor}    ppp authentication pap chap
    ...   ELSE IF  '${SecurityType}' == 'chap'    cli    ${DEVICES.cisco.vendor}    ppp authentication chap
    ...   ELSE IF  '${SecurityType}' == 'pap'    cli    ${DEVICES.cisco.vendor}    ppp authentication pap
    ...   ELSE    log    No ${SecurityType} supported.
    cli    ${DEVICES.cisco.vendor}    end

Adding Default DNS Setting On Cisco Server
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    #Enter dhcp pool setting
    cli    ${DEVICES.cisco.vendor}    ip dhcp pool ${DEVICES.cisco.dhcp_pool_name}
    cli    ${DEVICES.cisco.vendor}    dns-server ${g_dut_DNS_from_company} ${DEVICES.cisco.gateway}
    cli    ${DEVICES.cisco.vendor}    end

Adding Fake DNS Setting On Cisco Server
    [Arguments]    ${fake_dns}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    #Enter dhcp pool setting
    cli    ${DEVICES.cisco.vendor}    ip dhcp pool ${DEVICES.cisco.dhcp_pool_name}
    cli    ${DEVICES.cisco.vendor}    dns-server ${fake_dns}
    cli    ${DEVICES.cisco.vendor}    end

Setting LAB DNS Only on Cisco Server
    [Arguments]    ${DEVICES.cisco.gateway}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    #Enter dhcp pool setting
    cli    ${DEVICES.cisco.vendor}    ip dhcp pool ${DEVICES.cisco.dhcp_pool_name}
    cli    ${DEVICES.cisco.vendor}    no dns-server
    cli    ${DEVICES.cisco.vendor}    dns-server ${DEVICES.cisco.gateway}
    cli    ${DEVICES.cisco.vendor}    end

Setting Company DNS Only on Cisco Server
    [Arguments]    ${g_dut_DNS_from_company}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    #Enter dhcp pool setting
    cli    ${DEVICES.cisco.vendor}    ip dhcp pool ${DEVICES.cisco.dhcp_pool_name}
    cli    ${DEVICES.cisco.vendor}    no dns-server
    cli    ${DEVICES.cisco.vendor}    dns-server ${g_dut_DNS_from_company}
    cli    ${DEVICES.cisco.vendor}    end

Remove DNS Setting On Cisco Server
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    #Enter dhcp pool setting
    cli    ${DEVICES.cisco.vendor}    ip dhcp pool ${DEVICES.cisco.dhcp_pool_name}
    cli    ${DEVICES.cisco.vendor}    no dns-server ${g_dut_DNS_from_company} ${DEVICES.cisco.gateway}
    cli    ${DEVICES.cisco.vendor}    end

Setting DHCP Server Lease Time
    [Arguments]    ${time}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    #Enter dhcp pool setting
    cli    ${DEVICES.cisco.vendor}    ip dhcp pool ${DEVICES.cisco.dhcp_pool_name}
    #Setting lease time
    run keyword if    ${time} == 60    cli    ${DEVICES.cisco.vendor}    lease 0 0 1
    run keyword if    ${time} == 3600    cli    ${DEVICES.cisco.vendor}    lease 0 1 0
    cli    ${DEVICES.cisco.vendor}    end

Disable DHCP Server
    [Documentation]  disable DHCP server by shutdown port.
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    cli    ${DEVICES.cisco.vendor}    interface ${DEVICES.cisco.ethernet_port_number}
    cli    ${DEVICES.cisco.vendor}    shutdown
    cli    ${DEVICES.cisco.vendor}    end

Enable DHCP Server
    [Documentation]  enable DHCP server by no shutdown port.
    [Tags]   @AUTHOR=Jujung_Chang
    [Timeout]    20

    #cisco prejob config
    cli    ${DEVICES.cisco.vendor}    \r\n
    #To avoid error mode situation.
    cli    ${DEVICES.cisco.vendor}    config t
    cli    ${DEVICES.cisco.vendor}    end

    cli    ${DEVICES.cisco.vendor}    config t    ${DEVICES.cisco.hostname}\\(config\\)#
    cli    ${DEVICES.cisco.vendor}    interface ${DEVICES.cisco.ethernet_port_number}
    cli    ${DEVICES.cisco.vendor}    no shutdown
    cli    ${DEVICES.cisco.vendor}    end