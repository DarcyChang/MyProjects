#ifndef _DAIG_BASIC_UTILS_H_
#define _DAIG_BASIC_UTILS_H_


DIAG_CODE run_basic_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE basic_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

#ifdef SUPPORT_CPU_UTILS
extern DIAG_CODE cpu_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE cpu_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_DDR_MEMORY_UTILS
extern DIAG_CODE ddr_memory_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE ddr_memory_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_NAND_FLASH_UTILS
extern DIAG_CODE nand_flash_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE nand_flash_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_USB_UTILS
extern DIAG_CODE usb_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE usb_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_HW_BUTTON_UTILS
extern DIAG_CODE hw_button_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE hw_button_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_LED_UTILS
extern DIAG_CODE led_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE led_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_SWITCH_UTILS
extern DIAG_CODE switch_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE switch_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_WATCHDOG_UTILS
extern DIAG_CODE watchdog_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE watchdog_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_WLAN_UTILS
extern DIAG_CODE wlan_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE wlan_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_RS_485_UTILS
extern DIAG_CODE rs_485_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE rs_485_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_HDD_UTILS
extern DIAG_CODE hdd_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE hdd_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_PMIC_UTILS
extern DIAG_CODE pmic_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE pmic_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_W3G_UTILS
extern DIAG_CODE w3g_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE w3g_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_LTE_UTILS
extern DIAG_CODE lte_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE lte_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_SIM_CARD_UTILS
extern DIAG_CODE sim_card_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE sim_card_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_RTC_UTILS
extern DIAG_CODE rtc_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE rtc_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_BATTERY_UTILS
extern DIAG_CODE battery_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE battery_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_ETHERNET_PHY_UTILS
extern DIAG_CODE ethernet_phy_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE ethernet_phy_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_CLOUD_UTILS
extern DIAG_CODE cloud_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE cloud_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif
#ifdef SUPPORT_SD_CARD_UTILS
extern DIAG_CODE sdc_utils(IO_DATA *pio_data, DIAG_RESULT *prst);
extern DIAG_CODE sdc_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
#endif


DIAGS_NODE diag_basic_menu[]={
{'0', NULL, "Diagnostic Basic Utilities Menu\0", NULL, NULL, YES, NO, NO, NULL},
#ifdef SUPPORT_USB_UTILS	
{'0', "usb", "USB Utilities\0", NULL, usb_utils, YES, YES, YES, usb_uid_handle},
#endif
#ifdef SUPPORT_WLAN_UTILS
{'0', "wln", "WLAN Utilities\0", NULL, wlan_utils, YES, YES, YES, wlan_uid_handle},
#endif
#ifdef SUPPORT_HW_BUTTON_UTILS
{'0', "btn", "Hardware Button Utilities\0", NULL, hw_button_utils, YES, YES, YES, hw_button_uid_handle},
#endif
#ifdef SUPPORT_LED_UTILS
{'0', "led", "LEDs Utilities\0", NULL, led_utils, YES, YES, YES, led_uid_handle},
#endif
#ifdef SUPPORT_W3G_UTILS
{'0', "w3g" ,"3G Utilities\0", NULL, w3g_utils, YES, YES, YES, w3g_uid_handle},
#endif
#ifdef SUPPORT_LTE_UTILS
{'0', "lte", "LTE Utilities\0", NULL, lte_utils, YES, YES, YES, lte_uid_handle},
#endif
#ifdef SUPPORT_HDD_UTILS
{'0', "hdd", "HDD Utilities\0", NULL, hdd_utils, YES, YES, YES, hdd_uid_handle},
#endif
#ifdef SUPPORT_PMIC_UTILS
{'0', "pmc", "PMIC Utilities\0", NULL, pmic_utils, YES, YES, YES, pmic_uid_handle},
#endif
#ifdef SUPPORT_SIM_CARD_UTILS
{'0', "sim", "SIM Card Utilities\0", NULL, sim_card_utils, YES, YES, YES, sim_card_uid_handle},
#endif
#ifdef SUPPORT_RTC_UTILS
{'0', "rtc", "RTC Utilities\0", NULL, rtc_utils, YES, YES, YES, rtc_uid_handle},
#endif
#ifdef SUPPORT_BATTERY_UTILS
{'0', "bty", "BATTERY Utilities\0", NULL, battery_utils, YES, YES, YES, battery_uid_handle},
#endif
#ifdef SUPPORT_CPU_UTILS
{'0', "cpu", "CPU Utilities\0", NULL, cpu_utils, YES, YES, YES, cpu_uid_handle},
#endif
#ifdef SUPPORT_DDR_MEMORY_UTILS
{'0', "mem", "DDR Memory Utilities\0", NULL, ddr_memory_utils, YES, YES, YES, ddr_memory_uid_handle},
#endif
#ifdef SUPPORT_NAND_FLASH_UTILS
{'0', "nad", "NAND Flash Utilities\0", NULL, nand_flash_utils, YES, YES, YES, nand_flash_uid_handle},
#endif
#ifdef SUPPORT_SWITCH_UTILS
{'0', "swh", "Switch Utilities\0", NULL, switch_utils, YES, YES, YES, switch_uid_handle},
#endif
#ifdef SUPPORT_WATCHDOG_UTILS
{'0', "wdg", "Watchdog Utilities\0", NULL, watchdog_utils, YES, YES, YES, watchdog_uid_handle},
#endif
#ifdef SUPPORT_RS_485_UTILS
{'0', "485", "RS-485 Utilities\0", NULL, rs_485_utils, YES, YES, YES, rs_485_uid_handle},
#endif
#ifdef SUPPORT_ETHERNET_PHY_UTILS
{'0', "enp", "Ethernet PHY Utilities\0", NULL, ethernet_phy_utils, YES, YES, YES, ethernet_phy_uid_handle},
#endif
#ifdef SUPPORT_CLOUD_UTILS
{'0', "cld", "CLOUD Utilities\0", NULL, cloud_utils, YES, YES, YES, cloud_uid_handle},
#endif
#ifdef SUPPORT_SD_CARD_UTILS
{'0', "sdc", "SD Card Utilities\0", NULL, sdc_utils, YES, YES, YES, sdc_uid_handle}
#endif
};

#define SIZE_BASIC_UTILS_MENU (sizeof diag_basic_menu / sizeof(DIAGS_NODE))

#endif

