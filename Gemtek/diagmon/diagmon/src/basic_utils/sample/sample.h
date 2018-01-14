#ifndef _DAIG_SAMPLE_H_
#define _DAIG_SAMPLE_H_

DIAG_CODE sample_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE sample_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_sample_tool(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_sample_tool(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE sample_tool_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_sample_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_sample_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE sample_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_sample_menu[]={
{'0', NULL, "Sample Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "smp01", "Sample Tool\0", get_param_sample_tool, run_sample_tool, YES, YES, YES, sample_tool_uid_handle},
{'0', "smp02", "Sample Test\0", get_param_sample_test, run_sample_test, YES, YES, YES, sample_test_uid_handle}
};

#define SIZE_SAMPLE_MENU (sizeof diag_basic_sample_menu / sizeof(DIAGS_NODE))

#endif

