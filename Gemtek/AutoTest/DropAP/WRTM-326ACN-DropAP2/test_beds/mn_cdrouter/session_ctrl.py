__author__ = 'bmelhus'

import cafe
from stp.equipment.cdrouter.cdrouter import CdrApiClass

def open_session_cdr(params, topology):
    params.session_mgr = session_mgr = cafe.get_session_manager()
    #-----------------------------------------------------------------------------------------------------
    # CD Router SSH
    # print(topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh'])
    params['cdr_profile'] = topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh']
    params['cdr_session'] = CdrApiClass(params.session_mgr.create_session("cdr", 'ssh', **params['cdr_profile']), eq_type="cdr")

    # print(params['cdr_profile'])
    params['cdr_session'].login()
    cdr = params['cdr_session']

def open_session_xc(params, topology):
    #-----------------------------------------------------------------------------------------------------
    # XCONN Telnet
    # print(topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh'])
    params['xc3_profile'] = topology['nodes']['xc3']['session_profile']['mgmt_vlan']['telnet']
    params['xc3_session'] = CdrApiClass(params.session_mgr.create_session("xc3", 'telnet', **params['xc3_profile']), eq_type="e72")

    # print(params['cdr_profile'])
    params['xc3_session'].login()
    xc3 = params['xc3_session']

def open_session_e7(params, topology):
    #-----------------------------------------------------------------------------------------------------
    # E7 DUT Telnet
    # print(topology['nodes']['cdrouter']['session_profile']['buddyweb']['ssh'])
    params['e7_profile'] = topology['nodes']['e72']['session_profile']['mgmt_vlan']['telnet']
    params['e7_session'] = CdrApiClass(params.session_mgr.create_session("e72", 'telnet', **params['e7_profile']), eq_type="e72")

    # print(params['cdr_profile'])
    params['e7_session'].login()
    e72 = params['e7_session']

def close_session_cdr(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params.session_mgr.remove_session(params['cdr_profile'])

def close_session_xc(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params.session_mgr.remove_session(params['xc3_profile'])

def close_session_e7(params):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    params.session_mgr.remove_session(params['e7_profile'])