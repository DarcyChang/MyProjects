#ifndef _DAIG_DATA_STRUCT_H_
#define _DAIG_DATA_STRUCT_H_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <ctype.h>
#include <math.h>
#include <termios.h>
#include <fcntl.h>

#ifdef SUPPORT_NVRAM
#include <nvram_utils.h>
#endif

#ifdef SUPPORT_LIBOBJ
#include <objApi.h>
#include <objComm.h>
#endif

//#ifdef SUPPORT_GUCI
//#include <guci.h>
//#endif

#define ETH_PORT_NUM (3) //V2D2

typedef unsigned int uint;

typedef enum diag_code{
	UNSET = 0,
	DONE = 1,
	ERROR = 2,
	FAIL = 3,
	PASS = 4,
	ESC = 5,
	TOP = 6,
	QUIT = 7,
	ENTER = 8,
	RUN = 9,
	STOP = 10,
	ON = 11,
	OFF = 12,
	YES = 13,
	NO = 14,
	FLAG = 15,
	HELP = 16
}DIAG_CODE;

typedef enum country{
	RD_FCC = 1,
	RD_IC = 2,
	RD_ETSI = 3,
	RD_SPAIN = 4,
	RD_FRANCE = 5,
	RD_MKK = 6,
	RD_ISREAL = 7,
	RD_MKK1 = 8,
	RD_MKK2 = 9,
	RD_MKK3 = 10,
	RD_NCC = 11,
	RD_RUSSIAN = 12,
	RD_CN = 13,
	RD_GLOBAL = 14,
	RD_WORLDWIDE = 15
}COUNTRY;

typedef enum wifi_band{
	G_BAND = 1,
	A_BAND = 2
}WIFI_BAND;

typedef enum battery_status{
	INIT = 1,
	DIS_CHARGING = 2,
	FULLY_CHARGED = 3,
	FULLY_DIS_CHARGED = 4
}BATTERY_STAT;

typedef enum rtc_battery_status{
	RTC_BATTERY_NORMAL = 0,
	RTC_BATTERY_FAULT = 1
}RTC_BATTERY_STAT;


typedef struct io_data{
	union component{
		struct CPU{
			uint time_sec;
			uint pin_index;
			int value;
		}cpu;
		struct DDR_MEM{
			uint time_sec;
			uint offset;
			uint size;
		}mem;	
		struct NOR_FLASH{
			uint flash_index;
			uint time_sec;
			uint offset;
			uint size;
			char *file_path;
		}nor;
		struct NAND_FLASH{
			uint time_sec;
			uint mtd_num;
			uint offset;
			uint size;
			uint erase_size;
			char *file_path;
		}nand;
		struct USB{
			uint port_index;
			uint time_sec;
		}usb;
		struct SWITCH{
			uint port_index;
			uint port_mark[ETH_PORT_NUM];
			uint pattern_mode;
			char phy_mac[18];
		}eth;
		struct WLAN{
			uint time_sec;
			uint chip_index;
			uint if_enabled[8];
			char ssid[8][33];
			uint channel[2];
			COUNTRY country_code;
			uint antenna_idx;
			int wifi_rssi;		// dbm
			char wifi_g_mac[18];
			char wifi_a_mac[18];
			WIFI_BAND band;
		}wl;
		struct WATCHDOG{
		}wdg;
		struct HW_BUTTON{
		}btn;
		struct LED{
			uint led_idx;
			uint color_idx;
			uint behavior_mode;
		}led;
		struct UART{
			uint port_index;
		}uart;
		struct POE{
			uint chip_index;
			uint port_mark[ETH_PORT_NUM];
			uint reg_offset;
			uint reg_value;
		}poe;
		struct RTC{
			uint sec;
			uint min;
			uint hour;
			uint day;
			uint month;
			uint year;
			RTC_BATTERY_STAT battery_status_flag;
		}rtc;
		struct XDSL{
		}xdsl;
		struct QUACK{
			uint cookie_index;
			char *cookie_value;
		}quack;
		struct SIM_CARD{
			char imsi_code[32];
		}sim;
		struct W3G{
			char imei_code[16];
			uint antenna_idx;
			int w3g_rssi;
		}w3g;
		struct LTE{
			char imei_code[16];
			uint antenna_idx;
			int lte_rssi;
		}lte;
		struct BATTERY{
			uint rel_charge; // unit: 0~100%
			uint abs_charge; // unit: 0~100%
			BATTERY_STAT status;
			uint charge_current; //unit: mA
		}battery;
		struct CLOUD{
			char pincode[32];
		}cloud;
		struct COM_TOOL{
			char base_mac[18];
			char sn[32];
			char version[32];
		}cmt;	
	}u;

	struct COMMON{
		DIAG_CODE flag_continuous;
		DIAG_CODE flag_err_stop;
		DIAG_CODE flag_stopwatch;
		DIAG_CODE flag_debug;
		DIAG_CODE flag_show_uid;
		DIAG_CODE flag_show_flags;
	}com;
	
	struct COUNTER{
		uint executed_num;
		uint failed_num;
	}counter;

	struct STOPWATCH{
		time_t start_time;
		time_t stop_time;
		time_t exe_time;
	}stopwatch;

	struct LC_MENU_OP{
		DIAG_CODE show_menu;
		DIAG_CODE show_flags;
		DIAG_CODE show_prompt;
	}lc_menu_op;
	
	struct BACKDOOR{
		DIAG_CODE backdoor_call;  //ON, OFF
	}backdoor;

	struct RUN_LEVEL{
		char mode[32];  //mfg
	}run_level;
	
	char **argv;
	int argc;
}IO_DATA;


typedef struct diag_result{
	DIAG_CODE ret;
	char *rst;
}DIAG_RESULT;

typedef struct diags_node{
	char index; // a to z
	char *UID;
	char *menu_name;
	DIAG_CODE (*para_function)(IO_DATA *, DIAG_RESULT *);
	DIAG_CODE (*menu_function)(IO_DATA *, DIAG_RESULT *);
	DIAG_CODE visible;
	DIAG_CODE usable;
	DIAG_CODE uid_quick_runnable;
	DIAG_CODE (*command_function)(IO_DATA *, DIAG_RESULT *);
}DIAGS_NODE;


#endif

