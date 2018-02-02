package provide CalixIxiaHltApi 1.00

if { [catch {
    package req Ixia
    package req IxTclHal
    package req IxTclNetwork
    package req Tclx
    package req ip
    } err ] } {
    puts $err
} else {
    puts "package HLTAPI for IxNetwork has been loaded!"
}

proc check {} { puts "package HLT is ready for use!" }

namespace eval CiHLT {

    variable folder
    # ::CiHLT::handles key list variable to handle obj name <-> handles mapping
    set handles ""
    # ::CiHLT::handles stats placeholder & use ::HLT_print_stats to print the result
    set stats ""
    set gtype ""
    set LOGTS ""
    set ERROR ""
    set _ERROR ERROR
    set _SUCCESS SUCCESS
}

proc CiHLT::enable_log {log_path} {
	variable logFileId
	global LOGTS

	set LOGTS [clock format [clock seconds] -format "%B_%d_%H_%M_%S"]
	file mkdir "$log_path/Log_$LOGTS"
	if {[catch {set logFileId [open $log_path/Log_$LOGTS/scriptLog.txt w]}]} {
		CsHLT::logErr "Open script log file failed!"
        #puts "Open script log file failed!"
        lappend CiHLT::ERROR "failed to open file!"
        puts $CiHLT::_ERROR
        return
	} else {
        #set ::CsHLT::log_enable 1
        CiHLT::log "log enabled!"
        puts $CiHLT::_SUCCESS
        #puts "log enabled!"
    }
    set folder "$log_path/Log_$LOGTS"
}

#*************************************************************************************************
#Purpose: write output log info to file.
# args:
#	==> msg : msg info .
#Author :James.cao
#*************************************************************************************************
proc CiHLT::log { msg } {
	variable logFileId
	variable line ""
	#variable ll1
	if {[info exists logFileId]} {
		append line [clock format [clock seconds] -format "%A %B %d %H:%M:%S"] "==>$msg"
		#puts $logFileId $line
		flush $logFileId
		#puts $CiHLT::_SUCCESS
	} else {return "ERROR"}
}

proc CiHLT::logErr {msg} {
	variable logFileId
	variable line ""
	#variable l1
	if {[info exists logFileId]} {
		append line [clock format [clock seconds] -format "%A %B %d %H:%M:%S"] "==>ERROR:$msg"
		#puts $logFileId $line
		flush $logFileId
		#puts $CiHLT::_SUCCESS
	} else {
		return "ERROR"
	}
}

#propose: generate a arr list
#Input: "-a 1 -b 2 -c 3"
#output: "a 1 b 2 c 3"
proc ::CiHLT::get_opt_array_list { vars } {
    array set tmp {}
    foreach v $vars {
        if {[regexp {^-(.*)} $v m m1]} {
            set cur $m1
            set tmp($cur) ""
        } else {
            lappend tmp($cur) $v
        }
    }
    return [array get tmp]
}

#propose: create opt list
#Input:
#output:
proc ::CiHLT::create_opt_str_from_array { in } {
    upvar $in arr
    set str ""
    foreach {k v} [array get arr] {
        append str " -${k} $v"
    }
    return $str
}

#propose: remove opt and value from arr
#Input:  "-q 1 -w 2 -e 3" q
#output: "-w 2 -e 3"
proc ::CiHLT::remove_opt_value { vars opt } {
    array set tmp [ get_opt_array_list $vars ]
    puts [array get tmp]
    if { [ catch { unset tmp($opt) } err ] } {
        msg $err warn
    }
    set str [ create_opt_str_from_array tmp ]
    return $str
}

#propose: get opt and value from arr
#Input:  "-q 1 -w 2 -e 3" q
#output: 1
proc ::CiHLT::get_opt_value { vars opt } {
    array set tmp [ get_opt_array_list $vars ]
    set res [array get tmp $opt ]
    if { $res == "" } {
        puts "cannot not find opt $opt in \"$vars\""
        return ""
    } else {
        return [lindex $res 1]
    }
}

#propose: key list print
#Input:
#return:
proc ::CiHLT::keylprint {listvalues {indentationLevel 0} {indentString "    "}} {
    foreach key [keylkeys listvalues] {
        set value [keylget listvalues $key]

        puts -nonewline [string repeat $indentString $indentationLevel]

        try_eval {
            # Attempt to treat the value as a nested keyedlist
            set subkeys [keylkeys listvalues $key]
            set sublistvalues [keylget listvalues $key]
            puts "$key:"
            keylprint $sublistvalues [expr {$indentationLevel + 1}] $indentString
        } {
            # The value is not a nested keyedlist
            puts "$key: $value"
        }
    }
}
#propose: set name to handle
#Input:  $handle $name
#return:  info:....
proc ::CiHLT::_ixia_set_obj_name { handle name } {
    ixNet setAttribute $handle -name "$name"
    ixNet commit
    puts "Info - [info script] - set name \"$name\" to $handle"
}
#propose: get name from handle
#Input:  $handle
#return:  $name
proc ::CiHLT::_ixia_get_obj_name { handle } {
    set name [ ixNet getAttribute $handle -name]
    return $name
}
#propose: get name form Handle?
#Input:
#return:
proc ::CiHLT::get_handle { name } {
    if [ catch { set h [ keylget ::CiHLT::handles "$name" ] } retCode ] {
        puts "Warn - [info script] - $retCode"
        raise $err
    }
    return $h
}
#propose: check if name is exist in handle
#Input:
#return:
proc ::CiHLT::is_handle_exist { name } {
    set keys [ keylkeys ::CiHLT::handles ]
    if { [lsearch $keys  "$name" ] < 0 } {
        return $::FAILURE
    } else {
        return $::SUCCESS
    }
}
#propose: check if name is exist, and if not, set name to handle
#Input:
#return:
proc ::CiHLT::set_handle { name handle } {
    set keys [ keylkeys ::CiHLT::handles ]
    if { [lsearch $keys  "$name" ] >= 0 } {
        puts "Warn - [info script] - name ref \"$name\" already exist"
    }
    keylset ::CiHLT::handles "$name" "$handle"
    puts "Info - [info script] - set name ref \"$name\" to handle \"$handle\""
}

#propose: print stats result
#Input:
#return:
proc ::CiHLT::printStats { {key ""} } {
    #set kl [keylget ::CiHLT::stats ""]
    if { $key == "" } {
        if { [catch {set kl "$::CiHLT::stats"} retCode] } {
            puts $CiHLT::_ERROR
            puts $retCode
            CiHLT::logErr "ERROR - Failed to print stats - $retCode!"
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:print stats"
        }
    } else {
        if { [catch  {set tmp [keylget ::CiHLT::stats $key] } retCode] } {
            keylset kl $key $tmp
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR - Failed to print stats - $retCode"
            return $retCode

        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:print stats"
        }
    }
    puts [string repeat "#" 80]
    puts [::CiHLT::keylprint $kl]
    puts [string repeat "#" 80]
    puts $CiHLT::_SUCCESS
}
#propose: get port handle
#Input:
#return:
proc CiHLT::getPortHandle {port} {

    return [ keylget ::CiHLT::handles  "port.${port}" ]
}
#propose: get vport handle
#Input:
#return:
proc CiHLT::getVPortHandle {port} {

    return [ keylget ::CiHLT::handles  "vport.${port}" ]
}
#propose: get protocol port handle(not supported on HLT version 4.30)
#Input:
#return:
proc CiHLT::getProtocolPortHandle {port} {

    return [ keylget ::CiHLT::handles  "pport.${port}" ]
}
#propose: Load Tcl package
#Input:
#return:
proc CiHLT::loadPackage {type} {
    if {[string toupper $type] == "IXIA"} {
        if {[catch {package require Ixia} retCode]} {
            puts "FAIL - [info script] - $retCode"
            return 0
        } else {
            set ::CiHLT::gtype $type
            package require IxTclNetwork
            set ::CiHLT::ixia_version [package require Ixia]
            return "$type package loaded! (ver: $::CiHLT::ixia_version)"
        }
    } elseif {[string toupper $type] == "SPIRENT"} {
        if {[catch {package require stc} retCode]} {
            puts "FAIL - [info script] - $retCode"
            puts $CiHLT::_ERROR
            return $retCode
        } else {

        }
    } else {
        puts "ERROE:unknown type:$type"
    }
}
#propose: Connect to traffic generator
#Input:  ip port tclserver
#return:
proc CiHLT::connect_to_chas { chassisIP portLst
                              { ixNetworkTclServer localhost:8009}
                              { tcl_server "" } } {
    #set port_list [list $uplcard/$uplport $dnlcard/$dnlport]
    if { ${tcl_server} == "" } {
        set connect_status [::ixia::connect                    \
                            -reset                                             \
                            -device     $chassisIP                             \
                            -port_list  $portLst                               \
                            -ixnetwork_tcl_server $ixNetworkTclServer          \
                            ]

    } else {
        set connect_status [::ixia::connect                    \
                                -reset                                             \
                                -device      $chassisIP                             \
                                -port_list   $portLst                               \
                                -ixnetwork_tcl_server $ixNetworkTclServer          \
                                -tcl_server   $tcl_server                          \
                               ]

    }
    puts $connect_status
    if {[keylget connect_status status] != $::SUCCESS} {
        CiHLT::logErr "ERROR - [keylget connect_status log]"
        puts $CiHLT::_ERROR
        return $connect_status
    } else {
        CiHLT::log "SUCCESS- Successed to connect to IXIA!"
        puts $CiHLT::_SUCCESS
        ## The connect_status contains multiple port handles save them into CiHLT::ports arrary
        set cnt 0
        #puts "****************"
        #puts "connect_status is: $connect_status"
        #puts "****************"
        foreach p $portLst {
            keylset ::CiHLT::handles "port.${p}"  "1/${p}"
            keylset ::CiHLT::handles "vport.${p}" [lindex [keylget connect_status vport_list] $cnt]
            catch { keylset ::CiHLT::handles "pport.${p}" [lindex [keylget connect_status vport_protocols_handle] $cnt] }
            incr cnt 1
        }
        return 1
    }
    #puts "**************************************"
    #puts "::CiHLT::handles is: $::CiHLT::handles"
    #puts "**************************************"
}

proc CiHLT::setPortName {mode port name {inputs ""}} {

        set portHandle [ eval CiHLT::getVPortHandle $port ]
        set str "-mode $mode -port_list $portHandle -port_name_list $name $inputs"
        set rstatus [eval ::ixia::vport_info $str]
        if {[keylget rstatus status] != $::SUCCESS} {
            CiHLT::logErr "ERROR - [keylget dhcp_portHandle_status log]"
            puts $CiHLT::_ERROR
            return $rstatus
        } else {
            CiHLT::log "SUCCESS: set port $port name"
            puts $CiHLT::_SUCCESS
        }
}
#propose: disconnect and clear all configurations
#Input:
#return:
proc CiHLT::cleanupSession { {reset 1}  } {
        catch {ixNet exec stopAllProtocols}
        after 2000

        #set port_handle [list $chasId/$uplcard/$uplport $chasId/$dnlcard/$dnlport]
        if { $reset == 1 } {
            set str "-reset"
        } else {
            set str ""
        }
        set cleanup_return [eval ::ixia::cleanup_session $str]
        if {[keylget cleanup_return status] != $::SUCCESS} {
            CiHLT::logErr "ERROR-[keylget cleanup_return log]"
            puts $CiHLT::_ERROR
            return $cleanup_return
        } else {
            CiHLT::log "SUCCESS: cleanup session"
            puts $CiHLT::_SUCCESS
        }
}

proc CiHLT::ClearArpTable { port } {
    set vport ""
    set c_card [ lindex [split $port "\/" ] 0 ]
    set c_port [ lindex [split $port "\/" ] 1 ]

    foreach  vport [ ixNet getL [ ixNet getRoot] vport ] {
        set info_card ""
        set info_port ""
        set info [ ixNet getA $vport -connectionInfo ]
        foreach item $info {
            set arr [ split $item "="]
            if { [lindex $arr 0 ] == "card" } {
                set info_card [lindex [split [lindex $arr 1] "\""] 1 ]
            } elseif { [lindex $arr 0 ] == "port" } {
                set info_port [lindex [split [lindex $arr 1] "\""] 1 ]
            }
        }
        if { $info_card == $c_card && $info_port == $c_port } {
            set status [ ixNet exec clearNeighborTable $vport]
            if { [ string match "::ixNet::OK*" $status ] } {
                puts $CiHLT::_SUCCESS
            } else {
                puts $CiHLT::_ERROR
            }
            return $status
        }
    }

}

proc CiHLT::getArpTable { port } {
    set c_card [ lindex [split $port "\/" ] 0 ]
    set c_port [ lindex [split $port "\/" ] 1 ]

    set arp_table {}
    foreach  vport [ ixNet getL [ ixNet getRoot] vport ] {
        set info_card ""
        set info_port ""
        set info [ ixNet getA $vport -connectionInfo ]
        foreach item $info {
            set arr [ split $item "="]
            if { [lindex $arr 0 ] == "card" } {
                set info_card [lindex [split [lindex $arr 1] "\""] 1 ]
            } elseif { [lindex $arr 0 ] == "port" } {
                set info_port [lindex [split [lindex $arr 1] "\""] 1 ]
            }
        }

        if { $info_card == $c_card && $info_port == $c_port } {
            foreach neighbor [ ixNet getL $vport discoveredNeighbor ] {
                set ip [ eval ixNet getA $neighbor -neighborIp]
                set mac [ eval ixNet getA $neighbor -neighborMac]
                # puts "$ip       $mac"
                lappend arp_table  "$ip/$mac"
            }
        }
    }
    return $arp_table
}

proc CiHLT::getDiscoveredNeighborIp { port } {
    set vport ""
    set c_card [ lindex [split $port "\/" ] 0 ]
    set c_port [ lindex [split $port "\/" ] 1 ]

    set ips ""
    foreach  vport [ ixNet getL [ ixNet getRoot] vport ] {
        set info_card ""
        set info_port ""
        set info [ ixNet getA $vport -connectionInfo ]
        foreach item $info {
            set arr [ split $item "="]
            if { [lindex $arr 0 ] == "card" } {
                set info_card [lindex [split [lindex $arr 1] "\""] 1 ]
            } elseif { [lindex $arr 0 ] == "port" } {
                set info_port [lindex [split [lindex $arr 1] "\""] 1 ]
            }
        }
        if { $info_card == $c_card && $info_port == $c_port } {
            foreach neighbor [ ixNet getL $vport discoveredNeighbor ] {
                set ip [ eval ixNet getA $neighbor -neighborIp]
                lappend ips $ip
            }
        }
    }
    return $ips
}

proc CiHLT::interfaceConfig { ports inputs} {
        set portHandle ""
        foreach i $ports {
			lappend portHandle [ eval CiHLT::getVPortHandle $i ]
        }
		#set str "-port_handle $portHandle $inputs"
        #set interface_status [eval ::ixia::interface_config $str]
		set interface_status [eval ::ixia::interface_config -port_handle $portHandle $inputs]
        if {[keylget interface_status status] != $::SUCCESS} {
             CiHLT::logErr "ERROR - [keylget interface_status log]"
             puts $CiHLT::_ERROR
             return $interface_status
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:configure interface $ports"
            puts $interface_status
            return [keylget interface_status interface_handle ]
        }
}
proc CiHLT::_interfaceConfig { ports mode inputs} {
        set portHandle ""
        foreach i $ports {
			lappend portHandle [ eval CiHLT::getVPortHandle $i ]
        }
		#set str "-port_handle $portHandle -mode $mode $inputs"
        #set interface_status [eval ::ixia::interface_config $str]
		set interface_status [eval ::ixia::interface_config -port_handle $portHandle $inputs]
        if {[keylget interface_status status] != $::SUCCESS} {
             CiHLT::logErr "ERROR - [keylget interface_status log]"
             puts $CiHLT::_ERROR
             return $interface_status
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:configure interface $ports"
            puts $interface_status
            return [keylget interface_status interface_handle ]
        }
}

# proc CiHLT::interfaceModify { interface service attr value } {

#     set output [ eval ixNet setA $interface/$service -$attr $value ]

#     puts $output

#     if { [ string match "::ixNet::OK" $output ] } {
#         puts $CiHLT::_SUCCESS

#     } else {
#         puts $CiHLT::_ERROR
#     }
#     return $output
# }

proc CiHLT::interfaceModify { handle port {inputs ""}} {

    set port_handle [ eval CiHLT::getVPortHandle $port ]
    set status [ eval ::ixia::interface_config -mode modify \
                     -port_handle $port_handle \
                     -interface_handle $handle \
                     $inputs]
    puts $status
    if {[keylget status status] != $::SUCCESS} {
        CiHLT::logErr "ERROR - [keylget status log]"
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
    }
}

proc CiHLT::interfaceSendPing { interface ip } {
    set ping_status [ ixNet exec sendPing  $interface $ip ]
    if { [ string match "::ixNet::OK-*" $ping_status ] } {
        puts $CiHLT::_SUCCESS
        set output [ lindex [ split $ping_status "-" ] end ]
        return $output
    } else {
        puts $CiHLT::_ERROR
        return $ping_status
    }
}

proc CiHLT::interfaceSendArp { interface } {
    set arp_status [ ixNet exec sendArp $interface ]

    if { [ string match "::ixNet::OK" $arp_status ] } {
        puts $CiHLT::_SUCCESS

    } else {
        puts $CiHLT::_ERROR
    }
    return $arp_status
}

proc CiHLT::interfaceSendNs { interface } {

    set ns_status [ ixNet exec sendNs $interface ]

    if { [ string match "::ixNet::OK" $ns_status ] } {
        puts $CiHLT::_SUCCESS
    } else {
        puts $CiHLT::_ERROR
    }

    return $ns_status
}

proc CiHLT::interfaceSendRs { interface } {

    set rs_status [ ixNet exec sendRs $interface ]

    if { [ string match "::ixNet::OK" $rs_status ] } {
        puts $CiHLT::_SUCCESS
    } else {
        puts $CiHLT::_ERROR
    }

    puts $rs_status
}

proc CiHLT::interfaceEnableDHCPv4 { interface } {

    set dhcp_v4_status [ ixNet setA $interface/dhcpV4Properties -enabled true ]
    ixNet commit

    if { ! [ string match "::ixNet::OK" $dhcp_v4_status ] } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
    }
    return $dhcp_v4_status
}

proc CiHLT::interfaceEnableDHCPv6 { interface } {

    set dhcp_v6_status [ ixNet setA $interface/dhcpV6Properties -enabled true ]
    ixNet commit

    if { ! [ string match "::ixNet::OK" $dhcp_v6_status ] } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
    }
    return $dhcp_v6_status
}

proc CiHLT::interfaceGetDHCPV4IpAddress { interface } {

    set ip [ ixNet getA $interface/dhcpV4DiscoveredInfo -ipv4Address]
    puts $ip
    if { "4" != [ ::ip::version $ip ]  ||  "0" == $ip } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
    }
    return $ip
}

proc CiHLT::interfaceGetDHCPV6IpAddress { interface } {

    set ip [ ixNet getA $interface/dhcpV6DiscoveredInfo -ipv6Address]
    puts $ip
    if { $ip == "" } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
    }
    return $ip

}

proc CiHLT::interfaceGetDHCPV4DiscoveredInfo { interface attr } {
    set v [ ixNet getA $interface/dhcpV4DiscoveredInfo -$attr ]
    return $v
}

proc CiHLT::interfaceGetDHCPV6DiscoveredInfo { interface attr } {
    set v [ ixNet getA $interface/dhcpV6DiscoveredInfo -$attr ]
    return $v
}

#propose: configure DHCP client
#Input:
#return:
proc CiHLT::dhcpClientConfig { port mode inputs} {

        # set port_handle  [list $chasId/$card/$port]
        # set port_handle $port_list

        if {$mode != "create"} {
            set str "-mode $mode $inputs"
        } else {
             set portHandle [ eval CiHLT::getVPortHandle $port ]
             set str "-mode $mode -port_handle $portHandle $inputs"
        }
        set dhcp_portHandle_status [eval ::ixia::emulation_dhcp_config $str]
        puts $dhcp_portHandle_status
        if {[keylget dhcp_portHandle_status status] != $::SUCCESS} {
            CiHLT::logErr "ERROR: configure dhcp client"
            puts $CiHLT::_ERROR
            return [keylget dhcp_portHandle_status log]
        } else {
            puts $CiHLT::_SUCCESS
             CiHLT::log "SUCCESS: configure dhcp client: $port"
            #puts $dhcp_portHandle_status
            if { [string tolower $mode] == "create" } {
                set h [keylget dhcp_portHandle_status handle]
                return $h
            }  else {

            }
        }
}
#propose: configure DHCP client group
#Input:
#return:
proc CiHLT::dhcpClientGroupConfig {portHandle mode {inputs ""} } {

        set str "-mode $mode -handle $portHandle $inputs"
        #puts $str
        set dhcp_group_status [eval ::ixia::emulation_dhcp_group_config $str]
        #puts $dhcp_group_status
        if {[keylget dhcp_group_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr  "ERROR - [keylget dhcp_group_status log]"
            return [keylget dhcp_group_status log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:configure dhcp client group!"
            #puts "client=$dhcp_group_status"
            set ::CiHLT::dhcp_group_status $dhcp_group_status
            if { [string tolower $mode] == "create" } {
                set h [keylget dhcp_group_status handle]
                #hack to make sure handle can be use from iTest
                #puts $h
                set h [ regsub -all \" $h  "\\\""]
                return $h
            }
        }
}

proc CiHLT::delete_dhcp_client { args } {
    puts " Args: $args "
    foreach { key value } $args {
       set key [ string tolower $key ]
        switch -exact -- $key {
            -group_handle {
                ixNet remove $value
                ixNet commit
                after 1000
                puts $CiHLT::_SUCCESS
                return 
            }
            -port_handle {
                #set phandleres [::ixia::convert_porthandle_to_vport -port_handle $value]
                #set phandle [ keylget phandleres handle ]
                set phandle $value
                set prohandle [ ixNet getL $phandle protocolStack ]
                set ethhandlelist [ ixNet getL $prohandle ethernet ]
                if { $ethhandlelist != "" } {
                    foreach ethhandle $ethhandlelist {
                        set dhcphandle [ixNet getL $ethhandle dhcpEndpoint ]
                        if { $dhcphandle != "" } {
                            ixNet remove $ethhandle
                            ixNet commit
                            after 1000
                            puts $CiHLT::_SUCCESS
                            return
                        }
                        else {
                            puts $CiHLT::_ERROR
                            return
                        }
                    }
                }
            }
        }
    }
    puts $CiHLT::_ERROR
}

#propose: configure DHCP client control
#Input:
#return:
proc CiHLT::dhcpClientControl { port action { inputs " " } } {

        #set port_handle [list $chasId/$card/$port]
        set portHandle [ CiHLT::getVPortHandle $port ]
        set str "-port_handle $portHandle -action $action $inputs"
        set control_status_0 [eval ::ixia::emulation_dhcp_control $str]
        puts "::ixia::emulation_dhcp_control $str"
        puts $control_status_0
        if {[keylget control_status_0 status] != $::SUCCESS} {
            CiHLT::logErr  "ERROR:control dhcp client!"
            puts $CiHLT::_ERROR
            return [keylget control_status_0 log]
        } else {
            CiHLT::log "SUCCESS:control dhcp client!"
            puts $CiHLT::_SUCCESS
        }

}

#propose: configure DHCP client control by name
#Input:
#return:
proc CiHLT::dhcpClientControlByHandle { handle action { inputs " " } } {

        #set port_handle [list $chasId/$card/$port]
        #set portHandle [ CiHLT::getVPortHandle $port ]
        set str "-handle $handle -action $action $inputs"
        set control_status_0 [eval ::ixia::emulation_dhcp_control $str]
        puts "::ixia::emulation_dhcp_control $str"
        puts $control_status_0
        if {[keylget control_status_0 status] != $::SUCCESS} {
            CiHLT::logErr  "ERROR:control dhcp client!"
            puts $CiHLT::_ERROR
            return [keylget control_status_0 log]
        } else {
            CiHLT::log "SUCCESS:control dhcp client!"
            puts $CiHLT::_SUCCESS
        }
}

proc CiHLT::_getDHCPClientHandlesByPort { port } {
    set portHandle [ CiHLT::getVPortHandle $port ]
    set vport [::ixia::ixNetworkGetPortObjref $portHandle]
    set vport [keylget vport vport_objref]
    set eth [ ixNet getL $vport/protocolStack ethernet]
    set endpoints  [ ixNet getL $eth dhcpEndpoint ]
    set endpoint_range [ixNet getL $endpoints range]
    return $endpoint_range
}

#propose: get DHCP client stats
#Input:
#return:
proc CiHLT::dhcpClientStat {port mode {inputs ""} } {

        #set port_handle [list $chasId/$card/$port]

        set portHandle [ CiHLT::getVPortHandle $port ]
        set str "-port_handle $portHandle -mode $mode -version ixnetwork $inputs"
        set dhcp_stats_client [eval ::ixia::emulation_dhcp_stats $str]
        puts "::ixia::emulation_dhcp_stats $str"
        if {[keylget dhcp_stats_client status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR:get dhcp client stats"
            return [keylget dhcp_stats_client log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:get dhcp client stats"
            set ::CiHLT::stats $dhcp_stats_client
            puts $::CiHLT::stats
        }
}

#propose: get DHCP client stats
#Input:
#return:
proc CiHLT::dhcpClientStatByHandle {handle mode {inputs ""} } {

        #set port_handle [list $chasId/$card/$port]

        #set portHandle [ CiHLT::getVPortHandle $port ]
        set str "-handle $handle -mode $mode -version ixnetwork $inputs"
        set dhcp_stats_client [eval ::ixia::emulation_dhcp_stats $str]
        puts "::ixia::emulation_dhcp_stats $str"
        if {[keylget dhcp_stats_client status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR:get dhcp client stats"
            return [keylget dhcp_stats_client log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:get dhcp client stats"
            set ::CiHLT::stats $dhcp_stats_client
            puts $::CiHLT::stats
        }
}

#propose: configure DHCP server
#Input:
#return:
proc CiHLT::dhcpServerConfig {port mode inputs } {
        puts "Start dhcp server configuration ..."
        update idletasks
        if { $mode == "create"} {
            set portHandle [ eval CiHLT::getVPortHandle $port ]
            set str "-mode $mode -port_handle $portHandle $inputs"
        } else {
            set str "-mode $mode $inputs"
        }
        puts "::ixia::emulation_dhcp_server_config $str"
        set dhcp_server_config_status [eval ::ixia::emulation_dhcp_server_config $str]
        if {[keylget dhcp_server_config_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR to config dhcp server"
            return [keylget dhcp_server_config_status log]
        } else {
            puts $CiHLT::_SUCCESS
             CiHLT::log "SUCCESS:configure dhcp server."
            if { [string tolower $mode] == "create" } {
                set dhcp_server_session_handle [keylget dhcp_server_config_status handle.dhcp_handle]
                return $dhcp_server_session_handle
            }
        }
}

#propose: DHCP server control
#Input:
#return:
proc CiHLT::dhcpServerControl { port action { inputs " " } } {

        #set port_handle [list $chasId/$card/$port]
        set portHandle [ eval CiHLT::getVPortHandle $port ]
        set str "-port_handle $portHandle -action $action $inputs"
        puts "::ixia::emulation_dhcp_server_control $str"
        set control_status_1 [eval ::ixia::emulation_dhcp_server_control $str]
        puts $control_status_1
        if {[keylget control_status_1 status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR to control dhcp server."
            return [keylget control_status_1 log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:control dhcp server"
        }
}

#propose: DHCP server control
#Input:
#return:
proc CiHLT::dhcpServerControlByHandle { handle action { inputs " " } } {

        #set port_handle [list $chasId/$card/$port]
        #set portHandle [ eval CiHLT::getVPortHandle $port ]
        set str "-dhcp_handle $handle -action $action $inputs"
        puts "::ixia::emulation_dhcp_server_control $str"
        set control_status_1 [eval ::ixia::emulation_dhcp_server_control $str]
        puts $control_status_1
        if {[keylget control_status_1 status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR to control dhcp server."
            return [keylget control_status_1 log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:control dhcp server"
        }
}

#propose: get DHCP server stats
#Input:
#return:
proc CiHLT::dhcpServerStat { port action { inputs " " } } {

        #set port_handle [list $chasId/$card/$port]
        set portHandle [ eval CiHLT::getVPortHandle $port ]
        set str "-port_handle $portHandle -action $action $inputs"
        set dhcp_stats_server [eval ::ixia::emulation_dhcp_server_stats $str]
        puts "::ixia::emulation_dhcp_server_stats $str"
        if {[keylget dhcp_stats_server status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR:get dhcp stats."
            return [keylget dhcp_stats_server log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:get dhcp stats."
            set ::CiHLT::stats $dhcp_stats_server
        }
}

#propose: get DHCP server stats
#Input:
#return:
proc CiHLT::dhcpServerStatByHandle { handle action { inputs " " } } {

        set str " -dhcp_handle $handle -action $action $inputs"
        puts "::ixia::emulation_dhcp_server_stats $str"
        set dss [eval ::ixia::emulation_dhcp_server_stats $str]
        puts "::ixia::emulation_dhcp_server_stats $str"
        if {[keylget dss status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR: failed to get dhcp server stats."
            return [keylget dss log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:get dhcp stats."
            set ::CiHLT::stats $dss
        }
}

#propose: test control (no supported on HLT version 4.30)
#Input:
#return:
proc CiHLT::_ixia_test_control { action {inputs ""} } {
    switch -exact [string tolower $action] {
        "start_all_protocols" { set ret [ixNet exec startAllProtocols]}
        "stop_all_protocols" { set ret [ixNet exec stopAllProtocols]}
        "start" {
                set handle [ get_opt_value "$inputs" "handle" ]
                 # handle dhcp_server handle
                switch -regexp $handle {
                    "/dhcpServerRange$"  { set handle [regsub -- "/dhcpServerRange" $handle "" ] }
                }
                set ret [ixNet exec start $handle]
                }
        "stop" {
                set handle [ get_opt_value "$inputs" "handle" ]
                 # handle dhcp_server handle
                switch -regexp $handle {
                    "/dhcpServerRange$"  { set handle [regsub -- "/dhcpServerRange" $handle "" ] }
                }
                set ret [ixNet exec stop $handle]
                }
        default { puts "FAIL - invalid to $action"; return }
                }
    if { $ret != "::ixNet::OK" } {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR:ixia test control."
        return "not able to $action"
    } else {
        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS:ixia test control"
    }
}
proc CiHLT::get_ixia_version { } {
    set ver [package req Ixia]
    return $ver
}
proc CiHLT::testControl {action {inputs "" } } {
        set ver [CiHLT::get_ixia_version]
        if { $ver <= "6.20" } {
            CiHLT::_ixia_test_control $action $inputs
        } else {
            set str "-action $action $inputs"
            set ret [eval ::ixia::test_control $str]
            if {[keylget ret status] != $::SUCCESS} {
                puts $CiHLT::_ERROR
                CiHLT::logErr "ERROR:test control."
                return [keylget ret log]
            } else {
                puts $CiHLT::_SUCCESS
                CiHLT::log "SUCCESS:test control."
            }
        }
}
#propose: Stop all protocols
#Input:
#return:
proc CiHLT::_ixia_StopAllProtocols { } {
    if {[catch {ixNet exec stopAllProtocols} msg]} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR:ixia_StopAllProtocols."
        return "failed to stop all protocols!"
    } else {
        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS:test control."
    }
    after 12000
}
#propose: traffic configure
#Input:
#return:
proc CiHLT::trafficConfig { mode inputs} {

        set str "-mode $mode $inputs"

        set traffic_status [eval ::ixia::traffic_config $str]
        if {[keylget traffic_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR-configure traffic"
            return [keylget traffic_status log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:configure traffic"
            #puts $traffic_status
            if { [string tolower $mode] == "create" } {
                set h [keylget traffic_status stream_id]
                return $h
            }
        }
}
#propose: traffic control
#Input:
#return:
proc CiHLT::trafficControl {port action use_low_api {inputs "" } } {
        if {$action=="run"} {
            set root [ixNet getRoot]
            set restartCapture 0
            set restartCaptureJudgement 0
            set portList [ ixNet getL $root vport ]
            foreach hPort $portList {
                set cstate [ixNet getA $hPort/capture -isCaptureRunning]
                if { $cstate == "true" } {
                    set restartCapture 1
                    break
                }
            }
            if { $restartCapture } {
                catch {
                    ixNet exec stopCapture
                    after 2000
                    ixNet exec closeAllTabs
                    set restartCaptureJudgement 1
                }
            }
            set trafficList [ ixNet getL $root/traffic trafficItem ]
                    foreach traffic $trafficList {
                if { [ ixNet getA $traffic -state ] == "unapplied" } {
                    ixNet exec apply $root/traffic
                    after 1000
                }
                lappend flowList [ ixNet getL $traffic highLevelStream]
            }
            set lport [ eval CiHLT::getVPortHandle $port ]
            set phandleres [::ixia::convert_porthandle_to_vport -port_handle $lport]
            set phandle [keylget phandleres handle]
            foreach flow $flowList {
                foreach deepFlow $flow {
                    set txPort [ ixNet getA $deepFlow -txPortId ]
                    set state [ ixNet getA $deepFlow -state]

                    if { $state != "started"} {
                        if { $txPort == $phandle } {
                            lappend txList $deepFlow
                        }
                    }
                }
            }
                    if { $restartCaptureJudgement } {
                catch {
                    ixNet exec startCapture
                    after 2000
                }
            }
            ixNet exec startStatelessTraffic $txList

            set timeout 30
            puts $CiHLT::_SUCCESS
        } else {
            set portHandle [ eval CiHLT::getVPortHandle $port ]
            set str "-port_handle $portHandle -action $action $inputs"
            set traffic_status [eval ::ixia::traffic_control $str]
            if {[keylget traffic_status status] != $::SUCCESS} {
                puts $CiHLT::_ERROR
                CiHLT::logErr "ERROR: $action traffic control: $traffic_status"
                return [keylget traffic_status log]
            } else {
                puts $CiHLT::_SUCCESS
                CiHLT::log "SUCCESS:$action traffic control"
            }
        }
}
#propose: get traffic stats
#Input:
#return:
proc CiHLT::trafficStat { mode {option ""}} {

    set traffic_status [::ixia::traffic_stats \
        -mode                   $mode \
        -traffic_generator      ixnetwork \
        ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR: $mode traffic stats"
        return [keylget traffic_status log]
    } else {
        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS:$mode traffic stats"
    }
    set ::CiHLT::stats $traffic_status
}

#propose: get traffic stats
#Input:
#return:
proc CiHLT::trafficStatOnPort { mode port {generator ixnetwork} } {

    set portHandle [ eval CiHLT::getVPortHandle $port ]

    set traffic_status [::ixia::traffic_stats \
        -mode                   $mode \
        -traffic_generator      $generator \
        -port_handle            $portHandle \
        ]
    if {[keylget traffic_status status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR: $mode traffic stats"
        return [keylget traffic_status log]
    } else {
        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS:$mode traffic stats"
    }
    set ::CiHLT::stats $traffic_status
}

#propose: configure buffer
#Input:
#return:
proc CiHLT::packetConfigBuffers { port action {inputs ""} } {
        #ixia engineer said action not support in ixnetwork, so we omit it
        set str "-port_handle $port $inputs"
        set config_status [eval ::ixia::packet_config_buffers $str]
        if {[keylget config_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR: $port configure buffer"
            return [keylget config_status log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:$port configure buffer"
        }
}
#propose: configure filter
#Input:
#return:
proc CiHLT::packetConfigFilter { port mode {inputs ""}} {

        set str "-port_handle $port -mode $mode $inputs"
        set config_status [eval ::ixia::packet_config_filter $str]
        if {[keylget config_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR:$port configure filter"
            return [keylget config_status log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "$port configure filter"
        }
}
#propose: configure trigger
#Input:
#return:
proc CiHLT::packetConfigTriggers { port mode {inputs ""}} {

        set str "-port_handle $port -mode $mode $inputs"
        set config_status [eval ::ixia::packet_config_triggers $str]
        if {[keylget config_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            CiHLT::logErr "ERROR:$port configure trigger"
            return [keylget config_status log]
        } else {
            puts $CiHLT::_SUCCESS
            CiHLT::log "SUCCESS:$port configure trigger"
        }

}
#propose: packet control
#Input:
#return:
proc CiHLT::packetControl {{port} action {inputs ""}} {

    # if { $action == "start" } {

    #     if {[catch [ixNet exec apply [ixNet getRoot]traffic] msg]} {
    #         puts "Apply traffic successful!"
    #         puts $CiHLT::_SUCCESS
    #     } else {
    #         puts "Failed to apply traffic, $msg"
    #         puts $CiHLT::_ERROR
    #     }
    #     after 50000
    # }

    set str "-port_handle $port -action $action $inputs"
    set start_status [eval ::ixia::packet_control $str]
    if {[keylget start_status status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR:$port packet control"
        return [keylget start_status log]
    } else {
        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS: $port packet control"
    }
}

#propose: get packet stats
#Input:
#return:
proc CiHLT::packetStats { port filename stop pkt_mode {inputs ""} } {
    # temp fix can not save captured packets to file for IXIA version 7.3
        # set str "-port_handle $port -stop $stop $inputs"
        # set s_status [eval ::ixia::packet_stats $str]
        # if {[keylget s_status status] != $::SUCCESS} {
        #     puts $CiHLT::_ERROR
        #     CiHLT::logErr "ERROR: $port get packet stats"
        #     return [keylget s_status log]
        # } else {
        #     CiHLT::log "SUCCESS:$port get packet stats"
        # }

        if { [catch {ixNet exec saveCapture "c:/Public"} msg] } {
            puts $CiHLT::_ERROR
            puts "Failed to save captured packets!"
            CiHLT::logErr "ERROR - Failed to save captured packets!"
        } else {
            puts "Successed to save captrued packets to ."
        }

        regsub -all "/" $port "-" portName
        if { $pkt_mode == "data"} {
            puts "storing data packets."
            set filecap "${portName}_HW.cap"
        } elseif { $pkt_mode == "control" } {
            puts "storing control packets."
            set filecap "${portName}_SW.cap"
        } else {
            puts $CiHLT::_ERROR
            return
        }
        set res [ixNet exec copyFile [ixNet readFrom "c:/Public/$filecap" -ixNetRelative] [ixNet writeTo $filename -overWrite]]
        puts $CiHLT::_SUCCESS
}

#propose: save ixia captured packets to file
#Input:
#return:
proc CiHLT::saveCapToFile_old { dir name { name2 "" } } {
   variable folder
    set hcnt 0
    set folder [clock format [clock seconds] -format "%Y_%B_%d_%H_%M_%S"]
    set path $dir/$folder
    file mkdir $path
    if { [catch {ixNet exec saveCapture $path} msg] } {
        puts "ERROR - Failed to save captured packets!"
    } else {
        puts "SUCCESS - Successed to save captrued packets!"
    }
    cd $dir/$folder
    set fLst [glob *.cap]
    set lo [llength $fLst]
    if { $lo == 2 } {
        for {set i 0} {$i < $lo} {incr i} {
            set filename [lindex $fLst $i]
            set rname [file rootname $filename]
            set b [lindex [split $rname _] 1]
            if {$b == "HW"} {
                file rename -force $filename ${name}_HW.cap
                file copy -force $path/${name}_HW.cap $dir/${name}_HW.cap
            } elseif { $b == "SW" } {
                file rename -force $filename ${name}_SW.cap
                file copy -force $path/${name}_SW.cap $dir/${name}_SW.cap
            } else {
                return error
            }
        }
    } elseif { $lo == 4 } {
        for {set i 0} {$i < $lo} {incr i} {
            set filename [lindex $fLst $i]
            set rname [file rootname $filename]
            set b [lindex [split $rname _] 1]
            if {$b == "HW"} {
                if {$hcnt == 1} {
                        file rename -force $filename ${name2}_HW.cap
                        file copy -force $path/${name2}_HW.cap $dir/
                    } else {
                        file rename -force $filename ${name}_HW.cap
                        file copy -force $path/${name}_HW.cap $dir/
                        incr cnt 1
                    }
            } elseif { $b == "SW" } {
                if {$scnt == 1} {
                    file rename -force $filename ${name2}_SW.cap
                    file copy -force $path/${name2}_SW.cap $dir/
                    incr hcnt 1
                } else {
                    file rename -force $filename ${name}_SW.cap
                    file copy -force $path/${name}_SW.cap $dir/
                    incr scnt 1
                }

            } else {
                return error
            }
        }
    } elseif { $lo == 0 } {

        puts "no files found"
    } else {

        puts "there are more than 4 files in $dir/$folder"
    }
}
#propose: save ixia captured packets to file
#Input:
#return:
proc CiHLT::saveCapToFile { dir {name ""} { name2 "" } } {
   variable folder
    set hcnt 0
    set scnt 0

    set folder [clock format [clock seconds] -format "%Y_%B_%d_%H_%M_%S"]
    set path $dir/$folder
    file mkdir $path
    cd $dir/$folder
    if { [catch {ixNet exec saveCapture $path} msg] } {
        puts $CiHLT::_ERROR
        puts "Failed to save captured packets!"
        CiHLT::logErr "ERROR - Failed to save captured packets!"
    } else {
        puts $CiHLT::_SUCCESS
        puts "Successed to save captrued packets to $dir and backup file in $path!"
        CiHLT::log "ERROR - Failed to save captured packets!"
    }
    if {$name != ""} {
        cd $dir/$folder
        set fLst [glob *.cap]
        set lo [llength $fLst]
        if { $lo == 2 } {
            for {set i 0} {$i < $lo} {incr i} {
                set filename [lindex $fLst $i]
                set rname [file rootname $filename]
                set b [lindex [split $rname _] 1]
                if {$b == "HW"} {
                    file rename -force $filename ${name}_HW.cap
                    file copy -force $path/${name}_HW.cap $dir/${name}_HW.cap
                } elseif { $b == "SW" } {
                    file rename -force $filename ${name}_SW.cap
                    file copy -force $path/${name}_SW.cap $dir/${name}_SW.cap
                } else {
                    return error
                }
            }
        } elseif { $lo == 4 } {
            for {set i 0} {$i < $lo} {incr i} {
                set filename [lindex $fLst $i]
                set rname [file rootname $filename]
                set b [lindex [split $rname _] 1]
                if {$b == "HW"} {
                    if {$hcnt == 1} {
                            if {$name2 != ""} {
                                file rename -force $filename ${name2}_HW.cap
                                file copy -force $path/${name2}_HW.cap $dir/
                                } else {
                                    return "name2 is empty!"
                                }

                        } else {
                            file rename -force $filename ${name}_HW.cap
                            file copy -force $path/${name}_HW.cap $dir/
                            incr cnt 1
                        }
                } elseif { $b == "SW" } {
                    if {$scnt == 1} {
                            if {$name2 != ""} {
                                file rename -force $filename ${name2}_HW.cap
                                file copy -force $path/${name2}_HW.cap $dir/
                            } else {
                                return "name2 is empty!"
                            }
                        file rename -force $filename ${name2}_SW.cap
                        file copy -force $path/${name2}_SW.cap $dir/
                        incr hcnt 1
                    } else {
                        file rename -force $filename ${name}_SW.cap
                        file copy -force $path/${name}_SW.cap $dir/
                        incr scnt 1
                    }
                } else {
                    return error
                }
            }
        } elseif { $lo == 0 } {

            puts "no files found"
        } else {

            puts "there are more than 4 files in $dir/$folder"
        }
    } else {
        puts "file name is keep unchanged!"
        set fLst [glob *.cap]
        set lo [llength $fLst]
        for {set i 0} {$i < $lo} {incr i} {
            set filename [lindex $fLst $i]
            file copy -force $path/$filename $dir/
        }
    }
    return $folder
}
proc CiHLT::get_list_value {keylist key} {

    set value [keylget keylist $key]
    return $value
}

#propose: IGMP Querier Config
#Input:
#return:
proc CiHLT::igmpQuerierConfig { handle mode inputs} {

        if { [string tolower $mode] == "create" } {
            set str "-port_handle $handle -mode $mode $inputs"
        } else {
            set str "-mode $mode -handle $handle  $inputs"
        }

        puts "[::ixia::emulation_igmp_querier_config $str]"

        set config_igmp_querier_status [eval ::ixia::emulation_igmp_querier_config $str]
        if {[keylget config_igmp_querier_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return [ keylget config_igmp_querier_status log ]
        } else {
            puts $CiHLT::_SUCCESS
            if { [string tolower $mode] == "create" } {
                set igmp_querier_handle [keylget config_igmp_querier_status handle]
                return $igmp_querier_handle
            }
      }
}

proc CiHLT::getIGMPQuerierInterface { querier_handler } {

    set interface [ ixNet getA $querier_handler -interfaces ]
    puts $interface
    return interface
}

#propose: IGMP control
#Input:
#return:
proc CiHLT::igmpControl { handle mode } {

        if { [string tolower $mode] == "start" ||  [string tolower $mode] == "stop" } {
            set str "-handle $handle -mode $mode "
        } else {
            set str "-mode $mode"
        }

        set igmp_status [eval ::ixia::emulation_igmp_control $str]
        if {[keylget igmp_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return $igmp_status
        } else {
            puts $CiHLT::_SUCCESS
        }
}

#propose: IGMP configure
#Input:
#return:
proc CiHLT::igmpConfig { handle mode inputs} {

        if { [string tolower $mode] == "create" } {
            set str "-port_handle $handle -mode $mode $inputs"
        } elseif { [string tolower $mode] == "disable_all" } {
            set str "-port_handle $handle -mode $mode $inputs"
        } else {
            set str "-handle $handle -mode $mode $inputs"
        }

        set config_igmp_status [eval ::ixia::emulation_igmp_config $str]
        if {[keylget config_igmp_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return [keylget config_igmp_status log]"
        } else {
            puts $CiHLT::_SUCCESS
            if { [string tolower $mode] == "create" } {
                set session_handle [keylget config_igmp_status handle]
                return $session_handle
            }
        }
}

#propose: IGMP group configure
#Input:
#return:
proc CiHLT::igmpGroupConfig { handle mode inputs} {
        if { [string tolower $mode] == "create" } {
            set str "-mode $mode $inputs"
        } else {
            set str "-handle $handle -mode $mode $inputs"
        }

        set group_status [eval ::ixia::emulation_igmp_group_config $str]
        if {[keylget group_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return [keylget group_status log]"

        } else {
            puts $CiHLT::_SUCCESS
            if { [string tolower $mode] == "create" } {
                set group_member_handle [keylget group_status handle]
                return $group_member_handle
            }
        }
}

#propose: IGMP statistics
#Input:
#return:
proc CiHLT::igmpInfo {port_handle mode} {

        set str "-port_handle $port_handle -mode $mode"
        set igmp_status [eval ::ixia::emulation_igmp_info $str]
        if {[keylget igmp_status status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return [keylget igmp_status log]

        } else {
            puts $CiHLT::_SUCCESS
            set ::CiHLT::stats $igmp_status
            puts $::CiHLT::stats
        }
}


#propose: Multicast group config
#Input:
#return:
proc CiHLT::multcastGroupConfig {handle mode inputs} {

        if { [string tolower $mode] == "create" } {
            set str "-mode $mode $inputs"
        } else {
            set str "-handle $handle -mode $mode $inputs"
        }

        set ret_group [eval ::ixia::emulation_multicast_group_config $str]
        if {[keylget ret_group status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return [keylget ret_group log]

        } else {
            puts $CiHLT::_SUCCESS
            if { [string tolower $mode] == "create" } {
                set group_handle [keylget ret_group handle]
                return $group_handle
            }
        }
}

#propose: Multicast source config
#Input:
#return:
proc CiHLT::multcastSourceConfig {handle mode inputs} {

        if { [string tolower $mode] == "create" } {
            set str "-mode $mode $inputs"
        } else {
            set str "-handle $handle -mode $mode $inputs"
        }

        set ret_source [eval ::ixia::emulation_multicast_source_config $str]
        if {[keylget ret_source status] != $::SUCCESS} {
            puts $CiHLT::_ERROR
            return [keylget ret_source log]

        } else {
            puts $CiHLT::_SUCCESS
            if { [string tolower $mode] == "create" } {
                set source_handle [keylget ret_source handle]
                return $source_handle
            }
        }
}

#propose: configure PPPOX
#Input:
#return:
proc CiHLT::pppoxConfig {port mode inputs } {

    puts "Start pppoe server configuration ..."
    update idletasks

    set portHandle [ eval CiHLT::getVPortHandle $port ]
    set str "-port_handle $portHandle -mode $mode $inputs"

    set pppox_config_status [eval ::ixia::pppox_config $str]
    if {[keylget pppox_config_status status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR: $port configure pppox"
        return [keylget pppox_config_status log]
    } else {

        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS: $port configure pppox"
        if { [string tolower $mode] == "add" } {
            set pppox_session_handle [keylget pppox_config_status handle]
            puts "{handle $pppox_session_handle}"
            return $pppox_session_handle
        }  else {
            return ""
        }
    }
}

#propose: PPPOX control
#Input:
#return:
proc CiHLT::pppoxControl { portHandle action { inputs " " } } {

    #set port_handle [list $chasId/$card/$port]
    set str "-handle $portHandle -action $action $inputs"
    set control_status [eval ::ixia::pppox_control $str]
    if {[keylget control_status status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::log "ERROR: control pppox $portHandle"
        return [keylget control_status log]
    } else {
        puts $CiHLT::_SUCCESS
        CiHLT::log "SUCCESS: control pppox $portHandle"
    }
    after 5000
}

#propose: PPPOX stats
#Input:
#return:
proc CiHLT::pppoxStats { port handle mode { inputs " " } } {

    #set port_handle [list $chasId/$card/$port]
    set portHandle [ eval CiHLT::getVPortHandle $port ]
    set str "-port_handle $portHandle -handle $handle -mode $mode $inputs"
    set pppox_stats [eval ::ixia::pppox_stats $str]
    if {[keylget pppox_stats status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR:get $port pppox stats"
        return [keylget pppox_stats log]
    } else {
        puts "SUCCESS!!"
        CiHLT::log "SUCCESS: get $port pppox stats"
        set ::CiHLT::stats $pppox_stats
        return $pppox_stats
    }
}

proc CiHLT::pppoxStatsByPort { port mode { inputs " "} } {

    set portHandle [ eval CiHLT::getVPortHandle $port ]
    set str "-port_handle $portHandle -mode $mode $inputs"
    set pppox_stats [eval ::ixia::pppox_stats $str]
    if {[keylget pppox_stats status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
        CiHLT::logErr "ERROR:get $port pppox stats"
        return [keylget pppox_stats log]
    } else {
        puts "SUCCESS!!"
        CiHLT::log "SUCCESS: get $port pppox stats"
        set ::CiHLT::stats $pppox_stats
        return $pppox_stats
    }
}

#propose: temp
#Input:
#return:
proc CiHLT::temp {args} {

    ################################################################################
    # LINK STATUS - Check port link status - up
    ################################################################################

    # Default value for desired status = up

    puts "check port link state desired status - up"

    set port_link_status [::ixia::test_control -action check_link_state -port_handle $port_handle]

    if {[keylget port_link_status status] != $::SUCCESS} {
        puts "ERROR - $test_name - [keylget port_link_status log]"
        return 0
    }

    foreach port $port_handle {
        set port_status [keylget port_link_status $port.state]
        if {$port_status != "up"} {
            puts "ERROR - Port $port doesnt have desired state set"
            incr cfgError
        } else {
            puts "Port $port State : $port_status"
        }
    }

    puts ">>> STARTING ALL PROTOCOLS..."
    set start_protcols_status [::ixia::test_control -action start_all_protocols -port_handle $port_handle]
    ################################################################################
    # Collect traffic stats
    ################################################################################

    for {set try 0} {$try < 30} {incr try} {
        set res_instantaneous [ixia::traffic_stats  \
            -mode traffic_item                      \
            -measure_mode instantaneous             \
        ]
        if {[keylget res_instantaneous status] != $::SUCCESS} {
            error "traffic_stats run failed: $res"
        }
        if {![keylget res_instantaneous waiting_for_stats]} {
            break
        }
        after 1000
    }

    for {set try 0} {$try < 30} {incr try} {
        set res_cumulative [ixia::traffic_stats     \
            -mode traffic_item                      \
            -measure_mode cumulative                \
        ]
        if {[keylget res_cumulative status] != $::SUCCESS} {
            error "traffic_stats run failed: $res"
        }
        if {![keylget res_cumulative waiting_for_stats]} {
            break
        }
        after 1000
    }
    ################################################################################
    # Collect traffic stats
    ################################################################################

    for {set try 0} {$try < 30} {incr try} {
        set res_instantaneous [ixia::traffic_stats  \
            -mode aggregate                         \
            -measure_mode instantaneous             \
        ]
        if {[keylget res_instantaneous status] != $::SUCCESS} {
            error "traffic_stats run failed: $res"
        }
        if {![keylget res_instantaneous waiting_for_stats]} {
            break
        }
        after 1000
    }

    for {set try 0} {$try < 30} {incr try} {
        set res_cumulative [ixia::traffic_stats     \
            -mode aggregate                         \
            -measure_mode cumulative                \
        ]
        if {[keylget res_cumulative status] != $::SUCCESS} {
            error "traffic_stats run failed: $res"
        }
        if {![keylget res_cumulative waiting_for_stats]} {
            break
        }
        after 1000
    }
}

# ######
# proc to handle hlt api get stats issue for dhcp clients
# ######
proc CiHLT::_ixnet_get_vport { port } {
	set s1 [lindex [ split $port "/" ] 0]
	set s2 [lindex [ split $port "/" ] 1]
	#puts "$s1 $s2"
	set vPorts [ixNet getList [ixNet getRoot] vport]
	foreach p $vPorts {
		 set r [lindex [ ixTclNet::GetAssignmentInfo $p ] 0]
		 #puts $r
		 set r0 [lindex $r 0]
		 set r1 [lindex $r 1]
		 set r2 [lindex $r 2]
		 #puts "$r1 $r2"
		 if { $r1 == $s1 && $r2 == $s2 } {
			return $p
		 }
	}
}

proc CiHLT::_ixnet_get_dhcp_count { port } {
	set vport [ CiHLT::_ixnet_get_vport $port]
	set eth [ixNet getList $vport/protocolStack ethernet]
	set dhcpEndpoint [lindex [ixNet getList $eth dhcpEndpoint] 0 ]
	set range [ ixNet getL $dhcpEndpoint range ]
	return [llength $range]
}

proc CiHLT::_ixnet_get_dhcp_mac {port {index 0}} {
	set vport [ CiHLT::_ixnet_get_vport $port]
	set eth [ixNet getList $vport/protocolStack ethernet]
	set dhcpEndpoint [lindex [ixNet getList $eth dhcpEndpoint] 0 ]
	set range [lindex [ ixNet getL $dhcpEndpoint range ] $index ]
	set name [ ixNet getA $range/dhcpRange -name ]
	set mac [ ixNet getA $range/macRange -mac]
	set count [ ixNet getA $range/macRange -count]
	set increment [ ixNet getA $range/macRange -incrementBy]

	set _mac [regsub -all \: $mac ""]
	set _mac [expr 0x$_mac]
	#puts $_mac
	set _increment [regsub -all \: $increment ""]
	set _increment [expr 0x$_increment]
	#puts $_increment

	set l_mac ""
	for { set i 0 } { $i < $count } { incr i 1 } {
		set hex [ format %012X [expr {$_mac + ($_increment * $i)} ] ]
		set _hex [split $hex ""]
		set tmp ""
		for { set j 0} { $j < [llength $_hex]} { incr j 1} {
			append tmp [lindex $_hex $j]
			if { [expr {$j % 2} ] } {
				append tmp ":"
			}
		}
		lappend l_mac [ string range $tmp 0 end-1 ]
	}
	set ret  ""
	lappend ret "$name"
	lappend ret "$l_mac"
	return $ret
}

proc CiHLT::_ixnet_get_dhcp_stats {} {
	puts "Add the custom view"
	set custom_view [ixNet add [ixNet getRoot]/statistics view]
	ixNet setAttr $custom_view -caption "dhcp_client_per_session_stats"
	ixNet setAttr $custom_view -type layer23ProtocolStack
	ixNet setAttr $custom_view -visible true
	ixNet commit
	set custom_view [lindex [ixNet remapIds $custom_view] 0]

	puts "Retrieve relevant filters for the view"
	set availableProtocolStackFilter [ixNet getList $custom_view availableProtocolStackFilter]
	set name DHCP-R
	set filters ""
	foreach af $availableProtocolStackFilter {
		if { [ regexp $name $af ] } { lappend filters $af}
	}
	puts "filters=$filters"
	puts "Configure the filter selection area"
	ixNet setMultiAttr $custom_view/layer23ProtocolStackFilter                       \
		-drilldownType          perSession                                           \
		-numberOfResults        500                                                  \
		-protocolStackFilterId  "$filters"
	ixNet commit
	puts "Configuring the sorting order"
	ixNet setMultiAttr $custom_view/layer23ProtocolStackFilter                       \
		-sortAscending          true                                                 \
		-sortingStatistic       [lindex [ixNet getList $custom_view statistic] 1]
	ixNet commit

	puts "Enable the stats columns to be disaplyed"
	set statsList [ixNet getList $custom_view statistic]
	foreach stat $statsList {
		ixNet setAttr $stat -enabled true
	}
	ixNet commit

	puts "Get the custom view going and start retrieveing stats"
	ixNet setAttribute $custom_view -enabled true
	ixNet commit
	after 10000
	#show result

	#puts [ ixNet getAttribute ${custom_view}/page -columnCaptions ]
	set ret [ ixNet  getAttribute ${custom_view}/page -rowValues ]
	#set ret [ixNet getAttribute ${custom_view}/page -rowCount ]
	ixNet remove $custom_view
	ixNet commit
	return $ret
}

proc CiHLT::_get_dhcp_mac_and_ipaddr { port } {

	set num [ CiHLT::_ixnet_get_dhcp_count $port ]
	array set dhcp_mac ""
	for {set i 0} { $i < $num } {incr i 1} {
		set _info [ CiHLT::_ixnet_get_dhcp_mac $port $i]
		set name [lindex $_info 0]
		set lmac [lindex $_info 1]
		set cnt 0
		foreach mac $lmac {
			set cnt [ incr cnt 1 ]
			set dhcp_mac(${name}:${cnt}) $mac
		}
	}

	array set dhcp_ip ""

	set lret [ CiHLT::_ixnet_get_dhcp_stats ]
	set lname ""
	foreach l $lret {
		set l [lindex $l 0]
		set port [lindex $l 0]
		set name [lindex $l 2]
		#puts $port,$name
		lappend lname $name
		set ip [lindex $l 10]
		#puts $ip
		set dhcp_ip($name) $ip
	}

	array set dhcp_info ""
	foreach name $lname {
		set dhcp_info($name) "$dhcp_mac($name) $dhcp_ip($name)"
	}
	return [array get dhcp_info]
}
# test
# CiHLT::get_dhcp_mac_and_ipaddr 8/4

proc CiHLT::cfmConfig { port mode { inputs ""} } {

    if { $mode == "create" } {
        set port_handle [ CiHLT::getPortHandle $port ]
        set str "-mode create -port_handle $port_handle $inputs"
    } else {
        set str "-mode $mode $inputs"
    }

    set res [ eval ::ixia::emulation_cfm_config $str ]

    if {[keylget res status] != $::SUCCESS} {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
        if { $mode == "create"} {
            set handles [ keylget res handle ]
            return "{handle $handles}"
        }
    }
}

proc CiHLT::cfmMdMegConfig { bridge_handle mode {inputs "" } } {

    if { $mode == "create" } {
        set str "-mode create -bridge_handle $bridge_handle $inputs"
    } else {
        set str "-mode $mode $inputs"
    }

    set res [ eval ::ixia::emulation_cfm_md_meg_config $str ]

    if { [keylget res status ] != $::SUCCESS } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS

        if { $mode == "create"} {
            set handles [ keylget res handle ]
            return "{handle $handles}"
        }
    }
}

proc CiHLT::cfmMipMepConfig { bridge_handle mode { inputs ""}} {

    if { $mode == "create" } {
        set str "-mode create -bridge_handle $bridge_handle $inputs"
    } else {
        set str "-mode $mode $inputs"
    }

    set  res [ eval ::ixia::emulation_cfm_mip_mep_config $str ]

    if { [keylget res status] != $::SUCCESS } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
        if { $mode == "create" } {
            set handles [ keylget res handle ]
            return "{handle $handles}"
        }
    }
}

proc CiHLT::cfmVlanConfig { bridge_handle mode { inputs ""}} {

    if { $mode == "create" } {
        set str "-mode $mode -bridge_handle $bridge_handle $inputs"
    } else {
        set str "-mode $mode $inputs"
    }

    set res [ eval ::ixia::emulation_cfm_vlan_config $str ]

    if { [ keylget res status ] != $::SUCCESS } {
        puts $CiHLT::_ERROR
        return $res
    } else {
        puts $CiHLT::_SUCCESS
        if { $mode == "create" } {
            set handles [ keylget res handle ]
            return "{handle $handles}"
        }
    }
}

proc CiHLT::cfmLinksConfig { bridge_handle mode { inputs ""}} {

    if { $mode == "create" } {
        set str "-mode $mode -bridge_handle $bridge_handle $inputs"
    } else {
        set str "-mode $mode $inputs"
    }

    set res [ eval ::ixia::emulation_cfm_links_config $str ]

    if { [ keylget res status ] != $::SUCCESS } {
        puts $CiHLT::_ERROR
        return $res
    } else {
        puts $CiHLT::_SUCCESS
        if { $mode == "create" } {
            set handles [ keylget res handle ]
            return "{handle $handles}"
        }
    }
}

proc CiHLT::cfmControl { port mode } {

    set port_handle [ CiHLT::getPortHandle $port]
    set res [ eval ::ixia::emulation_cfm_control -mode $mode \
              -port_handle $port_handle ]

    if { [keylget res status] != $::SUCCESS } {
        puts $CiHLT::_ERROR
    } else {
        puts $CiHLT::_SUCCESS
    }
}
