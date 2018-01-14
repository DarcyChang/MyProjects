#ifndef _DAIG_CLOUD_H_
#define _DAIG_CLOUD_H_

DIAG_CODE CLOUD_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE CLOUD_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_cloud_pincode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_cloud_pincode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_cloud_pincode_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_cloud_pincode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_cloud_pincode(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_cloud_pincode_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_cloud_menu[]={
{'0', NULL, "Sample Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "cld01", "Set Cloud Pincode\0", get_param_set_cloud_pincode, run_set_cloud_pincode, YES, YES, YES, set_cloud_pincode_uid_handle},
{'0', "cld02", "Get Cloud Pincode\0", get_param_get_cloud_pincode, run_get_cloud_pincode, YES, YES, YES, get_cloud_pincode_uid_handle}
};

#define SIZE_CLOUD_MENU (sizeof diag_basic_cloud_menu / sizeof(DIAGS_NODE))

#endif

