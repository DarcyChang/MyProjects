
DIAG_CODE get_param_set_base_mac(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	char input[18];

	DBGMSG("get parameters\n");

	memset(input, 0, sizeof(input));
	printf("Please enter the MAC address (XX:XX:XX:XX:XX:XX)> ");
	scanf("%18s[^\n]", input);
	snprintf(pio_data->u.cmt.base_mac, sizeof(pio_data->u.cmt.base_mac), "%s", input);

	ret = check_mac_address(pio_data);
	if(ret == ERROR) {
		diag_report(prst, ERROR, "Invalid MAC address!");
		return ERROR;
	}

	return DONE;
}

DIAG_CODE run_set_base_mac(IO_DATA *pio_data, DIAG_RESULT *prst)
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
		unsigned char mac[6];

		if(sscanf(pio_data->u.cmt.base_mac, "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx", &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]) == 6) {
			char cmd[256];
			snprintf(cmd, sizeof(cmd), "uci -c /mnt/data/config set mfg.system.base_mac='%02x:%02x:%02x:%02x:%02x:%02x'",
					mac[0], mac[1], mac[2], mac[3], mac[4], mac[5] );
			system(cmd);

			system("uci -c /mnt/data/config commit");

			system("/sbin/set_wifi_mac.sh");
		} else 
			local_ret = -1;

		/* report the result */
		/* The secondary parameter of diag_report() must be DONE or ERROR */
		if(local_ret == -1) {
			ret = diag_report(prst, ERROR, "Invalid MAC address!");
		}else if(local_ret == 0){
			ret = diag_report(prst, DONE, "");
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN);
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE set_base_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 1;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string> <mac>\n");
		printf("EX: diagmon -c cmn-cmn03 FF:FF:FF:FF:FF:FF\n");
	}else if(pio_data->argc == (3 + params_num)) {
		strncpy(pio_data->u.cmt.base_mac, pio_data->argv[UID_IDX+1], 17);
		ret = run_set_base_mac(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

