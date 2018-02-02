*** Settings ***

*** Variables ***


*** Keywords ***
Login Linux Wifi Client To Connect To DUT Without Security Key
    [Arguments]    ${device}    ${ssid}    ${wifi_client_interface}    ${dut_gw}
    [Documentation]    Connect to DUT without security key
    [Tags]    @AUTHOR=Hans_Sun

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo killall dhclient
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${ssid}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    sed -i '3ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -i ${wifi_client_interface} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    ${device}    ${ssid}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${wifi_client_interface}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${wifi_client_interface} &
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    ${device}    ${dut_gw}

Verify Wireless Scan With Hidden or not
    [Arguments]    ${device}    ${test_ssid}    ${hidden}=no
    [Documentation]    Scan SSID and rescan after disable broadcast SSID
    [Tags]    @AUTHOR=Gavin_Chang

    #Scan SSID
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    echo 'ctrl_interface=/var/run/wpa_supplicant/' > scan.conf
    cli    ${device}    echo 'update_config=1' >> scan.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -D wext -i ${DEVICES.wifi_client.int} -c ~/scan.conf -B
    Run Keyword If    '${hidden}' == 'no'    Wait Until Keyword Succeeds    5x    3s    Scan SSID Successful    wifi_client    ${test_ssid}
    ...    ELSE IF    '${hidden}' == 'yes'    Wait Until Keyword Succeeds    5x    3s    Scan SSID Fail    wifi_client    ${test_ssid}

Scan SSID Successful
    [Arguments]    ${device}    ${scan_ssid_name}
    [Documentation]    Scan the broadcast SSID(enabled)
    [Tags]    @AUTHOR=Gavin_Chang

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_cli scan
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_cli scan_results | grep ${scan_ssid_name} > temp
    ${result} =    cli    ${device}    cat temp
    log    ${result}
    Should Contain    ${result}    ${scan_ssid_name}
    cli    ${device}    rm temp

Scan SSID Fail
    [Arguments]    ${device}    ${scan_ssid_name}
    [Documentation]    Scan the broadcast SSID(disabled)
    [Tags]    @AUTHOR=Gavin_Chang

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_cli scan
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_cli scan_results | grep ${scan_ssid_name} > temp
    ${result} =    cli    ${device}    cat temp
    log    ${result}
    Should Not Contain    ${result}    ${scan_ssid_name}
    cli    ${device}    rm temp

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
    [Arguments]    ${device}    ${ssid}    ${secruity_key}    ${wifi_client_interface}    ${dut_gw}
    [Documentation]    Connect to DUT with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo killall dhclient
    cli    ${device}    wpa_passphrase ${ssid} ${secruity_key} > wpa.conf
    cli    ${device}    sed -i '4ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -D wext -i ${wifi_client_interface} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    ${device}    ${ssid}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${wifi_client_interface}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${wifi_client_interface} &
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    ${device}    ${dut_gw}

Login Linux Wifi Client To Connect To DUT With Unmatched Security Key
    [Arguments]    ${device}    ${ssid}    ${secruity_key}    ${wifi_client_interface}    ${dut_gw}
    [Documentation]    Connect to DUT with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Run Keyword And Ignore Error    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    Run Keyword And Ignore Error    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo killall dhclient
    cli    ${device}    wpa_passphrase ${ssid} ${secruity_key} > wpa.conf
    cli    ${device}    sed -i '4ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -D wext -i ${wifi_client_interface} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Down    ${device}    ${ssid}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${wifi_client_interface}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${wifi_client_interface} &
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Fail    ${device}    ${dut_gw}

Use Iperf Send Traffic and Verify Connection Successful
    [Arguments]    ${src}    ${dst}    ${triffic_ip}    ${count}=10
    [Documentation]    Use iperf send traffic bewteen LAN and WAN
    ${timeout} =    Evaluate    ${count}+20
    log    ${timeout}
    Run Keyword And Ignore Error    cli    ${src}    killall iperf
    cli    ${dst}    iperf -s &
    ${result}=   cli    ${src}    iperf -c ${triffic_ip} -t ${count}    timeout=${timeout}
    log    ${result}
    Should Contain    ${result}    Client connecting to ${triffic_ip}

Login Linux Wifi Client To Connect To DUT Using WEP Encryption
    [Arguments]    ${device}    ${ssid}    ${secruity_key}    ${wifi_client_interface}    ${dut_gw}
    [Documentation]    Connect to DUT with matched security key
    [Tags]    @AUTHOR=Hans_Sun

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo killall dhclient
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${ssid}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE' >> wpa.conf
    cli    ${device}    echo 'wep_key0="${g_dut_wep_ssid_pw}"' >> wpa.conf
    cli    ${device}    echo 'wep_tx_keyidx=0\n}' >> wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -D wext -i ${wifi_client_interface} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    ${device}    ${ssid}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${wifi_client_interface}
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${wifi_client_interface} &
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    ${device}    ${dut_gw}

Login Linux Wifi Client To Connect To DUT With Guest SSID
    [Arguments]    ${device}    ${ssid}    ${wifi_client_interface}
    [Documentation]    Connect to DUT without security key
    [Tags]    @AUTHOR=Hans_Sun

    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S sudo killall dhclient
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${ssid}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    sed -i '3ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${DEVICES.wifi_client.password} | sudo -S wpa_supplicant -i ${wifi_client_interface} -c ~/wpa.conf -B

Is Linux wget Successful
    [Arguments]    ${my_device}    ${website_url}    ${wait_time}=10    ${IP_URL}=3
    [Documentation]    Linux wget to connect http website
    [Tags]     @AUTHOR=Thomas_Chen

    ${result} =    cli    ${my_device}    wget ${website_url} --timeout=${wait_time} -t 1
    ${result}    Run Keyword If    ${IP_URL} > 0    Get Line    ${result}    ${IP_URL}
    ...    ELSE    set variable    ${result}
    log    ${result}
    Should Contain    ${result}    HTTP request sent, awaiting response... 200 OK

Is Linux wget Failed
    [Arguments]    ${my_device}    ${website_url}    ${wait_time}=10    ${IP_URL}=2
    [Documentation]    Linux wget to connect http website
    [Tags]     @AUTHOR=Thomas_Chen

    ${result} =    cli    ${my_device}    wget ${website_url} --timeout=${wait_time} -t 1
    ${result}    Run Keyword If    ${IP_URL} > 0    Get Line    ${result}    ${IP_URL}
    ...    ELSE    set variable    ${result}
    log    ${result}
    Should Contain    ${result}     Connection timed out
