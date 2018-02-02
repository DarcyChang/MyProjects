*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Jamie_Chang    norun

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown  Run keywords    Exit Shell Mode

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${count_eth1_on}    0
${count_eth1_off}    0
${count_eth2_on}    0
${count_eth2_off}    0
${count_eth3_on}    0
${count_eth3_off}    0
${count_eth4_on}    0
${count_eth4_off}    0
${times}    50


*** Test Cases ***
test_Ethernet_1_4_Flashing_Green_Activity_Device_Connected_and_Traffic
    [Documentation]    test_Ethernet_1_4_Flashing_Green_Activity_Device_Connected_and_Traffic
    ...    Verify if the Ethernet LED stay in Flashing Green state when Device is connected.
    ...    1. Connect LAN port Ethernet 1-4 of device and start a data traffic.
    ...    2. LAN port Ethernet 1-4 LED must be in a Flashing Green Activity state.
    [Tags]    @TCID=PREMS-TC-7897    @globalid=1597620LED844F    @DUT=844FB    @DUT=844F897    @AUTHOR=Gemtek_Jamie_Chang
    [Timeout]
    #Set LAN port1 Powered UP. LAN port2-4 Powered DOWN
    ${resulteth11} =    cli    n1    ethctl eth0 phy-power down
    ${resulteth11} =    cli    n1    ethctl eth0 phy-power up
    log    ${resulteth11}
    ${resulteth12} =    cli    n1    ethctl eth1 phy-power down
    log    ${resulteth12}
    ${resulteth13} =    cli    n1    ethctl eth2 phy-power down
    log    ${resulteth13}
    ${resulteth14} =    cli    n1    ethctl eth3 phy-power down
    log    ${resulteth14}
    #Check LAN port1 is flashing. LAN port1 LED Register Value 10 bit are not all 0
    ${result1}    ${result2} =    Get Eth0_LED_Flashing Register Value    n1    ${times}
    Should not Be Equal    ${result1}    0
    Should not Be Equal    ${result2}    0
    #Clean up set LAN port1-4 Powered UP.
    ${resulteth11} =    cli    n1    ethctl eth0 phy-power up
    log    ${resulteth11}
    ${resulteth12} =    cli    n1    ethctl eth1 phy-power up
    log    ${resulteth12}
    ${resulteth13} =    cli    n1    ethctl eth2 phy-power up
    log    ${resulteth13}
    ${resulteth14} =    cli    n1    ethctl eth3 phy-power up
    log    ${resulteth14}

    #Set LAN port2 Powered UP. LAN port1 and port3-4 Powered DOWN
    ${resulteth21} =    cli    n1    ethctl eth0 phy-power down
    log    ${resulteth21}
    ${resulteth21} =    cli    n1    ethctl eth1 phy-power down
    ${resulteth22} =    cli    n1    ethctl eth1 phy-power up
    log    ${resulteth22}
    ${resulteth23} =    cli    n1    ethctl eth2 phy-power down
    log    ${resulteth23}
    ${resulteth24} =    cli    n1    ethctl eth3 phy-power down
    log    ${resulteth24}
    #Check LAN port2 is flashing. LAN port2 LED Register Value 11 bit are not all 0
    ${result3}    ${result4} =    Get Eth1_LED_Flashing Register Value    n1    ${times}
    Should not Be Equal    ${result3}    0
    Should not Be Equal    ${result4}    0
    #Clean up set LAN port1-4 Powered UP.
    ${resulteth21} =    cli    n1    ethctl eth0 phy-power up
    log    ${resulteth21}
    ${resulteth22} =    cli    n1    ethctl eth1 phy-power up
    log    ${resulteth22}
    ${resulteth23} =    cli    n1    ethctl eth2 phy-power up
    log    ${resulteth23}
    ${resulteth24} =    cli    n1    ethctl eth3 phy-power up
    log    ${resulteth24}

    #Set LAN port3 Powered UP. LAN port1-2 and port4 Powered DOWN
    ${resulteth31} =    cli    n1    ethctl eth0 phy-power down
    log    ${resulteth31}
    ${resulteth32} =    cli    n1    ethctl eth1 phy-power down
    log    ${resulteth32}
    ${resulteth33} =    cli    n1    ethctl eth2 phy-power down
    ${resulteth33} =    cli    n1    ethctl eth2 phy-power up
    log    ${resulteth33}
    ${resulteth34} =    cli    n1    ethctl eth3 phy-power down
    log    ${resulteth34}
    #Check LAN port3 is flashing. LAN port3 LED Register Value 12 bit are not all 0
    ${result5}    ${result6} =    Get Eth2_LED_Flashing Register Value    n1    ${times}
    Should not Be Equal    ${result5}    0
    Should not Be Equal    ${result6}    0
    #Clean up set LAN port1-4 Powered UP.
    ${resulteth31} =    cli    n1    ethctl eth0 phy-power up
    log    ${resulteth31}
    ${resulteth32} =    cli    n1    ethctl eth1 phy-power up
    log    ${resulteth32}
    ${resulteth33} =    cli    n1    ethctl eth2 phy-power up
    log    ${resulteth33}
    ${resulteth34} =    cli    n1    ethctl eth3 phy-power up
    log    ${resulteth34}

    #Set LAN port4 Powered UP. LAN port1-3 Powered DOWN
    ${resulteth41} =    cli    n1    ethctl eth0 phy-power down
    log    ${resulteth41}
    ${resulteth42} =    cli    n1    ethctl eth1 phy-power down
    log    ${resulteth42}
    ${resulteth43} =    cli    n1    ethctl eth2 phy-power down
    log    ${resulteth43}
    ${resulteth44} =    cli    n1    ethctl eth3 phy-power down
    ${resulteth44} =    cli    n1    ethctl eth3 phy-power up
    log    ${resulteth44}
    #Check LAN port4 is flashing. LAN port4 LED Register Value 13 bit are not all 0
    ${result7}    ${result8} =    Get Eth3_LED_Flashing Register Value    n1    ${times}
    Should not Be Equal    ${result7}    0
    Should not Be Equal    ${result8}    0
    #Clean up set LAN port1-4 Powered UP.
    ${resulteth41} =    cli    n1    ethctl eth0 phy-power up
    log    ${resulteth41}
    ${resulteth42} =    cli    n1    ethctl eth1 phy-power up
    log    ${resulteth42}
    ${resulteth43} =    cli    n1    ethctl eth2 phy-power up
    log    ${resulteth43}
    ${resulteth44} =    cli    n1    ethctl eth3 phy-power up
    log    ${resulteth44}


*** Keywords ***

Get Eth0_LED_Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]    Check Eth1_LED_on Register Value 10 bit is 0
    [Tags]    @AUTHOR=Gemtek_Jamie_Chang

    :FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List    ${register_value_list}    0
    \    ...    ELSE    Set Variable    false_default_str
    \    log    ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 1 0111 1110 1010 1110 1011
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w([\\w{1}])    1
    \    ${ret} =    Get From List    ${ret_list}    0
    \    ${count_eth1_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth1_on} + 1
        ...    ELSE    Set Variable    ${count_eth1_on}
    \    ${count_eth1_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth1_off} + 1
        ...    ELSE    Set Variable    ${count_eth1_off}
    [Return]    ${count_eth1_on}    ${count_eth1_off}

Get Eth1_LED_Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]    Check Eth2_LED_on Register Value 11 bit is 0
    [Tags]    @AUTHOR=Gemtek_Jamie_Chang

    :FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List    ${register_value_list}    0
    \    ...    ELSE    Set Variable    false_default_str
    \    log    ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 1 0111 1110 1010 1110 0011
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    \    ${ret} =    Get From List    ${ret_list}    0
    \    ${count_eth2_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth2_on} + 1
        ...    ELSE    Set Variable    ${count_eth2_on}
    \    ${count_eth2_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth2_off} + 1
        ...    ELSE    Set Variable    ${count_eth2_off}
    [Return]    ${count_eth2_on}    ${count_eth2_off}

Get Eth2_LED_Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]    Check Eth3_LED_on Register Value 12 bit is 0
    [Tags]    @AUTHOR=Gemtek_Jamie_Chang

    :FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List    ${register_value_list}    0
    \    ...    ELSE    Set Variable    false_default_str
    \    log    ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 1 0111 1110 1010 1110
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    \    ${ret} =    Get From List    ${ret_list}    0
    \    ${count_eth3_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth3_on} + 1
        ...    ELSE    Set Variable    ${count_eth3_on}
    \    ${count_eth3_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth3_off} + 1
        ...    ELSE    Set Variable    ${count_eth3_off}
    [Return]    ${count_eth3_on}    ${count_eth3_off}

Get Eth3_LED_Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]    Check Eth4_LED_on Register Value 13 bit is 0
    [Tags]    @AUTHOR=Gemtek_Jamie_Chang

    :FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})    1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    \    ...    ELSE    Set Variable    false_default_str
    \    log    ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4    #something like 1 0111 1110 1010 1100
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{2}([\\w{1}])    1
    \    ${ret} =    Get From List    ${ret_list}    0
    \    ${count_eth4_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_eth4_on} + 1
       ...    ELSE    Set Variable    ${count_eth4_on}
    \    ${count_eth4_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_eth4_off} + 1
        ...    ELSE    Set Variable    ${count_eth4_off}
    [Return]    ${count_eth4_on}    ${count_eth4_off}

Enter Shell Mode
    [Arguments]
    [Documentation]    Enter shell mode
    [Tags]    @AUTHOR=Gemtek_Jamie_Chang

    Wait Until Keyword Succeeds    3x   10 sec    cli    n1    sh

Exit Shell Mode
    [Arguments]
    [Documentation]     Exit CPE shell mode
    [Tags]    @AUTHOR=Gemtek_Jamie_Chang

    cli    n1    exit

