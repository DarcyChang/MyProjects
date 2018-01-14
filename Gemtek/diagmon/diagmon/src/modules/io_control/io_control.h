#ifndef __IO_CONTROL_H__
#define __IO_CONTROL_H__

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define init __attribute__((constructor))

struct io_control {
	char name[32];
	int (*io_handler)(int, char**);
};

struct io_operation {
	int count;
	struct io_control *io_ctl;
};

void ADD_IO_CONTROL(struct io_control io);
void RELEASE_IO_CONTROL(struct io_control *io_ctl);
int io_control_entry(char *entry);
void io_control_list_entry(void);

#endif
