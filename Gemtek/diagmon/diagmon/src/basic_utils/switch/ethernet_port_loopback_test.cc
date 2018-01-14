
DIAG_CODE get_param_ethernet_port_loopback_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n"); 
	return DONE;
}

DIAG_CODE run_ethernet_port_loopback_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = 0;
	char cmd[256];
	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/

	timer_start(pio_data);
	do{
		/* test, tool body */
		//DBGMSG("run_memory_0_test\n");
		//local_ret = run_test_tool(size);
		
		/* report the result */
		/* The secondary parameter of diag_report() must be PASS or FAIL */
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

DIAG_CODE ethernet_port_loopback_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;
	int i = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c bsc-swh-swh02\n");
	}else if(pio_data->argc == (3 + params_num)) {

		//clear port mark for loopback test
		for(i = 0; i < ETH_PORT_NUM; i++) {
			pio_data->u.eth.port_mark[i] = 0;
		}	
		
		ret = run_ethernet_port_loopback_test(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

