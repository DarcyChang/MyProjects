
DIAG_CODE get_param_set_system_run_level(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	return DONE;
}

DIAG_CODE run_set_system_run_level(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = 0;
	
	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/

	timer_start(pio_data);
	do{
		/* test, tool body */
		// local_ret = run_test_tool();

		/* report the result */
		/* The secondary parameter of diag_report() must be DONE or ERROR */
		if(local_ret == -1) {
			ret = diag_report(prst, ERROR, "Today is not your day, please contact the pitiful PL");
		}else if(local_ret == 0){
			ret = diag_report(prst, DONE, "");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN);
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE set_system_run_level_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 1;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string> <run_level>\n");
		printf("EX: diagmon -c cmn-cmn09 mfg\n");
	}else if(pio_data->argc == (3 + params_num)) {
		strcpy(pio_data->run_level.mode, pio_data->argv[UID_IDX+1]);
		ret = run_set_system_run_level(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

