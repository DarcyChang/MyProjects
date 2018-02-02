proc readOutput { pipe } {
    global readResults

    if {[eof $pipe]} {
        catch {close $pipe}
        set readResults(done) 1
        return
    }
    gets $pipe line
    puts "$line"
}
proc writecfgfile { vwpath cfgfilename filestring } {
    #Initialize return value
    set success 1
    #Open the output file for writing
    #Make the directory if it does not already exist
    file mkdir $vwpath/automation/conf/Calix
    set cfgfilename "$vwpath/automation/conf/Calix/$cfgfilename"

    #Overwrite the output file if it already exists
    if [catch {set outfile [open $cfgfilename w ]} result] {
        puts stderr "Cannot open file: $cfgfilename"
        set success 0
    }
    puts $outfile "$filestring"
    close $outfile
    puts "writecfgfile: $success"
    return $success
}
proc ixvwexecute { tclshpath vwpath cfgfilename } {
    set readResults(done) 0
    set readResults(failCnt) 0
    set readResults(failLines) ""
    set readResults(flowInfo) ""
    set readResults(frameInfo) ""
    set readResults(loss) ""
    set readResults(completed) ""
    set readResults(txRetrans) ""
    set readResults(latency) ""
    set readResults(abortCnt) 0
    set readResults(logLocation) ""

    set cfgfilename "$vwpath/automation/conf/Calix/$cfgfilename"
    set cmdPipe [open "| $tclshpath/bin/tclsh $vwpath/automation/bin/vw_auto.tcl --debug 3 -f $cfgfilename" r+]
    fileevent $cmdPipe readable [list readOutput $cmdPipe]
    vwait readResults(done)

    # Clean up IxVeriwave log information
    # Convert to Windoze file name
    if {$readResults(logLocation) != " "} {
        while { [string first "/" $readResults(logLocation)] != "-1"} {
            set replaceIndx [string first "/" $readResults(logLocation)]
            set readResults(logLocation) [string replace $readResults(logLocation) $replaceIndx $replaceIndx "\\"]
        }
        # No file clean up performed but should be done by user
        #file delete -force $readResults(logLocation)
        #puts "##### Cleanup deleted: $readResults(logLocation)"
    }
    puts "ixvwexecute: done"
}