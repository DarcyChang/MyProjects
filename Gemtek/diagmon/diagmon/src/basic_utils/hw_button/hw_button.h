#ifndef _DAIG_HW_BUTTON_H_
#define _DAIG_HW_BUTTON_H_

#include <sys/wait.h>

DIAG_CODE hw_button_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE hw_button_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_reset_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_reset_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE reset_btn_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_wps_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_wps_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE wps_btn_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE btn_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_hw_button_menu[]={
{'0', NULL, "Hardware Button Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "btn01", "Reset Button Test\0", get_param_reset_btn_test, run_reset_btn_test, YES, YES, YES, reset_btn_test_uid_handle},
{'0', "btn02", "WPS Button Test\0", get_param_wps_btn_test, run_wps_btn_test, YES, YES, YES, wps_btn_test_uid_handle},
{'0', "btn03", "Button Test\0", get_param_btn_test, run_btn_test, YES, YES, YES, btn_test_uid_handle},
};

#define SIZE_HW_BUTTON_MENU (sizeof diag_basic_hw_button_menu / sizeof(DIAGS_NODE))

#endif

