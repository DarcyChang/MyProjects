#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <mtd/mtd-user.h>
#include <linux/ioctl.h>
#include <libgen.h>
#include <sys/ioctl.h>

#include <libflash.h>

#include "crc32.h"
//#include <errUtils.h>
#include "chardev.h"

#if 0
#define DBGMSG(fmt, args...) printf("{%s}%s(%d): " fmt, __FILE__, __FUNCTION__, __LINE__, ##args)
#else
#define DBGMSG(fmt, args...)
#endif

#define DEVDUMP "/tmp/dev_dump.tmp"
#define FILENAME "/tmp/flashtester.tmp"
#define DEVICE1 "/dev/mtd1"
#define DEVICE2 "/dev/mtd2"
#define NOR_FLASH MTD_NORFLASH
#define NAND_FLASH MTD_NANDFLASH

#define NAND_FLASH_PROTECT_START_ADD 0x0
#define NAND_FLASH_PROTECT_SIZE 0x1000000 //16MB
#define NAND_FLASH_BACKUP_FILE "/tmp/nand_backup"
#define NOR_FLASH_BACKUP_FILE "/tmp/nor_backup"

#define VERIFY_SUCCESS -1

#define MAX_Dprintf 32

//#define MAX_TESTSIZE 0x2000000 //32MB
#define MAX_TESTSIZE 0x1000000 //32MB

#define Dprintf(fmt, args...) { \
	printf(fmt, ##args); \
	sprintf(error_message[error_index].err_str, fmt, ##args); \
	error_index++; \
	if ((MAX_Dprintf - 1) == MAX_Dprintf) { \
		sprintf(error_message[error_index].err_str, "MAX_Dprintf:[%d] is FULL!!!\n", MAX_Dprintf); \
	} \
}

// For mother test
#define GEN_FILE 0x1
#define CALC_CRC 0x2
#define NAND_ERASE 0x4
#define HEAD 0
#define MIDDLE 1
#define TAIL 2
#define MAX 3
#define PROTECT_FW_SIZE 0x400000 // 4MB
#define RESERVE_NAND_BAD_BLOCK 0x300000  // 3 MB
#define TEST_SIZE 0x100000	// 1 MB

int MINTEST_FLAG = 0;
//int ERR_FLAG = 0;
//int CONT_FLAG = 0;
//unsigned long erase_mini = 0x20000; // 128 KB
unsigned long erase_size = 0;
unsigned long erase_unit = 0;
unsigned long erase_mini = 0;
unsigned long flash_type = 0;
unsigned long flash_size = 0;
unsigned long device_offset = 0;
int cfe_size = 0;
char device_path[128];
int erase_diag = 0;

int error_index = 0;
typedef struct err_msg {
	char err_str[512];
} err_msg;

err_msg error_message[MAX_Dprintf];

int mother_test_flag = 0;
int gen_file_flag = 0; // 0x0:initial  0x1:generated file  0x2:calculated crc32  0x4:NAND flash erased all

unsigned long file_crc32(char *filename, size_t filesize)
{
	unsigned long file_crc = 0;
	void *start = NULL;
	int fd = -1; 

	DBGMSG("filename:[%s]  filesize:[0x%x]\n", filename, filesize);

	fd = open(filename, O_RDWR);
	if(fd < 0) {
		perror("open");
		Dprintf("open:[%s] fail!!!\n", filename);
	}
	else {
		start = mmap(NULL, filesize, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
	}

	if (start == MAP_FAILED) {
		perror("mmap failed");
		Dprintf("{%s}%s(%d): mmap FAIL!!!\n", __FILE__, __FUNCTION__, __LINE__);
	}
	else {
		file_crc = crc32(start, filesize);
		munmap(start, filesize);
	}
	if (fd >= 0) close(fd);
	
	DBGMSG("Count %s crc:[%lu]\n", filename, file_crc);

	return file_crc;
}

unsigned long verify_walk01(unsigned char *buf, unsigned int size, int mode)
{
	int result = VERIFY_SUCCESS, i, j;
	unsigned char check;
	unsigned char *check_p;

	check_p = buf;
	check = 0;
	for (i = 0; i < size; i++) {
		if (mode == 258) {
			check |= check_p[i];
		}
		else {
			check |= ~check_p[i];
		}
		//DBGMSG("check:[0x%x] i:[0x%x]\n", check, i);
		if ( (i % 8) == 7 ) {
			if (check != 0xff) {
				result++;
				printf("verify_walk01 FAIL!!!\n");
				i -= 7;
				for (j = 0; j < 8; j++) {
					if ( (check & 0x01) == 0x01 ) { 
						i++;
						check = check >> 1;
					}   
					else {
						result = i;
						break;
					}   
				}  
				break;
			}
			check = 0;
		}
	}
	return result;
}

int verify_dump_file(size_t size, int mode)
{
	int result = 0;
	int fd2 = -1;
	unsigned long bad_verify_offset = 0;
	void *start2 = NULL;

	fd2 = open(DEVDUMP, O_RDWR);
	if(fd2 < 0) {
		Dprintf("open:[%s] fail!!!\n", DEVDUMP);
		perror("open");
		result++;
	}
	if (!result) {
		start2 = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd2, 0);
		if (start2 == MAP_FAILED) {
			perror("mmap failed");
			Dprintf("{%s}%s(%d): mmap FAIL!!!\n", __FILE__, __FUNCTION__, __LINE__);
			result++;
		}
	}
	if (!result) {
		bad_verify_offset = verify_walk01(start2, size, mode);
		if (bad_verify_offset != VERIFY_SUCCESS) {
			result++;
		}
	}
	munmap(start2, size);
	if (fd2 >= 0) close(fd2);

	return result;
}

int verify_data(size_t size, int mode, unsigned long **device_crc)
{
	int result = 0;
	char sh_cmd[256];

	if (flash_type == NOR_FLASH) {
		result += norflash_tool_read(size, DEVDUMP);
		
	}
	else if (flash_type == NAND_FLASH) {
		printf("Start nanddump...\n");
		sprintf(sh_cmd, "nanddump -g -b -o -s 0x%x -l %d -f %s %s", (int)device_offset, size, DEVDUMP, device_path);
		DBGMSG("sh_cmd:[%s]\n", sh_cmd);
		result += system(sh_cmd);
	}

	if (mode > 256) {
		result += verify_dump_file(size, mode);
	}
	else {
		*device_crc = file_crc32(DEVDUMP, size);
		DBGMSG("*device_crc:[%lu]\n", *device_crc);
	}
	unlink(DEVDUMP);

	return result;
}

int print_result(int mode, int result, int file_crc, size_t size, unsigned long bad_verify_offset, unsigned long device_crc)
{
	if (mode == 257) {
		if (result == 0) {
			printf("Walk 0 test: PASS.\n");
		}
		else {
			Dprintf("Walk 0 test: FAIL!!!.\n");
			Dprintf("bad_verify_offset:[0x%x]\n", (int)bad_verify_offset);
			Dprintf("device_path:[%s] device_offset:[0x%x] size:[0x%x] physical_bad_addr:[0x%x]\n", device_path, (int)device_offset, size, (int)device_offset + (int)bad_verify_offset + cfe_size);
		}
	}
	else if (mode == 258) {
		if (result == 0) {
			printf("Walk 1 test: PASS.\n");
		}
		else {
			Dprintf("Walk 1 test: FAIL!!!.\n");
			Dprintf("bad_verify_offset:[0x%x]\n", (int)bad_verify_offset);
			Dprintf("device_path:[%s] device_offset:[0x%x] size:[0x%x] physical_bad_addr:[0x%x]\n", device_path, (int)device_offset, size, (int)device_offset + (int)bad_verify_offset + cfe_size);
		}
	}
	else {
		DBGMSG("file_crc:[%lu] device_crc:[%lu]\n", file_crc, device_crc);

		if (device_crc == file_crc) {
			printf("Size:[%d] mode:[%d] test: PASS.\n", size, mode);
		}
		else {
			Dprintf("Size:[%d] mode:[%d] test: FAIL!!!.\n", size, mode);
			result++;
		}
	}
	return result;
}

static void usage(char *argv0)
{
	printf("Usage: %s offset size mode device_path\n", basename(argv0));	
	printf("    offset: the device address offset (MUST be a multiple of offset_minimum erase size)\n");	
	printf("    size: test device size (MUST be a multiple of offset_minimum erase size)\n");	
	printf("    mode: 0 ~ 256, 256 is random, 257 is walk 0, 258 is walk 1\n");	
	printf("    device_path: mtd device path ex: /dev/mtd1\n");	
	printf("    BACKUP_WHOLE_NANDm: 0 is backup diagmon only,  1 is backup whole NAND flash\n");	
	printf("example:\n");	
	printf("    %s 0x400000 0x100000 256 1\n", basename(argv0));	
	printf("    %s mother MINTEST_FLAG\n", basename(argv0));	
	printf("    %s mother 1 0\n", basename(argv0));	
}

int gen_file(unsigned int size, int mode)
{
	int i, num, ret = 0,	walk_num = 0x80;
	FILE *fp = NULL;
	float percent;
	//unsigned char *file_buf = NULL;


	fp = fopen(FILENAME, "w+");
	if(fp == NULL){
		perror("fopen");
		Dprintf("fopen:[%s] FAIL!!!\n", FILENAME);
		ret = -1;
	}

	if (mode == 258) {  // walk 1
		for (i = 0; i < size; i++) {
			if (walk_num == 0x80) {
				walk_num = 1;
			}   
			else {
				walk_num = walk_num << 1;
			}   
			fprintf(fp, "%c", walk_num);
			if ((i % 1000000) == 0) {
				percent = (float) i/size;
				printf("Generate file ..... %.0f %% \n", 100*percent);
			}
		}
	}
	else if (mode == 257) { 	// walk 0
		for (i = 0; i < size; i++) {
			if (walk_num == 0x80) {
				walk_num = 1;
			}   
			else {
				walk_num = walk_num << 1;
			}   
			fprintf(fp, "%c", ~walk_num);
			if ((i % 1000000) == 0) {
				percent = (float) i/size;
				printf("Generate file ..... %.0f %% \n", 100*percent);
			}
		}
	}
	else if (mode == 256) { 	// random
		srand((int) time(0));
		for (i = 0; i < size; i++) {
			num = (int) (rand() % 256);
			//DBGMSG("num:[%d]\n", num);
			fprintf(fp, "%c", num);
			if ((i % 1000000) == 0) {
				percent = (float) i/size;
				printf("Generate file ..... %.0f %% \n", 100*percent);
			}
		}
	}
	else { 	// assigned char
		for (i = 0; i < size; i++) {
			fprintf(fp, "%c", mode);
			if ((i % 1000000) == 0) {
				percent = (float) i/size;
				printf("Generate file ..... %.0f %% \n", 100*percent);
			}
		}
	}

	if (i == size) {
		percent = (float) i/size;
		printf("Generate file ..... %.0f %% \n", 100*percent);
		printf("\n");
		ret = 0;
	}
	else {
		ret = -1;
	}

	fclose(fp);

	return ret;
}

/*
 * MEMGETREGIONCOUNT
 * MEMGETREGIONINFO
 */
static int getregions(struct region_info_user *regions, int *n)
{
	int i,err;
	int fd = -1; 

	DBGMSG("device_path:[%s]\n", device_path);
	if ((fd = open(device_path, O_SYNC | O_RDONLY)) < 0) {
		perror(device_path);
		Dprintf("open:[%s] FAIL!!!\n", device_path);
		return -1;
	}   

	err = ioctl (fd,MEMGETREGIONCOUNT,n);
	if (err) {
		close(fd);
		return (err);
	}

	for (i = 0; i < *n; i++)
	{
		regions[i].regionindex = i;
		err = ioctl (fd,MEMGETREGIONINFO,&regions[i]);
		if (err) {
			close(fd);
			return (err);
		}
	}
	close(fd);
	return (0);
}

int get_device_info(mtd_info_t *info)
{
	int ret = 0; 
	int fd = -1; 

	if ((fd = open(device_path, O_WRONLY)) < 0) {
		perror(device_path);
		Dprintf("open:[%s] FAIL!!!\n", device_path);
		return -1;
	}   

	if (ioctl(fd, MEMGETINFO, info) != 0) {
		perror(device_path);
		Dprintf("ioctl:[%s]\n", device_path);
		close(fd);
		return -1;
	}   

	close(fd);

	return ret;
}

int dev_backup_nand(unsigned int size, unsigned offset)
{
	int result = 0;
	char sh_cmd[256];
	printf("Start nanddump...\n");
	sprintf(sh_cmd, "nanddump -g -b -o -s 0x%x -l %d -f %s %s", offset, size, NAND_FLASH_BACKUP_FILE, device_path);
	DBGMSG("sh_cmd:[%s]\n", sh_cmd);
	result = system(sh_cmd);
	return result;
}

int dev_backup(unsigned int size, char *backup_file)
{
	unsigned long ret = 0;

   ret = norflash_tool_read(size, backup_file);
	return ret;
}

int flash_erase_all()
{
	char cmd_buf[128];
	int ret;

	printf("Start flash_eraseall...\n");
	sprintf(cmd_buf, "flash_eraseall --quiet %s", device_path);
	DBGMSG("cmd_buf:[%s]\n", cmd_buf);

	ret = system(cmd_buf);
	if (ret != 0) {
		printf("FAIL!!!\n");
		Dprintf("flash_eraseall FAIL!!!\n");
		ret = -1;
	}
	return ret;
}

int norflash_tool_erase_region(int offset, int size)
{
	char cmd_buf[128];
	int ret;

	sprintf(cmd_buf, "norflash_tool -m erase -o 0x%x -s 0x%x", (int)offset, (int)size);
	
	DBGMSG("cmd_buf:[%s]\n", cmd_buf);

	ret = system(cmd_buf);
	if (ret != 0) {
		//Dprintf("flash_erase FAIL!!!\n");
		ret = -1;
	}
	return ret;
}

int flash_erase_region(unsigned int offset, unsigned int size)
{
	char cmd_buf[128];
	int ret;

	printf("Start flash_erase...\n");
	sprintf(cmd_buf, "flash_erase %s 0x%x 0x%x > /dev/null", device_path, offset, (size -1) / erase_mini + 1);
	DBGMSG("cmd_buf:[%s]\n", cmd_buf);

	ret = system(cmd_buf);
	if (ret != 0) {
		Dprintf("flash_erase FAIL!!!\n");
		ret = -1;
	}
	return ret;
}

int norflash_tool_write(int test_offset, int test_size, char *filename)
{
	char cmd_buf[128];
	int ret;

	sprintf(cmd_buf, "norflash_tool -m write -o 0x%x -s 0x%x -f \"%s\"", (int)test_offset, test_size, filename);
	
	DBGMSG("cmd_buf:[%s]\n", cmd_buf);

	ret = system(cmd_buf);
	if (ret != 0) {
		//Dprintf("flash_erase FAIL!!!\n");
		ret = -1;
	}
	return ret;
}

int norflash_tool_read(int size, char *filename)
{
	char cmd_buf[128];
	int ret;

	sprintf(cmd_buf, "norflash_tool -m read -o 0x%x -s 0x%x -f \"%s\"", (int)device_offset, size, filename);
	DBGMSG("cmd_buf:[%s]\n", cmd_buf);

	ret = system(cmd_buf);
	if (ret != 0) {
		//Dprintf("flash_erase FAIL!!!\n");
		ret = -1;
	}
	return ret;
}

int dev_restore_nand(unsigned int offset, unsigned int size)
{
	int ret = 0;
	char sh_cmd[256];

	ret = flash_erase_region(offset, size);
	if (ret == 0) {
		printf("Start nandwrite...\n");
		sprintf(sh_cmd, "nandwrite -q -s 0x%x %s %s", offset, device_path, NAND_FLASH_BACKUP_FILE);
		DBGMSG("sh_cmd:[%s]\n", sh_cmd);
		ret = system(sh_cmd);
	}
	else {
		Dprintf("NAND flash erase FAIL!!!\n");
	}
	
	return ret;
}

int dev_restore(unsigned int test_offset, unsigned int test_size, char *backup_file)
{
	unsigned long ret = 0;

	ret += norflash_tool_erase_region(test_offset, test_size);
	if (ret == 0) {
		ret = norflash_tool_write(test_offset, test_size, backup_file);
	}
	else {
		printf("%s(%d) NOR flash erase FAIL!!!\n", __FUNCTION__, __LINE__);
	}

	return ret;
}

int check_arg(int offset, int size, int mode)
{
	int ret = 0;
	if (mode < 0 || mode > 258) {
		Dprintf("mode is out of range! \n\n");
		ret = -1;	
	}
	else if (size != erase_size) {
		Dprintf("size MUST be a multiple of offset_minimum erase size [0x%x] !!! size:[0x%x]\n", (int)erase_mini, (int)size);
		ret = -1;
	}
	else if (offset != device_offset) {
		Dprintf("offset MUST be a multiple of offset_minimum erase size [0x%x] !!! offset:[0x%x]\n", (int)erase_mini, (int)offset);
		ret = -1;
	}

	return ret;
}

#if 0
struct region_info_user {
	uint32_t offset;     /* At which this region starts,
								 * from the beginning of the MTD */
	uint32_t erasesize;     /* For this region */
	uint32_t numblocks;     /* Number of blocks in this region */
	uint32_t regionindex;
};
#endif

int global_var(size_t size, unsigned int offset)
{
	int i, n, ret = 0;
	mtd_info_t info;
	int erase_size_8k;
	int erase_unit_8k;
	int erase_size_64k;
	int erase_unit_64k;
	static struct region_info_user region[1024];

	ret += getregions(region, &n);
	if (ret == 0) {
		DBGMSG("region n:[%d]\n", n);
		for (i = 0; i < n; i++) {
			/*
			DBGMSG("region[%d].offset = 0x%.8x\n", i ,region[i].offset);
			DBGMSG("region[%d].erasesize = 0x%.8x\n", i, region[i].erasesize);
			DBGMSG("region[%d].numblocks = %d\n", i, region[i].numblocks);
			DBGMSG("region[%d].regionindex = %d\n\n", i, region[i].regionindex);
			*/
			erase_mini = region[i].erasesize;
		}
	}
	else {
		perror ("MEMGETREGIONCOUNT");
		return (1);
	}

	ret += get_device_info(&info);
	if (ret == 0) {
		/*
		DBGMSG("info.type:[%d] MTD_NANDFLASH:[%d] MTD_NORFLASH:[%d]\n",info.type, MTD_NANDFLASH, MTD_NORFLASH);
		DBGMSG("info.flags:[%d]\n", info.flags);
		DBGMSG("info.size:[%d]\n", info.size);
		DBGMSG("info.erasesize:[%d]\n", info.erasesize);
		DBGMSG("info.writesize:[%d]\n", info.writesize);
		DBGMSG("info.oobsize:[%d]\n", info.oobsize);
		DBGMSG("info.ecctype:[%d]\n", info.ecctype);
		DBGMSG("info.eccsize:[%d]\n", info.eccsize);
		*/

		flash_type = info.type;
		flash_size = info.size;
		if (erase_mini == 0) 
			erase_mini = info.erasesize;
		erase_unit = (size - 1) / erase_mini + 1;
		erase_size = erase_unit * erase_mini;
		// 8M NOR flash block size is 64KB at offset 0x10000
		//32M NOR flash block size is 128KB at offset 0x0

		/*	
		cfe_size = 0;
		if (info.size == (0x800000 - 0x10000)) {	// First NOR flash test region = 8MB - 64KB (CFE region) 
			cfe_size = 0x10000;
			erase_size_8k = 0x10000 - offset;
			if (erase_size_8k > 0) { 	// Don't confuse. This is a CFI bug from BCM. It is in order to avoid the bug.
				erase_size_64k = size - erase_size_8k;
				erase_unit_64k = erase_size_64k / 0x10000;
				erase_unit_8k = erase_size_8k / 0x2000;
				erase_unit = erase_unit_8k + erase_unit_64k;
			}
			else {
				erase_size_64k = size;
				erase_unit_64k = erase_size_64k / 0x10000;
				erase_unit = erase_unit_64k;
			}
		}
		else if (info.size == (0x2000000 - 0x20000)) {	// 32 MB First NOR flash
			cfe_size = 0x20000;
		}
		else {
			cfe_size = 0x10000; 		// Ponderoso2 8MB NOR flash with 64KB CFE
		}
		*/
		DBGMSG("erase_unit:[%d]\n", erase_unit);
	}
	else {
		Dprintf("Get get_device_info ERROR!!!\n");
		ret = -1;
	}

	if (offset == 0)
	{
		device_offset = 0;
	}
	else if (offset > 0) {
		device_offset = ((offset - 1) / erase_mini + 1) * erase_mini;
	}
	else {
		Dprintf("offset ERROR!!!\n");
		ret = -1;
	}
	return ret;
}

//int motherboard_flash_test(void)
int flashtester_mother(void)
{
	unsigned int mode = 0;
	unsigned int device_num, position = 0;
	int i = 0, ret = 0, i_mod, i_quo;
	//mode = 258;		// Walk 1
	//mode = 257;		// Walk 0
	//mode = 256;		// Random

	if (MINTEST_FLAG == 0) {
		mode = 256;
		position = MAX;
		for (i = 0; i < 2; i++) {
			device_num = i + 1;
			printf("\n");
			printf("=============== motherboard_flash_mode_test mode:[%d], device_num:[%d], position:[%d]===============\n", mode, device_num, position);
			ret = motherboard_flash_mode_test(mode, device_num, position);
			if (ret != 0) {
				ret =  -100;
				break;
			}
		}
	}
	else {
		for (i = 0; i < 6; i++) {
			i_mod = i % 3;	
			i_quo = i / 3;
			if (i_mod == 0) {
				mode = 258;
				position = HEAD;
			}
			else if (i_mod == 1) {
				mode = 257;
				position = MIDDLE;
			}
			else if (i_mod == 2) {
				mode = 256;
				position = TAIL;
			}

			if (i_quo == 0) {
				device_num = 1;
			}
			else {
				device_num = 2;
			}

			printf("=============== motherboard_flash_mode_test mode:[%d], device_num:[%d], position:[%d]===============\n", mode, device_num, position);
			ret = motherboard_flash_mode_test(mode, device_num, position);
			if (ret != 0) {
				ret =  -100;
				break;
			}
		}
	}

//	if (ret == 0) {
//		ret = system("check_badblocks");
//	}

	if (ret == 0) {
		printf("\nFlash Test is PASSED\n\n");
	}
	else {
		printf("\nFlash Test is FAILED\n\n");
	}
	
	return ret;
}

int check_arguments(int argc, char *argv[], int *offset, int *test_size, int *mode)
{
	int ret = 0;
	if ((argv[1] != NULL) && (strcmp(argv[1], "erase_diag") == 0)) {
		sprintf(device_path, "%s", DEVICE2);	// Diagmon is stored in NAND flash.
		flash_erase_all();
		//goto FAIL; //erase is finshed, NOT fail.
		ret = -1;	
	}
	else if( argc != 5) {
		DBGMSG("argc:[%d]\n", argc);
		usage(argv[0]);		
		ret = -1;	
	}
	else {
		sscanf(argv[1], "%x", offset);	
		sscanf(argv[2], "%x", test_size);
		*mode = atoi(argv[3]);
		sprintf(device_path, "%s", argv[4]);
	}

	if (ret == 0) {
		DBGMSG("offset:[0x%x]\n", *offset);
		DBGMSG("test_size:[0x%x]\n", *test_size);
		DBGMSG("mode:[%d]\n", *mode);
		DBGMSG("device_path:[%s]\n", device_path);

		memset(error_message, 0, sizeof(error_message));
	}
	else {
		return ret;
	}

	if (ret == 0) {
		ret = global_var(*test_size, *offset);
		if (ret != 0) {
			Dprintf("global_var get ERROR!!!\n");
			ret = -1;
		}
		ret = check_arg(*offset, *test_size, *mode);
	}

	if (ret != 0) 
		usage(argv[0]);		

	return ret;
}

int backup_data(unsigned int test_size, unsigned int offset)
{
	int ret = 0;

	if (flash_type == NOR_FLASH) {	// NOR flash have to backup and restore
		printf("NOR flash backup... device_path:[%s] device_offset:[0x%x] size:[0x%x]...\n", device_path, (int)device_offset, (int)test_size);

		if (test_size < MAX_TESTSIZE) {
			ret = global_var(test_size, offset);
			if (ret != 0) {
				Dprintf("global_var get ERROR!!!\n");
				ret = -1;
			}
			else {
				ret = dev_backup(test_size, NOR_FLASH_BACKUP_FILE);
			}
		}
		else {
			Dprintf("Test NOR flash size:[0x%x] greater than MAX_TESTSIZE:[0x%x]\n", test_size, MAX_TESTSIZE);
			ret = -1;
		}

		if (ret == -1 ) {
			Dprintf("Backup FAIL!\n");
		}
		else {
			printf("Backup OK!\n");
		}
	}
	else if (flash_type == NAND_FLASH) {	// NAND flash have to backup and restore
		printf("NAND flash backup... device_path:[%s] device_offset:[0x%x] size:[0x%x]...\n", device_path, (int)offset, (int)test_size);
		ret = dev_backup_nand(test_size, offset);
		if (ret == -1 ) {
			Dprintf("Backup FAIL!\n");
		}
		else {
			printf("Backup OK!\n");
		}
	}
	return ret;
}

int write_test_file(int offset, int size)
{
	int ret = 0;
	char sh_cmd[128];

	if (flash_type == NOR_FLASH) {
		//ret = flash_erase_region();
		ret = norflash_tool_erase_region(offset, size);
		if (ret == -1) {
			Dprintf("flash_erase FAIL!!!\n");
			//result++;
		}
		else {
			//ret = mtd_write_func(FILENAME, size, device_path, device_offset);
			ret = norflash_tool_write(offset, size, FILENAME);
		}
	}
	else if (flash_type == NAND_FLASH) {
		if ((gen_file_flag & NAND_ERASE) == 0) {
			ret = flash_erase_region(offset, size);
			gen_file_flag |= NAND_ERASE;
		}
		if (ret == -1) {
			printf("flash_eraseall FAIL!!!\n");
			//result++;
		}
		else {
			printf("Start nandwrite...\n");
			sprintf(sh_cmd, "nandwrite -q -s 0x%x -p %s %s", (int)device_offset, device_path, FILENAME);
			DBGMSG("sh_cmd:[%s]\n", sh_cmd);
			ret = system(sh_cmd);
		}
	}
	else {
		Dprintf("Unknow flash flash_type (NOR/NAND)! \n");
		//result++;
		ret = -1;
	}
	return ret;
}

int restore_data(unsigned int test_size, unsigned int test_offset)
{
	int ret = 0;
	if (flash_type == NOR_FLASH) {	// NOR flash have to backup and restore
		printf("NOR flash restore... device_path:[%s] test_offset:[0x%x] size:[0x%x]...\n", device_path, (int)test_offset, test_size);
		ret = dev_restore(test_offset, test_size, NOR_FLASH_BACKUP_FILE);
		if (ret == -1 ) {
			Dprintf("Restore FAIL!\n");
			//result++;
		}
		else {
			unlink(NOR_FLASH_BACKUP_FILE);
			printf("Restore OK!\n");
		}
	}
	else if (flash_type == NAND_FLASH) {	// NAND flash have to backup and restore
		printf("NAND flash restore... device_path:[%s] device_offset:[0x%x] ...\n", device_path, test_offset);
		ret = dev_restore_nand(test_offset, test_size);

		if (ret == -1 ) {
			Dprintf("Restore FAIL!\n");
			//result++;
		}
		else {
			unlink(NAND_FLASH_BACKUP_FILE);
			printf("Restore OK!\n");
		}
	}
	return ret;
}

int flashtester_main(unsigned int test_offset, unsigned int test_size, int mode)
{
	int result = 0, ret = 0, i = 0;
	int size = 0, offset = 0, size_run;
	int fd = 0, fd2 = 0;
	unsigned long file_crc = 0, device_crc = 0, bad_verify_offset = 0;
	void *start = NULL;
	void *start2 = NULL;
	unsigned char *dev_buf = NULL;
	char sh_cmd[256];

//Test Start ///////////////////////////////////////////////////////////////////
	gen_file_flag = 0;
	offset = test_offset;
	size = test_size;
	size_run = size;
	while ((size > 0) && (result == 0)) {
		if (size < MAX_TESTSIZE) {
			size_run = size;
			gen_file_flag = gen_file_flag & ~GEN_FILE;
			gen_file_flag = gen_file_flag & ~CALC_CRC;
		}
		else {
			size_run = MAX_TESTSIZE;
		}

		//Backup /////////////////////////////////////////////////
		ret = backup_data(size_run, offset);
		if (ret != 0) {
			DBGMSG("ERROR!!!\n");
			goto FAIL;
		}

		gen_file_flag = gen_file_flag & ~NAND_ERASE; // NAND flash MUST erase every time.
		//DBGMSG("gen_file_flag:[%d] size_run:[0x%x] size:[0x%x] offset:[0x%x]\n", gen_file_flag, size_run, size, offset);

		ret = global_var(size_run, offset);
		if (ret != 0) {
			Dprintf("global_var get ERROR!!!\n");
			goto FAIL;
		}
		
		printf("Start flash test...gen_file_flag:[%d] size_run:[0x%x] size:[0x%x] offset:[0x%x]\n", gen_file_flag, size_run, size, offset);
		//////// Generate test file and count its crc value ////////
		if ((gen_file_flag & GEN_FILE) == 0) {
			ret = gen_file(size_run, mode);
			gen_file_flag |= GEN_FILE;
		}

		if (ret != 0) {
			Dprintf("%s create fail!\n", FILENAME);
			goto FAIL;
		}
		else {
			//printf("%s create success...\n", FILENAME);
		}

		//mode = 258;    // Walk 1
		//mode = 257;    // Walk 0
		if ((mode <= 256) && (gen_file_flag & CALC_CRC) == 0) { 	// CRC is not required for Walk 1 and Walk 0 
			file_crc = file_crc32(FILENAME, size_run);
			gen_file_flag |= CALC_CRC;
		}

		//////// Write test file to flash ////////
		printf("Write test file to flash...\n");
		ret = write_test_file(offset, size_run);
		if (ret != 0) {
			DBGMSG("ERROR!!!\n");
			result++;
			goto FAIL;
		}

		//////// Verify the data in flash ////////
		printf("Verify the data in flash...\n");
		result = verify_data(size_run, mode, &device_crc);
		if (result) goto FAIL;

		//Restore ////////////////////////////////////////////////////
		ret = restore_data(size_run, offset);
		if (ret != 0) {
			DBGMSG("ERROR!!!\n");
			result++;
			goto FAIL;
		}

		//////// print the test result ////////
		result = print_result(mode, result, file_crc, size_run, bad_verify_offset, device_crc);
		if (result) goto FAIL;

		size -= size_run;
		offset += size_run;
	}

	if (mode <= 256) {
		unlink(FILENAME);
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

	if (fd >= 0) {
		close(fd);
	}
	if (start) {
		munmap(start, size);
	}
	if (fd2 >= 0) {
		close(fd2);
	}
	if (dev_buf) {
		free(dev_buf);
	}
	if (start2) {
		munmap(start2, size);
	}
	printf("result:[%d]\n", result);
	return result;
}

int motherboard_flash_mode_test(unsigned int mode, unsigned int device_num, unsigned int position)
{
	int i, ret = 0;
	char str[128];
	unsigned int test_offset = 0, test_size = 0;
	unsigned int offset_min = 0, offset_max = 0, size_max = 0;
	erase_mini = 0;

	DBGMSG("mode:[%d] device_num:[%d] position:[%d]\n", mode, device_num, position);

	if (device_num == 1) {
		sprintf(device_path, "/dev/mtd1");
	}
	else if (device_num == 2) {
		sprintf(device_path, "/dev/mtd2");
	}
	else {
		printf("error device_num\n");
		ret = -1;
		goto FAIL;
	}

	ret = global_var(0, 0);
	if (ret != 0) {
		Dprintf("global_var get ERROR!!!\n");
		goto FAIL;
	}

	if (flash_type == MTD_NORFLASH) {
		offset_max = ((flash_size) / erase_mini) * erase_mini - erase_mini;
	}
	else {
		offset_max = ((flash_size - RESERVE_NAND_BAD_BLOCK) / erase_mini) * erase_mini - erase_mini;
	}
	DBGMSG("offset_min:[0x%x]  offset_max:[0x%x]  erase_mini:[0x%x]\n", offset_min, offset_max, erase_mini);

	if (device_num == 1) {
		offset_min = PROTECT_FW_SIZE;
	}

	if (position == HEAD) {
		test_offset = (offset_min / erase_mini) * erase_mini;
	}
	else if (position == MIDDLE) {
		test_offset = (((offset_max + offset_min) / 2) / erase_mini) * erase_mini;

	}
	else if (position == TAIL) {
		test_offset = ((offset_max - TEST_SIZE) / erase_mini + 1) * erase_mini;
	}
	else if (position == MAX) {
		test_offset = offset_min;
	}


	if (test_offset % erase_mini != 0) {
		printf("ERROR: test_offset MUST be a multiple of offset_minimum erase size:[0x%x]\n", erase_mini);
		ret = -1;
		goto FAIL;
	}
	if ((test_offset > offset_max) || (test_offset < offset_min)) {
		printf("ERROR: test_offset out of range, offset_minimum:0x%x offset_maximum:0x%x\n", offset_min, offset_max);
		ret = -1;
		goto FAIL;
	}
	
	if (position == MAX) {
		if (flash_type == MTD_NORFLASH) {
			test_size = flash_size - PROTECT_FW_SIZE;
		}
		else {
			test_size = flash_size - RESERVE_NAND_BAD_BLOCK;
		}
	}
	else {
		test_size = TEST_SIZE;
	}

	if (test_size % erase_mini != 0) {
		printf("ERROR: test_size MUST be a multiple of offset_minimum erase test_size:[0x%x]\n", erase_mini);
		ret = -1;
		goto FAIL;
	}

	size_max = offset_max - offset_min + erase_mini;
	if (test_size > size_max) {
		printf("ERROR: test_size:[0x%x] out of range, size_max:[0x%x]\n", test_size, size_max);
		ret = -1;
		goto FAIL;
	}
	
	ret = global_var(test_size, test_offset);
	if (ret != 0) {
		Dprintf("global_var get ERROR!!!\n");
		goto FAIL;
	}

	DBGMSG("device_num:[0x%x] test_offset:[0x%x] test_size:[0x%x]\n", device_num, test_offset, test_size);
	ret = flashtester_main(test_offset, test_size, mode);

FAIL:
	return ret;
}

int main(int argc, char *argv[])
{
	int ret = 0;
	size_t test_size = 0, test_offset = 0;	// Variable test_xxxx is the parameter of program.
	int mode = 0;
	
	// Check paramters or Erase Diag ///////////////////////////////////////////
	if (argv[1] && strcmp(argv[1], "mother") == 0) {
		if (argv[2]) MINTEST_FLAG = atoi(argv[2]);
		mother_test_flag = 1;
		DBGMSG("MINTEST_FLAG:[%d]\n", MINTEST_FLAG);
		ret = flashtester_mother();
	}
	else {
		mother_test_flag = 0;
		ret = check_arguments(argc, argv, &test_offset, &test_size, &mode);
		if (ret != 0) {
			DBGMSG("ERROR!!!\n");
		}
		else {
			ret = flashtester_main(test_offset, test_size, mode);
		}
	}

	return ret;
}

