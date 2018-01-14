#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define RETRY_TIME 10

int main(int argc, char *argv[])
{
	int i, j;
	FILE *fp = NULL;
	char buf[16384];	// 16M
	struct timeval t1, t2;
	double timecost, totalcost = 0;	

	//for(i = 0; i < argc; i++)
		//printf("argv[%d]: %s\n",i ,argv[i]);

	for(j = 0; j < RETRY_TIME; j++) {

		fp = fopen(argv[1], "rb");

		if(fp == NULL) {
			printf("Open file error!\n");
			exit(1);
		}

		gettimeofday(&t1, NULL);

		while(!feof(fp)) {
			fread(&buf, atoi(argv[2]), 1, fp);
		}

		gettimeofday(&t2, NULL);

		fclose(fp);
		
		timecost = (t2.tv_sec - t1.tv_sec) * 1000.0;    // sec to ms
		timecost += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms	
		
		//printf("Code time cost(sec): %f\n", timecost/1000.0);
		totalcost += timecost;
	}
	
	printf("Read buffer size:%d \n", atoi(argv[2]));
	printf("Average run time(sec):%f \n", (totalcost/RETRY_TIME)/1000.0);
	return 0;
}
