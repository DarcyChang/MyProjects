
DIAG_CODE get_param_memory_0_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	ret = get_memory_info(pio_data);

	return ret;
}

DIAG_CODE run_memory_0_test(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = 0;
	char cmd[256];
	
	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/
	unsigned int offset = pio_data->u.mem.offset;
	int size = pio_data->u.mem.size;

	timer_start(pio_data);
	do{
		/* test, tool body */
		//DBGMSG("run_memory_0_test\n");
		//local_ret = run_test_tool(size);
		
		memset(cmd, 0, sizeof(cmd));
		sprintf(cmd, "memtester -p %x %dM 1 14", offset, size);

		local_ret = system(cmd);

		/* report the result */
		/* The secondary parameter of diag_report() must be PASS or FAIL */
		if(local_ret == -1) {
			ret = diag_report(prst, FAIL, "memory_0_test fail report");
		}else if(local_ret == 0){
			ret = diag_report(prst, PASS, "memory_0_test pass report");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN); 
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE memory_0_test_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 2;
	DIAG_CODE ret = 0;
	int offset = 0;
	int size = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string> <offset> <size>\n");
		printf("EX: diagmon -c bsc-mem-mem02 0x1200000 1\n");
	}else if(pio_data->argc == (3 + params_num)) {
		sscanf (pio_data->argv[UID_IDX+1] , "%x" , &offset);
		pio_data->u.mem.offset = offset;
		sscanf (pio_data->argv[UID_IDX+2] , "%d" , &size);
		pio_data->u.mem.size = size;
		ret = run_memory_0_test(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

