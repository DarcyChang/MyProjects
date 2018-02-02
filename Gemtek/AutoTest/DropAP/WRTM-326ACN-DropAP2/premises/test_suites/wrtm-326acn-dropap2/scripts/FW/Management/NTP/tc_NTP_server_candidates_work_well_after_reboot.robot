*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=NTP    @AUTHOR=Jujung_Chang
Test teardown    Reset NTP Candidates
*** Variables ***
${Dummy_Candidate_Name_0}    0.openwrt.pool.ntp.org1
${Dummy_Candidate_Name_2}    2.openwrt.pool.ntp.org1
${Dummy_Candidate_Name_3}    3.openwrt.pool.ntp.org1
${Candidate_Name_0}    0.openwrt.pool.ntp.org
${Candidate_Name_1}    1.openwrt.pool.ntp.org
${Candidate_Name_2}    2.openwrt.pool.ntp.org
${Candidate_Name_3}    3.openwrt.pool.ntp.org

*** Test Cases ***
tc_NTP_server_candidates_work_well_after_reboot
    [Documentation]  tc_NTP_server_candidates_work_well_after_reboot
    ...    1. To setting secondary NTP server on the GUI.
    ...    2. Modified first NTP server is fake.
    ...    3. Reboot the DUT
    ...    4. Verify the time will be updated correctly using secondary NTP server.

    [Tags]   @TCID=WRTM-326ACN-266    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    To setting secondary NTP server on the GUI
    Modified NTP server is fake except the secondary
    Reboot the DUT
    Verify the time will be updated correctly using secondary NTP server

*** Keywords ***
To setting secondary NTP server on the GUI
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Login Web GUI
    Config DHCP Client

    Go to web page Device Management>System and Beneath System Properties
    Modify NTP Candidate Name    1    ${Candidate_Name_1}

Modified NTP server is fake except the secondary
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Modify NTP Candidate Name    0    ${Dummy_Candidate_Name_0}
    Modify NTP Candidate Name    2    ${Dummy_Candidate_Name_2}
    Modify NTP Candidate Name    3    ${Dummy_Candidate_Name_3}

Reboot the DUT
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Click Reboot Button And Verify Function Is Work
    Login Web GUI

Verify the time will be updated correctly using secondary NTP server
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Go to web page Device Management>System and Beneath System Properties
    ${realtime_before_push_syn_brower} =  Get Real Time
    sleep     10s
    Click SYNC WITH BROWSER Button
    ${realtime_after_push_syn_brower} =  Get Real Time
    Should Not Be Equal    ${realtime_before_push_syn_brower}    ${realtime_after_push_syn_brower}

    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management
    Checking NTP packets When Modified NTP Server On GUI

Go to web page Device Management>System and Beneath System Properties
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Get Real Time
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result} =   Get Element text    web    ${Text_time}
    log    ${result}
    [Return]    ${result}

Click SYNC WITH BROWSER Button
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cpe click    web    ${Button_SYNC}
    #wait sync up time for GUI
    sleep    5

Reset NTP Candidates
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Modify NTP Candidate Name    0    ${Candidate_Name_0}
    Modify NTP Candidate Name    2    ${Candidate_Name_2}
    Modify NTP Candidate Name    3    ${Candidate_Name_3}

*** comment ***
2017-12-08     Jujung_Chang
Init the script
