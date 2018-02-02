*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Jujung_Chang    norun

Suite Setup    Run keywords    Enter Shell Mode And Cisco Prejob Config
Suite Teardown  Run keywords    Exit Shell Mode And Cisco
*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${count_eth_on}    0
${count_eth_off}    0
${times}    20

*** Test Cases ***
tc_Verify_Ethernet_1_4_Off
   [Documentation]    tc_Verify_ethernet_1_4_off
   ...    We use cisco router to enable and disable ethernet port.
   ...    Fisrt, we shutdown ethernet port by cisco router, then we check LED registers and interface status.
   ...    Second, we open ethernet port by cisco router, then we check again.
   ...    Third, we shutdown ethernet port by cisco router, then we check again.
   [Tags]   @TCID=PREMS-TC-7895   @globalid=1597618LED844F    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Jujung_Chang
   [Timeout]

   #shutdown fastethernet 5-7
   cli    cisco    config t    dhcpv6\\(config\\)#
   cli    cisco    interface range fastEthernet 5-7    dhcpv6\\(config-if-range\\)#
   cli    cisco    sh    dhcpv6\\(config-if-range\\)#

   #check interface status
   ${ret}    cli    cisco    do show ip int brief FastEthernet5    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    administratively down
   ${ret}    cli    cisco    do show ip int brief FastEthernet6    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    administratively down
   ${ret}    cli    cisco    do show ip int brief FastEthernet7    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    administratively down
   #check registers value
   Wait Until Keyword Succeeds    3x    10 sec    Check Ethernet LED Register Should be Off

   #no shutdown fastethernet 5-7
   cli    cisco    interface range fastEthernet 5-7    dhcpv6\\(config-if-range\\)#
   cli    cisco    no sh    dhcpv6\\(config-if-range\\)#

   #check interface status
   ${ret}    cli    cisco    do show ip int brief FastEthernet5    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    up
   ${ret}    cli    cisco    do show ip int brief FastEthernet6    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    up
   ${ret}    cli    cisco    do show ip int brief FastEthernet7    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    up

   #check registers value and check LED solid bright
   ${result} =   Wait Until Keyword Succeeds    5x   1 sec    Check Eth1 LED On in Certain Tries    n1
   log    ${result}
   Should Be Equal     ${result}    0
   ${result} =   Wait Until Keyword Succeeds    5x   1 sec    Check Eth2 LED On in Certain Tries    n1
   log    ${result}
   Should Be Equal     ${result}    0
   ${result} =   Wait Until Keyword Succeeds    5x   1 sec    Check Eth3 LED On in Certain Tries    n1
   log    ${result}
   Should Be Equal     ${result}    0

   #check LED  is flashing
   ${result_on} =    Wait Until Keyword Succeeds    5x   1 sec    Check Eth1 LED flashing in Certain Tries    n1    ${times}
   Should not Be Equal    ${result_on}    0
   ${result_on} =    Wait Until Keyword Succeeds    5x   1 sec    Check Eth2 LED flashing in Certain Tries    n1    ${times}
   Should not Be Equal    ${result_on}    0
   ${result_on} =    Wait Until Keyword Succeeds    5x   1 sec    Check Eth3 LED flashing in Certain Tries    n1    ${times}
   Should not Be Equal    ${result_on}    0

   #shutdown fastethernet 5-7
   cli    cisco    interface range fastEthernet 5-7    dhcpv6\\(config-if-range\\)#
   cli    cisco    sh    dhcpv6\\(config-if-range\\)#

   #check interface status
   ${ret}    cli    cisco    do show ip int brief FastEthernet5    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    administratively down
   ${ret}    cli    cisco    do show ip int brief FastEthernet6    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    administratively down
   ${ret}    cli    cisco    do show ip int brief FastEthernet7    dhcpv6\\(config-if-range\\)#
   log   ${ret}
   Should Contain    ${ret}    administratively down
   #check registers value
   Wait Until Keyword Succeeds    3x   10 sec    Check Ethernet LED Register Should be Off


*** Keywords ***
Check Eth1 LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 17cac3ee  => should retrive third hex: 3->0011, bit 10 is 0
    ...                when green off Register Value is 17cac7ee  => should retrive third hex: 7->0111, bit 10 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Eth1 LED Register Value   ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Check Eth2 LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 17cac7ee  => should retrive third hex: 7->0111, bit 11 is 0
    ...                when green off Register Value is 17cacfee  => should retrive third hex: f->1111, bit 11 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Eth2 LED Register Value   ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Check Eth3 LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 17cac3ee  => should retrive third hex: c->1100, bit 12 is 0
    ...                when green off Register Value is 17cad3ee  => should retrive third hex: d->1101, bit 12 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Eth3 LED Register Value   ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Check Ethernet LED Register Should be Off
    [Arguments]
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Get Eth1 LED Register Value    n1
    log    ${result}
    Should Be Equal    ${result}    1

    ${result} =   Get Eth2 LED Register Value    n1
    log    ${result}
    Should Be Equal    ${result}    1

    ${result} =   Get Eth3 LED Register Value    n1
    log    ${result}
    Should Be Equal    ${result}   1

Get Eth1 LED Register Value
    [Arguments]    ${device}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    #bit 11    0xFFFE8114 : 17eaebea  => should retrive second hex: b->1011, bit 11 is 1
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List    ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log    ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 1 0111 1110 1010 1110 1011
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w([\\w{1}])    1
    ${ret} =    Get From List    ${ret_list}    0

    log to console    ${ret}
    [Return]    ${ret}

Get Eth2 LED Register Value
    [Arguments]    ${device}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    #bit 11    0xFFFE8114 : 17eaebea  => should retrive second hex: b->1011, bit 11 is 1
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List    ${register_value_list}    0
    ...    ELSE    Set Varible    false_default_str
    log    ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 1 0111 1110 1010 1110 1011
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    ${ret} =    Get From List    ${ret_list}    0

    log to console    ${ret}
    [Return]    ${ret}

Get Eth3 LED Register Value
    [Arguments]    ${device}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    #bit 12   0xFFFE8114 : 17eaf3ea   => should retrive second hex: f-> 1111  ,bit 12 is 1
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})    1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List    ${register_value_list}    0
    ...    ELSE    Set Varible    false_default_str
    log    ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4    #something like 1 0111 1110 1010 111 1
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    ${ret} =    Get From List    ${ret_list}    0

    log to console    ${ret}
    [Return]    ${ret}

Check Eth1 LED flashing in Certain Tries
    [Arguments]    ${device}    ${times}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result_on}    ${result_off} =    Wait Until Keyword Succeeds    5x    3s    Get Eth1 flashing Register Value    ${device}    ${times}
    log    ${result_on}
    log    ${result_off}
    Should not Be Equal    ${result_on}    0
    [Return]    ${result_on}

Check Eth2 LED flashing in Certain Tries
    [Arguments]    ${device}    ${times}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result_on}    ${result_off} =    Wait Until Keyword Succeeds    5x    3s    Get Eth2 flashing Register Value   ${device}    ${times}
    log    ${result_on}
    log    ${result_off}
    Should not Be Equal    ${result_on}    0
    [Return]    ${result_on}

Check Eth3 LED flashing in Certain Tries
    [Arguments]    ${device}    ${times}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result_on}    ${result_off} =    Wait Until Keyword Succeeds    5x    3s    Get Eth3 flashing Register Value   ${device}    ${times}
    log    ${result_on}
    log    ${result_off}
    Should not Be Equal    ${result_on}    0
    [Return]    ${result_on}

Get Eth1 flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check ETH_flashing Register Value 10/11/12 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_eth_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth_on} + 1
        ...    ELSE    Set Variable    ${count_eth_on}
    \    log    ${count_eth_on}
    \    ${count_eth_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth_off} + 1
        ...    ELSE    Set Variable    ${count_eth_off}
    [Return]    ${count_eth_on}    ${count_eth_off}

Get Eth2 flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check ETH_flashing Register Value 10/11/12 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_eth_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth_on} + 1
        ...    ELSE    Set Variable    ${count_eth_on}
    \    ${count_eth_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth_off} + 1
        ...    ELSE    Set Variable    ${count_eth_off}
    [Return]    ${count_eth_on}    ${count_eth_off}

Get Eth3 flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check ETH_flashing Register Value 10/11/12 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})    1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_eth_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth_on} + 1
        ...    ELSE    Set Variable    ${count_eth_on}
    \    ${count_eth_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth_off} + 1
        ...    ELSE    Set Variable    ${count_eth_off}
    [Return]    ${count_eth_on}    ${count_eth_off}

Enter Shell Mode And Cisco Prejob Config
    [Arguments]
    [Documentation]    Enter shell mode and cisco prejob config
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    Wait Until Keyword Succeeds    3x   10 sec    cli    n1    sh
    #cisco prejob config
    Wait Until Keyword Succeeds    3x   10 sec    cli    cisco    enable    dhcpv6#
    cli    cisco    terminal length 0    dhcpv6#
    cli    cisco    config t    dhcpv6\\(config\\)#
    cli    cisco    no logging console    dhcpv6\\(config\\)#
    cli    cisco    line console 0    dhcpv6\\(config-line\\)#
    cli    cisco    no exec-timeout    dhcpv6\\(config-line\\)#
    cli    cisco    exit    dhcpv6\\(config\\)#

Exit Shell Mode And Cisco
    [Arguments]
    [Documentation]    Exit CPE shell mode and cisco privilege mode
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    cli    n1    exit
    #no shutdown fastethernet 5-7
    cli    cisco    interface range fastEthernet 5-7    dhcpv6\\(config-if-range\\)#
    cli    cisco    no sh    dhcpv6\\(config-if-range\\)#
    cli    cisco    exit    dhcpv6\\(config\\)#
    cli    cisco    exit    dhcpv6#

