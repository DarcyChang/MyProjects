#ifndef _DAIG_LED_H_
#define _DAIG_LED_H_

DIAG_CODE led_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE led_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_turn_on_all_leds(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_turn_on_all_leds(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE turn_on_all_leds_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_turn_off_all_leds(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_turn_off_all_leds(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE turn_off_all_leds_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_led_menu[]={
{'0', NULL, "LED Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "led01", "Turn On All LEDs\0", get_param_turn_on_all_leds, run_turn_on_all_leds, YES, YES, YES, turn_on_all_leds_uid_handle},
{'0', "led02", "Turn Off All LEDs\0", get_param_turn_off_all_leds, run_turn_off_all_leds, YES, YES, YES, turn_off_all_leds_uid_handle}
};

#define SIZE_LED_MENU (sizeof diag_basic_led_menu / sizeof(DIAGS_NODE))

#endif

