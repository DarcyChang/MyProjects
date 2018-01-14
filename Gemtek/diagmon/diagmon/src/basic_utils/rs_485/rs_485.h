#ifndef _DAIG_RS_485_H_
#define _DAIG_RS_485_H_

DIAG_CODE rs_485_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE rs_485_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_rs_485_send_test_signal(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_rs_485_send_test_signal(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE rs_485_send_test_signal_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_rs_485_enter_receive_mode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_rs_485_enter_receive_mode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE rs_485_enter_receive_mode_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

#define VERSTR       "Do Re Mi Fa So La Ti Do"
#define UART2_DEV    "/dev/ttyS1"

DIAGS_NODE diag_basic_rs_485_menu[]={
{'0', NULL, "RS-485 Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "48501", "RS-485 Send a Test Signal\0", get_param_rs_485_send_test_signal, run_rs_485_send_test_signal, YES, YES, YES, rs_485_send_test_signal_uid_handle},
{'0', "48502", "RS-485 Enter Receive Mode\0", get_param_rs_485_enter_receive_mode, run_rs_485_enter_receive_mode, YES, YES, YES, rs_485_enter_receive_mode_uid_handle}
};

#define SIZE_RS_485_MENU (sizeof diag_basic_rs_485_menu / sizeof(DIAGS_NODE))

#endif

