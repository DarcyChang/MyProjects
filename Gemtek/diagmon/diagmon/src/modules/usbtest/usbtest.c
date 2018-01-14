#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
#include <sys/types.h>
#include <dirent.h>

#include <signal.h> // for interrupt signal handler
#include <unistd.h> // for interrupt signal handler

#define USB_MOUNT_PATH "/tmp/storage/USB"//"/media/" //"/mnt/sd"
//#define USB_INFO_PATH "/proc/bus/usb/devices"
#define USB_INFO_PATH "/sys/kernel/debug/usb/devices"
#define PATH_MAX_LEN (64)

void usage()
{
	printf("\nusage: usbtest [a/b/c/d]\n");
	printf(" a: usb traffic test\n");
	printf(" b: usb insertion test\n");
	printf(" c: usb enumeration test\n");
	printf(" d: usb pattern test\n");
}

void mountusbfs(void) 
{
	char mountstr[100];

	FILE* fp = NULL;
	if( (fp = fopen("/proc/mounts", "r")) ) {
		while (fgets(mountstr, sizeof(mountstr), fp))
		{
			if (strstr(mountstr, USB_MOUNT_PATH)) {
				fclose(fp);
				return;
			}
		}
		fclose(fp);
		printf(" Could not get USB mount path.\n");
	}else
		printf(" Could not open mount file '/proc/mounts' for reading.\n");
}

int getusbtraffic(void)
{
	char tempstr[50];
	char cmd[192];
	char mountpath[PATH_MAX_LEN];
	FILE* fp = NULL;
	char* fpstr = NULL;
	int i,count=1000;
	int flag = 0;
	int str_len = 0;

	if( (fp = fopen("/proc/mounts", "r")) ) {
		while (fgets(cmd, sizeof(cmd), fp))
		{
			if ((fpstr = strstr(cmd, USB_MOUNT_PATH)) != NULL) {
				memset(mountpath, 0x0, sizeof(mountpath));
				
				str_len = strcspn(fpstr, " ");
				if(str_len >= PATH_MAX_LEN) {
					printf("[Error] mount path length (%d) greater than PATH_MAX_LEN(%d)", str_len, PATH_MAX_LEN);
					return -1;
				}
					
				strncpy(mountpath, fpstr, str_len);
				printf(" USB mount path= %s\n", mountpath);
				flag = 1;
			}
		}
		
		fclose(fp);
		if(flag != 1) {
			printf(" Can't find USB mount path.\n");
			return -1;
		}
	}else {
			printf(" Could not open /proc/mounts.\n");
			return -1;
	}

	sprintf(tempstr, "%s/ciffartusb", mountpath);
	printf(" Test usb file path= %s\n", tempstr);

	if( (fp = fopen(tempstr, "w")) ) {
		// printf("try to create a file in USB......\n");
		for (i=1;i<=count;i++)
			fprintf(fp,"This is a USB-traffic-Test file\n");
		printf(" try to write data into USB.......\n");
	}else {
		printf(" Could not create a file in USB.\n");
		return -1;
	}
	fclose(fp);

	i=0;
	
	if( (fp = fopen(tempstr, "r")) ) {
		printf(" try to read data from USB......\n");
		while (fgets(tempstr, sizeof(tempstr), fp))
		{ 
			if (strstr(tempstr, "This is a USB-traffic-Test file\n"))
				i++;    
		}
		
		fclose(fp);
		sprintf(cmd, "rm -rf %s 2> /dev/null 1>&2", tempstr);
		system(cmd);     

		if (i==count) {
			// printf("USB Traffic Test is OK.\n\n");
			return 0;
		}else {
			printf(" USB R/W miss.\n");   
			return -1;
		}
	}else { 
		printf(" Could not read/write from USB.\n");
		return -1;
	}
}

int getusbinsert(void)
{
    char tempstr[100];
    char Driver[20];
    char *strptr = NULL;
    FILE* fp =NULL;
	if( (fp = fopen(USB_INFO_PATH, "r")) ){
		while (fgets(tempstr, sizeof(tempstr), fp))
		{
			strptr = strstr(tempstr, "Driver=usb-storage");
			if(strptr) {
				printf(" Get usb information:\n %s", tempstr);
				printf(" USB is conncected.\n");
				fclose(fp);
				return 0;
			}
		}
		printf(" USB is NOT connected!!\n");
		fclose(fp);
		return -1;
	}else {
		printf(" Could not open %s!.\n", USB_INFO_PATH);
		return -1;
	}
}

int getusbinfo(void)
{
	char tempstr[100];
	char Vendor[32];
	char Product[32];
	char SerialNumber[32];
	char Protocol[32];
	char Transport[32];
	int  chker=0;    // check if usb info. exist

	char *strptr = NULL;

	//DIR * dir;
	//DIR * dir2;
	//struct dirent * ptr;

	
	//dir = opendir("/proc/scsi/usb-storage");
	//if(dir) {
		//while((ptr = readdir(dir)) != NULL)
		//{
			//sprintf(tempstr, "/proc/scsi/usb-storage/%s", ptr->d_name);
			//printf("open file path %s\n", tempstr);
			//if((dir2 = opendir(tempstr)) == NULL) {
				strcpy(tempstr, USB_INFO_PATH);
				FILE* fp = NULL;
				if( (fp = fopen(tempstr, "r")) ) {
					while (fgets(tempstr, sizeof(tempstr), fp))
					{
						strptr = strstr(tempstr, "Vendor=");
						if(strptr) {
							strptr += 7;
							memset(Vendor,0,sizeof(Vendor));
							strncpy(Vendor, strptr, 5);
							chker = 1;
						}

						strptr = strstr(tempstr, "Product=");
						if(strptr) {
							strptr += 8;
							memset(Product,0,sizeof(Product));
							strncpy(Product, strptr, sizeof(Product)-1);
							chker = 1;
						}

						strptr = strstr(tempstr, "SerialNumber=");
						if(strptr) {
							strptr += 13;
							memset(SerialNumber,0,sizeof(SerialNumber));
							strncpy(SerialNumber, strptr, sizeof(SerialNumber)-1);
							chker = 1;
						}

						strptr = strstr(tempstr, "ProdID=");
						if(strptr) {
							strptr += 7;
							memset(Protocol,0,sizeof(Protocol));
							strncpy(Protocol, strptr, 5);
							chker = 1;
						}

						strptr = strstr(tempstr, "Manufacturer=");
						if(strptr) {
							strptr += 13;
							memset(Transport,0,sizeof(Transport));
							strncpy(Transport, strptr, sizeof(Transport)-1);
							chker = 1;
						}
					}
					fclose(fp);

					if(chker == 1) {
						printf(" USB Vendor: %s", Vendor);
						printf(" USB Product: %s", Product);
						printf(" USB SerialNumber: %s", SerialNumber);
						printf(" USB ProdID: %s", Protocol);
						printf(" USB Manufacturer: %s", Transport);
						//closedir(dir);
						return 0;
					}else {
						printf(" Could not get device information!.\n");
						//closedir(dir);
						return -1;
					}
				}else {
					printf(" Could not open %s.\n", tempstr);
					return -1;
				}
			//} else {
			//printf("%s: directory\n", ptr->d_name);
			//closedir(dir2);
			//}
		//}
	//}else {
		//printf(" Could not open /proc/scsi/usb-storage!.\n");
		//return -1;
	//}
}		

int main(int argc, char *argv[])
{
	int RET=-1; // return value  0:PASS  -1:FAIL

	if(argc==2) {
		if(!strcmp(argv[1], "a")) {   
			mountusbfs(); 
			if (getusbtraffic()==0) {
				printf(" USB Traffic Test is PASSED\n");
				RET=0;
			}
			else {
				printf(" USB Traffic Test is FAILED\n");
				RET=-1;
			}
		}
		else if(!strcmp(argv[1], "b")) { 
			mountusbfs(); 
			if (getusbinsert()==0) {
				printf(" USB Insertion Test is PASSED\n");
				RET=0;
			}
			else {
				printf(" USB Insertion Test is FAILED\n");
				RET=-1;
			}
		}
		else if(!strcmp(argv[1], "c")) {
			mountusbfs(); 
			if (getusbinfo()==0) {
				printf(" USB Enumeration Test is PASSED\n");
				RET=0;
			}
			else {
				printf(" USB Enumeration Test is FAILED\n");
				RET=-1;
			}
		}
		else if(!strcmp(argv[1], "d")) {
			printf(" USB no test pattern mode.\n");
			//system("reg s bfbb0000 && reg w 54 41005");
			//printf(" USB Change to test pattern mode.\n");
			//printf(" Plaese reboot device to reset USB.\n");
			RET=0;
		}
	}
	else 
		usage();
  
	return RET;
}

