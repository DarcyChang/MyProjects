#ifndef __IO_UTIL_H__
#define __IO_UTIL_H__

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdbool.h>

void print_byte_bit(unsigned char value);

/* ==================
   Index I/O Port API 
   ================== */

int initial_index_ioport(void);
int exit_index_ioport(void);
void index_ioport_read_byte(unsigned int index_port, unsigned int date_port, unsigned char offset, unsigned char *val);
void index_ioport_write_byte(unsigned int index_port, unsigned int date_port, unsigned char offset, unsigned char *val);
void dump_index_ioport_map(unsigned int index_port, unsigned int data_port);

/* =============================
   Memory Mapping I/O Access API 
   ============================= */

int initial_mmap_ioport(void);
int exit_mmap_ioport(void);
void mmap_ioport_read_byte(off_t base_address, unsigned int offset, unsigned char *val);
void mmap_ioport_write_byte(off_t base_address, unsigned int offset, unsigned char *val);

#endif
