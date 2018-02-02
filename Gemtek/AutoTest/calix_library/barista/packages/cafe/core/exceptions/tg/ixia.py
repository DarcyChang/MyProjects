__author__ = 'Shawn Wang'

from cafe.core.exceptions.exceptions import CafeException


class IXIAError(CafeException):

    code = '000060000'
    description = 'IXIA General Error'


class IXIAConnectChassisError(IXIAError):

    code = '000060001'
    description = 'IXIA connect to chassis error'


class IXIAConfigureInterfaceError(IXIAError):

    code = '000060002'
    description = 'IXIA configure interface error'


class IXIACleanupSessionError(IXIAError):

    code = '000060003'
    description = 'IXIA clean up session error'


class IXIAEnableTestLogError(IXIAError):

    code = '000060004'
    description = 'IXIA enable log error'


class IXIAConfigureTrafficError(IXIAError):

    code = '000060021'
    description = 'IXIA configure traffic error'


class IXIAControlTrafficError(IXIAError):

    code = '000060040'
    description = 'IXIA control traffic error'


class IXIAGetTrafficStatsError(IXIAError):

    code = '000060041'
    description = 'IXIA get traffic stats error'


class IXIAEnableTrafficError(IXIAError):

    code = '000060042'
    description = 'IXIA enable traffic error'


class IXIADisableTrafficError(IXIAError):

    code = '000060043'
    description = 'IXIA disable traffic error'


class IXIAConfigureDHCPServerError(IXIAError):

    code = '000060060'
    description = 'IXIA configure dhcp server error'


class IXIAConfigureDHCPClientError(IXIAError):

    code = '000060063'
    description = 'IXIA configure dhcp client error'


class IXIAConfigureDHCPClientGroupError(IXIAError):

    code = '000060066'
    description = 'IXIA configure dhcp client group error'


class IXIAControlDHCPServerError(IXIAError):

    code = '000060069'
    description = 'IXIA control dhcp server error'


class IXIAControlDHCPClientGroupError(IXIAError):

    code = '000060070'
    description = 'IXIA control dhcp client group error'


class IXIAGetDHCPServerStatsError(IXIAError):

    code = '000060071'
    description = 'IXIA get dhcp server stats error'


class IXIAGetDHCPClientStatsError(IXIAError):

    code = '000060072'
    description = 'IXIA get dhcp client stats error'


class IXIAConfigurePPPoXServerError(IXIAError):

    code = '000060100'
    description = 'IXIA configure pppox server error'


class IXIAConfigurePPPoXClientError(IXIAError):

    code = '000060103'
    description = 'IXIA configure pppox client error'


class IXIAControlPPPoXError(IXIAError):

    code = '000060106'
    description = 'IXIA control pppox error'


class IXIAGetPPPoXStatsError(IXIAError):

    code = '000060107'
    description = 'IXIA get pppox stats error'


class IXIAConfigureIGMPQuerierError(IXIAError):

    code = '000060130'
    description = 'IXIA configure igmp querier error'


class IXIAConfigureIGMPError(IXIAError):

    code = '000060133'
    description = 'IXIA configure igmp session error'


class IXIAConfigureIGMPGoupError(IXIAError):

    code = '000060136'
    description = 'IXIA configure imgp group error'


class IXIAConfigureMulticastGroupError(IXIAError):

    code = '000060139'
    description = 'IXIA configure multicast group error'


class IXIAConfigureMulticastSourceError(IXIAError):

    code = '000060142'
    description = 'IXIA configure multicast source error'


class IXIAControlIGMPQuerierError(IXIAError):

    code = '000060145'
    description = 'IXIA control igmp querier error'


class IXIAControlIGMPGroupError(IXIAError):

    code = '000060146'
    description = 'IXIA control igmp group error'


class IXIAGetIGMPQuerierStatsError(IXIAError):

    code = '000060147'
    description = 'IXIA get igmp querier stats error'


class IXIAGetIGMPGroupStatsError(IXIAError):

    code = '000060148'
    description = 'IXIA get imgp group stats error'


class IXIAEnableIGMPError(IXIAError):

    code = '000060149'
    description = 'IXIA enable igmp error'


class IXIADisableIGMPError(IXIAError):

    code = '000060150'
    description = 'IXIA disable igmp error'


class IXIAConfigurePacketTriggerError(IXIAError):

    code = '00060170'
    description = 'IXIA configure packet trigger error'


class IXIAConfigurePacketBufferError(IXIAError):

    code = '00060171'
    description = 'IXIA configure packet buffer error'


class IXIAConfigurePacketFilterError(IXIAError):

    code = '00060172'
    description = 'IXIA configure packet filter error'


class IXIAControlPacketError(IXIAError):

    code = '00060173'
    description = 'IXIA control packet error'


class IXIAGetPacketStatsError(IXIAError):

    code = '00060174'
    description = 'IXIA get packet stats error'


class IXIAConfigureHostError(IXIAError):

    code = '000060180'
    description = 'IXIA configure device error'


class IXIAHostSendCommandError(IXIAError):

    code = '000060183'
    description = 'IXIA device send command error'


class IXIAControlAllDeviceError(IXIAError):

    code = '000060185'
    description = 'IXIA control all device error'


class IXIAControlAllProtocolError(IXIAError):

    code = '000060186'
    description = 'IXIA control all protocol error'


class IXIAConfigureCFMBridgeError(IXIAError):

    code = '00060200'
    description = 'IXIA configure cfm bridge error'


class IXIAConfigureCFMVlanError(IXIAError):

    code = '00060201'
    description = 'IXIA configure cfm vlan error'


class IXIAConfigureCFMLinksError(IXIAError):

    code = '00060202'
    description = 'IXIA configure cfm links error'


class IXIAConfigureCFMMdMegError(IXIAError):

    code = '00060203'
    description = 'IXIA configure cfm md_meg error'


class IXIAConfigureCFMMipMepError(IXIAError):

    code = '00060204'
    description = 'IXIA configure cfm mip_mep error'


class IXIAControlCFMBridgeError(IXIAError):

    code = '00060205'
    description = 'IXIA control cfm bridge error'
