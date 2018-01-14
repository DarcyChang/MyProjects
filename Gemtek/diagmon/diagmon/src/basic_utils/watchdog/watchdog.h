#ifndef _DAIG_WATCHDOG_H_
#define _DAIG_WATCHDOG_H_

DIAG_CODE watchdog_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE watchdog_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_watchdog_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_watchdog_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_watchdog_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_watchdog_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_watchdog_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE watchdog_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_watchdog_menu[]={
{'0', NULL, "Watchdog Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "wdg01", "Show Watchdog Info\0", get_param_show_watchdog_info, run_show_watchdog_info, YES, YES, YES, show_watchdog_info_uid_handle},
{'0', "wdg02", "Watchdog Test\0", get_param_watchdog_test, run_watchdog_test, YES, YES, YES, watchdog_test_uid_handle}
};

#define SIZE_WATCHDOG_MENU (sizeof diag_basic_watchdog_menu / sizeof(DIAGS_NODE))

#endif

