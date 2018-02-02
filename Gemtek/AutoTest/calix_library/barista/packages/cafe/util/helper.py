import random
import re

import ipaddress

__author__ = 'kelvin'

import os
import cafe
import inspect
from cafe.core.utils import Param, get_func
from cafe.core.utils import CafeCodeError
import ast
import collections
import sys
import requests
import subprocess
import time
from lxml import etree, objectify


# def get_pip2():
#     path = os.path.dirname(sys.executable)
#     return os.path.join(path, "pip2")
#
# def get_pypm():
#     path = os.path.dirname(sys.executable)
#     return os.path.join(path, "pypm")
#
# try:
#     import wget
# except ImportError:
#     sys.stderr.write("error: python package wget import problem.\n")
#     msg = "in termianl, type: sudo %s install wget\n" % get_pip2()
#     sys.stderr.write(msg)
#     exit(-1)

def pprint_xml(elem):
    """
    pretty print lxml element to console
    """
    print etree.tostring(elem, pretty_print=True)

def get_xlm_elem_text(element, xpath):
    """
    get lxml elements' text values

    Args:
        element (obj or str): lxml element object or string of xml
        xpath (str): xpath to search for child elements

    Return:
        list of values of child elements

    Note:
        if xpath does not matches. the return list is empty []
    """

    if isinstance(element, (str,)):
        elem = etree.XML(element)
    else:
        #assume if is the lxml object
        #if not then the following code will raise exception anyway
        elem = element

    ###clean up xml namespace
    for _elem in elem.getiterator():
        if not hasattr(_elem.tag, 'find'): continue  # (1)
        i = _elem.tag.find('}')
        if i >= 0:
            _elem.tag = _elem.tag[i+1:]

    objectify.deannotate(elem, cleanup_namespaces=True)
    ###
    r = elem.xpath(xpath)
    if r:
        return [ _r.text for _r in r ]
    else:
        return []

def wait_until_session_srv_stop(host="localhost", port=None, max_time=180):
    """
    wait until session server is stop
    by examine the tcp port using by the session server are all released

    TODO:
        check the port state in remote host. currrent implementation work for local host only

    Args:
        host: session server host
        port: session server port
        max_time (int): maximum wait time in sec.

    Return:
        bool: True if session server is stopped before the max_time is reached; false otherwise
    """

    #TODO: how to check for remote host
    #now assumpt the host is local only
    if port is None:
        port = cafe.get_config().session_server.port

    cmd = "netstat -a |grep %s" % str(port)

    t0 = time.time()

    while t0 + max_time > time.time():
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        if output.strip() == "":
            return True
        else:
            #print (output)
            print("WARNING: session server (%s,%s) is still running" % (host, port))
            time.sleep(10)

    return False



def download_file_from_url(url, filename):
    """
    download file from a url

    Args:
        url (str)
        filename (str)

    Returns
        requests request object

    Raise:
        RuntimeError: when the response of download is not ok (http return code 200).

    Example:
    >>> r = download_file_from_url(link, "/tmp/python.tar.gz")
    >>> #print the size of the downloaded file
    >>> print len(r.content)
    >>> #print the requests response object headers data structure
    >>> print r.headers
    >>> #print show if the download is success
    >>> print r.ok
    """
    with open(filename, "wb") as handle:
        response = requests.get(url)
        if not response.ok:
            #do something when download is wrong
            raise RuntimeError("download url response is not ok url=%s, filename=%s" %
                               (url, filename))
        for block in response.iter_content(1024):
            handle.write(block)

    return response


def flatten(d, parent_key='', sep='.'):
    """
    flatten nested dictionary
    >>> d = {"a": {"b": {"c": 1, "d": [1, 2]}}}
    >>> x = flatten(d)
    >>> self.assertEquals(x["a.b.c"], 1)
    >>> self.assertListEqual(x["a.b.d"], [1, 2])

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def check_ping(ipaddr, count=1):
    """
    check ipaddr (hostname) is reachable

    Args:
        ipaddr: ip address or hostname
        count: ping count
    Returns:
        bool: True is reachable; False otherwise
    """
    response = os.system("ping -c %s %s" % (str(count), ipaddr))
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False
    return pingstatus

def literal_eval(s):
    """convert string into python data type

    Args:
    s (str): string of data strcuture

    Returns
    python data type
    """

    return ast.literal_eval(s)

def load_ts_config(filename):

    param = cafe.get_test_param()

    d = Param()
    d.load_ini(filename)
    param.ts_config = d

    #getting the phyiscal topology
    topo_file = d.topology.file
    topo = cafe.get_topology()
    topo.load(topo_file)

    #getting logical topology from phyiscal topology
    try:
        func = get_func(d.topology.function)
        kwargs = d.topology.kwargs
        logical_topo = func(topo, **kwargs)
    except:
        raise CafeCodeError("topology.function or topology.kwargs not found %s" % os.path.abspath(filename))

    param.topo = logical_topo

    test = cafe.Param()
    for f in d.parameters.files:
        test.load(f)

    test.evaluate(test, ns=locals())
    param.test = test

    ret = cafe.Param()
    ret.test = test
    ret.topo = logical_topo
    ret.ts_config = d

    return ret

class CafeFileHelper(object):
    """Cafe File helper class. contains methods to create or manage files in cafe.

    """
    def abspath(self, relative_path):
        """return absolute path of relative path w.r.t the caller.

        Args:
            relative_path: relative path w.r.t to caller

        Returns:
            absolute path of relative <path>.

        """
        (frame, filename, line_number,
            function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        d = os.path.dirname(filename)
        return os.path.join(d, relative_path)

    def create_cafe_paths(self):
        """Create Cafe config paths

        it creates:
            cafe_runner.db_path
            create cafe_runner.log_path
            create cafe_runner.test_result_path

        """
        from cafe.core.config import get_config
        config = get_config()
        #config.bp()

        self.create_path(config.cafe_runner.db_path)
        self.create_path(config.cafe_runner.log_path)
        self.create_path(config.cafe_runner.test_result_path)

    def create_path(self, path):
        try:
            os.makedirs(os.path.abspath(path))
        except:
            pass

#cfs = CafeFileHelper()
def get_cfs():
    return CafeFileHelper()


def str2unicode(data, encoding='UTF-8'):
    if not isinstance(data, basestring):
        raise TypeError('Input data must be base on basestring')

    if isinstance(data, str):
        return data.decode(encoding=encoding)
    return data


def unicode2str(data, encoding='UTF-8'):
    if not isinstance(data, basestring):
        raise TypeError('Input data must be base on basestring')
    if isinstance(data, unicode):
        return data.encode(encoding=encoding)
    return data


def generate_random_mac_address(oui=None):
    """
    Generate random mac address, set mac oui with 00:00:00 if oui not given.
    Args:
        oui: The mac address default oui, it must be set with pattern 00:00:0A or 00-0D-4B

    Returns: full mac address.
    Examples:
        | ${res} | generate_random_mac_address |
        | ${res} | generate_random_mac_address | 00:00:0A |

    """
    if oui is None:
        oui = '00:00:00'

    if not re.match(r'^[\dA-F]{2}[:-][\dA-F]{2}[:-][\dA-F]{2}$', oui.upper()):
        raise ValueError('OUI must be set with pattern 00:00:0A or 00-0D-4B')
    _candidate = '0123456789ABCDEF'
    _remain = ''.join(random.choice(_candidate) for i in range(6))
    return '{}:{}:{}:{}'.format(oui.upper(), _remain[:2], _remain[2:4], _remain[4:]).replace('-', ':')


def generate_ip_address(ip):
    """
    Generate ip address, A string or integer representing the IP.
    Examples:
        | ${ip} | generate ip address | 192.168.1.1 |
        | ${ip} | generate ip address | 3232235777 |

    """
    return ipaddress.ip_address(_get_valid_ip_address(ip))


def generate_ip_network(address, strict=True):
    return ipaddress.ip_network(_get_valid_ip_address(address), strict=strict)


def _get_valid_ip_address(address):
    if isinstance(address, int):
        return address
    elif isinstance(address, basestring):
        if re.match(r'^\d+$', address):
            return int(address)
        else:
            return str2unicode(address)

if __name__ == "__main__":
    #c = CafeFileHelper()
    #print(c.relpath("config/ts.ini"))
    #c.create_cafe_paths()
    pass
    #from cafe.util.helper import wait_until_session_srv_stop as w
    #wait_until_session_srv_stop(port=18890)