#include "wizard.h"

//typedef unsigned long DWORD;

struct RSSI_INFO 
{
	unsigned long RSSI;
	unsigned char reserved[100];
};

IO_DATA global_pio_data;

int GetRSSIStatus(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;
	//char ret_str[64];
    IO_DATA pio_data;
    DIAG_RESULT prst;
    DIAG_CODE ret = UNSET;
	struct RSSI_INFO RSSI_Info;

	/* do your test action */
	diag_parameters_init(&pio_data);
	memset(&RSSI_Info, 0x0, sizeof(RSSI_Info));
	
	printf("GetRSSIStatus\n");

    ret = run_show_w3g_rssi_info(&pio_data, &prst);
	//printf("pio_data.u.w3g.w3g_rssi = %d\n", pio_data.u.w3g.w3g_rssi);
	if (ret == DONE) {
    	RSSI_Info.RSSI = pio_data.u.w3g.w3g_rssi;
	}else {
		printf("run_show_w3g_rssi_info error!! \n");
	}
	
	memcpy(sndbuf, "BackdoorPacketGetRSSIStatus_Ack", sizeof("BackdoorPacketGetRSSIStatus_Ack"));
	for( p=sndbuf ; *p ; p++ );

	memcpy(p, &RSSI_Info, sizeof(RSSI_Info));
	snd_len = strlen("BackdoorPacketGetRSSIStatus_Ack") + sizeof(RSSI_Info);

	hit = 1 ;
	return hit;
}
