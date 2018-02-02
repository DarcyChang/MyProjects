*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Hans_Sun    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Reset USB Module
*** Variables ***
${844fb_dump_led_register}     dw fffe8114

*** Test Cases ***
tc_Verify_USB_Solid_Green_Device_Connected_no_Traffic
    [Documentation]    tc_Verify_USB_LED_ON_when_USB_port_enabled
    ...    Verify if the USB LED stay in Solid Green state when device is connected.
    ...    1.When Device is connected a USB port, USB LED be in a Solid Green activity state.
    ...    2.When Device is disconnected a USB port, USB LED be in off state
    ...    3. Device is connected a USB port again, USB LED be in a Solid Green activity state.
    [Tags]    @TCID=PREMS-TC-7906    @globalid=1597631LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]
    #Check USB is existed and mounted
    ${result} =   cli    n1    ls /mnt/
    Should Contain    ${result}    disk
    #Check USB_on Register Value 23 bit is 0
    ${result} =   Wait Until Keyword Succeeds    10x    1s    Check LED On in Certain Tries    n1
    log    ${result}
    Should Be Equal     ${result}    0
    #Unmount USB module by Command line
    cli    n1    rmmod bcm63xx_usb
    #Check USB_off Register Value 23 bit is 1
    ${result} =   Wait Until Keyword Succeeds    10x    1s    Check LED Off in Certain Tries    n1
    log    ${result}
    Should Be Equal     ${result}    1
    #Check disk2_1 file is not exist in /mnt/
    ${result} =   cli    n1    ls /mnt/
    log    ${result}
    Should Not Contain    ${result}    disk
    #Mount USB module by Command line
    cli    n1    insmod /lib/modules/3.4.11-rt19/kernel/arch/arm/plat-bcm63xx/bcm63xx_usb.ko
    #Check USB is existed and mounted
    Wait Until Keyword Succeeds    5x    3s    Check USB Disk
    #Check USB_on Register Value 23 bit is 0
    ${result} =   Wait Until Keyword Succeeds    10x    1s    Check LED On in Certain Tries    n1
    log    ${result}
    Should Be Equal     ${result}    0

*** Keywords ***
Get USB LED Status From Register Value
    [Arguments]    ${device}
    [Documentation]    when usb on Register Value is 076afbee  => should retrive third hex: 6->0110, bit 23 is 0
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{2}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    ([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

Check USB Disk
    [Arguments]
    [Documentation]    To check if disk file is existed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =    cli    n1    ls /mnt/
    Should Contain    ${result}    disk

Check LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when led flashing transfer to solid, retry to check register value
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get USB LED Status From Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Check LED Off in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when led flashing transfer to solid, retry to check register value
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get USB LED Status From Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    1
    [Return]    ${result}

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