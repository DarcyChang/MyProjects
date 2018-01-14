/*
Linux I/O Port Control Command Set
Author: Eli Chang
*/
#include "io_control.h"

struct io_operation io_ops = {
	.count = 0, 
	.io_ctl = NULL
};

void ADD_IO_CONTROL(struct io_control io)
{
	if(!io_ops.count) {
		io_ops.io_ctl = (struct io_control *)malloc(sizeof(struct io_control));
		io_ops.io_ctl[io_ops.count++] = io;
	}
	else {
		struct io_control *tmp = NULL;
		tmp = (struct io_control *)realloc(io_ops.io_ctl, sizeof(struct io_control)*(io_ops.count+1));
		if(tmp) {
			io_ops.io_ctl = tmp;
			io_ops.io_ctl[io_ops.count++] = io;
		}
		else
			printf("Add new io command fault.\n");
	}
}

void RELEASE_IO_CONTROL(struct io_control *io_ctl)
{
	free(io_ctl);
}

int io_control_entry(char *entry)
{
	int idx;
	for(idx=0; idx<io_ops.count && strncmp(io_ops.io_ctl[idx].name, entry, 32); idx++)
		;
	return (idx<io_ops.count)?idx:-1;
}

void io_control_list_entry(void)
{
	int i;
	printf("Sub-Command Set:\n");
	for(i=0; i<io_ops.count; i++) {
		printf("%s\t", io_ops.io_ctl[i].name);
		if(!((i+1)%5))
			printf("\n");
	}
	printf("\n");
}
