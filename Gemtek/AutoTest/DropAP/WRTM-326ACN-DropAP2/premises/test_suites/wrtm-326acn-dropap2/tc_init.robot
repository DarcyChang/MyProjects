*** Settings ***

Resource      base.robot

Force Tags    @FEATURE=    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_init
    [Documentation]    Check web page have authorization code or not
    [Tags]    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Check web page have authorization code and setup button or not

*** Keywords ***
Check web page have authorization code and setup button or not
    delete all cookies    web
    open browser    web
    go to page    web    ${g_dut_gui_url}
    ${r1}    run keyword and return status    cpe click    web    ${Link_Configure_DropAP}
    run keyword if    '${r1}'=='True'    no operation
    ...    ELSE    Check web page show authorization code or setup button


Check web page show authorization code or setup button
    ${r2}    run keyword and return status    cpe click    web    ${Link_Setup_DropAP}
    run keyword if    '${r2}'=='True'    run keywords    go to page    web    ${g_dut_gui_url}
    ...    AND    Wait Until Element Is Visible    web    ${Link_Setup_DropAP}
    ...    AND    Config Setup DropAP
    ...    ELSE    run keywords    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    ...    AND    cli    dut1    restore_default    timeout=20
    ...    AND    sleep    120
    ...    AND    go to page    web    ${g_dut_gui_url}
    ...    AND    Wait Until Element Is Visible    web    ${Link_Setup_DropAP}
    ...    AND    Config Setup DropAP

*** comment ***
2017-11-09     Hans_Sun
Init the script
