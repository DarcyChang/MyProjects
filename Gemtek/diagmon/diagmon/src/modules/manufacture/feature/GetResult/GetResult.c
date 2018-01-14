#include "wizard.h"

int GetResult(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	char testing_result[10];
	FILE *fp;

	strcpy(testing_result, "\0");

	memcpy(sndbuf, "BackdoorPacketRetrieveResultGetting_Ack", sizeof("BackdoorPacketRetrieveResultGetting_Ack"));
	for( p=sndbuf ; *p ; p++ );

	/* do your test action */
	if(access("/tmp/reset_button_result", R_OK) == 0){
		if(access("/tmp/wps_button_result", R_OK) == 0){
			strcpy(testing_result, "1");
		}else
			strcpy(testing_result, "0");
	}else
		strcpy(testing_result, "0");

	strcpy(p, testing_result);

	snd_len = strlen("BackdoorPacketRetrieveResultGetting_Ack") + strlen(testing_result) ;

	hit = 1 ;
	return hit;
}
