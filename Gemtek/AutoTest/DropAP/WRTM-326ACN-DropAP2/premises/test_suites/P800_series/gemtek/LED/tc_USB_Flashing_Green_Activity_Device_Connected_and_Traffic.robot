*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Hans_Sun    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Reset USB Module
*** Variables ***
${844fb_dump_led_register}    dw fffe8114
${count_usb_on}    0
${count_usb_off}    0
${times}    10

*** Test Cases ***
tc_Flashing_Green_Activity_Device_Connected_and_Traffic
    [Documentation]   tc_Flashing_Green_Activity_Device_Connected_and_Traffic
    ...    Verify if the USB LED stay in Flashing Green Activity state when Device Connected and Traffic.
    ...    1. Connect a device in a USB port and start a data traffic.
    ...    2. USB LED must be in a Flashing Green Activity state.
    [Tags]    @TCID=PREMS-TC-7907    @globalid=1597632LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]
    #Check USB is existed and mounted
    ${result} =   cli    n1    ls /mnt/
    Should Contain    ${result}    disk
    ${ret} =    Get Line    ${result}    1
    #Check add file from USB to device
    cli    n1    rm /mnt/${ret}/lib
    cli    n1    mkdir /mnt/${ret}/lib
    cli    n1    cp -r /lib/libcrypto.so.1.0.0 /mnt/${ret}/lib &
    cli    n1    cp -r /lib/libcms_core.so /mnt/${ret}/lib &

    #Check USB_flashing Register Value 23 bit is 0 or 1
    Wait Until Keyword Succeeds    15x    0.5s    Get USB Flashing Register Value    n1    ${times}
    #Check file is existed on device
    Wait Until Keyword Succeeds    10x    3s    Check USB File    ${ret}
    #Check files transmission is done, from USB to DUT
    Wait Until Keyword Succeeds    12x    20s    Check Files Transmission Is Done    ${ret}

    cli    n1    rm -rf /mnt/${ret}/lib

*** Keywords ***
Get USB Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check USB_flashing Register Value 23 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{2}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_usb_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_usb_on} + 1
        ...    ELSE    Set Variable    ${count_usb_on}
    \    ${count_usb_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_usb_off} + 1
        ...    ELSE    Set Variable    ${count_usb_off}
    Should not Be Equal    ${count_usb_on}    0
    Should not Be Equal    ${count_usb_off}    0

Check USB File
    [Arguments]    ${ret}
    [Documentation]    To check if disk file is existed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   cli    n1    ls mnt/${ret}/
    Should Contain    ${result}    lib

Check USB Disk
    [Arguments]
    [Documentation]    To check if disk file is existed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   cli    n1    ls mnt/
    Should Contain    ${result}    disk

Check Files Transmission Is Done
    [Arguments]    ${ret}
    [Documentation]    Check files transmission is done, from USB to DUT
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${check_lib_folder_not_contain} =   cli    n1    find /mnt/${ret}/lib -type f | wc -l
    log    ${check_lib_folder_not_contain}
    Should Contain    ${check_lib_folder_not_contain}    2

Enter Shell Mode
    [Arguments]
    [Documentation]    Go to shell mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    Wait Until Keyword Succeeds    5x    3s    cli    n1    sh    ~ #
    #Wait for USB to come up, it looks like sometimtes after reboot, usb didn't be initialed successfully, so we need to re-insert module
    Reset USB Module
    Wait Until Keyword Succeeds    5x    3s    cli    n1    sh    ~ #

Reset USB Module
    [Arguments]
    [Documentation]    Reset USB module
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    #Check USB is existed and mounted
    ${result} =   cli    n1    ls /mnt/
    ${ret} =    Get Line    ${result}    1
    cli    n1    umount /mnt/${ret}
    cli    n1    rmmod bcm63xx_usb
    cli    n1    insmod /lib/modules/3.4.11-rt19/kernel/arch/arm/plat-bcm63xx/bcm63xx_usb.ko
    Wait Until Keyword Succeeds    5x    3s    Check USB Disk
    cli    n1    exit
