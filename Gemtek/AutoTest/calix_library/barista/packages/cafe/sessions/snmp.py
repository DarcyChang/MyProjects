from SnmpLibrary import SnmpLibrary
from pysnmp.smi.error import WrongValueError

SNMP_V2C = "snmp_v2c"
SNMP_V3 = "snmp_v3"

class SnmpError(Exception): pass

class SnmpSessionBase(object):
    def __init__(self, sid=None, host=None, port=161, timeout=120, logfile=None):
        self.snmp_library = SnmpLibrary()
        self.sid = sid
        self.host = host
        self.port = port
        self.connected = False
    
    def login(self):
        try:
            self.snmp_library.get("sysDescr")
        except RuntimeError as e:
            raise SnmpError("Could not connect to SNMP host %s:%s" % (self.host, self.port))

        self.connected = True

    def close(self):
        if self.connected:
            self.snmp_library.close_snmp_connection()
            self.connected = False

    def __del__(self):
        self.close()



class SnmpV2CSession(SnmpSessionBase):
    def __init__(self, sid=None, host=None, port=161, community=None, timeout=120, logfile=None, **kwargs):
        if community is None:
            raise SnmpError("'community' field not found in SNMPv2 connection '%s'" % sid)

        super(SnmpV2CSession, self).__init__(sid, host, port, timeout, logfile)
        self.community_string = community

    def login(self):
        self.session_index = self.snmp_library.open_snmp_v2c_connection(
                self.host, 
                self.community_string, 
                self.port, 
                self.sid,
                )
        super(SnmpV2CSession, self).login()


class SnmpV3Session(SnmpSessionBase):
    AUTH_PROTOCOLS = ['MD5', 'SHA', None]
    ENCR_PROTOCOLS = ['DES', '3DES', 'AES128', 'AES192', 'AES256', None]

    def __init__(self, sid=None, host=None, port=161, username=None, password=None, 
            encryption_password=None, authentication_protocol=None, encryption_protocol=None, timeout=120, logfile=None, **kwargs):
        if username is None:
            raise SnmpError("'username' field not found in SNMPv3 connection '%s'" % sid)

        if password is None and authentication_protocol is not None:
            raise SnmpError("'password' field not found in SNMPv3 connection '%s'. Password must be specified if authentication protocol is not None." % sid)
        
        if encryption_password is None and encryption_protocol is not None:
            raise SnmpError("'encryption_password' field not found in SNMPv3 connection '%s'. Encryption key must be specified if encryption protocol is not None." % sid)

        super(SnmpV3Session, self).__init__(sid, host, port, timeout, logfile)

        if authentication_protocol not in SnmpV3Session.AUTH_PROTOCOLS:
            options = ", ".join(map(lambda x: "'%s'" % x if isinstance(x, str) else str(x), SnmpV3Session.AUTH_PROTOCOLS))
            raise SnmpError("Invalid authentication protocol '%s'. Must be one of: %s" % (authentication_protocol, options))

        if encryption_protocol not in SnmpV3Session.ENCR_PROTOCOLS:
            options = ", ".join(map(lambda x: "'%s'" % x if isinstance(x, str) else str(x), SnmpV3Session.ENCR_PROTOCOLS))
            raise SnmpError("Invalid authentication protocol '%s'. Must be one of: %s" % (encryption_protocol, options))

        self.user = username
        self.password = password
        self.encryption_password = encryption_password
        self.authentication_protocol = authentication_protocol
        self.encryption_protocol = encryption_protocol

        with open("my_dump.txt", "w") as f:
            f.write("LOCALS: %s" % str(locals()))

    def login(self):
        self.session_index = self.snmp_library.open_snmp_v3_connection(
                self.host,
                self.user,
                self.password,
                self.encryption_password,
                self.authentication_protocol,
                self.encryption_protocol,
                self.port)

        try:
            super(SnmpV3Session, self).login()
        except WrongValueError:
            raise SnmpError("Invalid authentication/encryption key. Please check the keys and authentication/encryption protocol settings")

def SnmpSession(sid=None, host=None, port=161, version="2c", **kwargs):
    if version == "2c":
        return SnmpV2CSession(sid, host, port, **kwargs)
    elif version == "3":
        return SnmpV3Session(sid, host, port, **kwargs)
    else:
        raise SnmpError("Unknown SNMP version: '%s'. Supported versions: '2c', '3'" % version)

if __name__ == "__main__":
    # s = SnmpV2CSession("sid", "10.243.19.213", 161, "public")
    s = SnmpSession("sid", "10.243.19.213", 161, "2c", community="public")
    s.login()
    print(s.snmp_library.get_display_string("sysDescr"))

    # s2 = SnmpV3Session("sid2", "10.243.19.213", 161, "testuser", "testuser", "key", "MD5", "DES")
    # s2 = SnmpV3Session("sid2", "10.243.19.213", 161, "testuser")
    s2 = SnmpSession("sid2", "10.243.19.213", 161, "3", username="testuser")
    s2.login()


