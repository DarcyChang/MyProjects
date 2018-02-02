__author__ = 'xizhang'

import cafe
from cafe.sessions.restapi import *
from .proto.base import DriverBase

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

class RestfulDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app
        pass

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

        """
        return self._session.get(url, timeout, payload, **kwargs)

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
        """
        return self._session.post(url, data, **kwargs)

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

        """
        return self._session.put(url, data, **kwargs)

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

        """
        return self._session.delete(url, **kwargs)



