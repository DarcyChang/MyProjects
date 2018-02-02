"""Netconf session APIs

Methods:
    RestfulSession.post()   - Create
    RestfulSession.get()    - Read
    RestfulSession.put()    - Update
    RestfulSession.delete() - Delete
"""
__author__ = 'kelvin'

from ncclient import manager
from ncclient import operations as ncops
from cafe.core.logger import CLogger as Logger
from cafe.core.utils import create_folder
from cafe.core.signals import SESSION_RESTFUL_ERROR
from lxml import etree
import requests
import  time

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
retry_count = 6
"""
>>>
>>>
>>> import requests
>>>
>>>
>>> s = requests.Session()
>>> s.auth = ('kelee', 'Zaq!2wsx')
>>> s.headers.update({'Content-type': 'application/json'})
>>> r = s.get("http://maps.googleapis.com/maps/api/geocode/xml?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false")
<Response [200]>
>>> r = s.get("http://jira.calix.local/rest/api/2/search?jql=assignee=kelee")
>>> r.text
>>> r.__class__
"""
class RestfulSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=SESSION_RESTFUL_ERROR)

class RestfulSession(object):
    """netconfig APIs class

    """
    def __init__(self, sid=None , user="", password="", auth_type="default",
                 headers={'Content-type': 'application/json'},
                 timeout = 3, logfile=None, **kwargs):
        self.sid = sid
        self.session = requests.Session()
        self.user = user
        self.password = password
        self.auth_type = auth_type
        self.headers = headers
        self.timeout = timeout
        self.session_log = Logger(self.sid)
        self.session_log.console = False
        self.logfile = logfile

    def login(self):
        """Restful API login is not required to be implemented
        """
        pass

    @property
    def headers(self):
        if self.session:
            return self.session.headers
        else:
            return None

    @headers.setter
    def headers(self, h):
        if self.session:
            self.session.headers.update(h)

    @property
    def auth_type(self):
        return self._auth_type

    @auth_type.setter
    def auth_type(self, t):
        self._auth_type = str(t).lower()
        if self.session:
            self.session.auth = (self.user, self.password)

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, f):
        if f is None:
            self.session_log.disable_file_logging()
            return
        if create_folder(f):
            debug("create folder for %s successful" % f)
        else:
            debug("create folder for %s failed" % f)
            return
        self._logfile = f
        self.session_log.enable_file_logging(log_file=f)

    def _write_log(self, s):
        if self.session_log:
            try:
                root = etree.XML(s)
                self.session_log.info(etree.tostring(root, pretty_print=True))
            except:
                self.session_log.info(s)

    def close(self):
        if self.session:
            self.session.close()
            self._write_log("close successful. session(%s)" % self.sid)

    def get(self, url, timeout=None, payload=None, **kwargs):
        """Restful api get operation

        Args:
            url (str): url  of web resource
            timeout (float): stop waiting for a response after a given number of seconds. defauts is None; to use the
            default timeout value set when the session is created.
            payload (dict): addition key/value pair infor for the url. detail refer to "
                http://docs.python-requests.org/en/latest/user/quickstart/" ->Passing Parameters In URLs section

        Returns:
            requests.models.Response object. please refer to
                "http://docs.python-requests.org/en/latest/user/quickstart/#response-content"

        Note:
            timeout is not a time limit on the entire response download;
            rather, an exception is raised if the server has not issued a response
            for timeout seconds (more precisely, if no bytes have been received on
            the underlying socket for timeout seconds).

        Raises:
            RestfulSessionException: if any restful api operation error, such as url is not reachable.

        Example:
            >>> session_mgr = get_session_manager(host='localhost', port=18890)
            >>> s = session_mgr.create_session("rest_1", session_type="restful")
            >>> r = s.get("http://maps.googleapis.com/maps/api/geocode/xml?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false")
            >>> assert "200" in str(r)
            >>> session_mgr.remove_session(s.sid)
        """
        self._write_log("get - url == %s" % url)

        for i in range(retry_count):
            try:
                if timeout is None:
                    ret = self.session.get(url, timeout=self.timeout, params=payload, **kwargs)
                else:
                    ret = self.session.get(url, timeout=float(timeout), params=payload, **kwargs)
                break
            except Exception as e:
                if i == retry_count - 1:
                    raise RestfulSessionException("get operation error. session(%s).\r\nDetail: %s" % (self.sid, e.message))
                else:
                    self._write_log("Get action error, waiting for a retry")
                    time.sleep(30)

        self._write_log("get - return ==")
        self._write_log(ret)
        self._write_log(ret.text)

        return ret

    def post(self, url, data=None, **kwargs):
        """Restful api post (create) operation

        Args:
            url (str): url  of web resource
            data (object):  object to be created. the object type and content is depending on the url.
                it can be file stream for uploading a file or json for create a data entry.
            kwargs: additional post operation parameters

        Returns:
            requests.models.Response object. please refer to
                "http://docs.python-requests.org/en/latest/user/quickstart/#response-content"

        Raises:
            RestfulSessionException: if any restful api operation error, such as url is not reachable.

        Example:
            >>> session_mgr = get_session_manager(host='localhost', port=18890)
            >>> s = session_mgr.create_session("rest_1", session_type="restful")
            >>> data={"title": "foo", "body": "bar", "userId": 1}
            >>> r = s.post("http://jsonplaceholder.typicode.com/posts", data=json.dumps(data))
            >>> assert "201" in str(r)
            >>> session_mgr.remove_session(s.sid)

        """
        self._write_log("post - url == %s" % url)
        self._write_log("post - data == %s" % str(data))
        self._write_log("post - kwargs == %s" % str(kwargs))

        try:
            ret = self.session.post(url, data=data, **kwargs)
        except:
            raise RestfulSessionException("post operation error. session(%s)" % self.sid)

        self._write_log("post - return ==")
        self._write_log(ret)
        self._write_log(ret.text)

        return ret

    def put(self, url, data=None, **kwargs):
        """Restful api put (update) operation

        Args:
            url (str): url  of web resource
            data (object):  object to be created. the object type and content is depending on the url.
                it can be file stream for uploading a file or json for create a data entry.
            kwargs: additional post operation parameters

        Returns:
            requests.models.Response object. please refer to
                "http://docs.python-requests.org/en/latest/user/quickstart/#response-content"

        Raises:
            RestfulSessionException: if any restful api operation error, such as url is not reachable.

        Example:
            >>> session_mgr = get_session_manager(host='localhost', port=18890)
            >>> s = session_mgr.create_session("rest_1", session_type="restful")
            >>> data={"title": "foo", "body": "bar", "userId": 20, "id": 1}
            >>> r = s.put("http://jsonplaceholder.typicode.com/posts/1", data=json.dumps(data))
            >>> print(r)
            >>> assert "200" in str(r))
            >>> session_mgr.remove_session(s.sid)

        """
        self._write_log("put - url == %s" % url)
        self._write_log("put - data == %s" % str(data))
        self._write_log("put - kwargs == %s" % str(kwargs))

        try:
            ret = self.session.put(url, data=data, **kwargs)
        except:
            raise RestfulSessionException("put operation error. session(%s)" % self.sid)

        self._write_log("put - return ==")
        self._write_log(ret)
        self._write_log(ret.text)

        return ret

    def delete(self, url, **kwargs):
        """Restful api delete operation

        Args:
            url (str): url  of web resource
            kwargs: additional post operation parameters

        Returns:
            requests.models.Response object. please refer to
                "http://docs.python-requests.org/en/latest/user/quickstart/#response-content"

        Raises:
            RestfulSessionException: if any restful api operation error, such as url is not reachable.

        Example:
            >>> session_mgr = get_session_manager(host='localhost', port=18890)
            >>> s = session_mgr.create_session("rest_1", session_type="restful")
            >>> r = s.delete("http://jsonplaceholder.typicode.com/posts/1")
            >>> print(r)
            >>> assert "200" in str(r)
            >>> session_mgr.remove_session(s.sid)

        """
        self._write_log("delete - url == %s" % url)
        self._write_log("delete - kwargs == %s" % str(kwargs))

        try:
            ret = self.session.delete(url, **kwargs)
        except:
            raise RestfulSessionException("delete operation error. session(%s)" % self.sid)

        self._write_log("delete - return ==")
        self._write_log(ret)
        self._write_log(ret.text)

        return ret
    # def edit_config(self, config, target="running"):
    #     """edit device configruation.
    #
    #     Args:
    #         config (xml string): xml rpc message to configure device attributes.
    #         target (string): netconfig target device configuration datastore. default "running".
    #
    #     Returns:
    #         ncclient.RPCReply object. please refer to http://ncclient.readthedocs.org/en/latest
    #
    #     Examples:
    #         >>> x = '''
    #         >>>     <config>
    #         >>>         <config xmlns="http://www.calix.com/ns/exa/base">
    #         >>>         <interface>
    #         >>>            <ethernet>
    #         >>>              <port>g1</port>
    #         >>>               <shutdown>false</shutdown>
    #         >>>            </ethernet>
    #         >>>         </interface>
    #         >>>         </config>
    #         >>>     </config>
    #         >>> '''
    #         >>> cx = self.session_mgr.create_session("netconf_1", session_type="netconf", timeout=4,
    #         >>>                                  host="10.243.19.213", user="root", password="root")
    #         >>> cx.login()
    #         >>> try:
    #         >>>     r = cx.session.edit_config(target="running", config=x)
    #         >>>     print(r.ok)
    #         >>> finally:
    #         >>>     self.session_mgr.remove_session(cx.sid)
    #
    #     """
    #
    #     self._write_log("edit_config - target == %s" % target)
    #     self._write_log("edit_config - config ==")
    #     self._write_log(str(config))
    #
    #     if config is None:
    #         raise NetConfSessionException("edit_config: invalid config value: session (%s)" % self.sid)
    #
    #     ret = self.session.edit_config(target=target, config=config)
    #
    #     self._write_log("edit_config - return ==")
    #     self._write_log(str(ret))
    #
    #     return ret

# if __name__ == "__main__":
#
#     from cafe.core.logger import init_logging
#     init_logging()
#     import cafe
#     session_mgr = cafe.get_session_manager(host='localhost', port=18890)
#
#
#     #s = RestfulSession(sid="rest", logfile="restapi.log")
#     s = session_mgr.create_session("rest_1", session_type="restful")
#
#     s.session_log.set_console(True)
#     r = s.get("http://maps.googleapis.com/maps/api/geocode/xml?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false")
#     #print(r)
#     #print(r.text)
#
#     url = 'http://myserver/post_service'
#     data = dict(name='joe', age='10')
#     try:
#         r = s.post(url, data=data, allow_redirects=True)
#     except:
#         pass
#
#     session_mgr.remove_session(s.sid)
#     s = session_mgr.create_session("rest_1", session_type="restful")
#
#     import json
#
#     data={"title": "foo", "body": "bar", "userId": 1}
#     #print json.dumps(data)
#     r = s.post("http://jsonplaceholder.typicode.com/posts", data=json.dumps(data))
#
#     data={"title": "foo", "body": "bar", "userId": 20, "id": 1}
#     #print json.dumps(data)
#     r = s.put("http://jsonplaceholder.typicode.com/posts/1", data=json.dumps(data))
#
#     r = s.delete("http://jsonplaceholder.typicode.com/posts/1")
#     r = requests.delete("http://jsonplaceholder.typicode.com/posts/1")
#     print(r)
