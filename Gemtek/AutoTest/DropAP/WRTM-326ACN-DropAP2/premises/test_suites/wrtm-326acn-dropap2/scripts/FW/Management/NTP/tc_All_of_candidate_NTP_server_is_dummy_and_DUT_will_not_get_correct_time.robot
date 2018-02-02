*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=NTP    @AUTHOR=Jujung_Chang
Test teardown    Reset NTP Candidates
*** Variables ***
${Dummy_Candidate_Name_0}    0.openwrt.pool.ntp.org1
${Dummy_Candidate_Name_1}    1.openwrt.pool.ntp.org1
${Dummy_Candidate_Name_2}    2.openwrt.pool.ntp.org1
${Dummy_Candidate_Name_3}    3.openwrt.pool.ntp.org1
${Candidate_Name_0}    0.openwrt.pool.ntp.org
${Candidate_Name_1}    1.openwrt.pool.ntp.org
${Candidate_Name_2}    2.openwrt.pool.ntp.org
${Candidate_Name_3}    3.openwrt.pool.ntp.org

*** Test Cases ***
tc_All_of_candidate_NTP_server_is_dummy_and_DUT_will_not_get_correct_time
    [Documentation]  tc_All_of_candidate_NTP_server_is_dummy_and_DUT_will_not_get_correct_time
    ...    1. Modified all of candidate is dummy.
    ...    2. Change the time.
    ...    3. Verify NTP clients should not update the time with NTP server.

    [Tags]   @TCID=WRTM-326ACN-270    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Modified all of candidate is dummy
    Change the time
    Verify NTP clients should not update the time with NTP server

*** Keywords ***
Modified all of candidate is dummy
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Login Web GUI
    Config DHCP Client

    Go to web page Device Management>System and Beneath System Properties
    Modify NTP Candidate Name    0    ${Dummy_Candidate_Name_0}
    Modify NTP Candidate Name    1    ${Dummy_Candidate_Name_1}
    Modify NTP Candidate Name    2    ${Dummy_Candidate_Name_2}
    Modify NTP Candidate Name    3    ${Dummy_Candidate_Name_3}

Change the time
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Click SYNC WITH BROWSER Button

Verify NTP clients should not update the time with NTP server
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Checking NTP packets When Modified NTP Server On GUI Is Failed

Go to web page Device Management>System and Beneath System Properties
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

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
    Modify NTP Candidate Name    1    ${Candidate_Name_1}
    Modify NTP Candidate Name    2    ${Candidate_Name_2}
    Modify NTP Candidate Name    3    ${Candidate_Name_3}

*** comment ***
2017-12-08     Jujung_Chang
Init the script
