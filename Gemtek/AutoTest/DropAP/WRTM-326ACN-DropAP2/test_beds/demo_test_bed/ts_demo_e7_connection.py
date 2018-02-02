__author__ = 'gliverm'

import cafe
from cafe.core.logger import init_logging
from stp.test_cases import tc_demo
from stp.equipment.calix.e7 import E7ApiClass


def open_sessions(params, topology):
    """
    Description:
        Open sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    # TODO: Convert over to using Cafe provided parameter usage
    # TODO: Need to extract returns from calls to verify success
    # Start session manager
    params.session_mgr = session_mgr = cafe.get_session_manager()

    # Open E7 Session(s) - opens sessions to all E7 DUTs in parameter file
    e7_nodename = params['e7']['e7']
    params['e7']['e7_profile'] = topology['nodes'][e7_nodename]['session_profile']['mgmt_vlan']['telnet']
    params['e7']['e7_session'] = E7ApiClass(params.session_mgr.create_session(e7_nodename, 'telnet',
                                                                              **params['e7']['e7_profile']),
                                            eq_type="e7")
    params['e7']['e7_session'].login()


def close_sessions(params, topology):
    """
    Description:
        Attempt to close sessions required for test suite.
    Args:
        params(dict) : Dictionary of test suite instance parameters
        topology(dict) : Dictionary of test suite equipment topology information
    Returns:
    """
    # Close E7 Session(s) - all that are listed as DUTs in parameter file
    # e7_node_list = params['e7'].keys()
    # for e7_node in e7_node_list:
    #     params.session_mgr.remove_session(params['e7'][e7_node])
    params.session_mgr.remove_session(params['e7']['e7_session'])


@cafe.test_suite()
def my_test_suite():

    # Initialize logging
    init_logging()
    # Initialize parameter dictionary - may be a better approach to loading parameters
    params = cafe.Param({})

    if not cafe.executing_in_runner():
        # Get runner config file
        cafe.load_config_file("config/config.ini")

        # Test suite parameter file
        params.load_ini("params/ts_demo_e7_connection.ini")

        # Test bed topology information imported here - may be a better approach to loading topology
        topology = cafe.get_topology()
        topology.load(params.topology.file)

    # Open Sessions Needed for Test Suite
    open_sessions(params, topology)

    # Test cases must be registered with Cafe prior to execution
    cafe.register_test_case(tc_demo.tc_123_e7_command_test, args=[params])

    # Execute all registered test cases
    cafe.run_test_cases()

    # Close Sessions Needed for Test Suite
    close_sessions(params, topology)

if not cafe.executing_in_runner():
    my_test_suite()

