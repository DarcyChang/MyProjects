#ifndef _DAIG_W3G_H_
#define _DAIG_W3G_H_

DIAG_CODE w3g_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE w3g_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_w3g_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_w3g_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_w3g_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_w3g_imei_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_w3g_imei_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_w3g_imei_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_w3g_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_w3g_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_w3g_rssi_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_w3g_menu[]={
{'0', NULL, "3G Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "w3g01", "Show 3G Info\0", get_param_show_w3g_info, run_show_w3g_info, YES, YES, YES, show_w3g_info_uid_handle},
{'0', "w3g02", "Show 3G IMEI code Info\0", get_param_show_w3g_imei_info, run_show_w3g_imei_info, YES, YES, YES, show_w3g_imei_info_uid_handle},
{'0', "w3g03", "Show 3G RSSI info\0", get_param_show_w3g_rssi_info, run_show_w3g_rssi_info, YES, YES, YES, show_w3g_rssi_info_uid_handle}
};

#define SIZE_W3G_MENU (sizeof diag_basic_w3g_menu / sizeof(DIAGS_NODE))

#endif

