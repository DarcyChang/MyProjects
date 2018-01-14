#include <stdio.h>
#include <data_struct.h>

IO_DATA global_pio_data;

void diag_parameters_init(IO_DATA *pio_data)
{
	//pio_data->backdoor.backdoor_call = ON;
}

int main(int argc, char *argv[])
{
	IO_DATA pio_data;
	DIAG_RESULT prst;
	DIAG_CODE ret;
	char ret_str[64];
	
	printf ("module_sample\n");
	prst.ret = UNSET;
	memset(ret_str, 0x0, sizeof(ret_str));
	prst.rst = ret_str;

	//diag_parameters_init(&pio_data);
	
	//ret = run_show_version(&pio_data, &prst);

	printf("prst.ret = %d, prst.rst = %s\n", prst.ret, prst.rst);
	clear_diag_result(prst);

	return 0;
}

