__author__ = 'akhanov'

from cafe import __main__
import os
import sys
import logging
import json
import traceback
import re
from ConfigParser import ConfigParser
import argparse
import time

from cafe.runner.utilities import change_pwd, get_project_paths
from cafe.core.utils import expand_path
from cafe.runner.parameters.type_handler import TypeHandler, PathTypeHandler
from cafe.core.config import get_config
from cafe.core.config import Param
from cafe.core.decorators import SingletonClass
from cafe.util.helper import get_cfs
from cafe.core.logger import init_logging
from cafe.core.logger import CLogger


class OptionsException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "OptionsException: %s" % self.message


@SingletonClass
class _Options(object):
    SCHEMA_FILE = os.path.dirname(__file__) + os.path.sep + "param_schema.json"
    TYPE_IDTFR = ':'
    INSTANCE_TYPE = "__INSTANCE_TYPE__"
    PARAM_TYPE = "__PARAM_TYPE__"
    ENUM_TYPE = "enum"

    __schema = {'params': {}, 'templates': {}}
    __config = {}
    __instances = {}

    def __init__(self, schema_file=SCHEMA_FILE):
        # Needs to be set to true - in case if config is not loaded before a test suite is executed in Cafe-Python
        self.__new_changes = True
        self.__log_queue = []
        self.reset_runner_state()
        self.__load_schema(schema_file)

    def reset_runner_state(self):
        config = get_config()
        config.runner_state = Param()
        config.runner_state.executing_in_runner = False
        config.runner_state.timestamp = Param()
        config.runner_state.timestamp.path_safe = time.strftime("%m_%d_%Y_%H_%M_%S")
        config.runner_state.user = Param()
        if not os.access(os.getcwd(), os.W_OK | os.X_OK):
            config.runner_state.user.available_log_dir = os.path.expanduser('~/cafe_logs')
        else:
            config.runner_state.user.available_log_dir = '.'

        path_ref_file, path_reference = get_project_paths(self, __main__.__file__, "cafepath")
        config.runner_state.path_reference_file = path_ref_file
        config.runner_state.path_reference = path_reference

    def push_log_queue(self, message, level="DEBUG"):
        self.__log_queue.insert(0, (level, message))

    def __process_log_queue(self):
        while len(self.__log_queue) > 0:
            level, message = self.__log_queue.pop()
            logger = get_config().runner_state.logger

            if level == "DEBUG":
                proc = logger.debug
            elif level == "ERROR":
                proc = logger.error
            elif level == "TRACE":
                proc = logger.trace
            elif level == "INFO":
                proc = logger.info
            elif level == "WARNING":
                proc = logger.warn

            proc(message)

    def __get_section_name(self, section):
        return section.split(self.TYPE_IDTFR)[0]

    def __get_section_type(self, section):
        try:
            return section.split(self.TYPE_IDTFR)[1]
        except IndexError:
            return ''

    def __load_schema(self, schema_file=SCHEMA_FILE):
        f = open(schema_file, "r")

        if f is None:
            raise OptionsException("missing schema file '%s'" % schema_file)

        try:
            j = json.load(f)
        except:
            raise OptionsException(traceback.format_exc() + "\n\nSchema is invalid!!!")

        for sec_name in j:
            section = j[sec_name]
            if sec_name.startswith(self.TYPE_IDTFR):
                name = self.__get_section_type(sec_name)
                self.__schema['templates'][name] = {}
                s = self.__schema['templates'][name]
            else:
                self.__schema['params'][sec_name] = {}
                s = self.__schema['params'][sec_name]

            s.update(section)

    def __get_schema_node(self, chain):
        try:
            return reduce(lambda x, y: x[y], chain, self.__schema)
        except KeyError:
            raise OptionsException("'%s' not found in schema" % ".".join(chain))

    def __get_schema_node_chain(self, path):
        if re.match("^[^.:]+(:[^.:]+)\.[^.:]+$", path):
            chain = path.split(".")
            return ['templates'] + [self.__get_section_type(chain[0])] + chain[1:]
        elif re.match("^[^.:]+(:[^.:]+)?\.[^.:]+$", path):
            chain = path.split(".")
            return ['params'] + [self.__get_section_name(chain[0])] + chain[1:]
        else:
            raise OptionsException("'%s' does not comply with parameter syntax 'section[:template].parameter'" % path)

    def __get_config_chain(self, path):
        if not re.match("^[^.:]+(:[^.:]+)?\.[^.:]+$", path):
            raise OptionsException("'%s' does not comply with parameter syntax 'section[:template].parameter'" % path)

        chain = path.split(".")
        return [self.__get_section_name(chain[0])] + chain[1:], self.__get_section_type(chain[0])

    def __calculator(self, val_name):
        try:
            fetch = str(self.get(val_name))
        except OptionsException:
            try:
                self.__set_default(val_name)
                fetch = str(self.get(val_name))
            except Exception as e:
                print("Unknown reference: %s" % val_name)
                raise

        return fetch

    def __substitute(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            refs = re.findall("\$\{.*?\}", value, re.UNICODE)

            for ref in refs:
                val_name = ref[2:-1]
                calculators = {
                    'TIMESTAMP_PATH': get_config().get_time_stamp_path,
                    'CAFE_AVAILABLE_LOG_DIR': get_config().get_available_log_dir,
                }

                v = calculators.get(val_name, self.__calculator)(val_name)
                value = value.replace(ref, self.__substitute(v))

        return value

    def __verify(self, path, value):
        chain = self.__get_schema_node_chain(path)
        schema = self.__get_schema_node(chain)
        param_type = schema['type']

        if isinstance(param_type, list):
            param_type = self.ENUM_TYPE

        return TypeHandler(param_type)(value, schema)

    def __set_param(self, path, value):
        chain, instance_type = self.__get_config_chain(path)
        value = self.__substitute(value)
        value = self.__verify(path, value)

        if instance_type:
            # this path is a instance, e.g.: a:TypeA.b.c.d
            self.__build_instance(chain[0], instance_type)

        s = self.__config

        for node in chain[:-1]:
            if node not in s:
                s[node] = {}

            s = s[node]

        s[chain[-1]] = value

    def __get_param(self, path):
        chain, _ = self.__get_config_chain(path)

        try:
            return reduce(lambda x, y: x[y], chain, self.__config)
        except KeyError:
            raise OptionsException("'%s' not found in config" % (path,))

    def __build_instance(self, instance_name, instance_type):
        if instance_name in self.__config:
            return

        self.__config[instance_name] = {}
        self.__config[instance_name]['__type__'] = instance_type
        self.__track_instance(instance_name, instance_type)
        self.__setup_instance(instance_name, instance_type, False)

    def __set_default(self, path):
        chain = self.__get_schema_node_chain(path)
        schema = self.__get_schema_node(chain)
        self.__set_param(path, schema['default'])

    def __setup_instance(self, section, section_type, overwrite=False):
        for param in self.__schema['templates'][section_type]:
            exists = True
            try:
                self.__get_param("%s.%s" % (section, param))
            except OptionsException:
                exists = False

            if overwrite or not exists:
                self.__set_param("%s:%s.%s" % (section, section_type, param),
                                 self.__schema['templates'][section_type][param]['default'])

    def __load_defaults(self, overwrite=False):
        for section in self.__schema['params']:
            for param in self.__schema['params'][section]:
                path = '%s.%s' % (section, param)
                exists = True
                try:
                    self.__get_param(path)
                except OptionsException:
                    exists = False

                if overwrite or not exists:
                    self.__set_default(path)

        # '_default_report' is default value of cafe_runner.reports, so I think it's better to initialize it here
        self.__config['_default_report'] = {}
        self.__config['_default_report']['__type__'] = "console_report"

        for section in self.__config:
            if '__type__' in self.__config[section]:
                tp = self.__config[section]['__type__']
                self.__setup_instance(section, tp, overwrite)

    def set(self, path, value):
        self.__set_param(path, value)

    def get(self, path):
        return self.__get_param(path)

    def dump(self):
        return self.__config

    def get_instances(self):
        return self.__instances

    def apply(self):
        if not self.__new_changes:
            return

        self.__load_defaults()

        config = get_config()

        for section in self.__config:
            config[section] = Param()

            for param in self.__config[section]:
                config[section][param] = self.__config[section][param]

        get_cfs().create_cafe_paths()

        init_logging(config.logger.level)
        root_logger = logging.getLogger()
        root_logger.setLevel(config.logger.level)

        if 'logger' not in config.runner_state:
            config.runner_state.logger = CLogger()

        logfile = PathTypeHandler().parse(os.path.join(config.cafe_runner.log_path, config.cafe_runner.runner_log_name))
        config.runner_state.logger.enable_file_logging(logfile)
        config.runner_state.logger.set_console(config.logger.console)
        config.runner_state.logger.set_level(config.logger.level)

        config.runner_state.callbacks = config.cafe_runner.renderer(config.runner_state.logger)

        self.__process_log_queue()

        # Load topology, if present
        if config.topology.file is not None:
            from cafe import get_topology
            from cafe.topology.topo import TopologyError

            try:
                get_topology().load(config.topology.file)
                config.runner_state.logger.debug("Loaded topology file '%s'" % config.topology.file)
            except TopologyError:
                config.runner_state.logger.error("Unable to load topology file '%s'" % config.topology.file)

        # Load parameter files, if present
        if config.parameters.files is not None:
            from cafe import get_test_param, param_merge
            from cafe.core.utils import ParamFileError

            for fname in config.parameters.files:
                p = Param()

                try:
                    p.load(fname)
                    config.runner_state.logger.debug("Loaded parameter file '%s'" % fname)
                except ParamFileError:
                    config.runner_state.logger.error("Unable to load parameter file '%s'" % fname)

                param_merge(get_test_param(), p)

        self.__new_changes = False
        config.bp()
        return config

    def load_config_file(self, filename):
        """Loads parameters from a configuration file

        Args:
            filename (str): The path of the configuration file to load

        """

        filename = PathTypeHandler().parse(filename)
        new_curdir = os.path.dirname(os.path.realpath(filename))

        #make sure the filename exists;
        #note: ConfigPraser.read() will not check it
        #re-open CAFE-987
        if not os.path.isfile(filename):
            sys.stderr.write("\nERROR: Configuration file not found! (%s)\n" % filename)
            #exit(1)

        ini = ConfigParser()

        try:
            ini.read(filename)
        except Exception as e:
            sys.stderr.write("\nERROR: Configuration load failed!\n%s\n" % e.message)
            exit(1)

        with change_pwd(new_curdir):
            for section in ini.sections():
                s_name = self.__get_section_name(section)
                t_name = self.__get_section_type(section)

                if t_name:
                    self.__build_instance(s_name, t_name)
                else:
                    self.__config[s_name] = {}

                for option in ini.options(section):
                    path = "%s.%s" % (section, option)
                    value = ini.get(section, option)

                    try:
                        self.__set_param(path, value)
                    except:
                        chain = self.__get_schema_node_chain(path)
                        param_type = self.__get_schema_node(chain)['type']
                        sys.stderr.write("\nERROR: Value '%s' is not a valid '%s' for parameter '%s'\n" %
                                         (value, param_type, path))
                        raise

        self.__new_changes = True

    def __track_instance(self, section, instance_type):
        if instance_type not in self.__instances:
            self.__instances[instance_type] = []

        self.__instances[instance_type].append(section)

    def load_command_line_args(self, in_args=None):
        args = argparse.ArgumentParser(description="Cafe Runner - executes test cases in bulk")
        '''
        args.add_argument('--runner.path', help='Path to file, test case, or test suite to execute. '
                                     'Format: path[:<test_suite>|:<test_case>]', default=None)
        '''
        args.add_argument('-c', '--config_file', help='Configuration file path')

        for section in self.__schema['params'].keys():
            for arg in self.__schema['params'][section].keys():
                arg_name = "--%s.%s" % (section, arg)
                descr = self.__schema['params'][section][arg]['description']
                default = self.__schema['params'][section][arg]['default']
                #args.add_argument(arg_name, help=descr, default=default)
                args.add_argument(arg_name, help=descr)

        if in_args:
            known, unknown = args.parse_known_args(in_args)
        else:
            known, unknown = args.parse_known_args()

        vals = vars(known)
        # Why we need deal with these unknown arguments?
        vals.update(dict(zip(
            map(lambda x: x.lstrip('-'), unknown[0::2]),
            unknown[1::2])
        ))

        self.load_args(vals)

    def load_args(self, args):
        config_file = args.pop('config_file', None)
        if config_file:
            if not os.path.exists(os.path.realpath(config_file)):
                print("Configuration file '%s' not found!" % config_file)
                exit()

            self.load_config_file(config_file)

        for path in args:
            value = args[path]
            if value is not None:
                try:
                    self.__set_param(path, value)
                except OptionsException:
                    sys.stderr.write("\nERROR: '%s' is not a valid Cafe parameter\n" % path)
                    raise
                except:
                    chain = self.__get_schema_node_chain(path)
                    param_type = self.__get_schema_node(chain)['type']
                    sys.stderr.write("\nERROR: Value '%s' is not a valid '%s' for parameter '%s'\n" %
                                     (value, param_type, path))
                    raise

        self.apply()

    def clear(self):
        self.__config = {}
        self.__instances = {}


options = _Options()


def load_config_file(fname):
    filename = expand_path(fname)
    options.load_config_file(filename)
    options.apply()
    get_config().runner_state.logger.debug("Loaded configuration file '%s'" % filename)
    # from cafe.core.db import create_test_db
    # logger = CLogger("cafe")
    # create_test_db(db_path=get_config().cafe_runner.db_path, logger=logger.get_child("testdb"))

