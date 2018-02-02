__author__ = 'glivermo'
import cafe
import time
import re
from stp.api.ixveriwave.ixveriwavelib import ixvw_simplebenchtest
from stp.api.ixveriwave.ixveriwavelib import delremotefile


# TODO: Consider removing E7 work from test case collection.  May be better fit in test suite as functions
@cafe.test_case()
def enet_ont_build_e7_provisioning(params):
    # Obtain required parameters
    e7 = params['e7']['e7_session']
    gponontid = params['execution']['gponontid']
    gponontport = params['execution']['gponontport']
    e7uplink = params['execution']['e7uplink']
    servicevlan = params['execution']['servicevlan']

    e7.set_interface(interface=e7uplink, role="trunk", trusted="enabled", rstp_active="disabled")

    e7.enable_eth_port(eth_port=e7uplink)

    e7.enable_interface(interface=e7uplink)

    e7.create_vlan(vlan=servicevlan, dhcp_snooping="enabled", mac_forced_forwarding="enabled",
                   ip_source_verify="enabled")

    e7.add_interface(interface=e7uplink, to_vlan=servicevlan)

    e7.create_bw_profile(name="200MbpsSym", upstream_pir="200m", downstream_pir="200m")

    e7.create_svc_match(name="MatchUntagged")

    e7.add_untagged_rule(to_svc_match_list="MatchUntagged", src_mac="ignore")

    e7.create_svc_tag_action(name="AddTag", tatype="add-tag", outer=servicevlan,
                             svc_match_list="MatchUntagged")

    e7.add_eth_svc(name="Data1", totype="ont-port", interface=gponontid + "/" + gponontport, bw_profile="200MbpsSym",
                   svc_tag_action="AddTag")

@cafe.test_case()
def enet_ont_remove_e7_provisioning(params):
    # Obtain required parameters
    e7 = params['e7']['e7_session']
    gponontid = params['execution']['gponontid']
    gponontport = params['execution']['gponontport']
    e7uplink = params['execution']['e7uplink']
    servicevlan = params['execution']['servicevlan']

    e7.disable_eth_port(eth_port=e7uplink)

    e7.disable_interface(interface=e7uplink)

    e7.remove_eth_svc(name="Data1", fromtype="ont-port", interface=gponontid + "/" + gponontport)

    e7.delete_svc_tag_action(name="AddTag")

    # Assumption is that this is the only tag action on a clean system
    e7.remove_untagged_rule(untagged_rule="1", from_svc_match_list="MatchUntagged")

    e7.delete_svc_match(name="MatchUntagged")

    e7.delete_bw_profile(name="200MbpsSym")

    e7.remove_interface(interface=e7uplink, from_vlan=servicevlan)

    e7.delete_vlan(vlan=servicevlan)

    e7.set_interface(interface=e7uplink, role="trunk", rstp_active="enabled")

@cafe.test_case()
def gpon_ont_build_e7_provisioning(params):
    # Obtain required parameters
    e7 = params['e7']['e7_session']
    gponontid = params['execution']['gponontid']
    gponontport = params['execution']['gponontport']
    e7uplink = params['execution']['e7uplink']
    servicevlan = params['execution']['servicevlan']

    e7.set_interface(interface=e7uplink, role="trunk", trusted="enabled", rstp_active="disabled")

    e7.enable_eth_port(eth_port=e7uplink)

    e7.enable_interface(interface=e7uplink)

    e7.create_vlan(vlan=servicevlan, dhcp_snooping="enabled", mac_forced_forwarding="enabled",
                            ip_source_verify="enabled")

    e7.add_interface(interface=e7uplink, to_vlan=servicevlan)

    e7.create_bw_profile(name="200MbpsSym", upstream_pir="200m", downstream_pir="200m")

    e7.create_svc_match(name="MatchVLAN")

    e7.add_tagged_rule(to_svc_match_list="MatchVLAN", vlan=servicevlan)

    e7.create_svc_tag_action(name="ChangeTag", tatype="change-tag", outer=servicevlan,
                             svc_match_list="MatchVLAN")

    e7.add_eth_svc(name="Data1", totype="ont-port", interface=gponontid + "/" + gponontport, bw_profile="200MbpsSym",
                   svc_tag_action="ChangeTag")

@cafe.test_case()
def gpon_ont_remove_e7_provisioning(params):
    # Obtain required parameters
    e7 = params['e7']['e7_session']
    gponontid = params['execution']['gponontid']
    gponontport = params['execution']['gponontport']
    e7uplink = params['execution']['e7uplink']
    servicevlan = params['execution']['servicevlan']

    e7.disable_eth_port(eth_port=e7uplink)

    e7.disable_interface(interface=e7uplink)

    e7.remove_eth_svc(name="Data1", fromtype="ont-port", interface=gponontid + "/" + gponontport)

    e7.delete_svc_tag_action(name="ChangeTag")

    e7.remove_tagged_rule(tagged_rule="1", from_svc_match_list="MatchVLAN")

    e7.delete_svc_match(name="MatchVLAN")

    e7.delete_bw_profile(name="200MbpsSym")

    e7.remove_interface(interface=e7uplink, from_vlan=servicevlan)

    e7.delete_vlan(vlan=servicevlan)

    e7.set_interface(interface=e7uplink, role="trunk", rstp_active="enabled")

@cafe.test_case()
def tc_546775_5g_primary_ssid_lan_isolation(params):
    """
    @id=546775
    Description:
    (5Ghz) Primary SSID <-> LAN Client Isolation: Using default configuration connect one client the Primary SSID 
    and the other to the LAN. Use DHCP for clients if possible. From the SSID client generate unicast traffic to LAN 
    client. Retest changing the direction of the traffic flow. -> Traffic received at the rate generated/expected.  
    Throughput is not the focus of this test.  Test may also be performed using bi-directional traffic.

    Hint: Veriwave wireless client groups was set to be behind NAT.
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
    ixvwlanmac = "00:01:01:01:01:01"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"
    
    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwlanport, destinttype="802.3", destmac=ixvwlanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to LAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])
        
    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwlanport, srcinttype="802.3", srcmac=ixvwlanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac, destbehindnat="true",
                                  framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - LAN to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                 keytype="default")

@cafe.test_case()
def tc_546776_5g_primary_ssid_wan_isolation(params):
    """
    @id=546776
    Description:
        (5GHz) Primary SSID <-> WAN Isolation: Using default configuration connect one client the Primary SSID and the other
        to the operator emulated CORE network. Use DHCP for clients if possible. From the SSID client generate unicast traffic
        to LAN client. Retest changing the direction of the traffic flow. -> Traffic received at the rate generated/expected.
        Throughput is not the focus of this test.  Test may also be performed using bi-directional traffic.

        Hint: Veriwave wireless client group set to be behind NAT.
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
    ixvwwanmac = "00:02:02:01:01:01"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwwanport = params['ixvw']['ixvwwanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwwanport, destinttype="802.3", destmac=ixvwwanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to WAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwwanport, srcinttype="802.3", srcmac=ixvwwanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac, destbehindnat="true",
                                  framesize="500", srcpercentrate="5", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - WAN to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="default")

@cafe.test_case()
def tc_546777_5g_primary_ssid_intra_isolation(params):
    """
    @id=546777
    Description:
    (5GHz) Primary SSID - Client Intra-SSID (within SSID) Isolation: Using default configuration connect two clients 
    to the Primary SSID. Use DHCP for clients if possible. From one client generate unicast UDP traffic to the other 
    SSID client. -> Traffic received at the rate generated/expected. Throughput is not the focus of this test.  Test 
    may also be performed using bi-directional traffic

    Hint: Veriwave client group set to not be behind NAT.
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # TODO: Need to build a uitlity to increment a MAC address netaddr is interesting

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to"
                                                             "Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="default")

@cafe.test_case()
def tc_546778_5g_primary_ssid_nonprimary_ssid_isolation_nosubnet(params):
    """
    @id=546778
    Description:
    (5GHz) Primary SSID <-> Non-Primary SSID - Client Intra-SSID Isolation enabled & Inter-SSID Isolation (Subnet) 
    Disabled: Enable Primary and a Guest or Operator or IPTV SSIDs. Non-Primary SSID is NOT provisioned with separate 
    subnet to Isolate SSID and intra-SSID isolation enabled. Connect a client to each SSID. Use DHCP for clients if 
    possible. From one SSID client generate unicast traffic to the other SSID client.  Retest changing the direction 
    of the traffic flow. -> Traffic received at the rate generated/expected. Throughput is not the focus of this test.  
    Test may also be performed using bi-directional traffic

    Hint: Veriwave client group set to not be behind NAT.
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="enabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="default")

@cafe.test_case()
def tc_546779_5g_primary_ssid_nonprimary_ssid_isolation_subnet(params):
    """
    @id=546779
    Description:
    (5GHz) Primary SSID <-> Non-Primary SSID - Client Intra-SSID Isolation disabled & Inter-SSID Isolation (Subnet) 
    enabled: Enable Primary and a Guest or Operator or IPTV SSIDs. Non-Primary SSID is provisioned with separate 
    subnet to Isolate SSID and intra-SSID isolation is disabled. Connect a client to each SSID. Use DHCP for clients 
    if possible. From one SSID client generate unicast traffic to WAN client. Retest changing the direction of the 
    traffic flow. -> Traffic is not forwarded
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"
    guestclasscnetwork = "10"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, broadcast="enabled")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw='192.168.' + guestclasscnetwork + '.1', startip='192.168.' + guestclasscnetwork + '.2',
                              stopip='192.168.' + guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['warningmsg'] is not None and result['loss_percent'] == "100.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['warningmsg'] is not None and result['loss_percent'] == "100.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  keytype="default")

@cafe.test_case()
def tc_546782_5g_nonprimary_ssid_lan_isolationdisabled(params):
    """
    @id=546882
    Description:
    (5GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Disabled <-> LAN Client Isolation: Enable a Guest or 
    Operator SSID. No separate subnet for inter-SSID isolation is present. Connect a client to the SSID and LAN. Use 
    DHCP for clients if possible. From the SSID client generate unicast traffic to the other SSID client. Retest 
    changing the direction of the traffic flow. -> Traffic received at the rate generated/expected. Throughput is not 
    the focus of this test.  Test may also be performed using bi-directional traffic

    Hint: Veriwave client group set to not be behind NAT.
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
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwlanmac = "00:01:01:01:01:01"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwlanport, destinttype="802.3", destmac=ixvwlanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Non-Primary SSID to LAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwlanport, srcinttype="802.3", srcmac=ixvwlanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiophyinttype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  destbehindnat="true", framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - LAN to Non-Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546783_5g_nonprimary_ssid_lan_isolationenabled(params):
    """
    @id=546883
    Description:
    (5GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Enabled <-> LAN Client Isolation: Enable a Guest or Operator 
    SSID. A separate subnet for isolation is enabled on the non-Primary SSID.  Connect a client to the SSID and LAN. 
    Use DHCP for clients if possible. From the SSID client generate unicast traffic to the other SSID client. Retest 
    changing the direction of the traffic flow. -> Traffic is not forwarded.
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
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwlanmac = "00:01:01:01:01:01"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"
    guestclasscnetwork = "192.168.10"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwlanport, destinttype="802.3", destmac=ixvwlanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    # Warning: No frames were received; Forwarding Rate is zero
    # Warning: Port 10.83.2.199_card1_port1 did not receive any valid VeriWave frames; latency numbers may be invalid.
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - LAN to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwlanport, srcinttype="802.3", srcmac=ixvwlanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  framesize="500", srcpercentrate="3", debug=3)
    # old cafe.Checkpoint(result['errormsg']).contains(exp="did not receive an ARP response", title="IxVW Simple Benchmark Throughput")
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Guest SSID to LAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546784_5g_nonprimary_ssid_wan_isolationenabled(params):
    """
    @id=546784
    Description:
    (5GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Enabled <-> WAN Client Isolation: Enable Guest or Operator
    or IPTV SSID. A separate subnet for inter-SSID isolation is present. Connect a client to the SSID and the WAN.
    From the SSID client generate unicast UDP traffic to the WAN client.  Retest changing the direction of the traffic
    flow  ->Traffic received at the rate generated/expected. Throughput is not the focus of this test.  Test may also
    be performed using bi-directional traffic

    Hint: Veriwave WiFi client group set to be behind NAT.
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
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwwanmac = "00:02:02:01:01:01"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"
    guestclasscnetwork = "192.168.10"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwwanport = params['ixvw']['ixvwwanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype,
                                  srcmac=ixvwradiomac,
                                  destint=ixvwwanport, destinttype="802.3", destmac=ixvwwanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to WAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwwanport, srcinttype="802.3", srcmac=ixvwwanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  destbehindnat="true", framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - WAN to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546785_5g_nonprimary_ssid_wan_isolationenabled(params):
    """
    @id=546785
    Description:
    (5GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Disabled <-> WAN Client Isolation: Enable Guest or
    Operator or IPTV SSID. No separate subnet for inter-SSID isolation is present. Connect a client to the SSID and
    the WAN. From the SSID client generate unicast UDP traffic to the WAN client.  Retest chaing the direction of
    the traffic flow  ->Traffic received at the rate generated/expected. Throughput is not the focus of this test.
    Test may also be performed using bi-directional traffic

    Hint: Veriwave WiFi client group set to be behind NAT.
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
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwwanmac = "00:02:02:01:01:01"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwwanport = params['ixvw']['ixvwwanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwwanport, destinttype="802.3", destmac=ixvwwanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to WAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwwanport, srcinttype="802.3", srcmac=ixvwwanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype+ '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  destbehindnat="true", framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - WAN to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546786_5g_nonprimary_ssid_intra_isolationdisabled(params):
    """
    @id=546786
    Description:
    (5GHz) Non-Primary SSID Intra-SSID Isolation Disabled: Enable a Guest or Operator or IPTV SSID with intra-SSID
    isolation disabled.  Connect two clients to the SSID. Use DHCP for clients if possible. Generate unicast UDP
    traffic from one client to the other.-> Traffic received at the rate generated/expected. Throughput is not the
    focus of this test.  Test may also be performed using bi-directional traffic
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # TODO: Need to build a uitlity to increment a MAC address netaddr is interesting

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

   # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiointtype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to"
                                                             "Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546787_5g_nonprimary_ssid_intra_isolationenabled(params):
    """
    @id=546787
    Description:
    (5GHz) Non-Primary SSID Intra-SSID Isolation Enabled: Enable Guest or Operator SSID with Intra SSID isolation
    is enabled. Connect a client to the SSID and the WAN. From the SSID client generate unicast UDP traffic to the
    WAN client.  Retest changing the direction of the traffic flow  ->Traffic is not forwarded.
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # TODO: Need to build a uitlity to increment a MAC address netaddr is interesting

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

   # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="enabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)

    cafe.Checkpoint(result['errormsg']).contains(exp="did not receive an ARP response", title="IxVW Simple Benchmark Throughput")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546788_5g_two_nonprimary_ssid_bothinterisolationdisabled(params):
    """
    @id=546788
    Description:
    (5GHz) Unique Non-Primary <-> Non-Primary -  Client Inter-SSID Isolation (Subnet) Disabled on Both:  Enable two
    non-Primary SSIDs. Inter-SSID isolation is disabled on both SSIDs.  Connect a client to each SSID. Use DHCP for
    clients if possible. From one SSID client generate unicast UDP traffic to the other SSID client.  Retest changing
    the direction of the traffic flow. -> Traffic received at the rate generated/expected. Throughput is not the
    focus of this test.  Test may also be performed using bi-directional traffic
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="Security Off")
    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Operator_1', destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Operator SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Operator_1', srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - LAN to Non-Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")

@cafe.test_case()
def tc_546789_5g_two_nonprimary_ssid_bothinterisolationenabled(params):
    """
    @id=546789
    Description:
    (5GHz) Unique Non-Primary <-> Non-Primary - Client Inter-SSID Isolation (Subnet) Enabled on Both: Enable two
    non-Primary SSIDs. Inter-SSID isolation is enabled on both SSIDs.  Connect a client to each SSID. Use DHCP for
    clients if possible. From one SSID client generate unicast UDP traffic to the other SSID client.  Retest changing
    the direction of the traffic flow. -> No traffic received. Note non-Primary SSIDs used.

    Hint: Veriwave WiFi client group NOT set to be behind NAT.
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"
    guestclasscnetwork = "192.168.10"
    operatorclasscnetwork = "192.168.100"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=operatorclasscnetwork + '.1', startip=operatorclasscnetwork + '.2',
                              stopip=operatorclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="Security Off")
    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Operator_1', destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Guest SSID to Operator SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Operator_1', srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Operator SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")

@cafe.test_case()
def tc_546790_5g_two_nonprimary_ssid_differentinterisolation(params):
    """
    @id=546790
    Description:
    (5GHz) Unique Non-Primary <-> Non-Primary - Client Inter-SSID Isolation (Subnet) Enabled one One: Enable two
    non-Primary SSIDs. Inter-SSID isolation is enabled on one SSID.  Connect a client to each SSID. Use DHCP for
    clients if possible. From one SSID client generate unicast UDP traffic to the other SSID client.  Retest
    changing the direction of the traffic flow. -> No traffic received. Note non-Primary SSIDs used.

    Hint: Veriwave WiFi client group NOT set to be behind NAT
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
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11ac"
    ixvwradiophyinttype = "802.11ac"
    ixvwradiobandwidth = "80"
    guestclasscnetwork = "192.168.10"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="Security Off")
    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Operator_1', destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Guest SSID to Operator SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Operator_1', srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Operator SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")

@cafe.test_case()
def tc_546796_24g_primary_ssid_lan_isolation(params):
    """
    @id=546796
    Description:
        (2.4Ghz) Primary SSID <-> LAN Client Isolation: Using default configuration connect one client the Primary
        SSID and the other to the LAN. Use DHCP for clients if possible. From the SSID client generate unicast
        traffic to LAN client. Retest changing the direction of the traffic flow. -> Traffic received at the rate
        generated/expected.  Throughput is not the focus of this test.  Test may also be performed using
        bi-directional traffic.

        Hint: Veriwave wireless client groups was set to be behind NAT.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwlanmac = "00:01:01:01:01:01"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, ssidstate="enabled", broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwlanport, destinttype="802.3", destmac=ixvwlanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to LAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])
        
    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwlanport, srcinttype="802.3", srcmac=ixvwlanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac, destbehindnat="true",
                                  framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - LAN to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_546797_24g_primary_ssid_wan_isolation(params):
    """
    @id=546797
    Description:
        (2.4GHz) Primary SSID <-> WAN Isolation: Using default configuration connect one client the Primary SSID and
        the other to the operator emulated CORE network. Use DHCP for clients if possible. From the SSID client
        generate unicast traffic to LAN client. Retest changing the direction of the traffic flow. -> Traffic received
        at the rate generated/expected.  Throughput is not the focus of this test.  Test may also be performed using
        bi-directional traffic.

        Hint: Veriwave wireless client group set to be behind NAT.

    """   
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwwanmac = "00:02:02:01:01:01"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    
    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwwanport = params['ixvw']['ixvwwanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, ssidstate="enabled", broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")
    #time.sleep(60)

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw="20",
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwwanport, destinttype="802.3", destmac=ixvwwanmac,
                                  framesize="500", srcpercentrate=ixvwradiobandwidth, debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to WAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwwanport, srcinttype="802.3", srcmac=ixvwwanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac, destbehindnat="true",
                                  framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - WAN to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_546798_24g_primary_ssid_intra_isolation(params):
    """
    @id=546798
    Description:
        Hint: Veriwave wireless client groups was set to be behind NAT.
        (2.4GHz) Primary SSID - Client Intra-SSID (within SSID) Isolation: Using default configuration connect two
        clients to the Primary SSID. Use DHCP for clients if possible. From one client generate unicast UDP traffic
        to the other SSID client. -> Traffic received at the rate generated/expected. Throughput is not the focus of
        this test.  Test may also be performed using bi-directional traffic

        Hint: Veriwave client group set to not be behind NAT.

    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # TODO: Need to build a uitlity to increment a MAC address netaddr is interesting

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, ssidstate="enabled", broadcast="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to"
                                                             "Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_546799_24g_primary_ssid_nonprimary_ssid_isolation_nosubnet(params):
    """
    @id=546799
    Description:
    (2.4GHz) Primary SSID <-> Non-Primary SSID - Client Intra-SSID Isolation enabled & Inter-SSID Isolation (Subnet)
    Disabled: Enable Primary and a Guest or Operator SSIDs. Non-Primary SSID is NOT provisioned with separate subnet
    to Isolate SSID and intra-SSID isolation enabled. Connect a client to each SSID. Use DHCP for clients if possible.
    From one SSID client generate unicast traffic to the other SSID client.  Retest changing the direction of the
    traffic flow. -> Traffic received at the rate generated/expected. Throughput is not the focus of this test.  Test
    may also be performed using bi-directional traffic

    Hint: Veriwave client group set to not be behind NAT.
    """   
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, ssidstate="enabled", broadcast="enabled")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="enabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_546800_24g_primary_ssid_nonprimary_ssid_isolation_subnet(params):
    """
    @id=546800
    Description:
    (2.4GHz) Primary SSID <-> Non-Primary SSID - Client Intra-SSID Isolation disabled & Inter-SSID Isolation (Subnet)
    enabled: Enable Primary and a Guest or Operator SSIDs. Non-Primary SSID is provisioned with separate subnet to
    Isolate SSID and intra-SSID isolation is disabled. Connect a client to each SSID. Use DHCP for clients if
    possible. From one SSID client generate unicast traffic to WAN client. Retest changing the direction of the
    traffic flow. -> Traffic is not forwarded.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    guestclasscnetwork = "9"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, ssidstate="enabled", broadcast="enabled")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw='192.168.' + guestclasscnetwork + '.1', startip='192.168.' + guestclasscnetwork + '.2',
                              stopip='192.168.' + guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['warningmsg'] is not None and result['loss_percent'] == "100.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype="802.11n", srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['warningmsg'] is not None and result['loss_percent'] == "100.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_546801_24g_primary_ssid_nonprimary_ssid_isolation_subnetandintra(params):
    """
    @id=546801
    Description:
    (2.4GHz) Primary SSID <-> Non-Primary SSID - Client Intra-SSID & Inter-SSID Isolation (Subnet) enabled: Enable
    Primary and a Guest or Operator SSID. Guest SSID is provisioned with separate subnet to for inter-SSID isolation
    and intra-SSID isolation set to enabled. Connect a client to each SSID. Use DHCP for clients if possible. From one
    SSID client generate unicast traffic to the other SSID client.  Retest changing the direction of the traffic
    flow.  -> Traffic is not forwarded.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    guestclasscnetwork = "9"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=fsan, ssidstate="enabled", broadcast="enabled")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled",
                              gw='192.168.' + guestclasscnetwork + '.1', startip='192.168.' + guestclasscnetwork + '.2',
                              stopip='192.168.' + guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=fsan, securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=fsan, srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['warningmsg'] is not None and result['loss_percent'] == "100.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Primary SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=fsan, destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['warningmsg'] is not None and result['loss_percent'] == "100.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype="2.4GHz", channel="Auto")

    # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype="2.4GHz", ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype="2.4GHz", ssid=fsan, securitytype="WPA - WPA2-Personal",
                                  encryptiontype="AES", keytype="default")

@cafe.test_case()
def tc_546803_24g_nonprimary_ssid_lan_isolationdisabled(params):
    """
    @id=546803
    Description:
    (2.4GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Disabled <-> LAN Client Isolation: Enable a Guest or
    Operator SSID. No separate subnet for inter-SSID isolation is present. Connect a client to the SSID and LAN. Use
    DHCP for clients if possible. From the SSID client generate unicast traffic to the other SSID client. Retest
    changing the direction of the traffic flow. -> Traffic received at the rate generated/expected. Throughput is not
    the focus of this test.  Test may also be performed using bi-directional traffic

    Hint: Veriwave client group set to not be behind NAT.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']
    
    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwlanmac = "00:01:01:01:01:01"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw="20",
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwlanport, destinttype="802.3", destmac=ixvwlanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Non-Primary SSID to LAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwlanport, srcinttype="802.3", srcmac=ixvwlanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiophyinttype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  destbehindnat="true", framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - LAN to Non-Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546804_24g_nonprimary_ssid_lan_isolationenabled(params):
    """
    @id=546804
    Description:
    (2.4GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Enabled <-> LAN Client Isolation: Enable a Guest or
    Operator SSID. A separate subnet for isolation is enabled on the non-Primary SSID.  Connect a client to the SSID
    and LAN. Use DHCP for clients if possible. From the SSID client generate unicast traffic to the other SSID client.
    Retest changing the direction of the traffic flow. -> Traffic is not forwarded.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwlanmac = "00:01:01:01:01:01"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    guestclasscnetwork = "192.168.9"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwlanport = params['ixvw']['ixvwlanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwlanport, destinttype="802.3", destmac=ixvwlanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    # Warning: No frames were received; Forwarding Rate is zero
    # Warning: Port 10.83.2.199_card1_port1 did not receive any valid VeriWave frames; latency numbers may be invalid.
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - LAN to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwlanport, srcinttype="802.3", srcmac=ixvwlanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  framesize="500", srcpercentrate="3", debug=3)
    # old cafe.Checkpoint(result['errormsg']).contains(exp="did not receive an ARP response", title="IxVW Simple Benchmark Throughput")
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Guest SSID to LAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546805_24g_nonprimary_ssid_wan_isolationenabled(params):
    """
    @id=546805
    Description:
    (2.4GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Enabled <-> WAN Client Isolation: Enable Guest or Operator
    SSID. A separate subnet for inter-SSID isolation is present. Connect a client to the SSID and the WAN. From the
    SSID client generate unicast UDP traffic to the WAN client.  Retest changing the direction of the traffic flow
    ->Traffic received at the rate generated/expected. Throughput is not the focus of this test.  Test may also be
    performed using bi-directional traffic

    Hint: Veriwave WiFi client group set to be behind NAT.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwwanmac = "00:02:02:01:01:01"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    guestclasscnetwork = "192.168.9"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwwanport = params['ixvw']['ixvwwanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype,
                                  srcmac=ixvwradiomac,
                                  destint=ixvwwanport, destinttype="802.3", destmac=ixvwwanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to WAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwwanport, srcinttype="802.3", srcmac=ixvwwanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  destbehindnat="true", framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - WAN to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546806_24g_nonprimary_ssid_wan_isolationenabled(params):
    """
    @id=546806
    Description:
    (2.4GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Disabled <-> WAN Client Isolation: Enable Guest or
    Operator SSID. No separate subnet for inter-SSID isolation is present. Connect a client to the SSID and the WAN.
    From the SSID client generate unicast UDP traffic to the WAN client.  Retest changing the direction of the traffic
    flow  ->Traffic received at the rate generated/expected. Throughput is not the focus of this test.  Test may also
    be performed using bi-directional traffic

    Hint: Veriwave WiFi client group set to be behind NAT
    """
# Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac = "00:03:03:01:01:01"
    ixvwwanmac = "00:02:02:01:01:01"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']
    ixvwwanport = params['ixvw']['ixvwwanport']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac,
                                  destint=ixvwwanport, destinttype="802.3", destmac=ixvwwanmac,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to WAN")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwwanport, srcinttype="802.3", srcmac=ixvwwanmac,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype+ '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac,
                                  destbehindnat="true", framesize="500", srcpercentrate="3", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - WAN to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546807_24g_nonprimary_ssid_intra_isolationdisabled(params):
    """
    @id=546807
    Description:
    (2.4GHz) Non-Primary SSID Intra-SSID Isolation Disabled: Enable a Guest or Operator SSID with intra-SSID isolation
    disabled.  Connect two clients to the SSID. Use DHCP for clients if possible. Generate unicast UDP traffic from
    one client to the other.-> Traffic received at the rate generated/expected. Throughput is not the focus of this
    test.  Test may also be performed using bi-directional traffic

    Hint: Veriwave client group set to not be behind NAT.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # TODO: Need to build a uitlity to increment a MAC address netaddr is interesting

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

   # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiointtype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to"
                                                             "Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546808_24g_nonprimary_ssid_intra_isolationenabled(params):
    """
    @id=546808
    Description:
    (2.4GHz) Non-Primary SSID Intra-SSID Isolation Enabled: Enable a Guest or Operator SSID with intra-SSID isolation
    enabled.  Connect two clients to the SSID. Use DHCP for clients if possible. Generate unicast UDP traffic from
    one client to the other.-> Traffic is not forwarded
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # TODO: Need to build a uitlity to increment a MAC address netaddr is interesting

    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

   # Not sure if the guest network is always made up of the last 6 characters of the fsan or not
    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="enabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)

    cafe.Checkpoint(result['errormsg']).contains(exp="did not receive an ARP response", title="IxVW Simple Benchmark Throughput")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

@cafe.test_case()
def tc_546809_24g_two_nonprimary_ssid_bothinterisolationdisabled(params):
    """
    @id=546809
    Description:
    (2.4GHz) Non-Primary SSID Inter-SSID Isolation (Subnet) Disabled <-> WAN Client Isolation: Enable Guest or
    Operator SSID. No separate subnet for inter-SSID isolation is present. Connect a client to the SSID and the WAN.
    From the SSID client generate unicast UDP traffic to the WAN client.  Retest changing the direction of the traffic
    flow  ->Traffic received at the rate generated/expected. Throughput is not the focus of this test.  Test may also
    be performed using bi-directional traffic

    Hint: Veriwave WiFi client group set to be behind NAT
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="Security Off")
    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Operator_1', destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - Guest SSID to Operator SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Operator_1', srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    if result['errormsg'] is None and result['loss_percent'] == "0.0" and result['abortcnt'] == "0":
        success = True
    else:
        success = False
    cafe.Checkpoint(str(success)).contains(exp="True", title="IxVW Simple Benchmark Throughput - LAN to Non-Primary SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")

@cafe.test_case()
def tc_546810_24g_two_nonprimary_ssid_bothinterisolationenabled(params):
    """
    @id=546810
    Description:
    (2.4GHz) Unique Non-Primary <-> Non-Primary - Client Inter-SSID Isolation (Subnet) Enabled on Both: Enable two
    non-Primary SSIDs. Inter-SSID isolation is enabled on both SSIDs.  Connect a client to each SSID. Use DHCP for
    clients if possible. From one SSID client generate unicast UDP traffic to the other SSID client.  Retest changing
    the direction of the traffic flow. -> No traffic received. Note non-Primary SSIDs used.

    Hint: Veriwave WiFi client group NOT set to be behind NAT.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    guestclasscnetwork = "192.168.9"
    operatorclasscnetwork = "192.168.90"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=operatorclasscnetwork + '.1', startip=operatorclasscnetwork + '.2',
                              stopip=operatorclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="Security Off")
    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Operator_1', destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Guest SSID to Operator SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Operator_1', srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Operator SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")

@cafe.test_case()
def tc_546811_24g_two_nonprimary_ssid_differentinterisolation(params):
    """
    @id=546810
    Description:
    (2.4GHz) Unique Non-Primary <-> Non-Primary - Client Inter-SSID Isolation (Subnet) Enabled one One: Enable two
    non-Primary SSIDs. Inter-SSID isolation is enabled on one SSID.  Connect a client to each SSID. Use DHCP for
    clients if possible. From one SSID client generate unicast UDP traffic to the other SSID client.  Retest changing
    the direction of the traffic flow. -> No traffic received. Note non-Primary SSIDs used.

    Hint: Veriwave WiFi client group NOT set to be behind NAT.
    """
    # Obtain required parameters
    ontgui = params['ontgui']['ontgui_session']
    ixvw =  params['ixvw']['ixvwpcsession']
    ontip = params['ontgui']['ontgui']
    fsan = params['execution']['ontfsan']

    # Set re-used variable information - ease of script re-use needs
    radiotype = '2.4GHz'
    wifimode = "802.11b, 802.11g, and 802.11n"
    wifichannel = "6"
    wifibandwidth = "20 MHz"
    ixvwradiomac_1 = "00:03:03:01:01:01"
    ixvwradiomac_2 = "00:03:03:01:01:02"
    ixvwradiointtype = "802.11n"
    ixvwradiophyinttype = "802.11n"
    ixvwradiobandwidth = "20"
    guestclasscnetwork = "192.168.9"

    # Obtain global IxVeriwave port settings
    ixvwchassisip = params['ixvw']['ixvwchassisip']
    ixvwradioport = params['ixvw']['ixvwradioport']
    ixvwradiogrouptype=params['ixvw']['ixvwradiogrouptype']

    # #####
    # Configure WiFi values (Assume all values need to be set even if default)
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, radio="on", mode=wifimode,
                               bandwidth=wifibandwidth, channel=wifichannel, powerlevel="100%")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="enabled",
                              gw=guestclasscnetwork + '.1', startip=guestclasscnetwork + '.2',
                              stopip=guestclasscnetwork + '.254', mask="255.255.255.0")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="enabled",
                              broadcast="enabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                                  securitytype="Security Off")

    ontgui.wireless_securitysetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                                  securitytype="Security Off")
    # #####
    # TODO: Add in setting of primary SSID IP addressing parameters to known default values

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Guest' + fsan[-6:], srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_1,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Operator_1', destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_2,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Guest SSID to Operator SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # Execute brief benchmark test to prove/disprove connectivity
    result = ixvw_simplebenchtest(ixvw, chassisname=ixvwchassisip, wifichannel=wifichannel,
                                  srcint=ixvwradioport, srcinttype=ixvwradiointtype, srcgrouptype=ixvwradiogrouptype,
                                  srcchanbw=ixvwradiobandwidth,
                                  srcssid=radiotype + '_Operator_1', srcphyinterface=ixvwradiophyinttype, srcmac=ixvwradiomac_2,
                                  destint=ixvwradioport, destinttype=ixvwradiointtype, destgrouptype=ixvwradiogrouptype,
                                  destchanbw=ixvwradiobandwidth,
                                  destssid=radiotype + '_Guest' + fsan[-6:], destphyinterface=ixvwradiophyinttype, destmac=ixvwradiomac_1,
                                  framesize="500", srcpercentrate="20", debug=3)
    cafe.Checkpoint(result['warningmsg']).contains(exp="did not receive any valid VeriWave frames",
                                                   title="IxVW Simple Benchmark Throughput - Operator SSID to Guest SSID")
    # Clean up remote log directory if one was created
    if result['logdir']:
        delremotefile(ixvw, filename=result['logdir'])

    # #####
    # Return WiFi values to known defaults
    ontgui.wireless_radiosetup(ontip=ontip, radiotype=radiotype, channel="Auto")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:],
                              broadcast="enabled", clientisolate="enabled", ssidisolate="enabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Guest' + fsan[-6:], ssidstate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1',
                              broadcast="disabled", clientisolate="disabled", ssidisolate="disabled")

    ontgui.wireless_ssidsetup(ontip=ontip, radiotype=radiotype, ssid=radiotype + '_Operator_1', ssidstate="disabled")