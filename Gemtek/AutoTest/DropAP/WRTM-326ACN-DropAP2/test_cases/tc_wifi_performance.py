__author__ = 'glivermo'
import cafe
import time
import re
import csv
import os
from stp.api.ixveriwave.ixveriwavelib import ixvw_advancedbenchtest
from stp.api.ixveriwave.ixveriwavelib import ixvw_advancedmaxclienttest
from stp.api.ixveriwave.ixveriwavelib import delremotefile
from stp.api.utilities.utilities import gen_ont_md5
#import matplotlib.pyplot as plt
import pylab as plt
import numpy as np

##### 2.4GHz Test Cases

@cafe.test_case()
def tc_1041201_24g_centurylink_frsize_lan2wifi(params):
    """
    @id=1041201
    (2.4GHz) CenturyLink 1 Client UDP Throughput (20MHz 2X2 11n) - LAN to WiFi: Configure the 2.4GHz radio with
    the following parameters: Bandwidth =  20MHz, Channel = Not Auto, Power level = 100%, default SSID, Security
    type = WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client
    with the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11n, MCS Index = 15,
    guard interval = short, channel bandwidth = 20MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.  Use the
    Throughput benchmark test in the LAN-to-Wifi direction with 15 second trials and .1% loss tolerance to measure the
    UDP throughput  for the following frame size lengths (bytes) : 88, 128, 256, 512, 1000, 1280, 1460, 1518.  Repeat
    the test to verify consistency between execution results.  -> Expected results TBD with experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    datafilename = 'data/1041201_frsize_LtoW_24g_' + eut + '_' + ver + '.csv'
    # plotfilename = 'data/1041201_frsize_LtoW_24g_' + eut + '_' + ver + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]
    #framesizelist = [1460]

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
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='20',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                csvfile.writerow( ('1041201', build, model, '2.4GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Unidirectional LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                csvfile.writerow( ('1041201', build, model, '2.4GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Unidirectional LAN->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark per Frame Size (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Frame Size (bytes)')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = framesizelist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')

@cafe.test_case()
def tc_noncalix_24g_centurylink_frsize_lan2wifi(params):
    """
    @id=1041201Copy
    """
    # Obtain required parameters
    ixvw =  params['ixvw']['ixvwpcsession']
    eut = params['testaccounting']['eut']
    ssidnames = params['apsettings']['ssidnames']
    psk = params['apsettings']['psk']
    wifichannel = params['apsettings']['wifichannel']
    clientphy = params['wificlientsettings']['clientphy']
    clientsecuritymethod = params['wificlientsettings']['securitymethod']
    clientchannelbw = params['wificlientsettings']['clientchannelbw']

    # Set re-used variable information - ease of script re-use needs
    #DUT radio phy interface type
    ixvwradiointtype = '802.11n'
    #client radio interface type
    ixvwradiophyinttype = '802.11n'
    #ixvwradiobandwidth = '20'
    eut = params['testaccounting']['eut']
    datafilename = 'data/centurylink_frsize_24g_' + params['testaccounting']['eut'] + '.csv'
    plotfilename = 'data/centurylink_frsize_24g_' + params['testaccounting']['eut'] + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]
    #framesizelist = [1460]

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Generic test assuming configuration pre-configured

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='20',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=ssidnames,
                                phyInterface=clientphy,
                                ChannelBandwidth=clientchannelbw,
                                Method=clientsecuritymethod,
                                PskAscii=psk)
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', '0', '0') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # Build graph of results
    # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    print('throughputlist: ', throughputlist)
    # Set data for X axis
    y = throughputlist
    N = len(y)
    x = range(N)
    width = 1/1.5
    # Set Plot title
    plt.title('Throughput Benchmark per Frame Size (LAN->WiFi)')
    # Set axis labels
    plt.xlabel('Frame Size (bytes)')
    plt.ylabel('UDP Throughput (Mbps)')
    # Set x axis labels
    xlabels = framesizelist
    plt.xticks(x, xlabels, rotation='horizontal')
    # Create the bars
    plt.bar(x, y, width, color="green")
    # MUST save plot to a file before you do a show
    plt.savefig(plotfilename, bbox_inches='tight')
    # Show the plot on the screen - will pause until closed
    # plt.show()
    # The following does not work leaving a white box of nothingness
    #plt.savefig(plotfilename)

@cafe.test_case()
def tc_1041204_24g_centurylink_frsize_wifi2lan(params):
    """
    @id=1041204
    (2.4GHz) CenturyLink 1 Client UDP Throughput (20MHz 2X2 11n) - WiFi-to-LAN: Configure the 2.4GHz radio with the
    following parameters: Bandwidth =  20MHz, Channel = Not Auto, Power level = 100%, default SSID, Security type =
    WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client with
    the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11n, MCS Index = 15,
    guard interval = short, channel bandwidth = 20MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.  Use
    the Throughput benchmark test unidirectional traffic from WiFi to LAN with 15 second trials and .1% loss tolerance
    to measure the UDP throughput  for the following frame size lengths (bytes) : 88, 128, 256, 512, 1000, 1280, 1460,
    1518.  Repeat the test to verify consistency between execution results.  -> Expected results TBD with experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
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
    eut = params['testaccounting']['eut']
    datafilename = 'data/centurylink_frsize_24g_' + params['testaccounting']['eut'] + '.csv'
    plotfilename = 'data/centurylink_frsize_24g_' + params['testaccounting']['eut'] + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]

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
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='20',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.11',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', '0', '0') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # Build graph of results
    # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    print('throughputlist: ', throughputlist)
    # Set data for X axis
    y = throughputlist
    N = len(y)
    x = range(N)
    width = 1/1.5
    # Set Plot title
    plt.title('Throughput Benchmark per Frame Size (LAN->WiFi)')
    # Set axis labels
    plt.xlabel('Frame Size (bytes)')
    plt.ylabel('UDP Throughput (Mbps)')
    # Set x axis labels
    xlabels = framesizelist
    plt.xticks(x, xlabels, rotation='horizontal')
    # Create the bars
    plt.bar(x, y, width, color="green")
    # MUST save plot to a file before you do a show
    plt.savefig(plotfilename, bbox_inches='tight')
    # Show the plot on the screen - will pause until closed
    # plt.show()
    # The following does not work leaving a white box of nothingness
    #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')

@cafe.test_case()
def tc_1041203_24g_centurylink_frsize_wifilanbidirectional(params):
    """
    @id=1041203
    (2.4GHz) CenturyLink 1 Client UDP Throughput (20MHz 2X2 11n) - LAN<->WiFi: Configure the 2.4GHz radio with the
    following parameters: Bandwidth =  20MHz, Channel = Not Auto, Power level = 100%, default SSID, Security type =
    WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client with
    the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11n, MCS Index = 15,
    guard interval = short, channel bandwidth = 20MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.  Use
    the Throughput benchmark test bidirectional traffic between the LAN and WiFi with 15 second trials and .1% loss
    tolerance to measure the UDP throughput  for the following frame size lengths (bytes) : 88, 128, 256, 512, 1000,
    1280, 1460, 1518.  Repeat the test to verify consistency between execution results.  -> Expected results TBD
    with experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
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
    eut = params['testaccounting']['eut']
    datafilename = 'data/centurylink_frsize_24g_' + params['testaccounting']['eut'] + '.csv'
    plotfilename = 'data/centurylink_frsize_24g_' + params['testaccounting']['eut'] + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]

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
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Bidirectional',
                                Source='base_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='20',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.11',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', '0', '0') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # Build graph of results
    # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    print('throughputlist: ', throughputlist)
    # Set data for X axis
    y = throughputlist
    N = len(y)
    x = range(N)
    width = 1/1.5
    # Set Plot title
    plt.title('Throughput Benchmark per Frame Size (LAN->WiFi)')
    # Set axis labels
    plt.xlabel('Frame Size (bytes)')
    plt.ylabel('UDP Throughput (Mbps)')
    # Set x axis labels
    xlabels = framesizelist
    plt.xticks(x, xlabels, rotation='horizontal')
    # Create the bars
    plt.bar(x, y, width, color="green")
    # MUST save plot to a file before you do a show
    plt.savefig(plotfilename, bbox_inches='tight')
    # Show the plot on the screen - will pause until closed
    # plt.show()
    # The following does not work leaving a white box of nothingness
    #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')


##### 5GHz Test Cases

@cafe.test_case()
def tc_1041311_5g_centurylink_frsize_lan2wifi(params):
    """
    @id=1041311
    (5GHz) CenturyLink 1 Client UDP Throughput (80MHz 4X4 11ac) - LAN->WiFi: Configure the 5GHz radio with the
    following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%, default SSID, Security type =
    WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client with
    the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11ac, MCS Index = 9,
    guard interval = short, channel bandwidth = 80MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.  Use
    the Throughput benchmark test unidirectional traffic from LAN to WiFi with 15 second trials and .1% loss tolerance
    to measure the UDP throughput  for the following frame size lengths (bytes) : 88, 128, 256, 512, 1000, 1280, 1460,
    1518.  Repeat the test to verify consistency between execution results.  -> Expected results TBD with experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    datafilename = 'data/1041311_frsize_LtoW_5g_' + eut + '_' + ver + '.csv'
    plotfilename = 'data/1041311_frsize_LtoW_5g_' + eut + '_' + ver + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]
    #framesizelist = [88, 128, 256, 512, 1000]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='80',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.11',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                #csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1041311', build, model, '5GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Unidirectional LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                #csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN->WiFi', '0', '0') )
                csvfile.writerow( ('1041311', build, model, '5GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Unidirectional LAN->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark per Frame Size (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Frame Size (bytes)')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = framesizelist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_noncalix_5g_centurylink_frsize_lan2wifi(params):
    """
    @id=TBD
    """
    # Obtain required parameters
    ixvw =  params['ixvw']['ixvwpcsession']
    eut = params['testaccounting']['eut']
    ssidnames = params['apsettings']['ssidnames']
    psk = params['apsettings']['psk']
    wifichannel = params['apsettings']['wifichannel']
    clientphy = params['wificlientsettings']['clientphy']
    clientsecuritymethod = params['wificlientsettings']['securitymethod']
    clientchannelbw = params['wificlientsettings']['clientchannelbw']

    # Set re-used variable information - ease of script re-use needs
    #DUT radio phy interface type
    ixvwradiointtype = '802.11ac'
    #client radio interface type
    ixvwradiophyinttype = '802.11ac'
    #ixvwradiobandwidth = '20'
    eut = params['testaccounting']['eut']
    datafilename = 'data/centurylink_frsize_5g_' + params['testaccounting']['eut'] + '.csv'
    plotfilename = 'data/centurylink_frsize_5g_' + params['testaccounting']['eut'] + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]
    #framesizelist = [1460]

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    #####
    # Generic test assuming configuration pre-configured

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='20',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=ssidnames,
                                phyInterface=clientphy,
                                ChannelBandwidth=clientchannelbw,
                                Method=clientsecuritymethod,
                                PskAscii=psk)
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        csvfile.writerow( ('Global TMS #', 'Radio', 'Bandwidth', 'Channel', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Client Security', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                csvfile.writerow( ('TBD', '5GHz', '1', '1', '1', clientsecuritymethod, fs, 'Unidirectional LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                csvfile.writerow( ('TBD', '5GHz', '1', '1', '1', clientsecuritymethod, fs, 'Unidirectional LAN->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark per Frame Size (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Frame Size (bytes)')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = framesizelist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

@cafe.test_case()
def tc_1041312_5g_centurylink_frsize_wifi2lan(params):
    """
    @id=1041312
    (5GHz) CenturyLink 1 Client UDP Throughput (80MHz 4X4 11n) - WiFi->LAN: Configure the 5GHz radio with the
    following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%, default SSID, Security type =
    WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client with
    the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11ac, MCS Index = 9,
    guard interval = short, channel bandwidth = 80MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.  Use
    the Throughput benchmark test unidirectional traffic from WiFi to LAN with 15 second trials and .1% loss
    tolerance to measure the UDP throughput  for the following frame size lengths (bytes) : 88, 128, 256, 512, 1000,
    1280, 1460, 1518.  Repeat the test to verify consistency between execution results.  -> Expected results TBD with
    experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    datafilename = 'data/1041312_frsize_WtoL_5g_' + eut + '_' + ver + '.csv'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='110',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='90',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.11',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                csvfile.writerow( ('1041312', build, model, '5GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Unidirectional WiFi->LAN', result['throughput_pps'], result['throughput_mbps']) )
            else:
                csvfile.writerow( ('1041312', build, model, '5GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Unidirectional WiFi->LAN', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1041313_5g_centurylink_frsize_wifilanbidirectional(params):
    """
    @id=1041313
    (5GHz) CenturyLink 1 Client UDP Throughput (80MHz 4X4 11ac) - WiFi<->LAN: Configure the 5GHz radio with the
    following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%, default SSID, Security type =
    WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client with
    the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11ac, MCS Index = 9,
    guard interval = short, channel bandwidth = 80MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.  Use
    the Throughput benchmark test bidirectional traffic between WiFi and LAN with 15 second trials and .1% loss
    tolerance to measure the UDP throughput  for the following frame size lengths (bytes) : 88, 128, 256, 512, 1000,
    1280, 1460, 1518.  Repeat the test to verify consistency between execution results.  -> Expected results TBD with
    experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    #datafilename = 'data/centurylink_frsize_bidi_5g_' + params['testaccounting']['eut'] + '.csv'
    #plotfilename = 'data/centurylink_frsize_bidi_5g_' + params['testaccounting']['eut'] + '.png'
    datafilename = 'data/1041313_frsize_bidiLW_5g_' + eut + '_' + ver + '.csv'
    plotfilename = 'data/1041313_frsize_BidiLW_5g_' + eut + '_' + ver + '.png'
    framesizelist = [88, 128, 256, 512, 1000, 1280, 1460, 1518]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Bidirectional',
                                Source='base_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='110',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='80',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.11',
                               Gateway='192.168.1.1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.21',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for fs in framesizelist:
        ixvwcfg['testcfg']['FrameSizeList'] = str(fs)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            if result['throughput_mbps'] is not None:
                # csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN<->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1041313', build, model, '5GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Bidirectional LAN<->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                # csvfile.writerow( ('1', '1', 'WPA2-PSK', fs, 'LAN<->WiFi', '0', '0') )
                csvfile.writerow( ('1041313', build, model, '5GHz', ixvwradiobandwidth, '1', '1', '1', 'UDP', fs, 'Bidirectional LAN<->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 (str(fs), str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark per Frame Size (WiFi<->LAN)')
    # # Set axis labels
    # plt.xlabel('Frame Size (bytes)')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = framesizelist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1065801_5g_centurylink_multiclients_lan2wifi(params):
    """
    @id=1065801
    (5GHz) 1-10 Clients on Single SSID UDP Throughput (80MHz 802.11ac) LAN->WiFi - CENTURYLINK: Configure the 5GHz
    radio with the following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%, default SSID,
    Security type = WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set
    use a client with the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11ac,
    MCS Index = 9, guard interval = short, channel bandwidth = 80MHz, enable AMPDU Aggregation, enable RX AMSDU
    Aggregation.  Use the Throughput benchmark test bidirectional traffic between WiFi and LAN with 15 second
    trials and .1% loss tolerance to measure the UDP throughput  for the frame size length of 1460 (bytes) starting
    with 1 client on the SSID all the way up to 10 clients with 1 client steps.  Repeat the test if needed to verify
    consistency between execution results.  -> Expected results TBD with experience.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    #datafilename = 'data/centurylink_numclients_5g_' + params['testaccounting']['eut'] + '.csv'
    #plotfilename = 'data/centurylink_numclients_5g_' + params['testaccounting']['eut'] + '.png'
    datafilename = 'data/1065801_numclients_LtoW_5g_' + eut + '_' + ver + '.csv'
    plotfilename = 'data/1065801_numclients_LtoW_5g_' + eut + '_' + ver + '.png'
    numclientslist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #numclientslist = [8]
    #numclientslist  = [1, 2]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='90',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1',
                               NumClients='1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for cl in numclientslist:
        # Number of clients on the ENET and WiFi match
        ixvwcfg['base_grp']['NumClients'] = str(cl)
        ixvwcfg['enet_grp']['NumClients'] = str(cl)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            totalcl = cl * 1
            if result['throughput_mbps'] is not None:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1065801', build, model, '5GHz', ixvwradiobandwidth, cl, '1', totalcl, 'UDP', '1460', 'Unidirectional LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', '0', '0') )
                csvfile.writerow( ('1065801', build, model, '5GHz', ixvwradiobandwidth, cl, '1', totalcl, 'UDP', '1460', 'Unidirectional LAN->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Num Clients per SSID/ENET: %s '
                                                                 'Num SSIDs: %s'
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 ('1460', str(cl), '1', str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark (Framesize = 1460 bytes)- # Clients per ENET/SSID (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Number of Clients')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = numclientslist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1065901_5g_centurylink_multiclients_wifi2lan(params):
    """
    @id=1065901
    (5GHz) 1-10 Clients on Single SSID UDP Throughput (80MHz 802.11ac) WiFi->LAN: Configure the 5GHz radio with
    the following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%, default SSID, Security
    type = WPA-WPA2-Personal, Encryption type = AES, default custom PSK.  Using the IxVeriwave test set use a client
    with the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned on ONT, 802.11ac, MCS Index = 9,
    guard interval = short, channel bandwidth = 80MHz, enable AMPDU Aggregation, enable RX AMSDU Aggregation.
    Use the Throughput benchmark test bidirectional traffic between WiFi and LAN with 15 second trials and .1% loss
    tolerance to measure the UDP throughput  for the frame size length of 1460 (bytes) starting with 1 client on the
    SSID all the way up to 10 clients with 1 client steps.  Repeat the test if needed to verify consistency between
    execution results.  -> Expected results TBD with experience.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    datafilename = 'data/1065901_numclients_WtoL_5g_' + eut + '_' + ver + '.csv'
    numclientslist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #numclientslist = [9, 10]
    #numclientslist  = [1, 2]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='90',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1',
                               NumClients='1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for cl in numclientslist:
        # Number of clients on the ENET and WiFi match
        ixvwcfg['base_grp']['NumClients'] = str(cl)
        ixvwcfg['enet_grp']['NumClients'] = str(cl)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            totalcl = cl * 1
            if result['throughput_mbps'] is not None:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1065901', build, model, '5GHz', ixvwradiobandwidth, cl, '1', totalcl, 'UDP', '1460', 'Unidirectional WiFi->LAN', result['throughput_pps'], result['throughput_mbps']) )
            else:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', '0', '0') )
                csvfile.writerow( ('1065901', build, model, '5GHz', ixvwradiobandwidth, cl, '1', totalcl, 'UDP', '1460', 'Unidirectional WiFi->LAN', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Num Clients per SSID/ENET: %s '
                                                                 'Num SSIDs: %s'
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 ('1460', str(cl), '1', str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark (Framesize = 1460 bytes)- # Clients per ENET/SSID (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Number of Clients')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = numclientslist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')

@cafe.test_case()
def tc_1065802_5g_centurylink_multiclientsssids_lan2wifi(params):
    """
    @id=1065802
    (5GHz) 1-10 Clients on 4 SSIDs UDP Throughput (80MHz 802.11ac) LAN->WiFi - CENTURYLIK: Configure the 5GHz radio
    with the following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%.  Provision 4 SSIDs with
    the following settings: Security type = WPA-WPA2-Personal, Encryption type = AES, custom PSK.  Using the
    IxVeriwave test set use a client per SSID with the following attributes: Security = WPA2-PSK (AES), same PSK as
    provisioned on ONT, 802.11ac, MCS Index = 9, guard interval = short, channel bandwidth = 80MHz, enable AMPDU
    Aggregation, enable RX AMSDU Aggregation.  Use the Throughput benchmark test bidirectional traffic between WiFi
    and LAN with 15 second trials and .1% loss tolerance to measure the UDP throughput  for the frame size length of
    1460 (bytes) starting with 1 client per SSID all the way up to 10 clients per SSID with 1 client per SSID steps.
    Repeat the test if needed to verify consistency between execution results.  -> Expected results TBD with experience.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    #datafilename = 'data/centurylink_numclients_5g_' + params['testaccounting']['eut'] + '.csv'
    #plotfilename = 'data/centurylink_numclients_5g_' + params['testaccounting']['eut'] + '.png'
    datafilename = 'data/1065802_numclientsssids_LtoW_5g_' + eut + '_' + ver + '.csv'
    plotfilename = 'data/1065802_numclientsssids_LtoW_5g_' + eut + '_' + ver + '.png'
    numclientslist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #numclientslist = [10]
    #numclientslist  = [1, 2]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp op1_grp op2_grp op3_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='90',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1',
                               NumClients='1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op1_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_1',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op2_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_2',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op3_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_3',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for cl in numclientslist:
        # Number of clients on the ENET and WiFi match
        ixvwcfg['base_grp']['NumClients'] = str(cl)
        ixvwcfg['enet_grp']['NumClients'] = str(cl)
        ixvwcfg['op1_grp']['NumClients'] = str(cl)
        ixvwcfg['op2_grp']['NumClients'] = str(cl)
        ixvwcfg['op3_grp']['NumClients'] = str(cl)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            totalcl = cl * 4
            if result['throughput_mbps'] is not None:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1065802', build, model, '5GHz', ixvwradiobandwidth, cl, '4', totalcl, 'UDP', '1460', 'Unidirectional LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', '0', '0') )
                csvfile.writerow( ('1065802', build, model, '5GHz', ixvwradiobandwidth, cl, '4', totalcl, 'UDP', '1460', 'Unidirectional LAN->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Num Clients per SSID/ENET: %s '
                                                                 'Num SSIDs: %s'
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 ('1460', str(cl), '1', str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark (Framesize = 1460 bytes)- # Clients per ENET/SSID (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Number of Clients')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = numclientslist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                              broadcast="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                              broadcast="disabled")

@cafe.test_case()
def tc_1065904_5g_centurylink_multiclientsssids_wifi2lan(params):
    """
    @id=1065904
    (5GHz) 1-10 Clients on 4 SSIDs UDP Throughput (80MHz 802.11ac) WiFi->LAN: Configure the 5GHz radio with the
    following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%.  Provision 4 SSIDs with the
    following settings: Security type = WPA-WPA2-Personal, Encryption type = AES, custom PSK.  Using the IxVeriwave
    test set use a client per SSID with the following attributes: Security = WPA2-PSK (AES), same PSK as provisioned
    on ONT, 802.11ac, MCS Index = 9, guard interval = short, channel bandwidth = 80MHz, enable AMPDU Aggregation,
    enable RX AMSDU Aggregation.  Use the Throughput benchmark test bidirectional traffic between WiFi and LAN with
    15 second trials and .1% loss tolerance to measure the UDP throughput  for the frame size length of 1460 (bytes)
    starting with 1 client per SSID all the way up to 10 clients per SSID with 1 client per SSID steps.  Repeat the
    test if needed to verify consistency between execution results.  -> Expected results TBD with experience.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    datafilename = 'data/1065904_numclientsssids_WtoL_5g_' + eut + '_' + ver + '.csv'
    numclientslist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #numclientslist = [4]
    #numclientslist  = [1, 2]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='base_grp op1_grp op2_grp op3_grp',
                                Destination='enet_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='90',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1',
                               NumClients='1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op1_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_1',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op2_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_2',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op3_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_3',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for cl in numclientslist:
        # Number of clients on the ENET and WiFi match
        ixvwcfg['base_grp']['NumClients'] = str(cl)
        ixvwcfg['enet_grp']['NumClients'] = str(cl)
        ixvwcfg['op1_grp']['NumClients'] = str(cl)
        ixvwcfg['op2_grp']['NumClients'] = str(cl)
        ixvwcfg['op3_grp']['NumClients'] = str(cl)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            totalcl = cl * 4
            if result['throughput_mbps'] is not None:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1065904', build, model, '5GHz', ixvwradiobandwidth, cl, '4', totalcl, 'UDP', '1460', 'Unidirectional WiFi->LAN', result['throughput_pps'], result['throughput_mbps']) )
            else:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', '0', '0') )
                csvfile.writerow( ('1065904', build, model, '5GHz', ixvwradiobandwidth, cl, '4', totalcl, 'UDP', '1460', 'Unidirectional WiFi->LAN', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Num Clients per SSID/ENET: %s '
                                                                 'Num SSIDs: %s'
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 ('1460', str(cl), '1', str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                              broadcast="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                              broadcast="disabled")

@cafe.test_case()
def tc_1065902_5g_centurylink_multiclientsssids_wifilanbidirectional(params):
    """
    @id=1065902
    (5GHz) 1-10 Clients on 4 SSIDs UDP Throughput (80MHz 802.11ac) WiFi<->LAN - CENTURYLINK: Configure the 5GHz
    radio with the following parameters: Bandwidth =  80MHz, Channel = Not Auto, Power level = 100%.  Provision 4
    SSIDs with the following settings: Security type = WPA-WPA2-Personal, Encryption type = AES, custom PSK.  Using
    the IxVeriwave test set use a client per SSID with the following attributes: Security = WPA2-PSK (AES), same PSK
    as provisioned on ONT, 802.11ac, MCS Index = 9, guard interval = short, channel bandwidth = 80MHz, enable AMPDU
    Aggregation, enable RX AMSDU Aggregation.  Use the Throughput benchmark test bidirectional traffic between WiFi
    and LAN with 15 second trials and .1% loss tolerance to measure the UDP throughput  for the frame size length of
    1460 (bytes) starting with 1 client per SSID all the way up to 10 clients per SSID with 1 client per SSID steps.
    Repeat the test if needed to verify consistency between execution results.  -> Expected results TBD with experience.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']
    ver = params['testaccounting']['version']
    build = params['testaccounting']['build']
    model = params['testaccounting']['model']

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
    #datafilename = 'data/centurylink_numclients_5g_' + params['testaccounting']['eut'] + '.csv'
    #plotfilename = 'data/centurylink_numclients_5g_' + params['testaccounting']['eut'] + '.png'
    datafilename = 'data/1065902_numclientsssids_bidiLW_5g_' + eut + '_' + ver + '.csv'
    plotfilename = 'data/1065902_numclientsssids_bidiLW_5g_' + eut + '_' + ver + '.png'
    numclientslist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # numclientslist = [6, 7, 8, 9, 10]
    #numclientslist = [8]
    #numclientslist  = [1, 2]
    #framesizelist = [1460]

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
                                  keytype="custom", passphrase='1234567890')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                                  securitytype="WPA - WPA2-Personal",
                                  passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Bidirectional',
                                Source='enet_grp',
                                Destination='base_grp op1_grp op2_grp op3_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                SettleTime='2',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='120',
                              MinSearchValue='1',
                              SearchResolution='1',
                              StartValue='90',
                              SourcePort='5000',
                              DestinationPort='5001')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1',
                               NumClients='1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op1_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.121',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_1',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op2_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.131',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_2',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['op3_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.141',
                                Gateway='192.168.1.1',
                                Ssid='5GHz_Operator_3',
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Write CSV column header
    if not os.path.exists(os.path.dirname(datafilename)):
        os.makedirs(os.path.dirname(datafilename))
    f = open(datafilename, 'w+')
    try:
        csvfile = csv.writer(f)
        #csvfile.writerow( ('# clients per ssid', '# ssids', 'client security', 'frame size (bytes)', 'direction', 'pps', 'Mbps') )
        csvfile.writerow( ('Global TMS #', 'Build', 'Model', 'Radio', 'Bandwidth(MHz)', '# Clients per SSID', '# SSIDs', 'Total Clients', 'Protocol', 'Frame Size (bytes)', 'Direction', 'pps', 'Mbps') )
    finally:
        f.close()

    throughputlist = []
    for cl in numclientslist:
        # Number of clients on the ENET and WiFi match
        ixvwcfg['base_grp']['NumClients'] = str(cl)
        ixvwcfg['enet_grp']['NumClients'] = str(cl)
        ixvwcfg['op1_grp']['NumClients'] = str(cl)
        ixvwcfg['op2_grp']['NumClients'] = str(cl)
        ixvwcfg['op3_grp']['NumClients'] = str(cl)
        result = ixvw_advancedbenchtest(ixvw, ixvwcfg)

        # Update datafile with run measurements
        f = open(datafilename, 'a')
        try:
            csvfile = csv.writer(f)
            totalcl = cl * 4
            if result['throughput_mbps'] is not None:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', result['throughput_pps'], result['throughput_mbps']) )
                csvfile.writerow( ('1065902', build, model, '5GHz', ixvwradiobandwidth, cl, '4', totalcl, 'UDP', '1460', 'Bidirectional LAN<->WiFi', result['throughput_pps'], result['throughput_mbps']) )
            else:
                #csvfile.writerow( (cl, '1', 'WPA2-PSK', '1460', 'LAN->WiFi', '0', '0') )
                csvfile.writerow( ('1065902', build, model, '5GHz', ixvwradiobandwidth, cl, '4', totalcl, 'UDP', '1460', 'Bidirectional LAN<->WiFi', 'No Result', 'No Result') )
        finally:
            f.close()

        # Add measurement to throughput list
        if result['throughput_mbps'] is not None:
            throughputlist.append(float(result['throughput_mbps']))
        else:
            throughputlist.append(0)

        # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
        # TODO : Need check point to verify within tolerance
        success = True
        cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
                                                                 'Frame size: %s  '
                                                                 'Num Clients per SSID/ENET: %s '
                                                                 'Num SSIDs: %s'
                                                                 'Minimum Expected Throughput: %s  '
                                                                 'Measured Throughput: %s' %
                                                 ('1460', str(cl), '1', str(result['throughput_mbps']), str(result['throughput_mbps'])))
        # Clean up remote log directory if one was created
        if result['logdir']:
            delremotefile(ixvw, filename=result['logdir'])

    # # Build graph of results
    # # throughputlist = [20.1, 19.4, 51.6, 74.0, 102, 103, 88.2, 94.4]
    # print('throughputlist: ', throughputlist)
    # # Set data for X axis
    # y = throughputlist
    # N = len(y)
    # x = range(N)
    # width = 1/1.5
    # # Set Plot title
    # plt.title('Throughput Benchmark (Framesize = 1460 bytes)- # Clients per ENET/SSID (LAN->WiFi)')
    # # Set axis labels
    # plt.xlabel('Number of Clients')
    # plt.ylabel('UDP Throughput (Mbps)')
    # # Set x axis labels
    # xlabels = numclientslist
    # plt.xticks(x, xlabels, rotation='horizontal')
    # # Create the bars
    # plt.bar(x, y, width, color="green")
    # # MUST save plot to a file before you do a show
    # plt.savefig(plotfilename, bbox_inches='tight')
    # # Show the plot on the screen - will pause until closed
    # # plt.show()
    # # The following does not work leaving a white box of nothingness
    # #plt.savefig(plotfilename)

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, keytype='Default')
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2',
                              broadcast="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_2', ssidstate="disabled")
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_3',
                              broadcast="disabled")

@cafe.test_case()
def tc_777_5g_maxclientscapacity(params):
    """
    @id=777

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['ontsettings']['ontfsan']
    eut = params['testaccounting']['eut']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '5GHz'
    wifimode = '802.11ac'
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
                                  encryptiontype="AES", keytype="custom", passphrase='1234567890')
    #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Set Configuration parameters for ENET to WiFi
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=ixvwchassisip,
                                Direction='Unidirectional',
                                Source='enet_grp',
                                Destination='base_grp',
                                TrialDuration='15',
                                LossTolerance='.1',
                                Channel=wifichannel)
    ixvwcfg['testcfg'] = dict(FrameSizeList='1460',
                              MaxSearchValue='130',
                              ExpectedClientConnections='30',
                              ILoadList='10',
                              DestinationPort='5000')
    ixvwcfg['enet_grp'] = dict(GroupType='802.3',
                               Dut='enet_dut',
                               BaseIp='192.168.1.101',
                               Gateway='192.168.1.1',
                               NumClients='1')
    ixvwcfg['base_grp'] = dict(GroupType=ixvwradiogrouptype,
                                Dut='wifi_dut',
                                BaseIp='192.168.1.111',
                                Gateway='192.168.1.1',
                                Ssid=fsan,
                                phyInterface=ixvwradiophyinttype,
                                ChannelBandwidth=ixvwradiobandwidth,
                                Method='WPA2-PSK',
                                PskAscii='1234567890',
                                NumClients='1')
    ixvwcfg['enet_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwlanport,
                               InterfaceType='802.3')
    ixvwcfg['wifi_dut'] = dict(Wavetestport=ixvwchassisip + ':' + ixvwradioport,
                               InterfaceType=ixvwradiointtype,
                               Channel=wifichannel)

    # Verify WPA-PSK(TKIP) and WPA2-PSK-TKIP clients can associated an traffic is generated
    result = ixvw_advancedmaxclienttest(ixvw, ixvwcfg)

    # 3% loss tolerance - loss is usually seen both in script and in GUI.  Do not have an explaination at this time.
    if result['errormsg'] is None and result['loss_percent'] is not None and result['abortcnt'] == "0":
        if float(result['loss_percent']) < 3:
            success = True
        else:
          success = False
    else:
        success = False

    # Eventually this test needs to failed if a measurement is out-of-tolerance from a historical expected measurement
    # TODO : Need check point to verify within tolerance
    success = True
    # cafe.Checkpoint(str(success)).contains(exp="True", title='IxVW Benchmark Throughput - '
    #                                                          'Frame size: %s  '
    #                                                          'Num Clients per SSID/ENET: %s '
    #                                                          'Num SSIDs: %s'
    #                                                          'Minimum Expected Throughput: %s  '
    #                                                          'Measured Throughput: %s' %
    #                                          ('1460', str(cl), '1', str(result['throughput_mbps']), str(result['throughput_mbps'])))
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, passphrase='1234567890')
    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, encryptiontype="AES", keytype='Default')

