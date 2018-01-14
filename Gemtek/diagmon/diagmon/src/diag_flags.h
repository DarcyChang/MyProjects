#ifndef _DAIG_FLAGS_H_
#define _DAIG_FLAGS_H_


DIAG_CODE run_flags_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_debug_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_stopwatch_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_continuous_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_err_stop_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_show_uid_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_show_flags_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_flags_restore_default_utils(IO_DATA *pio_data, DIAG_RESULT *prst);

DIAGS_NODE diag_flags_menu[]={
{'0', NULL, "Diagnostic Flag Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "flg01", "toggle \"Debug\" flag\0", NULL, run_flags_debug_utils, YES, YES, NO, NULL},
{'0', "flg02", "toggle \"Stopwatch\" flag\0", NULL, run_flags_stopwatch_utils, YES, YES, NO, NULL},
{'0', "flg03", "toggle \"Continuous\" flag\0", NULL, run_flags_continuous_utils, YES, YES, NO, NULL},
{'0', "flg04", "toggle \"Stop on error\" flag\0", NULL, run_flags_err_stop_utils, YES, YES, NO, NULL},
{'0', "flg05", "toggle \"Show UID\" flag\0", NULL, run_flags_show_uid_utils, YES, YES, NO, NULL},
{'0', "flg06", "toggle \"Show flags status\" flag\0", NULL, run_flags_show_flags_utils, YES, YES, NO, NULL},
{'0', "flg07", "restore all flags to default\0", NULL, run_flags_restore_default_utils, YES, YES, NO, NULL}
};

#define SIZE_FLAGS_MENU (sizeof diag_flags_menu / sizeof(DIAGS_NODE))

#endif

