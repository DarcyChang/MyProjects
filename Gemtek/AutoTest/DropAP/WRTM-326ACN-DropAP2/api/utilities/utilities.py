__author__ = 'gliverm'

from cafe.core.db import teststep
from cafe.core.logger import CLogger as Logger
import time
import md5,sys
import cafe
import re

logger = Logger(__name__)
debug = logger.debug
error = logger.error

"""
API Library: utilities
Description:
    This library contains all functions are general miscellaneous utility scripts.
"""

def gen_ont_md5(fsan):
    """
    Description:
        Generate the md5 related security WPA key and adminstrative password for the ONT primary WiFi SSID.
        Note: Past renditions have also returned the digest, salt, salt+fsan, digest w/salt along with the
        WPA Passkey and admin password.
    Args:
        fsan(str)(required) : ONT fsan value
    Returns:
        Dictionary:
            'key' : string value of generated pass key
            'adminpassword' : ONT administrative password
            'checkpoint' : boolean result of checkpoint on expected results
    """

    salt='8d2k'
    message=fsan
    saltedmessage=salt+message

    m = md5.new()
    m.update(saltedmessage)
    digest=m.hexdigest()
    result = {}
    result['wpakey'] = digest[5:21]
    result['adminpsswd'] = digest[23:31]
    return result

# if __name__ == "__main__":
#     '''
#     The purpose of this section is to test teh APIs created.
#     '''
#     import cafe
#     session_mgr = cafe.get_session_manager()
#     # create a ssh session to exa device
#     exa_ssh_session = session_mgr.create_session("exa1", session_type="ssh",
#                                                  host="10.243.19.213",
#                                                  user="root", password="root")
#     # get EXACommClass object - EXA equipment lib
#     exa = EXAApiClass(exa_ssh_session)
#     # login and open exa cli console
#     exa.login()
#     # exa.command return a dict data structure as we have declare it as teststep
#     r = exa.command("show interface craft 1")
#     cafe.Checkpoint(r['response']).regex("craft 1")
#
#     r = exa.get_interface_craft(1)
#     cafe.Checkpoint(r['name']).regex("craft 1")
