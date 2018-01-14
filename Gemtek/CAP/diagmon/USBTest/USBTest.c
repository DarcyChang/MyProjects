#include "wizard.h"
#include <sys/stat.h>

typedef struct USB_REQ_INFO
{
	unsigned char Req[10];  //==> ACCESS or D-ACCESS or OVERCUR
	unsigned char reserved[100];  // reserved(fill 0x00 all)
}USB_REQ_INFO;

int USBTest(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	char *dir = NULL;
	char *file_size = NULL;
	char md5sum[33]="";
	char correct_md5sum[33]="";
	char cmd[256]="";
	char Action_Status;
	IO_DATA pio_data;
	DIAG_CODE ret;
	DIAG_RESULT prst;
	USB_REQ_INFO usb_req_info;
	struct stat buf;
	int stat_ret = 0;
	FILE *fptr;	

	/* do your test action */
	diag_parameters_init(&pio_data);
	ret = UNSET;
	
	memset(&usb_req_info,0,sizeof(usb_req_info));
	p = rcvbuf + sizeof("BackdoorPacketUSBTest_Req")-1;
	if(p != NULL){

		int usb3Check_ret = -1;
		memcpy(&usb_req_info,p,sizeof(usb_req_info));
		if(strstr(usb_req_info.Req, "2.0") != 0) {
			// add USB 2.0/3.0 check for ClassConnect wizard
			usb3Check_ret = system("lsusb -D `ls /dev/bus/usb/002/* | awk '{ if (!/001$/) print $0 }'` 2> /dev/null | grep 'Device can operate at SuperSpeed'");
			if(WEXITSTATUS(usb3Check_ret) == 0){
				printf("USB3.0 storage detected!!\n");
				ret = FAIL;
			}else{
				ret = run_usb_traffic_test(&pio_data, &prst);
			}

		}else if(strstr(usb_req_info.Req, "3.0") != 0) {
			// add USB 2.0/3.0 check for ClassConnect wizard
			usb3Check_ret = system("lsusb -D `ls /dev/bus/usb/002/* | awk '{ if (!/001$/) print $0 }'` 2> /dev/null | grep 'Device can operate at SuperSpeed'");
			if(WEXITSTATUS(usb3Check_ret) == 0){
				ret = run_usb_traffic_test(&pio_data, &prst);
			}else{
				printf("No USB3.0 storage detected!!\n");
				ret = FAIL;
			}
			
		}else if((strstr(usb_req_info.Req, "SATA") != 0) || (strstr(usb_req_info.Req, "sata") != 0)) {
			ret = run_hdd_traffic_test(&pio_data, &prst);
			if(ret == PASS) {
				
				/* Hugo: Check content hub in HDD */
				if(strlen(p+4) != 0) { /* Darcy : Just verify HDD traffic without directory. */
					ret = FAIL;
					printf("p+4 = %s\n", p+4);
					dir = strtok(p+4, ",");
					stat_ret = stat(dir, &buf);
					printf("File size in HDD content hub = %d\n", buf.st_size);

					if(dir != NULL){
						file_size = strtok(NULL, ",");
						if(file_size != NULL){
							/* Darcy : There are two way to verify content hub file in HDD.
							 * One is md5 check sum (packet string include "M", like as "SATA/media/preloaded/content_dir/IER Manifest_English.zip,Mfe6b89d7fb65af4d539544f31ca807fe"),
							 * another is file size (without "M", like as "SATA/media/preloaded/content_dir/IER Manifest_English.zip,33756338").
							*/
							if(!strncmp("M", file_size, 1)){ 
								sprintf(cmd, "md5sum \"%s\" | awk '{printf $1}' > /tmp/content_file_md5sum", dir);
								system(cmd);			
								fptr = fopen("/tmp/content_file_md5sum","r");

								if(fgets(md5sum, 33, fptr) == NULL)
									printf("Open /tmp/content_file_md5sum fail.\n");
								fclose(fptr);
								memcpy(correct_md5sum, file_size+1, sizeof(correct_md5sum));								
								printf("Correct md5sum = %s\n", correct_md5sum);		

								if(strcmp(md5sum, correct_md5sum) == 0){
									printf("[PASS] md5sum = %s does match.\n", md5sum);		
									ret = PASS;
								}else {
									perror("HDD content hub check");
									printf("[PASS] md5sum = %s doesn't match.\n", md5sum);		
								}

							}else{
								if(buf.st_size == atoi(file_size)){
									printf("[PASS] Correct file size = %s does match.\n", file_size);		
									ret = PASS;
								}else {
									perror("HDD content hub check");
									printf("[FAIL] Correct file size = %s doesn't match.\n", file_size);		
								}
							}
						}
					}
				}
			}

		}else {
			printf("incorrect req!\n");
			ret = FAIL;
		}
	}

	if(ret == PASS) {
		Action_Status = '1'; //successful
	}else {
		Action_Status = '0'; //failed
	}

	memcpy(sndbuf, "BackdoorPacketUSBTest_Ack", sizeof("BackdoorPacketUSBTest_Ack"));
	for( p=sndbuf ; *p ; p++ );

	memcpy(p, &Action_Status, sizeof(Action_Status));
	snd_len = strlen("BackdoorPacketUSBTest_Ack") + sizeof(Action_Status);

	hit = 1 ;
	return hit;
}
