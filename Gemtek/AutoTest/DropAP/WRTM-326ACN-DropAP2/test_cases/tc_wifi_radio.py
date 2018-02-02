__author__ = 'glivermo'
import cafe
import time
import re
from stp.api.ixveriwave.ixveriwavelib import ixvw_simplebenchtest
from stp.api.ixveriwave.ixveriwavelib import ixvw_advancedbenchtest
from stp.api.ixveriwave.ixveriwavelib import delremotefile
from stp.api.utilities.utilities import gen_ont_md5

@cafe.test_case()
def tc_1052807_24g_radio_toggle(params):
    """
    @id=1052807
    Description:
    (2.4GHz) Toggle Radio On/Off and Base SSID Operation:  Provision the radio with the following: mode = '802.11b,
    802.11g, 802.11n', bandwidth = 80GHz, channel = not auto.  Using IxVeriwave execute a short UDP test with a
    client set up as follows: 802.11n, bandwidth = 20MHz..  Disable the radio and repeat client test.  Enable the
    radio and repeat client test.  -> The base SSID client can only associated when the radio is enabled.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11n'
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
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
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
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 20MHz bandwidthClient
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Disable the radio
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="off")
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    # The ac card reports 'did not find BSSID' where as the n card reports 'did not find any BSSIDs'
    matchobj = re.match(r'.*(did not find a?n?y? ?BSSID).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "BSSID not found")

    # Enable the radio
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on")
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

@cafe.test_case()
def tc_1052808_24g_80211n_bandwidth_toggle(params):
    """
    @id=1052808
    Description:
    (2.4GHz) Toggle 802.11n Mode Bandwidth: Provision the radio with the following: mode = '802.11b, 802.11g, and
    802.11n', bandwidth = 40MHz, channel = not auto..  Using IxVeriwave execute a short UDP test with a client set up
    as follows: 802.11n, bandwidth = 40MHz.  Repeat test with client set at 20MHz.    Modify the ONT bandwidth to
    20MHz.  Retest 2 times with the two client bandwidth settings.    Modify the ONT bandwidth to 40MHz.  Retest 2
    times with the two client bandwidth settings.  -> (Using WBW2600 WiFi 802.11 a/b/g/n IxVeriwave radio card)
    Clients are allowed to associate in all cases.  When the 40MHz client is connected to the 20MHz radio traffic
    is forwarded in only the Enet -> WiFi direction.
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
    #wifibandwidth = '80 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    #ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth="40 MHz", channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
                                Destination='enet_grp',
                                SettleTime='5',
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
                               BaseIp='192.168.1.100',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.110',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth='40',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # # Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "40 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Change to 20MHz bandwidth on ONT
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth='20 MHz')

    # Verify 40MHz bandwidthClient in WiFi -> ENET direction
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    #
    # In WiFi -> ENET direction the behavior is the client connects bu no throughput allowed.
    # Developed on IxVeriwave 'n' card.  May operate differently on ac card.
    matchobj = re.match(r'.*(No throughput measurement).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "40 MHz Client no traffic in ENET->WiFi direction")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 40MHz bandwidthClient in ENET -> WiFi direction
    ixvwcfg['globalcfg']['Source'] = 'enet_grp'
    ixvwcfg['globalcfg']['Destination'] = 'base_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
         success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "40 MHz Client traffic in WiFi->ENET direction")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    ixvwcfg['globalcfg']['Source'] = 'base_grp'
    ixvwcfg['globalcfg']['Destination'] = 'enet_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
         success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Change back to 40MHz bandwidth on ONT
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth="40 MHz")

    #Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "40 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')

@cafe.test_case()
def tc_665920_24g_80211bgn_client_phy(params):
    """
    @id=665920
    Description:
    (2.4GHz) Radio Mode '802.11b, 802.11g, 802.11n' (20MHz) Client Phy Association: Provision the 2.4GHz radio with
    radio mode '802.11b, 802.11g, 802.11n'.  Using the IxVeriwave associate an 802.11n(20MHz) client and perform a
    short UDP traffic test.  Repeat the test for each of the following client phys: 802.11ag, and 802.11b.  Perform a
    final test with 802.11n, 802.11ag, and 802.11b client types associated simultaneously.  -> All clients are able
    to associate and traffic forwarded.
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
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11b Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'n_grp ag_grp b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11n, ag, b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665921_24g_80211gn_client_phy(params):
    """
    @id=665921
    Description:
    (2.4GHz) Radio Mode '802.11g and 802.11n' (20MHz) Client Phy Association: Provision the 2.4GHz radio with radio
    mode '802.11g and 802.11n'.  Using the IxVeriwave associate an 802.11n(20MHz) client and perform a short UDP
    traffic test.  Repeat the test for each of the following client phys: 802.11ag, and 802.11b.  Perform a final
    test with 802.11n and 802.11ag client types associated simultaneously.  -> Only 802.11n and 802.11ag clients
    associate and forward traffic.  The 802.11B client fails association.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11g and 802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11b Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    matchobj = re.match(r'.*(b_grp.*EAPOL pairwise key installed: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association fails")

    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'n_grp ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11n, ag, b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, mode="802.11b, 802.11g, and 802.11n",
                               channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665922_24g_80211n_client_phy(params):
    """
    @id=665922
    Description:
    (2.4GHz) Radio Mode '802.11n' (20MHz) Client Phy Association: Provision the 2.4GHz radio with radio mode
    '802.11n'.  Using the IxVeriwave associate an 802.11n(20MHz) client and perform a short UDP traffic test.
    Repeat the test for each of the following client phys: 802.11ag, and 802.11b.   -> Only 802.11n client associates
    and forwards traffic.  The 802.11b an 802.11ag clients fail association.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11n'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    matchobj = re.match(r'.*(ag_grp.*Association response: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Verify 802.11ag Client association fails")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11b Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    matchobj = re.match(r'.*(b_grp.*Association response: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Verify 802.11b Client association correctly fails")

    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, mode="802.11b, 802.11g, and 802.11n",
                               channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665923_24g_80211bg_client_phy(params):
    """
    @id=665923
    Description:
    (2.4GHz) Radio Mode '802.11b and 802.11g' Client Phy Association: Provision the 2.4GHz radio with radio mode
    '802.11b and 802.11g'.  Using the IxVeriwave associate an 802.11n(20MHz) client and perform a short UDP traffic
    test.  Repeat the test for each of the following client phys:  802.11ag, and 802.11b.  Perform a final test with
    802.11n, 802.11ag, and 802.11b client types associated simultaneously.  -> All clients are able to associate and
    traffic forwarded.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b and 802.11g'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11b Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'n_grp ag_grp b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11n, ag, b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, mode="802.11b, 802.11g, and 802.11n", channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665924_24g_80211g_client_phy(params):
    """
    @id=665924
    Description:
    (2.4GHz) Radio Mode '802.11g' Client Phy Association: Provision the 2.4GHz radio with radio mode '802.11g'.
    Using the IxVeriwave associate an 802.11n(20MHz) client and perform a short UDP traffic test.  Repeat the test for
    each of the following client phys:  802.11ag, and 802.11b.  Perform a final test with 802.11n and 802.11ag client
    types associated simultaneously.  -> Only 802.11n and 802.11ag clients associate and forward traffic.  The 802.11b
    client fails association.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11g'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11b Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    matchobj = re.match(r'.*(b_grp.*EAPOL pairwise key installed: FAILED).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association fails")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'n_grp ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11n and ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, mode="802.11b, 802.11g, and 802.11n", channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665925_24g_80211b_client_phy(params):
    """
    @id=665925
    Description:
    (2.4GHz) Radio Mode '802.11b' Client Phy Association: Provision the 2.4GHz radio with radio mode '802.11g'.
    Using the IxVeriwave associate an 802.11n(20MHz) client and perform a short UDP traffic test.  Repeat the test for
    each of the following client phys:  802.11ag, and 802.11b.  Perform a final test with 802.11n, 802.11ag, and
    802.11b client types associated simultaneously.  -> All clients are able to associate and traffic forwarded.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = '802.11b'
    wifichannel = '6'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 20MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11b Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'n_grp ag_grp b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11n, ag, b Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, mode='802.11b, 802.11g, and 802.11n', channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1052810_24g_20mhz_channels(params):
    """
    @id=1052810
    Description:
    (2.4GHz) 20 MHz - Manual Channel Select  (US): Provision the 5GHz radio with '802.11b, 802.11g, 802.11n' mode
    and 20MHz bandwidth.  For each selectable channel (1,2,3,4,5,6,7,8,9,10,11) available select the channel and
    verify a 20MHz IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel selected
    clients can be associated and traffic forwarded.

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
    wifichannel = ''
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel='1', powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype)

    # Verify Channel 1 Operation
    ixvwcfg['globalcfg']['Channel'] = '1'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 1 Client association with no throughput loss")
        # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 2 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='2')
    ixvwcfg['globalcfg']['Channel'] = '2'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 2 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 3 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='3')
    ixvwcfg['globalcfg']['Channel'] = '3'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 3 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 4 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='4')
    ixvwcfg['globalcfg']['Channel'] = '4'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 4 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 5 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='5')
    ixvwcfg['globalcfg']['Channel'] = '5'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 5 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 6 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='6')
    ixvwcfg['globalcfg']['Channel'] = '6'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 6 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 7 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='7')
    ixvwcfg['globalcfg']['Channel'] = '7'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 7 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 8 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='8')
    ixvwcfg['globalcfg']['Channel'] = '8'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 8 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 9 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='9')
    ixvwcfg['globalcfg']['Channel'] = '9'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 9 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 10 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='10')
    ixvwcfg['globalcfg']['Channel'] = '10'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 10 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 11 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='11')
    ixvwcfg['globalcfg']['Channel'] = '11'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 11 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1052811_24g_40mhz_channels(params):
    """
    @id=1052811
    Description:
    (2.4GHz) 40 MHz - Manual Channel Select  (US): Provision the 5GHz radio with '802.11b, 802.11g, 802.11n' mode
    and 40MHz bandwidth.  For each selectable channel (1,2,3,4,5,6,7) available select the channel and verify a 40MHz
    IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel selected clients can be
    associated and traffic forwarded.

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
    wifichannel = ''
    wifibandwidth = '40 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '40'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel='1', powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='n_grp',
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
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='40',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype)

    # Verify Channel 1 Operation
    ixvwcfg['globalcfg']['Channel'] = '1'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 1 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 2 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='2')
    ixvwcfg['globalcfg']['Channel'] = '2'
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 2 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 3 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='3')
    ixvwcfg['globalcfg']['Channel'] = '3'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 3 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 4 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='4')
    ixvwcfg['globalcfg']['Channel'] = '4'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 4 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 5 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='5')
    ixvwcfg['globalcfg']['Channel'] = '5'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 5 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 6 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='6')
    ixvwcfg['globalcfg']['Channel'] = '6'
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 6 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 7 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='7')
    ixvwcfg['globalcfg']['Channel'] = '7'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 1:
            success = True
        else:
          success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                             'Channel 7 Client association with < 1% throughput loss')
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth='20 MHz', channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1043401_5g_80211ac_bandwidth_toggle(params):
    """
    @id=1043401
    Description:
    (5GHz) Toggle 802.11ac Mode Bandwidth: Provision the radio with the following: mode = 802.11ac, bandwidth = 80GHz,
    channel = not auto..  Using IxVeriwave execute a short UDP test with a client set up as follows: 802.11ac,
    bandwidth = 80MHz.  Repeat test with client set at 40MHz.  Repeat test with client set at 20MHz.    Modify the
    ONT bandwidth to 40MHz.  Retest 3 times with the three client bandwidth settings.  Modify the ONT bandwidth to
    20MHz.  Retest 3 times with the three client bandwidth settings.    Modify the ONT bandwidth to 40MHz.  Retest 3
    times wiht the three client bandwidth settings.  Modify the ONT bandwidth to 80MHz.  Retest 3 times with the three
    client bandwidths.  -> Clients are allowed to associated only when the client bandwidth is <= the provisioned AP
    channel bandwidth.

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
    #wifibandwidth = '80 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    #ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth="80 MHz", channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
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
                                ChannelBandwidth='80',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 80MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '80'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "80 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "40 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Change to 40MHz bandwidth on ONT
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth="40 MHz")
    #Verify 80MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '80'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    #
    # #     Adapted AP's Bandwidth for Port ('10.83.2.199_card4_port1').
    # # Port's Configured Information follows:
    # #   Bandwidth: 40, Channel: 36, Band: 5000, CenterFrequency: 5190 based on selected bssid: '06:06:31:b4:4f:ea'
    # #
    # #
    # # Completed: Created 1 clients in 0.02 seconds
    # #
    # # Error: VCAL_ERROR_UNMATCHED_CHANNELBANDWIDTH_CLIENT_PORT(-1054) channel-b error.
    # #  Error with mc.write('wifi') in waveapps.py.
    #
    matchobj = re.match(r'.*(VCAL_ERROR_UNMATCHED_CHANNELBANDWIDTH_CLIENT_PORT).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "80 MHz Client association not allowed")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "40 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
         success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Change to 20MHz bandwidth on ONT
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth="20 MHz")

    # Verify 80MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '80'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    matchobj = re.match(r'.*(VCAL_ERROR_UNMATCHED_CHANNELBANDWIDTH_CLIENT_PORT).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "80 MHz Client association not allowed")
    # Clean up remote log directory if one was created
    if result['logdir']:
         delremotefile(ixvw, filename=result['logdir'])

    # Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    matchobj = re.match(r'.*(VCAL_ERROR_UNMATCHED_CHANNELBANDWIDTH_CLIENT_PORT).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "40 MHz Client association not allowed")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Change to 40MHz bandwidth on ONT
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth="40 MHz")

    #Verify 80MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '80'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    matchobj = re.match(r'.*(VCAL_ERROR_UNMATCHED_CHANNELBANDWIDTH_CLIENT_PORT).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "80 MHz Client association not allowed")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    #Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "40 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Change to 80MHz bandwidth on ONT
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth="80 MHz")

    # Verify 80MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '80'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "80 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 40MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "40 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 20MHz bandwidthClient
    ixvwcfg['base_grp']['ChannelBandwidth'] = '20'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "20 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047001_5g_radio_toggle(params):
    """
    @id=1047001
    Description:
    (5GHz) Toggle Radio On/Off and Base SSID Operation:  Provision the radio with the following: mode = 802.11ac,
    bandwidth = 80GHz, channel = not auto.  Using IxVeriwave execute a short UDP test with a client set up as follows:
    802.11ac, bandwidth = 80MHz..  Disable the radio and repeat client test.  Enable the radio and repeat client test.
    -> The base SSID client can only associated when the radio is enabled.
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
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
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
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 80MHz bandwidthClient
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "80 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Disable the radio
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="off")
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    matchobj = re.match(r'.*(did not find BSSID).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                             "BSSID not found")

    # Enable the radio
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on")
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "80 MHz Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665928_5g_80211ac_client_phy(params):
    """
    @id=665928
    Description:
    (5GHz) Radio Mode 802.11ac Client Phy Association: Provision the 5GHz radio with radio mode 802.11ac.  Using the
    IxVeriwave associate an 802.11ac 80MHz client and perform a short UDP traffic test.  Repeat the test 3 additional
    times using the following client phys: 802.11n(20MHz), 802.11ag, and 802.11b.  Perform a final test with
    802.11ac, 802.11n, and 802.11ag client types associated simultaneously. -> 802.11ac, n, and ag clients are always
    able to associated and traffic is forwarded with zero loss.  802.11b client is not supported on Quantenna.
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
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='80',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11ac Client
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ac Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    matchobj = re.match(r'.*(b_grp failed to connect).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association fails")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'ac_grp n_grp ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11ac, n, ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_665929_5g_80211n_client_phy(params):
    """
    @id=665929
    Description:
    (5GHz) Radio Mode 802.11n (20MHz) Client Phy Association: Provision the 5GHz radio with radio mode 802.11n
    (20MHz).  Using the IxVeriwave associate an 802.11ac 20MHz client and perform a short UDP traffic test.
    Repeat the test 3 additional times using the following client phys: 802.11n(20MHz), 802.11ag, and 802.11b.
    Perform a final test with 802.11ac, 802.11n and 802.11ag client types associated simultaneously.  -> 802.11ac,
    802.11n, and ag clients are always able to associated and traffic is forwarded with zero loss.  802.11ac not
    supported when in 802.11n mode.  802.11b client is not supported on Quantenna.

    Note: That the ac client will connect but will negotiated to send at n speeds.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = '802.11n Only'
    wifichannel = '36'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['n_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11n',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['ag_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ag',
                                ChannelBandwidth='n',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['b_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11b',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify 802.11ac Client
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ac Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'n_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11n Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11ag Client
    ixvwcfg['globalcfg']['Source'] = 'ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify 802.11n Client
    ixvwcfg['globalcfg']['Source'] = 'b_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    matchobj = re.match(r'.*(b_grp failed to connect).*', result['console'], re.S)
    if matchobj:
        if matchobj.group(1):
            success = True
        else:
            success = False
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "802.11b Client association fails")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify all clients simultaneously
    ixvwcfg['globalcfg']['Source'] = 'ac_grp n_grp ag_grp'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Simultaneous 802.11ac, n, ag Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, mode="802.11ac and 802.11n", channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047203_5g_80mhz_nondfs_channels(params):
    """
    @id=1047203
    Description:
    (5GHz) 80 MHz - Manual Chan Select with DFS Disabled: Provision the 5GHz radio with 802.11ac mode  and 80MHz
    bandwidth.  DFS is disabled.  For each non-DFS channel (36, 149) available select the channel and verify an
    IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel selected clients can be
    associated and traffic forwarded.

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
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='disable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='36')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 36 Operation
    ixvwcfg['globalcfg']['Channel'] = '36'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 36 Client association with no throughput loss")
        # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 149 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='149')
    ixvwcfg['globalcfg']['Channel'] = '149'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 149 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, dfs='enable')
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047204_5g_80mhz_dfs_channels(params):
    """
    @id=1047204
    Description:
    (5GHz) 80 MHz - Manual Channel Select DFS Channels: Provision the 5GHz radio with 802.11ac mode  and 80MHz
    bandwidth.  DFS is enabled.  For each DFS channel (52, 100, 132) available select the channel and verify an
    IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel selected clients can be
    associated and traffic forwarded.
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
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='enable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='52')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='80',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 52 Operation
    ixvwcfg['globalcfg']['Channel'] = '52'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 52 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 100 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='100')
    ixvwcfg['globalcfg']['Channel'] = '100'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 100 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 132 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='132')
    ixvwcfg['globalcfg']['Channel'] = '132'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 132 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, dfs='enable')
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='auto')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047205_5g_40mhz_nondfs_channels(params):
    """
    @id=1047205
    Description:
    (5GHz) 40 MHz - Manual Channel Select  Non-DFS Channels: Provision the 5GHz radio with 802.11ac mode  and 40MHz
    bandwidth.  DFS is disabled.  For each non-DFS channel (36, 44, 149, 157) available select the channel and verify
    an IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel selected clients can be
    associated and traffic forwarded.

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
    wifibandwidth = '40 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '40'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='disable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='36')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='40',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 36 Operation
    ixvwcfg['globalcfg']['Channel'] = '36'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 36 Client association with no throughput loss")
        # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 44 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='44')
    ixvwcfg['globalcfg']['Channel'] = '44'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 44 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 149 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='149')
    ixvwcfg['globalcfg']['Channel'] = '149'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 149 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 157 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='157')
    ixvwcfg['globalcfg']['Channel'] = '157'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 157 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, dfs='enable')
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047206_5g_40mhz_dfs_channels(params):
    """
    @id=1047206
    Description:
    (5GHz) 40 MHz - Manual Channel Select DFS Channels: Provision the 5GHz radio with 802.11ac mode and 40MHz
    bandwidth.  DFS is enabled.  For each DFS channel (52, 60, 100, 108, 132) available select the channel and
    verify an IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel selected clients
    can be associated and traffic forwarded.
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
    wifichannel = '52'
    wifibandwidth = '40 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '40'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='enable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='52')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='40',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 52 Operation
    ixvwcfg['globalcfg']['Channel'] = '52'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 52 Client association with no throughput loss")
        # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 60 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='60')
    ixvwcfg['globalcfg']['Channel'] = '60'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 60 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 100 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='100')
    ixvwcfg['globalcfg']['Channel'] = '100'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 100 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 108 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='108')
    ixvwcfg['globalcfg']['Channel'] = '108'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 108 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 132 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='132')
    ixvwcfg['globalcfg']['Channel'] = '132'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 132 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth='80 MHz', channel="Auto")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, dfs='enable')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047207_5g_20mhz_nondfs_channels(params):
    """
    @id=1047207
    Description:
    (5GHz) 20 MHz - Manual Channel Select  Non-DFS Channels: Provision the 5GHz radio with 802.11ac mode  and 80MHz
    bandwidth.  DFS is disabled.  For each non-DFS channel (36, 40, 44, 48, 149, 153, 157, 161) available select the
    channel and verify an IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel
    selected clients can be associated and traffic forwarded
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
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='disable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='36')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 36 Operation
    ixvwcfg['globalcfg']['Channel'] = '36'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 36 Client association with no throughput loss")
        # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 40 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='40')
    ixvwcfg['globalcfg']['Channel'] = '40'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 40 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 44 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='44')
    ixvwcfg['globalcfg']['Channel'] = '44'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 44 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 48 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='48')
    ixvwcfg['globalcfg']['Channel'] = '48'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 48 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 149 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='149')
    ixvwcfg['globalcfg']['Channel'] = '149'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 149 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 153 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='153')
    ixvwcfg['globalcfg']['Channel'] = '153'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 153 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 157 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='157')
    ixvwcfg['globalcfg']['Channel'] = '157'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 157 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 161 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='161')
    ixvwcfg['globalcfg']['Channel'] = '161'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 161 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth='80 MHz', channel="Auto")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047208_5g_20mhz_dfs_channels(params):
    """
    @id=1047208
    Description:
    (5GHz) 20 MHz - Manual Channel Select DFS Channels: Provision the 5GHz radio with 802.11ac mode  and 20MHz
    bandwidth.  DFS is enabled.  For each DFS channel (52, 56, 60, 64, 100, 104, 108, 112, 132, 136) available select
    the channel and verify an IxVeriwave client can be associated and execute a brief UDP test.  -> For each channel
    selected clients can be associated and traffic forwarded
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
    wifichannel = '52'
    wifibandwidth = '20 MHz'
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '20'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='enable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='52')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 52 Operation
    ixvwcfg['globalcfg']['Channel'] = '52'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 52 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 56 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='56')
    ixvwcfg['globalcfg']['Channel'] = '56'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 56 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 60 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='60')
    ixvwcfg['globalcfg']['Channel'] = '60'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 60 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 64 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='64')
    ixvwcfg['globalcfg']['Channel'] = '64'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 64 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 100 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='100')
    ixvwcfg['globalcfg']['Channel'] = '100'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 100 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 104 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='104')
    ixvwcfg['globalcfg']['Channel'] = '104'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 104 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 108 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='108')
    ixvwcfg['globalcfg']['Channel'] = '108'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 108 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 112 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='112')
    ixvwcfg['globalcfg']['Channel'] = '112'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 112 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 132 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='132')
    ixvwcfg['globalcfg']['Channel'] = '132'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 132 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 136 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='136')
    ixvwcfg['globalcfg']['Channel'] = '136'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 136 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, bandwidth='80 MHz', channel="Auto")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, dfs='enable')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1047701_5g_80mhz_toggle_channels(params):
    """
    @id=1047701
    Description:
    (5GHz) Toggle Manual Channel Selection between DFS and non-DFS: Provision the 5GHz radio with 802.11ac mode and
    80MHz bandwidth.  DFS is enabled.  Manually provision a non-DFS channel and verify an IxVeriwave client can be
    associated and execute a brief UDP test.  Manually provision a DFS channel and retest client using the new
    channel.  Repeat a third time changing back to a non-DFS channel.   -> For each channel selected clients can be
    associated and traffic forwarded
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
    #ixvwradiophyinttype = '802.11ac'
    ixvwradiobandwidth = '80'

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Configure WiFi values (Assume all values need to be set even if default)
    # Start out with 80MHz setting
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, dfs='enable', powerlevel="100%")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='36')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    #Set IxVeriwave variables
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='ac_grp',
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
    ixvwcfg['ac_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                Dhcp='Enable',
                                Ssid=fsan,
                                phyInterface='802.11ac',
                                ChannelBandwidth='20',
                                Method='WPA-PSK-AES',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify Channel 36 Operation
    ixvwcfg['globalcfg']['Channel'] = '36'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 36 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 100 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='100')
    ixvwcfg['globalcfg']['Channel'] = '100'
    # Need wait time for provisioning to take place
    time.sleep(30)
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 100 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Verify Channel 149 Operation
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel='149')
    ixvwcfg['globalcfg']['Channel'] = '149'
    result = ixvw_advancedbenchtest(ixvw, ixvwcfg)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Benchmark Throughput - "
                                                              "Channel 149 Client association with no throughput loss")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, dfs='enable')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')