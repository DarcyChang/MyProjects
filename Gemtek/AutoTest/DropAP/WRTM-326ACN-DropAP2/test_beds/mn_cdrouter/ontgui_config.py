__author__ = 'bmelhus'

import cafe
from stp.equipment.calix.ont_gui import ONTGuiApiClass

def conf_tr069(params):
    ont_gui = params['ont_gui']
    ont_ip = params['ontgui']['ont_ip']
    acs_url = params['tr069']['acs_url']
    tr069_uname = params['tr069']['tr069_uname']
    tr069_pword = params['tr069']['tr069_pword']
    tr069_vlan = params['tr069']['tr069_vlan']
    per_intvl = params['tr069']['tr069_period_intvl']

    tr069_setup = ont_gui.tr069_setup(ontip=ont_ip, acs_url=acs_url, uname=tr069_uname, pword=tr069_pword, periodic_inform="True", inform_intvl=per_intvl, tr069_vlan=tr069_vlan, tr069_wan="TR-069_Interface")
    return tr069_setup

def rstr_dflts(params):
    # print("params: " + str(params))
    ont_gui = params['ont_gui']
    ont_ip = params['ontgui']['ont_ip']

    rstr_dflt = ont_gui.restore_dflts(ontip=ont_ip)
    return rstr_dflt

def chk_cfg_dld_cmplt(eut, rg_scenario, params):
    ont_gui = params['ont_gui']
    ont_ip = params['ontgui']['ont_ip']

    dld_chk = ont_gui.chk_dld_cmplt(ontip=ont_ip, eut=eut, scenario=rg_scenario)
    return dld_chk