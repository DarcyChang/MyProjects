__author__ = 'gliverm'

from cafe.core.db import teststep
from cafe.core.logger import CLogger as Logger
from cafe.resp.response_map import ResponseMap
from cafe.sessions.winexe import WinExeSession
from cafe.sessions.tcl_remote import TCLRemoteShell
import time
import re
import random

logger = Logger(__name__)
debug = logger.debug
error = logger.error

"""
API Library: ixveriwavelib
Description:
    This library contains all functions used to interact with the IxVeriwave test set.  Automation built to interact
    with a remote Windows OS managment machine.  The library contains internal functions and user facing functions.
"""

def __analyze_results(ixvw_output):
    """
    Description:
        Analyze the results from Ixveriwave to return interesting data in dictionary form
    Parameters:
        ixvw_output : (str) Output from an IxVeriwave test

    Return: (dict) Dictionary of extracted information
    """
    result = {}

    # Extract log directory
    matchobj = re.match(r'.*#### Full logs are at:(.+)/output.log.*', ixvw_output, re.S)
    if matchobj:
        if matchobj.group(1):
            result['logdir'] = matchobj.group(1)
        else:
            result['logdir'] = None
    else:
        result['logdir'] = None

    # TODO: The loss extraction needs to be rethought.  Should look for the last PASS statement
    # TODO: The loss extraction needs to be rethought.  Should look for last FAIL statement.
    #  Extract last loss report information - I don't like this since can have multiple tests
    matchobj = re.match(r'.* Achieved load of [\d\.]* with ([\d\.]*)% loss .*', ixvw_output, re.S)
    if matchobj:
        if matchobj.group(1):
            result['loss_percent'] = matchobj.group(1)
        else:
            result['loss_percent'] = None
    else:
        result['loss_percent'] = None

    # Extract Completed Throughput pps and Mbps
    # Completed: Throughput for 1460 byte packets is 8374.3 pkts/sec (or 97.8M bits/sec)
    matchobj = re.match(r'.*Completed: Throughput for (\d*) byte packets is ([\d\.]*) pkts/sec \(or ([\d\.]*)M bits/sec\).*', ixvw_output, re.S)
    if matchobj:
        if matchobj.group(1):
            result['framesize_byte'] = matchobj.group(1)
        else:
            result['framesize_byte'] = None
        if matchobj.group(2):
            result['throughput_pps'] = matchobj.group(2)
        else:
            result['throughput_pps'] = None
        if matchobj.group(3):
            result['throughput_mbps'] = matchobj.group(3)
        else:
            result['throughput_mbps'] = None
    else:
        result['throughput_pps'] = None
        result['throughput_mbps'] = None

    # Extract Completed Throughput pps and Gbps
    # Completed: Throughput for 1460 byte packets is 8374.3 pkts/sec (or 97.8M bits/sec)
    if result['throughput_mbps'] == None:
        matchobj = re.match(r'.*Completed: Throughput for (\d*) byte packets is ([\d\.]*) pkts/sec \(or ([\d\.]*)G bits/sec\).*', ixvw_output, re.S)
        if matchobj:
            if matchobj.group(1):
                result['framesize_byte'] = matchobj.group(1)
            else:
                result['framesize_byte'] = None
            if matchobj.group(2):
                result['throughput_pps'] = matchobj.group(2)
            else:
                result['throughput_pps'] = None
            if matchobj.group(3):
                mbps = float(matchobj.group(3)) * 1000
                result['throughput_mbps'] = str(mbps)
            else:
                result['throughput_mbps'] = None

    # Extract Completed TX retransmision and ACK failed rate
    # Tx Retransmission rate : 0.0 pkts/sec Tx ACK Failed rate : 0.0 pkts/sec
    matchobj = re.match(r'.*Tx Retransmission rate : ([\d\.]*) pkts/sec Tx ACK Failed rate : ([\d\.]*) pkts/sec.*', ixvw_output, re.S)
    if matchobj:
        if matchobj.group(1):
            result['txretransmissionrate_pps'] = matchobj.group(1)
        else:
            result['txretransmissionrate_pps'] = None
        if matchobj.group(2):
            result['txackfailedrate_pps'] = matchobj.group(2)
        else:
            result['txackfailedrate_pps'] = None
    else:
        result['txretransmissionrate_pps'] = None
        result['txackfailedrate_pps'] = None

    # Extract Completed Latency min, max, avg, jitter
    matchobj = re.match(r'.*Latency: min = ([\d\.]*[m|u]*S) max = ([\d\.]*[m|u]*S) avg = ([\d\.]*[u|m]*S), Jitter = ([\d\.]*[m|u]*S).*', ixvw_output, re.S)
    if matchobj:
        if matchobj.group(1):
            result['latencymin'] = matchobj.group(1)
        else:
            result['latencymin'] = None
        if matchobj.group(2):
            result['latencymax'] = matchobj.group(2)
        else:
            result['latencymax'] = None
        if matchobj.group(3):
            result['latencyavg'] = matchobj.group(3)
        else:
            result['latencyavg'] = None
        if matchobj.group(4):
            result['jitter'] = matchobj.group(4)
        else:
            result['jitter'] = None
    else:
        result['latencymin'] = None
        result['latencymax'] = None
        result['latencyavg'] = None
        result['jitter'] = None

    # Extract Test Summary Abort Count
    matchobj = re.match(r'.* Test Summary: \d* failure\(s\), (\d*) abort\(s\), \d* skip\(s\) during \d* test\(s\).*', ixvw_output, re.S)
    if matchobj:
        if matchobj.group(1):
            result['abortcnt'] = matchobj.group(1)
        else:
            result['abortcnt'] = None
    else:
        result['abortcnt'] = None

    # TODO: Need to return ALL errors
    # Extract last error message
    matchobj = re.match(r'.*Error: (.*?)[\n|\r].*', ixvw_output, re.S)
    # INFO: Error: Port 10.83.2.199_card2_port1 did not find any BSSIDs on channel 6
    if matchobj:
        if matchobj.group(1):
            result['errormsg'] = matchobj.group(1)
        else:
            result['errormsg'] = None
    else:
        result['errormsg'] = None

    # TODO : Need to return ALL warnings
    # Extract last warning message
    matchobj = re.match(r'.*Warning: (.*?)[\n|\r].*', ixvw_output, re.S)
    # INFO: Warning: Port 10.83.2.199_card2_port1 did not receive any valid VeriWave frames; latency numbers may be invalid.
    if matchobj:
        if matchobj.group(1):
            result['warningmsg'] = matchobj.group(1)
        else:
            result['warningmsg'] = None
    else:
        result['warningmsg'] = None

    # Return actual console output to allow user to extract additional information
    result['console'] = ixvw_output

    return result

def __append_line(lst, line):
    """
    Description:
        Utility to add line to list of strings that will eventually be joined and written as a file.
    """
    lst.append(line + '\n')

def __build_802_11_client_group_cfg(clientgroupname, groupcfg):
    """
    Description:
        Build the section of the configuration file that control a WiFi client.
    Parameters:
        clientgroupname :   (str) (required) Name of client group to build
        groupcfg        :   (dict) All keys and values required to build configuration

        Dictionary keys and values are described here.  To help ease maintenance and clarity the dictionary keys
        and values are set to be EXACTLY what the IxVeriwave toosl and documentation use versus following strict
        Python style guide for Cafe.  All keys and values if alphabetic are case-sensitive.  If an optional dictionary
        key/value is not present the keylset will not be created forcing default values to be used.

        Refer to IxVeriwave documentation for additional information.

        'Dut'           :   (str) (required) References a Dut that is defiend in the configuraiton.  This is used so
                            the client group can be assigned to a specific port.
        'GroupType'     :   (str) (required) (802.11abgn, 802.11ac, 802.3) Specifies the type of client group
        'Dhcp'          :   (str) (required) (Disable/Enable) Enable or disable use of DHCP for the client group
        'BaseIp'        :   (str) Required if DHCP is disabled. Starting IP address ot use for clients in this group.
        'Gateway'       :   (str) IP address of the gateway
        'IncrIp'        :   (str) Specifies which IP octet to increment and by how much for each subsequent client in
                            the group.  Example, 0.0.0.1, increment the 4th octet by 1. Default '0.0.0.1'
        'BehindNAT'     :   (str) (True/False) Declares that the client group is behind a NAT device
        'phyInterface'  :   (str) (required) (802.11n, 802.11ag, 802.11b, 802.11ac) Hardware setup for the clients
        'ChannelBandwidth'  :   (str) (20, 40, 80) MHz bandwidth value used for WiFi channel.
        'SigBandwidth'  :   (str) (20, 40, 80) MHz bandwidth value used for ac signal. IF value not present but
                            'ChannelBandwidth' does exist then 'ChannelBandwidth' is used.  It is the perception of the
                            author that this behavior will ease re-use across radio types.
        'Method'        :   (str) Specifies the security method(s) to use.  See IxVeriwave document for complete
                            listing.  If this is a list the test will be run for each Method listed.
        'PskAscii'      :   (str) String of ASCII characters representing the Pre-shared key (PSK).
        'Wep40Ascii'    :   (str) String of ASCII characters to use in creation of 40 bit WEP key.  Ascii key will be
                            used if both hex and ascii are present.
        'Wep40Hex       :   (str) String of 10 hex characters to use in creation of 40 bit WEP key.
        'NumClients"    :   (str) Integer Number of clients in the group

    Return: (str) of created configuration lines
    """

    cfglst = []
    grp_prefix = 'keylset ' + clientgroupname + ' '
    __append_line(cfglst, "#Group " + clientgroupname)
    __append_line(cfglst, grp_prefix + 'GroupType ' + groupcfg['GroupType'])
    __append_line(cfglst, grp_prefix + 'Dut ' + groupcfg['Dut'])
    # SSID needs to be groomed to work in TCL environment.
    # each space character needs to be replaced with '\\\\ '
    # additional testing needs to be done as to how to represent a backslash as part of SSID and othes special chars
    #strlen = len(groupcfg['Ssid'])
    newssidlst = []
    for char in groupcfg['Ssid']:
        if char == " ":
            newssidlst.append('\\\\ ')
        else:
            newssidlst.append(char)
    newssid = ''.join(newssidlst)
    __append_line(cfglst, grp_prefix + 'Ssid ' + newssid)
    #__append_line(cfglst, grp_prefix + 'Ssid ' + groupcfg['Ssid'])
    if 'Dhcp' in groupcfg:
        __append_line(cfglst, grp_prefix + 'Dhcp ' + groupcfg['Dhcp'])
    if 'Gateway' in groupcfg:
        __append_line(cfglst, grp_prefix + 'Gateway ' + groupcfg['Gateway'])
    if 'IncrIp' in groupcfg:
        __append_line(cfglst, grp_prefix + 'IncrIp ' + groupcfg['IncrIp'])
    __append_line(cfglst, grp_prefix + 'GratuitousArp True')
    __append_line(cfglst, grp_prefix + 'MacAddress None')
    # __append_line(cfglst, grp_prefix + 'MacAddressMode Increment')
    # __append_line(cfglst, grp_prefix + 'MacAddressIncr 1')
    __append_line(cfglst, grp_prefix + 'phyInterface ' + groupcfg['phyInterface'])
    # TODO : May want to bring out rate values
    if groupcfg['phyInterface'] == "802.11b":
        __append_line(cfglst, grp_prefix + 'DataPhyRate 11')
        __append_line(cfglst, grp_prefix + 'MgmtPhyRate 5.5')
    if groupcfg['phyInterface'] == "802.11ag":
        __append_line(cfglst, grp_prefix + 'DataPhyRate 54')
        __append_line(cfglst, grp_prefix + 'MgmtPhyRate 24')
    # TODO: Look into making more values settable
    if groupcfg['phyInterface'] == "802.11n":
        __append_line(cfglst, grp_prefix + 'PlcpConfiguration mixed')
        __append_line(cfglst, grp_prefix + 'ChannelBandwidth ' + groupcfg['ChannelBandwidth'])
        __append_line(cfglst, grp_prefix + 'EnableAMSDUrxaggregation True')
        __append_line(cfglst, grp_prefix + 'EnableAMPDUaggregation True')
        __append_line(cfglst, grp_prefix + 'ChannelModel Bypass')
        __append_line(cfglst, grp_prefix + 'DataMcsIndex 15')
        __append_line(cfglst, grp_prefix + 'GuardInterval short')
    # TODO: Look into making more values settable
    if groupcfg['phyInterface'] == "802.11ac":
        __append_line(cfglst, grp_prefix + 'NumSpatialStreams 4')
        __append_line(cfglst, grp_prefix + 'PlcpConfiguration vht_mixed')
        __append_line(cfglst, grp_prefix + 'EnableAMSDUrxaggregation True')
        if 'SigBandwidth' not in groupcfg:
            __append_line(cfglst, grp_prefix + 'SigBandwidth ' + groupcfg['ChannelBandwidth'])
            if groupcfg['ChannelBandwidth'] == '20':
                __append_line(cfglst, grp_prefix + 'VhtDataMcs 8')
            else:
                __append_line(cfglst, grp_prefix + 'VhtDataMcs 9')
        else:
            __append_line(cfglst, grp_prefix + 'SigBandwidth ' + groupcfg['SigBandwidth'])
            if groupcfg['SigBandwidth'] == '20':
                __append_line(cfglst, grp_prefix + 'VhtDataMcs 8')
            else:
                __append_line(cfglst, grp_prefix + 'VhtDataMcs 9')
        __append_line(cfglst, grp_prefix + 'EnableAMPDUaggregation True')
        __append_line(cfglst, grp_prefix + 'DuplicateControlFrames False')
        __append_line(cfglst, grp_prefix + 'ChannelModel Bypass')
        __append_line(cfglst, grp_prefix + 'GuardInterval short')

    if 'NumClients' in groupcfg:
        __append_line(cfglst, grp_prefix + 'NumClients ' + groupcfg['NumClients'])
    if 'BehindNAT' in groupcfg:
        __append_line(cfglst, grp_prefix + 'BehindNAT ' + groupcfg['BehindNAT'])
    __append_line(cfglst, grp_prefix + 'Qos Enable')
    if 'BaseIp' in groupcfg:
        # if 'Dhcp' not in groupcfg:
        #     __append_line(cfglst, grp_prefix + 'Dhcp Disable')
        __append_line(cfglst, grp_prefix + 'BaseIp ' + groupcfg['BaseIp'])
    else:
        if 'Dhcp' not in groupcfg:
            __append_line(cfglst, grp_prefix + 'Dhcp Enable')
    if 'Method' in groupcfg:
        __append_line(cfglst, grp_prefix + 'Method { ' + groupcfg['Method'] + ' }')
    else:
        __append_line(cfglst, grp_prefix + 'Method { None }')
    __append_line(cfglst, grp_prefix + 'EnableValidateCertificate off')
    if 'PskAscii' in groupcfg:
        __append_line(cfglst, grp_prefix + 'PskAscii ' + groupcfg['PskAscii'])
    if 'WepKey40Ascii' in groupcfg:
        __append_line(cfglst, grp_prefix + 'WepKey40Ascii' + groupcfg['WepKey40Ascii'])
    if 'WepKey40Hex' in groupcfg:
        __append_line(cfglst, grp_prefix + 'WepKey40Hex' + groupcfg['WepKey40Hex'])
    __append_line(cfglst, "")
    
    return cfglst

def __build_enet_client_group_cfg(clientgroupname, groupcfg):
    """
    Description:
        Build the section of the configuration file that control an Ethernet client.
    Parameters:
        clientgroupname :   (str) (required) Name of client group to build
        groupcfg        :   (dict) All keys and values required to build configuration

        Dictionary keys and values are described here.  To help ease maintenance and clarity the dictionary keys
        and values are set to be EXACTLY what the IxVeriwave toosl and documentation use versus following strict
        Python style guide for Cafe.  All keys and values if alphabetic are case-sensitive.  If an optional dictionary
        key/value is not present the keylset will not be created forcing default values to be used.

        Refer to IxVeriwave documentation for additional information.

        'Dut'           :   (str) (required) References a Dut that is defiend inthe configuraiton.  This is used so the
                            client group can be assigned to a specific port.
        'Dhcp'          :   (str) (Disable/Enable) Enable or disable use of DHCP for the client group
        'BaseIp'        :   (str) Required if DHCP is disabled. Starting IP address ot use for clients in this group.
        'Gateway'       :   (str) IP address of the gateway
        'IncrIp'        :   (str) Specifies which IP octet to increment and by how much for each subsequent client in
                            the group.  Example, 0.0.0.1, increment the 4th octet by 1. Default '0.0.0.1'
        'BehindNAT'     :   (str) (True/False) Declares that the client group is behind a NAT device
        'VLANEnable'    :   (str) (True/False)
        'VLANId'        :   (str) Numeric VLAN ID value.
        'NumClients"    :   (str) Integer Number of clients in the group. Default 1.
    Return: (str) of created configuration lines
    """
    cfglst = []

    grp_prefix = 'keylset ' + clientgroupname + ' '
    __append_line(cfglst, "#Group " + clientgroupname)
    __append_line(cfglst, grp_prefix + 'GroupType 802.3')
    __append_line(cfglst, grp_prefix + 'Dut ' + groupcfg['Dut'])
    #  __append_line(cfglst, grp_prefix + 'MacAddressMode Increment')
    #  __append_line(cfglst, grp_prefix + 'MacAddressIncr 1')
    __append_line(cfglst, grp_prefix + 'MacAddress None')
    if 'Dhcp' in groupcfg:
        __append_line(cfglst, grp_prefix + 'Dhcp ' + groupcfg['Dhcp'])
    if 'Gateway' in groupcfg:
        __append_line(cfglst, grp_prefix + 'Gateway ' + groupcfg['Gateway'])
    if 'IncrIp' in groupcfg:
        __append_line(cfglst, grp_prefix + 'IncrIp ' + groupcfg['IncrIp'])
    __append_line(cfglst, grp_prefix + 'GratuitousArp True')
    # Don't believe specific MAC addresses need to be used but I could be wrong
    # May need to enter a random seed for this to work - could use date and time as the seed
    # __append_line(cfglst, grp_prefix + 'MacAddress " + args['srcmac']')
    if 'NumClients' in groupcfg:
        __append_line(cfglst, grp_prefix + 'NumClients ' + groupcfg['NumClients'])
    if 'BehindNAT' in groupcfg:
        __append_line(cfglst, grp_prefix + 'BehindNAT ' + groupcfg['BehindNAT'])
    __append_line(cfglst, grp_prefix + 'Qos Disable')
    if 'BaseIp' in groupcfg:
        # if 'Dhcp' not in groupcfg:
        #     __append_line(cfglst, grp_prefix + 'Dhcp Disable')
        __append_line(cfglst, grp_prefix + 'BaseIp ' + groupcfg['BaseIp'])
    else:
        if 'Dhcp' not in groupcfg:
            __append_line(cfglst, grp_prefix + 'Dhcp Enable')
    if 'VLANEnable' in groupcfg:
        __append_line(cfglst, grp_prefix + 'VLANEnable ' + groupcfg['VLANEnable'])
    if 'VLANId' in groupcfg:
        __append_line(cfglst, grp_prefix + 'VLANId ' + groupcfg['VLANId'])
    __append_line(cfglst, "")
    
    return cfglst

def __build_enet_dut_cfg(dutname, dutcfg):
    """
    Description:
        Build the section of the configuration file that control and Ethernet DUT.  Only DUTs that are used should 
        be created.
    Parameters:
        dutname     :   (str) (required) Name of client group to build
        dutcfg      :   (dict) All keys and values required to build configuration

        Dictionary keys and values are described here.  To help ease maintenance and clarity the dictionary keys
        and values are set to be EXACTLY what the IxVeriwave toosl and documentation use versus following strict
        Python style guide for Cafe.  All keys and values if alphabetic are case-sensitive.  If an optional dictionary
        key/value is not present the keylset will not be created forcing default values to be used.

        'Wavetestport'  :   (str) IxVeriwave <ChassisName>:<slot>:<port> associated with DUT
    Return: (str) of created configuration lines
    """
    cfglst = []

    dut_prefix = 'keylset ' + dutname + ' '
    __append_line(cfglst, "#Group " + dutname)
    __append_line(cfglst, dut_prefix + 'used True')
    __append_line(cfglst, dut_prefix + 'Vendor generic')
    __append_line(cfglst, dut_prefix + 'APModel None')
    __append_line(cfglst, dut_prefix + 'APSWVersion None')
    __append_line(cfglst, dut_prefix + 'WLANSwitchModel None')
    __append_line(cfglst, dut_prefix + 'WLANSwitchSWVersion None')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.BindStatus True')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.WavetestPort ' + dutcfg['Wavetestport'])
    __append_line(cfglst, dut_prefix + 'Interface.802_3.EthernetSpeed 100')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.Duplex full')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.Autonegotiation on')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.HighPerformance on')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.InterfaceType 802.3')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.EnableRxAttenuation on')
    __append_line(cfglst, dut_prefix + 'Interface.802_3.SecondaryChannelPlacement defer')
    __append_line(cfglst, "")

    return cfglst

def __build_global_cfg(globalcfg):
    """
    Build the section of the configuration file that control Global IxVeriwave parameters.  Parameters passed in via
    a dictionary.  Dictionary keys and values are set to be EXACTLY wo what is documenated by IxVeriwave versus
    following Python guidelines for Cafe.  All keys and values if alphabetic are case-sensitive.  The IxVeriwave
    parameters that can be passed in are as follows:

    ChassisName (str)           :   IP address or host name of IxVeriwave Chassis
    LossTolerance (str)         :   Amount of acceptable frame loss when testing throughput. Float. Default = 0.
    Source (str)                :   List of source group names used for source test traffic .  If a list values must be
                                    space delimited and NOT by a comma.
    Destination (str)           :   List of destination group names used for destination test traffic.  If a list
                                    values must be space delimited and NOT by a comma.
    Ports (str)                 :   List of ports in the test which are usually associated with DUTs
    Direction (str)             :   Describes how the test traffic should be run relative to the source and destination
                                    groups.  (Unidirectional, Bidirectional)
    TrialDuration (str)         :   Number of seconds to run any specific trial or test iteration. Default = 30.
    Channel (str)               :   Channel or channels to use for testing.  IF this is a list the test run for each
                                    channel listed.
    WirelessGroupCount (str)    :   Number of WiFi groups in use for test

    Parameters:
        globalcfg (dict):  All keys and values required to build configuration

    Returns:
        str : Created configuration lines
    """
    cfglst = []

    # Set Global configuration
    gbl_prefix = 'keylset global_config '
    __append_line(cfglst, '#Generated from Cafe')
    timestamp = time.strftime("%m-%d-%y %H:%M:%S", time.localtime())
    __append_line(cfglst, '#TimeStamp: ' + timestamp)
    __append_line(cfglst, gbl_prefix + 'ChassisName {' + globalcfg['ChassisName'] + '}')
    __append_line(cfglst, gbl_prefix + 'RandomSeed ' + str(random.randint(1, 999999999)))
    __append_line(cfglst, "")
    __append_line(cfglst, '#LogsAndResultsInfo Global Options')
    # TODO: Remove hardcoded log directory
    __append_line(cfglst, gbl_prefix + 'LogsDir C:/Users/Testmin/VeriWave/WaveApps/Results')
    __append_line(cfglst, gbl_prefix + 'GeneratePdfReport True')
    __append_line(cfglst, "")
    __append_line(cfglst, '#Test Traffic Global Options')
    __append_line(cfglst, gbl_prefix + 'Source {' + globalcfg['Source'] + '}')
    __append_line(cfglst, gbl_prefix + 'Destination {' + globalcfg['Destination'] + '}')
    __append_line(cfglst, gbl_prefix + 'Ports {' + globalcfg['Ports'] + '}')
    # __append_line(cfglst, gbl_prefix + 'MappingOption 0')
    __append_line(cfglst, gbl_prefix + 'PayloadData None')
    # __append_line(cfglst, gbl_prefix + 'DestinationPort ' + globalcfg['DestinationPort'])
    # __append_line(cfglst, gbl_prefix + 'SourcePort ' + globalcfg['SourcePort'])
    #__append_line(cfglst, gbl_prefix + 'TestList {unicast_unidirectional_throughput}')
    __append_line(cfglst, gbl_prefix + 'TestList {' + globalcfg['TestList'] + '}')
    __append_line(cfglst, gbl_prefix + 'Direction {' + globalcfg['Direction'] + '}')
    # Assumption there always be a WiFi group present
    __append_line(cfglst, gbl_prefix + 'Channel {' + globalcfg['Channel'] + '}')
    __append_line(cfglst, gbl_prefix + 'WirelessGroupCount ' + str(globalcfg['WirelessGroupCount']))
    __append_line(cfglst, gbl_prefix + 'FlowType UDP')
    __append_line(cfglst, gbl_prefix + 'ArpNumRetries 5')
    __append_line(cfglst, gbl_prefix + 'ArpRate 100')
    __append_line(cfglst, gbl_prefix + 'ArpTimeout 5')
    __append_line(cfglst, gbl_prefix + 'NumTrials 1')
    if 'SettleTime' in globalcfg:
        __append_line(cfglst, gbl_prefix + 'SettleTime ' + globalcfg['SettleTime'])
    else:
        __append_line(cfglst, gbl_prefix + 'SettleTime 3')
    if 'LossTolerance' in globalcfg:
        __append_line(cfglst, gbl_prefix + 'LossTolerance ' + globalcfg['LossTolerance'])
    if 'TrialDuration' in globalcfg:
        __append_line(cfglst, gbl_prefix + 'TrialDuration ' + globalcfg['TrialDuration'])
        __append_line(cfglst, gbl_prefix + 'TestDurationSec ' + globalcfg['TrialDuration'])
    __append_line(cfglst, "")

    return cfglst

def __build_test_cfg(testcfg):
    """
    Description:
        Build the section of the configuration file that control test parameters.
    Parameters:
        testcfg        :   (dict) All keys and values required to build configuration

        Dictionary keys and values are described here.  To help ease maintenance and clarity the dictionary keys
        and values are set to be EXACTLY what the IxVeriwave tools and documentation use versus following strict
        Python style guide for Cafe.  All keys and values if alphabetic are case-sensitive.  If an optional dictionary
        key/value is not present the keylset will not be created forcing default values to be used.

        Refer to IxVeriwave documentation for additional information.

        # Test Parameters
        'SourcePort'        :   (str) (required) 1-65535 IP port number of source port
        'DestinationPort'   :   (str) (required) 1-65535 IP port number of destination port
        'FrameSizeList'     :   (str) (required) A List of framesizes to use in the test. Example: '1460 1518'
        'MaxSearchValue'    :   (str) Value of ILOAD to set as the maximum.  Default = 150% of theoretical maximum,
                                otherwise express as a percentage of theoretical maximum when Mode = Percentage.
        'MinSearchValue'    :   (str) Value of ILOAD to set as the minimum.  Default = 1% of theoretical minimum,
                                otherwise express as a percentage of theoretical maximum when Mode = Percentage.
        'SearchResolution'  :   (str) Floating.  Determines the precision of the binary search algorithm.  Represents
                                a percentage relative ot the previous result.  Default = .1.
        'StartValue'        :   (str) Value of ILOAD to set as the starting point in the search.  Default = 50% of
                                theoretical maximum, otherwise express as a percentage of theoretical maximum when
                                Mode = Percentage.
    Return: (str) of created configuration lines
    """
    cfglst = []

    # TODO: This section should be augmented to include other IxVeriwave tests: maxclient, . . . etc.

    if testcfg['Test'] == 'unicast_unidirectional_throughput':
        # Unidirectional Throughput Options
        test_prefix = 'keylset unicast_unidirectional_throughput '
        __append_line(cfglst, '#Test Parameters Specific to test')
        __append_line(cfglst, '#unicast_unidirectional_throughput Options')
        __append_line(cfglst, test_prefix + 'Test unicast_unidirectional_throughput')
        __append_line(cfglst, test_prefix + 'Frame Custom')
        __append_line(cfglst, test_prefix + 'FrameSizeList {' + testcfg['FrameSizeList'] + '}')
        if 'SearchResolution' in testcfg:
            __append_line(cfglst, test_prefix + 'SearchResolution ' + testcfg['SearchResolution'] + '%')
        if 'MinSearchValue' in testcfg:
            __append_line(cfglst, test_prefix + 'MinSearchValue ' + testcfg['MinSearchValue'] + '%')
        if 'MaxSearchValue' in testcfg:
            __append_line(cfglst, test_prefix + 'MaxSearchValue ' + testcfg['MaxSearchValue'] + '%')
        __append_line(cfglst, test_prefix + 'Mode Percent')
        if 'StartValue' in testcfg:
            __append_line(cfglst, test_prefix + 'StartValue ' + testcfg['StartValue'] + '%')
        __append_line(cfglst, test_prefix + 'AcceptableThroughput 0')
        __append_line(cfglst, test_prefix + 'DestinationPort ' + testcfg['DestinationPort'])
        __append_line(cfglst, test_prefix + 'SourcePort ' + testcfg['SourcePort'])
        __append_line(cfglst, "")

    if testcfg['Test'] == 'unicast_max_client_capacity':
        # Unidirectional Throughput Options
        test_prefix = 'keylset unicast_max_client_capacity '
        __append_line(cfglst, '#Test Parameters Specific to test')
        __append_line(cfglst, '#unicast_max_client_capacity Options')
        __append_line(cfglst, test_prefix + 'Test unicast_max_client_capacity')
        __append_line(cfglst, test_prefix + 'FrameSizeList {' + testcfg['FrameSizeList'] + '}')
        __append_line(cfglst, test_prefix + 'ILoadList {' + testcfg['ILoadList'] + '}')
        if 'MaxSearchValue' in testcfg:
            __append_line(cfglst, test_prefix + 'MaxSearchValue ' + testcfg['MaxSearchValue'])
        if 'ExpectedClientConnections' in testcfg:
            __append_line(cfglst, test_prefix + 'ExpectedClientConnections ' + testcfg['ExpectedClientConnections'])
        else:
            __append_line(cfglst, test_prefix + 'ExpectedClientConnections 30')
        __append_line(cfglst, test_prefix + 'DestinationPort ' + testcfg['DestinationPort'])
        __append_line(cfglst, "")

    return cfglst

def __build_wifi_dut_cfg(dutname, dutcfg):
        """
    Description:
        Build the section of the configuration file that control and Ethernet DUT.  Only DUTs that are used should 
        be created.
    Parameters:
        dutname     :   (str) (required) Name of client group to build
        dutcfg      :   (dict) All keys and values required to build configuration

        Dictionary keys and values are described here.  To help ease maintenance and clarity the dictionary keys
        and values are set to be EXACTLY what the IxVeriwave toosl and documentation use versus following strict
        Python style guide for Cafe.  All keys and values if alphabetic are case-sensitive.  If an optional dictionary
        key/value is not present the keylset will not be created forcing default values to be used.

        'Wavetestport'  :   (str) (required) IxVeriwave <Chassisname>:<slot>:<port> associated with DUT
        'Channel'       :   (str) Channel for the port.  Setting the channel in this field has the highest priority and
                            will override a channel setting at the global and client level. (Experiementation)
        'InterfaceType' :   (str) Identifies the type of port (802.11bg, 802.11bg, 802.11a, 802.11n, 802.11n5G
                            802.11ac).
        Return: (str) of created configuration lines
        """
        cfglst = []

        dut_prefix = 'keylset ' + dutname + ' '
        __append_line(cfglst, "#Group " + dutname)
        __append_line(cfglst, dut_prefix + 'used True')
        __append_line(cfglst, dut_prefix + 'Vendor generic')
        __append_line(cfglst, dut_prefix + 'APModel None')
        __append_line(cfglst, dut_prefix + 'APSWVersion None')
        __append_line(cfglst, dut_prefix + 'WLANSwitchModel None')
        __append_line(cfglst, dut_prefix + 'WLANSwitchSWVersion None')

        if dutcfg['InterfaceType'] == "802.11n":
            __append_line(cfglst, dut_prefix + 'Interface.802_11n.BindStatus True')
            __append_line(cfglst, dut_prefix + 'Interface.802_11n.WavetestPort ' + dutcfg['Wavetestport'])
            __append_line(cfglst, dut_prefix + 'Interface.802_11n.HighPerformance on')
            __append_line(cfglst, dut_prefix + 'Interface.802_11n.InterfaceType 802.11n')
            __append_line(cfglst, dut_prefix + 'Interface.802_11n.EnableRxAttenuation on')
            __append_line(cfglst, dut_prefix + 'Interface.802_11n.SecondaryChannelPlacement defer')
            if 'Channel' in dutcfg:
                __append_line(cfglst, dut_prefix + 'Interface.802_11n.Channel ' + dutcfg['Channel'])
        if dutcfg['InterfaceType'] == "802.11ac":
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.BindStatus True')
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.WavetestPort ' + dutcfg['Wavetestport'])
            # __append_line(cfglst, dut_prefix + 'Interface.802_11ac.ChannelBandwidth ' + dutcfg['ChannelBandwidth'])
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.HighPerformance on')
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.InterfaceType 802.11ac')
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.EnableRxAttenuation off')
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.SecondaryChannelPlacement defer')
            if 'Channel' in dutcfg:
                __append_line(cfglst, dut_prefix + 'Interface.802_11ac.Channel ' + dutcfg['Channel'])
            __append_line(cfglst, dut_prefix + 'Interface.802_11ac.EnableFollowApBandwidth 1')
        __append_line(cfglst, "")

        return cfglst

def delremotefile(tclsession, filename):
    # TODO : Should create a more meaningful return.  Maybe perform a catch statement.
    result = tclsession.command('file delete -force ' + filename)

def ixvw_advancedbenchtest(tclsession, ixvwcfg, tclshpath='c:/tcl', vwpath='c:/VW_Auto'):
    # def ixvw_advancedbenchtest():
    """
    Description:
        Build TCL file for advanced bench test.  This function is for POWER users of IxVeriwave only
    Parameters:

    Returns:
        Dictionary
    """

    success = True
    ####################################################################################################################
    # Generate IxVeriwave Configuration file for test
    # ixvwcfg = {}
    # ixvwcfg['globalcfg'] = dict(ChassisName='10.83.2.199',
    #                             Direction='Unidirectional',
    #                             Source='enet_grp1',
    #                             Destination='wifi_grp1',
    #                             TrialDuration='15',
    #                             LossTolerance='.75',
    #                             Channel='36')
    # ixvwcfg['testcfg'] = dict(SourcePort='5000',
    #                           DestinationPort='5001',
    #                           FrameSizeList='1460',
    #                           MaxSearchValue='90',
    #                           MinSearchValue='20',
    #                           SearchResolution='1',
    #                           StartValue='90')
    # ixvwcfg['enet_grp1'] = dict(GroupType='802.3',
    #                             Dut='enet_dut',
    #                             Dhcp='Disable',
    #                             BaseIp='192.168.1.10',
    #                             Gateway='192.168.0.1',
    #                             IncrIp='0.0.0.1',
    #                             BehindNAT='False',
    #                             VLANEnable='False')
    # ixvwcfg['wifi_grp1'] = dict(GroupType='802.11ac',
    #                             Dut='wifi_dut',
    #                             Ssid='YoMomma',
    #                             Dhcp='Disable',
    #                             BaseIp='192.168.1.20',
    #                             Gateway='192.168.0.1',
    #                             IncrIp='0.0.0.1',
    #                             BehindNAT='False',
    #                             phyInterface='802.11ac',
    #                             SigBandwidth='80')
    # ixvwcfg['enet_dut'] = dict(Wavetestport='10.83.2.199:1:3',
    #                            InterfaceType='802.3')
    # ixvwcfg['wifi_dut'] = dict(Wavetestport='10.83.2.199:4:1',
    #                            InterfaceType='802.11ac')

    # Get a list of all client groups
    clientgrp_list = []
    # Add in Source groups
    grps = ixvwcfg['globalcfg']['Source'].split()
    for grp in grps:
        clientgrp_list.append(grp)
    # Add in Destination Groups
    grps = ixvwcfg['globalcfg']['Destination'].split()
    for grp in grps:
        clientgrp_list.append(grp)

    # Get a list of unique DUTs - known as Ports
    dut_list = []
    for grp in clientgrp_list:
        if ixvwcfg[grp]['Dut'] not in dut_list:
            dut_list.append(ixvwcfg[grp]['Dut'])
    ixvwcfg['globalcfg']['Ports'] = ' '.join(dut_list)

    # Count the number of wifi groups
    cnt = 0
    for grp in clientgrp_list:
        if ixvwcfg[grp]['GroupType'][0:6] == "802.11":
            cnt += 1
    ixvwcfg['globalcfg']['WirelessGroupCount'] = str(cnt)

    cfglst = []
    # Add Global Configuration
    ixvwcfg['globalcfg']['TestList'] = 'unicast_unidirectional_throughput'
    cfglst.extend(__build_global_cfg(globalcfg=ixvwcfg['globalcfg']))

    # Add Test Configuration
    #Set test type
    ixvwcfg['testcfg']['Test'] = 'unicast_unidirectional_throughput'
    cfglst.extend(__build_test_cfg(testcfg=ixvwcfg['testcfg']))

    # Add Group Configuration
    for grp in clientgrp_list:
        # Build Wifi group
        if ixvwcfg[grp]['GroupType'][0:6] == "802.11":
            cfglst.extend(__build_802_11_client_group_cfg(clientgroupname=grp, groupcfg=ixvwcfg[grp]))
        else:
            # Build ENET group (default)
            cfglst.extend(__build_enet_client_group_cfg(clientgroupname=grp, groupcfg=ixvwcfg[grp]))

    # Add DUT Configuration
    for dut in dut_list:
        # Build Wifi DUT
        if ixvwcfg[dut]['InterfaceType'][0:6] == "802.11":
            cfglst.extend(__build_wifi_dut_cfg(dutname=dut, dutcfg=ixvwcfg[dut]))
        else:
            cfglst.extend(__build_enet_dut_cfg(dutname=dut, dutcfg=ixvwcfg[dut]))

    # Append closing lines to Configuration
    __append_line(cfglst, "#Source a file looking for a license key definition")
    __append_line(cfglst, "catch {source [file join \$env(HOME) \"vw_licenses.tcl\"]}")
    __append_line(cfglst, "")

    # Print Config file to script for debug reasons
    # for line in cfglst:
    #    print line

    # TODO: Investigate setting TCL shell timeout to low value like 10 seconds and set implicit value when required.
    # Push string over the configuration to the remote system one line at a time
    # Note: Did not have deterministic repeatable results when pushed over as one string.  Did not confirm cause.
    #       Possible reasons could be string too long for one of the machines buffers OR the use of the % within the
    #       string may have caused issues when echoed as a function of the TCL shell.  Just guesses at this point.
    #       Internet search at time of trouble shooting did not lead to any good explanations.
    tclsession.command('set cfgfilestring ""')
    for line in cfglst:
        tclsession.command('set cfgfilestring "$cfgfilestring ' + line + '"')

    # Read in the tcl library for IxVeriwave
    # Note this depth is from the perspective of the calling test suite directory
    # TODO: Figure out how to get a better directory location for any calling module
    tcllibfile = file("../../api/ixveriwave/tcllib/ixveriwavelib.tcl", "r")
    tclliblist = tcllibfile.read()
    tcllibstring = ''.join(tclliblist)
    tcllibfile.close()
    # Apply TCL Library required to execute configuration file against IxVeriwave
    # Note: Have not yet experienced issues with sending library to remove as one large string
    tclsession.command(tcllibstring)

    # Write configuration file to remote IxVeriwave Mgmt machine
    tclsession.command('writecfgfile "' + vwpath + '" "cafe_throughput.tcl"' + ' "$cfgfilestring"')

    # Execute IxVeriwave test
    ixvw_output = tclsession.command("ixvwexecute \"" + tclshpath + "\" \"" + vwpath +
                            "\" \"cafe_throughput.tcl\"")[2]

    result = __analyze_results(ixvw_output)

    return result

def ixvw_advancedmaxclienttest(tclsession, ixvwcfg, tclshpath='c:/tcl', vwpath='c:/VW_Auto'):
    """
    Description:
        Build TCL file for advanced max client capacity test.  This function is for POWER users of IxVeriwave only
    Parameters:

    Returns:
        Dictionary
    """

    # Get a list of all client groups
    clientgrp_list = []
    # Add in Source groups
    grps = ixvwcfg['globalcfg']['Source'].split()
    for grp in grps:
        clientgrp_list.append(grp)
    # Add in Destination Groups
    grps = ixvwcfg['globalcfg']['Destination'].split()
    for grp in grps:
        clientgrp_list.append(grp)

    # Get a list of unique DUTs - known as Ports
    dut_list = []
    for grp in clientgrp_list:
        if ixvwcfg[grp]['Dut'] not in dut_list:
            dut_list.append(ixvwcfg[grp]['Dut'])
    ixvwcfg['globalcfg']['Ports'] = ' '.join(dut_list)

    # Count the number of wifi groups
    cnt = 0
    for grp in clientgrp_list:
        if ixvwcfg[grp]['GroupType'][0:6] == "802.11":
            cnt += 1
    ixvwcfg['globalcfg']['WirelessGroupCount'] = str(cnt)

    cfglst = []
    # Add Global Configuration
    ixvwcfg['globalcfg']['TestList'] = 'unicast_max_client_capacity'
    cfglst.extend(__build_global_cfg(globalcfg=ixvwcfg['globalcfg']))

    # Add Test Configuration
    #Set test type
    ixvwcfg['testcfg']['Test'] = 'unicast_max_client_capacity'
    cfglst.extend(__build_test_cfg(testcfg=ixvwcfg['testcfg']))

    # Add Group Configuration
    for grp in clientgrp_list:
        # Build Wifi group
        if ixvwcfg[grp]['GroupType'][0:6] == "802.11":
            cfglst.extend(__build_802_11_client_group_cfg(clientgroupname=grp, groupcfg=ixvwcfg[grp]))
        else:
            # Build ENET group (default)
            cfglst.extend(__build_enet_client_group_cfg(clientgroupname=grp, groupcfg=ixvwcfg[grp]))

    # Add DUT Configuration
    for dut in dut_list:
        # Build Wifi DUT
        if ixvwcfg[dut]['InterfaceType'][0:6] == "802.11":
            cfglst.extend(__build_wifi_dut_cfg(dutname=dut, dutcfg=ixvwcfg[dut]))
        else:
            cfglst.extend(__build_enet_dut_cfg(dutname=dut, dutcfg=ixvwcfg[dut]))

    # Append closing lines to Configuration
    __append_line(cfglst, "#Source a file looking for a license key definition")
    __append_line(cfglst, "catch {source [file join \$env(HOME) \"vw_licenses.tcl\"]}")
    __append_line(cfglst, "")

    # Print Config file to script for debug reasons
    # for line in cfglst:
    #    print line

    # TODO: Investigate setting TCL shell timeout to low value like 10 seconds and set implicit value when required.
    # Push string over the configuration to the remote system one line at a time
    # Note: Did not have deterministic repeatable results when pushed over as one string.  Did not confirm cause.
    #       Possible reasons could be string too long for one of the machines buffers OR the use of the % within the
    #       string may have caused issues when echoed as a function of the TCL shell.  Just guesses at this point.
    #       Internet search at time of trouble shooting did not lead to any good explanations.
    tclsession.command('set cfgfilestring ""')
    for line in cfglst:
        tclsession.command('set cfgfilestring "$cfgfilestring ' + line + '"')

    # Read in the tcl library for IxVeriwave
    # Note this depth is from the perspective of the calling test suite directory
    # TODO: Figure out how to get a better directory location for any calling module
    tcllibfile = file("../../api/ixveriwave/tcllib/ixveriwavelib.tcl", "r")
    tclliblist = tcllibfile.read()
    tcllibstring = ''.join(tclliblist)
    tcllibfile.close()
    # Apply TCL Library required to execute configuration file against IxVeriwave
    # Note: Have not yet experienced issues with sending library to remove as one large string
    tclsession.command(tcllibstring)

    # Write configuration file to remote IxVeriwave Mgmt machine
    tclsession.command('writecfgfile "' + vwpath + '" "cafe_maxclients.tcl"' + ' "$cfgfilestring"')

    # Execute IxVeriwave test
    ixvw_output = tclsession.command("ixvwexecute \"" + tclshpath + "\" \"" + vwpath +
                            "\" \"cafe_maxclients.tcl\"")[2]

    result = __analyze_results(ixvw_output)

    return result

def ixvw_simplebenchtest(ixvw, chassisname=None, wifichannel=None,
                         srcint=None, srcinttype=None, srcgrouptype=None, srcssid=None, 
                         srcphyinterface="802.11n",
                         srcsecmethod="None", srcsecsecret=None, srcbehindnat="False", srcvlan="untagged", 
                         srcchanbw="20", srcport="5000", srcmac="None",
                         destint=None, destinttype=None, destgrouptype=None, destssid=None, 
                         destphyinterface="802.11n",
                         destsecmethod="None", destsecsecret=None, destbehindnat="False", destvlan="untagged",
                         destchanbw="20", destport="5001", destmac="None",
                         framesize="500", srcpercentrate="20", losstolerance="100",
                         debug="0", tclshpath='c:/tcl', vwpath='c:/VW_Auto'):
    """
    Description:
        Build TCL file for simple bench test
    Parameters:
        -chassisname       (DNS name or IP address of IxVeriwave Chassis)
        -wifichannel       (Integer Value of WiFi channel)

        -srcint            (Source IxVeriwave Card:Port)
        -srcinttype        (Source Inteface/Card Type: 802.11n, 802.11ac, 802.3)
        -srcgrouptype      (Wifi - Source group type: 80211abgn, 802.11ac)
        -srcssid           (Wifi - Source SSID value)
        -srcphyinterface   (Wifi - Source client hardware: 802.11b, 802.11ag, 802.11n, 802.11ac)
        -srcsecmethod      (Wifi - Source security method of client)
        -srcsecsecret      (Wifi - Source security ASCII Shared Secret)
        -srcbehindnat      (Source is behind NAT: false (default) true)
        -srcvlan           (ENET - Source VLAN: untagged, 0-255?)
        -srcchanbw         (Wifi - Source n/AC Channel bandwidth)

        -destint           (Destination IxVeriwave Card:Port)
        -destintyype       (Destination Inteface/Card Type: 802.11n, 802.11ac, 802.3)
        -destgrouptype     (Wifi - Source group type: 80211abgn, 802.11ac)
        -destssid          (Wifi - Destination SSID value)
        -destphyinterface  (Wifi - Destination client hardware: 80211b, 802.11ag, 802.11n, 802.11ac)
        -destsecmethod     (Wifi - Destination security method of client)
        -destsecsecret     (Wifi - Destination security ASCII Shared Secret)
        -destbehindnat     (Destination is behind NAT: false (default) true)
        -destvlan          (ENET - Destination VLAN: untagged, 0-255?)
        -destchanbw        (Wifi - Destination n/AC Channel bandwidth)

        -framesize         (Generated Traffic Custom Frame size)
        -srcpercentrate    (Generated Traffic percentage rate from source)
        -losstolerance     (Percent loss tolerance to be within for Passing)

        -tclshpath         (Root path of TCL shell.  Default: c:/Tcl84)
                           (   path slash direction is irrelevant)
        -vwpath            (Root path of IxVeriwave WaveAutomate.  Default: C:/VW_Auto )
                           (   path slash direction is irrelevant)
    Returns:
        Dictionary
    """
    ixvwcfg = {}
    ixvwcfg['globalcfg'] = dict(ChassisName=chassisname,
                                Direction='Unidirectional',
                                Source='src_grp',
                                Destination='dest_grp',
                                TrialDuration='15',
                                SettleTime='5',
                                LossTolerance=losstolerance,
                                Channel=wifichannel)
    
    ixvwcfg['testcfg'] = dict(SourcePort=srcport,
                              DestinationPort=destport,
                              FrameSizeList=framesize,
                              MaxSearchValue=srcpercentrate,
                              MinSearchValue=srcpercentrate,
                              SearchResolution='1',
                              StartValue=srcpercentrate)
    
    ixvwcfg['src_grp'] = dict(GroupType=srcgrouptype,
                              Dut='src_dut',
                              Dhcp='Enable')
    if srcgrouptype is None and srcinttype == '802.3':
        ixvwcfg['src_grp']['GroupType'] = '802.3'
    if str(srcbehindnat).lower() == 'true':
        ixvwcfg['src_grp']['BehindNAT'] = 'True'
    if srcmac is not None:
        ixvwcfg['src_grp']['MacAddress'] = srcmac
    if srcgrouptype == '802.11abgn' or srcgrouptype == '802.11ac':
        ixvwcfg['src_grp']['phyInterface'] = srcphyinterface
        ixvwcfg['src_grp']['Ssid'] = srcssid
        if srcphyinterface == "802.11n":
            ixvwcfg['src_grp']['ChannelBandwidth'] = srcchanbw
        if srcphyinterface == "802.11ac":
            ixvwcfg['src_grp']['SigBandwidth'] = srcchanbw
        if srcsecmethod is not None:
            ixvwcfg['src_grp']['Method'] = srcsecmethod
        if srcsecsecret is not None:
            ixvwcfg['src_grp']['PskAscii'] = srcsecsecret
    else:
        # ixvwcfg['src_grp']['phyInterface'] = '802.3'
        if srcvlan is not None and srcvlan != "untagged":
            ixvwcfg['src_grp']['VLANId'] = srcvlan

    ixvwcfg['dest_grp'] = dict(GroupType=destgrouptype,
                              Dhcp='Enable')   
    if destgrouptype is None and destinttype == '802.3':
        ixvwcfg['dest_grp']['GroupType'] = '802.3'
    if str(destbehindnat).lower() == 'true':
        ixvwcfg['dest_grp']['BehindNAT'] = 'True'
    if srcint == destint:
        ixvwcfg['dest_grp']['Dut'] = 'src_dut'
    else:
        ixvwcfg['dest_grp']['Dut'] = 'dest_dut'
    if str(destbehindnat).lower() == 'true':
        ixvwcfg['dest_grp']['BehindNat'] = 'True'
    if destmac is not None:
        ixvwcfg['dest_grp']['MacAddress'] = destmac
    if destgrouptype == '802.11abgn' or destgrouptype == '802.11ac':
        ixvwcfg['dest_grp']['phyInterface'] = destphyinterface
        ixvwcfg['dest_grp']['Ssid'] = destssid
        if destphyinterface == "802.11n":
            ixvwcfg['dest_grp']['ChannelBandwidth'] = destchanbw
        if destphyinterface == "802.11ac":
            ixvwcfg['dest_grp']['SigBandwidth'] = destchanbw
        if destsecmethod is not None:
            ixvwcfg['dest_grp']['Method'] = destsecmethod
        if destsecsecret is not None:
            ixvwcfg['dest_grp']['PskAscii'] = destsecsecret
    else:
        # ixvwcfg['dest_grp']['phyInterface'] = '802.3'
        if destvlan is not None and destvlan != "untagged":
            ixvwcfg['dest_grp']['VLANId'] = destvlan

    ixvwcfg['src_dut'] = dict(Wavetestport=chassisname + ':' + srcint,
                               InterfaceType=srcinttype)
    if srcinttype != "802.3":
        ixvwcfg['src_dut']['Channel'] = wifichannel

    if srcint != destint:
        ixvwcfg['dest_dut'] = dict(Wavetestport=chassisname + ':' + destint,
                                   InterfaceType=destinttype)
        if destinttype != "802.3":
            ixvwcfg['dest_dut']['Channel'] = wifichannel

    result = ixvw_advancedbenchtest(ixvw, ixvwcfg, tclshpath=tclshpath, vwpath=vwpath)
    return result

#if __name__ == "__main__":
#     '''
#     The purpose of this section is to test the APIs created.
#     '''
#    import cafe
#    ixvw_advancedbenchtest()
#     session_mgr = cafe.get_session_manager()
#     # create a ssh session to exa device
#     exa_ssh_session = session_mgr.create_session("exa1", session_type="ssh",
#                                                  host="10.243.19.213",
#                                                  user="root", password="root")
#     # get EXACommClass object - EXA equipment lib
#     exa = EXAApiClass(exa_ssh_session)
#     # login and open exa cli console
#     exa.login()
#     # exa.command return a dict data structure as we have declare it as teststep
#     r = exa.command("show interface craft 1")
#     cafe.Checkpoint(r['response']).regex("craft 1")
#
#     r = exa.get_interface_craft(1)
#     cafe.Checkpoint(r['name']).regex("craft 1")
