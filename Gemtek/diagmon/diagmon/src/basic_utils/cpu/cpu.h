#ifndef _DAIG_CPU_H_
#define _DAIG_CPU_H_

DIAG_CODE cpu_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE cpu_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_cpu_full_loading(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_cpu_full_loading(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE cpu_full_loading_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_cpu_usage(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_cpu_usage(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_cpu_usage_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_gpio(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_gpio(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_gpio_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_gpio(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_gpio(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_gpio_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_cpu_menu[]={
{'0', NULL, "CPU Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "cpu01", "CPU Full Loading Tool\0", get_param_cpu_full_loading, run_cpu_full_loading, YES, YES, YES, cpu_full_loading_uid_handle},
{'0', "cpu02", "Show CPU Usage\0", get_param_show_cpu_usage, run_show_cpu_usage, NO, YES, YES, show_cpu_usage_uid_handle},
{'0', "cpu03", "Set GPIO Tool\0", get_param_set_gpio, run_set_gpio, NO, YES, YES, set_gpio_uid_handle},
{'0', "cpu04", "Get GPIO Tool\0", get_param_get_gpio, run_get_gpio, NO, YES, YES, get_gpio_uid_handle}
};

#define SIZE_CPU_MENU (sizeof diag_basic_cpu_menu / sizeof(DIAGS_NODE))

#endif

