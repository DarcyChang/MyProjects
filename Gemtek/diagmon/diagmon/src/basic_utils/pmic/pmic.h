#ifndef _DAIG_PMIC_H_
#define _DAIG_PMIC_H_

DIAG_CODE pmic_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE pmic_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_pmic_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_pmic_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_pmic_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

DIAGS_NODE diag_basic_pmic_menu[]={
{'0', NULL, "PMIC Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "pmc01", "Show PMIC Info\0", get_param_show_pmic_info, run_show_pmic_info, YES, YES, YES, show_pmic_info_uid_handle}
};

#define SIZE_PMIC_MENU (sizeof diag_basic_pmic_menu / sizeof(DIAGS_NODE))

#endif

