
DIAG_CODE get_param_show_w3g_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	return DONE;
}

DIAG_CODE run_show_w3g_rssi_info(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = 0;
	
	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/
	int rssi = 0;

	timer_start(pio_data);
	do{
		/* test, tool body */
		// local_ret = run_test_tool();
		pio_data->u.w3g.w3g_rssi = 0;
		local_ret = get_w3g_module_rssi(&rssi);			
		pio_data->u.w3g.w3g_rssi = rssi;
		printf("w3g rssi:%d\n ", pio_data->u.w3g.w3g_rssi);
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

DIAG_CODE show_w3g_rssi_info_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c bsc-smp-smp01\n");
	}else if(pio_data->argc == (3 + params_num)) {
		ret = run_show_w3g_rssi_info(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}