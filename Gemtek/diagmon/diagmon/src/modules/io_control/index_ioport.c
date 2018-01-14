#include "io_util.h"
#include "io_control.h"

static bool w_flag=false;
static bool r_flag=true;
static bool view_flag=false;
static bool MFG_flag=false;

static void inline DisableWrite(void) {w_flag = false;}
static void inline EnableWrite(void) {w_flag = true;}
static void inline DisableRead(void) {r_flag = false;}
static void inline EnableRead(void) {r_flag = true;}
static void inline DisableView(void) {view_flag = false;}
static void inline EnableView(void) {view_flag = true;}
static void inline DisableMFG(void) {MFG_flag = false;}
static void inline EnableMFG(void) {MFG_flag = true;}

void index_ioport_usage_menu(void)
{
	printf("Linux Indexed I/O Port Access Tool.\n");
	printf("Author: Eli Chang\n\n");
	printf( "Arguments:\n"
			"\t-d - Date Port\n"
			"\t-i - Index Port\n"
			"\t-M - MFG Flag\n"
			"\t-o - Offset Address\n"
			"\t-r - Read Mode\n"
			"\t-s - Show Index I/O Port Map\n"
			"\t-v - Setting Value\n"
			"\t-w - Write Mode\n"
	);
}

int index_ioport_main(int argc, char **argv)
{
	int chopt;
	unsigned int idx_port=0x00, data_port=0x00;
	unsigned char data_val=0x00, port_offset=0x00;
	if(argc < 2) {
		index_ioport_usage_menu();
		return 0;
	}
	while((chopt = getopt(argc, argv, "d:hi:Mo:rsv:w")) != -1 ) {
		switch(chopt) {
			case 'd': //date port
				data_port = strtoul(optarg, NULL, 0);
				break;
			case 'i': //index port
				idx_port = strtoul(optarg, NULL, 0);
				break;
			case 'M': //MFG Flag
				EnableMFG();
				break;
			case 'o': //offset
				port_offset = strtoul(optarg, NULL, 0);
				break;
			case 'r': //read
				break;
			case 's': //view
				EnableView();
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
				index_ioport_usage_menu();
				return 0;
		}
	}

	initial_index_ioport();
	
	printf("Index Port:\t0x%02x\n", idx_port);
	printf("Date Port:\t0x%02x\n", data_port);
	if(!view_flag) {
		printf("Port Offset:\t0x%02x\n\n", port_offset);
		if(r_flag) {
			index_ioport_read_byte(idx_port, data_port, port_offset, &data_val);
			printf("The value is 0x%02x\n", data_val);
		}
		else if(w_flag) {
			printf("Are you sure write the value [0x%02x]? \n[Y/N]---> ", data_val);
			if(MFG_flag)
				chopt = 'Y';
			else
				scanf("%c", (char*)&chopt);
			if((char)chopt == 'Y' || (char)chopt == 'y') {
				index_ioport_write_byte(idx_port, data_port, port_offset, &data_val);
				index_ioport_read_byte(idx_port, data_port, port_offset, &data_val);
				printf("The value is 0x%02x\n", data_val);
			}
			else
				printf("Not Chnage.\n");
		}
	}
	else if(r_flag)
		dump_index_ioport_map(idx_port, data_port);
	
	exit_index_ioport();
	return 0;
}

void init register_index_ioport(void)
{
	struct io_control index_ioport = {
		.name = "idxio",
		.io_handler = index_ioport_main
	};

	ADD_IO_CONTROL(index_ioport);
}
