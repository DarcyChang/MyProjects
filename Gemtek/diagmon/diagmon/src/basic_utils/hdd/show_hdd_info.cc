
DIAG_CODE get_param_show_hdd_info(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	return DONE;
}

DIAG_CODE run_show_hdd_info(IO_DATA *pio_data, DIAG_RESULT *prst)
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
		if(YES == is_hdd_device())
		 	local_ret = system("hdparm -I /dev/sda");
		else
			local_ret = -1;
		
		/* report the result */
		/* The secondary parameter of diag_report() must be DONE or ERROR */
		if(local_ret == 0){
			ret = diag_report(prst, DONE, "");
		}else{
			ret = diag_report(prst, ERROR, "Today is not your day, please contact the pitiful PL");
		}
	}while(diag_flow_control(ret, pio_data) == RUN);
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE show_hdd_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c bsc-smp-smp01\n");
	}else if(pio_data->argc == (3 + params_num)) {
		ret = run_show_hdd_info(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}
