#include "wizard.h"

struct CMD_INFO
{
	unsigned char Cmd[150]; 
	unsigned char reserved[50];   // default by zero(0x00) ( don't care ) 
};

struct CMD_RETURN
{
  unsigned char CmdReturn[1000]; 
  unsigned char reserved[100];   // default by zero(0x00) ( don't care ) 
};

int SendCommandLine(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	struct CMD_INFO CMD_Info;
	struct CMD_RETURN CMD_Ret;
	IO_DATA pio_data;
	DIAG_RESULT prst;
	DIAG_CODE ret = UNSET;

	/* do your test action */
	diag_parameters_init(&pio_data);
	
	memset(&CMD_Info,0x0,sizeof(CMD_Info));
	memset(&CMD_Ret,0x0,sizeof(CMD_Ret));
	p = rcvbuf + sizeof("BackdoorPacketCmdLine_Req")-1;
	if(p != NULL){

		memcpy(&CMD_Info, p, sizeof(CMD_Info));
		//printf("CMD_Info.Cmd = %s\n",CMD_Info.Cmd);
	
		if(strstr(CMD_Info.Cmd, "poweroff") != 0) {
			//ret = run_system_poweroff(&pio_data, &prst);
			ret = DONE;
			
		}else if(strstr(CMD_Info.Cmd, "halt") != 0) {
			//ret = run_system_halt(&pio_data, &prst);
			ret = DONE;
			
		}else if(strstr(CMD_Info.Cmd, "reboot") != 0) {
			//ret = run_system_reboot(&pio_data, &prst);
			ret = DONE;
		
		}else if(strstr(CMD_Info.Cmd, "apup") != 0) {
			ret = run_setup_wifi_throughput(&pio_data, &prst);
			//system("/etc/ath/apup");
			//ret = DONE;
		
		}else if(strstr(CMD_Info.Cmd, "apdown") != 0) {
			system("/bin/sh /etc/ath/apdown");
			ret = DONE;
		
		}else if(strstr(CMD_Info.Cmd, "upgradebios") != 0) {
			char system_cmd[128], buf[128], *param;
			char bios_path[128];
			struct stat fileStat;

			ret = ERROR;
			sprintf(buf, "%s", CMD_Info.Cmd);
			param = strtok(buf, " ");
			if(param != NULL) {
				param = strtok(NULL, " ");
				if(param != NULL) {
					// Download the bios
					printf("bios name:[%s]\n", param);
					sprintf(bios_path, "/tmp/%s", param);
					sprintf(system_cmd, "cd /tmp && tftp -gr %s 192.168.1.10", param);
					system(system_cmd);

					// Determine whether the file exists
					if((0 == stat(bios_path, &fileStat)) && (fileStat.st_size != 0)) {
						sprintf(system_cmd, "dd if=%s of=/dev/mtdblock0", bios_path);
						printf("%s\n", system_cmd);
						system(system_cmd);
						ret = DONE;
					} else {			
						ret = ERROR;
					}
				}
			}
		}else if(strstr(CMD_Info.Cmd, "installLionicLicense") != 0) {
			struct stat fileStat;

			system("/bin/rm /mnt/data/lionic/lcua/LICENSE");
			
			system("install_lionic_license.sh");
			if(0 == stat("/mnt/data/lionic/lcua/LICENSE", &fileStat))
				ret = DONE;
			else
				ret = ERROR;

		}else if(strstr(CMD_Info.Cmd, "removeLionicLicense") != 0) {
			struct stat fileStat;

			system("/bin/rm /mnt/data/lionic/lcua/LICENSE");
			system("/bin/sync");
			if(0 != stat("/mnt/data/lionic/lcua/LICENSE", &fileStat))
				ret = DONE;
			else
				ret = ERROR;

		}else if(strstr(CMD_Info.Cmd, "installCloudCert") != 0) {
			struct stat fileStat;

			system("/bin/rm /mnt/data/cloud/ca.cert");
			system("/bin/rm /mnt/data/cloud/ca.enc.key");

			system("install_cloud_cert.sh");
			if( (0 == stat("/mnt/data/cloud/ca.cert", &fileStat)) && (0 == stat("/mnt/data/cloud/ca.enc.key", &fileStat)) )
				ret = DONE;
			else
				ret = ERROR;

		}else if(strstr(CMD_Info.Cmd, "removeCloudCert") != 0) {
			struct stat fileStat;
			
			system("/bin/rm /mnt/data/cloud/ca.cert");
			system("/bin/rm /mnt/data/cloud/ca.enc.key");
			system("/bin/sync");
			if( (0 != stat("/mnt/data/cloud/ca.cert", &fileStat)) && (0 != stat("/mnt/data/cloud/ca.enc.key", &fileStat)) )
				ret = DONE;
			else
				ret = ERROR;

		}else if(strstr(CMD_Info.Cmd, "mfgmode") != 0) {

			strcpy(pio_data.run_level.mode, "mfg");
			ret = run_set_system_run_level(&pio_data, &prst);
			
		}else if(strstr(CMD_Info.Cmd, "resetBtnTest") != 0) {

			ret = run_reset_btn_test(&pio_data, &prst);
			
		}else if(strstr(CMD_Info.Cmd, "wpsBtnTest") != 0) {

			ret = run_wps_btn_test(&pio_data, &prst);
			
		}else {
			ret = ERROR;
		}
	}

	if( DONE == ret || PASS == ret) {
		strcpy(CMD_Ret.CmdReturn, "SUCCESS");
	}else {
		strcpy(CMD_Ret.CmdReturn, "ERROR");
	}

	memcpy(sndbuf, "BackdoorPacketCmdLine_Ack", sizeof("BackdoorPacketCmdLine_Ack"));
	for( p=sndbuf ; *p ; p++ );

	memcpy(p,&CMD_Ret,sizeof(CMD_Ret));
	snd_len = strlen("BackdoorPacketCmdLine_Ack")+sizeof(CMD_Ret);

	hit = 1 ;

	//sendto(ECfd, sndbuf, snd_len, 0, ( struct sockaddr *)&Cli, Cli_sz);

	if(strstr(CMD_Info.Cmd, "poweroff") != 0) {
		//ret = run_system_poweroff(&pio_data, &prst);
	}else if(strstr(CMD_Info.Cmd, "halt") != 0) {
		//ret = run_system_halt(&pio_data, &prst);
	}else if(strstr(CMD_Info.Cmd, "reboot") != 0) {
		ret = run_system_reboot(&pio_data, &prst);
	}else if(strstr(CMD_Info.Cmd, "uciDefault") != 0) {
		system("restore_default");
	}else {
		ret = ERROR;
	}
	
	return hit;
}
