
DIAG_CODE get_param_show_cpu_usage(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

        ret = get_cputest_input(1, pio_data);

        return ret;
}

DIAG_CODE run_show_cpu_usage(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = 0;
        char cmd[256];

	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/
        unsigned int sec = pio_data->u.cpu.time_sec;

	timer_start(pio_data);
	do{
		/* test, tool body */
		//DBGMSG("run_memory_0_test\n");
		//local_ret = run_test_tool(size);

                printf("Renew cpu usage in %d seconds\n", sec);
                memset(cmd, 0, sizeof(cmd));
                sprintf(cmd, "cpu -c %d", sec);
                local_ret = system(cmd);


		/* report the result */
		/* The secondary parameter of diag_report() must be PASS or FAIL */
                if(local_ret == -1) {
                        ret = diag_report(prst, ERROR, "show_cpu_usage error report");
                }else if(local_ret == 0){
                        ret = diag_report(prst, DONE, "");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN); 
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE show_cpu_usage_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 1;
	DIAG_CODE ret = 0;
	int sec = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string> <second>\n");
		printf("EX: diagmon -c bsc-cpu-cpu02 5\n");
	}else if(pio_data->argc == (3 + params_num)) {
		sscanf (pio_data->argv[UID_IDX+1] , "%d" , &sec);
		pio_data->u.cpu.time_sec = sec;
		ret = run_show_cpu_usage(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

