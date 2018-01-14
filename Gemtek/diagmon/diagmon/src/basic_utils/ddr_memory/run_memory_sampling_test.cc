#define OFFSET1 0x1200000
#define OFFSET2 0x3200000
#define OFFSET3 0x6400000
#define SIZE1 1

DIAG_CODE run_sampling_test()
{
	DIAG_CODE ret = 0;
	char cmd[256];	

	memset(cmd, 0, sizeof(cmd));
	sprintf(cmd, "memtester -p %x %dM 1 13", OFFSET1, SIZE1);
	ret = system(cmd);

	if(ret == -1)
		return ret;

	else if(ret == 0){

		memset(cmd, 0, sizeof(cmd));
		sprintf(cmd, "memtester -p %x %dM 1 14", OFFSET2, SIZE1);
		ret = system(cmd);

		if(ret == -1)
			return ret;

		else if(ret == 0){

			memset(cmd, 0, sizeof(cmd));
			sprintf(cmd, "memtester -p %x %dM 1 0", OFFSET3, SIZE1);
			ret = system(cmd);
			return ret;
		}
	}
}


DIAG_CODE get_param_memory_sampling_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	return DONE;
}

DIAG_CODE run_memory_sampling_test(IO_DATA *pio_data, DIAG_RESULT *prst)
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
		//DBGMSG("run_memory_0_test\n");
		//local_ret = run_test_tool(size);

		local_ret = run_sampling_test();

		/* report the result */
		/* The secondary parameter of diag_report() must be PASS or FAIL */
		if(local_ret == -1) {
			ret = diag_report(prst, FAIL, "memory_sampling_test fail report");
		}else if(local_ret == 0){
			ret = diag_report(prst, PASS, "memory_sampling_test pass report");
		}else{
			// get unexpected ret
		}

	}while(diag_flow_control(ret, pio_data) == RUN); 
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE memory_sampling_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c bsc-mem-mem08\n");
	}else if(pio_data->argc == (3 + params_num)) {
		ret = run_memory_sampling_test(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

