package provide CalixStcHltApi 1.00

if { [catch {
    package req SpirentHltApi
    package req stc
    package req stclib
    package req SpirentTestCenter
} err ] } {
    puts $err
} else {
    puts "Spirent STC HLTAPI has been loaded!"
}

namespace eval CsHLT {
    set LOGTS ""
    set handles ""
    set stats ""
    set log_enable ""
    set RETURNVALUE ""
	set ERROR ""
    set __ERROR ERROR
	set __SUCCESS SUCCESS
	variable CT [clock format [clock seconds] -format "%B_%d_%H_%M_%S"]
}
#*************************************************************************************************
#Purpose: Get port info after chassis session was established.
# args:
#	==>
#Author :
#*************************************************************************************************
proc CsHLT::get_port_handle {port} {
    #puts $CsHLT::handles
    return [keylget CsHLT::handles "port_$port"]
}

proc CsHLT::get_stream_handle {{sname}} {
    set portkeylist [keylkeys CsHLT::handles]
    foreach portkey $portkeylist {
        set portHdl [keylget CsHLT::handles "$portkey"]
        set streamHdlList [::stc::get $portHdl -children-StreamBlock]
        foreach streamHdl "$streamHdlList" {
            set streamName [::stc::get $streamHdl -Name]
            if {[string compare $sname $streamName] == 0} {
                return "ret:$streamHdl"
            }
         }
    }
    return ""
}
#*************************************************************************************************
#Purpose: enable HLTAPI log info.
# args:
#	==> path : spicify a location for log path.
#Author :James.cao
#*************************************************************************************************
proc CsHLT::enable_hltlog {path} {
    variable CT
    puts "====>$CT"
    set res [eval ::sth::test_config -logfile $path/hltLogfile \
                 -log 1\
                 -vendorlogfile $path/stcExport\
                 -vendorlog 1\
                 -hltlog 1\
                 -hltlogfile hltExport\
                 -hlt2stcmappingfile $path/hlt2StcMapping\
                 -hlt2stcmapping 1\
                 -log_level 7 ]
    keylget res status status
    if {$status == 1} {
        CsHLT::log "hltlog enabled!"
        puts $CsHLT::__SUCCESS
    } else {
        CsHLT::logErr "failed to enable hltlog!"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to enable hltlog!"
    }
}

#*************************************************************************************************
#Purpose: enable output log info(make dir and open file).
# args:
#	==> path : spicify a location for log path.
#Author :James.cao
#*************************************************************************************************
proc CsHLT::logOn {log_path} {
	variable logFileId
	variable CT

	#set LOGTS [clock format [clock seconds] -format "%B_%d_%H_%M_%S"]
	file mkdir "$log_path/Log_$CsHLT::CT"
	if {[catch {set logFileId [open $log_path/Log_$CsHLT::CT/scriptLog.txt w]}]} {
		CsHLT::logErr "Open script log file failed!"
        lappend CsHLT::ERROR "failed to open file!"
        puts $CsHLT::__ERROR
        return
	} else {
        #set ::CsHLT::log_enable 1
        CsHLT::log "log enabled!"
        puts $CsHLT::__SUCCESS
    }
    set folder "$log_path/Log_$CsHLT::CT"
    CsHLT::enable_hltlog $folder
}

#*************************************************************************************************
#Purpose: write output log info to file.
# args:
#	==> msg : msg info .
#Author :James.cao
#*************************************************************************************************
proc CsHLT::log { msg } {
	variable logFileId
	variable line ""
	#variable ll1
	if {[info exists logFileId]} {
		append line [clock format [clock seconds] -format "%A %B %d %H:%M:%S"] "==>$msg"
		puts $logFileId $line
		flush $logFileId
        #puts $CsHLT::__SUCCESS
		puts "$msg"
	} else {return "ERROR"}
}
proc CsHLT::logErr {msg} {
	variable logFileId
	variable line ""
	#variable l1
	if {[info exists logFileId]} {
		append line [clock format [clock seconds] -format "%A %B %d %H:%M:%S"] "==>ERROR:$msg"
		puts $logFileId $line
		flush $logFileId
		puts "$msg"
        #puts $CsHLT::__SUCCESS
	} else {
		return "ERROR"
	}
}
#*************************************************************************************************
#Purpose: print stats info with a processed format, user can choose keyword to specify which kind
#	of stats can be displayed.
# args:
#	[option]==> key: keyword for result list, user can specify the keyword which you want to be
#			displayed.
#Author :Kelvin Lee
#*************************************************************************************************
proc CsHLT::print_stats {{key ""}} {
	set error 0
    puts "printing stats..."
    if { $key == "" } {
        #if { [catch {set kl $::CsHLT::stats } retCode] } {
        #    puts "PASSED!"
        #} else {
        #    puts "FAILED - Failed to print stats - $retCode!"
        #}
        set kl $::CsHLT::stats
    } else {
        if { [catch {set tmp [keylget ::CsHLT::stats $key] } retCode] } {
            CsHLT::logErr "FAILED - Failed to print stats - $retCode"
            #lappend CsHLT::ERROR "Failed to print stats - $retCode"
            puts $CsHLT::__ERROR
            set error 1
        } else {
            keylset kl $key $tmp
            CsHLT::log "PASSED!"
			puts $CsHLT::__SUCCESS
        }
    }

    puts [string repeat "#" 45]
    set stats [::CsHLT::keylprint $kl]
    #puts $stats
    puts [string repeat "#" 45]
    puts $CsHLT::__SUCCESS
    #puts PASS
    #CsHLT::log $stats
	#if {!$error} {
	#	puts $CsHLT::__SUCCESS
	#}
}

#*************************************************************************************************
#Purpose: print stats list with a processed format.
# args:
#	==>listvalues: all values of list
#	[option]==> indentationLevel: counts of indentation
#	[option]==> indentString :indentString
#Author :Kelvin Lee
#*************************************************************************************************
proc ::CsHLT::keylprint {listvalues {indentationLevel 0} {indentString "    "}} {
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

#*************************************************************************************************
#Purpose: Connect to STC chassis.
# args:
#	==> chasIp: STC chassis ip address.
#	==> portList: STC port list.
#Author :James Cao
#*************************************************************************************************
proc CsHLT::connect_to_chas {chasIp portList {xml ""} } {
	CsHLT::log "Connecting to Chassis $chasIp..."
	if { $xml == "" } {
		set res [eval ::sth::connect -device $chasIp -port_list "$portList"  -break_locks 1]
	} else {
		CsHLT::log "Loading xml file $xml"
		set res0 [eval ::sth::load_xml -filename "$xml"]
		CsHLT::log "$res0"
		keylget res0 status status
		if {!$status} {
            lappend CsHLT::ERROR "failed to load xml: $res0"
		    puts $CsHLT::__ERROR
		    return 1
		} else {
		    set res [eval ::sth::connect -device $chasIp -port_list "$portList" -offline 0 -break_locks 1]
		}
	}
    foreach p $portList {
        set a [keylget res port_handle.$chasIp.$p]
        #puts $a
        #keylset ::CsHLT::handles "port.$p" $a
        keylset CsHLT::handles "port_$p" $a
    }
    CsHLT::log "res=============>$res"
	keylget res status status
	if {!$status} {
		#puts $res
		CsHLT::logErr "FAILED: $res"
        lappend CsHLT::ERROR "failed to connect to chassis: $res"
		puts $CsHLT::__ERROR
		return 1
	} else {
		CsHLT::log "Connected to $chasIp and ports $portList were(was) reserved!"
		puts $CsHLT::__SUCCESS
        if {[llength $portList] == 2} {
            set port1 [lindex $portList 0]
            set port2 [lindex $portList 1]
            keylget res port_handle.$chasIp.$port1 host1
            keylget res port_handle.$chasIp.$port2 host2
            set portHandles "$host1 $host2"
            return $portHandles
        }
    }

}

#*************************************************************************************************
#Purpose: STC interface property configure.
# args:
#	==> portList: STC interface list.
#	==> mode: configure or modify interface.
#	[option]==> options: Default is null,extend option for other parameter configure.
#Author :James Cao
#*************************************************************************************************
proc CsHLT::interface_conf {port mode {options ""}} {

	CsHLT::log "$mode interface $port is in process..."
    set port_handle [CsHLT::get_port_handle $port]
    #puts "handle ====> $handle"
    if { $mode == "create" } {
        set opts "-mode $mode -port_handle $port_handle $options"
    } else {
        set opts "-mode $mode -port_handle $port_handle $options"
    }
	#set opts "-mode $mode -port_handle $handle $options"
	puts $opts
	set res [eval ::sth::interface_config $opts]
	CsHLT::log "response info: ====> $res"
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to config interface: $res"
		puts $CsHLT::__ERROR
		return
	} else {
		CsHLT::log "$mode interface $port is done!"
		puts $CsHLT::__SUCCESS
	}
}

#*************************************************************************************************
#Purpose: DHCP server configure.
# args:
#	==> port: STC test ports
#	==> mode: create, modify or delete
#   [option]==>options: Default is null,extend option for other parameter configure..
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_server_create {port {options ""} {version 4}} {

	CsHLT::log "Create dhcp server is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-mode create -port_handle $handle $options"
	#puts "opts ===> -mode $mode -port_handle $port $options"
	set res [ eval ::sth::emulation_dhcp_server_config  $opts]
	CsHLT::log "response info: ====> $res"
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to config dhcp server"
		puts $CsHLT::__ERROR
		return
	} else {
		CsHLT::log "Create dhcp server is done!"
		puts $CsHLT::__SUCCESS
	}
	if {$version ==	4} {
        return [keylget res handle.dhcp_handle]
    } elseif {$version == 6} {
        return [keylget res handle.dhcpv6_handle]
    }
}

#*************************************************************************************************
#Purpose: DHCP server custom options configure.
# args:
#	==> server_handle: STC server port handle
#	==> option_type: options which defined in RFC 2132 , such as 1,3,43,82
#   ==> msg_type:which response message will be included in when the option set.
#       valid params:OFFER ACK NAK
#       and the combination value with |   example: OFFER|ACK
#   ==> enable_wildcards:if the option is wildcards
#       valid params:TRUE or FALSE
#   ==> hex_value:if the option string is hexadecimal.
#       valid params:TRUE or FALSE
#   ==> payload: option payload
#Author :Jeff Zou
#*************************************************************************************************
proc CsHLT::create_dhcp_server_option { server_handle  option_type  msg_type  enable_wildcards  hex_value  payload } {

	CsHLT::log "Start create dhcp server custom option..."
	puts $server_handle

	set dhcpv4serverconfig [ stc::get $server_handle -children-Dhcpv4ServerConfig ]
	puts $dhcpv4serverconfig

	set dhcpv4serverdefaultpoolconfig [ stc::get $dhcpv4serverconfig -children-Dhcpv4ServerDefaultPoolConfig ]
	puts $dhcpv4serverdefaultpoolconfig

    set dhcpv4ServerMsgOption [ stc::create "Dhcpv4ServerMsgOption" \
        -under $dhcpv4serverdefaultpoolconfig \
        -OptionType $option_type \
        -EnableWildcards $enable_wildcards \
        -MsgType $msg_type \
        -HexValue $hex_value \
        -Payload $payload  ]
    puts $dhcpv4ServerMsgOption
    if { [ string match "*dhcpv4servermsgoption*" $dhcpv4ServerMsgOption ] } {
        puts $CsHLT::__SUCCESS
        return $dhcpv4ServerMsgOption
    }
    puts $CsHLT::__ERROR

}


#*************************************************************************************************
#Purpose: DHCP client basic configure.
# args:
#	==> port: STC test ports
#	==> mode: create, modify or delete
#   [option]==>options: Default is null,extend option for other parameter configure..
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_client_basic_create {port {options ""}} {

	CsHLT::log "Create dhcp client is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-mode create -port_handle $handle $options"
	puts $opts
	set res [eval sth::emulation_dhcp_config $opts]
	puts "sth::emulation_dhcp_config  $opts"
	CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to create dhcp basic"
        puts $CsHLT::__ERROR
    	return
    } else {
    	CsHLT::log "Create dhcp client is done!"
        puts $CsHLT::__SUCCESS
    }
    return [keylget res handles]

}

#*************************************************************************************************
#Purpose: DHCP client group configure, including session nums.
# args:
#	==> handle: handle info from dhcp client configure
#	==> mode: create, modify or delete
#   [option]==>options: Default is null,extend option for other parameter configure..
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_client_group_conf {handle mode {options ""} {version 4}} {

	CsHLT::log "$mode dhcp client group is in process..."
	set opts "-handle $handle -mode $mode $options"
	set res [eval sth::emulation_dhcp_group_config $opts]
    puts $res
	CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to configure dhcp client group"
		puts $CsHLT::__ERROR
        return
    } else {
    	puts $CsHLT::__SUCCESS
    	CsHLT::log "$mode dhcp client group is done!"
        #puts PASS
    }
    if {$version == 4} {
        return [keylget res handle]
    } elseif {$version == 6} {
        return [keylget res dhcpv6_handle]
    }

}


#*************************************************************************************************
#Purpose: DHCP server protocol control.
# args:
#	==> portHandle: get the handle info when connected to chassis
#	==> mode: connect or reset
#   [option]==>options: Default is null,extend option for other parameter configure..
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_server_ctrl {port mode {options ""}} {

	CsHLT::log "$mode dhcp sever is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-port_handle $handle -action $mode $options"
	set res [ eval sth::emulation_dhcp_server_control  $opts]
	CsHLT::log "response info: ====> $res"

	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
		puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to $mode dhcp server"
        #puts FAIL
		return
	} else {
		puts $CsHLT::__SUCCESS
		CsHLT::log "$mode DHCP server..."
	}

	after 5000
}

#*************************************************************************************************
#Purpose: DHCP client protocol control.
# args:
#	==> portHandle: get the handle info when connected to chassis
#	==> mode: bind or release
#   [option]==>options: Default is null,extend option for other parameter configure..
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_client_ctrl {port mode {options ""}} {

	CsHLT::log "$mode dhcp client is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-port_handle $handle -action $mode $options"
	puts "sth::emulation_dhcp_control $opts"
    set res [eval sth::emulation_dhcp_control $opts]
	CsHLT::log "response info: ====> $res"

	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
		puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to $mode dhcp client"
        #puts FAIL
		return
	} else {
		puts $CsHLT::__SUCCESS
		CsHLT::log "$mode DHCP client..."
	}

	after 5000
}


#*************************************************************************************************
#Purpose: get DHCP server stats.
# args:
#	==> portHandle: get the handle info when connected to chassis
#	==> mode: collect or clear.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_server_stats {handle mode {option ""}} {

	CsHLT::log "$mode dhcp server stats is in process..."
    #set handle [CsHLT::get_port_handle $port]
	set opts "-dhcp_handle $handle -action $mode $option"
	set res [ eval sth::emulation_dhcp_server_stats $opts]
	CsHLT::log "response info: ====> $res"
	set ::CsHLT::stats $res
    CsHLT::log $res
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
		puts $CsHLT::__ERROR
        lappend CsHLT::ERROR " failed to $mode dhcp server"
        #puts FAIL
		return
	} else {
		puts $CsHLT::__SUCCESS
		CsHLT::log "Successful to $mode DHCP server stats"
        #puts PASS
        #return $res
	}
}

#*************************************************************************************************
#Purpose: get DHCP client stats.
# args:
#	==> portHandle: get the handle info when connected to chassis
#	==> mode: collect or clear.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::dhcp_client_stats {port mode {option ""}} {

	CsHLT::log "$mode dhcp client stats is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-port_handle $handle -action $mode $option"
	set res [ eval sth::emulation_dhcp_stats $opts]
	CsHLT::log "response info: ====> $res"
	set ::CsHLT::stats $res
    CsHLT::log $res
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
		puts $CsHLT::__ERROR
        lappend CsHLT::ERROR " failed to $mode dhcp client stats"
        #puts FAIL
		return
	} else {
		puts $CsHLT::__SUCCESS
		CsHLT::log "Successful to $mode DHCP client stats"
        #puts PASS
        return $res
	}
}

#*************************************************************************************************
#Purpose: Logout STC and clear all configurations.
# args:
#	==> portList: All ports which had been reserved.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::cleanup_session {port_list} {
    CsHLT::log "cleanup session..."
    puts "$port_list"
    set handle ""
    set ph ""

    foreach p $port_list {
        set ph [CsHLT::get_port_handle $p]
        lappend handle $ph
    }
    set prj [stc::get $ph -parent]

	set res [eval ::sth::cleanup_session -port_handle $handle -maintain_lock 0 -clean_dbfile 1 -clean_labserver_session 1]
    #set res [eval ::sth::cleanup_session]

    stc::create port -under $prj
    stc::create port -under $prj

	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED: $res"
		puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to cleanup session"
        #puts FAIL
		return
	} else {
		puts $CsHLT::__SUCCESS
		CsHLT::log "Session is cleaned successfully!"
		stc::waituntilcomplete
        #puts PASS
	}
    #CsHLT::log $CsHLT::ERROR
}

#*************************************************************************************************
#Purpose: Save current configuration to xml file.
# args:
#	==> project
#	==> filename: specify saved file name, also can be a absolute path of file.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::save_as_xml { filename {project project1} } {
    CsHLT::log "Save xml configure file is in progress..."
	set opts " -config $project -filename $filename"
	if {[catch {eval stc::perform saveasxml $opts} msg] } {
		CsHLT::logErr "ERROR: $msg"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to save xml configure file"
	} else {
        CsHLT::log "PASSED: Successful to save to xml configure file!"
        puts $CsHLT::__SUCCESS
	}
}

#*************************************************************************************************
#Purpose: load configuration from a xml file.
# args:
#	==> filename: specify a xml file name, also can be a absolute path of file.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::load_xml_config {filename} {

    CsHLT::log "Load xml configure file is in progress..."

	if {[catch {eval sth::load_xml -filename $filename} msg]} {
		CsHLT::logErr "ERROR: $msg"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to load xml configure"
	} else {
        CsHLT::log "Successful to load $filename !"
        puts $CsHLT::__SUCCESS

    }
}

proc CsHLT::get_all_stream_names_and_handles { } {
    set portkeylist [keylkeys CsHLT::handles]
    set d "#"
    foreach portkey $portkeylist {
        set portHdl [keylget CsHLT::handles "$portkey"]
        set streamHdlList [::stc::get $portHdl -children-StreamBlock]
        foreach streamHdl "$streamHdlList" {
            set streamName [::stc::get $streamHdl -Name]
            append d $streamName "#" $streamHdl "#"
        }
    }
    return $d
}

proc CsHLT::startAllProtocol {} {
    CsHLT::log "start all protocol"
    if {[catch {eval sth::start_devices} msg]} {
        CsHLT::logErr "ERROR: $msg"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to start the protocol"
    } else {
        CsHLT::log "Successful to start the protocol!"
        puts $CsHLT::__SUCCESS
        stc::waituntilcomplete
    }
}

proc CsHLT::stopAllProtocol {} {
    CsHLT::log "stop all protocol"
    if {[catch {eval sth::stop_devices} msg]} {
        CsHLT::logErr "ERROR: $msg"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to stop the protocol"
    } else {
        CsHLT::log "Successful to stop the protocol!"
        puts $CsHLT::__SUCCESS
        stc::waituntilcomplete
    }
}

proc CsHLT::DevicesStartAllCommand {} {
    CsHLT::log "Start All the Devices"

    set res [ stc::perform DevicesStartAllCommand]

    puts $res

    set v [ split $res "-"]

    foreach item $v {
        set k [lindex $item 0]
        if { $k == "State" } {
            if { [lindex $item 1] == "COMPLETED" } {
                puts $CsHLT::__SUCCESS
                return
            }
        }
    }
    puts $CsHLT::__ERROR
}

proc CsHLT::DevicesStopAllCommand {} {
    CsHLT::log "Stop All the Devices"
    set res [ stc::perform DevicesStopAllCommand]
    puts $res

    set v [ split $res "-"]

    foreach item $v {
        set k [lindex $item 0]
        if { $k == "State" } {
            if { [lindex $item 1] == "COMPLETED" } {
                puts $CsHLT::__SUCCESS
                return
            }
        }
    }
    puts $CsHLT::__ERROR
}

proc CsHLT::apply {} {
    CsHLT::log "apply the config"
    if {[catch {eval stc::apply} msg]} {
        CsHLT::logErr "ERROR: $msg"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to apply configure"
    } else {
        CsHLT::log "Successful to apply config!"
        puts $CsHLT::__SUCCESS
    }
}

#*************************************************************************************************
#Purpose: Creates, modifies, removes, or resets a stream block of network traffic on
#        the specified test port(s). A stream is a series of packets that can be
#        tracked by Spirent HLTAPI. A stream block is a collection of one or
#        more streams represented by a base stream definition plus one or more rules
#        that describe how the base definition is modified to produce additional
#        streams..
# args:
#	==> mode: Creates, modifies, removes, or resets.
#   ==> port: STC ports
#   [option]==> options: Default is null,extend option for other parameter configure.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::traffic_conf {mode port {options ""}} {

    CsHLT::log "$mode traffic is in process..."

    if { [string tolower $mode] == "create" } {
        set handle [CsHLT::get_port_handle $port]
        set opts "-mode $mode -port_handle $handle $options"
    } else {
        set opts "-mode $mode $options"
    }
    set res [eval sth::traffic_config $opts ]
    #puts "sth::traffic_config $opts"
    #puts "[string repeat * 30]"
    #puts "return info is ========> $res"
    #puts "[string repeat * 30]"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to $mode traffic"
        return
    }
    CsHLT::log "$mode traffic is done!"
    if { $mode == "create" } {
        keylget res stream_id streamid
        puts $CsHLT::__SUCCESS
        return $streamid
    } else {
        puts $CsHLT::__SUCCESS
        return
    }
}


proc CsHLT::traffic_disable {streamid {options ""}} {

    CsHLT::log "Disable traffic is in process..."
    set opts "-mode disable -stream_id $streamid $options"
    set res [eval sth::traffic_config $opts ]
    #puts "============================="
    #puts "return info is ========> $res"
    #puts "============================="
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to disable traffic"
        return
    }
    CsHLT::log "disable traffic is done!"
    keylget res stream_id streamid
    return $streamid
}


#*************************************************************************************************
#Purpose: Controls traffic generation on the specified test ports
# args:
#	==> action: start or stop, clear_stats.
#   ==> port: STC ports
#   [option]==> options: Default is null,extend option for other parameter configure.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::traffic_ctrl {action port {options ""}} {

	CsHLT::log "$port $action traffic is in process..."
    set handle [CsHLT::get_port_handle $port]
    CsHLT::log "$handle"
	set opts "-port_handle $handle -action $action $options"
	set res [eval sth::traffic_control $opts]

	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to $action traffic"
		return
	}
    CsHLT::log "$action traffic is done!"
    puts $CsHLT::__SUCCESS
    after 3000
}

proc CsHLT::traffic_ctrl_by_name {action stream_handle {options ""}} {

	CsHLT::log "$action traffic is in process..."
    #set handle [CsHLT::get_port_handle $port]
    CsHLT::log "$stream_handle"
	set opts "-stream_handle $stream_handle -action $action $options"
	set res [eval sth::traffic_control $opts]

	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to $action traffic"
		return
	}
    CsHLT::log "$action traffic is done!"
    puts $CsHLT::__SUCCESS
    after 3000
}

proc CsHLT::start_all_traffic {{ports} {options ""}} {

	CsHLT::log "start traffic is in process..."

    set opts "-port_handle $ports -action run $options"
	set res [eval sth::traffic_control $opts]
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to start all traffic"
		return
	}
    CsHLT::log "start all traffic is done!"
    after 3000
}


proc CsHLT::stop_all_traffic {{ports} {options ""}} {

	CsHLT::log "stop traffic is in process..."

    set opts "-port_handle $ports -action stop $options"
	set res [eval sth::traffic_control $opts]

	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to stop all traffic"
		return
	}
    CsHLT::log "stop all traffic is done!"
    after 3000
}

#*************************************************************************************************
#Purpose: Retrieves statistical information about traffic streams
# args:
#	==> action: Specifies the type of statistics to collect: aggregate,out_of_filter,detailed_streams,all
#   ==> port: STC ports
#   [option]==> options: Default is null,extend option for other parameter configure.
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::traffic_stats {mode port {options ""}} {

	CsHLT::log "Retrieves $mode traffic statistics is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-mode $mode -port_handle $handle $options"
	set res [eval sth::traffic_stats $opts]
    #puts "return res is =======> $res"
	set ::CsHLT::stats $res
    CsHLT::log $res
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to stop all traffic"
		return
	}
    CsHLT::log "$mode traffic stats is done!"
    puts $CsHLT::__SUCCESS
    return $res
}

#*************************************************************************************************
#Purpose: Defines how Spirent HLTAPI will manage the buffers for packet capturing.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************

proc CsHLT::packetConfigBuffers { port action {inputs ""} } {
    CsHLT::log "$action capture buffer is in process..."
    set opts "-port_handle $port -action $action $inputs"
	set res [eval sth::packet_config_buffers $opts]
	CsHLT::log "response info: ====> $res"
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to config capture buffer"
        return [keylget res log]
	} else {
		CsHLT::log "$action capture buffer is done!"
        puts $CsHLT::__SUCCESS
	}
}
#*************************************************************************************************
#Purpose: Defines the condition (trigger) that will start or stop packet capturing.
#         By default, Spirent HLTAPI captures all data and control plane packets
#         that it sends and all data plane packets that it receives.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::packetConfigTriggers { port mode {inputs ""}} {

        set str "-port_handle $port -mode $mode $inputs"
        set res [eval sth::packet_config_triggers $str]
        keylget res status status
        if {!$status} {
            CsHLT::logErr "FAILED:  $res"
            puts $CsHLT::__ERROR
            lappend CsHLT::ERROR "failed to configure capture trigger"
            return
        } else {
            CsHLT::log "capture trigger is done!"
            puts $CsHLT::__SUCCESS
        }
}

#*************************************************************************************************
#Purpose: Defines how Spirent HLTAPI will filter the captured data. If you do not
#         define any filters, Spirent HLTAPI captures all data.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::packetConfigFilter { port mode {inputs ""}} {

        set str "-port_handle $port -mode $mode $inputs"
        set res [eval sth::packet_config_filter $str]
        keylget res status status
        if {!$status} {
            CsHLT::logErr "FAILED:  $res"
            puts $CsHLT::__ERROR
            lappend CsHLT::ERROR "failed to configure capture filter"
            return
        } else {
            CsHLT::log "capture filter is done!"
            puts $CsHLT::__SUCCESS
            return PASS
        }
}

#*************************************************************************************************
#Purpose: Defines how Spirent HLTAPI will manage the buffers for packet capturing.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::cap_conf_ctrl {{port_handle} action} {

    CsHLT::log "$action capture is in process..."
	set opts "-port_handle $port_handle -action $action"
	set res [eval sth::packet_control $opts]
	CsHLT::log "response info: ====> $res"
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to $action capture"
		return
	} else {
		CsHLT::log "$action capture is done!"
        puts $CsHLT::__SUCCESS
	}
}

#*************************************************************************************************
#Purpose: Returns information about the status of the packet capture.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::cap_conf_info {handle} {

    CsHLT::log "get capture info is in process..."
	set opts "-port_handle $handle -action status"
	set res [eval sth::packet_info $opts]
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to get capture info"
		return
	} else {
		CsHLT::log "get capture info is done!"
		keylget res stopped stopped
        puts $CsHLT::__SUCCESS
		return "ret:$stopped"
	}
}
#*************************************************************************************************
#Purpose: Returns statistical information about each packet associated with the specified
#         port(s). Statistics include the connection status and number and type of messages
#         sent and received from the specified port.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::cap_conf_stats {port_handle filename {format "pcap"} {options ""}} {

    CsHLT::log "get capture stats is in process..."
	set opts "-port_handle $port_handle -action filtered -format $format -filename $filename $options"
	set res [eval sth::packet_stats $opts]
	CsHLT::log "response info: ====> $res"
	keylget res status status
	if {!$status} {
		CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to get capture stats"
		return
	} else {
		CsHLT::log "get capture stats is done!"
        puts $CsHLT::__SUCCESS
	}
}

#*************************************************************************************************
#Purpose: Defines how Spirent HLTAPI will manage the PPPox Conf
# args:
#	==>
#   ==>
#   [option]==>
#Author :Shawn.Wang
#*************************************************************************************************
proc CsHLT::pppoe_client_conf {  port mode {options ""} } {

    if { $mode == "create" } {
        set handle [CsHLT::get_port_handle $port]
        set opts "-port_handle $handle -mode $mode $options "
    } else {
        set opts "-mode $mode $options"
    }
    set res [eval sth::pppox_config $opts]
    puts "$res\n"
    keylget res status status
    if { !$status } {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILD to Conf pppoe client: $res"
        exit 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "PPPoe Conf is done!"
        keylget res handle clientHandle
        return $clientHandle
    }
}

proc CsHLT::pppoe_client_create {port {options ""}} {

	CsHLT::log "create pppoe is in process..."

    set handle [CsHLT::get_port_handle $port]
    set opts "-port_handle $handle -mode create $options"
    set res [eval sth::pppox_config  $opts ]
    puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to create pppoe:  $res"
        exit 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "create pppoe is done!"
        keylget res handle clientHandle
        return $clientHandle

    }
}
#*************************************************************************************************
proc CsHLT::pppoe_client_modify {handle {options ""}} {

	CsHLT::log "modify pppoe is in process..."
    set opts "-handle $handle -mode modify $options"
    set res [eval sth::pppox_config  $opts ]
    #puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to modify pppoe:  $res"
        exit 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "modify pppoe is done!"
    }
}

#*************************************************************************************************
#Purpose: Defines how Spirent HLTAPI will manage the buffers for packet capturing.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::pppoe_client_ctrl {handle action {options ""}} {

	CsHLT::log "$action pppoe is in process..."
	set opts "-handle $handle -action $action $options"
	set res [eval sth::pppox_control $opts]
	#puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $action pppoe:  $res"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$action pppoe is done!"
        #keylget res handles pppoe_handles
        #return pppoe_handles
    }
}

proc CsHLT::pppoe_client_stats {handle mode {options ""}} {

	CsHLT::log "$mode pppoe statictics is in process..."
	set opts "-handle $handle -mode $mode $options"
	set res [eval sth::pppox_stats $opts]
  set ::CsHLT::stats $res
	#puts "$res\n"
  keylget res status status
  if { !$status} {
      puts $CsHLT::__ERROR
      CsHLT::logErr "FAILED to $mode pppoe statictics:  $res"
      return 0
  } else {
      puts $CsHLT::__SUCCESS
      CsHLT::log "$mode pppoe statictics is done!"
      #keylget res handles pppoe_handles
      #return pppoe_handles
    }
}

proc CsHLT::pppoe_server_conf { port mode {options ""} } {
    if { $mode == "create" } {
        set handle [CsHLT::get_port_handle $port]
        set opts "-port_handle $handle -mode $mode $options"
    } else {
        set opts "-mode $mode $options"
    }
    set res [eval sth::pppox_server_config $opts]
    puts "$res\n"
    keylget res status status

    if { !$status } {
        puts $CsHLT::ERROR
        CsHLT::logErr "FAILD to config pppoe server!"
    } else {
        puts $CsHLT::__SUCCESS
        if { $mode == "create" } {
            keylget res handle serverHandle
            return $serverHandle
        }
    }
}

proc CsHLT::pppoe_server_create {port {options ""}} {

	CsHLT::log "create pppoe server is in process..."
    set handle [CsHLT::get_port_handle $port]
	set opts "-port_handle $handle -mode create $options"
	set res [eval sth::pppox_server_config $opts]
	puts "=====================>$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode pppoe server :  $res"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "create pppoe server is done!"
        #keylget res handles pppoe_handles
        #return pppoe_handles
        keylget res handle serverHandle
        return $serverHandle
    }
}

proc CsHLT::pppoe_server_ctrl {handle action {options ""}} {

	CsHLT::log "$action pppoe server is in process..."
	set opts "-handle $handle -action $action $options"
	set res [eval sth::pppox_server_control $opts]
	#puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $action pppoe server:  $res"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$action pppoe server is done!"
        #keylget res handles pppoe_handles
        #return pppoe_handles
    }
}

proc CsHLT::pppoe_server_stats {handle mode {options ""}} {

	CsHLT::log "$mode pppoe server statictics is in process..."
	set opts "-handle $handle -mode $mode $options"
	set res [eval sth::pppox_server_stats $opts]
	puts "$res"
    set ::CsHLT::stats $res
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode pppoe server statictics:  $res"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode pppoe server statictics is done!"
        #keylget res handles pppoe_handles
        #return pppoe_handles
    }
}

proc CsHLT::device_conf { port mode {options ""}} {

    CsHLT::log "$mode devce is in process..."

    if { $mode == "create" } {
        set handle [CsHLT::get_port_handle $port]
        set opts "-port_handle $handle -mode create $options"
    } else {
        set opts "-mode $mode $options"
    }

    set res [eval sth::emulation_device_config $opts]

    puts "$res"

    set ::CsHLT::stats $res
    keylget res status status

    if { !$status } {
        puts $CsHLT::ERROR
        CsHLT::logErr "FAILD to $mode device"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        if { $mode == "create" } {
            CsHLT::log "$mode device is done"
            keylget res handle deviceHandle
            puts "{handle : $deviceHandle}"
            return "$deviceHandle"
        } else {
            return 0
        }
    }
}

proc CsHLT::device_send_ping { host_handle  dst_ip } {

    set host_ip [ eval stc::get $host_handle -ipv4address ]

    puts $host_ip

    set res [ stc::perform PingStartCommand -DeviceList $host_handle \
                  -WaitForPingToFinish true -PingIpv4SrcAddr $host_ip \
                  -PingIpv4DstAddr $dst_ip ]
    puts $res
    set port [ stc::get $host_handle -affiliationport-targets ]
    set pingreport [ stc::get $port -children-pingreport ]
    set result [ stc::get $pingreport -pingresult ]
    foreach line [ split $result "\r\n" ] {
        if { [ string match "*ping*" $line ] || [ string match "*packets transmitted*" $line ] } {
            puts $CsHLT::__SUCCESS
            return $result
        }
    }
    puts $CsHLT::__ERROR
}

proc CsHLT::device_send_arp { host_handle } {

    set port [ stc::get $host_handle -affiliationport-targets ]

    stc::perform ArpNdStartCommand -HandleList $host_handle \
        -WaitForArpToFinish true -ForceArp true

    set report [ stc::get $port -children-arpndreport ]

    set count [ stc::get $report -attemptedarpndcount ]

    if { $count > 0 } {
        puts $CsHLT::__SUCCESS
        return [ eval stc::get $report -arpndstatus ]
    } else {
        puts $CsHLT::__ERROR
    }
}

proc CsHLT::start_arp_nd_on_all_devices { } {

    set portkeylist [keylkeys CsHLT::handles]
    set port_list ""
    foreach portkey $portkeylist {
        set portHdl [keylget CsHLT::handles "$portkey"]
        lappend port_list $portHdl
    }

    set res [ stc::perform ArpNdStartOnAllDevicesCommand -PortList "$port_list" \
              -WaitForArpToFinish true ]
    puts $res

    set v [ split $res "-"]

    foreach item $v {
        set k [lindex $item 0]
        if { $k == "State" } {
            if { [lindex $item 1] == "COMPLETED" } {
                puts $CsHLT::__SUCCESS
                return
            }
        }
    }
    puts $CsHLT::__ERROR
}

proc CsHLT::igmp_conf {mode handle {options ""}} {

    CsHLT::log "$mode igmp is in process..."

    if { [string tolower $mode] == "create" } {
        set opts "-mode $mode -port_handle $handle $options"
    } elseif { [string tolower $mode] == "disable_all" } {
        set opts "-mode $mode -port_handle $handle $options"
    } else {
        set opts "-handle $handle -mode $mode $options"
    }

    set res [eval sth::emulation_igmp_config  $opts ]
    puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode igmp:  $res"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode igmp is done!"
        if { [string tolower $mode] == "create" } {
            keylget res handle igmpHandle
            return "$igmpHandle"
        }
    }
}


proc CsHLT::igmp_ctrl {mode handle {options ""}} {

    CsHLT::log "$mode igmp is in process..."

    set opts "-handle $handle -mode $mode $options"
    set res [eval sth::emulation_igmp_control  $opts ]
    #puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode igmp:  $res"
        return 0
    } else {
        after 10000
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode igmp is done!"

    }
}

proc CsHLT::igmp_group_conf {mode {options ""}} {

    CsHLT::log "$mode igmp group is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_igmp_group_config  $opts ]
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode igmp group:  $res"
        return 0
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode igmp group is done!"
        if { [string tolower $mode] == "create" } {
            keylget res handle igmpGroup
            return $igmpGroup
        }
    }
}

proc CsHLT::igmp_info {handle {options ""}} {

    CsHLT::log "get igmp info is in process..."

    set opts "-port_handle $handle $options"
    set res [eval sth::emulation_igmp_info $opts ]
    #puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to get igmp info:  $res"
        return 0
    } else {
        set ::CsHLT::stats $res
        puts $CsHLT::__SUCCESS
        CsHLT::log "get igmp info is done!"
        return $res
    }
}

proc CsHLT::igmp_querier_conf { mode handle {options ""}} {

    CsHLT::log "$mode igmp querier is in process..."
    if { [string tolower $mode] == "create" } {
        set opts "-mode $mode -port_handle $handle $options"
    } else {
        set opts "-handle $handle -mode $mode $options"
    }
    set res [eval sth::emulation_igmp_querier_config $opts]
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode igmp querier:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode igmp querier is done!"
        if { [string tolower $mode] == "create" } {
            keylget res handle igmpQuerier
            return $igmpQuerier
        }
    }
}

proc CsHLT::igmp_querier_ctrl {mode handle {options ""}} {

    CsHLT::log "$mode igmp querier is in process..."
    set opts "-mode $mode -handle $handle $options"
    set res [eval sth::emulation_igmp_querier_control $opts ]
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode igmp querier:  $res"
        return
    } else {
        after 10000
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode igmp querier is done!"

    }
}

proc CsHLT::igmp_querier_info {handle {options ""}} {

    CsHLT::log "igmp querier info is in process..."
    set opts "-port_handle $handle $options"
    set res [eval sth::emulation_igmp_querier_info $opts ]
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to igmp querier info:  $res"
        return
    } else {
        set ::CsHLT::stats $res
        puts $CsHLT::__SUCCESS
        CsHLT::log "igmp querier info is done!"
        return $res
    }
}

proc CsHLT::check_querier_state {igmp_querier_handle node } {

    foreach i $igmp_querier_handle {
        keylget node results.$i.router_state st
        if {$st != "UP" } {
            puts $CsHLT::__ERROR
            return
        } else {
            puts "$i : up"
        }
    }
    puts $CsHLT::__SUCCESS
    return 1
}

proc CsHLT::multicast_group_conf { mode {options ""}} {

    CsHLT::log "$mode multicast group is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_multicast_group_config  $opts ]

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode multicast group:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode multicast group is done!"
        keylget res handle mcGroupHandle
        return $mcGroupHandle
    }
}

proc CsHLT::multicast_source_conf { mode {options ""}} {

    CsHLT::log "$mode multicast source is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_multicast_source_config  $opts ]

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode multicast source:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode multicast source is done!"
        if { [string tolower $mode] == "create" } {
            keylget res handle mcSourceHandle
            return $mcSourceHandle
        }
    }
}

#*************************************************************************************************
#Purpose: Defines how Spirent HLTAPI will manage the buffers for packet capturing.
# args:
#	==>
#   ==>
#   [option]==>
#Author :James.Cao
#*************************************************************************************************
proc CsHLT::packet_ctrl {portHandle action {options ""}} {

    CsHLT::log "$action packet is in process..."
	set opts "-port_handle $portHandle -action $action $options"
	set res [eval sth::packet_control $opts]
	puts $res
}

proc CsHLT::get_keylist_value {listvalues key} {
    #global RETURNVALUE
    foreach k [keylkeys listvalues] {
        set value [keylget listvalues $k]
        if {$key == $k} {
            set CsHLT::RETURNVALUE $value
        } else {
            try_eval {
                set subkeys [keylkeys listvalues $k]
                set sublistvalues [keylget listvalues $k]
				get_keylist_value $sublistvalues $key
            } {  }
		}
    }
    return $CsHLT::RETURNVALUE
}

proc CsHLT::get_list_value {keylist key} {

    set value [keylget keylist $key]
    return $value
}

proc CsHLT::create_device {port {options ""}} {

    CsHLT::log "device configuration is in process..."
    set handle [CsHLT::get_port_handle $port]
    set opts "-mode create -port_handle $handle $options"
    puts $opts
    set res [eval sth::emulation_device_config $opts ]
    #puts "$res\n"
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to config device:  $res"
        return
    } else {
        set ::CsHLT::stats $res
        puts $CsHLT::__SUCCESS
        CsHLT::log "device config is done!"
        return $res
    }
}

proc CsHLT::emulation_dhcp_server_config {port mode version {options ""} } {

    CsHLT::log "emulation dhcp server is in process..."
    if {$mode == "create"} {
        set port_handle [CsHLT::get_port_handle $port]
        set opts "-mode $mode -port_handle $port_handle $options"
    } else {
        set opts "-mode $mode $options"
    }
    puts $opts
    puts "::sth::emulation_dhcp_server_config $opts"
    set res [ eval ::sth::emulation_dhcp_server_config  $opts]
    puts $res
    set ::CsHLT::stats $res
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        #lappend CsHLT::ERROR "failed to emulation dhcp server"
        puts $CsHLT::__ERROR
        return 1
    } else {
        CsHLT::log "emulation dhcp server is done!"
        puts $CsHLT::__SUCCESS
    }
    if {$mode == "create"} {
        if {$version ==	4} {
            return [keylget res handle.dhcp_handle]
        } elseif {$version == 6} {
            return [keylget res handle.dhcpv6_handle]
        }
    } else {
        return $CsHLT::__SUCCESS
    }
}

proc CsHLT::emulation_dhcp_server_control {handle action {options ""}} {

    CsHLT::log "emulation dhcp sever is in process..."
    #set port_handle [CsHLT::get_port_handle $port]
    set opts "-dhcp_handle $handle -action $action $options"
    puts $opts
    set res [ eval sth::emulation_dhcp_server_control  $opts]
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to emulation dhcp server"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation DHCP server is done!"
        return
    }
}

proc CsHLT::emulation_dhcp_server_stats {handle {options ""}} {

    CsHLT::log "emulation dhcp sever stats is in process..."
    #set port_handle [CsHLT::get_port_handle $port]
    set opts "-dhcp_handle $handle $options"
    puts $opts
    set res [ eval sth::emulation_dhcp_server_stats $opts]
    puts $res
    set ::CsHLT::stats $res
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to emulation dhcp server stats"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation DHCP server stats is done!"
        return
    }
}

proc CsHLT::emulation_dhcp_server_relay_agent_config {handle action {options ""}} {

    CsHLT::log "emulation dhcp sever relay agent config is in process..."
    if {$action == "create"} {
        #set port_handle [CsHLT::get_port_handle $port]
        set opts "-handle $handle -action $action $options"
    } else {
        set opts "-action $action $options"
    }
    puts $opts
    set res [ eval sth::emulation_dhcp_server_relay_agent_config $opts]
    puts $res
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "Failed to emulation dhcp server relay agent config."
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation DHCP server relay agent config is done!"
        return
    }
}

proc CsHLT::emulation_dhcp_config {port mode {options ""}} {

    CsHLT::log "emulation dhcp client is in process..."
    if {$mode == "create"} {
        set handle [CsHLT::get_port_handle $port]
        set opts "-mode $mode -port_handle $handle $options"
    } else {
        set opts "-mode $mode $options"
    }

    set res [eval sth::emulation_dhcp_config $opts]
    puts "sth::emulation_dhcp_config $opts"
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to emulation dhcp basic"
        puts $CsHLT::__ERROR
        return
    } elseif { $mode == "create"} {
        CsHLT::log "emulation dhcp client is done!"
        puts $CsHLT::__SUCCESS
        return [keylget res handles]
    } else {
        CsHLT::log "emulation dhcp client is done!"
        puts $CsHLT::__SUCCESS
    }
}

proc CsHLT::resetDhcpClient {handle {options ""}} {

    CsHLT::log "reset dhcp client is in process..."
    set opts "-mode reset -handle $handle $options"

    set res [eval sth::emulation_dhcp_config $opts]
    puts "sth::emulation_dhcp_config $opts"
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to emulation dhcp basic"
        puts $CsHLT::__ERROR
    } else {
        CsHLT::log "reset dhcp client is done!"
        puts $CsHLT::__SUCCESS
    }
}



proc CsHLT::emulation_dhcp_group_config {handle mode version {options ""} } {

    CsHLT::log "emulation dhcp client group is in process..."
    set opts "-handle $handle -mode $mode $options"
    puts $opts
    set res [eval sth::emulation_dhcp_group_config $opts]
    puts $res
    puts "sth::emulation_dhcp_group_config $opts"
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to emulation dhcp client group"
        puts $CsHLT::__ERROR
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation dhcp client group is done!"
    }
    if {$version == 4 && $mode == "create"} {
        return [keylget res handles]
    } elseif {$version == 6 && $mode == "create"} {
        return [keylget res dhcpv6_handle]
    }
}

proc CsHLT::resetDhcpClientGroup {handle {options ""}} {

    CsHLT::log "reset dhcp client group is in process..."
    set opts "-mode reset -handle $handle $options"

    set res [eval sth::emulation_dhcp_group_config $opts]
    puts "sth::emulation_dhcp_group_config $opts"
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        lappend CsHLT::ERROR "failed to emulation dhcp client group basic"
        puts $CsHLT::__ERROR
        return
    } else {
        CsHLT::log "reset dhcp client group is done!"
        puts $CsHLT::__SUCCESS
    }
}

proc CsHLT::emulation_dhcp_control {handle action {options ""}} {

    CsHLT::log "emulation dhcp client is in process..."
    #set port_handle [CsHLT::get_port_handle $port]
    #set opts "-port_handle $port_handle -action $action $options"
    set opts "-handle $handle -action $action $options"
    #puts "sth::emulation_dhcp_server_control $opts"
    puts $opts
    set res [eval sth::emulation_dhcp_control $opts]
    puts $res
    CsHLT::log "response info: ====> $res"

    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to emulation dhcp client"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation DHCP client is done!"
        return
    }
}

proc CsHLT::emulation_dhcp_stats {handle {options ""}} {

    CsHLT::log "emulation dhcp client stats is in process..."
    #set port_handle [CsHLT::get_port_handle $port]
    set opts "-handle $handle $options"
    #puts "sth::emulation_dhcp_control $opts"
    puts $opts
    set res [eval sth::emulation_dhcp_stats $opts]
    puts $res
    set ::CsHLT::stats $res
    CsHLT::log "response info: ====> $res"

    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to emulation dhcp client stats"
        #puts FAIL
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation DHCP client stats is done!"
        return
    }
}


proc CsHLT::emulation_bgp_config { mode {options ""}} {

    CsHLT::log "$mode bgp config is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_bgp_config  $opts ]

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode bgp config:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode bgp config is done!"
        if { [string tolower $mode] == "enable" } {
            keylget res handles rethandles
            foreach handle $rethandles {
                stc::config $handle -EnablePingResponse true
            }
            return "ret:$rethandles:"
        }
    }
}

proc CsHLT::emulation_bgp_route_config { mode {options ""}} {

    CsHLT::log "$mode bgp route config is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_bgp_route_config  $opts ]

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode bgp route config:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode bgp route config is done!"
        if { [string tolower $mode] == "add" } {
            keylget res handles rethandle
            return "ret:$rethandle:"
        }
    }
}

proc CsHLT::emulation_bgp_control { mode {options ""}} {

    CsHLT::log "$mode bgp control is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_bgp_control  $opts ]

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode bgp control:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode bgp control is done!"
    }
}

proc CsHLT::emulation_bgp_info { mode {options ""}} {

    CsHLT::log "$mode bgp control is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_bgp_info  $opts ]
    puts $res

    set ::CsHLT::stats $res
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to emulation bgp info"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation bgp info done!"
        return
    }
}

proc CsHLT::emulation_bgp_route_info { mode {options ""}} {

    CsHLT::log "$mode bgp route info is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_bgp_route_info  $opts ]
    puts $res

    set ::CsHLT::stats $res
    CsHLT::log "response info: ====> $res"
    keylget res status status
    if {!$status} {
        CsHLT::logErr "FAILED:  $res"
        puts $CsHLT::__ERROR
        lappend CsHLT::ERROR "failed to emulation bgp route info"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation bgp route info done!"
        return
    }
}

proc CsHLT::emulation_bgp_route_generator { mode {options ""}} {

    CsHLT::log "$mode bgp route generator is in process..."
    set opts "-mode $mode $options"
    set res [eval sth::emulation_bgp_route_generator  $opts ]

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode bgp route generator:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode bgp route generator is done!"
        if { [string tolower $mode] == "create" } {
            keylget res elem_handle rethandle
            return $rethandle
        }
    }
}

proc CsHLT::emulation_ospf_config { handle mode {options ""}} {
    CsHLT::log "$mode ospf config is in process..."
     if { [string tolower $mode] == "create" } {
         set opts "-port_handle $handle -mode $mode $options"
     } else {
         set opts "-handle $handle -mode $mode $options"
     }

    set res [eval sth::emulation_ospf_config  $opts ]
    puts $res
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode ospf config:  $res"
        return $res
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode ospf config is done!"
        if { [string tolower $mode] == "create" } {
            keylget res handles rethandles
            foreach handle $rethandles {
                stc::config $handle -EnablePingResponse true
            }
            return "return_handle: $rethandles"
        }
    }
}

proc CsHLT::emulation_ospf_topology_route_config { mode {options ""}} {
    CsHLT::log "$mode ospf_topology_route config is in process..."

    set opts "-mode $mode $options"
    set res [eval sth::emulation_ospf_topology_route_config  $opts ]
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode ospf_topology_route config:  $res"
        return $res
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode ospf_topology_route config is done!"
        if { [string tolower $mode] == "create" } {
            keylget res elem_handle rethandle
            return "return_handle: $rethandle"
        }
    }
}

proc CsHLT::emulation_ospf_lsa_config { mode {options ""}} {
    CsHLT::log "$mode ospf_lsa config is in process..."

    set opts "-mode $mode $options"
    set res [eval sth::emulation_ospf_lsa_config  $opts ]
    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode ospf_lsa config:  $res"
        return $res
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode ospf_lsa config is done!"
        if { [string tolower $mode] == "create" } {
            keylget res lsa_handle rethandle
            return "return_handle: $rethandle"
        }
    }
}

proc CsHLT::emulation_ospf_control { handle mode {options ""}} {
    CsHLT::log "$mode ospf control is in process..."
    set opts "-handle $handle -mode $mode $options"

    set res [eval sth::emulation_ospf_control  $opts ]
    puts $res

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to $mode ospf control:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "$mode ospf control is done!"
    }
}

proc CsHLT::emulation_ospf_info { handle mode version } {
    CsHLT::log "ospf $version info is in process..."
    set opts "-handle $handle -mode $mode"

    if { [string tolower $version] == "ospfv2" } {
        set res [eval sth::emulation_ospfv2_info  $opts ]
        puts $res
    } elseif { [string tolower $version] == "ospfv3" } {
        set res [eval sth::emulation_ospfv3_info  $opts ]
        puts $res
    } else {
        puts "wrong version $version"
        return
    }

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to ospf $version info:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "ospf $version info is done!"
        return $res
    }
}

proc CsHLT::emulation_ospf_router_info { handle } {
    CsHLT::log "ospf router info is in process..."
    set opts "-handle $handle"

    set res [eval sth::emulation_ospf_route_info  $opts ]
    puts $res
    set ::CsHLT::stats $res

    keylget res status status
    if { !$status} {
        puts $CsHLT::__ERROR
        CsHLT::logErr "FAILED to emulation ospf router info:  $res"
        return
    } else {
        puts $CsHLT::__SUCCESS
        CsHLT::log "emulation ospf router info is done!"
        return $res
    }
}

proc CsHLT::isis_config { port mode {inputs ""} } {

    if { $mode == "create" || $mode == "enable" } {
        set port_handle [CsHLT::get_port_handle $port]
        set str "-port_handle $port_handle -mode $mode $inputs"
    } else {
        set str "-mode $mode $inputs"
    }
    puts "sth::emulation_isis_config $str"
    set isis_res [ eval sth::emulation_isis_config $str ]

    keylget isis_res status isis_status

    if {!$isis_status} {
        puts $CsHLT::__ERROR
    } else {
        puts $CsHLT::__SUCCESS
        if { $mode == "create" || $mode == "enable" } {
            keylget isis_res handle handles
            return "{handles :$handles}"
        }
    }
}

proc CsHLT::isis_topology_route_config { isis_handle mode {inputs ""} } {

    if { $mode == "create"} {
        set str "-handle $isis_handle -mode $mode $inputs"
    } else {
        set str "-mode $mode $inputs"
    }

    set isis_res [eval sth::emulation_isis_topology_route_config $str ]

    keylget isis_res status isis_status

    if {!$isis_status} {
        puts $CsHLT::__ERROR
    } else {
        puts $CsHLT::__SUCCESS
        if { $mode == "create"} {
            keylget isis_res elem_handle handle
            return "{handle :$handle}"
        }
    }
}

proc CsHLT::isis_lsp_generator_config { isis_handle mode {inputs ""}} {

    if { $mode == "create"} {
        set str "-handle $isis_handle -mode $mode $inputs"
    } else {
        set str "-mode $mode $inputs"
    }
    set isis_res [ eval sth::emulation_isis_lsp_generator $str]
    keylget isis_res status isis_status
    if { !$isis_status } {
        puts $CsHLT::__ERROR
    } else {
        puts $CsHLT::__SUCCESS
        if { $mode == "create"} {
            keylget isis_res elem_handle handle
            return "{handle :$handle}"
        }
    }
}

proc CsHLT::isis_control {lsp_session_handle mode {inputs ""}} {

    set str "-handle $lsp_session_handle -mode $mode $inputs"

    set isis_res [ eval sth::emulation_isis_control $str]

    keylget isis_res status isis_status

    if { !$isis_status } {
        keylget isis_res log error_log

        CsHLT::logErr "FAILED:  $error_log"
        puts $CsHLT::__ERROR
    } else {
        puts $CsHLT::__SUCCESS
        }
}


proc CsHLT::isis_info { isis_router_handle mode } {

    set str "-handle $isis_router_handle -mode $mode "

    set isis_res [ eval sth::emulation_isis_info $str]

    set ::CsHLT::stats $isis_res

    keylget isis_res status isis_status

    if { !$isis_status } {
        puts $CsHLT::__ERROR
    } else {
        puts $CsHLT::__SUCCESS
        return $isis_res
    }
}
