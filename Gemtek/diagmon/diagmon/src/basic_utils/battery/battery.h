#ifndef _DAIG_BATTERY_H_
#define _DAIG_BATTERY_H_

DIAG_CODE battery_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE battery_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_rel_charge(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_rel_charge(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_rel_charge_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_abs_charge(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_abs_charge(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_abs_charge_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_battery_status(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_battery_status(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_battery_status_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_charge_current(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_charge_current(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_charge_current_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_battery_menu[]={
{'0', NULL, "Battery Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "bty01", "Show relative status of charge\0", get_param_show_rel_charge, run_show_rel_charge, YES, YES, YES, show_rel_charge_uid_handle},
{'0', "bty02", "Show absolute status of charge\0", get_param_show_abs_charge, run_show_abs_charge, YES, YES, YES, show_abs_charge_uid_handle},
{'0', "bty03", "Show battery status\0", get_param_show_battery_status, run_show_battery_status, YES, YES, YES, show_battery_status_uid_handle},
{'0', "bty04", "Show charge current\0", get_param_show_charge_current, run_show_charge_current, YES, YES, YES, show_charge_current_uid_handle}
};

#define SIZE_BATTERY_MENU (sizeof diag_basic_battery_menu / sizeof(DIAGS_NODE))

#endif

