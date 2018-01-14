/* Please put the common functions here if they are necessary */

DIAG_CODE check_mac_address(IO_DATA *pio_data)
{
	char mac[6];

	if(sscanf(pio_data->u.cmt.base_mac, "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx", &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]) != 6)
		return ERROR;
	return DONE;
}

DIAG_CODE set_run_level(char *mode)
{

	return DONE;
}
