#include "io_control.h"

extern struct io_operation io_ops;

int main(int argc, char **argv)
{
	int entry_idx=-1;

	if(argc < 2) {
		io_control_list_entry();
		return 0;
	}

	if((entry_idx = io_control_entry(argv[1])) != -1) {
		printf("Run Sub-Command: %s\n", io_ops.io_ctl[entry_idx].name);
		io_ops.io_ctl[entry_idx].io_handler((argc-1), (argv+1));
	}
	else
		io_control_list_entry();

	RELEASE_IO_CONTROL(io_ops.io_ctl);
	return 0;
}
