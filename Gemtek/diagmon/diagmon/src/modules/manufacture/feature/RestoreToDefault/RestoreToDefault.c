#include "wizard.h"

IO_DATA global_pio_data;

int RestoreToDefault(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	IO_DATA pio_data;
	DIAG_RESULT prst;
	char Action_Status;
		

	memcpy(sndbuf, "BackdoorPacketRestoreToDefault_Ack", sizeof("BackdoorPacketRestoreToDefault_Ack"));
	for( p=sndbuf ; *p ; p++ );

	/* do your test action */
	Action_Status = '1'; //successful
	memcpy(p,&Action_Status,sizeof(Action_Status));
	snd_len = strlen("BackdoorPacketRestoreToDefault_Ack") + sizeof(Action_Status) ;
	sendto(ECfd, sndbuf, snd_len, 0, ( struct sockaddr *)&Cli, Cli_sz);

	run_restore_to_default(&pio_data, &prst);

	sleep(10);
	hit = 1 ;
	return hit;
}
