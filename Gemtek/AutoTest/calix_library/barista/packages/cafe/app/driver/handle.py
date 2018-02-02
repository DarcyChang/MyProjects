__author__ = 'kelvin'
class Handle(object):
    """
    class for managing the session/driver object handle
    """
    handle_types = [
                    'stream',
                    'port',
                    'ospf',
                    'ospf_lsa',
                    'ospf_topology_route',
                    'igmp_session',
                    'igmp_querier',
                    'igmp_group',
                    'multicast_group',
                    'multicast_source',
                    'dhcp_server',
                    'dhcp_client',
                    'dhcp_client_group',
                    'dhcp_server_v6',
                    'dhcp_client_v6',
                    'dhcp_client_group_v6',
                    'dhcp_client_relay_agent',
                    'pppoe_client',
                    'pppoe_server',
                    'cfm_bridge',
                    'cfm_md_meg',
                    'cfm_mip_mep',
                    'cfm_links',
                    'cfm_vlan',
                    'device',
                    'bgp',
                    'bgp_route',
                    'bgp_route_generator',
                    'isis_router',
                    'isis_topology_route',
                    'isis_lsp_generator'
                    ]

    def __init__(self, ref, value, handle=None, htype="port", neighbor=None):
        self._ref = ref
        self._value = value
        self._handle = handle
        self._neighbor = neighbor

        if not htype.lower() in self.handle_types:
            raise AttributeError('handle type %s is not supported' % htype)

        self._htype = htype.lower()
    @property
    def handle(self):
        return self._handle

    @property
    def ref(self):
        return self._ref

    @property
    def value(self):
        return self._value

    @property
    def handle_type(self):
        return self._htype

    @property
    def neighbor(self):
        return self._neighbor

    def __str__(self):
        return str(self._value)
