/* Please put the common functions here if they are necessary */

//#define DEBUG

DIAG_CODE is_hdd_device(void)
{
	char tempstr[100];
	char nowscsi[8];
	char *strptr = NULL;
	//int ret = -1, scsiIdx = 0, usbnum = 0;
	FILE* fp =NULL;
	//int checknum = 0;
	int ifHDD = 0;
	
	if( (fp = fopen("/proc/scsi/scsi", "r")) ) {
		ifHDD = 0;
		while (fgets(tempstr, sizeof(tempstr), fp))
		{
			strptr = strstr(tempstr, "Host: ");
			if(strptr) {
				memset(nowscsi, 0x00, sizeof(nowscsi));
				strncpy(nowscsi, strptr+6, 6);
#ifdef DEBUG				
				printf("Get storage information:\n %s", tempstr);
				printf(" storage is conncected.\n");
#endif				
				fgets(tempstr, sizeof(tempstr), fp);
				if (strptr = strstr(tempstr, "Vendor: ATA") != NULL) {	//SATA HDD
					if(strstr(nowscsi, "scsi0") != NULL) {
						ifHDD = 1;
					}
				} 
			}
		}
		fclose(fp);
	}
	else
		printf(" Could not open /proc/scsi/scsi!.\n");

	return (ifHDD == 1)?(YES):(NO);
}