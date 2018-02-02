__author__ = 'glivermo'
import cafe
import time
import re
from stp.api.ixveriwave.ixveriwavelib import ixvw_simplebenchtest
from stp.api.ixveriwave.ixveriwavelib import ixvw_advancedbenchtest
from stp.api.ixveriwave.ixveriwavelib import delremotefile
from stp.api.utilities.utilities import gen_ont_md5

@cafe.test_case()
def tc_675201_24g_base_ssid_default_security(params):
    """
    @id=675201
    Description:
    (2.4GHz) SEC Default Security Settings: Use Factory default security settings on base SSID (WPA-WPA2 Personal,
    AES, default key).  Use IxVeriwave test clients  to connect and generate traffic between the base SSID and another
    client which may be on the LAN, WAN, or Wifi.  IxVeriwave set to: WPA2-PSK, ASCII shared secret = 16 hex based
    on ONT FSAN.    -> Association made and data flow between two clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    
    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # Obtain default ONT md5 key
    md5 = gen_ont_md5(fsan=fsan)

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")
    
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth, srcsecmethod='WPA2-PSK', srcsecsecret=md5['wpakey'],
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype,
                                  destint=ixvwlanport, destinttype='802.3',
                                  framesize='1460', srcpercentrate="20")

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

@cafe.test_case()
def tc_675202_24g_base_ssid_custom_key(params):
    """
    @id=675202
    Description:
    (2.4GHz) SEC Base SSID Change Security Key: On base SSID provision following security settings: WPA-WPA2-Personal,
    AES, custom security key.  Use IxVeriwave test clients to connect and generate traffic between the base SSID and
    another client which may be on the LAN, WAN, or WiFi.  IxVeriwave set to: WPA2-PSK, ASCII shared secret = custom
    security key. -> Association made and data flow between two clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = "6"
    wifibandwidth = '20 MHz'
    ixvwradiointtype = '802.11n'
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth, srcsecmethod='WPA2-PSK', srcsecsecret='1234567890',
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype,
                                  destint=ixvwlanport, destinttype='802.3',
                                  framesize='1460', srcpercentrate="20")

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_675203_24g_guest_opertor_ssid_default_security_key(params):
    """
    @id=675203
    Description:
    (2.4GHz) SEC Guest SSID Default Security Key: Enable the guest SSID and all Operator SSIDs(if present).  Enable
    security type WPA-WPA2-Personal, encryption AES, and the default security key of "1234567890".  Use IxVeriwave
    test clients to connect and generate traffic between a client from each SSID to a LAN, WAN, or WiFi client.
    IxVeriwave set to: WPA2-PSK, ASCII shared secret = custom security key. -> Association made and data  flow
    between clients at a rate with no loss.

    Note: The 836GE default passphrase for guest network = "1234567890".  The 800G/GH default for the guest and all
    operator SSIDs is "1234567890".
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    if str(eut).lower() is not "836ge":
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_6', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
    if str(eut).lower() is not "836ge":
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_6',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values
    # TODO: May need about 10 seconds of wait time here to make sure radio took all the changes.
    time.sleep(5)

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    if str(eut).lower() is not "836ge":
        ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                    Direction='Unidirectional',
                                    Source='guest_grp op1_grp op2_grp op3_grp op4_grp op5_grp op6_grp',
                                    Destination='enet_grp',
                                    TrialDuration='15',
                                    LossTolerance='100',
                                    Channel=wifichannel)
    else:
        ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='guest_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='10',
                              MinSearchValue='10',
                              SearchResolution='1',
                              StartValue='10')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                BaseIp='192.168.1.200',
                                Gateway='192.168.1.1')
    ixvwcfg['guest_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                BaseIp='192.168.1.100',
                                Gateway='192.168.1.1',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    if str(eut).lower() is not "836ge":
        ixvwcfg['op1_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_1',
                                    BaseIp='192.168.1.10',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op2_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_2',
                                    BaseIp='192.168.1.20',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op3_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_3',
                                    BaseIp='192.168.1.30',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op4_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_4',
                                    BaseIp='192.168.1.40',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op5_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_5',
                                    BaseIp='192.168.1.50',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op6_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_6',
                                    BaseIp='192.168.1.60',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    # All operator security are set to default values for this test
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")
    if str(eut).lower() is not "836ge":
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_6',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_6', ssidstate="disabled")

@cafe.test_case()
def tc_675204_24g_base_guest_ssid_custom_security_key(params):
    """
    @id=675204
    Description:
    (2.4GHz) Base & Guest SSID Custom Valid Security Key: Enable the Base/Primary & Guest SSIDs.  Enable security
    type WPA-WPA2-Personal, encryption AES, and a security different from the default.  Each SSID should be
    provisioned with a unique custom key.  The key should contain a sampling of valid values including alphanumerics
    and symbols. Example: 'abcdefgh12345678~!@#$%^&'.  Use IxVeriwave test clients to connect and generate traffic
    between a client from each SSID and a LAN client and SSID client. IxVeriwave set to:    WPA2-PSK, ASCII shared
    secret = custom security key.  Retest using the minimum character length valid PSK.  Retest using the maximum
    character length (63) valid PSK.  -> For each test association made and data  flow between LAN client and a client
    on each SSID clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp guest_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='10',
                              MinSearchValue='10',
                              SearchResolution='1',
                              StartValue='10')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               Dhcp='Enable')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Verify the minimum character length SSID
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='12345678')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='12345678')
    ixvwcfg['base_grp']['PskAscii'] = '12345678'
    ixvwcfg['guest_grp']['PskAscii'] = '12345678'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Verify the maximum character length SSID
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan,
                                  passphrase='123456789012345678901234567890123456789012345678901234567890123')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='123456789012345678901234567890123456789012345678901234567890123')
    ixvwcfg['base_grp']['PskAscii'] = '123456789012345678901234567890123456789012345678901234567890123'
    ixvwcfg['guest_grp']['PskAscii'] = '123456789012345678901234567890123456789012345678901234567890123'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_675209_24g_base_guest_ssid_security_off(params):
    """
    @id=675209
    Description:
    (2.4GHz) SEC Base and Guest SSID Security Off:   Enable both the Base/Primary and Guest SSIDs.  On both SSIDs set
    security to off.   Use IxVeriwave test clients to connect and generate traffic between a LAN client and SSID client.
    IxVeriwave security set to None.  -> Association made and data flow between LAN client and a client on each SSID
    clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = "20 MHz"
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype='Security Off')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp guest_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='10',
                              MinSearchValue='10',
                              SearchResolution='1',
                              StartValue='10')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               Dhcp='Enable')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth)
    ixvwcfg['guest_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth)
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype='WPA - WPA2-Personal')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_675210_24g_base_guest_ssid_security_wpawpa2_enc_both(params):
    """
    @id=675210
    (2.4GHz) SEC Base and Guest SSID Security WPA-WPA2-Personal, Encrypt BOTH: Enable the Base/Primary & Guest SSIDs
    (radio mode capable of 802.11n).  On each SSID Enable security type=WPA-WPA2-Personal, encryption=Both.  Use a
    unique non default/custom security pass key on each SSIDs.  Use IxVeriwave test clients to connect and generate
    traffic between a LAN and SSIDs clients.  IxVeriwave set to create 4 clients per SSID.  Each client configured
    with the ONT provisioned ASCII shared key for the SSID but the security methods are all unique: WPA-PSK, WPA2-PSK,
    WPA-PSK-AES, WPA2-PSK-TKIP.  -> Association made and data  flow between LAN client and a client on each SSID
    clients at a rate with no loss or very low loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="Both", keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="Both", passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp_tkip base_grp_aes base_grp_wpa base_grp_wpa2 guest_grp_tkip '
                                       'guest_grp_aes guest_grp_wpa guest_grp_wpa2',
                                Destination='enet_grp',
                                TrialDuration='15',
                                SettleTime='10',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='20',
                              MinSearchValue='20',
                              SearchResolution='1',
                              StartValue='20')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                Dhcp='Enable')
    ixvwcfg['base_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.11',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.31',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.41',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # 3% loss tolerance - loss is usually seen both in script and in GUI.  Do not have an explaination at this time.
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 3:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Clients association with < 3% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_675211_24g_base_guest_ssid_security_wpawpa2_enc_aes(params):
    """
    @id=675211
    Description:
    (2.4GHz) SEC Base and Guest SSID Security WPA-WPA2-Personal, Encrypt AES: Enable the Base/Primary & Guest SSIDs
    (radio mode capable of 802.11n).  On each SSID Enable security type=WPA-WPA2-Personal, encryption=AES.  Use a
    unique non default/custom security pass key on each SSIDs.  Use IxVeriwave test clients to connect and generate
    traffic between a LAN and SSIDs clients.  IxVeriwave set to create 4 clients per SSID.  Each client configured
    with the ONT provisioned ASCII shared key for the SSID but the security methods are all unique: WPA-PSK, WPA2-PSK,
    WPA-PSK-AES, WPA2-PSK-TKIP.   -> Association made and data  flow between LAN client and a WPA2-PSK and WPA-PSK-AES
    clients on each SSID clients at a rate with no loss or very low loss.  WPA-PSK and WPA2-PSK-TKIP clients not
    allowed to associate.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Validate WPA2-PSK & WPA-PSK-AES clients associated and forward traffic
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp_aes base_grp_wpa2 guest_grp_aes guest_grp_wpa2',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='50',
                              MinSearchValue='50',
                              SearchResolution='1',
                              StartValue='50')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut')
    ixvwcfg['base_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.11',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.31',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.41',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # 3% loss tolerance - loss is usually seen both in script and in GUI.  Do not have an explaination at this time.
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 3:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Clients association with < 3% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Validate WPA2-PSK-TKIP, WPA-PSK(TKIP),  clients fail Wifi association
    ixvwcfg['globalcfg']['Source'] = 'base_grp_tkip guest_grp_tkip base_grp_wpa guest_grp_wpa'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # Verify client Wifi association failed
    matchobj = re.match(r'.*(Association request: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    # And that none of the WiFi clients were able to connect
    matchobj = re.match(r'.*(Mobile client [\w|\s]* is connected).*', result['console'], re.S)
    if matchobj is not None:
        success = False
    else:
        success = True
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Client association failure")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_675212_24g_base_guest_ssid_security_wpawpa2_enc_tkip(params):
    """
    @id=675212
    Description:
    (2.4GHz) Base and Guest SSID Security WPA-WPA2-Personal, Encrypt TKIP: Enable the Base/Primary & Guest SSIDs
    (radio mode capable of 802.11n).  On each SSID Enable security type=WPA-WPA2-Personal, encryption=TKIP.  Use a
    unique non default/custom security pass key on each SSIDs.  Use IxVeriwave test clients to connect and generate
    traffic between a LAN and SSIDs clients.  IxVeriwave set to create 4 clients per SSID.  Each client configured
    with the ONT provisioned ASCII shared key for the SSID but the security methods are all unique: WPA-PSK, WPA2-PSK,
    WPA-PSK-AES, WPA2-PSK-TKIP.  -> Association made and data  flow between LAN client and WPA-PSK and WPA2-PSK-TKIP
    WiFi clients on each SSID clients at a rate with no loss or very low loss.  Association not allowed for WPA2-PSK
    or WPA-PSK-AES.

    WARNING!!!! PREM-14869
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="TKIP", keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="TKIP", passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp_tkip base_grp_wpa guest_grp_tkip guest_grp_wpa',
                                Destination='enet_grp',
                                TrialDuration='15',
                                SettleTime='10',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='20',
                              MinSearchValue='20',
                              SearchResolution='1',
                              StartValue='20')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                Dhcp='Enable')
    ixvwcfg['base_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.11',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.31',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.41',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify WPA-PSK(TKIP) and WPA2-PSK-TKIP clients can associated an traffic is generated
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # 3% loss tolerance - loss is usually seen both in script and in GUI.  Do not have an explaination at this time.
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 3:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Clients association with < 3% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify WPA-PSK-AES and WPA2-PSK(AES) clients can NOT associate with AP
    ixvwcfg['globalcfg']['Source'] = 'base_grp_aes base_grp_wpa2 guest_grp_aes guest_grp_wpa2'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # Verify a client Wifi association failed
    matchobj = re.match(r'.*(Association request: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    # And none of the clients were able to connect
    matchobj = re.match(r'.*(Mobile client [\w|\s]* is connected).*', result['console'], re.S)
    if matchobj is not None:
        success = False
    else:
        success = True
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Client association failure")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_1019101_24g_base_guest_ssid_security_wpa2_enc_aes(params):
    """
    @id=1019101
    Description:
    (2.4GHz) Base and Guest SSID Security WPA2-Personal, Encrypt AES: Enable the Base/Primary & Guest SSIDs (radio
    mode capable of 802.11n).  On each SSID Enable security type=WPA2-Personal, encryption=AES.  Use a unique non
    default/custom security pass key on each SSIDs.  Use IxVeriwave test clients to connect and generate traffic
    between a LAN and SSIDs clients.  IxVeriwave set to create 4 clients per SSID.  Each client configured with the
    ONT provisioned ASCII shared key for the SSID but the security methods are all unique: WPA-PSK, WPA2-PSK,
    WPA-PSK-AES, WPA2-PSK-TKIP.   -> Association made and data  flow between LAN client and a WPA2-PSK clients on
    each SSID clients at a rate with no loss or very low loss.  WPA-PSK, WPA-PSK-AES, and WPA2-PSK-TKIP clients not
    allowed to associate
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b, 802.11g, and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA2-Personal",
                                  encryptiontype="AES", passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Validate WPA2-PSK clients associated and forward traffic
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp_wpa2 guest_grp_wpa2',
                                Destination='enet_grp',
                                TrialDuration='15',
                                SettleTime='10',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='20',
                              MinSearchValue='20',
                              SearchResolution='1',
                              StartValue='20')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                Dhcp='Enable')
    ixvwcfg['base_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.11',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.31',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.41',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # 3% loss tolerance - loss is usually seen both in script and in GUI.  Do not have an explaination at this time.
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 3:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Clients association with < 3% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Validate WPA2-PSK-TKIP, WPA-PSK(TKIP), and WPA2-PSK-TKIP clients fail Wifi association
    ixvwcfg['globalcfg']['Source'] = 'base_grp_aes base_grp_tkip guest_grp_tkip guest_grp_aes base_grp_wpa guest_grp_wpa'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # Verify a client Wifi association failed
    matchobj = re.match(r'.*(Association request: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    # And none of the clients were able to connect
    matchobj = re.match(r'.*(Mobile client [\w|\s]* is connected).*', result['console'], re.S)
    if matchobj is not None:
        success = False
    else:
        success = True
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Client association failure")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_981722_5g_base_ssid_default_security(params):
    """
    @id=981722
    Description:
    (5GHz) SEC Default Security Settings: Use Factory default security settings on base SSID (WPA-WPA2 Personal,
    AES, default key).  Use IxVeriwave test clients  to connect and generate traffic between the base SSID and another
    client which may be on the LAN, WAN, or Wifi.  IxVeriwave set to: WPA2-PSK, ASCII shared secret = 16 hex based
    on ONT FSAN.    -> Association made and data flow between two clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = "36"
    wifibandwidth = "80 MHz"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # Obtain default ONT md5 key
    md5 = gen_ont_md5(fsan=fsan)

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="default")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth, srcsecmethod='WPA2-PSK', srcsecsecret=md5['wpakey'],
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype,
                                  destint=ixvwlanport, destinttype='802.3',
                                  framesize='1460', srcpercentrate="20")

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

@cafe.test_case()
def tc_981707_5g_base_ssid_custom_key(params):
    """
    @id=981707
    Description:
    (5Hz) SEC Base SSID Change Security Key: On base SSID provision following security settings: WPA-WPA2-Personal,
    AES, custom security key.  Use IxVeriwave test clients to connect and generate traffic between the base SSID and
    another client which may be on the LAN, WAN, or WiFi.  IxVeriwave set to: WPA2-PSK, ASCII shared secret = custom
    security key. -> Association made and data flow between two clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = "36"
    wifibandwidth = '80 MHz'
    ixvwradiointtype = '802.11ac'
    ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth, srcsecmethod='WPA2-PSK', srcsecsecret='1234567890',
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype,
                                  destint=ixvwlanport, destinttype='802.3',
                                  framesize='1460', srcpercentrate="20")

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="default")

@cafe.test_case()
def tc_981708_5g_guest_opertor_ssid_default_security_key(params):
    """
    @id=981708
    Description:
    (5GHz) SEC Guest SSID Default Security Key: Enable the guest SSID and all Operator SSIDs(if present).  Enable
    security type WPA-WPA2-Personal, encryption AES, and the default security key of "1234567890".  Use IxVeriwave
    test clients to connect and generate traffic between a client from each SSID to a LAN, WAN, or WiFi client.
    IxVeriwave set to: WPA2-PSK, ASCII shared secret = custom security key. -> Association made and data  flow
    between clients at a rate with no loss.

    Note: The 836GE default passphrase for guest network = "1234567890".  The 800G/GH default for the guest and all
    operator SSIDs is "1234567890".
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = '36'
    wifibandwidth = '80 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    if str(eut).lower() is not "836ge":
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5', ssidstate="enabled",
                                  broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
    if str(eut).lower() is not "836ge":
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
        ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5',
                                  securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values
    # TODO: May need about 10 seconds of wait time here to make sure radio took all the changes.
    time.sleep(5)

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    if str(eut).lower() is not "836ge":
        ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                    Direction='Unidirectional',
                                    Source='guest_grp op1_grp op2_grp op3_grp op4_grp op5_grp',
                                    Destination='enet_grp',
                                    TrialDuration='15',
                                    LossTolerance='100',
                                    Channel=wifichannel)
    else:
        ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='guest_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='10',
                              MinSearchValue='10',
                              SearchResolution='1',
                              StartValue='10')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                BaseIp='192.168.1.200',
                                Gateway='192.168.1.1')
    ixvwcfg['guest_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                BaseIp='192.168.1.100',
                                Gateway='192.168.1.1',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    if str(eut).lower() is not "836ge":
        ixvwcfg['op1_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_1',
                                    BaseIp='192.168.1.10',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op2_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_2',
                                    BaseIp='192.168.1.20',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op3_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_3',
                                    BaseIp='192.168.1.30',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op4_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_4',
                                    BaseIp='192.168.1.40',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
        ixvwcfg['op5_grp'] = dict(GroupType=ixvwradiogrouptype,
                                    Dut='wifi_dut',
                                    Ssid=radiotype + '_Operator_5',
                                    BaseIp='192.168.1.50',
                                    Gateway='192.168.1.1',
                                    phyInterface=ixvwradiophyinttype,
                                    ChannelBandwidth=ixvwradiobandwidth,
                                    Method='WPA-PSK-AES',
                                    PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    # All operator security are set to default values for this test
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")
    if str(eut).lower() is not "836ge":
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_4', ssidstate="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5',
                                  broadcast="disabled")
        ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_5', ssidstate="disabled")

@cafe.test_case()
def tc_981709_5g_base_guest_ssid_custom_security_key(params):
    """
    @id=tc_981709
    Description:
    (5GHz) Base & Guest SSID Custom Valid Security Key: Enable the Base/Primary & Guest SSIDs.  Enable security
    type WPA-WPA2-Personal, encryption AES, and a security different from the default.  Each SSID should be
    provisioned with a unique custom key.  The key should contain a sampling of valid values including alphanumerics
    and symbols. Example: 'abcdefgh12345678~!@#$%^&'.  Use IxVeriwave test clients to connect and generate traffic
    between a client from each SSID and a LAN client and SSID client. IxVeriwave set to:    WPA2-PSK, ASCII shared
    secret = custom security key.  Retest using the minimum character length valid PSK.  Retest using the maximum
    character length (63) valid PSK.  -> For each test association made and data  flow between LAN client and a client
    on each SSID clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = '36'
    wifibandwidth = '80 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Verify the SSID with alphas, numeric, and symbols operate
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp guest_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='10',
                              MinSearchValue='10',
                              SearchResolution='1',
                              StartValue='10')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               Dhcp='Enable')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Verify the minimum character length SSID
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='12345678')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='12345678')
    ixvwcfg['base_grp']['PskAscii'] = '12345678'
    ixvwcfg['guest_grp']['PskAscii'] = '12345678'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Verify the maximum character length SSID
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan,
                                  passphrase='123456789012345678901234567890123456789012345678901234567890123')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='123456789012345678901234567890123456789012345678901234567890123')
    ixvwcfg['base_grp']['PskAscii'] = '123456789012345678901234567890123456789012345678901234567890123'
    ixvwcfg['guest_grp']['PskAscii'] = '123456789012345678901234567890123456789012345678901234567890123'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_981711_5g_base_guest_ssid_security_off(params):
    """
    @id=981711
    Description:
    (5GHz) SEC Base and Guest SSID Security Off:   Enable both the Base/Primary and Guest SSIDs.  On both SSIDs set
    security to off.   Use IxVeriwave test clients to connect and generate traffic between a LAN client and SSID client.
    IxVeriwave security set to None.  -> Association made and data flow between LAN client and a client on each SSID
    clients at a rate with no loss.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = '36'
    wifibandwidth = "80 MHz"
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype='Security Off')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp guest_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='10',
                              MinSearchValue='10',
                              SearchResolution='1',
                              StartValue='10')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               Dhcp='Enable')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth)
    ixvwcfg['guest_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth)
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype='WPA - WPA2-Personal')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_981713_5g_base_guest_ssid_security_wpawpa2_enc_aes(params):
    """
    @id=981713
    (5GHz) Base and Guest SSID Security WPA-WPA2-Personal, Encrypt AES: Enable the Base/Primary & Guest SSIDs.
    On each SSID Enable security type=WPA-WPA2-Personal, encryption=AES (radio mode capable of 802.11n).  Use a
    unique non default/custom security pass key on each SSIDs.  Use IxVeriwave test clients to connect and generate
    traffic between a LAN and SSIDs clients.  IxVeriwave set to create 4 clients per SSID.  Each client configured
    with the ONT provisioned ASCII shared key for the SSID but the security methods are all unique: WPA-PSK, WPA2-PSK,
    WPA-PSK-AES, WPA2-PSK-TKIP.   -> Association made and data  flow between LAN client and a WPA2-PSK and WPA-PSK-AES
    clients on each SSID clients at a rate with no loss or very low loss.  WPA-PSK and WPA2-PSK-TKIP clients not
    allowed to associate.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = '36'
    wifibandwidth = '80 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp_wpa2 guest_grp_wpa2 base_grp_aes guest_grp_aes',
                                Destination='enet_grp',
                                TrialDuration='15',
                                SettleTime='10',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='20',
                              MinSearchValue='20',
                              SearchResolution='1',
                              StartValue='20')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                Dhcp='Enable')
    ixvwcfg['base_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.11',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.31',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.41',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

# Validate WPA2-PSK-TKIP clients fail Wifi association
    ixvwcfg['globalcfg']['Source'] = 'base_grp_tkip guest_grp_tkip base_grp_wpa guest_grp_wpa'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # Verify client Wifi association failed
    matchobj = re.match(r'.*(Association request: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    matchobj = re.match(r'.*(Mobile client [\w|\s]* is connected).*', result['console'], re.S)
    if matchobj is not None:
        success = False
    else:
        success = True
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Client association failure")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_1020703_5g_base_guest_ssid_security_wpa2_enc_aes(params):
    """
    @id=1020703
    (2.4GHz) Base and Guest SSID Security WPA2-Personal, Encrypt AES: Enable the Base/Primary & Guest SSIDs
    (radio mode capable of 802.11n).  On each SSID Enable security type=WPA2-Personal, encryption=AES.  Use a unique
    non default/custom security pass key on each SSIDs.  Use IxVeriwave test clients to connect and generate traffic
    between a LAN and SSIDs clients.  IxVeriwave set to create 4 clients per SSID.  Each client configured with the
    ONT provisioned ASCII shared key for the SSID but the security methods are all unique: WPA-PSK, WPA2-PSK,
    WPA-PSK-AES, WPA2-PSK-TKIP.   -> Association made and data  flow between LAN client and a WPA2-PSK clients on
    each SSID clients at a rate with no loss or very low loss.  WPA-PSK, WPA-PSK-AES, and WPA2-PSK-TKIP clients not
    allowed to associate.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = "802.11ac and 802.11n"
    wifichannel = '36'
    wifibandwidth = '80 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA2-Personal",
                                  keytype="custom", passphrase='abcdefgh12345678~!@#$%^&base')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA2-Personal",
                                  passphrase='abcdefgh12345678~!@#$%^&guest')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET LAN to multiple Wifi Clients
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp_wpa2 guest_grp_wpa2',
                                Destination='enet_grp',
                                TrialDuration='15',
                                SettleTime='10',
                                LossTolerance='100',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(SourcePort='5000',
                              DestinationPort='5001',
                              FrameSizeList='1460',
                              MaxSearchValue='20',
                              MinSearchValue='20',
                              SearchResolution='1',
                              StartValue='20')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                                Dut='enet_dut',
                                Dhcp='Enable')
    ixvwcfg['base_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.11',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.31',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['base_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.41',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&base')
    ixvwcfg['guest_grp_tkip'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK-TKIP',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_aes'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK-AES',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['guest_grp_wpa2'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Ssid=radiotype + '_Guest' + fsan[-6:],
                                phyInterface=ixvwradiophyinttype,
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='abcdefgh12345678~!@#$%^&guest')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Clients association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Validate WPA2-PSK-TKIP, WPA-PSK(TKIP), and WPA2-PSK-TKIP clients fail Wifi association
    ixvwcfg['globalcfg']['Source'] = 'base_grp_aes base_grp_tkip guest_grp_tkip guest_grp_aes base_grp_wpa guest_grp_wpa'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # Verify client Wifi association failed
    matchobj = re.match(r'.*(Association request: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    matchobj = re.match(r'.*(Mobile client [\w|\s]* is connected).*', result['console'], re.S)
    if matchobj is not None:
        success = False
    else:
        success = True
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "Client association failure")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="WPA - WPA2-Personal", passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")


