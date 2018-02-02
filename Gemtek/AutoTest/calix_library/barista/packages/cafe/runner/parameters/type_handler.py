from abc import ABCMeta, abstractmethod, abstractproperty

from cafe.core.logger import CLogger
from cafe.core.decorators import SingletonClass
from cafe.core.utils import expand_path
from cafe.runner.renderers.cliprinter import TextRenderer
from cafe.runner.renderers.demorenderer import DemoRenderer
from cafe.runner.utilities import in_order, randomized

__author__ = 'akhanov'


_module_logger = CLogger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warning
exception = _module_logger.exception
error = _module_logger.error


class _TypeHandler(object):
    """Class for transforming values of parameters based on their type in the schema
    """

    def __init__(self):
        self.__handlers = {}
        for subcls in TypeHandlerBase.__subclasses__():
            self.__handlers[subcls.TYPE] = subcls()

    def __call__(self, type_):
        return self.__handlers[type_]


class TypeHandlerBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def __call__(self, param_value, *args):
        return self.parse(param_value, *args)

    @abstractmethod
    def parse(self, *args, **kwargs):
        pass

    @abstractproperty
    def TYPE(self):
        pass


class StringTypeHandler(TypeHandlerBase):
    TYPE = 'str'

    def parse(self, param, *args):
        """Type processor for parameters with type 'str'

        Args:
            param: The raw value of the parameter

        Returns:
            str: The transformed parameter. Exits if an error has been encountered

        """
        try:
            assert(isinstance(param, (str, unicode)))
        except AssertionError:
            exception("'%s' is not a valid string" % param)
            raise

        if isinstance(param, unicode):
            #decoded = param.decode('utf-8')
            decoded = param
            return decoded.replace(u'\xa0', ' ')
        else:
            return param


class PathTypeHandler(TypeHandlerBase):
    TYPE = 'path'

    def parse(self, param, *args):
        """Type processor for parameters with type 'path'

        Args:
            param: The raw value of the parameter

        Returns:
            str: The transformed parameter. Exits if an error has been encountered

        """
        if param is None:
            ret = None
        else:
            try:
                assert (isinstance(param, (str, unicode)))
                param = StringTypeHandler().parse(param).strip()
            except AssertionError:
                exception("'%s' is not a valid string" % param)
                raise

            # ret = os.path.realpath(os.path.expandvars(os.path.expanduser(param)))
            ret = expand_path(param)

        return ret


class EnumTypeHandler(TypeHandlerBase):
    TYPE = 'enum'

    def parse(self, param, schema):
        """Type processor for parameters with type 'enum'
        Verifies that the value is in the enumeration.

        Args:
            param: The raw value of the parameter
            value_list (list): The list of acceptable values of the parameter

        Returns:
            The value of the parameter after confirming that it is a member of the enumeration. Exits if an error
            has been encountered.

        """
        value_list = schema['type']
        try:
            assert(param in value_list)
        except AssertionError:
            exception("'%s' is not one of the following: %s" % (param, ",".join(value_list)))
            raise

        return param


class ProcedureTypeHandler(TypeHandlerBase):
    TYPE = 'procedure'

    def parse(self, param, *args):
        """Type processor for parameters with type 'procedure'
        Finds a python function with the specified name and returns it.

        Args:
            param (str): The raw value of the parameter

        Returns:
            function: The transformed parameter. Exits if an error has been encountered

        """
        try:
            assert (isinstance(param, (str, unicode)))
        except AssertionError:
            exception("'%s' is not a valid string" % param)

        chain = param.split(".")
        scope = globals()

        try:
            for link in chain[0:-1]:
                assert(link in scope)
                scope = scope[link].__dict__

            assert(chain[-1] in scope)
        except AssertionError:
            exception("'%s': procedure not found" % param)
            raise

        ret = scope[chain[-1]]
        '''
        print(ret)
        print(ret.__name__)
        '''
        return ret


class IntTypeHandler(TypeHandlerBase):
    TYPE = 'int'

    def parse(self, param, *args):
        """Type processor for parameters with type 'int'
        Converts the specified parameter to an integer type

        Args:
            param: The raw value of the parameter

        Returns:
            int: The transformed parameter. Exits if an error has been encountered

        Raises:
            AssertionError if the parameter is not an integer

        """
        try:
            return int(param)
        except ValueError:
            exception("'%s' is not an integer value" % param)
            raise


class ListTypeHandler(TypeHandlerBase):
    TYPE = 'list'

    def parse(self, param, *args):
        """Type processor for parameters with type 'list'
        Converts a string with comma-separated members into a list

        Args:
            param: The raw value of the parameter

        Returns:
            list: The transformed parameter. Exits if an error has been encountered

        """
        ret = None
        if param is not None:
            try:
                assert(isinstance(param, (str, unicode)))
            except AssertionError:
                exception("'%s' is not a valid string" % param)
                raise

            if isinstance(param, str):
                ret = map(str.strip, param.split(","))
            else:
                ret = map(unicode.strip, param.split(","))

        return ret


class PathListTypeHandler(TypeHandlerBase):
    TYPE = 'path_list'

    def parse(self, param, *args):
        """Type processor for parameters with type 'path_list'
        Converts a string with comma-separated members into a list

        Args:
            param: The raw value of the parameter

        Returns:
            list: The transformed parameter. Exits if an error has been encountered

        """
        ret = None
        if param is not None:
            try:
                assert (isinstance(param, (str, unicode)))
            except AssertionError:
                exception("'%s' is not a valid string" % param)
                raise

            if type(param) is str:
                ret = map(str.strip, param.split(","))
            else:
                ret = map(unicode.strip, param.split(","))

            ret = map(PathTypeHandler().parse, ret)

        return ret


class DictTypeHandler(TypeHandlerBase):
    TYPE = 'dictionary'

    def parse(self, param, *args):
        """Type processor for parameters with type 'dictionary'
        Converts a string with comma-separated key=value pairs into a dict

        Args:
            param: The raw value of the parameter

        Returns:
            dict: The transformed parameter. Exits if an error has been encountered
        """
        if isinstance(param, dict):
            return param

        ret = {}

        if param is not None:
            try:
                assert (isinstance(param, (str, unicode)))
            except AssertionError:
                exception("'%s' is not a valid string" % param)
                raise

            param = param.strip()
            if not param:
                return ret

            pairs = param.split(",")

            for i in pairs:
                try:
                    key, value = map(lambda x: x.strip(), i.split('='))
                    ret[key] = value
                except:
                    exception("'%s' is not a valid pair, whole param is:'%s'" % (i, param))
                    raise

        return ret


class BoolTypeHandler(TypeHandlerBase):
    TYPE = 'bool'

    def parse(self, param, *args):
        """Type processor for parameters with type 'bool'
        Converts a string "true" or "false" to True or False

        Args:
            param: The raw value of the parameter

        Returns:
            bool: The transformed parameter. Exits if an error has been encountered

        """
        if isinstance(param, bool):
            return param

        try:
            assert (isinstance(param, (str, unicode)))
        except AssertionError:
            exception("'%s' is not a valid string" % param)
            raise

        try:
            assert (param.lower() in ('true', 'false'))
        except AssertionError:
            exception("'%s' is not a valid bool value" % param)
            raise

        if param.lower() == "true":
            ret = True
        else:
            ret = False

        return ret


class EnumListTypeHandler(TypeHandlerBase):
    TYPE = 'enum_list'

    def parse(self, param, schema):
        valid_values = schema['values']
        ret = []
        if param is not None:
            try:
                assert (isinstance(param, (str, unicode)))
            except AssertionError:
                exception("'%s' is not a valid string" % param)
                raise

            if isinstance(param, str):
                ret = map(str.strip, param.split(","))
            else:
                ret = map(unicode.strip, param.split(","))

            if not all(map(lambda x: x in valid_values, ret)):
                raise RuntimeError("Not all elements of '%s' in valid values '%s'" % (param, valid_values))

        return ret


TypeHandler = _TypeHandler()
"""_TypeHandler: The Singleton instance of the _TypeHandler object
"""

