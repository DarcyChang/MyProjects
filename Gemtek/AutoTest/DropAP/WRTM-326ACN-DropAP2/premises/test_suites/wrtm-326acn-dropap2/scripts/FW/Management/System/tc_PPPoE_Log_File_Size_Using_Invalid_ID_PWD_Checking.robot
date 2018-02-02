*** Settings ***
Resource   base.robot

Test Setup    Clear DUT's ppp.log
Test teardown    Restore Networking Configuration
Force Tags  @FEATURE=System    @AUTHOR=Hans_Sun

*** Variables ***
${dummy_username}    abcd
${dummy_password}    abcd

*** Test Cases ***
tc_PPPoE_Log_File_Size_Using_Invalid_ID_PWD_Checking
    [Documentation]   tc_PPPoE_Log_File_Size_Using_Invalid_ID_PWD_Checking
    ...    1. Setting invalid ID/PWD on PPPoE page and trying to connect internet.
    ...    2. Using command "ls -alh /var/log/ppp.log" to see log file size If it is greater than 1M ,the case is failed. then is pass
    [Tags]   @TCID=WRTM-326ACN-465    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]
    Setting invalid ID/PWD on PPPoE page and trying to connect internet
    Using command "ls -alh /var/log/ppp.log" to see log file size If it is greater than 2M ,the case is failed. then is pass

*** Keywords ***
Setting invalid ID/PWD on PPPoE page and trying to connect internet
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Config PPPoE Client    ${dummy_username}    ${dummy_password}

Using command "ls -alh /var/log/ppp.log" to see log file size If it is greater than 2M ,the case is failed. then is pass
    [Tags]   @AUTHOR=Hans_Sun
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts

    sleep    280s
    Check ppp.log Rotation

Check ppp.log Rotation
    [Tags]   @AUTHOR=Hans_Sun
    ${ret} =    cli    dut1    ls -alh /var/log/ppp.log
    ${ret} =    Get Line    ${ret}    1
    @{list} =    Split String    ${ret}
    log    ${list}

    Checking Data Size    @{list}[4]

Checking Data Size
    [Arguments]    ${datasize}
    [Tags]   @AUTHOR=Jujung_Chang
    ${status} =  Run Keyword And Return Status   Should Contain    ${datasize}    M
    Run Keyword If    '${status}' == 'True'    Is Data Size Small Than 2M Or Not    ${datasize}
    Run Keyword If    '${status}' == 'False'   Pass Execution    "The data size is small than 2M."


Is Data Size Small Than 2M Or Not
    [Arguments]    ${datasize}
    [Tags]   @AUTHOR=Jujung_Chang
    ${datasize} =  Fetch From Left    ${datasize}    M
    ${datasize} =  Convert To Number    ${datasize}
    Run Keyword If    ${datasize} < 2    Pass Execution    "The data size is small than 2M."
    ...    ELSE    Fail    "The data size is bigger than 2M."

Clear DUT's ppp.log
    [Tags]   @AUTHOR=Hans_Sun
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    cli    dut1    rm /var/log/ppp.log

Restore Networking Configuration
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking
    Config DHCP Client

*** comment ***
2017-12-11     Hans_Sun
Init the script
