*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=GFAST    @AUTHOR=Gemtek_Hans_Sun    stable

Suite Setup    Run keywords    Enter Cli Mode
*** Variables ***
${Reboot_waiting_time}    150
${Bonding_line1}    line3
${Bonding_line2}    line4

*** Test Cases ***
tc_Monitor_GFAST_link_status_cold_reboot_844F
    [Documentation]   tc_Monitor_GFAST_link_status_cold_reboot_844F
    ...    1.Use apc to do the cold reboot
    ...    2.Use e5 to check GFAST bonding line is down or up
    ...    3.Check DUT web page of GFAST status
    [Tags]    @TCID=STP_DD-TC-11684    @globalid=1662608    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]
    #Use APC to do the cold reboot
    cli    apc    1    #Choose 1- Device Manager
    cli    apc    3    #Choose 3- Outlet Control/Configuration
    cli    apc    2    #Choose 2- Hans_CPE
    cli    apc    1    #Choose 1- Control Outlet
    cli    apc    3    #Choose 3- Immediate Reboot
    cli    apc    yes    to continue    #Enter 'YES' to continue, and 'to continue' is prompt
    #Check GFAST bonding line is up
    Wait Until Keyword Succeeds    10x    10s    Check Bonding Line Up    ${Bonding_line1}
    Wait Until Keyword Succeeds    10x    5s    Check Bonding Line Up    ${Bonding_line2}
    #Waiting reboot times for web gui
    sleep    ${Reboot_waiting_time}
    #Check web gui GFAST status
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Keyword Succeeds    5x    3s    click links    web    G.fast
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='image_table']    3    2    Active
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='image_table']    4    2    Active

*** Keywords ***
Enter Cli Mode
    [Arguments]
    [Documentation]    Go to cli mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    e5    cli

Check Bonding Line Up
    [Arguments]    ${Bonding_line}
    [Documentation]    To check bonding line status is showtime or init-hs
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   cli    e5    show interface line summary | include ${Bonding_line}
    Should Contain    ${result}    showtime

Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}
