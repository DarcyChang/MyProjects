__author__ = 'glivermo'

import cafe
from cafe.core.db import teststep
from stp.equipment.calix.e7 import E7ApiClass

# ##################################################################################################################
# Library calls of commonly used combinations of e7 commands
# ##################################################################################################################

# def send(session, cmd, timeout=3, prompt=None):
#     # TODO Needs to be expanded to perform send to other session types
#     # command return tuple of (prompt index, prompt regexp object, response)
#     idx, prompt, resp = session.command(cmd, timeout=timeout)
#     if idx < 0:
#         cafe.Checkpoint().fail("prompt is not found")
#     return resp


def lib_create_nl2nlringxconn(p_description, p_xconna_sess, p_xconna_int, p_xconnb_sess, p_xconnb_int, p_tlsvlan,
                              p_nativevlan, p_mirror=False):
    """
    Description:
        Create a Xconn pipe between two interfaces.  Refer to Xconnect documented for additional detail.
        Characteristics are as follows:
            xconnect between two interfaces build via TLS pipes
            RSTP tunneled
            LACP tunneled
            trust enabled
            mtu 9000
            all other values are default
    Args:
        p_name: X Connect pipe label
        p_xconna: equipment instance session of "from" of pipe to build
        p_xconnb: equipment instance session of "to" of pipe to build
        p_tlsvlan: Unique VLAN for TLS portion of pipe
        p_nativevlan:
        p_inta: EndPoint interface of XConnA
        p_intb: EndPoint interface of XConnB
        p_mirror: Enable means mirror is enabled and should be removed
    Returns:
        True if no failures encountered in function.  False if at least one error was encountered.  
    """
    # Initialize global checkpoint returned.  It takes only one failure to fail entire function.  Return is used 
    # do to function being used outside a test case.
    checkpoint = True
    
    # Build Side A of connection - destination
    if p_mirror:
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, description=p_description, 
                                            split_horizon_fwd="enabled",
                                            bpdu_guard="enabled", mtu="9000")):
            checkpoint = False
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, role="trunk")):
            checkpoint = False
        if not (p_xconna_sess.enable_eth_port(eth_port=p_xconna_int)):
            checkpoint = False
        if not (p_xconna_sess.enable_interface(interface=p_xconna_int)):
            checkpoint = False
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, native_vlan=p_nativevlan)):
            checkpoint = False
    else:
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, description=p_description, 
                                            split_horizon_fwd="disabled",
                                            bpdu_guard="disabled", mtu="9000")):
            checkpoint = False
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, role="edge")):
            checkpoint = False
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, native_vlan=p_nativevlan)):
            checkpoint = False
        if not (p_xconna_sess.create_tag_action(tag_action=None, vlan=p_tlsvlan, interface=p_xconna_int)):
            checkpoint = False
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, rstp_active="tunneled")):
            checkpoint = False
        if not (p_xconna_sess.set_interface(interface=p_xconna_int, lacp_tunnel="enabled")):
            checkpoint = False
        if not (p_xconna_sess.enable_eth_port(eth_port=p_xconna_int)):
            checkpoint = False
        if not (p_xconna_sess.enable_interface(interface=p_xconna_int)):
            checkpoint = False

    #Build Side B of connection - source
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, description=p_description, split_horizon_fwd="disabled",
                                    bpdu_guard="disabled", mtu="9000")):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, role="edge")):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, native_vlan=p_nativevlan)):
        checkpoint = False
    if not (p_xconnb_sess.create_tag_action(tag_action=None, vlan=p_tlsvlan, interface=p_xconnb_int)):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, rstp_active="tunneled")):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, lacp_tunnel="enabled")):
        checkpoint = False
    if not (p_xconnb_sess.enable_eth_port(eth_port=p_xconnb_int)):
        checkpoint = False
    if not (p_xconnb_sess.enable_interface(interface=p_xconnb_int)):
        checkpoint = False

    # If Mirroring is enabled add mirroring
    if p_mirror:
        if not (p_xconnb_sess.create_eth_mirror(dest_eth_port=p_xconna_int)):
            checkpoint = False
        if not (p_xconnb_sess.add_eth_port_to_eth_mirror(dest_eth_port=p_xconna_int)):
            checkpoint = False


@teststep("lib delete nl2nlringxconn")
def lib_delete_nl2nlringxconn(p_description, p_xconna_sess, p_xconna_int, p_xconnb_sess, p_xconnb_int, p_tlsvlan,
                              p_nativevlan, p_mirror=False):
    """
    Description:
        Delete a Xconn pipe between two interfaces.  Refer to Xconnect documented for additional detail.
        Characteristics are as follows:
            xconnect between two interfaces build via TLS pipes
            RSTP tunneled
            LACP tunneled
            trust enabled
            mtu 9000
            all other values are default
    Args:
        p_name: X Connect pipe label
        p_xconna: equipment instance session of "destination" of pipe to build
        p_xconnb: equipment instance session of "source" of pipe to build
        p_tlsvlan: Unique VLAN for TLS portion of pipe
        p_nativevlan:
        p_inta: EndPoint interface of XConnA
        p_intb: EndPoint interface of XConnB
        p_mirror: Enable means mirror is enabled and should be removed
    Returns:
        dictionary: success: true or false, errmsg: none or text with brief failure description
    """
    # Initialize global checkpoint returned.  It takes only one failure to fail entire function.  Return is used 
    # do to function being used outside a test case.
    checkpoint = True
      
    # Remove the port mirror if it exists
    if p_mirror:
        if not (p_xconnb_sess.add_eth_port_to_eth_mirror(dest_eth_port=p_xconna_int)):
            checkpoint = False
            
    # Tear Down Side A - destination
    if not (p_xconna_sess.disable_eth_port(eth_port=p_xconna_int)):
        checkpoint = False
    if not (p_xconna_sess.disable_interface(interface=p_xconna_int)):
        checkpoint = False
    if not (p_xconna_sess.set_interface(interface=p_xconna_int, lacp_tunnel="disabled")):
        checkpoint = False
    if not (p_xconna_sess.set_interface(interface=p_xconna_int, rstp_active="disabled")):
        checkpoint = False
    if not (p_xconna_sess.set_interface(interface=p_xconna_int, description="", native_vlan=p_nativevlan)):
        checkpoint = False
    if not (p_xconna_sess.set_interface(interface=p_xconna_int, rstp_active="disabled")):
        checkpoint = False
        
    # Tear Down Side B - source
    if not (p_xconnb_sess.disable_eth_port(eth_port=p_xconnb_int)):
        checkpoint = False
    if not (p_xconnb_sess.disable_interface(interface=p_xconnb_int)):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, lacp_tunnel="disabled")):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, rstp_active="disabled")):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, description="", native_vlan=p_nativevlan)):
        checkpoint = False
    if not (p_xconnb_sess.set_interface(interface=p_xconnb_int, rstp_active="disabled")):
        checkpoint = False        

    return checkpoint