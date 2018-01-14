#include "diag_cmm.h"
#include "diag_flags.h"

DIAG_CODE toggle_on_off(int *x)
{
	*x = (*x == ON)?OFF:ON;
	return DONE;
}

DIAG_CODE run_flags_debug_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	toggle_on_off((int *)&(pio_data->com.flag_debug));	
	return DONE;
}

DIAG_CODE run_flags_stopwatch_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	toggle_on_off((int *)&(pio_data->com.flag_stopwatch));	
	return DONE;
}

DIAG_CODE run_flags_continuous_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	toggle_on_off((int *)&(pio_data->com.flag_continuous));	
	return DONE;
}

DIAG_CODE run_flags_err_stop_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	toggle_on_off((int *)&(pio_data->com.flag_err_stop));	
	return DONE;
}

DIAG_CODE run_flags_show_uid_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	toggle_on_off((int *)&(pio_data->com.flag_show_uid));
	return DONE;
}

DIAG_CODE run_flags_show_flags_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	toggle_on_off((int *)&(pio_data->com.flag_show_flags));
	return DONE;
}

DIAG_CODE run_flags_restore_default_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	pio_data->com.flag_continuous = DEFAULT_FLAG_CONTINUOUS;
	pio_data->com.flag_err_stop = DEFAULT_FLAG_ERR_STOP;
	pio_data->com.flag_stopwatch = DEFAULT_FLAG_STOPWATCH;
	pio_data->com.flag_debug = DEFAULT_FLAG_DEBUG;
	pio_data->com.flag_show_uid = DEFAULT_FLAG_SHOW_UID;
	pio_data->com.flag_show_flags = DEFAULT_FLAG_SHOW_FLAGS;
	
	return DONE;
}

DIAG_CODE run_flags_utils(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int i;
	DIAG_CODE flag_valid_menu = UNSET;
	char inst[256];
	DIAG_CODE menu_ret = UNSET;
	DIAG_CODE option = UNSET;
	DIAGS_NODE *menu = diag_flags_menu;

	diag_menu_index_init(menu, SIZE_FLAGS_MENU);

	while (1) {
		flag_valid_menu = UNSET;
		pio_data->lc_menu_op.show_menu = ON;
		pio_data->lc_menu_op.show_flags = ON;
		show_menu(menu, SIZE_FLAGS_MENU, pio_data);

		memset (inst , 0 , 256);
		option = diag_get_menu_option(inst);

		if(option == ENTER) continue; 
		if(option == TOP) return TOP; 
		if(option == QUIT) return QUIT; 
		if(option == ESC) return ESC; 
		if(option == FLAG)  continue;
		if(option == HELP) 
			show_menu_usage();

		if(option == DONE) {
			for(i = 1; i < SIZE_FLAGS_MENU; i++) {
				if(menu[i].index == inst[0]) {
					flag_valid_menu = ON;
					if((menu[i].menu_function != NULL) && (menu[i].usable == YES))
						menu_ret = (*menu[i].menu_function)(pio_data, prst);
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
