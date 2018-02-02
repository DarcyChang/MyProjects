package require IxTclNetwork

puts "package IxNetwork has been loaded!"

namespace eval IxNC {
    set _ERROR ERROR
    set _SUCCESS SUCCESS

proc check {} {

   puts "IxNetwork lib is ready"
}

proc ixNetClearAllConfig {} {
    ixNet rollback
    ixNet execute newConfig
    after 2000
}

proc removePortList {portList} {
    set len [llength $portList]
    set i 0
    while { $i < $len } {
        set port [lindex $portList $i]
        ixNet remove $port
        ixNet commit
        incr i
    }
}

proc ixNetCleanUp {} {

    # if protocols are not stopped handle it from here
    catch {ixNet exec stopAllProtocols}

    # Clean all tabs
    catch {ixNet exec closeAllTabs}

    # Stop integrated if running
    catch {
         #stop test configuration if it is running
         catch {ixNet exec stopTestConfiguration}

         while { [regexp [ixNet getAtt [ixNet getRoot]/testConfiguration \
               -testRunning] true ] } {
               after 20000
          }
    };  # stopp !!!!

    # Remove port
    ixTclNet::UnassignPorts [ixNet getList [::ixNet getRoot] vport]
    removePortList [ixNet getList [::ixNet getRoot] vport]

    # clean
    catch {ixNet execute newConfig}
}

proc ixNetLoadconfigure_old {path confFile} {
    ixNetClearAllConfig
    catch {ixNet exec loadConfig [ixNet readFrom $path/$confFile.ixncfg]} tmpresult

    if {[string match *OK $tmpresult]} {
        #puts "Load configuration file is successful! $path/$confFile.ixncfg"
    } else {
        puts "Load configuration file is failed, $path/$confFile.ixncfg. said: $tmpresult"
        puts $IxNC::_ERROR
        return
    }
    #after 15000

    set v ""
    foreach v [ixNet getList [ixNet getRoot] vport] {
        puts "vport($v) - [ixNet getA $v -assignedTo]"
    }

    if { $v == "" } {
        puts "Load configuration file is failed, $path/$confFile.ixncfg. said: $tmpresult"
        puts $IxNC::_ERROR
        return
    }

    #wait for last vport to be up.
    for { set i 0 } { $i < 30 } { incr i 1 } {
        set res [ixNet getA $v -state]
        if { $res == "up" } { break }
        after 1000
    }
    catch {
        ixTclNet::ClearOwnershipForAllPorts
        ixTclNet::ConnectPorts
    }

    puts $IxNC::_SUCCESS
}

proc ixNetLoadconfigure {path confFile} {
    #ixNetClearAllConfig
    ixNetCleanUp

    # load config on windows
    #set remote_config "C:/$confFile.ixncfg"
    #set remote_config "C:/dhcp_dynamic_traffic.ixncfg"
    #catch {ixNet exec loadConfig [ixNet readFrom $remote_config -ixNetRelative]} tmpresult
    catch {ixNet exec loadConfig [ixNet readFrom $path/$confFile.ixncfg]} tmpresult

    if {[string match *OK $tmpresult]} {
        #puts "Load configuration file is successful! $path/$confFile.ixncfg"
    } else {
        puts "Load configuration file is failed, $remote_config. said: $tmpresult"
        puts $IxNC::_ERROR
        return
    }
    puts $IxNC::_SUCCESS

#    set v ""
#    foreach v [ixNet getList [ixNet getRoot] vport] {
#        puts "vport($v) - [ixNet getA $v -assignedTo]"
#
#        if { $v == "" } {
#            puts "Load configuration file is failed, $path/$confFile.ixncfg. said: $tmpresult"
#            puts $IxNC::_ERROR
#            return
#        }
#
#        #wait for last vport to be up.
#        for { set i 0 } { $i < 30 } { incr i 1 } {
#            set res [ixNet getA $v -state]
#            puts "status is $res"
#            if { $res == "up" } { break }
#            after 1000
#        }
#    }
#    catch {
#        ixTclNet::ClearOwnershipForAllPorts
#        ixTclNet::ConnectPorts
#    } tmpresult
#    puts $IxNC::_SUCCESS
}

proc ixNetCheckPortUp {} {
    set v ""
    foreach v [ixNet getList [ixNet getRoot] vport] {
        puts "vport($v) - [ixNet getA $v -assignedTo]"

        if { $v == "" } {
            puts $IxNC::_ERROR
            return
        }

        #wait for last vport to be up.
        for { set i 0 } { $i < 90 } { incr i 1 } {
            set res [ixNet getA $v -state]
            puts "status is $res"
            if { $res == "up" } { break }
            after 1000
        }
    }
    puts $IxNC::_SUCCESS
}

######################################################
proc ixNetStartAllProtocols_uncheckSession {} {
    if { [catch [ixNet exec startAllProtocols async] msg] } {
        puts "Start all protocols successful!"
        puts $IxNC::_SUCCESS

    } else {
        puts "Failed Start all protocols!"
        puts $IxNC::_ERROR
    }
    #after 12000
}

proc ixNetStartAllProtocols {} {
    if { [catch [ixNet exec startAllProtocols] msg] } {
        puts "Start all protocols successful!"
        puts $IxNC::_SUCCESS
    } else {
        ixNetCleanUp
        puts "Failed Start all protocols!"
        puts $IxNC::_ERROR
    }
    after 5000
}

proc ixNetStopAllProtocols {} {
    if {[catch [ixNet exec stopAllProtocols] msg]} {
    puts "Stop all protocols successful!"
    puts $IxNC::_SUCCESS
    } else {
        puts "failed stop all protocols!"
        puts $IxNC::_ERROR
    }
    after 12000
}

proc ixNetCheckProtocolSum {} {

    set viewName "Protocol Summary"
    set row [IxNC::ixNetGetOneRow $viewName 0]
    set name [lindex $row 0]
    set sessionInit [lindex $row 1]
    set sessionsucc [lindex $row 2]
    set sessionfail [lindex $row 3]
    if {$sessionInit == $sessionsucc && $sessionfail == 0} {
        puts Passed
        puts "successed session:$sessionsucc"
        puts $IxNC::_SUCCESS
    } else {
        puts $IxNC::_ERROR
    }
}
######################################################
proc ixNetCheckTrafficState {desiredTrafficState {timeout 90000}} {
        set attempts 0
        set waitInterval 2000

        while {true} {
                after $waitInterval
                update idletasks
                incr attempts
                if {[expr $attempts * $waitInterval] > $timeout} {
                        return "Timeout"
                }

                set currentState [ixNet getAttribute [ixNet getRoot]traffic -state]
                puts ">>>> $currentState"

                switch $currentState {
                        "error" {
                                puts "Error State"
                                return "Error State"
                        }
                        default {
                                if {$currentState == $desiredTrafficState} {
                                        puts $IxNC::_SUCCESS
                                        return $IxNC::_SUCCESS
                                }
                        }
                }
        }
}


proc ixNetApplyTraffic {} {
    ixNet setAttribute [ixNet getRoot]traffic -refreshLearnedInfoBeforeApply true
    ixNet commit
    # update idletasks
    # after 5000
	# update idletasks

    set attempts 0
    set waitInterval 2000

    while {true} {
        after $waitInterval
        update idletasks
        incr attempts
        if {[expr $attempts * $waitInterval] > 20000} {
            ixNetCleanUp
            puts "Failed to apply traffic, $msg"
            puts $IxNC::_ERROR
            return
        }

        set currentState [ixNet getAttribute [ixNet getRoot]traffic -state]
        puts ">>>> $currentState"

        switch $currentState {
            "error" {
                ixNetCleanUp
                puts "Failed to apply traffic, $msg"
                puts $IxNC::_ERROR
                return
            }
            default {
                if {$currentState == "unapplied" || $currentState == "stopped" } {
                    if {[catch [ixNet exec apply [ixNet getRoot]traffic] msg]} {
                        puts "Apply traffic successful!"
                        puts $IxNC::_SUCCESS
                        ixNetCheckTrafficState stopped 15000
                    } else {
                        ixNetCleanUp
                        puts "Failed to apply traffic, $msg"
                        puts $IxNC::_ERROR
                    }
                    return
                }
            }
        }
    }
}

proc ixNetStartTraffic {} {
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
    }
    if { $restartCaptureJudgement } {
        catch {
            ixNet exec startCapture
            after 2000
        }
    }

    if {[catch [ixNet exec start [ixNet getRoot]traffic] msg]} {
        puts "Start traffic successful!"
        puts $IxNC::_SUCCESS
    } else {
        puts "failed to start traffic!"
        puts $IxNC::_ERROR
    }
    ixNetCheckTrafficState started 60000
}

proc ixNetStopTraffic {} {
    if {[catch [ixNet exec stop [ixNet getRoot]traffic] msg]} {
        puts "Stop traffic successful!"
        puts $IxNC::_SUCCESS
    } else {
        puts "failed to Stop traffic!"
        puts $IxNC::_ERROR
    }
    after 5000
}
proc ixNetClearStatistic {} {
    if {[catch [ixNet exec clearStats] msg]} {
        puts "Clear Statistic successful!"
        puts $IxNC::_SUCCESS
    } else {
        puts "failed to Clear Statistic!"
        puts $IxNC::_ERROR
    }

    after 3000
}

######################################################
proc ixNetChecktrafficItemStatFull {row colum} {

    if { [catch {
                 set viewName "Traffic Item Statistics"
                 set rownum [IxNC::ixNetGetOneRow $viewName $row]
                 set value [lindex $rownum $colum]
                } msg] } {
                puts $value
                puts $IxNC::_ERROR
    } else {
        puts $value
        puts $IxNC::_SUCCESS
    }
}

proc ixNetGetOneRow {viewName rowIndex} {
    set viewPage [ixNetGetViewPage $viewName]
    set row_values [ixNet getAttribute $viewPage -rowValues]
    set one_rowList [lindex $row_values $rowIndex]
    set one_row [lindex $one_rowList 0]
    return $one_row
}

proc ixNetGetViewPage {viewName} {
    set viewList [ixNet getList [ixNet getRoot]/statistics view]
    set sg_view [lindex $viewList [ixNetGetViewIndex $viewName]]
    set viewPage [lindex [ixNet getList $sg_view page] 0]
    return $viewPage
}

proc ixNetGetViewIndex {viewName} {
    set root [ixNet getRoot]
    set viewList [ixNet getList $root/statistics view]
    set portView [lsearch $viewList ::ixNet::OBJ-/statistics/view:"$viewName"]
    return $portView
}



}
