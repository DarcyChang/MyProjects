__author__ = 'gliverm'

from cafe.core.db import teststep
from cafe.core.logger import CLogger as Logger
from cafe.core.signals import E7_SESSION_ERROR
from cafe.resp.response_map import ResponseMap
from cafe.resp.response_map import regex1
import cafe
import time


logger = Logger(__name__)
debug = logger.debug
error = logger.error

# ##################################################################################################################
# Temporary work arounds for cafe calls
# ##################################################################################################################


def gliverm_parse_key_value_pairs(r, start_line=0):
    """
    Description:
        parse response as key value pairs replacing Cafe call to allow for E7 separators
    Args:
        start_line (int): where to start parsing
    Returns:
        Param: dictionary of key value pairs
    """
    d = {}
    lines = str.split(r, '\r')[start_line:]
    for l in lines:
        i = l.strip()
        k, v = regex1(i, r"(.+):(.+)")
        if (type(k) == str) and (type(v) == str):
            k = k.strip()
            v = v.strip()
        if k:
            d[k] = v
    return d


class E7Exception(Exception):
    def __init__(self, msg=""):
        logger.exception(msg, signal=E7_SESSION_ERROR)


class E7BaseClass(object):
    """
    Class: CalixE7Base is base class of E7.  E7 defines all E-Series sharing the same CLI structure.
    """
    def __init__(self, session, session_type="telnet", release=None, eq_type='E7'):
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


class E7ApiClass(E7BaseClass):
    """
    APIs for E7.
    """
    # ##################################################################################################################
    # Internals to class
    # ##################################################################################################################

    def _send(self, cmd="", timeout=3):
        """
        Description:
            (Internal use): Write a command to the object returning the response.
        """
        self.session.write(cmd)
        # return tuple (prompt index, <prompt re match object>, text)
        r = self.session.expect_prompt(timeout=timeout)
        if r[0] < -1:
            return {"prompt": None, "response": r[2]}
        else:
            return {"prompt": r[1].group(), "response": r[2]}

    # ##################################################################################################################
    # External single commands to class
    # ##################################################################################################################

    def add_eth_port_to_eth_mirror(self, eth_port, mirror_type=None, exp="success"):
        """
        Description:
            Add Ethernet port to an already created etherport mirror.
        Args:
            None
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['add eth-port ', eth_port])
        if mirror_type:
            command_list.extend(['type', mirror_type])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 add eth-port to eth-mirror",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def add_eth_svc(self, name, totype=None, interface=None, bw_profile=None, svc_tag_action=None, outer_vlan=None, inner_vlan=None,
                    mcast_profile=None, description=None, pon_cos=None, us_cir_override=None,
                    us_pir_override=None, ds_pir_override=None, admin_state=None, exp="success"):
        """
        Description:
            Add Ethernet service to an interface or port. ONT Port only plumbed through but easy to others.
        Args:
            name(str)(required) - Name of Ethernet service
            totype(str)(optional) - Access Ethernet type to work on.  Valid options are:
                "dsl-bond-interface":    DSL bonded interface
                "interface":             DSL interface
                "ont-port":              ONT port
            interface(str)(optional) - Interface to work on.  Valid options:
                <ONT Eth. Port>            - <ont-id/ont-port>  In ont-port: f=fast-eth, g=gig-eth, h=hpna-eth,
                                             G=res-gw, F=full-bridge.  Example: 10001/g1
            bw_profile(str)(optional) - Name of bw-profile
            svc_tag_action(str)(optional) - Name of service tag-action
            outer_vlan(str)(optional) - Outer tag VLAN ID
            inner_vlan(str)(optional) - Inner tag VLAN ID
            mcast_profile(str)(optional) - name of multicast profile OR "none" for No multicast profile
            description(str)(optional) - Description of Ethernet service
            pon_cos(str)(optional) - PON US COS. Valid Options:
                derived                    - Derive PON US COS value.
                fixed                      - Legacy mode for pre-2.2 services.
                user-1                     - user defined PON US COS.
                user-2                     - user defined PON US COS.
                user-3                     - user defined PON US COS.
                user-4                     - user defined PON US COS.
                cos-1                      - system defined PON US COS.
                cos-2                      - system defined PON US COS.
                cos-3                      - system defined PON US COS.
                cos-4                      - system defined PON US COS.
            us_cir_override(str)(optional) - Upstream committed information rate.  Valid options:
                <0-2048Kb/s, 0-1000Mb/s,   - Upstream committed information rate (Kb/s in 64K
                1Gb/s>                       increments. Use "m" or "g" suffix for Mb/s or
                                             Gb/s), or:
                none                       - Do not override Bw Profile attribute
            us_pir_override(str)(optional) - Upstream peak information rate. Valid options:
                <0-2048Kb/s, 0-1000Mb/s,   - Upstream committed information rate (Kb/s in 64K
                1Gb/s>                       increments. Use "m" or "g" suffix for Mb/s or
                                             Gb/s), or:
                none                       - Do not override Bw Profile attribute
            ds_pir_override(str)(optional) - Downstream peak information rate. Valid options:
                <0-2048Kb/s, 0-1000Mb/s,   - Downstream committed information rate (Kb/s in 64K
                1Gb/s>                       increments. Use "m" or "g" suffix for Mb/s or
                                             Gb/s), or:
                none                       - Do not override Bw Profile attribute
            admin_state(str)(optional) - Admin state of service (enabled/disabled)
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        # TODO: Should also return rule index
        command_list = []
        command_list.extend(['add eth-svc'])
        if name:
            command_list.extend([name])
        if totype:
            command_list.extend(["to-" + totype])
        if interface:
            command_list.extend([interface])
        if bw_profile:
            command_list.extend(['bw-profile', bw_profile])
        if svc_tag_action:
            command_list.extend(['svc-tag-action', svc_tag_action])
        if outer_vlan:
            command_list.extend(['outer-vlan', outer_vlan])
        if inner_vlan:
            command_list.extend(['inner-vlan', inner_vlan])
        if mcast_profile:
            command_list.extend(['mcast-profile', mcast_profile])
        if description:
            command_list.extend(['description', description])
        if pon_cos:
            command_list.extend(['pon-cos', pon_cos])
        if us_cir_override:
            command_list.extend(['us-cir-override', us_cir_override])
        if us_pir_override:
            command_list.extend(['us-pir-override', us_pir_override])
        if ds_pir_override:
            command_list.extend(['ds-pir-override', ds_pir_override])
        if admin_state:
            command_list.extend(['admin-state', admin_state])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 add eth-svc",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def add_interface(self, interface, to_vlan=None, exp="success"):
        """
        Description:
            Disable interface.
        Args:
            inteface(str)(optional) - <card/port> or <LAG name>  In port: v=vdsl, g=gig-eth, x=10gig-eth. Examples:
                2/g1, 2/g1-2/g4, my-lag
            to_vlan(str)(optional) - VLAN name, ID or range (2 IDs separated by a "-")
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['add interface'])
        if interface:
            command_list.extend([interface])
        if to_vlan:
            command_list.extend(['to-vlan', to_vlan])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 add interface",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def add_tagged_rule(self, to_svc_match_list=None, vlan=None, p_bit=None, exp="success"):
        """
        Description:
            Add tagged-rule to service match-list.
        Args:
            to_svc_match_list(str)(optional) - Name of service match-list
            vlan(str)(optional) - VLAN ID of outer tag OR "ignore" to ignore tag
            p_bit(str)(optional) - p-bit value of outer tag or "any" to Match any p-bit
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        # TODO: Should also return rule index
        command_list = []
        command_list.extend(['add tagged-rule'])
        if to_svc_match_list:
            command_list.extend(['to-svc-match-list', to_svc_match_list])
        if vlan:
            command_list.extend(['vlan', vlan])
        if p_bit:
            command_list.extend(['p-bit', p_bit])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 add tagged rule",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def add_untagged_rule(self, to_svc_match_list=None, src_mac=None, src_mac_mask=None, ethertype=None,
                          any=None, exp="success"):
        """
        Description:
            Add tagged-rule to service match-list.  Did not add vpi or vci attributes.
        Args:
            to_svc_match_list(str)(optional) - Name of service match-list
            src_mac(str)(optional) - Source MAC address <x:x:x:x:x:x> OR 'ignore'
            src_mac_mask(str)(optional) - Source MAC mask <x:x:x:x:x:x> OR 'none' for no MAC mask OR 'oui' with
                Mask OUI fields (FF:FF:FF:00:00:00)
            ethertype(str)(optional) - valid options: "any" = any Ethertype, "pppoe" = PPPoE frames,
                "arp" = ARP frames, "ipv4" = IPv4 frames, "ipv6" = IPv6 frames
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        # TODO: Should also return rule index
        command_list = []
        command_list.extend(['add untagged-rule'])
        if to_svc_match_list:
            command_list.extend(['to-svc-match-list', to_svc_match_list])
        if src_mac:
            command_list.extend(['src-mac', src_mac])
        if src_mac_mask:
            command_list.extend(['src-mac-mask', src_mac_mask])
        if ethertype:
            command_list.extend(['ethertype', ethertype])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 add untagged rule",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def add_untagged_rule(self, to_svc_match_list=None, src_mac=None, src_mac_mask=None, ethertype=None,
                          any=None, exp="success"):
        """
        Description:
            Add tagged-rule to service match-list.  Did not add vpi or vci attributes.
        Args:
            to_svc_match_list(str)(optional) - Name of service match-list
            src_mac(str)(optional) - Source MAC address <x:x:x:x:x:x> OR 'ignore'
            src_mac_mask(str)(optional) - Source MAC mask <x:x:x:x:x:x> OR 'none' for no MAC mask OR 'oui' with
                Mask OUI fields (FF:FF:FF:00:00:00)
            ethertype(str)(optional) - valid options: "any" = any Ethertype, "pppoe" = PPPoE frames,
                "arp" = ARP frames, "ipv4" = IPv4 frames, "ipv6" = IPv6 frames
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        # TODO: Should also return rule index
        command_list = []
        command_list.extend(['add untagged-rule'])
        if to_svc_match_list:
            command_list.extend(['to-svc-match-list', to_svc_match_list])
        if src_mac:
            command_list.extend(['src-mac', src_mac])
        if src_mac_mask:
            command_list.extend(['src-mac-mask', src_mac_mask])
        if ethertype:
            command_list.extend(['ethertype', ethertype])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 add untagged rule",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def create_bw_profile(self, name, upstream_cir=None, upstream_pir=None, downstream_pir=None, upstream_cbs=None,
                          upstream_pbs=None, downstream_pbs=None, exp="success"):
        """
        Description:
            Create bandwidth profile.
        Args:
            name(str)(required) - Name of bandwidth profile
            upstream_cir(str)(optional) - Upstream committed information rate (Kb/s in 64K
                increments. Use "m" or "g" suffix for Mb/s or Gb/s)
            upstream_pir(str)(optional) - Upstream peak information rate (Kb/s in 64K
                increments. Use "m" or "g" suffix for Mb/s or Gb/s)
            downstream_pir(str)(optional) - downstream peak information rate (Kb/s in 64K
                increments. Use "m" or "g" suffix for Mb/s or Gb/s)
            upstream_cbs(str)(optional) - upstream committed burst size (kilobytes, or use
                "m" suffix for megabytes)
            upstream_pbs(str)(optional) - upstream peak burst size (kilobytes, or use "m"
                suffix for megabytes)
            downstream_bps(str)(optional) - downstream peak burst size (kilobytes, or use "m"
                suffix for megabytes)
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['create bw-profile'])
        if name:
            command_list.extend([name])
        if upstream_cir:
            command_list.extend(['upstream-cir', upstream_cir])
        if upstream_pir:
            command_list.extend(['upstream-pir', upstream_pir])
        if downstream_pir:
            command_list.extend(['downstream-pir', downstream_pir])
        if upstream_cbs:
            command_list.extend(['upstream-cbs', upstream_cbs])
        if upstream_pbs:
            command_list.extend(['upstream-pbs', upstream_pbs])
        if downstream_pbs:
            command_list.extend(['downstream-pbs', downstream_pbs])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 create bw-profile",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def create_eth_mirror(self, dest_eth_port=None, admin_state=None, exp="success"):
        """
        Description:
            Create Ethernet mirror.
        Args:
            None
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['create eth-mirror'])
        if dest_eth_port:
            command_list.extend(['dest-eth-port', dest_eth_port])
        if admin_state:
            command_list.extend(['admin-state', admin_state])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 create eth-mirror",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def create_svc_match(self, name, exp="success"):
        """
        Description:
            create service match-list
        Args:
            name(str)(optional) - Name of service match-list
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        result = {}
        command_str = "create svc-match " + name
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 create service match-list",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def create_svc_tag_action(self, name, tatype=None, outer=None, inner=None, svc_match_list=None,
                              ethertype=None, use_p_bit=None, derive_p_bit=None, untagged_p_bit=None,
                              use_inner_p_bit=None, exp="success"):
        """
        Description:
            Create service tag action
        Args:
            name(str)(required) - Name of service tag-action
            tatype(str)(optional) - type of service tag-action to create (add-2-tags, add-and-change, add-tag, change-tag)
            outer(str)(optional) - VLAN name or ID for new outer tag
            inner(str)(optional) - VLAN name or ID for new inner tag
            svc_match_list(str)(optional) - Name of service match-list
            ethertype(str)(optional) - Ethertype to use in outer tag (0x8100, 0x88a8, 0x9100, PPPoE, arp, ipv4, ipv6)
            use-p-bit(str)(optional) - Use a specific p-bit value in output tag. <0-7>  Use a specific p-bit value in
                output tag  OR "copy" to copy p-bit value from matched tag
            derive_p_bit(str)(optional) - Derive p-bit from a CoS Queue or layer-3 priority map.  Valid options are:
                "cos-1"     Use low p-bit from CoS 1.
                "cos-2"     Use low p-bit from CoS 2.
                "cos-3"     Use low p-bit from CoS 3.
                "cos-4"     Use low p-bit from CoS 4.
                "l3-prio"   Map a layer-3 priority into a pbit, using interface DSCP or IP precedence map.
            untagged_p_bit(str)(optional) - <0-7> When promoting, p-bit value for untagged frames.(default: 0)
            use_inner_p_bit(str)(optional) - <0-7> OR "preserve" OR "same-as-outer"  Use specific p-bit value in inner
                tag OR preserve p-bit value from matched tag OR same p-bit treatment as outer tag
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['create svc-tag-action'])
        if name:
            command_list.extend([name])
        if tatype:
            command_list.extend(['type', tatype])
        if outer:
            command_list.extend(['outer', outer])
        if inner:
            command_list.extend(['inner', inner])
        if svc_match_list:
            command_list.extend(['svc-match-list', svc_match_list])
        if ethertype:
            command_list.extend(['ethertype', ethertype])
        if use_p_bit:
            command_list.extend(['use-p-bit', use_p_bit])
        if derive_p_bit:
            command_list.extend(['derive-p-bit', derive_p_bit])
        if untagged_p_bit:
            command_list.extend(['untagged-p-bit', untagged_p_bit])
        if use_inner_p_bit:
            command_list.extend(['use-inner-p-bit', use_inner_p_bit])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 create service tag action",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def create_tag_action(self, interface=None, tag_action=None, vlan=None, match_pbit=None, match_tag=None,
                          expresp=None):
        """
        Description:
            Set the interface attributes.  Not all interface attributes have been added.
        Args:
            None
        Returns:
            True for pass, and False for fail.  To allow for use outside of test case.
        """
        command_list = []
        command_list.extend(['create tag-action'])
        if tag_action:
            command_list.extend(['tag-action', tag_action])
        if vlan:
            command_list.extend(['vlan', vlan])
        if interface:
            command_list.extend([interface])
        if match_pbit:
            command_list.extend(['match-pbit', match_pbit])
        if match_tag:
            command_list.extend(['match_tag', match_tag])

        command_str = ' '.join(command_list)
        resp = self.send(cmd=command_str)['response']
        if expresp is not None:
            checkpoint = cafe.Checkpoint(resp).contains(exp="success: Create tag-action",
                                                        title="create tag-action with default response",
                                                        pos_msg="Expected response found",
                                                        neg_msg="Expected response not found")
        else:
            checkpoint = cafe.Checkpoint(resp).contains(exp=expresp,
                                                        title="create tag-action with argument response",
                                                        pos_msg="Expected response found",
                                                        neg_msg="Expected response not found")
        # TODO: Think about always returning a dictionary so returns can easily be modified to return additional\
        #  info such as tag number in this case

        return checkpoint

    def create_vlan(self, vlan=None, name=None, mac_forced_forwarding=None, ip_source_verify=None, dhcp_snooping=None,
                    igmp_mode=None, exp="success"):
        """
        Description:
            Disable interface.
        Args:
            vlan(str)(optional) - VLAN ID or range (2 IDs separated by a "-")
            name(str)(optional) - Name of VLAN
            mac_forced_forwarding(str)(optional) - MAC forced forwarding (PON/DSL ports only)
            ip_source_verify(str)(optional) - Enable or disable IP source verificaiton (PON/DSL ports only)
            igmp_mode(str)(optional) - IGMP mode for VLAN
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['create vlan'])
        if vlan:
            command_list.extend([vlan])
        if name:
            command_list.extend(['name', name])
        if mac_forced_forwarding:
            command_list.extend(['mac-forced-forwarding', mac_forced_forwarding])
        if ip_source_verify:
            command_list.extend(['ip-source-verify', ip_source_verify])
        if dhcp_snooping:
            command_list.extend(['dhcp-snooping', dhcp_snooping])
        if igmp_mode:
            command_list.extend(['igmp-mode', igmp_mode])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 create vlan",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def delete_bw_profile(self, name, exp="success"):
        """
        Description:
            Delete bandwidth profile from system
        Args:
            name(str)(required) - Name of bandwidth profile
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "delete bw-profile " + name
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 delete bw-profile",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def delete_eth_mirror(self, exp="success"):
        """
        Description:
            Delete Ethernet mirror.
        Args:
            None
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "delete eth-mirror"
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 delete eth-mirror",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def delete_svc_match(self, name, exp="success"):
        """
        Description:
            Delete service match-list
        Args:
            name(str)(required) - Name of service match-list
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "delete svc-match " + name
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 delete service match-list",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def delete_svc_tag_action(self, name, exp="success"):
        """
        Description:
            Delete service tag action
        Args:
            name(str)(required) - Name of service tag-action
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "delete svc-tag-action " + name
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 delete service tag-action",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def delete_vlan(self, vlan, exp="success"):
        """
        Description:
            Delete VLAN from system.
        Args:
            eth_port(str)(optional) - <shelf/card/eth-port>
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "delete vlan " + vlan
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 delete vlan",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def disable_eth_port(self, eth_port, exp="success"):
        """
        Description:
            Disable ethernet port.
        Args:
            eth_port(str)(optional) - <shelf/card/eth-port>
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "disable eth-port " + eth_port
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 disable eth-port",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def disable_interface(self, interface, exp="success"):
        """
        Description:
            Disable interface.
        Args:
            interface(str)(optional) - <shelf/card/eth-port>
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "disable interface " + interface
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 disable interface",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def enable_eth_port(self, eth_port, exp="success"):
        """
        Description:
            Enable ethernet port.
        Args:
            eth_port(str)(optional) - <shelf/card/eth-port>
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "enable eth-port " + eth_port
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 enable eth-port",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def enable_interface(self, interface, exp="success"):
        """
        Description:
            Enable interface.
        Args:
            interface(str)(optional) - <shelf/card/eth-port>
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_str = "enable interface " + interface
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 enable interface",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def reconnect(self):
        """Reconnect to e7 node

        """
        param = cafe.get_test_param()
        time.sleep(10)
        try:
            param.e7_sess.session.close_connection()
            param.e7_sess.reconnect()
            param.e7_sess.login()
        except:
            raise RuntimeError("not able to reconnect e7")

    def remove_eth_port_to_eth_mirror(self, eth_port, exp="success"):
        """
        Description:
            Remove Ethernet port to an already created etherport mirror.
        Args:
            None
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['remove eth-port ', eth_port, ' from-eth-mirror'])
        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 remove eth-port from eth-mirror",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def login(self):
        """
        Description:
            login to e7 cli
        """
        self.session.login()
        # return tuple (prompt index, <prompt re match object>, text)

        self.session.write("set session timeout disable pager disable")
        r = self.session.expect_prompt()
        # print('r 0 : ',r[0])
        # print('r 2 : ',r[2])
        if r[0] < 0:
            raise E7Exception("E7 login failed. session(%s)" % self.session.sid)
        else:
            debug("E7 session open. session(%s)" % self.session.sid)

    def remove_eth_svc(self, name, fromtype=None, interface=None, exp="success"):
        """
        Description:
            Disable interface.
        Args:
            name(str)(required) - Name of Ethernet service
            totype(str)(optional) - Access Ethernet type to work on.  Valid options are:
                "dsl-bond-interface":    DSL bonded interface
                "interface":             DSL interface
                "ont-port":              ONT port
            interface(str)(optional) - Interface to work on.  Valid options:
                <ONT Eth. Port>            - <ont-id/ont-port>  In ont-port: f=fast-eth, g=gig-eth, h=hpna-eth,
                                             G=res-gw, F=full-bridge.  Example: 10001/g1

        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['remove eth-svc'])
        if name:
            command_list.extend([name])
        if fromtype:
            command_list.extend(["from-" + fromtype])
        if interface:
            command_list.extend([interface])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 remove eth-svc",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def remove_interface(self, interface, from_vlan=None, exp="success"):
        """
        Description:
            Disable interface.
        Args:
            inteface(str)(optional) - <card/port> or <LAG name>  In port: v=vdsl, g=gig-eth, x=10gig-eth. Examples:
                2/g1, 2/g1-2/g4, my-lag
            to_vlan(str)(optional) - VLAN name, ID or range (2 IDs separated by a "-")
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['remove interface'])
        if interface:
            command_list.extend([interface])
        if from_vlan:
            command_list.extend(['from-vlan', from_vlan])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 remove interface",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def remove_tagged_rule(self, tagged_rule=None, from_svc_match_list=None, exp="success"):
        """
        Description:
            Remove tagged rule from service match-list
        Args:
            tagged_rule(int)(optional) - Index of rule in service match-list
            from_svc_match_list(str)(optional) - Name of service match-list
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['remove tagged-rule'])
        if tagged_rule:
            command_list.extend([tagged_rule])
        if from_svc_match_list:
            command_list.extend(['from-svc-match-list', from_svc_match_list])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 remove tagged rule",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)

    def remove_untagged_rule(self, untagged_rule=None, from_svc_match_list=None, exp="success"):
        """
        Description:
            Remove Untagged rule from service match-list
        Args:
            untagged_rule(int)(optional) - Index of rule in service match-list
            from_svc_match_list(str)(optional) - Name of service match-list
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['remove untagged-rule'])
        if untagged_rule:
            command_list.extend([untagged_rule])
        if from_svc_match_list:
            command_list.extend(['from-svc-match-list', from_svc_match_list])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 remove untagged rule",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def send(self, cmd="", timeout=10):
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

    def set_interface(self, interface, name=None, role=None, description=None, native_vlan=None,
                      rstp_active=None, bpdu_guard=None, split_horizon_fwd=None, lacp_tunnel=None,
                      trusted=None, admin_state=None, mtu=None, exp="success"):
        """
        Description:
            Set the interface attributes.  Not all interface atributes have been added.
        Args:
            interface(str)(required) - <card/eth-port>
            name(str)(optional) - Name of this interface
            role(str)(optional) - Role of this interface
            description(str)(optional) - Description of this interface
            native_vlan(int)(optional) - Native VLAN for user traffic on this interface
            rstp_active(str)(optional) - Interface is running RSTP
            bpdu_guard(str)(optional) - Enable or disable RSTP BPDU guard mode
            split_horizon_fwd(str)(optional) - Enable or disable split-horizon forwarding on this interface
            lacp_tunnel(str)(optional) - Tunnel or drop LACP packets on this interface
            trusted(str)(optional) - Interface is trusted source of DHCP option 82 data
            admin_state(str)(optional) - Admin state of port
            mtu(int)(optional) - Maximum Transmission Unit size (bytes)
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['set interface'])
        if interface:
            command_list.extend([interface])
        if name:
            command_list.extend(['name', name])
        if role:
            command_list.extend(['role', role])
        if description:
            command_list.extend(['description', description])
        if native_vlan:
            command_list.extend(['native-vlan', native_vlan])
        if rstp_active:
            command_list.extend(['rstp-active', rstp_active])
        if bpdu_guard:
            command_list.extend(['bpdu-guard', bpdu_guard])
        if split_horizon_fwd:
            command_list.extend(['split-horizon-fwd', split_horizon_fwd])
        if lacp_tunnel:
            command_list.extend(['lacp-tunnel', lacp_tunnel])
        if trusted:
            command_list.extend(['trusted', trusted])
        if admin_state:
            command_list.extend(['admin-state', admin_state])
        if mtu:
            command_list.extend(['mtu', mtu])

        command_str = ' '.join(command_list)

        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 set interface",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def set_vlan(self, vlan=None, name=None, mac_forced_forwarding=None, ip_source_verify=None, dhcp_snooping=None,
                    igmp_mode=None, exp="success"):
        """
        Description:
            Set VLAN characteristic options.
        Args:
            vlan(str)(optional) - VLAN ID or range (2 IDs separated by a "-")
            name(str)(optional) - Name of VLAN
            mac_forced_forwarding(str)(optional) - MAC forced forwarding (PON/DSL ports only)
            ip_source_verify(str)(optional) - Enable or disable IP source verificaiton (PON/DSL ports only)
            igmp_mode(str)(optional) - IGMP mode for VLAN
        Returns:
            Dictionary:
                'response' : response string received as a result of applying command
                'checkpoint' : boolean result of checkpoint on expected results
        """
        command_list = []
        command_list.extend(['create vlan'])
        if vlan:
            command_list.extend([vlan])
        if name:
            command_list.extend(['name', name])
        if mac_forced_forwarding:
            command_list.extend(['mac-forced-forwarding', mac_forced_forwarding])
        if ip_source_verify:
            command_list.extend(['ip-source-verify', ip_source_verify])
        if dhcp_snooping:
            command_list.extend(['dhcp-snooping', dhcp_snooping])
        if igmp_mode:
            command_list.extend(['igmp-mode', igmp_mode])

        command_str = ' '.join(command_list)
        result = {'response': self.send(cmd=command_str)['response']}
        result['checkpoint'] = cafe.Checkpoint(result['response']).contains(exp=exp,
                                                        title="E7 set vlan",
                                                        pos_msg="success : command = " + command_str,
                                                        neg_msg="fail : command = " + command_str)
        return result

    def show_system(self):
        """
        Description:
            obtain show system information from system
        Args:
            None
        Returns:
            dictionary of version information based on E-Series sub type
        """

        r = self._send(cmd='show system')['response']
        # resp = ResponseMap(r).parse_key_value_pairs()
        # TODO Temporary work around to Cafe version of parse_key_value_pairs need to replace with usage change
        resp = gliverm_parse_key_value_pairs(r)

        return resp

    def show_tag_actions(self, tag_action=None):
        """
        Description:
            obtain show version information from system
        Returns:
            dictionary of version information based on E-Series sub type
        """

        # XConn1>show tag
        # Index Interface       Match                |  Tag Action
        # ----- --------------- -------------------  |  -------------------------
        # 1     2/g24           all                  |  add          : VLAN 100
        #
        # 1 tag action found.
        # XConn1>show tag-action 1
        # Index Interface       Match                |  Tag Action
        # ----- --------------- -------------------  |  -------------------------
        # 1     2/g24           all                  |  add          : VLAN 100
        # XConn1>

        command_list = []
        command_list.extend(['show tag-action'])
        if tag_action:
            command_list.extend([tag_action])
        command_str = ' '.join(command_list)
        resp = self.send(cmd=command_str)['response']
        pattern = "(\d+)\s\s+(.+)\s\s+(.+)\s\s+|\s\s+(.+)\s\s+:\s\s+VLAN(\d+)"
        mt = resp.table_match(pattern)
        print("mt : ", mt)

        return resp

    def show_version(self):
        """
        Description:
            obtain show version information from system
        Returns:
            dictionary of version information based on E-Series sub type
        """

        if self.eq_type[0:2] == "E7":
            # Multi card system
            r = self._send(cmd='show version')['response']
            # Return dictionary of table rows - Cafe title parsing does not work for this command
            resp = ResponseMap(r).parse_table(start_line=4,
                                              auto_title=False,
                                              title=['Card', 'Present', 'Running_Vers.', 'Committed"Vers.',
                                                     'Alt._Vers.'])
        else:
            # Single card system by default: eq_type = E3 or E5
            r = self._send(cmd='show version')['response']
            # TODO Temporary work around to Cafe version of parse_key_value_pairs need to replace with usage change
            # resp = ResponseMap(r).parse_key_value_pairs()
            resp = gliverm_parse_key_value_pairs(r)

        # print('resp : ',resp)

        return resp

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
