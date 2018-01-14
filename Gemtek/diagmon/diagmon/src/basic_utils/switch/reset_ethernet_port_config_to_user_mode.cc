
DIAG_CODE get_param_reset_ethernet_port_config_to_user_mode(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");
	//User Mode 1
	pio_data->u.eth.pattern_mode = 1;
	return DONE;
}

DIAG_CODE run_reset_ethernet_port_config_to_user_mode(IO_DATA *pio_data, DIAG_RESULT *prst)
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
		local_ret = SetMode(pio_data);
		/* report the result */
		/* The secondary parameter of diag_report() must be DONE or ERROR */
		if(local_ret == -1) {
			ret = diag_report(prst, ERROR, "Set to User mode failed");
		}else if(local_ret == 0){
			ret = diag_report(prst, DONE, "");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN);
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE reset_ethernet_port_config_to_user_mode_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c bsc-swh-swh06\n");
	}else if(pio_data->argc == (3 + params_num)) {

		pio_data->u.eth.pattern_mode = 1;
		ret = run_reset_ethernet_port_config_to_user_mode(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

