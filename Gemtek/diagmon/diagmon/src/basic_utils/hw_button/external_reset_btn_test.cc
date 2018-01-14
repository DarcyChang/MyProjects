
DIAG_CODE get_param_wps_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	return DONE;
}

DIAG_CODE run_wps_btn_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = -1;
	
	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/

	timer_start(pio_data);
	do{
		/* test, tool body */
		//DBGMSG("run_memory_0_test\n");

		/* report the result */
		/* The secondary parameter of diag_report() must be PASS or FAIL */
		if(local_ret == ERROR) {
			ret = diag_report(prst, FAIL, "external reset_btn_test fail report");
		}else if(local_ret == DONE){
			ret = diag_report(prst, PASS, "external reset_btn_test pass report");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN); 
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE wps_btn_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c bsc-btn-btn02\n");
	}else if(pio_data->argc == (3 + params_num)) {
		ret = run_wps_btn_test(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

