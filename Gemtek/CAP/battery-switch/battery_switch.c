#include <stdio.h>
#include <string.h>
#include "battery_switch.h"

#define TIMEOUT_SECONDS 60
#define SMBUS_BATTERY_CONNECTED 0
#define IIC_BATTERY_CONNECTED 1

static pthread_t Timeout = 1;

int TimeIsUp = 0;
int tempcount = 0;

static void *Timeout_60s(void *p)
{
	tempcount++; // Darcy : delete
	printf("create tempcount %d\n", tempcount); // Darcy : delete
	pthread_detach(pthread_self());
	pthread_cond_t cond;
	pthread_mutex_t mutex;
	pthread_cond_init(&cond,NULL); 
	pthread_mutex_init(&mutex,NULL);
	pthread_mutex_lock(&mutex);
	struct timespec to;
	to.tv_sec = time(0)+TIMEOUT_SECONDS;
	to.tv_nsec = 0;
	int Err = pthread_cond_timedwait(&cond, &mutex, &to);

	if(Err == ETIMEDOUT){
		TimeIsUp = 1;
	}
	pthread_mutex_unlock(&mutex);  
	printf("close tempcount %d\n", tempcount); // Darcy : delete
	return 0;
}

int Detect_Battery_Type()
{
	int Result = -1;
	while(1){
		Result = -1;
		TimeIsUp = 0;

		if(pthread_create(&Timeout, NULL, Timeout_60s, NULL) != 0) {
			DBGMSG("Create thread Timeout_60s FAIL !!!\n");
			return -1;  
		}

//		while((Result = SMBus_Battery_Status()) <= 0 && TimeIsUp != 1){
		while((Result = SMBus_Battery_Status()) > 100 && TimeIsUp != 1){
			sleep(1);		
		}

		printf("Line %d tempcount = %d\n", __LINE__, tempcount);
		printf("Time is up, unconnected SMBus Battery.\n");
#if 0
		while(1){
			if((Result = SMBus_Battery_Status()) <= 0 ){
				if(TimeIsUp == 1){
					printf("Line %d tempcount = %d\n", __LINE__, tempcount);
					printf("Time is up, unconnected SMBus Battery.\n");
					break;
//				sleep(1);		
				}	
			}else{
				break;
			}
		}
#endif
//		if(Result < 0){
		if(Result >= 0 && Result <= 100){
			printf("Connected SMBus Battery.\n");
//			break;
			return SMBUS_BATTERY_CONNECTED;
		}

		Result = -1;
		TimeIsUp = 0;

		if(pthread_create(&Timeout, NULL, Timeout_60s, NULL) != 0) {
			DBGMSG("Create thread Timeout_60s FAIL !!!\n");
			return -1;  
		}

		while((Result = IIC_Battery_Status()) < 0 && TimeIsUp != 1){
			sleep(1);		
		}
		printf("Line %d tempcount = %d\n", __LINE__, tempcount);
		printf("Time is up, unconnected IIC Battery.\n");
#if 0
		while(1){
			if((Result = IIC_Battery_Status()) <= 0 ){
				if(TimeIsUp == 1){
					printf("Line %d tempcount = %d\n", __LINE__, tempcount);
					printf("Time is up, unconnected IIC Battery.\n");
					break;
//				sleep(1);
				}			
			}else{
				break;
			}
		}
#endif
		if(Result >= 0){
			printf("Connected IIC Battery.\n");
			return IIC_BATTERY_CONNECTED;
//			break;	
		}
	}
	return 0;
}

int SMBus_Battery_Status()
{
	int BatteryStatus = -1;
	FILE *pp = NULL;
	char buf[80];
	
	system("echo \"r 0x0d\" > /proc/bb_smbus_reg");
	system("cat /proc/bb_smbus_reg > /tmp/BatteryChargeStatus");
	if((pp = popen("cat /tmp/BatteryChargeStatus", "r"))==NULL){
		DBGMSG("BatteryStatus create popen() fail.\n"); // modify to DBGMSG
		return -1;
	}else{
		memset(buf, 0, sizeof(buf));
		if(fgets(buf, sizeof(buf), pp)!=NULL){
			sscanf(buf, "%d", &BatteryStatus);
		}
	}
	pclose(pp);
	return BatteryStatus;
}

int IIC_Battery_Status()
{
	int BatteryStatus = -1;
	FILE *pp = NULL;
	char buf[80];
	
	system("i2cget -y 1 0x55 0x2c > /tmp/BatteryChargeStatus 2>/dev/null");
	if((pp = popen("cat /tmp/BatteryChargeStatus", "r"))==NULL){
		DBGMSG("BatteryStatus create popen() fail.\n"); 
		return -1;
	}else{
		memset(buf, 0, sizeof(buf));
		if(fgets(buf, sizeof(buf), pp)!=NULL){
			sscanf(buf, "%x", &BatteryStatus);
		}
	}
	pclose(pp);

	return BatteryStatus;
}

int SMBus_Battery_Charge_Status()
{
	int BatteryChargeStatus = 65536;
	FILE *pp = NULL;
	char buf[80];
	
	system("echo \"r 0x0a\" > /proc/bb_smbus_reg");
	system("cat /proc/bb_smbus_reg > /tmp/batterySwitch");
	if((pp = popen("cat /tmp/batterySwitch", "r"))==NULL){
		DBGMSG("BatteryChargeStatus create popen() fail.\n");
		return -1;
	}else{
		memset(buf, 0, sizeof(buf));
		if(fgets(buf, sizeof(buf), pp)!=NULL){
			sscanf(buf, "%d", &BatteryChargeStatus);
		}
	}
	pclose(pp);
	return BatteryChargeStatus;
}

int IIC_Battery_Charge_Status()
{
	int BatteryChargeStatus = 65535;
	FILE *pp = NULL;
	char buf[80];
	
	system("i2cget -y 1 0x55 0x14 w > /tmp/batterySwitch 2>/dev/null ");
	if((pp = popen("cat /tmp/batterySwitch", "r"))==NULL){
		DBGMSG("BatteryChargeStatus create popen() fail.\n");
		return -1;
	}else{
		memset(buf, 0, sizeof(buf));
		if(fgets(buf, sizeof(buf), pp)!=NULL){
			sscanf(buf, "%x", &BatteryChargeStatus);
		}
	}
	pclose(pp);
		
	/* If Battery status is discharge. */
	if(BatteryChargeStatus & 0x00008000)
		BatteryChargeStatus -= 65535;
		return BatteryChargeStatus;
}

int GPIO_Status()
{
	int GPIOHighLow = 0; // High = 1, is SMBus battery. Low = 0, is IIC Battery
	FILE *pp = NULL;
	char buf[80];

	system("echo 213 > /sys/class/gpio/export");
	system("cat /sys/class/gpio/gpio213/value > /tmp/gpio_battery_switch_status");

	if((pp = popen("cat /tmp/gpio_battery_switch_status", "r"))==NULL){
		DBGMSG("BatteryStatus create popen() fail.\n"); 
		return -1;
	}else{
		memset(buf, 0, sizeof(buf));
		if(fgets(buf, sizeof(buf), pp)!=NULL){
			sscanf(buf, "%d", &GPIOHighLow);
		}
	}
	pclose(pp);
//	printf("%s : %d : GPIOHighLow = %d\n", __func__, __LINE__, GPIOHighLow);
	
	return GPIOHighLow;
}

int Battery_Status()
{
	int GPIOHighLow = 0; // High = 1, is SMBus battery. Low = 0, is IIC Battery
	int BatteryStatus = -1;
	FILE *pp = NULL;
	char buf[80];
	
	GPIOHighLow = GPIO_Status();	
	
	if(GPIOHighLow == 1){
		system("echo \"r 0x0d\" > /proc/bb_smbus_reg");
		system("cat /proc/bb_smbus_reg > /tmp/BatteryChargeStatus");
		if((pp = popen("cat /tmp/BatteryChargeStatus", "r"))==NULL){
			DBGMSG("BatteryStatus create popen() fail.\n"); // modify to DBGMSG
			return -1;
		}else{
			memset(buf, 0, sizeof(buf));
			if(fgets(buf, sizeof(buf), pp)!=NULL){
				sscanf(buf, "%d", &BatteryStatus);
			}
		}
		pclose(pp);
		return BatteryStatus;
	}else{
		system("i2cget -y 1 0x55 0x2c > /tmp/BatteryChargeStatus 2>/dev/null");
		if((pp = popen("cat /tmp/BatteryChargeStatus", "r"))==NULL){
			DBGMSG("BatteryStatus create popen() fail.\n"); 
			return -1;
		}else{
			memset(buf, 0, sizeof(buf));
			if(fgets(buf, sizeof(buf), pp)!=NULL){
				sscanf(buf, "%x", &BatteryStatus);
			}
		}
		pclose(pp);

//		printf("%s : %d : BatteryStatus = %x\n", __func__, __LINE__, BatteryStatus); // delete
//		printf("%s : %d : BatteryStatus = %d\n", __func__, __LINE__, BatteryStatus); // delete
		return BatteryStatus;
	} // GPIOHighLow condition
}

int Battery_Charge_Status()
{
	int GPIOHighLow = 0; // High = 1, is SMBus battery. Low = 0, is IIC Battery
	int BatteryChargeStatus = 65536;
	FILE *pp = NULL;
	char buf[80];
	
	GPIOHighLow = GPIO_Status();	
	
	if(GPIOHighLow == 1){
		system("echo \"r 0x0a\" > /proc/bb_smbus_reg");
		system("cat /proc/bb_smbus_reg > /tmp/batterySwitch");
		if((pp = popen("cat /tmp/batterySwitch", "r"))==NULL){
			DBGMSG("BatteryChargeStatus create popen() fail.\n");
			return -1;
		}else{
			memset(buf, 0, sizeof(buf));
			if(fgets(buf, sizeof(buf), pp)!=NULL){
				sscanf(buf, "%d", &BatteryChargeStatus);
			}
		}
		pclose(pp);
		return BatteryChargeStatus;
	}else{
		system("i2cget -y 1 0x55 0x14 w > /tmp/batterySwitch 2>/dev/null ");
		if((pp = popen("cat /tmp/batterySwitch", "r"))==NULL){
			DBGMSG("BatteryChargeStatus create popen() fail.\n");
			return -1;
		}else{
			memset(buf, 0, sizeof(buf));
			if(fgets(buf, sizeof(buf), pp)!=NULL){
				sscanf(buf, "%x", &BatteryChargeStatus);
			}
		}
		pclose(pp);
		
		/* If Battery status is discharge. */
		if(BatteryChargeStatus & 0x00008000)
			BatteryChargeStatus -= 65535;

//		printf("%s : %d : BatteryChargeStatus = %x\n", __func__, __LINE__, BatteryChargeStatus); // delete
//		printf("%s : %d : BatteryChargeStatus = %d\n", __func__, __LINE__, BatteryChargeStatus); // delete
		return BatteryChargeStatus;
	} // GPIOHighLow condition
}

int main(int argc, char **argv)
{
	int BatteryStatus = 10000;
	int BatteryChargeStatus = 10000;
	int ConnectedStatus = -1;
	BatteryStatus = Battery_Status();
//	printf("%s : %d : BatteryStatus = %x\n", __func__, __LINE__, BatteryStatus); // delete
	printf("%s : %d : BatteryStatus = %d\n", __func__, __LINE__, BatteryStatus); // delete
//	BatteryChargeStatus = Battery_Charge_Status();
//	printf("%s : %d : BatteryChargeStatus = %x\n", __func__, __LINE__, BatteryChargeStatus); // delete
//	printf("%s : %d : BatteryChargeStatus = %d\n", __func__, __LINE__, BatteryChargeStatus); // delete

	BatteryChargeStatus = SMBus_Battery_Charge_Status();
	printf("%s : %d : SMBus BatteryChargeStatus = %d\n", __func__, __LINE__, BatteryChargeStatus); // delete
	BatteryChargeStatus = IIC_Battery_Charge_Status();
	printf("%s : %d : IIC BatteryChargeStatus = %d\n", __func__, __LINE__, BatteryChargeStatus); // delete
	ConnectedStatus = Detect_Battery_Type();
	printf("%s : %d : ConnectedStatus = %d\n", __func__, __LINE__, ConnectedStatus); // delete
	return 0;
}
