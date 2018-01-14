#include "wizard.h"

IO_DATA global_pio_data;

int Information(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	char ret_str[64];
	IO_DATA pio_data;
	DIAG_RESULT prst;
	DIAG_CODE ret;
		
	hit = 0;
	
	memcpy(sndbuf, "BackdoorPacketRetrieveInformation_Ack", strlen("BackdoorPacketRetrieveInformation_Ack"));
	for( p=sndbuf ; *p ; p++ );

	/* do your test action */
	diag_parameters_init(&pio_data);
	ret = run_show_version(&pio_data, &prst);

	if(ret == DONE)
	{	
		strcpy(p,pio_data.u.cmt.version);
		snd_len = strlen("BackdoorPacketRetrieveInformation_Ack") + strlen(pio_data.u.cmt.version);
	}
	else
		snd_len = strlen("BackdoorPacketRetrieveInformation_Ack") ;
	hit = 1;
	return hit;
}
