from decorator import decorator

from cafe.core.decorators import SingletonClass

__author__ = 'kelvin'

import logging
import logging.handlers
import logging.config
import sys
"""
    This is the cafe logging module.
    Use this module instead of python 'logging' module directly.

    example usage:
    # initialize logging for all logger
    init_logging()
    log1 = CLogger("mylog")
    log1.info("print something")

    # enable a logger to save log into a file
    log1.enable_file_logging("log1.txt")
    log1.info("save into file")
    # disable a logger file logging
    log1.disable_file_logging()
"""

VERBOSE = 0
FORMAT = "[%(asctime)s] - %(name)-20s - %(levelname)s: %(message)s"

FORMAT2 = "[%(asctime)s] - %(name)s: %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
# to match with RF
TRACE = logging.DEBUG // 2
SESSION_LOG = 15

DEFAULT_LOGGER_CONFIG = dict(
    console=False,
    level="ERROR"
)


class _CFormatter(logging.Formatter):
    DEFAULT_FORMAT = "[%(asctime)s.%(msecs)d] - %(name)-20s - %(levelname)s: %(message)s"
    TESTSUITE_FORMAT = "[%(asctime)s.%(msecs)d] - %(name)-20s - %(levelname)s: .. %(message)s"
    TESTCASE_FORMAT = "[%(asctime)s.%(msecs)d] - %(name)-20s - %(levelname)s: .... %(message)s"
    TESTSTEP_FORMAT = "[%(asctime)s.%(msecs)d] - %(name)-20s - %(levelname)s: ...... %(message)s"
    DEFAULT_LEVEL = 0
    TESTSUITE_LEVEL = 1
    TESTCASE_LEVEL = 2
    TESTSTEP_LEVEL = 3

    def __init__(self, fmt=FORMAT, dfmt=DATEFMT):
        logging.Formatter.__init__(self, fmt, dfmt)
        self.level = 0

    def set_test_level(self, level):
        self.level = level

    def format(self, record):
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if self.level == self.DEFAULT_LEVEL:
            self._fmt = self.DEFAULT_FORMAT

        elif self.level == self.TESTSUITE_LEVEL:
            self._fmt = self.TESTSUITE_FORMAT

        elif self.level == self.TESTCASE_LEVEL:
            self._fmt = self.TESTCASE_FORMAT

        elif self.level == self.TESTSTEP_LEVEL:
            self._fmt = self.TESTSTEP_FORMAT


        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)
        # Restore the original format configured by the user
        self._fmt = format_orig
        return result

@SingletonClass
class CFormatter(_CFormatter): pass

def get_log_formatter():
    return CFormatter()

class NetworkLogging(object):
    _network_handler = None
    @classmethod
    def enable(cls, host="localhost", port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        """enable network logging to cafe log server

        Args
            host    - cafe log server host name
            port    - cafe log server port
        """
        #self.logger = _get_network_logger(host, port, self.name)
        try:
            if cls._network_handler is None:
                root_logger = logging.getLogger('')
                cls._network_handler = logging.handlers.SocketHandler(host, port)
                root_logger.addHandler(cls._network_handler)
                print "****network_handler is created"
            else:
                print "****network_handler already exist %s" % str(cls.network_handler)
        except Exception as e:
                sys.__stderr__.write("WARN: add network logger handler problem: %s\n" % str(e))
                cls._network_handler = None

def _add_trace():
    #add new debug level TRACE. A level below DEBUG
    #_TRACE = 8
    logging.addLevelName(TRACE, "TRACE")
    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kws)
    logging.Logger.trace = trace

def _add_session_log():

    logging.addLevelName(SESSION_LOG, "SESSION_LOG")
    def session_log(self, message, *args, **kws):
        if self.isEnabledFor(SESSION_LOG):
            self._log(SESSION_LOG, message, args, **kws)
    logging.Logger.session_log = session_log

def load_logging_config(d):
    logging.config.dictConfig(d)
    _add_trace()
    _add_session_log()

#def init_logging(format=FORMAT, datefmt=DATEFMT, level=logging.DEBUG):
def init_logging(level=logging.DEBUG):
    """
    initialize all logger to have console printing.
    :return:
    """

    #enable console log printing
    #_add_trace()
    #logging.basicConfig(format=format, datefmt=datefmt, level=level)

    # reserve robot handler
    robot_handlers = []
    for h in logging.root.handlers:
        from robot.output.pyloggingconf import RobotHandler
        if isinstance(h, RobotHandler):
            # only log message that level >= WARNING will log to robot output.xml file.
            h.setLevel(level)
            robot_handlers.append(h)

    # if root logger does not have robot handler, then add stdout to its handler.
    if not robot_handlers:
        fmt = get_log_formatter()
        handle = logging.StreamHandler(sys.stdout)
        handle.setFormatter(fmt)
        robot_handlers.append(handle)

    logging.root.handlers = robot_handlers
    logging.root.setLevel(level)
    #add new debug level TRACE. A level below DEBUG
    #_TRACE = 8
    # logging.addLevelName(TRACE, "TRACE")
    # def trace(self, message, *args, **kws):
    #     if self.isEnabledFor(TRACE):
    #         self._log(TRACE, message, args, **kws)
    # logging.Logger.trace = trace

    #_add_trace()
    #_add_session_log()

#to make sure TRACE & Session log level is created into python logging
_add_trace()
_add_session_log()


@decorator
def flush_log(func, self, *args):
    self.flush_log()
    return func(self, *args)


class CLogger(object):
    """cafe framework logger object"""
    names = []

    def __init__(self, name=None):
        """
        cafe framework logger object
        Args:
            name: name of logger
        """
        if name is None:
            self.name = "cafe"
        else:
            self.name = name
        self.logger = logging.getLogger(self.name)
        self.console = True
        self.print_level = 0
        self._log_record_queue = []
        # to avoid additional handler being added

        # if self.name in self.names:
        #     return

        # if not self.logger.handlers:
        #     self.logger.setLevel(logging.DEBUG)
        #     _stream = logging.StreamHandler()
        #     _formatter = logging.Formatter(fmt=FORMAT, datefmt=DATEFMT)
        #     _stream.setFormatter(_formatter)
        #     self.logger.addHandler(_stream)
        #     self.names.append(self.name)


    @property
    def console(self):
        return self.logger.propagate

    @console.setter
    def console(self, v):
        self.logger.propagate = bool(v)

    def get_child(self, name):
        _name = self.name
        n = _name + "." + name
        return CLogger(n)

    def set_console(self, v):
        self.console = bool(v)

    def enable_file_logging(self, log_file=None, level=logging.DEBUG, max_size=20 * 1024 * 1024, max_backup_cnt=50):
        """
        enable file handler for this logger.
        The file handler is logging.handler.RotatingFileHandler. Each file has size of <max_size>
        and <max_backup_cnt> number of backups

        Args:
            log_file:  log file name
            level: minimum logging level
            max_size: max size of each log file
            max_backup_cnt: max number of backup files

        Returns:
            None
        """
        #reset logger handlers
        # self.logger.handlers = []
        fmt = get_log_formatter()
        handler = logging.handlers.RotatingFileHandler(
              log_file, maxBytes=max_size, backupCount=max_backup_cnt)
        handler.setLevel(level)
        handler.setFormatter(fmt)
        self.logger.addHandler(handler)

    def disable_file_logging(self):
        """
        disable the file handler of this logger
        :return:
        """

        handlers = self.logger.handlers[:]
        for i in handlers:
            if isinstance(i, logging.FileHandler):
                i.flush()
                i.close()
                self.logger.removeHandler(i)
        #self.logger.handlers = []

    def remove_handlers(self):
        handlers = self.logger.handlers[:]
        for i in handlers:
            i.flush()
            i.close()
            self.logger.removeHandler(i)

    # def add_network_handler(self, host="localhost", port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
    #     """
    #     make the logger object send log over the network
    #     :param host: host/ip address of the log server
    #     :param port: log server port
    #     :param logger_name: name of the logger. eg. "myapp.area1"
    #     :return: None
    #     """
    #     #self.logger = _get_network_logger(host, port, self.name)
    #     _root_logger = logging.getLogger('')
    #     _socket_handler = logging.handlers.SocketHandler(host, port)
    #     _root_logger.addHandler(_socket_handler)

    def add_robot_logger_handler(self):
        # This function will effect all the logger with same name.
        # So, just call once for each unique logger name.
        from robot.output.pyloggingconf import RobotHandler
        handler = RobotHandler()
        _root_logger = logging.getLogger(self.name)
        _root_logger.addHandler(handler)

    def add_handler(self, handler):
        self.logger.addHandler(handler)

    @flush_log
    def debug(self, msg=""):
        self.logger.debug(msg)

    @flush_log
    def info(self, msg=""):
        self.logger.info(msg)

    @flush_log
    def warning(self, msg=""):
        self.logger.warning(msg)

    @flush_log
    def log(self, lvl=logging.DEBUG, msg=""):
        self.logger.log(lvl, msg)

    @flush_log
    def error(self, msg="", signal="",):
        """
        generate a error message
        """
        _msg = str(signal) + " - " + msg
        self.logger.error(_msg)
        #if signal:
        #    self.logger.error(signal)

    @flush_log
    def exception(self, msg="", signal=""):
        _msg = str(signal) + " - " + msg

        exc_info = sys.exc_info()
        record = self._make_record(self.logger.name, logging.ERROR, _msg, exc_info)
        formatted_msg = logging.Formatter().format(record)
        self.logger.error(formatted_msg)

    @flush_log
    def critical(self, msg=''):
        self.logger.critical(msg)

    @flush_log
    def trace(self, msg=""):
        self.logger.trace(msg)

    @flush_log
    def session_log(self, msg=""):
        self.logger.session_log(msg)

    def set_level(self, level):
        self.logger.setLevel(level)

    warn = warning

    def set_print_level(self, level):
        self.print_level = level

    def push_log(self, level, msg):
        self._log_record_queue.append(self._make_record(self.logger.name, level, msg))

    def pop_log(self):
        try:
            ret = self._log_record_queue.pop()
        except IndexError:
            ret = None

        return ret

    def flush_log(self):
        for rec in self._log_record_queue:
            self.logger.handle(rec)

        self._log_record_queue = []

    def _make_record(self, logger_name, level, message, exc_info=None):
        fn, lno = "(unknown file)", 0
        return self.logger.makeRecord(logger_name, level, fn, lno, message, [], exc_info)


def _get_network_logger(host="localhost", port=logging.handlers.DEFAULT_TCP_LOGGING_PORT, logger_name=""):
    """
    return a logger object
    :param host: host/ip address of the log server
    :param port: log server port
    :param logger_name: name of the logger. eg. "myapp.area1"
    :return: return  object
    """
    _root_logger = logging.getLogger('')
    _root_logger.setLevel(logging.DEBUG)
    _socket_handler = logging.handlers.SocketHandler(host, port)
    _root_logger.addHandler(_socket_handler)
    _logger = logging.getLogger(logger_name)

    return _logger
