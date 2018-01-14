#ifndef _DAIG_SDC_H_
#define _DAIG_SDC_H_

DIAG_CODE sdc_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE sdc_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_sdc_traffic_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_sdc_traffic_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE sdc_traffic_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_sdc_menu[]={
{'0', NULL, "SD card Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "sdc01", "SD Card Traffic Test\0", get_param_sdc_traffic_test, run_sdc_traffic_test, YES, YES, YES, sdc_traffic_test_uid_handle}
};

#define SIZE_SDC_MENU (sizeof diag_basic_sdc_menu / sizeof(DIAGS_NODE))

#endif

