import pprint

__author__ = 'kelvin'
"""This module contains contains class(es) and functions relate to Cafe (global) Config parameter objects
"""
from cafe.core.utils import Param
from cafe.core.decorators import SingletonClass
from cafe.core.logger import CLogger

_module_logger = CLogger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warning
error = _module_logger.error


@SingletonClass
class Config(Param):
    """Singleton class of Cafe Config
    In Cafe, we use this object to reference to Cafe config parameters.\n
    It is subclasss cafe.core.utils.Param.\n
    Refer to cafe.core.utils.Param for detail usage of this class.\n
    """

    def print_config(self):
        info('Cafe Config:\n%s' % pprint.pformat(self))

    def get_time_stamp_path(self, *args):
        return self.runner_state.timestamp.path_safe

    def get_available_log_dir(self, *args):
        return self.runner_state.user.available_log_dir


def get_config():
    """return the Singleton object of Config

    In Cafe, we use Config object to reference the Cafe (global) config parameters.

    Returns:
        Config object.

    Examples:
        >>>import cafe
        >>>config = cafe.get_config()
        >>>
        >>>config.bp(); ##print the config parameters contents

    Note:
        Refer to cafe.core.utils.Param for detail usage of Config class. Config is a subclasss of cafe.core.utils.Param.

    """
    return Config()



