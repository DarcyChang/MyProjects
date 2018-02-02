__author__ = 'gliverm'

"""
    The intention of this file is to build a cache of examples of basic generic test case operation.
"""

# Must import cafe to be able to use the framework
import cafe

# Each test case MUST be prefaced with a Python decorator that will wrap the function with Cafe framework
# processing specific for a test case.
@cafe.test_case()
def tc_123_sample_test_case():
    """
    @test_id=123
    # Each test case MUST contain a test_id.  This value must be the same global ID value as in TMS.  The ID
    # should not include the EUT value which is different depending on which ONT is under test.

    # Other '@' values may be used in this section: @assignee, @tag, . . . etc.


    # Each test case must have a docstring to contain test case values and brief test case description.
    # Docstrings must follow google format to be correct extracted later by Sphinx via registration with Barista
    # Test case documentation may start out matching that of TMS but the expectation of the most up-to-date
    # version being in TMS (aka single location for updating documentation - limit admin work).
    """
    cafe.print_console("Hello! I am a test case!")
    # gliverm: Note this test case does not have a checkpoint and therefore no passing or failing steps

@cafe.test_case()
def tc_777_test_case_with_arg(name):
    """
    @test_id=777
    @assignee=some_random_person
    @tag=TEST
    Test case description goes here.
    """
    cafe.print_log("RANDOM ERROR?", level="ERROR")
    cafe.print_report("HELLO WORLD! THIS IS A REPORT")
    print("%s says hi!!!" % name)
    cafe.Checkpoint("Hello").verify_exact("Hello")
    cafe.Checkpoint("Hello").verify_exact("LOL")

@cafe.test_case()
def tc_45679RGGUI_test_case_1():
    """
    @test_id=45679RGGUI
    @assignee=gliverm
    @tag=TEST
    Test case description goes here.
    """
    cafe.Checkpoint("Hello").verify_exact("hi", "Custom Checkpoint", "CC Passed!", "CC Failed!")

@cafe.test_case()
def tc_888RGGUI_test_case_2():
    """
    @test_id=888RGGUI
    @assignee=gliverm
    @tag=TEST
    Test case description goes here.
    """
    cafe.Checkpoint("Hello").verify_exact("Hello", "Custom Checkpoint", "CC Passed!", "CC Failed!")

@cafe.test_case()
def tc_123_e7_command_test(params):
    """
    @test_id=123
    Test case description goes here.
    """
    # Obtain required parameters
    e7 = params['e7']['e7_session']

    # The checkpoint for a 'set' command is built into the api.  create_vlan and delete_vlan are 'set' commands.
    # The checkpoint for a 'get' command does not have a checkpoint built in because it is up to the
    # calling script to determine pass or fail from the information received
    e7.create_vlan(vlan='777', dhcp_snooping="enabled", mac_forced_forwarding="enabled",
                   ip_source_verify="enabled")

    e7.delete_vlan(vlan='777')


