#ifndef _DAIG_LTE_H_
#define _DAIG_LTE_H_

DIAG_CODE lte_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE lte_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_lte_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_lte_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_lte_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_lte_imei_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_lte_imei_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_lte_imei_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_lte_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_lte_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_lte_rssi_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_lte_menu[]={
{'0', NULL, "LTE Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "lte01", "Show LTE info\0", get_param_show_lte_info, run_show_lte_info, YES, YES, YES, show_lte_info_uid_handle},
{'0', "lte02", "Show LTE IMEI code info\0", get_param_show_lte_imei_info, run_show_lte_imei_info, YES, YES, YES, show_lte_imei_info_uid_handle},
{'0', "lte03", "Show LTE RSSI info\0", get_param_show_lte_rssi_info, run_show_lte_rssi_info, YES, YES, YES, show_lte_rssi_info_uid_handle}
};

#define SIZE_LTE_MENU (sizeof diag_basic_lte_menu / sizeof(DIAGS_NODE))

#endif

