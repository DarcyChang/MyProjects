#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include "chardev.h"

#define DEVICE "/dev/nordev"

unsigned int offset = 0;
unsigned int size = 0;
char *filename;
int method = 0;
unsigned int num = 0;

#define METHOD_READ 1
#define METHOD_WRITE 2
#define METHOD_ERASE 3
#define METHOD_PROTECT 4

#if 0
#define DBGMSG(fmt, args...) printf("{%s}%s(%d): " fmt, __FILE__, __FUNCTION__, __LINE__, ##args)
#else
#define DBGMSG(fmt, args...)
#endif

void usage(char *program)
{
	printf("usage:\n");
	printf("\t%s [options]\n", basename(program));
	printf("options:\n");
	printf("\t-m method: NOR flash read, write, erase or protect\n");
	printf("\t-o offset: NOR flash offset size\n");
	printf("\t-s size: read/write/erase size\n");
	printf("\t-f file: file path for store/read data from/to NOR flash\n");
	printf("example:\n");
	printf("\t%s -m read -o 0x100000 -s 0x200000 -f \"/tmp/read_nor.bin\"\n", basename(program));
	printf("\t%s -m protect 0xCCBBAA\n", basename(program));
	printf("\t\tAA: Status Register-1 value\n");
	printf("\t\tBB: Status Register-2 value\n");
	printf("\t\tCC: SPI flash command for read Status Register-2 command\n");
	printf("\t%s -m protect 0x3500B8 (Winbond: Protect address 0x000000 ~ 0x3FFFFF)\n", basename(program));
	printf("\t%s -m protect 0x35FFFF (Winbond: Show Status Register)\n", basename(program));
	printf("\t%s -m protect 0x15089C (MXIC: Protect address 0x000000 ~ 0x3FFFFF)\n", basename(program));
	printf("\t%s -m protect 0x15FFFF (MXIC: Show Status Register)\n", basename(program));
}

int options(int argc, char *argv[])
{
	int ch, ret = 0;
	unsigned char boolean = 0;
	char *ptr = NULL;

	if ((argc < 5) && (strcmp(argv[2], "protect") != 0)){
		usage(argv[0]);
		ret = 1;
	}   
	else {
		while ((ret == 0) && ((ch = getopt(argc, argv,"m:o:s:f:")) != -1)) {
			switch(ch) {
				case 'm':
					if (strncmp(optarg, "read", 4) == 0) {
						method = METHOD_READ;
					}
					else if (strncmp(optarg, "write", 5) == 0) {
						method = METHOD_WRITE;
					}
					else if (strncmp(optarg, "erase", 5) == 0) {
						method = METHOD_ERASE;
					}
					else if (strncmp(optarg, "protect", 7) == 0) {
						if (strncmp(argv[3], "0x", 2) == 0) {
							sscanf(argv[3], "0x%x", &num);
						}
						else {
							ret = 1;
						}

						method = METHOD_PROTECT;
						if (ret == 1) {
							usage(argv[0]);
						}
					}
					else {
						usage(argv[0]);
						ret = 1;
					}
					break;
				case 'o':
					if (strncmp(optarg, "0x", 2) == 0) {
						sscanf(optarg, "0x%x", &offset);
					}
					else {
						offset = atoi(optarg);
					}
					DBGMSG("option offset:[0x%x]\n", offset);
					break;
				case 's':
					if (strncmp(optarg, "0x", 2) == 0) {
						sscanf(optarg, "0x%x", &size);
					}
					else {
						size = atoi(optarg);
					}
					DBGMSG("option size:[0x%x]\n", size);
					break;
				case 'f':
					filename = optarg;
					DBGMSG("option filename:[%s]\n", filename);
					break;
				default:
					DBGMSG("other option:[%c]\n", ch);
					usage(argv[0]);
					ret = 1;
					break;
			}
		}
	}
	return ret;
}

int read_main()
{
	int fd = 0, ret = 0;
	FILE *fp = NULL;
	unsigned int count = 0;
	char *buf_p = NULL;

	buf_p = malloc(size);
	if (buf_p == NULL) {
		printf("%s(%d): malloc fail!!!\n", __FUNCTION__, __LINE__);
		ret++;
		goto FAIL;
	}

	memset(buf_p, 0, size);

	*(unsigned int*)buf_p = offset;

	DBGMSG("offset:[0x%x]\n", offset);
	DBGMSG("buf_p[0]:[0x%x]\n", buf_p[0]);
	DBGMSG("buf_p[1]:[0x%x]\n", buf_p[1]);
	DBGMSG("buf_p[2]:[0x%x]\n", buf_p[2]);
	DBGMSG("buf_p[3]:[0x%x]\n", buf_p[3]);

	fd = open(DEVICE, O_RDONLY);
	if (fd == -1) {
		printf("%s(%d): open %s fail!!!\n", __FUNCTION__, __LINE__, DEVICE);
		ret++;	
		goto FAIL; 
	}

	count = read(fd, buf_p, size);
	DBGMSG("count:[%d] !!!\n", count);

	fp = fopen(filename, "w"); 
	if (fp == NULL) {
		printf("%s(%d): fopen %s fail!!!\n", __FUNCTION__, __LINE__, filename);
		ret++;	
		goto FAIL; 
	}
	fwrite(buf_p, 1, size, fp);

FAIL:
	if (buf_p) {
		free(buf_p);
		buf_p = NULL;
	}

	if (fd) {
		close(fd);
		fd = 0;
	}

	if (fp) {
		fclose(fp);
		fp = NULL;
	}
	return ret;
}

int write_main()
{
	int fd = 0, ret = 0;
	FILE *fp = NULL;
	unsigned int count = 0;
	char *buf_p = NULL;

	buf_p = malloc(size + 4);
	if (buf_p == NULL) {
		printf("%s(%d): malloc fail!!!\n", __FUNCTION__, __LINE__);
		ret++;
		goto FAIL;
	}

	memset(buf_p, 0, size + 4);

	*(unsigned int*)buf_p = offset;

	DBGMSG("offset:[0x%x]\n", offset);
	DBGMSG("buf_p[0]:[0x%x]\n", buf_p[0]);
	DBGMSG("buf_p[1]:[0x%x]\n", buf_p[1]);
	DBGMSG("buf_p[2]:[0x%x]\n", buf_p[2]);
	DBGMSG("buf_p[3]:[0x%x]\n", buf_p[3]);

	fp = fopen(filename, "r"); 
	if (fp == NULL) {
		printf("%s(%d): fopen %s fail!!!\n", __FUNCTION__, __LINE__, filename);
		ret++;	
		goto FAIL; 
	}
	fread(buf_p + 4, 1, size, fp);

	fd = open(DEVICE, O_WRONLY);
	if (fd == -1) {
		printf("%s(%d): open %s fail!!!\n", __FUNCTION__, __LINE__, DEVICE);
		ret++;	
		goto FAIL; 
	}

	count = write(fd, buf_p, size);
	DBGMSG("count:[%d] !!!\n", count);

FAIL:
	if (buf_p) {
		free(buf_p);
		buf_p = NULL;
	}

	if (fd) {
		close(fd);
		fd = 0;
	}

	if (fp) {
		fclose(fp);
		fp = NULL;
	}
	return ret;
}

int erase_main()
{
	int fd = 0, ret = 0;
	FILE *fp = NULL;
	unsigned int count = 0;
	char *buf_p = NULL;

	buf_p = malloc(8);
	if (buf_p == NULL) {
		printf("%s(%d): malloc fail!!!\n", __FUNCTION__, __LINE__);
		ret++;
		goto FAIL;
	}

	memset(buf_p, 0, 8);

	*(unsigned int*)buf_p = 0xFFFFFFFF;  //Erase command
	*(unsigned int*)(buf_p + 4) = offset;  //offset

	DBGMSG("offset:[0x%x]\n", offset);
	DBGMSG("buf_p[0]:[0x%x]\n", buf_p[0]);
	DBGMSG("buf_p[1]:[0x%x]\n", buf_p[1]);
	DBGMSG("buf_p[2]:[0x%x]\n", buf_p[2]);
	DBGMSG("buf_p[3]:[0x%x]\n", buf_p[3]);
	DBGMSG("buf_p[4]:[0x%x]\n", buf_p[4]);
	DBGMSG("buf_p[5]:[0x%x]\n", buf_p[5]);
	DBGMSG("buf_p[6]:[0x%x]\n", buf_p[6]);
	DBGMSG("buf_p[7]:[0x%x]\n", buf_p[7]);

	fd = open(DEVICE, O_WRONLY);
	if (fd == -1) {
		printf("%s(%d): open %s fail!!!\n", __FUNCTION__, __LINE__, DEVICE);
		ret++;	
		goto FAIL; 
	}

	count = write(fd, buf_p, size);
	DBGMSG("count:[%d] !!!\n", count);

FAIL:
	if (buf_p) {
		free(buf_p);
		buf_p = NULL;
	}

	if (fd) {
		close(fd);
		fd = 0;
	}

	return ret;
}

int protect_main()
{
	int fd = -1, ret = 0;

	DBGMSG("Start...num:[0x%x]\n", num);
	if ((fd = open(DEVICE, O_RDWR)) < 0) {
		perror(DEVICE);
		DBGMSG("open:[%s] FAIL!!!\n", DEVICE);
		ret = 1;
		goto FAIL;
	}   

	ret = ioctl(fd, IOCTL_BLOCK_PROTECT, num);
	DBGMSG("ret:[%d]\n", ret);


FAIL:
	if (fd >= 0)
		close(fd);

	return ret;
}

int main(int argc, char *argv[])
{
	int ret = 0;

	ret += options(argc, argv);

	if (ret != 0)
		goto FAIL;

	if (method == METHOD_READ) {
		ret += read_main();
	}
	else if (method == METHOD_WRITE) {
		ret += write_main();
	}
	else if (method == METHOD_ERASE) {
		ret += erase_main();
	}
	else if (method == METHOD_PROTECT) {
		ret += protect_main();
	}
	else
		ret++;

FAIL:
	return ret;
}


