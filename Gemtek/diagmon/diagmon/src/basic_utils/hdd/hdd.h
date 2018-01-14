#ifndef _DAIG_HDD_H_
#define _DAIG_HDD_H_

DIAG_CODE hdd_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE hdd_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_hdd_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_hdd_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_hdd_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_hdd_traffic_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_hdd_traffic_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE hdd_traffic_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_hdd_menu[]={
{'0', NULL, "HDD Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "hdd01", "Show HDD Info\0", get_param_show_hdd_info, run_show_hdd_info, YES, YES, YES, show_hdd_info_uid_handle},
{'0', "hdd02", "HDD Traffic Test\0", get_param_hdd_traffic_test, run_hdd_traffic_test, YES, YES, YES, hdd_traffic_test_uid_handle}
};

#define SIZE_HDD_MENU (sizeof diag_basic_hdd_menu / sizeof(DIAGS_NODE))

#endif

