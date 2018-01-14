#include "io_util.h"
#include "io_control.h"

static bool w_flag=false;
static bool r_flag=true;
static bool MFG_flag=false;

static void inline DisableWrite(void) {w_flag = false;}
static void inline EnableWrite(void) {w_flag = true;}
static void inline DisableRead(void) {r_flag = false;}
static void inline EnableRead(void) {r_flag = true;}
static void inline DisableMFG(void) {MFG_flag = false;}
static void inline EnableMFG(void) {MFG_flag = true;}

void mmap_ioport_usage_menu(void)
{
	printf("Linux Memory Mapping I/O Access Tool.\n");
	printf("Author: Eli Chang\n\n");
	printf( "Arguments:\n"
			"\t-b - Base Address\n"
			"\t-M - MFG Flag\n"
			"\t-o - Offset Address\n"
			"\t-r - Read Mode\n"
			"\t-v - Setting Value\n"
			"\t-w - Write Mode\n"
	);
}

int mmap_ioport_main(int argc, char **argv)
{
	int chopt;
	unsigned int base_addr=0x00, port_offset=0x00;
	unsigned char data_val=0x00;
	if(argc < 2) {
		mmap_ioport_usage_menu();
		return 0;
	}
	while((chopt = getopt(argc, argv, "b:hMo:rv:w")) != -1 ) {
		switch(chopt) {
			case 'b': //base address
				base_addr = strtoul(optarg, NULL, 0);
				break;
			case 'M': //MFG Flag
				EnableMFG();
				break;
			case 'o': //offset
				port_offset = strtoul(optarg, NULL, 0);
				break;
			case 'r': //read
				break;
			case 'v':
				data_val = strtoul(optarg, NULL, 0);
				break;
			case 'w': //write
				EnableWrite();
				DisableRead();
				break;
			case 'h':
			default:
				mmap_ioport_usage_menu();
				return 0;
		}
	}

	initial_mmap_ioport();
	
	printf("Base Address:\t0x%02x\n", base_addr);
	printf("Port Offset:\t0x%02x\n\n", port_offset);
	if(r_flag) {
		mmap_ioport_read_byte(base_addr, port_offset, &data_val);
		printf("The value is 0x%02x\n", data_val);
	}
	else if(w_flag) {
		printf("Are you sure write the value [0x%02x]? \n[Y/N]---> ", data_val);
		if(MFG_flag)
			chopt = 'Y';
		else
			scanf("%c", (char*)&chopt);
		if((char)chopt == 'Y' || (char)chopt == 'y') {
			mmap_ioport_write_byte(base_addr, port_offset, &data_val);
			mmap_ioport_read_byte(base_addr, port_offset, &data_val);
			printf("The value is 0x%02x\n", data_val);
		}
		else
			printf("Not Chnage.\n");
	}
	
	exit_mmap_ioport();
	return 0;
}

void init register_mmap_ioport(void)
{
	struct io_control index_ioport = {
		.name = "mmio",
		.io_handler = mmap_ioport_main
	};

	ADD_IO_CONTROL(index_ioport);
}
