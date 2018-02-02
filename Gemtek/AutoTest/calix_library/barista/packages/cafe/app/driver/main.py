from cafe.app.driver.webgui import WebGuiDriver

__author__ = 'kelvin'

from exa_ssh import EXASSHDriver
from ssh import SSHDriver
from telnet import TelnetDriver
from stc import STCDriver
from ixia import IXIADriver
from atlassian import JiraDriver
from atlassian import TMSDriver
from atlassian import BambooDriver
from ccplus import CCPlusDriver
from cdrouter import CDRouterDriver
from restapi import RestfulDriver
from netconf import NetConfDriver
from snmp import SnmpDriver

def get_driver(equipment, session_type, session=None, name=None, app=None):
    _e = equipment.upper()
    _s = session_type.upper()
    if _e == "EXA" and _s == "SSH":
        return EXASSHDriver(session=session, name=name)
    elif _e == "ANY" and _s == "NETCONF":
        return NetConfDriver(session=session, name=name)
    elif _e == "ANY" and _s == "SNMP":
        return SnmpDriver(session=session, name=name)
    elif _e == "SHELL" and _s == "SSH":
        return SSHDriver(session=session, name=name)
    elif _e == "SHELL" and _s == "TELNET":
        return TelnetDriver(session=session, name=name)
    elif _e == "STC" and _s == "TCL":
        return STCDriver(session=session, name=name, app=app)
    elif _e == "IXIA" and _s == "TCL":
        return IXIADriver(session=session, name=name, app=app)
    elif _e == 'WEBGUI' and _s == 'WEB':
        return WebGuiDriver(session=session, name=name, app=app)
    elif _e == 'JIRA' and _s == 'RESTFUL':
        return JiraDriver(session=session, name=name, app=app)
    elif _e == 'TMS' and _s == 'RESTFUL':
        return TMSDriver(session=session, name=name, app=app)
    elif _e == 'BAMBOO' and _s == 'RESTFUL':
        return BambooDriver(session=session, name=name, app=app)
    elif _e == 'CCPLUS' and _s == 'RESTFUL':
        return CCPlusDriver(session=session, name=name, app=app)
    elif _e == 'CDROUTER' and _s == 'RESTFUL':
        return CDRouterDriver(session=session, name=name, app=app)
    elif _s == 'RESTFUL':
        return RestfulDriver(session=session, name=name, app=app)
    else:
        raise RuntimeError("invalid equipment (%s) and/or session type (%s)" % (_e, _s))

if __name__ == "__main__":
    import time
    import cafe
    from cafe.runner.runner import main
    from cafe.runner.parameters.options import options
    options.apply()
    main()
    mgr = cafe.get_session_manager()
    shell = mgr.create_session("123", "shell")
    d = SSHDriver(shell)
    print d.cmd("pwd")
    print d.cmd("ps -ef", timeout=10)
    print d.cmd("ps -ef | more")

    for i in range(10):
        #time.sleep(5)
        print d.cmd("pwd")
        #time.sleep(5)
        print d.cmd("hostname")
