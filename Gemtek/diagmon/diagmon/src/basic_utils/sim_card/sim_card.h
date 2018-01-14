#ifndef _DAIG_SIM_CARD_H_
#define _DAIG_SIM_CARD_H_

DIAG_CODE sim_card_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE sim_card_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_sim_card_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_sim_card_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_sim_card_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_imsi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_imsi_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_imsi_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_sim_card_menu[]={
{'0', NULL, "SIM Card Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "sim01", "Show SIM Card Info\0", get_param_show_sim_card_info, run_show_sim_card_info, YES, YES, YES, show_sim_card_info_uid_handle},
{'0', "sim02", "Show IMSI info\0", get_param_show_imsi_info, run_show_imsi_info, YES, YES, YES, show_imsi_info_uid_handle}
};

#define SIZE_SIM_CARD_MENU (sizeof diag_basic_sim_card_menu / sizeof(DIAGS_NODE))

#endif

