#ifndef _DAIG_ETHERNET_PHY_H_
#define _DAIG_ETHERNET_PHY_H_

DIAG_CODE ethernet_phy_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE ethernet_phy_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_phy_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_phy_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_phy_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_phy_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_phy_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_phy_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

extern DIAG_CODE check_mac_address(IO_DATA *pio_data);


DIAGS_NODE diag_basic_ethernet_phy_menu[]={
{'0', NULL, "Ethernet Phy Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "enp01", "Get PHY MAC\0", get_param_get_phy_mac, run_get_phy_mac, YES, YES, YES, get_phy_mac_uid_handle},
{'0', "enp02", "Set PHY MAC\0", get_param_set_phy_mac, run_set_phy_mac, YES, YES, YES, set_phy_mac_uid_handle}
};

#define SIZE_ETHERNET_PHY_MENU (sizeof diag_basic_ethernet_phy_menu / sizeof(DIAGS_NODE))

#endif

