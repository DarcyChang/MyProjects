__author__ = 'ccoughli'
import cafe
from cafe.core.logger import init_logging
# from stp.equipment.calix.e7 import E7ApiClass
# import stp.test_cases
import time
# import stp.api.e7.e7_lib

# Load config.ini file when not executing from command prompt
if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("config/config.ini")

print "what the heck"

def open_sessions(params, topology):


    # Open E7 Session(s) - opens sessions to all E7 DUTs in parameter file
    e7_nodename = params['e7']['e7']
    params['e7']['e7_profile'] = topology['nodes'][e7_nodename]['session_profile']['mgmt_vlan']['telnet']
    params['e7']['e7_session'] = E7ApiClass(params.session_mgr.create_session(e7_nodename, 'telnet',
                                                                              **params['e7']['e7_profile']),
                                            eq_type="e7")
    params['e7']['e7_session'].login()



    params.session_mgr.remove_session(params['e7']['e7_session'])