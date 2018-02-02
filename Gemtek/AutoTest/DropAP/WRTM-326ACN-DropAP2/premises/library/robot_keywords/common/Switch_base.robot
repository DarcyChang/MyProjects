*** Settings ***
Documentation     Switch basic operation Library
Resource          caferobot/cafebase.robot

*** Variables ***

*** Keywords ***
Switch_set_hybrid_port_pvlan
    [Arguments]    ${switch_session}    ${port}    ${vlanid}    ${switch_type}=H3C
    [Documentation]    Set the port VLAN on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | type | Switch type,support H3C and Cisco,default is H3C|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 |${switch_type}=H3C |
    ...    | Switch_set_port_vlan | 34 | 20 |${switch_type}=CISCO |
    # create ont
    Run Keyword If    '${switch_type}'=='CISCO'    Switch_set_hybrid_port_pvlan_cisco    ${switch_session}    ${port}    ${vlanid}
    Run Keyword If    '${switch_type}'=='H3C'    Switch_set_hybrid_port_pvlan_h3c    ${switch_session}    ${port}    ${vlanid}

Switch_set_hybrid_port_pvlan_h3c
    [Arguments]    ${device}    ${port}    ${vlanid}
    [Documentation]    Set the port VLAN on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | H3C | 34 | 20 |
    ...    | Switch_set_port_vlan | Cisco | 34 | 20 | Cisco |
    # create ont
    ${str_vlanid}    Convert To String    ${vlanid}
    ${result}    Session Command    ${device}    system-view
    ${result}    Session Command    ${device}    interface GigabitEthernet 1/0/${port}
    ${result}    Session Command    ${device}    port link-type hybrid
    ${result}    Session Command    ${device}    port hybrid pvid vlan ${vlanid}
    ${result}    Session Command    ${device}    port hybrid vlan ${vlanid} untagged
    ${result}    Session Command    ${device}    quit
    ${result}    Session Command    ${device}    quit
    #sleep      5
    ${result}    Session Command    ${device}    display current-configuration interface GigabitEthernet 1/0/${port}
    #Result Should Contain    ${str_vlanid}
    Should Match Regexp    ${result}    [\\s\\S]*[\\s]${str_vlanid}[\\s][\\s\\S]*

Switch_set_hybrid_port_pvlan_cisco
    [Arguments]    ${device}    ${port}    ${vlanid}
    [Documentation]    Set the port VLAN on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | H3C | 34 | 20 |
    ...    | Switch_set_port_vlan | Cisco | 34 | 20 | Cisco |
    # create ont
    ${str_vlanid}    Convert To String    ${vlanid}
    ${result}    Session Command    ${device}    enable
    ${result}    Session Command    ${device}    ${pwd}
    ${result}    Session Command    ${device}    conf ter
    ${result}    Session Command    ${device}    int f0/${port}
    ${result}    Session Command    ${device}    switch access vlan ${vlanid}
    ${result}    Session Command    ${device}    exit
    ${result}    Session Command    ${device}    exit
    ${result}    Session Command    ${device}    show running config inter f0/${port}
    Result Should Contain    ${str_vlanid}

Switch_set_hybrid_port_untag_vlan
    [Arguments]    ${switch_session}    ${port}    ${vlanid}    ${switch_type}=H3C
    [Documentation]    Set the port untag VLAN on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | type | Switch type,support H3C and Cisco,default is H3C|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 |${switch_type}=H3C |
    ...    | Switch_set_port_vlan | 34 | 20 |${switch_type}=CISCO |
    # create ont
    Run Keyword If    '${switch_type}'=='CISCO'    Switch_set_hybrid_port_untag_cisco    ${switch_session}    ${port}    ${vlanid}
    Run Keyword If    '${switch_type}'=='H3C'    Switch_set_hybrid_port_untag_h3c    ${switch_session}    ${port}    ${vlanid}

Switch_set_hybrid_port_untag_h3c
    [Arguments]    ${device}    ${port}    ${vlanid}
    [Documentation]    Set the port VLAN untag vlan on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 | H3C |
    ...    | Switch_set_port_vlan | 34 | 20 | Cisco |
    # create ont
    ${str_vlanid}    Convert To String    ${vlanid}
    ${result}    Session Command    ${device}    system-view
    ${result}    Session Command    ${device}    interface GigabitEthernet 1/0/${port}
    ${result}    Session Command    ${device}    port link-type hybrid
    ${result}    Session Command    ${device}    port hybrid vlan ${vlanid} untagged
    ${result}    Session Command    ${device}    quit
    ${result}    Session Command    ${device}    quit
    ##sleep      5
    ${result}    Session Command    ${device}    display current-configuration interface GigabitEthernet 1/0/${port}
    Result Should Contain    ${str_vlanid}

Switch_remove_hybrid_port_untag_vlan
    [Arguments]    ${switch_session}    ${port}    ${vlanid}    ${switch_type}=H3C
    [Documentation]    Set the port untag VLAN on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | type | Switch type,support H3C and Cisco,default is H3C|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 |${switch_type}=H3C |
    ...    | Switch_set_port_vlan | 34 | 20 |${switch_type}=CISCO |
    # create ont
    Run Keyword If    '${switch_type}'=='CISCO'    Switch_remove_hybrid_port_untag_cisco    ${switch_session}    ${port}    ${vlanid}
    Run Keyword If    '${switch_type}'=='H3C'    Switch_remove_hybrid_port_untag_h3c    ${switch_session}    ${port}    ${vlanid}

Switch_remove_hybrid_port_untag_h3c
    [Arguments]    ${device}    ${port}    ${vlanid}
    [Documentation]    Set the port VLAN untag vlan on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 | H3C |
    ...    | Switch_set_port_vlan | 34 | 20 | Cisco |
    # create ont
    ${str_vlanid}    Convert To String    ${vlanid}
    ${result}    cli    ${device}    system-view
    ${result}    cli    ${device}    interface GigabitEthernet 1/0/${port}
    ${result}    Session Command    ${device}    port link-type hybrid
    ${result}    Session Command    ${device}    undo port hybrid vlan ${vlanid}
    ${result}    Session Command    ${device}    quit
    ${result}    Session Command    ${device}    quit
    #sleep      5
    ${result}    Session Command    ${device}    display current-configuration interface GigabitEthernet 1/0/${port}
    Result Should Not Contain    ${str_vlanid}

Switch_set_access_vlan_h3c
    [Arguments]    ${device}    ${port}    ${vlanid}
    [Documentation]    Set the port VLAN untag vlan on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 | H3C |
    ...    | Switch_set_port_vlan | 34 | 20 | Cisco |
    # create ont
    ${str_vlanid}    Convert To String    ${vlanid}
    ${result}    Session Command    ${device}    system-view
    ${result}    Session Command    ${device}    interface GigabitEthernet 1/0/${port}
    ${result}    Session Command    ${device}    port link-type access
    ${result}    Session Command    ${device}    port access vlan ${vlanid}
    ${result}    Session Command    ${device}    quit
    ${result}    Session Command    ${device}    quit
    ##sleep      5
    ${result}    Session Command    ${device}    display current-configuration interface GigabitEthernet 1/0/${port}
    Result Should Contain    ${str_vlanid}

Switch_set_access_vlan_cisco
    [Arguments]    ${device}    ${port}    ${vlanid}
    [Documentation]    Set the port VLAN untag vlan on Switch,return True or False
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml | |
    ...    | port | the port ID | |
    ...    | vlanid | the vlan ID need to be set|
    ...    | mode | Port mode, support access and trunk |
    ...
    ...    Example:
    ...    | Switch_set_port_vlan | 34 | 20 | H3C |
    ...    | Switch_set_port_vlan | 34 | 20 | Cisco |
    # create ont
    ${str_vlanid}    Convert To String    ${vlanid}
    ${result}    Session Command    ${device}    enable
    ${result}    Session Command    ${device}    ${pwd}
    ${result}    Session Command    ${device}    configure term
    ${result}    Session Command    ${device}    interface gigabitEthernet 0/${port}
    ${result}    Session Command    ${device}    switchport mode acess
    ${result}    Session Command    ${device}    switchport access vlan ${vlanid}
    ${result}    Session Command    ${device}    end
    ##sleep      5
    ${result}    Session Command    ${device}    show running-configuration interface gigabitEthernet 0/${port}
    Result Should Contain    ${str_vlanid}