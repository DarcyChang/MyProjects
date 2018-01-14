#include "wizard.h"

int SDCardTest(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	char Action_Status;
	IO_DATA pio_data;
	DIAG_CODE ret;
	DIAG_RESULT prst;

	/* do your test action */
	diag_parameters_init(&pio_data);
	ret = UNSET;

	ret = run_sdc_traffic_test(&pio_data, &prst);

	if(ret == PASS) {
		Action_Status = '1'; //successful
	}else if(ret == STOP) {
		Action_Status = '2'; //stop
	}else if(ret == FAIL) {
		Action_Status = '3'; //failed	
	}else{
		Action_Status = '0'; //something error	
	}


	memcpy(sndbuf, "BackdoorPacketSDCardTest_Ack", sizeof("BackdoorPacketSDCardTest_Ack"));
	for( p=sndbuf ; *p ; p++ );

	memcpy(p, &Action_Status, sizeof(Action_Status));
	snd_len = strlen("BackdoorPacketSDCardTest_Ack") + sizeof(Action_Status);

	hit = 1 ;
	return hit;
}
