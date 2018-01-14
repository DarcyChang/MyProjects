/* Please put the common functions here if they are necessary */

int check_device(int vid, int pid) 
{
	int ret = 0;
	char device_str[64];
	FILE *fp = NULL;
	sprintf(device_str,"ID %04x:%04x", vid, pid);
		
	char buffer[128];
	char *p;
	memset(buffer, 0x0, sizeof(buffer));
	fp = popen("lsusb", "r");

	if(fp != NULL)
	{

		while(fgets(buffer, sizeof(buffer), fp))
		{
			DBGMSG("[%d] %s\n", __LINE__, buffer);
			p = NULL;
			if( (p = strstr(buffer, device_str)) != NULL)
			{
				ret = 1;
				break;
			}
			
		}
		pclose(fp);

	}

	return ret;

}

int get_w3g_module_imei(char *imei)
{
	char *p;
        DIAG_CODE ret = 0;
	FILE *fp = NULL;
	char buffer[128];
	int check = 0;
	
	memset(imei, 0x00, sizeof(imei));

	if(check_device(0x12d1, 0x1570))
	{
		fp = popen("atool_x86 imei", "r");
		if(fp != NULL)
		{
			while(fgets(buffer, sizeof(buffer), fp))
			{
				DBGMSG("[%d] %s\n", __LINE__, buffer);
				//strncpy(imei, buffer, strlen(buffer));

				if(strncmp(buffer, "IMEI CHECK : Pass", 17) == 0)
				{
					check = 1;
				}
				p = NULL;
				if( check == 1 && (p = strstr(buffer, "IMEI :" )) != NULL)
				{	
					ret = 1;
					sscanf( p, "IMEI : %s", imei);
					break;
				}
			}

			pclose(fp);
		}else{
			ret = -1;
		}
		
        	//strcpy(imei, "358191011536419");
	}else{

		ret = -1;
	}
        return ret;

}

int get_w3g_module_name(char *name)
{


        DIAG_CODE ret = 0;

	FILE *fp = NULL;
	char buffer[64];
	char *p;

	if(check_device(0x12d1, 0x1570))
	{
        	memset(name, 0x00, sizeof(name));

//	        strcpy(name, "Android");
//		fp = popen("modem-cmd /dev/ttyUSB0 AT+GMM", "r");
		fp = popen("atool_x86 conf", "r");

		if(fp != NULL)
		{
			while(fgets(buffer, sizeof(buffer), fp))
			{
				DBGMSG("[%d] %s\n", __LINE__, buffer);
				p = NULL;
				if( (p = strstr(buffer, "Model :")) != NULL)
				{
					sscanf( p, "Model : %s", name);
					break;
				}

			}
			pclose(fp);
		}else{
			ret = -1;
		}

	}else{
		ret = -1;
	}
        return ret;

}
int get_w3g_module_rssi(int* rssi)
{


	DIAG_CODE ret = 0;

	FILE *fp = NULL;
	char buffer[64];
	char *p;
  
	int mode = 13, freq = 2140, primary_target =  -50, aux_target = -50, window = 40; 
	char rssi_cmd[128], status[8];
   
	float primary_rssi, aux_rssi;

	sprintf(rssi_cmd, "atool_x86 rssi -m %d -f %d -pt %d -at %d -w %d -div", mode, freq, primary_target, aux_target, window);

	DBGMSG("[%d] %s\n", __LINE__, rssi_cmd);

  
	if(check_device(0x12d1, 0x1570))
	{
//		fp = popen("modem-cmd /dev/ttyUSB0 AT+CSQ", "r");
		fp = popen(rssi_cmd, "r");
	
		if(fp != NULL)
		{
			while(fgets(buffer, sizeof(buffer), fp))
			{
				DBGMSG("[%d] %s\n", __LINE__, buffer);
				if( strncmp(buffer, "W2100 RSSI TEST :", 17) == 0)
				{
					ret = 1;
					sscanf( buffer, "W2100 RSSI TEST : %f %f %s", &primary_rssi, &aux_rssi, status);
					DBGMSG("[%d] pri_rssi:%3.2f, aux_rssi:%3.2f, status %s\n", __LINE__, primary_rssi, aux_rssi, status);
					*rssi = (int) primary_rssi;
					break;					
				}
			}                
			pclose(fp);
		}else{
			 ret = -1;
		}

        }else{
                ret = -1;
        }
        return ret;

}
