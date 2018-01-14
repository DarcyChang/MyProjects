#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
#include <sys/types.h>
#include <dirent.h>

#include <signal.h> // for interrupt signal handler
#include <unistd.h> // for interrupt signal handler

#define SD_MOUNT_PATH "/tmp/storage/SD"
#define PATH_MAX_LEN (64)

void usage()
{
	printf("\nusage: sdtest [a]\n");
	printf(" a: sd traffic test\n");
}

void mountsdfs(void) 
{
	char mountstr[100];

	FILE* fp = NULL;
	if( (fp = fopen("/proc/mounts", "r")) ) {
		while (fgets(mountstr, sizeof(mountstr), fp))
		{
			if (strstr(mountstr, SD_MOUNT_PATH)) {
				fclose(fp);
				return;
			}
		}
		fclose(fp);
		printf(" Could not get SD mount path.\n");
	}else
		printf(" Could not open mount file '/proc/mounts' for reading.\n");
}

int getsdtraffic(void)
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
			if ((fpstr = strstr(cmd, SD_MOUNT_PATH)) != NULL) {
				memset(mountpath, 0x0, sizeof(mountpath));
				
				str_len = strcspn(fpstr, " ");
				if(str_len >= PATH_MAX_LEN) {
					printf("[Error] mount path length (%d) greater than PATH_MAX_LEN(%d)", str_len, PATH_MAX_LEN);
					return -1;
				}
					
				strncpy(mountpath, fpstr, str_len);
				printf(" SD mount path= %s\n", mountpath);
				flag = 1;
			}
		}
		
		fclose(fp);
		if(flag != 1) {
			printf(" Can't find SD mount path.\n");
			return -1;
		}
	}else {
			printf(" Could not open /proc/mounts.\n");
			return -1;
	}

	sprintf(tempstr, "%s/ciffartsd", mountpath);
	printf(" Test sd file path= %s\n", tempstr);

	if( (fp = fopen(tempstr, "w")) ) {
		// printf("try to create a file in SD......\n");
		for (i=1;i<=count;i++)
			fprintf(fp,"This is a SD-traffic-Test file\n");
		printf(" try to write data into SD.......\n");
	}else {
		printf(" Could not create a file in SD.\n");
		return -1;
	}
	fclose(fp);

	i=0;
	
	if( (fp = fopen(tempstr, "r")) ) {
		printf(" try to read data from SD......\n");
		while (fgets(tempstr, sizeof(tempstr), fp))
		{ 
			if (strstr(tempstr, "This is a SD-traffic-Test file\n"))
				i++;    
		}
		
		fclose(fp);
		sprintf(cmd, "rm -rf %s 2> /dev/null 1>&2", tempstr);
		system(cmd);     

		if (i==count) {
			// printf("SD Traffic Test is OK.\n\n");
			return 0;
		}else {
			printf(" SD R/W miss.\n");   
			return -1;
		}
	}else { 
		printf(" Could not read/write from SD.\n");
		return -1;
	}
}
	

int main(int argc, char *argv[])
{
	int RET=-1; // return value  0:PASS  -1:FAIL

	if(argc==2) {
		if(!strcmp(argv[1], "a")) {   
			mountsdfs(); 
			if (getsdtraffic()==0) {
				printf(" SD Traffic Test is PASSED\n");
				RET=0;
			}else {
				printf(" SD Traffic Test is FAILED\n");
				RET=-1;
			}
		}
	}else 
		usage();
  
	return RET;
}

