#include <sys/types.h>
#include <sys/stat.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wizard.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

struct sockaddr_in MultiCastServ, MultiCastCli;
char rcvBuffer[1024];
char sendBuffer[1024];
int  ECerr;
struct in_addr interface_addr;
int ECnSize = sizeof(struct sockaddr_in );
struct ip_mreq mreq;
int hit = 0;
int snd_len = 0;
int Cli_sz = sizeof(struct sockaddr_in) ;
int ECfd = -1;
char MyIP[16] = "";


static void daemonize(void)
{
    pid_t pid, sid;

    /* already a daemon */
    if ( getppid() == 1 ) return;

    /* Fork off the parent process */
    pid = fork();
    if (pid < 0) {
        exit(EXIT_FAILURE);
    }
    /* If we got a good PID, then we can exit the parent process. */
    if (pid > 0) {
        exit(EXIT_SUCCESS);
    }

    /* At this point we are executing as the child process */

    /* Change the file mode mask */
    umask(0);

    /* Create a new SID for the child process */
    sid = setsid();
    if (sid < 0) {
        exit(EXIT_FAILURE);
    }

    /* Change the current working directory.  This prevents the current
       directory from being locked; hence not being able to remove it. */
    if ((chdir("/")) < 0) {
        exit(EXIT_FAILURE);
    }

    /* Redirect standard files to /dev/null */
    freopen( "/dev/null", "r", stdin);
    freopen( "/dev/null", "w", stdout);
    freopen( "/dev/null", "w", stderr);
}


void diag_parameters_init(IO_DATA *pio_data)
{
	memset(pio_data, 0x0, sizeof(*pio_data));
	
	pio_data->backdoor.backdoor_call = ON;

	return;
}

int validate_IP_belong_subnet_mask(char *ip, char *subnet_ip, int mask)
{
	long l_ip, l_subnet_ip, l_mask;
	

	l_ip = inet_network(ip);
	l_subnet_ip = inet_network(subnet_ip);

	l_mask = 0xffffffff << (32 - mask);

	//printf("l_mask = 0x%08x\n", l_mask);
	//printf("l_ip = 0x%08x\n", l_ip);
	//printf("l_subnet_ip = 0x%08x\n", l_subnet_ip);

	if ((l_ip & l_mask) == (l_subnet_ip & l_mask)) {
		//printf("%s is belong in %s/%d\n", ip, subnet_ip, mask);
		return 0;
	}

	return -1;
}

int getMyIP()
{
	int fd;
	int count = 0;
	struct ifreq ifr;

	while(1)
	{
		fd = socket(AF_INET, SOCK_DGRAM, 0);

		/* I want to get an IPv4 IP address */
		ifr.ifr_addr.sa_family = AF_INET;

		/* I want IP address attached to "br0" */
		printf("try to get ip via br-lan\n");
		strncpy(ifr.ifr_name, "br-lan", IFNAMSIZ-1);
		

		ioctl(fd, SIOCGIFADDR, &ifr);

		close(fd);

		/* display result */
		sprintf(MyIP, "%s", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));
		//printf("sin_addr = %s\n", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));

		if(validate_IP_belong_subnet_mask(MyIP, "192.168.0.0", 16) == 0) {
			break;
		}else {
			count++;
			if (count <= 10) {
				sleep(3);
				printf("Cannot get a legal ip, wait 3 seconds and try again.\n");
			}else {
				printf("Cannot get a legal ip, terminate wizard.\n");
				return -1;
			}
		}
	}
	
	return 0;
}



int Start_MultiCast()
{
    
	int	on = 1;
	unsigned char	loop = 0;
	unsigned char	ttl = 3;
	struct ip_mreq	mreq;

	ECfd = socket ( AF_INET, SOCK_DGRAM, 0 );
	if ( ECfd < 0 )
	{
		printf("Easyconf : Create multicast socket fail!\n" );
		return -1;
	}
	/*Manage the multicast Inquiry*/
	MultiCastServ.sin_family = AF_INET;
	/*MultiCastServ.sin_addr.s_addr = inet_addr( MultiCastGroup );*/
	MultiCastServ.sin_addr.s_addr = INADDR_ANY;
	MultiCastServ.sin_port = htons( MultiCastPort );
	if( setsockopt( ECfd, SOL_SOCKET, SO_REUSEADDR, (char*)&on, sizeof(on)) < 0 )
		printf("Easyconf : Fail to SetSockopt SO_REUSEADDR when Ezconf!!\n" );

	ECerr = bind ( ECfd, (struct sockaddr*)&MultiCastServ, sizeof ( struct sockaddr_in ) );
		
	if(  ECerr < 0 )
	{
		printf("Easyconf : MultiCastcast bind fail!! \n"  );
		return -1;
	}

	if( setsockopt( ECfd, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(loop) ) < 0 )
		printf("Easyconf : Fail to SetSockopt IP_MULTICAST_LOOP when Ezconf!!\n" );

	if( setsockopt( ECfd, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl)) < 0 )
		printf("Easyconf : Fail to SetSockopt IP_MULTICAST_TTL when Ezconf!!\n" );
	interface_addr.s_addr = inet_addr(MyIP);
	setsockopt( ECfd, IPPROTO_IP, IP_MULTICAST_IF, &interface_addr, sizeof(interface_addr) );

	mreq.imr_multiaddr.s_addr = inet_addr(MultiCastGroup);
	mreq.imr_interface.s_addr = inet_addr(MyIP);

	if( setsockopt ( ECfd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq) ) < 0 )
		printf("Easyconf : Fail to SetSockopt IP_ADD_MEMBERSHIP when Ezconf!!\n" );

	return 0;
}

int match( const char* pattern, const char* string )
{
	//printf("pattern= %s\n", pattern);
	//printf("string = %s\n", string);
	return memcmp(pattern, string, strlen(pattern));
}

int product_test(struct sockaddr_in Cli, char *rcvbuf, char *sndbuf)
{
	//Testing Result
	int found = 0;;
	struct wizard_handlers *handler;
	struct wizard_handlers wizard_handlers[] = {
#include <handlers.h>
		{ NULL, NULL }
	};

	/* Clear the sndbuf */
	memset(sndbuf, 0, 1024);

	Cli.sin_family = AF_INET;
	Cli.sin_addr.s_addr = inet_addr ( MultiCastGroup );
	Cli.sin_port = htons ( MultiCastPort );

	for (handler = &wizard_handlers[0]; handler->pattern; handler++) {
		if (0 == match(handler->pattern, rcvbuf)) {
			if (handler->output) {
				found = 1;
				hit = handler->output(Cli, rcvbuf, sndbuf);
			}
		}
	}

	if ( found == 0) {
		printf("UNKNOWN PACKET\n");	
		printf("rcvbuf = %s\n", rcvbuf);
	} else {
		found = 0;
	} 

	//printf("sndbuf = [%s]\n", sndbuf);
	
	if(hit) {
		sendto(ECfd, sndbuf, snd_len, 0, ( struct sockaddr *)&Cli, Cli_sz);	
		return 1 ;	
	}		

	return 0 ;
}

int main(int argc, char **argv)
{
	int ret = 0;
	//Will be revocered for the final rlease
	ret = 1;

	//global_variable_init();

	//daemonize();

	printf("Easyconf : Start MAC writer\n" );

	if(getMyIP() == -1)
		return -1;
	
	ret = Start_MultiCast();

	while( 1 )
	{ 
		interface_addr.s_addr = inet_addr(MyIP);
		setsockopt( ECfd, IPPROTO_IP, IP_MULTICAST_IF, &interface_addr, sizeof(interface_addr) );

		mreq.imr_multiaddr.s_addr = inet_addr(MultiCastGroup);
		mreq.imr_interface.s_addr = inet_addr(MyIP);

		printf("\nEasyconf : MYIP is %s\n",MyIP);


		bzero(rcvBuffer,sizeof(rcvBuffer));

		//ECerr = recvfrom( ECfd, rcvBuffer, sizeof(rcvBuffer), 0, (struct sockaddr *)&MultiCastCli, (int *)&ECnSize );
		ECerr = recvfrom( ECfd, rcvBuffer, sizeof(rcvBuffer), 0, (struct sockaddr *)&MultiCastCli, (socklen_t *)&ECnSize );

		if( ECerr < 0 )
		{
			printf( "Easyconf : MultiCast process receive error!!\n" );
			continue;
		}
		else
		{		
			printf( "Easyconf : receive MultiCast Data!!\n" );
			product_test(MultiCastCli,rcvBuffer,sendBuffer);
		}		
	} /* end of while(1) */

	shutdown ( ECfd, 2 );
	close(ECfd);
	return ret;
}

