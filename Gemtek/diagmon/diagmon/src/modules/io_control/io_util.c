/*
Linux I/O Port Access API
Author: Eli Chang
*/
#include "io_util.h"

void print_byte_bit(unsigned char value)
{
	int i;
	for(i=7; i>=0; i--) {
		if((value>>i)&0x1)
			printf("1");
		else
			printf("0");
		if(!(i%4))
			printf(" ");
	}
	printf("\n");
}

/* ==================
   Index I/O Port API 
   ================== */

static int index_ioport_fd=-1;

int initial_index_ioport(void)
{
	if((index_ioport_fd = open("/dev/port", O_RDWR)) == -1) {
		perror("Initial Index I/O Port Fail");
		exit(errno);
	}
	return index_ioport_fd;
}

int exit_index_ioport(void)
{
	return close(index_ioport_fd);
}

void index_ioport_read_byte(
	unsigned int index_port, 
	unsigned int date_port, 
	unsigned char offset, 
	unsigned char *val)
{
	lseek(index_ioport_fd, index_port, SEEK_SET);
	write(index_ioport_fd, &offset, 1);
	lseek(index_ioport_fd, date_port, SEEK_SET);
	read(index_ioport_fd, val, 1);
}

void index_ioport_write_byte(
	unsigned int index_port, 
	unsigned int date_port, 
	unsigned char offset, 
	unsigned char *val)
{
	lseek(index_ioport_fd, index_port, SEEK_SET);
	write(index_ioport_fd, &offset, 1);
	lseek(index_ioport_fd, date_port, SEEK_SET);
	write(index_ioport_fd, val, 1);
}

void dump_index_ioport_map(unsigned int index_port, unsigned int data_port)
{
	printf("Index Port: 0x%02x, Date Port: 0x%02x\n", index_port, data_port);
	int i;
	unsigned char oft=0, data_val=0;
	printf("   ");
	for(i=0; i<16; i++)
		printf("%02X ", i);
	printf("\n");
	for(i=0; i<256; i++, oft=(unsigned char)i) {
		if(!(i%16))
			printf("%02X ", i);
		index_ioport_read_byte(index_port, data_port, oft, &data_val);
		printf("%02x ", data_val);
		if(!((i+1)%16))
			printf("\n");
	}
}

/* =============================
   Memory Mapping I/O Access API 
   ============================= */

static int mmap_ioport_fd=-1;

static void *fetch_mmap(off_t base_address)
{
	return mmap( 
		NULL, 
		getpagesize(), 
		PROT_READ|PROT_WRITE, 
		MAP_SHARED, 
		mmap_ioport_fd, 
		base_address
	);
}

int initial_mmap_ioport(void)
{
	if((mmap_ioport_fd = open("/dev/mem", O_RDWR)) == -1)
	{
		perror("Initial Memory Mapping I/O Port Fail");
		exit(errno);
	}
	return mmap_ioport_fd;
}

int exit_mmap_ioport(void)
{
	return close(mmap_ioport_fd);
}

void mmap_ioport_read_byte(off_t base_address, unsigned int offset, unsigned char *val)
{
	unsigned char *mp;
	volatile unsigned char *mpda;
	if((mp = (unsigned char *)fetch_mmap(base_address)) == MAP_FAILED) {
		perror("Memory Mapping Fault");
		exit(errno);
	}
	mpda = (volatile unsigned char *)mp;
	*val = *(mpda+offset);

	munmap(mp, getpagesize());
}

void mmap_ioport_write_byte(off_t base_address, unsigned int offset, unsigned char *val)
{
	unsigned char *mp;
	volatile unsigned char *mpda;
	if((mp = (unsigned char *)fetch_mmap(base_address)) == MAP_FAILED) {
		perror("Memory Mapping Fault");
		exit(errno);
	}
	mpda = (volatile unsigned char *)mp;
	*(mpda+offset) = *val;

	munmap(mp, getpagesize());
}
