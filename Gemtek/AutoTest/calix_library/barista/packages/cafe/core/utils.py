__author__ = 'kelvin'

from time import localtime, strftime
import os
import sys
import json
import pprint
import inspect
import dpath
from UserDict import UserDict
from cafe.core.decorators import SingletonClass
from logger import CLogger as Logger
from signals import CODE_EXCEPTION_RAISED, CODE_PARAM_FILE_ERROR
import contextlib
import collections
import yaml
import re
from logging import basicConfig
from distutils.util import strtobool

basicConfig()
logger = Logger(__name__)
logger.debug("importing module %s" % __name__)

debug = logger.debug
error = logger.error


class CafeCodeError(Exception):
    def __init__(self, message):
        super(CafeCodeError, self).__init__(message)
        frm = inspect.stack()[1]
        filename = frm[1]
        line = frm[2]
        #print(frm)
        mod = inspect.getmodule(frm[0])
        Logger(mod.__name__).exception("%s - %s,%s" % (message, filename, str(line)),
                                                     signal=CODE_EXCEPTION_RAISED)


class ParamLoadFromStringError(Exception):
    def __init__(self, message):
        super(ParamAttributeError, self).__init__(message)
        logger.exception(message, signal=CODE_EXCEPTION_RAISED)


class ParamAttributeError(Exception):
    def __init__(self, message):
        super(ParamAttributeError, self).__init__(message)
        # logger.exception(message, signal=CODE_EXCEPTION_RAISED)


class ParamFileError(Exception):
    def __init__(self, message):
        super(ParamFileError, self).__init__(message)
        #if sys.exc_info()[0]:
        #    debug(sys.exc_info()[:2])
        logger.exception(message, signal=CODE_EXCEPTION_RAISED)


class ParamMergeError(Exception):
    def __init__(self, message):
        super(ParamMergeError, self).__init__(message)
        #if sys.exc_info()[0]:
        #    debug(sys.exc_info()[:2])
        logger.exception(message, signal=CODE_EXCEPTION_RAISED)


class ParamCircularDefinitionError(Exception):
    def __init__(self, message):
        super(ParamCircularDefinitionError, self).__init__(message)
        logger.exception(message, signal=CODE_EXCEPTION_RAISED)


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def create_folder(filename):
    """
    create a folder for file <filename>
    :param filename: file name
    :return: True if successful; false otherwise
    """
    f = os.path.abspath(filename)
    d = os.path.dirname(f)
    ret = True
    try:
        os.mkdir(d)
    except OSError:
        pass
    except:
        ret = False
    return ret


def get_path(path, base_path=None):
    """
    return the abspath of <path>

    """
    #TODO: to have the base_path param implemented in config schema
    if base_path is None:
        # try:
        #     base_path = g_config["base_path"]
        # except:
        base_path = os.path.abspath("")

    logger.debug("get_path - base_path: %s" % base_path)

    if os.sep == path[0]:
        logger.debug("get_path - absolute pathname:% s" % path)
        return path
    else:
        logger.debug("get_path - relative pathname: %s" % os.path.join(base_path, path))
        return os.path.join(base_path, path)


def get_func(function_string):
    import importlib
    mod_name, func_name = function_string.rsplit('.',1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    return func


class Param(collections.MutableMapping):
    """
    Derived from dictionary. have the same behavior as dictionary and capability of objectify <key,value> pair

    Example:
        >>> x = Param()
        >>> x.a = 1
        >>> x.b = 2
        >>> x.c = 3
        >>> x['a'] == x.a
        >>> x['b'] == x.b
        >>> x['c'] == x.c
    """
    DICT_METHODS = ['values', 'items', 'keys', 'update']

    class ParamNode(object):
        REGEX = "\${(?P<name>[a-zA-Z][a-zA-Z0-9_-]*(\.[a-zA-Z][a-zA-Z0-9_-]*)*)}"

        def __init__(self, val):
            self.__value = val
            self._root = None

        def __repr__(self):
            if isinstance(self.__value, basestring) and re.search(self.REGEX, self.__value):
                try:
                    val = self.value
                except ParamAttributeError:
                    val = "<! Broken Reference !>"
                finally:
                    return "template(%s) -> %s" % (repr(self.__value), val)
            else:
                return repr(self.__value)

        def __get_value(self, path_chain):
            val = self.__value

            if isinstance(val, basestring):
                m = re.search(self.REGEX, val)

                while m is not None:
                    path = m.group('name')

                    if path in path_chain:
                        raise ParamCircularDefinitionError("Circular definition: %s" % " -> ".join(path_chain + [path]))

                    cur = self._root

                    for i in path.split('.'):
                        try:
                            #cur = dict.__getitem__(cur, i)
                            cur = cur._dict[i]
                        except (KeyError, TypeError):
                            raise ParamAttributeError("Could not find element '%s' in path '%s'" % (i, path))

                    if isinstance(cur, Param.ParamNode):
                        replacement = cur.__get_value(path_chain + [path])
                    else:
                        replacement = cur

                    val = re.sub(self.REGEX, replacement, val, 1)
                    m = re.search(self.REGEX, val)

            return val

        @property
        def value(self):
            return self.__get_value([])

        @value.setter
        def value(self, val):
            self.__value = val

        @property
        def raw_value(self):
            return self.__value

        # def __getattr__(self, item):
        #     return getattr(self.value, item)

    def __init__(self, d={}):
        super(Param, self).__setattr__('_dict', dict())
        super(Param, self).__setattr__('_root', self)
        self._update(d)

    DICT_METHODS = ['values', 'items', 'keys', 'update']

    def update(self, *args, **kwargs):
        return self._dict.update(*args, **kwargs)

    def __contains__(self, item):
        return self._dict.__contains__(item)

    def _update(self, d, ns=None, root_node=None):
        root = self if root_node is None else root_node
        if isinstance(d, Param):
            items = d._dict.items()
        else:
            items = d.items()

        for i, j in items:
            if isinstance(j, dict):
                _p = Param(j)
                _p._update(_p, ns, root)
                self.__setattr__(i, _p)

            elif isinstance(j, (list, tuple)):
                if ns:
                    _j = []
                    for k in j:
                        try:
                            _k = eval(k, ns)
                        except:
                            _k = k
                        _j.append(_k)

                else:
                    _j = j
                self.__setattr__(i, _j)
            elif isinstance(j, Param.ParamNode):
                if ns:
                    try:
                        _j.value = eval(str(_j.value), ns)
                    except Exception as e:
                        _j = j
                else:
                    _j = j

                _j._root = root_node
                self.__setattr__(i, _j)
            else:
                if ns:
                    try:
                        _j = eval(str(j), ns)
                    except:
                        _j = j
                else:
                    _j = j
                self.__setattr__(i, _j)

    def _set_root(self, root_node):
        super(Param, self).__setattr__('_root', root_node)

        for v in self._dict.values():
            if isinstance(v, Param):
                v._set_root(root_node)
            elif isinstance(v, Param.ParamNode):
                v._root = root_node

    def __hash__(self):
       # return hash(self.__repr__())
       return id(self)

    def __setattr__(self, name, value):
        name = str(name)
        if len(name) > 0 and "_" == name[0]:
            raise ParamAttributeError("key cannot be start with '-' or '_'")
        if len(name) > 0:
            self.__setitem__(name, value)

    def __setitem__(self, k, val):
        value = val.raw_value if isinstance(val, Param.ParamNode) else val
        key = k.replace(" ", "_").replace("-", "_")

        if isinstance(value, Param):
            self._dict[key] = value
            value._set_root(self._root)
        elif isinstance(value, dict):
            p = Param(value)
            p._set_root(self._root)
            self.__setitem__(key, p)
        else:
            new_node = Param.ParamNode(value)
            new_node._root = self._root
            self._dict[key] = new_node

    def __getattr__(self, name):
        if name in Param.DICT_METHODS:
            return getattr(self._dict, name)

        # if name in self or name is 'logger':
        if name in self or name is 'logger':
            return self.__getitem__(name)
        else:
            raise ParamAttributeError("Param __getattr__ No such attribute: " + name)

    def __getitem__(self, key):
        #value = dict.__getitem__(self, key)
        value = self._dict[key]

        if isinstance(value, Param.ParamNode):
            return value.value
        else:
            return value

    def __delattr__(self, name):
        if name in self:
            del self._dict[name]
        else:
            raise ParamAttributeError("Param __delattr__ No such attribute: " + name)

    def __delitem__(self, key):
        return self._dict.__delitem__(key)

    def __len__(self):
        return self._dict.__len__()

    def __iter__(self):
        return self._dict.__iter__()

    def bake_params(self):
        for k, v in self._dict.items():
            if isinstance(v, Param):
                v.bake_params()
            elif isinstance(v, Param.ParamNode):
                self[k] = v.value

    def _bp_helper(self, d, tab=0):
        indent = '    ' * tab
        segments = []

        for x, y in d.items():
            segment = "%s%s: " % (indent, x)

            if isinstance(y, collections.Mapping):
                if len(y) > 0:
                    segment += "{\n%s\n%s}" % (self._bp_helper(y, tab+1), indent)
                else:
                    segment += "{}"
            else:
                segment += "%s" % y

            segments.append(segment)

        ret = ',\n'.join(segments)

        return ret

    def bp(self):
        """
        beautiful print of param instance
        :return:
        """
        # pprint.pprint(self._dict, width=1)
        print '{\n' + self._bp_helper(self._dict, 1) + '\n}'


    def reset(self):
        for k in self.keys():
            self.__delattr__(k)

    def load_ini(self, ini_file):
        """ load ini file values into Param object

        Args:
            ini_file (str): ini file pathname

        Returns:
            None

        Example:
                >>> #test.ini file
                >>> [mysql]
                >>> user = 123123
                >>> pid_file = /tmp/result
                >>> ddd = ["abc",
                >>>      "efg"]
                >>> ggg = {"sdfsdf": 132131,
                >>>         "asdasd": "sdfdsf",
                >>>         "1": 2}

                >>> #python code
                >>> from cafe.core.utils import Param
                >>> d = Param()
                >>> d.load_ini("test.ini")
                >>> d.bp()
                >>>
                >>> #console
                >>> {'mysql': {'ddd': ['abc',
                >>>            'efg'],
                >>>    'ggg': {'1': 2,
                >>>            'asdasd': 'sdfdsf',
                >>>            'sdfsdf': 132131},
                >>>  'pid_file': '/tmp/result',
                >>>    'user': 123123}}
        """
        filename = os.path.expanduser(ini_file)
        filename = os.path.normpath(filename)
        if not os.path.isfile(filename):
            raise ParamFileError("no such file: " + filename)

        import ConfigParser
        import ast
        parser = ConfigParser.ConfigParser()
        parser.read(filename)

        def _eval(v):
            x = ""
            try:
                x = ast.literal_eval(v)
            except:
                x = v
            return x

        d = {s: {k: _eval(v) for k, v in parser.items(s)} for s in parser.sections()}
        self.update(d)
        self._update(self)

    def path_get(self, path, separator='/'):
        """
        path_get(path, separator='/')
        Given an object which contains only one possible match for the given path,
        return the value for the leaf matching the given path.

        If more than one leaf matches the glob, ValueError is raised. If the path is
        not found, KeyError is raised.
        """
        return dpath.get(self, path, separator)

    def path_set(self, path, value):
        """
        path_set(obj, path, value)
        Given a path, set all existing elements in the document
        to the given value. Returns the number of elements changed.
        """
        return dpath.set(self, path, value)

    def path_new(self, path, value):
        """
        path_new(obj, path, value)
        Set the element at the terminus of path to value, and create
        it if it does not exist (as opposed to 'set' that can only
        change existing keys).

        path will NOT be treated like a glob. If it has globbing
        characters in it, they will become part of the resulting
        keys
        """
        dpath.new(self, path, value)
        self._update(self)

    def load_yaml_string(self, s):
        """
        laod string of yaml data into param object
        """
        try:
            self.update(yaml.load(s))
            self._update(self)

        except:
            logger.debug(sys.exc_info())
            raise ParamLoadFromStringError("fail to load string into param object (%s)" % s )

    def load_yaml(self, yml_file):
        """
        load yaml file into param object
        """
        f = os.path.expanduser(yml_file)
        filename = os.path.normpath(f)
        if not os.path.isfile(filename):
           raise ParamFileError("no such file: " + filename)

        fp = open(filename, 'r')
        s = fp.read()

        try:
            self.update(yaml.load(s))
            self._update(self)

        except TypeError:
            logger.debug(sys.exc_info())
            raise ParamFileError("fail to load %s. possible reason invalid yaml format" % filename)

        finally:
            fp.close()

    def load(self, param_file):
        """
        load data file values into Param object
        supported file type are .json, .yaml, .ini
        """
        try:
            file_extension = os.path.splitext(param_file)[-1].lower()
        except:
            file_extension = ""

        #check extension
        if file_extension == ".json":
            self.load_json(param_file)
        elif file_extension == ".ini":
            self.load_ini(param_file)
        elif file_extension == ".yaml":
            self.load_yaml(param_file)
        else:
            raise ParamFileError("unsupported file extension %s. should be one of .json, .yaml, .ini" % file_extension)

    def load_json(self, json_file):
        """
        load json file values into Param object

        """
        filename = os.path.expanduser(json_file)
        filename = os.path.normpath(filename)
        if not os.path.isfile(filename):
            #logger.debug(sys.exc_info())
            #logger.error(msg=" - Runtime error - no such file: " + filename, signal=CODE_EXCEPTION_RAISED)
            #raise RuntimeWarning("No such file: " + filename)
            raise ParamFileError("no such file: " + filename)

        fp = open(filename, 'r')
        s = fp.read()

        try:
            self.update(json.loads(s))
            self._update(self)

        except:
            logger.debug(sys.exc_info())
            raise ParamFileError("fail to load %s. possible reason invalid json format" + filename)

        finally:
            fp.close()

    def dictionary(self):
        ret = dict()

        for k, v in self.items():
            if isinstance(v, Param):
                ret[k] = v.dictionary()
            elif isinstance(v, Param.ParamNode):
                ret[k] = v.value
            else:
                ret[k] = v

        return ret

    #alias
    set = __setattr__
    evaluate = _update
    bprint = bp

@SingletonClass
class TestParam(Param):
    pass

def get_test_param():
    return TestParam()

def param_merge(a, b):
    """merges b into a and return merged result

    Args:
        a (dict)
        b (dict)

    Returns:
        dict of merged result of a and b

    Example:
        >>> dict1 = {1:{"a":"A"},2:{"b":"B"}}
        >>> dict2 = {2:{"c":"C"},3:{"d":"D"}}
        >>> print dict(param_merge(dict1,dict2))
        >>> # {1: {'a': 'A'}, 2: {'c': 'C', 'b': 'B'}, 3: {'d': 'D'}}

    NOTE:
        tuples and arbitrary objects are not handled as it is totally ambiguous what should happen
    """

    key = None
    # ## debug output
    # sys.stderr.write("DEBUG: %s to %s\n" %(b,a))
    try:
        if a is None or isinstance(a, str) or isinstance(a, unicode) or isinstance(a, int) or isinstance(a, long) or isinstance(a, float):
            # border case for first run or if a is a primitive
            a = b
        elif isinstance(a, list):
            # lists can be only appended
            if isinstance(b, list):
                # merge lists
                a.extend(b)
            else:
                # append to list
                a.append(b)
        elif isinstance(a, collections.Mapping):
            # dicts must be merged
            if isinstance(b, collections.Mapping):
                for key in b:
                    if key in a:
                        a[key] = param_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                raise ParamMergeError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
        else:
            raise ParamMergeError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
    except TypeError, e:
        raise ParamMergeError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
    return a


@contextlib.contextmanager
def set_argv(arr):
    __tmp_argv = sys.argv
    sys.argv = arr

    yield

    sys.argv = __tmp_argv


@contextlib.contextmanager
def redirect_output(stdout=None, stderr=None):
    if stdout is not None:
        old_stdout = sys.__stdout__
        sys.__stdout__ = stdout

    if stderr is not None:
        old_stderr = sys.__stderr__
        sys.__stderr__ = stderr

    exception = None

    try:
        yield
    except Exception as e:
        exception = e

    if stdout is not None:
        sys.__stdout__ = old_stdout

    if stderr is not None:
        sys.__stderr__ = old_stderr

    if exception is not None:
        raise exception


if __name__ == "__main__":
    pass
    # print("ARGV before: ", sys.argv)
    #
    # with set_argv(['Hello', 'World!']):
    #     print("ARGV during: ", sys.argv)
    #
    # print("ARGV after: ", sys.argv)
#if __name__ == "__main__":
    # p = Param({"g": 1, "d": 34})
    # p.a = 1
    # p.b = 2
    # p.c = 3
    # print p.path_get('g')
    # set(p.items())
    # p.d = Param()
    # p.d.a = 5
    # p.d.b = 6
    # print p.path_get("d/b")
    # p.path_set("d/b", 7)
    # print p.path_get("d/b")
    # p.path_new("h/k", 9)
    # p.bp()

    # print(set(p.items()))
    # print (p)
    # print(p.__repr__())
    #
    # print("*" * 120)
    # p.load_ini("~/repo/calix/src/cafe/config/some.ini")
    #
    # p.bp()
    # p['cafe.logger'].bp()
    # print(p['cafe.runner']['topology_file'])
    #
    # dict1 = {1:{"a":"A"},2:{"b":"B"}}
    # dict2 = {2:{"c":"C"},3:{"d":"D"}}
    #
    # print dict(param_merge(dict1,dict2))


def expand_path(original_path):
    """
    Expands a cafe path into a full filesystem path. Properly replaces userhome ('~'), variables ('.', '..', etc.), and
    Cafe path references ('project://')

    Args:
        original_path (str): The cafe path to convert

    Returns:
        str: The full filesystem path that corresponds to original_path

    """
    # Need this here to get around cyclical import
    from cafe.core.config import get_config

    ret = original_path

    m = re.match("^(?P<path>\S+)://.*$", ret)

    if m is not None:
        if m.group('path') not in get_config().runner_state.path_reference:
            raise Exception("'%s' is not a valid path reference in '%s'. Please make sure the file 'cafepath' exists "
                            "and contains the definition of '%s'." % (m.group('path'), original_path, m.group('path')))

        ret = ret.replace(
            "%s://" % m.group('path'),
            get_config().runner_state.path_reference[m.group('path')] + os.path.sep
        )

    ret = os.path.realpath(os.path.expandvars(os.path.expanduser(ret)))
    return ret


@contextlib.contextmanager
def prevent_exit():
    temp = sys.exit
    sys.exit = lambda x: None

    yield

    sys.exit = temp


def static_vars(**kwargs):
    """Set static variables for function

    Args:
        **kwargs:

    Returns:

    """
    def _wrapper(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return _wrapper


def index_generator(start=0, step=1):
    count = start

    while True:
        yield count
        count += step


def str_to_bool(string):
    assert(isinstance(string, basestring))

    return bool(strtobool(string))
