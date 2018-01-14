#ifndef _DAIG_DDR_MEMORY_H_
#define _DAIG_DDR_MEMORY_H_

DIAG_CODE ddr_memory_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE ddr_memory_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_memory_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_memory_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_memory_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_memory_0_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_memory_0_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE memory_0_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_memory_1_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_memory_1_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE memory_1_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_memory_random_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_memory_random_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE memory_random_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_memory_sampling_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_memory_sampling_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE memory_sampling_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_memory_info();
DIAG_CODE getSystemMemInfo(int infoType);

DIAGS_NODE diag_basic_ddr_memory_menu[]={
{'0', NULL, "DDR Memory Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "mem01", "Show Memory Info\0", get_param_show_memory_info, run_show_memory_info, YES, YES, YES, show_memory_info_uid_handle},
{'0', "mem02", "Memory Walking 0's Test\0", get_param_memory_0_test, run_memory_0_test, YES, YES, YES, memory_0_test_uid_handle},
{'0', "mem03", "Memory Walking 1's Test\0", get_param_memory_1_test, run_memory_1_test, YES, YES, YES, memory_1_test_uid_handle},
{'0', "mem04", "Memory Pseudo Random Test\0", get_param_memory_random_test, run_memory_random_test, YES, YES, YES, memory_random_test_uid_handle},
{'0', "mem08", "Memory Sampling Test\0", get_param_memory_sampling_test, run_memory_sampling_test, YES, YES, YES, memory_sampling_test_uid_handle}
};

#define SIZE_DDR_MEMORY_MENU (sizeof diag_basic_ddr_memory_menu / sizeof(DIAGS_NODE))

#endif

