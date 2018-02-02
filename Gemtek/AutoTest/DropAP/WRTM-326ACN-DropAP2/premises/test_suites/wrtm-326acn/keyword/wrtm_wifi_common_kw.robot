*** Settings ***

*** Variables ***

*** Keywords ***
Config 2.4G Wireless
    [Arguments]    ${browser}    ${radio}=on    ${ssid}=myvita    ${hidden_ssid}=0    ${security}=wpa2-psk-mixed    ${password}=00myvita    ${auto_channel}=1    ${channel}=1    ${signalmode}=3
    [Documentation]    Configure 2.4G Wireless
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    # Go to device setting page
    Go To Page    ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Config Wireless Signal(1.environmental protection 3.balance 4.through wall)
    Select From List By Value    ${browser}    signalmode    ${signalmode}

    # Disable 2.4G
    Run Keyword If    '${radio}'=='off'    Run keywords    cpe click    ${browser}    xpath=//*[@id="wifi_net_setting"]/div[3]/div[2]/div[1]/div[1]/div/div/div/span[1]
    ...    AND    cpe click    ${browser}    id=save
    ...    AND    return from keyword

    # Enable 2.4G
    cpe click    ${browser}    xpath=//*[@id="wifi_net_setting"]/div[3]/div[2]/div[1]/div[1]/div/div/div/span[3]

    # Config SSID
    input text    ${browser}    ssid    ${ssid}
    Run Keyword If    ${hidden_ssid}==0    unselect checkbox    ${browser}    hidden
    ...    ELSE    select checkbox    ${browser}    hidden

    # Config security type(wpa2-psk-mixed or open)
    Select From List By Value    ${browser}    security    ${security}
    Run Keyword If    '${security}'=='wpa2-psk-mixed'    input text    ${browser}    Password_24g    ${password}

    # Config channel(2.4G 1~13)
    Run Keyword If    ${auto_channel}==1    select checkbox    ${browser}    signal_grade
    ...    ELSE    Run Keywords    unselect checkbox    ${browser}    signal_grade
    ...    AND    Select From List By Value    ${browser}    channel24G    ${channel}
    cpe click    ${browser}    id=save

    Run Keyword If    '${security}'=='open'    Run Keywords    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="myModal_alert"]/div/div/div[1]/button
    ...    AND    cpe click    ${browser}    xpath=//*[@id="myModal_alert"]/div/div/div[1]/button
    ...    AND    sleep    2s
    ...    AND    cpe click    ${browser}    id=save


Config 5G Wireless
    [Arguments]    ${browser}    ${radio}=on    ${ssid}=myvita    ${hidden_ssid}=0    ${security}=wpa2-psk-mixed    ${password}=00myvita    ${auto_channel}=1    ${channel}=1    ${signalmode}=3
    [Documentation]    Configure 5G Wireless
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    # Go to device setting page
    Go To Page    ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Config Wireless Signal(1.environmental protection 3.balance 4.through wall)
    Select From List By Value    ${browser}    signalmode    ${signalmode}

    # Disable 5G
    Run Keyword If    '${radio}'=='off'    Run keywords    cpe click    ${browser}    xpath=//*[@id="wifi_net_setting"]/div[5]/div[2]/div/div[1]/div[1]/div/div/div/span[1]
    ...    AND    cpe click    ${browser}    id=save
    ...    AND    return from keyword

    # Enable 5G
    cpe click    ${browser}    xpath=//*[@id="wifi_net_setting"]/div[5]/div[2]/div/div[1]/div[1]/div/div/div/span[3]

    # Config SSID
    input text    ${browser}    ssid_5g    ${ssid}
    Run Keyword If    ${hidden_ssid}==0    unselect checkbox    ${browser}    hidden_5g
    ...    ELSE    select checkbox    ${browser}    hidden_5g

    # Config security type(wpa2-psk-mixed or open)
    Select From List By Value    ${browser}    security_5g    ${security}
    Run Keyword If    '${security}'=='wpa2-psk-mixed'    input text    ${browser}    Password_5g    ${password}

    # Config channel(5G 149,153,157,161,165)
    Run Keyword If    ${auto_channel}==1    select checkbox    ${browser}    signal_grade_5g
    ...    ELSE    Run Keywords    unselect checkbox    ${browser}    signal_grade_5g
    ...    AND    Select From List By Value    ${browser}    channel5G    ${channel}
    cpe click    ${browser}    id=save

    Run Keyword If    '${security}'=='open'    Run Keywords    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="myModal_alert"]/div/div/div[1]/button
    ...    AND    cpe click    ${browser}    xpath=//*[@id="myModal_alert"]/div/div/div[1]/button
    ...    AND    sleep    2s
    ...    AND    cpe click    ${browser}    id=save


Is WIFI Interface Up
    [Arguments]    ${device}    ${ssid}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${ssid}

Is WIFI Interface Down
    [Arguments]    ${device}    ${ssid}
    [Documentation]    To check if wifi interface is down
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Not Contain    ${result}    ${ssid}


Login Linux Wifi Client To Connect To DUT With Matched Security Key
    [Arguments]    ${device}    ${ssid}    ${secruity_key}    ${wifi_client_interface}    ${assign_static_ip}    ${dut_gw}
    [Documentation]    Connect to DUT with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${ssid} ${secruity_key} > wpa.conf
    cli    ${device}    sed -i '4ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -D wext -i ${wifi_client_interface} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    ${device}    ${ssid}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S ifconfig ${wifi_client_interface} ${assign_static_ip}
    cli    ${device}    ifconfig
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    ${device}    ${dut_gw}

Login Linux Wifi Client To Connect To DUT Without Security Key
    [Arguments]    ${device}    ${ssid}    ${wifi_client_interface}    ${assign_static_ip}    ${dut_gw}
    [Documentation]    Connect to DUT without security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${ssid}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    sed -i '3ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -D wext -i ${wifi_client_interface} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    ${device}    ${ssid}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S ifconfig ${wifi_client_interface} ${assign_static_ip}
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    ${device}    ${dut_gw}

*** comment ***
2017-09-05  Gemtek_Thomas_Chen
1. Add Wait Until Element Is Visible for open security config in 2.4 and 5g

2017-08-30  Gemtek_Gavin_Chang
1. Add Config 2.4G and 5G.