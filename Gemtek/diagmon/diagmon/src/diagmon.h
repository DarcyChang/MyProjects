#ifndef _DAIG_MAIN_H_
#define _DAIG_MAIN_H_

extern DIAG_CODE run_flags_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE run_basic_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE basic_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#ifdef SUPPORT_COMMON_TOOL
extern DIAG_CODE common_tools(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE common_tools_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif

DIAG_CODE global_variable_init(void);

DIAGS_NODE diag_main_menu[]={
{'0', NULL, "Main Diagnostic Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'a', "flg", "Alter Diag Flags\0", NULL, run_flags_utils, YES, YES, YES, NULL},
{'b', "bsc", "Basic Utilities\0", NULL, run_basic_utils, YES, YES, YES, basic_uid_handle},
#ifdef SUPPORT_COMMON_TOOL
{'c', "cmn", "Common Tools\0", NULL, common_tools, YES, YES, YES, common_tools_uid_handle},
#endif
//{'d', "mbd", "Motherboard Test\0", NULL, NULL, YES, YES, YES, NULL}
};

#define SIZE_MAIN_MENU (sizeof diag_main_menu / sizeof(DIAGS_NODE))

#endif

