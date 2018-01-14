#include "diag_cmm.h"
#include "diagmon.h"

/*  global_variable */
IO_DATA global_pio_data;
DIAG_RESULT global_prst;

DIAG_CODE global_variable_init(void)
{
	memset(&global_pio_data, 0x0, sizeof(&global_pio_data));
	memset(&global_prst, 0x0, sizeof(&global_prst));

	global_pio_data.com.flag_continuous = DEFAULT_FLAG_CONTINUOUS;
	global_pio_data.com.flag_err_stop = DEFAULT_FLAG_ERR_STOP;
	global_pio_data.com.flag_stopwatch = DEFAULT_FLAG_STOPWATCH;
	global_pio_data.com.flag_debug = DEFAULT_FLAG_DEBUG;
	global_pio_data.com.flag_show_uid = DEFAULT_FLAG_SHOW_UID;
	global_pio_data.com.flag_show_flags = DEFAULT_FLAG_SHOW_FLAGS;
	global_pio_data.lc_menu_op.show_menu = ON;
	global_pio_data.lc_menu_op.show_flags = ON;
	global_pio_data.lc_menu_op.show_prompt = ON;
	global_pio_data.backdoor.backdoor_call = OFF;

	return DONE;
}

int main_utils()
{
	int i;
	DIAG_CODE flag_valid_menu = UNSET;
	char inst[256];
	DIAG_CODE menu_ret = UNSET;
	DIAG_CODE ret = UNSET;
	DIAG_CODE option = UNSET;
	DIAGS_NODE *menu = diag_main_menu;

	diag_menu_index_init(menu, SIZE_MAIN_MENU);

	while (1) {
		flag_valid_menu = UNSET;
		show_menu(menu, SIZE_MAIN_MENU, &global_pio_data);

		memset (inst , 0 , 256);
		option = diag_get_menu_option(inst);

		if(option == ENTER) continue;
		if(option == TOP) continue;
		if(option == QUIT) break;
		if(option == ESC) break;
		if(option == HELP) 
			show_menu_usage();
		
		if(option == FLAG) 
			menu_ret = run_flags_utils(&global_pio_data, &global_prst);

		if(option == DONE) {
			for(i = 1; i < SIZE_MAIN_MENU; i++) {
				if(menu[i].index == inst[0]) {
					flag_valid_menu = ON;
					if ((menu[i].menu_function != NULL) && (menu[i].usable == YES))
						menu_ret = (*menu[i].menu_function)(&global_pio_data, &global_prst);
					break;
				}
			}
			if(flag_valid_menu != ON) {
				show_illegal_menu_message();
				continue;
			}
		}
		
		if(menu_ret == TOP) continue;
		if(menu_ret == QUIT) break;
		if(menu_ret == ESC) continue;
  	}
  	
  	return DONE;
}


int main_uid_handle()
{
	int i;
	char uid_str[16];
	DIAGS_NODE *menu = diag_main_menu;
	DIAG_CODE menu_ret = UNSET;

	memset(uid_str, 0x0, sizeof(uid_str));
	strncpy(uid_str, global_pio_data.argv[UID_IDX], sizeof(uid_str));
	DBGMSG("uid = %s\n", uid_str);
	for(i = 1; i < SIZE_MAIN_MENU; i++) {
		if(strstr(uid_str, menu[i].UID) != 0) {
			DBGMSG("menu[%d].UID = %s\n", i, menu[i].UID);
			if((menu[i].command_function == NULL) || (menu[i].uid_quick_runnable != YES)) {
				printf("This tool does not support commond mode\n");
			}else {
				menu_ret = (*menu[i].command_function)(&global_pio_data, &global_prst);
			}
			break;
		}
	}
	return 0;
}

int main(int argc, char **argv)
{
	int opt = 0;
	int i = 0;

	global_variable_init();

	if(argc == 1) {
		printf ("Welcome to the Diagmon Shell environment\n");
		//printf ("Everythings are developing\n");
		main_utils();
		return 0;
	}

	while((opt=getopt(argc, argv, "c:")) != -1)
	{
		switch(opt)
		{
			case 'c':				
				DBGMSG("[main] argc = %d\n", argc);
				for(i = 0; i < argc; i++){
				DBGMSG("argv[%d] = %s\n", i, argv[i]);
				}
				global_pio_data.argv = argv;
				global_pio_data.argc = argc;
				main_uid_handle();
				break;
			default:
				printf("Incorrect Command!\n");
		}
	}
	return 0;
}

