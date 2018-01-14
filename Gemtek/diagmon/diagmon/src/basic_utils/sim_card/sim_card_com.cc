/* Please put the common functions here if they are necessary */


int get_sim_imsi(char *imsi)
{

	DIAG_CODE ret = 0;
	
	//modem-cmd /dev/ttyUSB1 AT+CIMI
	//strcpy(imsi, "357486050787944");
	FILE *fp = NULL;
	char buffer[128];
	char *p;
	int check = 0;

	if(check_device(0x12d1, 0x1570))
	{
//		fp = popen("modem-cmd /dev/ttyUSB0 AT+CIMI", "r");
		fp = popen("atool_x86 imsi", "r");
		if(fp != NULL)
		{
			while(fgets(buffer, sizeof(buffer), fp))
			{
				DBGMSG("[%d] %s\n", __LINE__, buffer);

				if( strncmp(buffer, "IMSI CHECK : Pass", 17) == 0)
				{
					check = 1;
				}

				p = NULL;
				if(check == 1 && (p = strstr(buffer, "Imsi :")) != NULL)
				{
					ret = 1;
					sscanf( p, "Imsi : %s", imsi);
					break;
				}
			}
			pclose(fp);
		}else{	
			ret = -1;
			//DBGMSG("modem-cmd /dev/ttyUSB0 AT+CIMI fail\n");
		}


	}else{
		DBGMSG("detect device 0x12d1 0x1570 fail\n");
	}


	return ret;

}

int get_sim_status(char *status)
{

	DIAG_CODE ret = 0; 
	FILE *fp = NULL;
	char buffer[128];

	if(check_device(0x12d1, 0x1570))
	{
		fp = popen("atool_x86 sim", "r");		
		if(fp != NULL)
		{
			while(fgets(buffer, sizeof(buffer), fp))
			{
				DBGMSG("[%d] %s\n", __LINE__, buffer);
				if(strncmp(buffer, "SIM CARD CHECK", 14) == 0)
				{
					ret = 1;
					sscanf( buffer, "SIM CARD CHECK : %s", status);	
					break;
				}
			}
			pclose(fp);
		}else{
			ret = -1;
			DBGMSG("[%d] popen fail\n", __LINE__);
		}


	}else{
		ret = -1;
		strcpy(status, "Fail");
	}

        return ret;

}

