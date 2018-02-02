import re
from collections import OrderedDict
from itertools import takewhile

from cafe.core.logger import CLogger as Logger
from cafe.core.signals import RESPONSE_MAP_ERROR, RESPONSE_MAP_MATCH_NOT_FOUND_ERROR
from cafe.core.utils import Param

__author__ = 'kelvin'

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning


class ResponseMapError(Exception):
    def __init__(self, msg=""):
        super(ResponseMapError, self).__init__(msg)
        _module_logger.exception(msg, signal=RESPONSE_MAP_ERROR)


class ResponseMapMatchNotFoundError(Exception):
    def __init__(self, msg=""):
        super(ResponseMapMatchNotFoundError, self).__init__(msg)
        _module_logger.exception(msg, signal=RESPONSE_MAP_MATCH_NOT_FOUND_ERROR)


# class ResponseMapMatchGroupNotExistError(Exception):
#     def __init__(self, msg=""):
#         super(ResponseMapMatchGroupNotExistError, self).__init__(msg)
#         _module_logger.exception(msg, signal=RESPONSE_MAP_MATCH_GROUP_NOT_EXIST_ERROR)

class PatternBuilder(Param):
    """Helper to create ResponseMap().patter_match pattern
    """
    def add(self, key, regex, group=None, flags=None, raise_error=None):
        """add a new/modify existing key of the pattern
        """
        v = {}
        if key in self:
            v = self[key]

        v["regex"] = str(regex)

        if group:
            v["group"] = int(group)

        if flags:
            v["flags"] = int(flags)

        if raise_error:
            v["raise_error"] = bool(raise_error)

        self[key] = v

class ResponseMap(object):
    """Response Map contains set of methods which help user to
    parse unformatted text into data structure for easier data manipulation
    and value comparison
    """
    def __init__(self, resp):
        self.response = resp

    def _regex1(self, s, exp):
        m = re.search(exp, str(s))
        if m:
            return (m.group(1), m.group(2))
        else:
            return (None, None)

    def _check_start_line(self, v):
        try:
            return int(v)
        except ValueError:
            raise ResponseMapError("input argument 'start_line' value (%s) must be an integer" % str(v))

    def _check_end_line(self, v):
        try:
            return int(v)
        except ValueError:
            raise ResponseMapError("input argument 'end_line' value (%s) must be an integer" % str(v))

    @staticmethod
    def create_pattern():
        return PatternBuilder()

    def parse_table(self, start_line=0, sep="\s\s+", skip_pattern="\-\-+", auto_title=True, title=[]):
        """parse table response into list of Param objects

        Args:
            start_line (int): line to start parsing. line < start_line will not be used
            sep (str): regexp of separator
            skip_pattern (str): regexp of skip pattern. line which match with this pattern will not be used.
            auto_title (bool): if True, the line # of <start_line> will be used as title line; if False, will use the <title>
            title (list): titles of all column.

        Returns:
            list of Param objects

        """

        # ensure the input argument types are correct
        _start_line = self._check_start_line(start_line)

        if not isinstance(auto_title, bool):
            raise ResponseMapError("input argument 'auto_title' must be a boolean")

        if not isinstance(title, list):
            raise ResponseMapError("input argument 'title' must be a list")

        lines = []
        ret = []

        for line in self.response.splitlines():
            if line.strip() == "":
                pass
            else:
                lines.append(line.strip())

        lines = lines[_start_line:]

        _lines = []
        for line in lines:
            if re.search(skip_pattern, line):
                pass
            else:
                _lines.append(line)

        if auto_title:
            _t = _lines.pop(0)
            _t = re.sub(sep, ",", _t)
            _title = _t.split(",")

        else:
            _title = title

        for line in _lines:
            _v = re.sub(sep, ",", line)
            _values = _v.split(",")
            d = Param(dict(zip(_title, _values)))
            ret.append(d)

        return ret

    def parse_key_value_pairs(self, start_line=0, end_line=None, seperator=r"\s+"):
        """parse response as key value pairs

        Args:
            start_line (int): where to start parsing. default is 0
            end_line: where to stop parsing. default is None. which the last line.
            seperator (regex): character(s) of splitting the key & value

        Returns:
            Param: dictionary of key value pairs

        Example:
            >>> s = '''
            >>> a 1
            >>> b 2
            >>> c 34 23
            >>> '''
            >>> r = ResponseMap(s)
            >>> m = r.parse_key_value_pairs()
            >>> print m
        """
        d = {}

        _start_line = self._check_start_line(start_line)
        if end_line is None:
            _end = len(self.response.splitlines())
        else:
            _end = self._check_end_line(end_line)

        lines = self.response.splitlines()[_start_line:_end]

        for l in lines:
            i = l.strip()
            k, v = self._regex1(i, r"(\S+)%s(.+)" % seperator)
            if k:
                d[k] = v
        return Param(d)

    def pattern_match(self, pattern={}, findall=False):
        """Response map api: pattern match

        This api is inspired by iTest response map pattern match.

        This api use python re.search internally, For detail information of python re.search function, please reference to
        python document. https://docs.python.org/2/library/re.html

        The pattern match is defined by the "pattern" input argument. It is a dictionary of dictionary

        Example:
            >>> pattern = {
            >>>     "key1": {
            >>>         "regex": <string value, python regular expression (must)>,
            >>>         "group", <int value, index of re match group (optional, default is 0)>,
            >>>         "flags", <int value, re flags (optional, default is re.MULTILINE|re.IGNORECASE)>,
            >>>         "raise_error": <bool value. raise error is not is not found (option, default is False)},
            >>>     "key2": {...},
            >>>     "key3": {...}}

        The return value is a Cafe Param object. where the Param keys are the same ones define by the pattern.
        if a key's value is None, this means there is not match is found.

        Example:
            >>> ret = {
            >>>     "key1": <some value>,
            >>>     "key2": <None. this is no match>,
            >>>     "key3": <None. this is no match>}

        Args:
            pattern (dict): pattern is a python dictionary data type. It is a dictionary of dictionary.
            findall (bool): if True, it return a dictionary of list of matched values.if False (default),
                it returns a dictionary of 1st-matched values. Set it to True if you expected to find all the matches pattern.

        Returns:
            Cafe Param object

        Raises:
            ResponseMapMatchNotFoundError: if a match is not found and raise_error is True.

        Examples:
                >>> #example of findall is False
                >>> s = '''
                >>> name: sssss
                >>> domain: test 1
                >>> packet loss: 4444
                >>> packet loss: 5555
                >>> '''
                >>> r = ResponseMap(s)
                >>> pd = {"name": {"regex": r"name: (.+)"},
                >>>      "domain": {"regex": r"domain: (.+)"},
                >>>      "packet_loss": {"regex": "packet loss: (\d+)", "group": 1}}
                >>>
                >>> d = r.pattern_match(pd)
                >>> d.bp()
                >>> #print out
                >>> {'domain': 'domain: test 1',
                >>> 'name': 'name: sssss',
                >>> 'packet_loss': '4444'}

        Examples:
                >>> #example of findall is True
                >>> s = '''
                >>> name: sssss
                >>> domain: test 1
                >>> packet loss: 4444
                >>> packet loss: 5555
                >>> '''
                >>> r = ResponseMap(s)
                >>> pd = {"name": {"regex": r"name: (.+)"},
                >>>      "domain": {"regex": r"domain: (.+)"},
                >>>      "packet_loss": {"regex": "packet loss: (\d+)", "group": 1}}
                >>>
                >>> d = r.pattern_match(pd, findall=True)
                >>> d.bp()
                >>> #print out
                >>> {'domain': ['domain: test 1'],
                >>> 'name': ['name: sssss'],
                >>> 'packet_loss': ['4444', '5555']}
        """

        d = {}
        # iniitalize
        for k, v in pattern.items():
            d[k] = None
            # print(v)
            if not "regex" in v:
                raise ResponseMapError("regex not found for key(%s)" % k)

            if not "group" in v:
                pattern[k]["group"] = 0

            if not "flags" in v:
                pattern[k]["flags"] = re.MULTILINE | re.IGNORECASE

            if "raise_error" in v:
                pass
            else:
                pattern[k]["raise_error"] = False

        # find match
        if not findall:
            for k, v in pattern.items():
                m = re.search(v["regex"], self.response, flags=v["flags"])
                if m:
                    try:
                        d[k] = m.group(v["group"])
                    except IndexError:
                        # raise ResponseMapMatchGroupNotExistError("look for group index (%d), "
                        #                                         "but max number of groups is (%d)" % (v["group"],
                        #                                                                    len(m.groups())))
                        warn("look for group index (%d), but max number of groups is (%d)" %
                             (v["group"], len(m.groups())))
        else:
            for k, v in pattern.items():
                m = re.finditer(v["regex"], self.response, flags=v["flags"])
                d[k] = []
                for _m in m:
                    try:
                        d[k].append(_m.group(v["group"]))
                    except IndexError:
                        warn("look for group index (%d), but max number of groups is (%d)" %
                             (v["group"], len(_m.groups())))

        # raise error if requested
        for k, v in pattern.items():
            if d[k] is None and v["raise_error"] is True:
                raise ResponseMapMatchNotFoundError("match for %s is not found in response" % k)

        return Param(d)

    def table_match_by_delimiter(self, start_line=None, end_line=None, delimiter=r"\s\s+", columns=None):
        """response map API: to parse table text response into list of dictionary

        Args:
            start_line (int): the beginning number in response to beparsed.
                default is None. which means starting from beginning
            end_line (int): the last line number in reponse to be parsed.
                default is None. which means parse until last line of the response.
            delimiter (str): regexp string to split each line in the response into columns of values
            columns (list of dict): If None, default column names will be assign. The default column names are 1, 2 .. n
                If given, follow the following syntax. (Note: only the column indexes which are specified in the dictionary
                are included in the return data structure.

        Note:
                >>> columns = {
                >>>     0: "id",
                >>>     1: "name",
                >>>     ...
                >>>     <index of column>: <column name>}
                >>>

        Returns:
            list of OrderedDict. The text response is mapping in a list of dictionary. Each dictionary in the list would
                have the following format.

        Note:
            If columns is None.
                >>> [{0: <row0 value1>, 1: <row0  value2>, ..., n: <row0  valueN>},
                >>>  {0: <row1 value1>, 1: <row1 value2>, ..., n: <row1 valueN>},
                >>>  {0: <rowN value1>, 1: <rowN value2>, ..., n: <rowN valueN>}]
            If columns is a list of dict
                >>> [{<column name 0>: <row0 value1>, <column name 1>: <row0  value2>, ..., <column name N>: <row0  valueN>},
                >>>  {<column name 0>: <row1 value1>, <column name 1>: <row1 value2>, ..., <column name N>: <row1 valueN>},
                >>>  {<column name 0>: <rowN value1>, <column name 1>: <rowN value2>, ..., <column name N>: <rowN valueN>}]

        Examples:
            >>> resp = '''
            >>> show interface craft| tab
            >>>                                                   NET                                                                                VENDOR      DHCP        DHCP   DHCP               TFTP                                        POOL   POOL
            >>>              ADMIN    OPER                        CONFIG                                             RX     RX       TX     TX       CLASS       CLIENT      LEASE  LEASE  SERVER      SERVER  DHCP     OPER   POOL  POOL    POOL  RANGE  RANGE
            >>> ID  NAME     STATE    STATE    MAC ADDR           TYPE    IP ADDRESS     IP MASK        IP GATEWAY   PKTS   OCTETS   PKTS   OCTETS   IDENTIFIER  IDENTIFIER  TIME   TIME   IDENTIFIER  NAME    SERVER   STATE  NAME  SUBNET  MASK  START  END
            >>> -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            >>> 1   craft 1  enable   unknown  00:02:5D:BA:8D:B7  static  10.243.19.213  255.255.252.0  10.243.16.1  73252  6321990  33653  9636125  -           -           -      -      -           -       disable  -      -     -       -     -      -
            >>> 2   craft 2  disable  unknown  00:02:5D:BA:8D:B7  static  none           none           -            0      0        0      0        -           -           -      -      -           -       disable  -      -     -       -     -      -
            >>>
            >>> '''
            >>> m = ResponseMap(resp)
            >>> ret1 = m.table_match_by_delimiter()
            >>>
            >>> print(resp)
            >>> r = ResponseMap(resp)
            >>>
            >>> table1 = r.table_match_by_delimiter()
            >>> import pprint
            >>> pprint.pprint(table1[-1]) ;# print last row of table
            >>> #printout
            >>> #OrderedDict([(0, '2'), (1, 'craft 2'), (2, 'disable'), ... , (25, '-')])
            >>> from collections import OrderedDict
            >>> table2 = r.table_match_by_delimiter(columns=OrderedDict({0: "id", 1: "name", 4: "mac"}))
            >>> pprint.pprint(table2[-1]) ;#print last row of table
            >>> #printout
            >>> #OrderedDict([('id', '2'), ('name', 'craft 2'), ('mac', '00:02:5D:BA:8D:B7')])
        """
        _l = self.response.splitlines()

        if start_line is None:
            _start = 0
        else:
            _start = self._check_start_line(start_line)

        if end_line is None:
            _end = len(_l)
        else:
            _end = self._check_end_line(end_line)

        ret = []

        if columns is None:
            for i in range(_start, _end):
                try:
                    line = _l[i]
                except IndexError:
                    break
                if str(line).strip() == "": continue
                _p = re.split(delimiter, str(line).strip())
                cnt = 0
                _d = OrderedDict()
                for j in _p:
                    _d[cnt] = j
                    cnt += 1
                ret.append(_d)

        else:
            for i in range(_start, _end):
                try:
                    line = _l[i]
                except IndexError:
                    continue
                if str(line).strip() == "": continue
                _p = re.split(delimiter, str(line).strip())
                _d = OrderedDict()
                for k, v in columns.items():
                    try:
                        _d[v] = _p[int(k)]
                    except IndexError:
                        pass
                ret.append(_d)
        return ret

    def linearize_tabbed_response(self, tab=" "):
        """
        Convert response of hierarchy structure into list of flatten data structure.
        for example, exa cli response.

        Args:
            tab (str) - indentation of the response of hierarchy structure

        Returns:
            list of "flatten" data strcuture

        Example:
            >>> r = session_1.command("show running-config", timeout=10)
            >>> #r["response"]
            >>> #interface ethernet x3
            >>> # no shutdown
            >>> # service-role inni
            >>> #  transport-service-profile tsp_x3
            >>> # !
            >>> #!
            >>> lines = ResponseMap(r["response"]).linearize_tabbed_response()
            >>> #lines
            >>> #["interface ethernet x3",
            >>> #"interface ethernet x3 no shutdown",
            >>> #"interface ethernet x3 service-role inni",
            >>> #"interface ethernet x3 service-role inni transport-service-profile tsp_x3",
            >>> #]

        """
        lines = self.response.splitlines()
        is_tab = tab.__eq__
        stack = []
        ret = []
        for line in lines:
            indent = len(list(takewhile(is_tab, line)))
            stack[indent:] = [line.lstrip()]
            ret.append(" ".join(stack))
        return ret

    def table_match(self, pattern, return_as_dict=False):
        """
        Match response into table in form of list of list or list of dictionary.

        Args:
            pattern (str): regex pattern to match each line of response
            return_as_dict (bool): - optional if True, return as list of dictionary; False returns as list of list

        Returns:
            list of list (default).
            or list of dictionary if <return_as_dict> == True

        Example:
            >>> r = session_1.command("show running-config", timeout=10)
            >>> lines = ResponseMap(r["response"]).linearize_tabbed_response()
            >>> resp = ResponseMap("\\n".join(lines))
            >>> x = resp.table_match(r"interface ethernet (\S+) service-role (\S+) transport-service-profile (\S+)")
            >>> for _x in x:
            >>>    print (_x)
            >>> # ...
            >>> # ('x3', 'inni', 'tsp_x3')
            >>> # ...
        """
        lines = self.response.splitlines()
        ret = []
        p = re.compile(pattern, flags=re.MULTILINE)
        for line in lines:
            m = p.match(line)
            if m:
                if return_as_dict is False:
                    ret.append(m.groups())
                else:
                    ret.append(m.groupdict())
        return ret

    def parse_nested_text(self, start_line=0, end_line=None, separator=r"\s+", string_identifier='"'):
        """Parses nested key-value pairs and transforms them into a tree-like structure. It groups together sections by
        name.

        Args:
            start_line (int): line from which to begin parsing from
            end_line (int): line at which to stop parsing. Default is None, in which case the text is parsed to the end.
            separator (str): a regular expression to define the token separator. Defaults to "\s+", which is all
                whitespace
            string_identifier (str): a character that denotes the beginning and end of a string; a string is treated as one token

        Returns:
            NestedKeyValueMap: The tree-like structure containing the result of the parse.

        Examples:
            >>> text = '''
            >>> custom header 1
            >>>     sub section 1
            >>>         key value
            >>>     sub section 2
            >>>         key value
            >>> custom header 2
            >>>     sub section 1
            >>>         key value
            >>> '''
            >>> resp = ResponseMap(text).parse_nested_text()

            Will internally be represented by a tree that looks like this:

            >>> {
            >>> 	'custom': {
            >>> 		'header': {
            >>> 			'1': {
            >>> 				'sub': {
            >>> 					'section': {
            >>> 						'1': {
            >>> 							'key': {
            >>> 								'value': {}
            >>> 							}
            >>> 						},
            >>> 						'2': {
            >>> 							'key': {
            >>> 								'value': {}
            >>> 							}
            >>> 						}
            >>> 					}
            >>> 				}
            >>> 			},
            >>> 			'2': {
            >>> 				'sub': {
            >>> 					'section': {
            >>> 						'1': {
            >>> 							'key': {
            >>> 								'value': {}
            >>> 							}
            >>> 						}
            >>> 					}
            >>> 				}
            >>> 			}
            >>> 		}
            >>> 	}
            >>> }

            Then, the 'value' under 'sub section 1' of 'custom header 1' can be retrieved like this:

            >>> resp['custom']['header']['1']['sub']['section']['1']['key'].next_value()

            Or if you want to get 'value' under 'custom header 2':

            >>> resp['custom']['header']['2']['sub']['section']['1']['key'].next_value()

        """
        lines = self.response.splitlines()[start_line:end_line]

        ret = _NestedKeyValueMapEmitter(-1)
        cur_node = ret

        for line in lines:
            if line.strip() == '':
                continue

            indent_level = len(line) - len(line.lstrip())

            unmerged_elements = re.split(separator, line.strip())
            elements = ['']

            # Merge elements if string_delimiter (" by default) is found
            for i in unmerged_elements:
                if elements[-1].count(string_identifier) % 2 == 1:
                    elements[-1] += " " + i
                elif elements[-1].strip() == "":
                    elements[-1] = i
                else:
                    elements.append(i)

            new_node = _NestedKeyValueMapEmitter(indent_level, str(elements), elements)

            if new_node.indentation > cur_node.indentation:
                parent_node = cur_node
            elif new_node.indentation == cur_node.indentation:
                parent_node = cur_node.parent
            else:
                peer_node = cur_node

                while peer_node.parent and new_node.indentation < peer_node.indentation:
                    peer_node = peer_node.parent

                # Handle unaligned indentation
                if new_node.indentation > peer_node.indentation:
                    parent_node = peer_node
                else:
                    parent_node = peer_node.parent

            cur_node = parent_node.add(new_node)

        return ret.emit()


class NestedTextMap(dict):
    """A dictionary-like structure with a couple of methods for accessing the data
    """

    def next_value(self, index=0):
        """Returns the value of the next token in the response.

        Args:
            index (int): The index of the next token, in case there is more than one. Defaults to 0.

        Examples:
            >>> text = '''
            >>> custom header 1
            >>>     sub section 1
            >>>         key value
            >>>     sub section 2
            >>>         key value
            >>> custom header 2
            >>>     sub section 1
            >>>         key value
            >>> '''
            >>> resp = ResponseMap(text).parse_nested_text()
            >>> resp['custom']['header'].next_value()  # Will return '1'
            >>> resp['custom']['header'].next_value(0) # Same thing as above; Will return '1'
            >>> resp['custom']['header'].next_value(1) # Will return '2'

        Returns:
            str: the value of the next string token in the mapping.

        Raises:
            IndexError: if index is out of range

        """
        return self.keys()[index]

    def next_value_list(self):
        """Returns the list of tokens available next

        Examples:
            >>> text = '''
            >>> custom header 1
            >>>     sub section 1
            >>>         key value
            >>>     sub section 2
            >>>         key value
            >>> custom header 2
            >>>     sub section 1
            >>>         key value
            >>> '''
            >>> resp = ResponseMap(text).parse_nested_text()
            >>> resp['custom']['header'].next_value_list()  # Will return the list ['1', '2']
            >>> resp['custom']['header']['1']['sub']['section']['1']['key'].next_value_list() # Will return ['value']
        """
        return self.keys()

    def __str__(self):
        """For ease of use, converting to string is the same as getting next value
        """
        return self.next_value(0)


class _NestedKeyValueMapEmitter(object):
    def __init__(self, indentation=0, name='', value=[]):
        """Helper object for ResponseMap.parse_nested_text()
        """
        self.indentation = indentation
        self.name = name
        self.parent = None
        self.children = {}
        self.value = value

    @staticmethod
    def __merge_dict(d1, d2):
        """Take two dictionaries and merge them together, preserving keys and values. Does not mutate d1 and d2

        Returns:
            dict: new dictionary containing the merged d1 and d2
        """
        ret = NestedTextMap()

        for k, v in (d1.items() + d2.items()):
            if k not in ret:
                ret[k] = v
            else:
                ret[k] = _NestedKeyValueMapEmitter.__merge_dict(ret[k], v)

        return ret

    def add(self, child_node):
        """Add a new node to the tree if it doesn't exist yet.

        Returns:
            _NestedKeyValueMapEmitter: reference to the added node, or to the existing node if new node was not added.
        """
        if child_node.name not in self.children:
            self.children[child_node.name] = child_node
            child_node.parent = self
            ret = child_node
        else:
            ret = self.children[child_node.name]

        return ret

    def emit(self):
        """Converts the tree structure into a NestedKeyValueMap

        Returns:
            NestedTextMap: the resulting mapping
        """
        ret = NestedTextMap()
        cur = ret

        for val in self.value:
            cur[val] = NestedTextMap()
            cur = cur[val]

        for i in self.children:
            child_tree = self.children[i].emit()
            cur.update(_NestedKeyValueMapEmitter.__merge_dict(cur, child_tree))

        return NestedTextMap(ret)

    def dump(self, indent=0):
        """Debug command - returns the hierarchy of the tree

        Returns:
            str: the text representation of the tree
        """
        ret = '%s(NODE: (%s)%s)\n' % (' ' * indent * 4, self.indentation, self.name)

        for i in self.children:
            ret += self.children[i].dump(indent + 1)

        return ret

    def __str__(self):
        return '(NODE: (%s)%s)' % (self.indentation, self.name)
