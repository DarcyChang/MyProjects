#ifndef _DAIG_WLAN_H_
#define _DAIG_WLAN_H_

DIAG_CODE wlan_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE wlan_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_basic_configuration_tool(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_basic_configuration_tool(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE basic_configuration_tool_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_wifi_register_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_wifi_register_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE wifi_register_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_continuous_tx_transmission_tool(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_continuous_tx_transmission_tool(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE continuous_tx_transmission_tool_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_wifi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_wifi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_wifi_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_wifi_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_wifi_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_wifi_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_wifi_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_wifi_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_wifi_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_wifi_country_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_wifi_country_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_wifi_country_code_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_wifi_country_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_wifi_country_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_wifi_country_code_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_wifi_ssid(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_wifi_ssid(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_wifi_ssid_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_wifi_ssid(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_wifi_ssid(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_wifi_ssid_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_wifi_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_wifi_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_wifi_rssi_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_wifi_band(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_wifi_band(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_wifi_band_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_wifi_band(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_wifi_band(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_wifi_band_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_wifi_channel(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_wifi_channel(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_wifi_channel_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_wifi_channel(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_wifi_channel(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_wifi_channel_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_setup_wifi_throughput(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_setup_wifi_throughput(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE setup_wifi_throughput_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

DIAG_CODE get_param_set_wifi_antenna(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_wifi_antenna(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_wifi_antenna_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

DIAG_CODE get_wlan_info(IO_DATA *pio_data, unsigned int index);
DIAG_CODE wireless_ssid(char * ssid_name);
DIAG_CODE get_ssid(char *ssid);
DIAG_CODE wireless_channel(unsigned int channel);
DIAG_CODE get_channel(unsigned int *channel);
DIAG_CODE wireless_device(viod);
DIAG_CODE wireless_interface(void);
DIAG_CODE wireless_tx(unsigned int time);

DIAGS_NODE diag_basic_wlan_menu[]={
{'0', NULL, "WLAN Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "wln01", "Basic configuration tool\0", get_param_basic_configuration_tool, run_basic_configuration_tool, NO, YES, YES, basic_configuration_tool_uid_handle},
{'0', "wln02", "Register test\0", get_param_wifi_register_test, run_wifi_register_test, NO, YES, YES, wifi_register_test_uid_handle},
{'0', "wln03", "Continuous TX transmission tool\0", get_param_continuous_tx_transmission_tool, run_continuous_tx_transmission_tool, NO, YES, YES, continuous_tx_transmission_tool_uid_handle},
{'0', "wln04", "Show WiFi info\0", get_param_show_wifi_info, run_show_wifi_info, NO, YES, YES, show_wifi_info_uid_handle},
{'0', "wln05", "Get WiFi MAC\0", get_param_get_wifi_mac, run_get_wifi_mac, YES, YES, YES, get_wifi_mac_uid_handle},
{'0', "wln06", "Set WiFi MAC\0", get_param_set_wifi_mac, run_set_wifi_mac, YES, YES, YES, set_wifi_mac_uid_handle},
{'0', "wln07", "Get Country Code\0", get_param_get_wifi_country_code, run_get_wifi_country_code, NO, YES, YES, get_wifi_country_code_uid_handle},
{'0', "wln08", "Set Country Code\0", get_param_set_wifi_country_code, run_set_wifi_country_code, NO, YES, YES, set_wifi_country_code_uid_handle},
{'0', "wln09", "Get SSID\0", get_param_get_wifi_ssid, run_get_wifi_ssid, NO, YES, YES, get_wifi_ssid_uid_handle},
{'0', "wln10", "Set SSID\0", get_param_set_wifi_ssid, run_set_wifi_ssid, NO, YES, YES, set_wifi_ssid_uid_handle},
{'0', "wln11", "Show WiFi RSSI info\0", get_param_show_wifi_rssi_info, run_show_wifi_rssi_info, NO, YES, YES, show_wifi_rssi_info_uid_handle},
{'0', "wln12", "Get WiFi Band\0", get_param_get_wifi_band, run_get_wifi_band, NO, YES, YES, get_wifi_band_uid_handle},
{'0', "wln13", "Set WiFi Band\0", get_param_set_wifi_band, run_set_wifi_band, NO, YES, YES, set_wifi_band_uid_handle},
{'0', "wln14", "Get WiFi Channel\0", get_param_get_wifi_channel, run_get_wifi_channel, NO, YES, YES, get_wifi_channel_uid_handle},
{'0', "wln15", "Set WiFi Channel\0", get_param_set_wifi_channel, run_set_wifi_channel, NO, YES, YES, set_wifi_channel_uid_handle},
{'0', "wln16", "Set up WiFi Throughput\0", get_param_setup_wifi_throughput, run_setup_wifi_throughput, YES, YES, YES, setup_wifi_throughput_uid_handle},
{'0', "wln17", "Set WiFi Antenna\0", get_param_set_wifi_antenna, run_set_wifi_antenna, NO, YES, YES, set_wifi_antenna_uid_handle}
};

#define SIZE_WLAN_MENU (sizeof diag_basic_wlan_menu / sizeof(DIAGS_NODE))

#endif

