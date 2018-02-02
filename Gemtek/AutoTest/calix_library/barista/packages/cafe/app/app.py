from cafe.util.stacktrace import register_remote_debug_handler

__author__ = 'kelvin'

import inspect
import os
import shutil
import sys
import traceback
from tempfile import NamedTemporaryFile
from distutils.version import LooseVersion

import cafe
from cafe.core.decorators import SingletonClass
from cafe.core.logger import CLogger
from cafe.core.utils import Param, get_test_param
from cafe.topology.topo_query import NodeQuery, LinkQuery, get_node_chain
from caferobot.listener.dynamic_listener import CafeDynamicListener
from cafe.core.exceptions.app.driver import DriverMethodNotImplementError


_module_logger = CLogger()
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


class SessionNode(object):

    def __init__(self, parent, name, config=None):
        self.parent = parent
        self.name = name
        self.d = None

        if config is None:
            self.d = self.parent.topo_query.connection[self.name]
        else:
            self.d = config

    def get(self):
        if "ip" in self.d:
            return self._get_driver_from_ip()
        elif "node" in self.d:
            return self._get_driver_from_node()
        elif 'type' in self.d and self.d['type'] == 'web':
            return self._get_web_driver()
        elif 'type' in self.d and self.d['type'] == 'restful':
            return self._get_restful_driver()
        else:
            raise RuntimeError("invalid name ref (%s) to get the device driver. please check you topo files" % self.name)

    def _get_driver_from_ip(self):
        from driver.main import get_driver
        d = self.d

        node = d["ip"]
        if "ip" in d:
            d["host"] = d["ip"]
        protocol = d["protocol"]

        print(d)
        print(protocol)

        _d = {}

        # TODO: should move the ip connectivity checking into the session_srv
        # #test the ip connectivity to host
        # if "ip" in d:
        #     if check_ping(d["host"]) is False:
        #         RuntimeError("host or ip address is not reachable (%s)" % d["host"])

        if protocol == "ssh":
            s = self.parent.session_mgr.create_session(self.name, session_type="ssh", **d)
            return get_driver("SHELL", "SSH", s, name=self.name, app=self.parent)

        elif protocol == 'telnet':
            s = self.parent.session_mgr.create_session(self.name, session_type="telnet", **d)
            return get_driver("SHELL", "TELNET", s, name=self.name, app=self.parent)

        elif protocol == "exa_ssh":
            s = self.parent.session_mgr.create_session(self.name, session_type="ssh", **d)
            driver = get_driver("EXA", "SSH", s, name=self.name, app=self.parent)
            if "ports" in d:
                driver.set_ports(d["ports"])
            return driver

        elif protocol == "netconf" or protocol == "netconf_ssh":
            s = self.parent.session_mgr.create_session(self.name, session_type="netconf", **d)
            driver = get_driver("ANY", "NETCONF", s, name=self.name, app=self.parent)
            if "ports" in d:
                driver.set_ports(d["ports"])
            return driver

        elif protocol == "snmp":
            s = self.parent.session_mgr.create_session(self.name, session_type="snmp", **d)
            driver = get_driver("ANY", "SNMP", s, name=self.name, app=self.parent)
            return driver

        elif protocol == "stc":
            d['tclsh'] = "/opt/active_tcl/bin/tclsh"
            d['timeout'] = 60

            #remove "host key" to avoid problem in creating the tcl session
            if "host" in d:
                d.pop("host")

            s = self.parent.session_mgr.create_session(self.name, session_type="tcl", **d)
            s.timeout = 120
            driver = get_driver("STC", "TCL", s,  name=self.name, app=self.parent)
            equipment_type = "stc"
            chassis_ip = d["ip"]

            ##
            # hack: update stc tcl session with stc tcl lib file in repo
            ##
            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            tcl_lib_pathname = os.path.join(path, "..", "equipment", "spirent", "stc", "hltapi_stc.tcl")
            with  NamedTemporaryFile(mode='w+t', prefix='hltapi_stc', suffix='.tcl', dir='/tmp') as f:
                dest_tcl_lib_pathname = f.name
                shutil.copy(tcl_lib_pathname, dest_tcl_lib_pathname)
                s.command("source %s" % dest_tcl_lib_pathname, timeout=60)

            driver._open(chassis_ip, equipment_type, ports=d["ports"])
            return driver

        elif protocol == "ix_network":
            #default tclsh for ixNetwork version <8.01
            d['tclsh'] = "/opt/active_tcl/bin/tclsh"
            d['timeout'] = 60
            ixnet_server = d["ixnet_server"]

            #check ixNetwork version and decide if d["tclsh"] need to be updated
            if os.path.exists(cafe.get_config().traffic_gen.ixia_version_file):
                p = Param()
                p.load_ini(cafe.get_config().traffic_gen.ixia_version_file)
                debug("ixia version %s" % str(p.ixia.version))

                if LooseVersion(str(p.ixia.version)) >= LooseVersion("8.01"):
                    d['tclsh'] = "/opt/ixia/bin/hltapitcl"

            else:
                debug("ixia version file (%s) not found." % cafe.get_config().traffic_gen.ixia_version_file)


            debug("ixia tclsh: %s" % d["tclsh"])
            debug("ixnet server: %s" % d["ixnet_server"])

            #remove "host key" to avoid problem in creating the tcl session
            if "host" in d:
                d.pop("host")

            s = self.parent.session_mgr.create_session(self.name, session_type="tcl", **d)
            s.timeout = 300
            driver = get_driver("IXIA", "TCL", s,  name=self.name, app=self.parent)
            equipment_type = "ix_network"
            chassis_ip = d["ip"]

            path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            tcl_lib_pathname1 = os.path.join(path, "..", "equipment", "ixia", "hltapi_ixia.tcl")
            tcl_lib_pathname2 = os.path.join(path, "..", "equipment", "ixia", "IxNetwork.tcl")

            f1 = NamedTemporaryFile(mode='w+t', prefix='hltapi_ixia', suffix='.tcl', dir='/tmp')
            f2 = NamedTemporaryFile(mode='w+t', prefix='IxNetwork', suffix='.tcl', dir='/tmp')

            dest_tcl_lib_pathname1 = f1.name
            dest_tcl_lib_pathname2 = f2.name

            shutil.copy(tcl_lib_pathname1, dest_tcl_lib_pathname1)
            shutil.copy(tcl_lib_pathname2, dest_tcl_lib_pathname2)

            s.command("set auto_path [linsert $auto_path 0 /opt/ixia/lib]")
            s.command("source %s" % dest_tcl_lib_pathname1, timeout=60)
            s.command("source %s" % dest_tcl_lib_pathname2, timeout=60)

            f1.close()
            f2.close()

            tcl_server = d['tcl_server'] if 'tcl_server' in d else ""
            driver.open(chassis_ip, equipment_type, ports=d["ports"],
                        ixNetworkTclServer=ixnet_server, tcl_server=tcl_server)
            return driver

        else:
            raise RuntimeError("unsupported protocol (%s)" % protocol)

    def _get_driver_from_node(self):
        from driver.main import get_driver
        d = self.d
        node = d["node"]
        session_profile = d["session_profile"]

        if node in self.parent.topo.nodes:
            session_param = self.parent.topo.nodes[node]["session_profile"][session_profile]
            equipment = self.parent.topo.nodes[node]["type"]
            session_type = self.parent.topo.nodes[node]["session_profile"][session_profile]["session_type"]
            # print "equipment: " + node + ":" + equipment
            # print session_type
            # print session_param
            s = self.parent.session_mgr.create_session(self.name, **session_param)
            # print s
            return get_driver(equipment, session_type, session=s,  name=self.name, app=self.parent)

    def _get_web_driver(self):
        d = self.d
        if 'firefox_profile' in d:
            if not os.path.isabs(d['firefox_profile']):
                topo_file = self.parent.config.topology.logical_query
                # get real path of profile file by topo_file
                d['firefox_profile'] = os.path.join(os.path.dirname(topo_file), d['firefox_profile'])

        s = self.parent.session_mgr.create_session(self.name, session_type="webgui", **d)
        from cafe.app import get_driver
        return get_driver("WEBGUI", "WEB", s, name=self.name, app=self.parent)

    def _get_restful_driver(self):
        d = self.d
        protocol = d["protocol"]
        s = self.parent.session_mgr.create_session(self.name, session_type="restful", **d)
        from cafe.app import get_driver
        return get_driver(protocol, "restful", s, name=self.name, app=self.parent)


@SingletonClass
class App(object):

    idb=None
    #TODO: discuss with team on the states of App()
    _session_built = is_initialized = False
    topo = None
    topo_nodes_links = None
    topo_query = None
    result = None
    drivers = None
    _session_built = False
    _cafe_param = Param()

    def __init__(self, dryrun=False):
        self.dryrun = dryrun
        self._initialize()
        self.rf_listener_queue = CafeDynamicListener()
        register_remote_debug_handler()

    @property
    def config(self):
        return cafe.get_config()

    @property
    def param(self):
        return cafe.get_test_param()

    @property
    def idb(self):
        return cafe.cafe.get_test_db()

    @property
    def logger(self):
        return _module_logger

    @property
    def session_mgr(self):
        if self._session_mgr:
            return self._session_mgr

        self._session_mgr = cafe.get_session_manager()
        return self._session_mgr

    @property
    def ptopo(self):
        return cafe.cafe.get_topology()

    def _initialize(self):
        if self.is_initialized:
            return
        try:

            self.topo = Param()
            self.topo_query = Param()
            self.topo_nodes_links = Param()
            self.result = Param()
            self.drivers = Param()
            self._session_mgr = None

            #initialize result data structure
            self.result["last"] = Param({"session": None, "prompt": None, "content": None})

            if not __debug__:
                print ("*** Config data structure ***")
                self.config.bp()
                print ("*** Param data structure ***")
                self.param.bp()

            if not self.dryrun:
                self.build_sessions()

            #this is removed due to duplication of function
            #self.is_initialized = True
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            sys.stderr.write("\n*** Error: failed to initialize cafe app. Exit, Error msg: %s!\n" % e)
            cafe.Checkpoint().fail("failed to initialize cafe app. Exit!")
            exit()

    def update_result(self, d):
        """
        puts result into App() data structure
        result data structure have as least the following keys

            - session (str): session of the result originated
            - prompt (str):  prompt, if any
            - content (str): content, if any

        Additional key is allowed for different session type
        """
        for k in ["session", "prompt", "content"]:
            if not k in d:
                raise RuntimeError("key '%s' is not in result" % k )

        self.result.last = Param(d)

    def verify_equal(self, exp=None, title=None):
        if title is None:
            title = "verify equal last content equal to %s" % str(exp)
        cafe.Checkpoint(self.result.last.content).verify_exact(exp=exp, title=title)

    def verify_regex(self, exp=None, title=None):
        if title is None:
            title = "verify equal last content regex to %s" % str(exp)
        cafe.Checkpoint(self.result.last.content).verify_regex(exp=exp, title=title)

    def _set_logical_topo(self):
        """
        create/set topology data structure
        """

        if "topology" not in self.config:
            return

        if self.config.topology.logical_query is None:
            self.topo_query['connection'] = {}
            self.logger.warning("topology information is not set in config ini file" +
                                " or from input args. no topology should be used in this test run")
        else:
            if self.config.topology.file:
                self.ptopo.load(self.config.topology.file)

            if not __debug__:
                print ("*** topology file ***")
                self.ptopo.bp()

            if self.config.topology.logical_query:
                self.topo_query.load(self.config.topology.logical_query)
            else:
                RuntimeError("config ini file is missing topology.logical_query file info")

            if not __debug__:
                print ("*** logical query file ***")
                self.topo_query.bp()

            #create the logical topo

            if self.config.topology.file and "node_query" in self.topo_query:
                for key in self.topo_query.node_query:
                    q = NodeQuery(key, **self.topo_query.node_query[key])

                    #to avoid duplication of node reference
                    if key in self.topo_nodes_links:
                        raise RuntimeError("node %s already exist in topo_nodes_links data structure")
                    self.topo_nodes_links[key] = q

            if self.config.topology.file and "link_query" in self.topo_query:
                for key in self.topo_query.link_query:
                    q = LinkQuery(key, **self.topo_query.link_query[key])

                    #to avoid duplication of link reference
                    if key in self.topo_nodes_links:
                        raise RuntimeError("link %s already exist in topo_nodes_links data structure")
                    self.topo_nodes_links[key] = q

            if self.config.topology.file and \
               'topo' in self.topo_query and \
               self.topo_query.topo.func == "node_chain":
                _nl = []
                for i in self.topo_query.topo.args:
                    _nl.append(self.topo_nodes_links[i])
                self.topo = get_node_chain(self.ptopo, *_nl)

                if not __debug__:
                    print ("*** logical topo data structure ***")
                    self.topo.bp()

    def copy_info(self, ref, **kwargs):
        """return copy a session connection config info referenced by "ref"
        In addition, we can overwrite session connection info by passing key value pairs
        The return copy can be used as input to build a local session.

        Args:
            ref:    session reference
            **kwargs:   key value pairs

        Return:
            cafe.core.utils.Param object

        Example:
            >>> #n1 is a exa_ssh session
            >>> #create a copy of n1 connection info and overwrite the ip address in the connection copy
            >>> conn = App().copy_info(n2, ip="10.243.19.214")
            >>> #build a new local session
            >>> App().build_local_session("n2", conn)

        Raise:
            RuntimeError: if ref cannot by found in exist App().drivers
        """
        ref = str(ref).lower()

        if ref not in App().drivers:
            RuntimeError("ref (%s) cannot be found in App().driver" % ref)

        driver = self.drivers[ref]

        #deep copy
        conn = Param(driver.connection)

        #assign new key value pairs
        for k, v in kwargs.items():
            conn[k] = v

        return conn

    def create_info(self, **kwargs):
        """create session connection config info object
        The return value can be used as input to build a local session.

        Args:
            **kwargs:   key value pairs

        Return:
            cafe.core.utils.Param object

        Example:
            >>> #create a connection info
            >>> conn = App().create_info(ip="10.243.19.213", type="exa", protocol=exa_ssh, user=root, password=root)
            >>> #build a new local session
            >>> App().build_local_session("n2", conn)

        """
        #TODO: create schema check for the input key/value pairs
        conn = Param(kwargs)
        return conn

    def _set_attrs(self):
        """
        set drivers as attributes of App() object
        """

        if "connection" not in self.topo_query:
            return

        for ref in self.topo_query.connection.keys():
            d = self.topo_query.connection[ref]
            self.drivers[ref] = SessionNode(self, ref).get()
            setattr(self, ref, self.drivers[ref])
            setattr(self.drivers[ref], "connection", d)

        for dd in self.drivers:
            self.logger.debug("driver created: %s" % dd)

    def _session_initiation(self):

        if self._session_built or "topology" not in self.config:
            return

        value = self.config.topology.session_initiation
        self.logger.debug("session initiation is %s" % value)

        if value == "REACHABLE":
            for d in self.drivers.keys():

                try:
                    if self.drivers[d].is_reachable():
                        self.logger.debug("Able to reach %s." % d)

                    else:
                        self.logger.error("Not able to reach %s." % d)
                        exit(-1)

                except (DriverMethodNotImplementError, AttributeError):
                    self.logger.debug("Does not perform reachable test on driver %s." % str(d))

        elif value == "CONNECT":
            for d in self.drivers.keys():
                self.logger.debug("try to connect %s." % d)

                try:
                    self.drivers[d].open_handle()

                    if self.drivers[d].is_connected():
                        self.logger.debug("Able to connect %s." % d)

                    else:
                        self.logger.error("Not able to connect %s." % d)
                        exit(-1)

                except (DriverMethodNotImplementError, AttributeError):
                    self.logger.debug("Does not perform connect before test start on driver %s." % str(d))
        else:
            #DO_NOTHING
            pass

    def node(self, ref):
        if ref in self.drivers:
            return self.drivers[ref]
        else:
            raise RuntimeError("session ref (%s) not found!" % ref)

    def params_global(self, ref):
        if "global" in self.param and self.param["global"]:
            return self.param["global"][ref]
        else:
            raise RuntimeError("parma global ref (%s) not found!" % ref)

    def build_sessions(self):
        """
        build all sessions baed on config.ini/topo.yaml files
        """
        if self._session_built:
            info('App() session has built')
            return

        #set topology data structure
        self._set_logical_topo()
        self._set_attrs()
        self._session_initiation()
        self.is_initialized = self._session_built = True

    def build_session(self, ref):
        if not ref in self.drivers:
            if ref in self.topo_query.connection.keys():
                d = self.topo_query.connection[ref]
                self.drivers[ref] = SessionNode(self, ref).get()
                #add "ref" as attribute of App()
                setattr(self, ref, self.drivers[ref])
                setattr(self.drivers[ref], "connection", d)

    def build_local_session(self, ref, config):
        """build a local session

        Args:
            ref:    session ref (unique id)
            config: session connection config info

        Raise:
            RuntimeError: if ref is already exist in App().drivers
        """
        if ref in self.drivers:
            raise RuntimeError("driver reference already exists (%s)" % ref)
        self.drivers[ref] = SessionNode(self, ref, config).get()
        setattr(self, ref, self.drivers[ref])
        setattr(self.drivers[ref], "connection", config)

    def destroy_local_session(self, ref):
        """build a local session
        Args:
            ref:    session ref (unique id)
        """
        if ref in self.topo_query.connection.keys():
            warn("ref (%s) is a global session. cannot be destroyed by this method" % ref)
            return
        self.destroy_session(ref)

    def destroy_session(self, ref):
        info('App() destroy session: %s' % ref)
        if ref in self.drivers:
            self.session_mgr.remove_session(ref)
            delattr(self, ref)
            driver = self.drivers.pop(ref)
            from caferobot.caseutil import InstanceRefSet
            InstanceRefSet.destroy_device(driver)
        else:
            warn("App() session(%s) not found" % ref)

    def destroy_sessions(self):
        if not self._session_built:
            info('App() sessions have destroyed')
            return

        # destory all sessions including global & local
        refs = self.drivers.keys()[:]
        for ref in refs:
            self.destroy_session(ref)

        self.topo_query.clear()
        self.ptopo.reset()
        self.topo_nodes_links.clear()
        self.drivers.clear()
        self.is_initialized = self._session_built = False

    def init_cafe_param(self):
        self._cafe_param.clear()
        self._cafe_param['APP'] = self
        # Add Sections/Parameters to _cafe_param
        for section, vars_ in get_test_param().iteritems():
            try:
                self._cafe_param[section]
            except KeyError:
                self._cafe_param[section] = Param()

            if not vars_:
                continue

            for k, v in vars_.iteritems():
                self._cafe_param[section][k] = v

        try:
            self._cafe_param['global']
        except KeyError:
            self._cafe_param['global'] = Param()

        # Copy variables from 'global' section to root of _ret - because they're global
        for global_param in self._cafe_param['global']:
            if global_param in self._cafe_param:
                raise Exception("%s is already a section. Cannot override a section with a parameter." % global_param)

            self._cafe_param[global_param] = self._cafe_param['global'][global_param]

        for k in App().drivers:
            if k in self._cafe_param:
                raise Exception("%s is a RF variable. Cannot override RF variable with driver object." % k)

            try:
                self._cafe_param[k] = getattr(App(), k)
            except AttributeError:
                raise Exception("%s is not found in App() drivers list." % k)

    def get_cafe_param(self):
        return self._cafe_param

    # reset result data structure
    def reset_result(self):
        self.result["last"].update({"session": None, "prompt": None, "content": None})

if __name__ == "__main__":
    pass
