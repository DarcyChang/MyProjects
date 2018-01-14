#ifndef _DAIG_USB_H_
#define _DAIG_USB_H_

DIAG_CODE usb_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE usb_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_usb_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_usb_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_usb_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_usb_traffic_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_usb_traffic_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE usb_traffic_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_usb_insertion_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_usb_insertion_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE usb_insertion_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_usb_pattern_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_usb_pattern_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE usb_pattern_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_usb_menu[]={
{'0', NULL, "USB Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "usb01", "Show USB Info\0", get_param_show_usb_info, run_show_usb_info, YES, YES, YES, show_usb_info_uid_handle},
{'0', "usb02", "USB Traffic Test\0", get_param_usb_traffic_test, run_usb_traffic_test, YES, YES, YES, usb_traffic_test_uid_handle},
{'0', "usb03", "USB Insertion Test\0", get_param_usb_insertion_test, run_usb_insertion_test, YES, YES, YES, usb_insertion_test_uid_handle},
{'0', "usb04", "USB Pattern Test\0", get_param_usb_pattern_test, run_usb_pattern_test, NO, YES, YES, usb_pattern_test_uid_handle}
};

#define SIZE_USB_MENU (sizeof diag_basic_usb_menu / sizeof(DIAGS_NODE))

#endif

