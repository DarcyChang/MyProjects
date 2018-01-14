#ifndef _DAIG_SWITCH_H_
#define _DAIG_SWITCH_H_

DIAG_CODE switch_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE switch_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_ethernet_port_link_status(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_ethernet_port_link_status(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_ethernet_port_link_status_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_ethernet_port_loopback_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_ethernet_port_loopback_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE ethernet_port_loopback_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_reset_ethernet_port_config_to_mfg_mode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_reset_ethernet_port_config_to_mfg_mode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE reset_ethernet_port_config_to_mfg_mode_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_reset_ethernet_port_config_to_user_mode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_reset_ethernet_port_config_to_user_mode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE reset_ethernet_port_config_to_user_mode_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_ethernet_port_config(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_ethernet_port_config(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_ethernet_port_config_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_i_connector_loopback_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_i_connector_loopback_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE i_connector_loopback_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_1000_base_t_pattern_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_1000_base_t_pattern_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE daig_1000_base_t_pattern_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_switch_menu[]={
{'0', NULL, "Switch Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "swh01", "Show Ethernet Port Link Status\0", get_param_show_ethernet_port_link_status, run_show_ethernet_port_link_status, YES, YES, YES, show_ethernet_port_link_status_uid_handle},
{'0', "swh02", "Port External Loopback Test\0", get_param_ethernet_port_loopback_test, run_ethernet_port_loopback_test, YES, YES, YES, ethernet_port_loopback_test_uid_handle},
{'0', "swh05", "Reset Ethernet Port Config to MFG Mode\0", get_param_reset_ethernet_port_config_to_mfg_mode, run_reset_ethernet_port_config_to_mfg_mode, YES, YES, YES, reset_ethernet_port_config_to_mfg_mode_uid_handle},
{'0', "swh06", "Reset Ethernet Port Config to USER Mode\0", get_param_reset_ethernet_port_config_to_user_mode, run_reset_ethernet_port_config_to_user_mode, YES, YES, YES, reset_ethernet_port_config_to_user_mode_uid_handle},
{'0', "swh08", "Show Ethernet Port Config\0", get_param_show_ethernet_port_config, run_show_ethernet_port_config, YES, YES, YES, show_ethernet_port_config_uid_handle},
{'0', "swh09", "I-Connector Loopback Test\0", get_param_i_connector_loopback_test, run_i_connector_loopback_test, YES, YES, YES, i_connector_loopback_test_uid_handle},
{'0', "swh10", "1000 Base-T Pattern Test\0", get_param_1000_base_t_pattern_test, run_1000_base_t_pattern_test, YES, YES, YES, daig_1000_base_t_pattern_test_uid_handle}
};

#define SIZE_SWITCH_MENU (sizeof diag_basic_switch_menu / sizeof(DIAGS_NODE))

#endif

