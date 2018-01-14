#ifndef _DAIG_RTC_H_
#define _DAIG_RTC_H_

DIAG_CODE rtc_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE rtc_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_display_rtc_time(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_display_rtc_time(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE display_rtc_time_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_rtc_time(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_rtc_time(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_rtc_time_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_reset_rtc_battery_status_flag(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_reset_rtc_battery_status_flag(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE reset_rtc_battery_status_flag_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_rtc_battery_status_flag(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_rtc_battery_status_flag(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_rtc_battery_status_flag_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);	


DIAGS_NODE diag_basic_rtc_menu[]={
{'0', NULL, "RTC Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "rtc01", "Display RTC time\0", get_param_display_rtc_time, run_display_rtc_time, YES, YES, YES, display_rtc_time_uid_handle},
{'0', "rtc02", "Set RTC time\0", get_param_set_rtc_time, run_set_rtc_time, YES, YES, YES, set_rtc_time_uid_handle},
{'0', "rtc03", "Reset RTC battery status flag\0", get_param_reset_rtc_battery_status_flag, run_reset_rtc_battery_status_flag, YES, YES, YES, reset_rtc_battery_status_flag_uid_handle},
{'0', "rtc04", "Get RTC battery status flag\0", get_param_get_rtc_battery_status_flag, run_get_rtc_battery_status_flag, YES, YES, YES, get_rtc_battery_status_flag_uid_handle}
};

#define SIZE_RTC_MENU (sizeof diag_basic_rtc_menu / sizeof(DIAGS_NODE))

#endif

