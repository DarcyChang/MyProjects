#include "wizard.h"

int Sample(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	char *p = rcvbuf ;

	memcpy(sndbuf, "String_Ack", sizeof("String_Ack"));
	for( p=sndbuf ; *p ; p++ );

	/* do your test action */


	snd_len = strlen("String_Ack") + 1 ;

	hit = 1 ;
	return hit;
}
