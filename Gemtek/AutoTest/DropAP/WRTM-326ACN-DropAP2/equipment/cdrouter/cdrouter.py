__author__ = 'bmelhus'

from cafe.core.logger import CLogger as Logger
import time
import re


logger = Logger(__name__)
debug = logger.debug
error = logger.error

# ##################################################################################################################
# CD Router Connect/Login
# ##################################################################################################################

class CdrBaseClass(object):
    """
    Class: CalixE7Base is base class of E7.  E7 defines all E-Series sharing the same CLI structure.
    """
    def __init__(self, session, session_type="ssh", release=None, eq_type='cdr'):
        """
        Description:
            Initialize individual CalixE7Base object.
        Args:
            name (str): Name of session
            session (object): session object (to handle communication between an E7 device and Cafe)
            session_type (str): describes protocol to connect to E7 device
            release (str): E7 release for future purpose.  Default = none
        """
        self.session = session
        self.session_type = session_type
        self.release = release
        self.eq_type = eq_type


class CdrApiClass(CdrBaseClass):
    """
    APIs for CD Router.
    """
    def login(self):
        """
        Description:
            login to CD Router
        """
        self.session.login()
        # return tuple (prompt index, <prompt re match object>, text)

        self.session.write("\r")
        r = self.session.expect_prompt()
        self.session.write("set session pager disabled timeout disabled")
        r = self.session.expect_prompt()
        self.session.write("\r")
        r = self.session.expect_prompt()
        # print('r 0 : ',r[0])
        # print('r 2 : ',r[2])
        if r[0] < 0:
            print("CD Router login failed. session(%s)" % self.session.sid)
            #raise CdrException("CD Router login failed. session(%s)" % self.session.sid)
        else:
            debug("CD Router session open. session(%s)" % self.session.sid)

    def _send(self, cmd="", timeout=3):
        """
        Description:
            (Internal use): Write a command to the object returning the response.
        """
        self.session.write(cmd)
        # return tuple (prompt index, <prompt re match object>, text)
        r = self.session.expect_prompt(timeout=timeout)
        # print(r)
        if re.search('remove', cmd, re.S):
            if re.search('ont-config', cmd, re.S):
                return {"prompt": None, "response": r[2]}
            else:
                if r[0] < -1:
                    return {"prompt": None, "response": r[2]}
                else:
                    return {"prompt": r[1].group(), "response": r[2]}
        elif re.search('retrieve', cmd, re.S):
            return {"prompt": None, "response": r[2]}
        elif re.search('bobo', cmd, re.S):
            time.sleep(30)
            if r[0] < -1:
                return {"prompt": None, "response": r[2]}
            else:
                return {"prompt": r[1].group(), "response": r[2]}
        else:
            if r[0] < -1:
                return {"prompt": None, "response": r[2]}
            else:
                return {"prompt": r[1].group(), "response": r[2]}

    def send(self, cmd="", timeout=3):
        """
        Description:
            send command and return response
        Args:
            cmd (str): command
            timeout (float): max time allowed for a response come from session
        Returns:
            dict: {"prompt": str, "response": str}
        """
        result = self._send(cmd, timeout)
        # TODO: Bring throttle out to a global tuning variable
        # Wait put in throttle commands to at most 1 a second
        time.sleep(1)
        return result