#ifndef _DAIG_CMM_H_
#define _DAIG_CMM_H_

#include "data_struct.h"

extern IO_DATA global_pio_data;

#define DBGMSG(fmt, args...)  \
	if(global_pio_data.com.flag_debug == ON)\
		printf("%s(%d): " fmt, __FUNCTION__, __LINE__, ##args)

#define OPTION_HANDLE(option) \
{ \
	if(option == ENTER) continue; \
	else if(option == TOP) return TOP; \
	else if(option == QUIT) return QUIT; \
	else if(option == ESC) return ESC; \
	else if(option == FLAG)  \
		menu_ret = run_flags_utils(pio_data, prst); \
	else if(option == HELP)  \
		show_menu_usage(); \
}		
	
#define MENU_RETURN_HANDLE(menu_ret) \
{ \
	if(menu_ret == TOP) return TOP; \
	else if(menu_ret == QUIT) return QUIT; \
	else if(menu_ret == ESC) continue; \
	else {pio_data->lc_menu_op.show_menu = OFF;pio_data->lc_menu_op.show_flags = OFF;} \
}


#define DEFAULT_FLAG_CONTINUOUS (OFF)
#define DEFAULT_FLAG_ERR_STOP (OFF)
#define DEFAULT_FLAG_STOPWATCH (OFF)
#define DEFAULT_FLAG_DEBUG (OFF)
#define DEFAULT_FLAG_SHOW_UID (OFF)	
#define DEFAULT_FLAG_SHOW_FLAGS (ON)	

#define UID_IDX (2)

void show_menu(DIAGS_NODE menu[], int menu_size, IO_DATA *global_pio_data);
void logAdd(char *Tstr, char *Istr, char *msg);
void timer_start(IO_DATA *pio_data);
void timer_stop(IO_DATA *pio_data);
DIAG_CODE diag_report(DIAG_RESULT *prst, DIAG_CODE ret, char *rst);
DIAG_CODE clear_diag_result(DIAG_RESULT *prst);
DIAG_CODE diag_get_menu_option(char *input_option);
DIAG_CODE diag_flow_control(DIAG_CODE result, IO_DATA *pio_data);
void diag_show_flag(IO_DATA *pio_data);
void show_illegal_menu_message(void);
void show_menu_usage(void);
void diag_menu_index_init(DIAGS_NODE menu[], int menu_size);

extern DIAG_CODE run_flags_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif

