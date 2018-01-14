#include <diag_cmm.h>

void show_menu(DIAGS_NODE menu[], int menu_size, IO_DATA *global_pio_data)
{
	int i = 0;

	if(global_pio_data->lc_menu_op.show_menu == ON) {
		printf("\n\n\t%s\n", menu[0].menu_name);
		
		for(i = 1; i < menu_size; i++) { // skip subject
			if(menu[i].visible == YES) {
				if((global_pio_data->com.flag_show_uid == ON) && (menu[i].UID != NULL))
					printf(" %c: [%s] %s\n", menu[i].index, menu[i].UID, menu[i].menu_name);
				else
					printf(" %c: %s\n", menu[i].index, menu[i].menu_name);
			}
		}
		printf("\n");
	}
	
	if(global_pio_data->lc_menu_op.show_flags == ON)
		diag_show_flag(global_pio_data);
	
	if(global_pio_data->lc_menu_op.show_prompt == ON)
		printf("enter %s item >", menu[0].menu_name);

	//reset
	global_pio_data->lc_menu_op.show_menu = ON;
	global_pio_data->lc_menu_op.show_flags = ON;
	global_pio_data->lc_menu_op.show_prompt = ON;

	return;
}

void logAdd(char *Tstr, char *Istr, char *msg)
{
#if 0 // not ready yet
        if(openErrLog()==1) {
                errLog_setTitle("Fatal error #1 %s test", Tstr);
                errLog_setTest("Start %s test", Istr);
                errLog_addMsg("%s", msg);
                errLog_endMsg();
                errLog_endTest(1, "%s test", Tstr);
                closeErrLog();
        }
#endif		
}

void timer_start(IO_DATA *pio_data)
{
	if(pio_data->com.flag_stopwatch != ON)
		return;
	
	time(&(pio_data->stopwatch.start_time));

	return;
}

void timer_stop(IO_DATA *pio_data)
{
	if(pio_data->com.flag_stopwatch != ON)
		return;
	
	time(&(pio_data->stopwatch.stop_time));
	pio_data->stopwatch.exe_time = (time_t) (pio_data->stopwatch.stop_time - pio_data->stopwatch.start_time);

	if(pio_data->stopwatch.exe_time <= 1)
		printf("The execution time: %d second\n", (int)pio_data->stopwatch.exe_time);
	else
		printf("The execution time: %d seconds\n", (int)pio_data->stopwatch.exe_time);

	return;
}

DIAG_CODE diag_report(DIAG_RESULT *prst, DIAG_CODE ret, char *rst)
{
	char *test_rst;
	test_rst = (char *) malloc(sizeof(char) * (strlen(rst) + 1));
	memset(test_rst, 0x0, sizeof(test_rst));
	
	prst->ret = ret;
	sprintf(test_rst, "%s", rst);
	prst->rst = test_rst;

	DBGMSG("prst->rst = %s\n", ((prst->rst)!=NULL)?(prst->rst):"");

#if 0 // for test
	if(prst->rst != NULL)
		free(prst->rst);
#endif

	switch(ret) {
		case PASS:
			printf("This test result is PASS.\n");
			break;
		case FAIL:
			printf("This test result is FAIL.\n");
			break;
		case DONE:
			printf("It is DONE.\n");
			break;
		case ERROR:
			printf("An ERROR is happened.\n");
			break;
		default:
			DBGMSG("undefined behavior\n");
	}
	
	printf("%s\n", (rst!=NULL)?rst:"");

	return ret;
}

DIAG_CODE clear_diag_result(DIAG_RESULT *prst)
{
	prst->ret = UNSET;
	
	if(prst->rst != NULL) {
		free(prst->rst);
		prst->rst = NULL;
	}

	return DONE;
}

DIAG_CODE diag_get_menu_option(char *input_option)
{
	uint element;
	char str[256], inst[256];
	//DIAG_CODE ret = UNSET;

	memset (str , 0 , 256);
	memset (inst , 0 , 256);

	if (!fgets (str, 255, stdin)) {
		printf ("Error in reading line from stdin\n");
		return QUIT;
	}

	element = sscanf (str , "%s" , inst);

	
	if(element == 0 || !strcmp(str, "\n")) return ENTER;	// press Return
	if(inst[0] == 27 || !strcmp(inst, "esc")) return ESC;	//press Esc
	if(!strcmp(inst, "quit") || !strcmp(inst, "exit")) return QUIT;
	if(!strcmp(inst, "main") || !strcmp(inst, "top")) return TOP;
	if(!strcmp(inst, "flag")) return FLAG;
	if(!strcmp(inst, "help")) return HELP;

	strncpy(input_option, inst, 256);

	return DONE;
}

/* to detect keyboard event */
int kbhit(void)
{
        struct termios oldt, newt;
        int ch;
        int oldf;

        tcgetattr(STDIN_FILENO, &oldt);
        newt = oldt;
        newt.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
        fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

        ch = getchar();

        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
        fcntl(STDIN_FILENO, F_SETFL, oldf);

        if(ch != EOF) {
                ungetc(ch, stdin);
                return 1;
        }

        return 0;
}

DIAG_CODE diag_flow_control(DIAG_CODE result, IO_DATA *pio_data)
{
	DIAG_CODE ret = UNSET;

	if (pio_data->backdoor.backdoor_call == ON) {
		return STOP;
	}
	
	if ((pio_data->com.flag_continuous == ON)
		&&~((pio_data->com.flag_err_stop == ON)&&(result == FAIL || result == ERROR))) {
		ret = RUN;
	}

	if( kbhit() ) {
		if(getchar()==27)
			ret = STOP;
	}	

	return ret;
}

void diag_show_flag(IO_DATA *pio_data)
{
	if(pio_data->com.flag_show_flags == OFF)
		return;
	
	printf("FLAGS: \n");
	printf("Debug [%s] ", (pio_data->com.flag_debug == ON)?"ON":"OFF");
	printf("Stopwatch [%s] ", (pio_data->com.flag_stopwatch == ON)?"ON":"OFF");
	printf("Show UID [%s] ", (pio_data->com.flag_show_uid == ON)?"ON":"OFF");
	printf("Show Flags [%s] ", (pio_data->com.flag_show_flags == ON)?"ON":"OFF");
	printf("\n");
	printf("Continuous [%s] ", (pio_data->com.flag_continuous == ON)?"ON":"OFF");
	printf("Stop on Error [%s] ", (pio_data->com.flag_err_stop == ON)?"ON":"OFF");
	printf("\n\n");

	return;
}

void show_illegal_menu_message(void)
{
	printf("\n illegal menu item..., please try again!!\n\n");
	return;
}

void show_menu_usage(void)
{
	printf("\n");
	printf("  help: Show this help\n");
	printf("  esc: Go back the upper menu. It will leave this tool if you are in main menu\n");
	printf("  top/main: Go back the main menu\n");
	printf("  exit/quit: Leave this diagnostic tool\n");
	printf("  flag: Enter the Diagnostic Flag Menu\n");
	printf("\n");
}

#if 0 //Hugo: not ready yet
int diag_system(const *cmd)
{
	pid_t status;
	int ret = 0;

	status = system(cmd);
	printf("wifexited(status):%d/n", WIFEXITED(status));
	printf("WEXITSTATUS(status):%d/n", WEXITSTATUS(status));

	if(status == -1) {
		printf("system error!\n");
		ret = -1;
	}

	if(WIFEXITED(status)) {
		ret = WEXITSTATUS(status);
	}else {
		ret = -1;
	}
	
	return ret;
}

#endif

void diag_menu_index_init(DIAGS_NODE menu[], int menu_size)
{
	int i = 0;
	int index = 0;
	
	for(i = 0; i < menu_size; i++)
	{
		if((NULL != menu[i].UID) && (YES == menu[i].visible)) {
			menu[i].index = 0x61 + index;
			//printf("menu[%d].index = %c \n", i, menu[i].index);
			if(index < 26)
				index++;
			else
				printf("[ERROR] menu index over 26!\n");
		}
	}

	return;
}

