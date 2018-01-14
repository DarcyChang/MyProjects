
DIAG_CODE get_param_show_version(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	DIAG_CODE ret = 0;
	DBGMSG("get parameters\n");

	return DONE;
}

DIAG_CODE run_show_version(IO_DATA *pio_data, DIAG_RESULT *prst)
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
		FILE *fp;
		char line[128], *ptr, *version;

		local_ret = -1;
		fp = fopen("/etc/version", "r");
		if(fp != NULL) {
			fgets(line, sizeof(line), fp);
			ptr = line;
			strsep(&ptr, " ");
			version = strsep(&ptr, " ");
			memset(pio_data->u.cmt.version, 0x0, 32);
			strncpy(pio_data->u.cmt.version, version, strlen(version)); 
			local_ret = 0;
			fclose(fp);
		}

		/* report the result */
		/* The secondary parameter of diag_report() must be DONE or ERROR */
		if(local_ret == -1) {
			ret = diag_report(prst, ERROR, "Cannot parse /etc/version file");
		}else if(local_ret == 0){
			ret = diag_report(prst, DONE, pio_data->u.cmt.version);
		}else{
			// get unexpected ret
		}
	}while(diag_flow_control(ret, pio_data) == RUN);
	timer_stop(pio_data);

	return ret;
}

DIAG_CODE show_version_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst)
{
	int params_num = 0;
	DIAG_CODE ret = 0;

	if((pio_data->argc == 4) && (strncmp(pio_data->argv[UID_IDX+1], "help", 4) == 0)) {
		printf("diagmon -c <uid string>\n");
		printf("EX: diagmon -c cmn-cmn01\n");
	}else if(pio_data->argc == (3 + params_num)) {
		ret = run_show_version(pio_data, prst);
	}else {
		printf("Incorrect command!!\n");
	}

	return ret;
}

