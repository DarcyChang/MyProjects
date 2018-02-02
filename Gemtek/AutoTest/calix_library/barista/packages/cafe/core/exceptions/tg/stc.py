__author__ = 'Shawn Wang'

from cafe.core.exceptions.exceptions import CafeException


class STCError(CafeException):

    code = '000050000'
    description = 'STC General Error'


class STCConnectChassisError(STCError):

    code = '000050001'
    description = 'STC connect to chassis error'


class STCConfigureInterfaceError(STCError):

    code = '000050002'
    description = 'STC configure interface error'


class STCCleanupSessionError(STCError):

    code = '000050003'
    description = 'STC clean up session error'


class STCEnableTestLogError(STCError):

    code = '000050004'
    description = 'STC enable log error'


class STCConfigureTrafficError(STCError):

    code = '000050021'
    description = 'STC configure traffic error'


class STCControlTrafficError(STCError):

    code = '000050040'
    description = 'STC control traffic error'


class STCGetTrafficStatsError(STCError):

    code = '000050041'
    description = 'STC get traffic stats error'


class STCEnableTrafficError(STCError):

    code = '000050042'
    description = 'STC enable traffic error'


class STCDisableTrafficError(STCError):

    code = '000050043'
    description = 'STC disable traffic error'


class STCConfigureDHCPServerError(STCError):

    code = '000050060'
    description = 'STC configure dhcp server error'


class STCConfigureDHCPClientError(STCError):

    code = '000050063'
    description = 'STC configure dhcp client error'


class STCConfigureDHCPClientGroupError(STCError):

    code = '000050066'
    description = 'STC configure dhcp client group error'


class STCControlDHCPServerError(STCError):

    code = '000050069'
    description = 'STC control dhcp server error'


class STCControlDHCPClientGroupError(STCError):

    code = '000050070'
    description = 'STC control dhcp client group error'


class STCGetDHCPServerStatsError(STCError):

    code = '000050071'
    description = 'STC get dhcp server stats error'


class STCGetDHCPClientStatsError(STCError):

    code = '000050072'
    description = 'STC get dhcp client stats error'


class STCConfigurePPPoXServerError(STCError):

    code = '000050100'
    description = 'STC configure pppox server error'


class STCConfigurePPPoXClientError(STCError):

    code = '000050103'
    description = 'STC configure pppox client error'


class STCControlPPPoXError(STCError):

    code = '000050106'
    description = 'STC control pppox error'


class STCGetPPPoXStatsError(STCError):

    code = '000050107'
    description = 'STC get pppox stats error'


class STCConfigureIGMPQuerierError(STCError):

    code = '000050130'
    description = 'STC configure igmp querier error'


class STCConfigureIGMPError(STCError):

    code = '000050133'
    description = 'STC configure igmp session error'


class STCConfigureIGMPGoupError(STCError):

    code = '000050136'
    description = 'STC configure imgp group error'


class STCConfigureMulticastGroupError(STCError):

    code = '000050139'
    description = 'STC configure multicast group error'


class STCConfigureMulticastSourceError(STCError):

    code = '000050142'
    description = 'STC configure multicast source error'


class STCControlIGMPQuerierError(STCError):

    code = '000050145'
    description = 'STC control igmp querier error'


class STCControlIGMPGroupError(STCError):

    code = '000050146'
    description = 'STC control igmp group error'


class STCGetIGMPQuerierStatsError(STCError):

    code = '000050147'
    description = 'STC get igmp querier stats error'


class STCGetIGMPGroupStatsError(STCError):

    code = '000050148'
    description = 'STC get imgp group stats error'


class STCEnableIGMPError(STCError):

    code = '000050149'
    description = 'STC enable igmp error'


class STCDisableIGMPError(STCError):

    code = '000050150'
    description = 'STC disable igmp error'


class STCConfigurePacketTriggerError(STCError):

    code = '00050170'
    description = 'STC configure packet trigger error'


class STCConfigurePacketBufferError(STCError):

    code = '00050171'
    description = 'STC configure packet buffer error'


class STCConfigurePacketFilterError(STCError):

    code = '00050172'
    description = 'STC configure packet filter error'


class STCControlPacketError(STCError):

    code = '00050173'
    description = 'STC control packet error'


class STCGetPacketStatsError(STCError):

    code = '00050174'
    description = 'STC get packet stats error'


class STCConfigureDeviceError(STCError):

    code = '000050180'
    description = 'STC configure device error'


class STCDeviceSendCommandError(STCError):

    code = '000050183'
    description = 'STC device send command error'


class STCControlAllDeviceError(STCError):

    code = '000050185'
    description = 'STC control all device error'


class STCControlAllProtocolError(STCError):

    code = '000050186'
    description = 'STC control all protocol error'

class STCBGPConfigError(STCError):

    code = '000050200'
    description = 'STC BGP config error'

class STCBGPRouteConfigError(STCError):

    code = '000050201'
    description = 'STC BGP route config error'

class STCBGPControlError(STCError):

    code = '000050202'
    description = 'STC BGP control error'

class STCBGPInfoError(STCError):

    code = '000050203'
    description = 'STC BGP Info error'

class STCBGPRouteGeneratorError(STCError):

    code = '000050204'
    description = 'STC BGP route Generator error'

class STCOSPFConfigError(STCError):

    code = '000050210'
    description = 'STC OSPF config error'

class STCOSPFTopoRouteConfigError(STCError):

    code = '000050211'
    description = 'STC OSPF topology route config error'

class STCOSPFLSAConfigError(STCError):

    code = '000050212'
    description = 'STC OSPF lsa config error'


class STCConfigureISISError(STCError):

    code = '00050220'
    description = 'STC configure isis error'


class STCControlISISError(STCError):

    code = '00050221'
    description = 'STC control isis error'


class STCConfigureISISTopologyRouteError(STCError):

    code = '00050222'
    description = 'STC configure isis topology route error'


class STCConfigureISISLspGeneratorError(STCError):

    code = '00050223'
    description = 'STC configure isis lsp generator error'


class STCGetISISInfoError(STCError):

    code = '00050224'
    description = 'STC get ISIS information error'

class STCLoadConfigError(STCError):

    code = '000050187'
    description = 'STC load config file error'