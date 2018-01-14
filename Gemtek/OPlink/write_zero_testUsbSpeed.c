#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define RETRY_TIME 10

int main(int argc, char *argv[])
{
	int i, j;
	char buf[1024];
	struct timeval t1, t2;
	double timecost, totalcost = 0;	


	sprintf(buf,"dd if=/dev/zero of=/media/mmcblk0p0/test_file bs=%dM count=%d", atoi(argv[1]), atoi(argv[2]));
	gettimeofday(&t1, NULL);

	system(buf);

	gettimeofday(&t2, NULL);
		
	timecost = (t2.tv_sec - t1.tv_sec) * 1000.0;    // sec to ms
	timecost += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms	
		
	
	printf("Write buffer size:%dM and file size:%d\n", atoi(argv[1]), atoi(argv[1])*atoi(argv[2]));
	printf("run time(sec):%f \n", timecost/1000.0);
	return 0;
}
