*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=GFAST    @AUTHOR=Gemtek_Hans_Sun    stable

Suite Setup    Run keywords    Enter Cli Mode

*** Variables ***
${image}     /home/vagrant/CALIX_844F_12.1.0.92.bin    #Used normal Calix image.
${Upload_waiting_time}    120
${Bonding_line1}    line3
${Bonding_line2}    line4

*** Test Cases ***
tc_Monitor_GFAST_link_status_upgrade_844F
    [Documentation]    tc_Monitor_GFAST_link_status_upgrade_844F
    ...    1.Login DUT upgrade image web page
    ...    2.Choose the latest Calix image, and execute upgrate firmware
    ...    3.Use e5 to check GFAST bonding line is down or up
    ...    4.Check DUT web page of GFAST status
    [Tags]    @TCID=STP_DD-TC-11689    @globalid=1662613    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Firmware Upgrade by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Firmware Upgrade
    Wait Until Keyword Succeeds    5x    3s    click links    web    Upgrade Image

    #execute upload image java script to show file upload dialog
    execute javascript    web    document.getElementById("fileUploadFrameObjId").style.display='block'
    select_frame    web    id=fileUploadFrameObjId
    choose file   web    id=fileObjectID    ${image}
    unselect_frame    web
    cpe click    web   id=upgrade_button

    #Check GFAST bonding line is down
    Wait Until Keyword Succeeds    15x    10s    Check Bonding Line Down    ${Bonding_line1}
    Wait Until Keyword Succeeds    10x    5s    Check Bonding Line Down    ${Bonding_line2}
    #Check GFAST bonding line is up
    Wait Until Keyword Succeeds    10x    10s    Check Bonding Line Up    ${Bonding_line1}
    Wait Until Keyword Succeeds    10x    5s    Check Bonding Line Up    ${Bonding_line2}

    Wait Until Element Is Not Visible    web    xpath=//button[contains(., 'Upgrade')]    ${Upload_waiting_time}    #After upload and reboot finish, web page upgrade button will disappear.
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Keyword Succeeds    5x    3s    click links    web    G.fast
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='image_table']    3    2    Active
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='image_table']    4    2    Active

*** Keywords ***
Enter Cli Mode
    [Arguments]
    [Documentation]    Enter shell mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    e5    cli

Check Bonding Line Up
    [Arguments]    ${Bonding_line}
    [Documentation]    To check bonding line status is showtime or init-hs
    [Tags]    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   cli    e5    show interface line summary | include ${Bonding_line}
    Should Contain    ${result}    showtime

Check Bonding Line Down
    [Arguments]    ${Bonding_line}
    [Documentation]    To check bonding line status is showtime or init-hs
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   cli    e5    show interface line summary | include ${Bonding_line}
    Should Not Contain    ${result}    showtime

Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}
*** comment ***