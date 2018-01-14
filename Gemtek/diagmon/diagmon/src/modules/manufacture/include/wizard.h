#ifndef __wizard_h__
#define __wizard_h__

#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <ctype.h>
#include <string.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/types.h>
#include <linux/if.h>
#include <linux/wireless.h>		/* for struct iwreq */
#include <feature.h>
#include <data_struct.h>
//#include <objApi.h>

#define MultiCastPort	  14675
#define MultiCastGroup	"234.2.2.9"
#define MAX_BUFFER_SIZE 1024
#define MAXSOCKFD       10

#if 1
#define DBGMSG(fmt, args...) printf("{%s}%s(%d): " fmt, __FILE__, __FUNCTION__, __LINE__, ##args)
#else
#define DBGMSG(fmt, args...)
#endif

extern struct sockaddr_in MultiCastServ, MultiCastCli;
extern int product_test(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf);
extern int getInterfaceHwAddr(char *interface, char *hwaddr);
extern int hit;
extern int ECfd;
extern int snd_len;
extern int Cli_sz;

struct wizard_handlers {
    char *pattern;
    int (*output)();
};

void diag_parameters_init(IO_DATA *pio_data);

#endif
