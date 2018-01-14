#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
//#include <errUtils.h>

#include <mtd/mtd-user.h>

#define NAND_DEVICE "/dev/mtd2"

#define ECCGETSTATS     _IOR('M', 18, struct mtd_ecc_stats)
#define MAX_BAD_BLOCKS 20

#if 0
#define DBGMSG(fmt, args...) printf("{%s}%s(%d): " fmt, __FILE__, __FUNCTION__, __LINE__, ##args)
#else
#define DBGMSG(fmt, args...)
#endif

#define MAX_Dprintf 32
#define Dprintf(fmt, args...) { \
	printf(fmt, ##args); \
	sprintf(error_message[error_index].err_str, fmt, ##args); \
	error_index++; \
	if ((MAX_Dprintf - 1) == MAX_Dprintf) { \
		sprintf(error_message[error_index].err_str, "MAX_Dprintf:[%d] is FULL!!!\n", MAX_Dprintf); \
	} \
}

int error_index = 0;
typedef struct err_msg {
	char err_str[512];
} err_msg;

err_msg error_message[MAX_Dprintf];

/*
 * struct mtd_ecc_stats - error correction stats
 *
 * @corrected: number of corrected bits
 * @failed: number of uncorrectable errors
 * @badblocks: number of bad blocks in this partition
 * @bbtblocks: number of blocks reserved for bad block tables
 */
/*
struct mtd_ecc_stats {
	uint32_t corrected;
	uint32_t failed;
	uint32_t badblocks;
	uint32_t bbtblocks;
};
*/

struct mtd_ecc_stats oldstats;
int check_badblocks(char *dev_path)
{
	int i, fd = -1, ret = 0;
	//fd = open(argv[optind], O_RDWR);
	fd = open(dev_path, O_RDWR);
	if (fd < 0) {
		perror("open");
		ret = 1;
		goto FAIL;
	}

	if (ioctl(fd, ECCGETSTATS, &oldstats)) {
		perror("ECCGETSTATS");
		ret = 1;
		goto FAIL;
	}   

	printf("ECC corrections: %d\n", oldstats.corrected);
	printf("ECC failures   : %d\n", oldstats.failed);
	printf("Bad blocks     : %d\n", oldstats.badblocks);
	printf("BBT blocks     : %d\n", oldstats.bbtblocks);

	if (oldstats.badblocks > MAX_BAD_BLOCKS) {
		Dprintf("The bad blocks number is greater than or equal to %d. Test FAIL!!!\n", MAX_BAD_BLOCKS);
		ret = 1;
	}
	else {
		printf("The bad blocks number is less then %d. Test OK!\n", MAX_BAD_BLOCKS);
	}

FAIL:
	//////// store error message to test result ////////
	if (error_index != 0) {
#if 0
		if(openErrLog() == 1) {
			printf("\n\n");
			errLog_setTitle("Fatal error #1 during Flash Tester test");
			errLog_setTest("Start Flash Tester test");
			for (i = 0; i < error_index; i++) {
				if (error_message[i].err_str == NULL) {
					break;
				}
				else {
					//errLog_addMsgFileOnly("%s", error_message[i].err_str);
					errLog_addMsg("%s", error_message[i].err_str);
				}
			}
			errLog_endMsg();
			errLog_endTest(1, "Flash Tester test");
			closeErrLog();
			printf("\n\n");
		}
#endif
	}

	if (fd >= 0)
		close(fd);

	return ret;
}

int show_badblocks_addr(unsigned long *start_addr, unsigned long *end_addr, char *dev_path)
{
	int i, fd = -1, ret = 0;
	mtd_info_t meminfo;
	unsigned long ofs = 0, flash_blocksize = 0, flash_writesize = 0;
	unsigned long long blockstart = 1;
	int badblock = 0, badblock_count = 0;

	fd = open(dev_path, O_RDWR);
	if (fd < 0) {
		perror("open");
		ret = 1;
		goto FAIL;
	}

	/* Fill in MTD device capability structure */
	if (ioctl(fd, MEMGETINFO, &meminfo) != 0) {
		perror("MEMGETINFO");
		close(fd);
		exit (EXIT_FAILURE);
	} 

	printf("=============MEMGETINFO=============\n");
	printf("meminfo.type:[%d] MTD_NANDFLASH:[%d] MTD_NORFLASH:[%d]\n",meminfo.type, MTD_NANDFLASH, MTD_NORFLASH);
	printf("meminfo.flags:[%d]\n", meminfo.flags);
	printf("meminfo.size:[%d]\n", meminfo.size);
	printf("meminfo.erasesize:[%d]\n", meminfo.erasesize);
	printf("meminfo.writesize:[%d]\n", meminfo.writesize);
	printf("meminfo.oobsize:[%d]\n", meminfo.oobsize);
	printf("meminfo.ecctype:[%d]\n", meminfo.ecctype);
	printf("meminfo.eccsize:[%d]\n", meminfo.eccsize);
	printf("====================================\n");

	flash_writesize = meminfo.writesize;
	flash_blocksize = meminfo.erasesize;

	for (ofs = start_addr; ofs < end_addr ; ofs += flash_writesize) {
		badblock = 0;
		// new eraseblock , check for bad block
		if (blockstart != (ofs & (~meminfo.erasesize + 1))) {
			blockstart = ofs & (~meminfo.erasesize + 1);
			if ((badblock = ioctl(fd, MEMGETBADBLOCK, &blockstart)) < 0) {
				perror("ioctl(MEMGETBADBLOCK)");
				goto FAIL;
			}
		}

		if (badblock) {
			badblock_count++;
			printf("\n========= The %d bad block =========\n", badblock_count);
			printf("bad block address: 0x%08x\n", ofs);
		}
	}

FAIL:
	//////// store error message to test result ////////

	if (fd >= 0)
		close(fd);

	return ret;
}

static void usage(char *argv0)
{
	printf("Usage: %s start_addr end_addr device_path\n", basename(argv0));	
	printf("    start_addr: MTD offset that start to check bad block address\n");	
	printf("    end_addr: MTD offset that the end of check bad block address\n");	
	printf("    device_path: MTD device path\n");	
	printf("example:\n");	
	printf("    %s /dev/mtd4\n", basename(argv0));	
	printf("    %s 0x0 0x8000000 /dev/mtd4\n", basename(argv0));	
}

int main(int argc, char *argv[])
{
	int result = 0;
	unsigned long start_addr = 0, end_addr = 0;
	char dev_path[128];
	DBGMSG("argc:[%d]\n", argc);
	if (argc == 4) {
		sscanf(argv[1], "0x%x", &start_addr);
		sscanf(argv[2], "0x%x", &end_addr);
		sprintf(dev_path, "%s", argv[3]);
		DBGMSG("start_addr:[0x%x] end_addr:[0x%x] dev_path:[%s]\n", start_addr, end_addr, dev_path);
		result += show_badblocks_addr(start_addr, end_addr, dev_path);
	}
	else if (argc == 2) {
		sprintf(dev_path, "%s", argv[1]);
		result += check_badblocks(dev_path);
	}
	else {
		usage(argv[0]);		
	}
	return result;
}

