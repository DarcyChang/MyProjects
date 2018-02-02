# This file contains confidential and / or privileged information belonging to Spirent Communications plc,
# its affiliates and / or subsidiaries.

###/*! \file pkgindex.tcl
###    \brief Pkgindex File
###    
###    This file contains the declaration of the HltApi package for Tcl. This file is required to facilitate the use of 
###    "package require SpirentHltApi" command.
###*/

# Tcl package index file, version 1.1
# This file is generated by the "pkg_mkIndex" command
# and sourced either when an application starts up or
# by a "package unknown" script.  It invokes the
# "package ifneeded" command to set up package-related
# information so that packages will be loaded automatically
# in response to "package require" commands.  When this
# script is sourced, the variable $dir must contain the
# full path name of this file's directory.

set dir "C:/Tcl/lib/stcHltapi/SourceCode"

package ifneeded SpirentHltApi 2.00 [list source [file join $dir hltapi_5.10_stc_2.10.tcl]]
package ifneeded SpirentHltApiWrapper 1.00 [list source [file join $dir/hltapiWrapper sth_wrapper.lib]]
package ifneeded CalixStcHltApi 1.00 [list source C:/Tcl/lib/stcHltapi/hltapi_stc.tcl]