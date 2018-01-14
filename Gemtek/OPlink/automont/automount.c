#include <unistd.h>
#include <sys/vfs.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mount.h>
#include <errno.h>
#include <objApi.h>
#include <nvram.h>
#include <fcntl.h>
#include <dirent.h>
#include <time.h>
#include <ct_log.h>
#define USB_PLUGIN "/tmp/usbpath"
#define USB_ERROR "/tmp/usb_error"
int file_exists (char * fileName)
{
	struct stat buf;
	int i = stat ( fileName, &buf );
		/* File found */
		if ( i == 0 ){
	    		return 1;
	  	}
	  	return 0;
}
int main(int argc, char **argv)
{
	char	devpath[64];
	char	usbpath[64];
	char	usberror[64];
	char	vendor[64];
	char	product[64];
	char	getinfo[128];
	char	test_cmd[128];
	FILE	*fp;
	int	ret = 0;
	int	i = 0;
	int	num = 0;
	int	total = 0;
	int	usb_error = 0;
	int	sur_cnt = 0;
	int	len = 0;
	int	start_on=0;
	int	start_time=0;
	int	stop_time=0;
	int	now_time=0;
        time_t	timep;
        struct	tm *p;	
	time(&timep);
        p = localtime(&timep);
        DIR	*dir;
        struct dirent **ent;
	struct objUsbdisk usbdisk;
	struct objSurveillance surveillance;
      	struct objSURschedule *objsurschedule = NULL;

	if(*argv == NULL){
		printf("no argv\n");
		return;
	}
       	if(objGet(GID_OBJS_USBDISK, &usbdisk) < 0)
       	        return;
        if(objGet(GID_OBJS_SURVEILLANCE, &surveillance) < 0 )
                return;

	sprintf(devpath, "/dev/%s", argv[1]);
	sprintf(usbpath, "/media/%s", argv[1]);

	if(!strcmp("add",getenv("ACTION"))){
		while(!file_exists(devpath)){
			sprintf(test_cmd,"mknod %s b %s %s",devpath,argv[2],argv[3]);
			system(test_cmd);
			usleep(100*1000);
		}
                fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/systime-ntpc/{count++}END{print count}'", "r");
                if(fp!= NULL)
                        fscanf(fp, "%d", &num);
                if(fp!= NULL)
                        pclose(fp);
		if(num==0)
                	sleep(30);
		mkdir(usbpath,S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
		for(i=0;i<3;i++){
			ret = mount(devpath, usbpath, "vfat", NULL, "");
			if(ret <0){
				usleep(1000);
			}else{
				sleep(3);
				break;
			}
			if(i==2){
				CT_LOG_DEBUG("AUTOMOUNT", "%s is not FAT format\n", argv[1]);
				fp = fopen(USB_ERROR,"w");
				fprintf(fp,"error: Not FAT format\n");
				fclose(fp);
				return -1;

			}
		}
		remove(USB_ERROR);
		total = scandir( "/media", &ent, 0, alphasort);
		if(strcmp(argv[1],ent[total-1]->d_name)){
			CT_LOG_DEBUG("AUTOMOUNT", "%s is not last mount point\n", argv[1]);
			umount(usbpath);
			remove(usbpath);
			return -1;
		}

		fp = fopen(USB_PLUGIN,"w");
		fprintf(fp,"%s", ent[total-1]->d_name);
		fclose(fp);
		
		CT_LOG_DEBUG("AUTOMOUNT", "%s mount on %s\n", argv[1],usbpath);
		i = 0;
		while(1){
			sprintf(getinfo,"/proc/scsi/usb-storage/%d", i);
			if(fp = fopen(getinfo,"r")){
				fclose(fp);
				break;
			}
			i++;
			usleep(100);
		}
		sprintf(getinfo, "echo -n `cat /proc/scsi/usb-storage/%d | grep Vendor | awk -F \": \"  '{ print $2 }'` > /tmp/usbdisk_info", i);
		system(getinfo);
		system("echo -n \" \" >> /tmp/usbdisk_info");
		sprintf(getinfo, "echo -n `cat /proc/scsi/usb-storage/%d | grep Product | awk -F \": \" '{ print $2 }'` >> /tmp/usbdisk_info", i);
		system(getinfo);
		if(surveillance.enable){
			if(surveillance.mode){
				if(surveillance.schedule){
					objSURscheduleGetAll((void **) &objsurschedule, &len);
					for(i = 0; i < 7; i++)
					{	
						if((objsurschedule[i].start_h || objsurschedule[i].start_m 
							|| objsurschedule[i].stop_h || objsurschedule[i].stop_m) == 0)
							continue;
						start_time=i*10000+objsurschedule[i].start_h*100+objsurschedule[i].start_m;
						stop_time=i*10000+objsurschedule[i].stop_h*100+objsurschedule[i].stop_m;
						if(stop_time < start_time)
							stop_time+=10000;
						now_time=(p->tm_wday)*10000+(p->tm_hour)*100+(p->tm_min);
						if(stop_time>=70000 && now_time<10000){
							if((now_time+70000) <= stop_time)
								start_on=1;
						}else{
							if(start_time <= now_time && now_time <= stop_time )
								start_on=1;
						}
					}
					system("rcConf restart schedule_record");
					if(start_on){	
						fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
						if(fp!= NULL)
        						fscanf(fp, "%d", &num);
						if(fp!= NULL)
							pclose(fp);
						while(num < 3) {
							usleep(1000);
							fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
							if(fp!= NULL)
        							fscanf(fp, "%d", &num);
							if(fp!= NULL)
							pclose(fp);
						}
						usleep(1000);
						system("start_record.sh");
                        			fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
                        			if(fp!= NULL)
                        			        fscanf(fp, "%d", &num);
                        			if(fp!= NULL)
                        			        pclose(fp);
                        			while(num < 5) {
                        				system("start_record.sh");
                        			        usleep(1000);
                        			        fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
                        			        if(fp!= NULL)
                        			                fscanf(fp, "%d", &num);
                        			        if(fp!= NULL)
                        			        pclose(fp);
                        			}
					}
				}else{
					system("rcConf restart schedule_record");
                        		fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
                        		if(fp!= NULL)
                        		        fscanf(fp, "%d", &num);
                        		if(fp!= NULL)
                        		        pclose(fp);
                        		while(num < 3) {
                        		        usleep(1000);
                        		        fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
                        		        if(fp!= NULL)
                        		                fscanf(fp, "%d", &num);
                        		        if(fp!= NULL)
                        		        pclose(fp);
                        		}
					usleep(1000);
                        		system("start_record.sh");
                        		fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
                        		if(fp!= NULL)
                        		        fscanf(fp, "%d", &num);
                        		if(fp!= NULL)
                        		        pclose(fp);
                        		while(num < 5) {
                        			system("start_record.sh");
                        		        usleep(1000);
                        		        fp = popen("ps -ef | LANG=C awk 'BEGIN{count=0}!/ps/&&/gst-record/{count++}END{print count}'", "r");
                        		        if(fp!= NULL)
                        		                fscanf(fp, "%d", &num);
                        		        if(fp!= NULL)
                        		        pclose(fp);
                        		}
				}
			}else{
				system("rcConf start takepic");
			}
			
		}

	}else{
		system("stop_record.sh");
		system("rcConf stop schedule_record");
		system("rcConf stop takepic");
		umount(usbpath);
		remove(usbpath);
		remove(USB_ERROR);
		remove(USB_PLUGIN);
		remove("/tmp/usb_remove");
		strcpy(usbdisk.usb_disk_info,"-");
		strcpy(usbdisk.usb_disk_size,"-");
		strcpy(usbdisk.usb_disk_status,"-");
		objSet(GID_OBJS_USBDISK, &usbdisk);
		nvram_commit(RT2860_NVRAM);
		CT_LOG_DEBUG("AUTOMOUNT", "%s umount success\n", argv[1]);
	}
	return 0;

}
