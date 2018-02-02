*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=WebGUI    @AUTHOR=thomas_chen    norun

*** Variables ***

${844fb_dump_led_register}     dw fffe8114


*** Test Cases ***
tc_Verify_demo_cli_cisco_demo
   [Documentation]    tc_Verify_demo_cli_cisco_demo
   ...    To demostrate the usage of CLI automation
   [Tags]   @DUT=844FB  @DUT=844F
   [Timeout]
   cli    cisco    enable
   cli    cisco    terminal length 0
   cli    cisco    config t    dhcpv6\\(config\\)#
   cli    cisco    no logging console    dhcpv6\\(config\\)#
   cli    cisco    line console 0    dhcpv6\\(config-line\\)#
   cli    cisco    no exec-timeout    dhcpv6\\(config-line\\)#
   cli    cisco    exit    dhcpv6\\(config\\)#
   #shutdown fastethernet 5-7
   cli    cisco    config t    dhcpv6\\(config\\)#
   cli    cisco    interface range fastEthernet 5-7    dhcpv6\\(config-if-range\\)#
   cli    cisco    sh    dhcpv6\\(config-if-range\\)#
   #sleep 5 seconds for interface to come down
   sleep    5
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
   #no shutdown fastethernet 5-7
   cli    cisco    interface range fastEthernet 5-7    dhcpv6\\(config-if-range\\)#
   cli    cisco    no sh    dhcpv6\\(config-if-range\\)#
   #sleep 5 seconds for interface to come up
   sleep    5
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
   cli    cisco    exit    dhcpv6\\(config\\)#
   cli    cisco    exit


*** comment ***






