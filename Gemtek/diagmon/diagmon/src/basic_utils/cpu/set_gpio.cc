
DIAG_CODE get_param_set_gpio(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

        ret = get_cputest_input(2, pio_data);

        return ret;
}

DIAG_CODE run_set_gpio(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	/* local variables */
	DIAG_CODE ret = 0;
	int local_ret = 0;
	char cmd[256];

	/* get parameters if it is necessary */
	/* ex:
	int size = pio_data->u.xxx.yyy;
	*/
	unsigned int pin = pio_data->u.cpu.pin_index;
	int value = pio_data->u.cpu.value;

	timer_start(pio_data);
	do{
		/* test, tool body */
		//DBGMSG("run_memory_0_test\n");
		//local_ret = run_test_tool(size);

		printf("All GPIO pins changed to pure gpio mode\n");
                memset(cmd, 0, sizeof(cmd));
                sprintf(cmd, "gpio g 1");
		system(cmd);

		printf("GPIO pin%d changed to output direction\n", pin);
                memset(cmd, 0, sizeof(cmd));
                sprintf(cmd, "gpio w %d %d", pin, value);
		local_ret = system(cmd);

		/* report the result */
		/* The secondary parameter of diag_report() must be PASS or FAIL */
		if(local_ret == -1) {
			ret = diag_report(prst, ERROR, "set_gpio_tool error report");
		}else if(local_ret == 0){
			ret = diag_report(prst, DONE, "");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN); 
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE set_gpio_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 2;
	DIAG_CODE ret = 0;
	int pin_idx = 0;
	int pin_val = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string> <pin_index> <value>\n");
		printf("EX: diagmon -c bsc-cpu-cpu03 10 0\n");
	}else if(pio_data->argc == (3 + params_num)) {
		sscanf (pio_data->argv[UID_IDX+1] , "%d" , &pin_idx);
		pio_data->u.cpu.pin_index = pin_idx;
		sscanf (pio_data->argv[UID_IDX+2] , "%d" , &pin_val);
		pio_data->u.cpu.pin_index = pin_val;
		ret = run_set_gpio(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

