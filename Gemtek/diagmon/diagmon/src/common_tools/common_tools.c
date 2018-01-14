#include <diag_cmm.h>
#include "common_tools.h"
#include "common_tools_com.cc"
#include "show_version.cc"
#include "show_base_mac.cc"
#include "set_base_mac.cc"
#include "restore_to_default.cc"
#include "system_reboot.cc"
#include "get_sn_code.cc"
#include "set_sn_code.cc"
#include "show_system_run_level.cc"
#include "set_system_run_level.cc"
#include "system_poweroff.cc"
#include "system_halt.cc"

DIAG_CODE common_tools(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int i;
	DIAG_CODE flag_valid_menu = UNSET;
	char inst[256];
	DIAG_CODE menu_ret = UNSET;
	DIAG_CODE para_ret = UNSET;
	DIAG_CODE option = UNSET;
	DIAGS_NODE *menu = diag_common_tools_menu;

	diag_menu_index_init(menu, SIZE_COMMON_TOOLS_MENU);

	while (1) {
		flag_valid_menu = UNSET;
		show_menu(menu, SIZE_COMMON_TOOLS_MENU, pio_data);

		memset (inst , 0 , 256);
		option = diag_get_menu_option(inst);

		OPTION_HANDLE(option);

		if(option == DONE) {
			for(i = 1; i < SIZE_COMMON_TOOLS_MENU; i++) {
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

DIAG_CODE common_tools_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int i;
	char uid_str[16];
	DIAGS_NODE *menu = diag_common_tools_menu;
	DIAG_CODE menu_ret = UNSET;
	
	memset(uid_str, 0x0, sizeof(uid_str));
	strncpy(uid_str, pio_data->argv[UID_IDX], sizeof(uid_str));
	DBGMSG("uid = %s\n", uid_str);
	for(i = 1; i < SIZE_COMMON_TOOLS_MENU; i++) {
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
