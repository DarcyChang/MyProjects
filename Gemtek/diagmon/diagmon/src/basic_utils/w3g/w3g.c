#include <diag_cmm.h>
#include "w3g.h"
#include "w3g_com.cc"
#include "show_w3g_info.cc"
#include "show_w3g_imei_info.cc"
#include "show_w3g_rssi_info.cc"

DIAG_CODE w3g_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int i;
	DIAG_CODE flag_valid_menu = UNSET;
	char inst[256];
	DIAG_CODE menu_ret = UNSET;
	DIAG_CODE para_ret = UNSET;
	DIAG_CODE option = UNSET;
	DIAGS_NODE *menu = diag_basic_w3g_menu;

	diag_menu_index_init(menu, SIZE_W3G_MENU);

	while (1) {
		flag_valid_menu = UNSET;
		show_menu(menu, SIZE_W3G_MENU, pio_data);

		memset (inst , 0 , 256);
		option = diag_get_menu_option(inst);

		OPTION_HANDLE(option);

		if(option == DONE) {
			for(i = 1; i < SIZE_W3G_MENU; i++) {
				if(menu[i].index == inst[0]) {
					flag_valid_menu = ON;
					if(menu[i].usable == YES) {
						if(menu[i].para_function != NULL)
							para_ret = (*menu[i].para_function)(pio_data, prst);
						if((para_ret == DONE) 
							&& (menu[i].menu_function != NULL))	
							menu_ret = (*menu[i].menu_function)(pio_data, prst);
					}
					break;
				}
			}
			if(flag_valid_menu != ON) {
				show_illegal_menu_message();
				continue;
			}
		}

		clear_diag_result(prst);
		MENU_RETURN_HANDLE(menu_ret);
	}

	return DONE;
}

DIAG_CODE w3g_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int i;
	char uid_str[16];
	DIAGS_NODE *menu = diag_basic_w3g_menu;
	DIAG_CODE menu_ret = UNSET;
	
	memset(uid_str, 0x0, sizeof(uid_str));
	strncpy(uid_str, pio_data->argv[UID_IDX], sizeof(uid_str));
	DBGMSG("uid = %s\n", uid_str);
	for(i = 1; i < SIZE_W3G_MENU; i++) {
		if(strstr(uid_str, menu[i].UID) != 0) {
			DBGMSG("menu[%d].UID = %s\n", i, menu[i].UID);
			if((menu[i].command_function == NULL) || (menu[i].uid_quick_runnable != YES)) {
				printf("This tool does not support commond mode!\n");
			}else {
				menu_ret = (*menu[i].command_function)(pio_data, prst);
			}
			break;
		}
	}

	return menu_ret;
}
