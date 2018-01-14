#ifndef _DAIG_NAND_FLASH_H_
#define _DAIG_NAND_FLASH_H_

DIAG_CODE nand_flash_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_flash_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_nand_flash_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_nand_flash_info(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_nand_flash_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_flash_0_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_flash_0_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_flash_0_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_flash_1_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_flash_1_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_flash_1_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_flash_random_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_flash_random_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_flash_random_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_copy_flash_to_file(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_copy_flash_to_file(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_copy_flash_to_file_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_copy_file_to_flash(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_copy_file_to_flash(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_copy_file_to_flash_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_erase_flash(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_erase_flash(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_erase_flash_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_erase_image(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_erase_image(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_erase_image_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_load_image_to_flash(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_load_image_to_flash(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_bad_block_number_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_bad_block_number_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_bad_block_number_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_nand_flash_sampling_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_nand_flash_sampling_test(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE nand_flash_sampling_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);


DIAGS_NODE diag_basic_nand_flash_menu[]={
{'0', NULL, "NAND_Flash Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "nad01", "Show NAND Flash Info\0", get_param_show_nand_flash_info, run_show_nand_flash_info, YES, YES, YES, show_nand_flash_info_uid_handle},
{'0', "nad02", "NAND Flash Walking 0's Test\0", get_param_nand_flash_0_test, run_nand_flash_0_test, YES, YES, YES, nand_flash_0_test_uid_handle},
{'0', "nad03", "NAND Flash Walking 1's Test\0", get_param_nand_flash_1_test, run_nand_flash_1_test, YES, YES, YES, nand_flash_1_test_uid_handle},
{'0', "nad04", "NAND Flash Pseudo Random Test\0", get_param_nand_flash_random_test, run_nand_flash_random_test, YES, YES, YES, nand_flash_random_test_uid_handle},
{'0', "nad05", "NAND Copy from Flash to File\0", get_param_nand_copy_flash_to_file, run_nand_copy_flash_to_file, YES, YES, YES, nand_copy_flash_to_file_uid_handle},
{'0', "nad06", "NAND Copy from File to Flash\0", get_param_nand_copy_file_to_flash, run_nand_copy_file_to_flash, YES, YES, YES, nand_copy_file_to_flash_uid_handle},
{'0', "nad08", "Erase NAND Flash\0", get_param_nand_erase_flash, run_nand_erase_flash, YES, YES, YES, nand_erase_flash_uid_handle},
{'0', "nad09", "Erase Image in NAND Flash\0", get_param_nand_erase_image, run_nand_erase_image, YES, YES, YES, nand_erase_image_uid_handle},
{'0', "nad11", "Bad Block Number Test\0", get_param_nand_bad_block_number_test, run_nand_bad_block_number_test, YES, YES, YES, nand_bad_block_number_test_uid_handle},
{'0', "nad12", "NAND flash Sampling Test\0", get_param_nand_flash_sampling_test, run_nand_flash_sampling_test, YES, YES, YES, nand_flash_sampling_test_uid_handle},
{'0', "nad10", "Load Image to NAND Flash\0", get_param_nand_load_image_to_flash, run_nand_load_image_to_flash, NO, YES, YES, NULL}
};

#define SIZE_NAND_FLASH_MENU (sizeof diag_basic_nand_flash_menu / sizeof(DIAGS_NODE))

#endif

