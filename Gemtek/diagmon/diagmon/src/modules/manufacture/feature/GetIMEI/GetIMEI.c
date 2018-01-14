#include "wizard.h"

struct IMEI_INFO
{
	unsigned char IMEI[20];
	unsigned char reserved[100];
};

int GetIMEI(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	struct IMEI_INFO IMEI_Info;
	IO_DATA pio_data;
    DIAG_RESULT prst;
    DIAG_CODE ret;

	hit = 0;

	/* do your test action */
	diag_parameters_init(&pio_data);
	ret = UNSET;
	memset(&IMEI_Info, 0x0, sizeof(IMEI_Info));
    ret = run_show_w3g_imei_info(&pio_data, &prst);
	
	if(ret == DONE) {
		strcpy(IMEI_Info.IMEI, pio_data.u.w3g.imei_code);
		strcpy(IMEI_Info.reserved, "3GIMEI");
	}else {
		strcpy(IMEI_Info.IMEI, "ERROR");
	}

	memcpy(sndbuf, "BackdoorPacketGetIMEI_Ack", sizeof("BackdoorPacketGetIMEI_Ack"));
	for( p=sndbuf ; *p ; p++ );

	memcpy(p,&IMEI_Info,sizeof(IMEI_Info));
    snd_len = strlen("BackdoorPacketGetIMEI_Ack")+sizeof(IMEI_Info);

	hit = 1 ;
	return hit;
}
