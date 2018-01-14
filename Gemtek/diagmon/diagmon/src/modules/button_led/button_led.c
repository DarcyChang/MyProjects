#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <poll.h>
#include <data_struct.h>

int fd;
IO_DATA global_pio_data;

void diag_parameters_init(IO_DATA *pio_data)
{
	//pio_data->backdoor.backdoor_call = ON;
}

int gpio_set_dir_in(int pin)
{
	return 0;
}

int gpio_read_bit(int idx, int *value)
{
	return 0;
}

int main(int argc, char *argv[])
{
	IO_DATA pio_data;
	DIAG_RESULT prst;
	DIAG_CODE ret;

	return 0;
}

