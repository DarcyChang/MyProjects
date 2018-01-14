ifneq ($(strip $(TOOLPREFIX)),)
CROSS:=$(TOOLPREFIX)
endif

CC = ${CROSS}gcc


#######################################################
# DIAGMON UTILITIES CONFIG                            #
#######################################################
CONFIG_COMMON_TOOL_SUPPORT = y
CONFIG_BASIC_UTILS_SUPPORT = y
CONFIG_CPU_UTILS_SUPPORT = y
CONFIG_DDR_MEMORY_UTILS_SUPPORT = n
CONFIG_NAND_FLASH_UTILS_SUPPORT = n
CONFIG_USB_UTILS_SUPPORT = y
CONFIG_SWITCH_UTILS_SUPPORT = n
CONFIG_WLAN_UTILS_SUPPORT = y
CONFIG_WATCHDOG_UTILS_SUPPORT = n
CONFIG_HW_BUTTON_UTILS_SUPPORT = y
CONFIG_LED_UTILS_SUPPORT = y
CONFIG_RS_485_UTILS_SUPPORT = n
CONFIG_HDD_UTILS_SUPPORT = y
CONFIG_PMIC_UTILS_SUPPORT = y
CONFIG_W3G_UTILS_SUPPORT = y
CONFIG_LTE_UTILS_SUPPORT = y
CONFIG_SIM_CARD_UTILS_SUPPORT = y
CONFIG_RTC_UTILS_SUPPORT = n
CONFIG_BATTERY_UTILS_SUPPORT = y
CONFIG_ETHERNET_PHY_UTILS_SUPPORT = y
CONFIG_CLOUD_UTILS_SUPPORT = n
CONFIG_SD_CARD_UTILS_SUPPORT = y

CONFIG_NVRAM_SUPPORT = n
CONFIG_LIBOBJ_SUPPORT = n
CONFIG_GUCI_SUPPORT = n

#######################################################
# END DIAGMON UTILITIES CONFIG                        #
#######################################################

EXEC = diagmon
OBJS = diagmon.o diag_cmm.o diag_flags.o
LIBS = diag_cmm.o diag_flags.o

CFLAGS += $(TARGET_CFLAGS)

ifeq ($(CONFIG_COMMON_TOOL_SUPPORT),y)
OBJS +=	common_tools/common_tools.o
LIBS += common_tools/common_tools.o
CFLAGS += -DSUPPORT_COMMON_TOOL
endif

ifeq ($(CONFIG_BASIC_UTILS_SUPPORT),y)
OBJS +=	basic_utils/basic_utils.o

ifeq ($(CONFIG_CPU_UTILS_SUPPORT),y)
OBJS +=	basic_utils/cpu/cpu.o
LIBS += basic_utils/cpu/cpu.o
CFLAGS += -DSUPPORT_CPU_UTILS
endif

ifeq ($(CONFIG_DDR_MEMORY_UTILS_SUPPORT),y)
OBJS +=	basic_utils/ddr_memory/ddr_memory.o
LIBS += basic_utils/ddr_memory/ddr_memory.o
CFLAGS += -DSUPPORT_DDR_MEMORY_UTILS
endif

ifeq ($(CONFIG_NAND_FLASH_UTILS_SUPPORT),y)
OBJS +=	basic_utils/nand_flash/nand_flash.o
LIBS += basic_utils/nand_flash/nand_flash.o
CFLAGS += -DSUPPORT_NAND_FLASH_UTILS
endif

ifeq ($(CONFIG_USB_UTILS_SUPPORT),y)
OBJS +=	basic_utils/usb/usb.o
LIBS +=	basic_utils/usb/usb.o
CFLAGS += -DSUPPORT_USB_UTILS
endif

ifeq ($(CONFIG_SWITCH_UTILS_SUPPORT),y)
OBJS +=	basic_utils/switch/switch.o
LIBS += basic_utils/switch/switch.o
CFLAGS += -DSUPPORT_SWITCH_UTILS
endif

ifeq ($(CONFIG_WLAN_UTILS_SUPPORT),y)
OBJS +=	basic_utils/wlan/wlan.o
LIBS +=	basic_utils/wlan/wlan.o
CFLAGS += -DSUPPORT_WLAN_UTILS
endif

ifeq ($(CONFIG_WATCHDOG_UTILS_SUPPORT),y)
OBJS +=	basic_utils/watchdog/watchdog.o
LIBS += basic_utils/watchdog/watchdog.o
CFLAGS += -DSUPPORT_WATCHDOG_UTILS
endif

ifeq ($(CONFIG_HW_BUTTON_UTILS_SUPPORT),y)
OBJS +=	basic_utils/hw_button/hw_button.o
LIBS +=	basic_utils/hw_button/hw_button.o
CFLAGS += -DSUPPORT_HW_BUTTON_UTILS
endif

ifeq ($(CONFIG_LED_UTILS_SUPPORT),y)
OBJS +=	basic_utils/led/led.o
LIBS +=	basic_utils/led/led.o
CFLAGS += -DSUPPORT_LED_UTILS
endif

ifeq ($(CONFIG_RS_485_UTILS_SUPPORT),y)
OBJS +=	basic_utils/rs_485/rs_485.o
LIBS += basic_utils/rs_485/rs_485.o
CFLAGS += -DSUPPORT_RS_485_UTILS
endif
 
ifeq ($(CONFIG_HDD_UTILS_SUPPORT),y)
OBJS +=	basic_utils/hdd/hdd.o
LIBS += basic_utils/hdd/hdd.o
CFLAGS += -DSUPPORT_HDD_UTILS
endif

ifeq ($(CONFIG_PMIC_UTILS_SUPPORT),y)
OBJS +=	basic_utils/pmic/pmic.o
LIBS += basic_utils/pmic/pmic.o
CFLAGS += -DSUPPORT_PMIC_UTILS
endif

ifeq ($(CONFIG_W3G_UTILS_SUPPORT),y)
OBJS +=	basic_utils/w3g/w3g.o
LIBS += basic_utils/w3g/w3g.o
CFLAGS += -DSUPPORT_W3G_UTILS
endif

ifeq ($(CONFIG_LTE_UTILS_SUPPORT),y)
OBJS +=	basic_utils/lte/lte.o
LIBS += basic_utils/lte/lte.o
CFLAGS += -DSUPPORT_LTE_UTILS
endif

ifeq ($(CONFIG_SIM_CARD_UTILS_SUPPORT),y)
OBJS +=	basic_utils/sim_card/sim_card.o
LIBS += basic_utils/sim_card/sim_card.o
CFLAGS += -DSUPPORT_SIM_CARD_UTILS
endif

ifeq ($(CONFIG_RTC_UTILS_SUPPORT),y)
OBJS +=	basic_utils/rtc/rtc.o
LIBS += basic_utils/rtc/rtc.o
CFLAGS += -DSUPPORT_RTC_UTILS
endif

ifeq ($(CONFIG_BATTERY_UTILS_SUPPORT),y)
OBJS +=	basic_utils/battery/battery.o
LIBS += basic_utils/battery/battery.o
CFLAGS += -DSUPPORT_BATTERY_UTILS
endif

ifeq ($(CONFIG_ETHERNET_PHY_UTILS_SUPPORT),y)
OBJS +=	basic_utils/ethernet_phy/ethernet_phy.o
LIBS += basic_utils/ethernet_phy/ethernet_phy.o
CFLAGS += -DSUPPORT_ETHERNET_PHY_UTILS
endif

ifeq ($(CONFIG_CLOUD_UTILS_SUPPORT),y)
OBJS +=	basic_utils/cloud/cloud.o
LIBS += basic_utils/cloud/cloud.o
CFLAGS += -DSUPPORT_CLOUD_UTILS
endif

ifeq ($(CONFIG_SD_CARD_UTILS_SUPPORT),y)
OBJS +=	basic_utils/sdc/sdc.o
LIBS += basic_utils/sdc/sdc.o
CFLAGS += -DSUPPORT_SD_CARD_UTILS
endif
endif

	
CFLAGS += -I$(ROOTDIR)/$(LINUXDIR) -I./
CFLAGS += -DCONFIG_RALINK_MT7620

ifeq ($(CONFIG_NVRAM_SUPPORT),y)
CFLAGS += -I$(ROOTDIR)/nvram/include
CFLAGS += -DSUPPORT_NVRAM
LDFLAGS += -L$(ROOTDIR)/lib/libnvram -lnvram
endif

ifeq ($(CONFIG_LIBOBJ_SUPPORT),y)
CFLAGS += -DOBJ_X86_NVRAM
CFLAGS += -DSUPPORT_LIBOBJ

CFLAGS +=  -I$(ROOTDIR)/lib/libobj
LDFLAGS += -L$(ROOTDIR)/lib/libobj -lobj

CFLAGS +=  -I$(ROOTDIR)/lib/scew-0.4.0
LDFLAGS +=  -lscew 

CFLAGS += -I$(ROOTDIR)/lib/redis-2.4.17/deps/hiredis
LDFLAGS += -L$(ROOTDIR)/lib -lhiredis
endif

ifeq ($(CONFIG_GUCI_SUPPORT),y)
CFLAGS += -DSUPPORT_GUCI
endif

diag_dir_y	+= modules

all: clean libdiags.a $(EXEC)
	for i in $(diag_dir_y) ; do make -C $$i $@ || exit $?; done

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

libdiags.a: $(LIBS)
	$(AR) $(ARFLAGS) $@ $?

romfs:
	$(ROMFSINST) /usr/bin/$(EXEC)
	$(ROMFSINST) /lib/libdiags.a
	for i in $(diag_dir_y) ; do make -C $$i $@ || exit $?; done

install:
	install -D -m 755 diagmon $(INSTALL_ROOT)/usr/bin/diagmon
	for i in $(diag_dir_y) ; do make -C $$i $@ || exit $?; done

clean:
	rm -f $(EXEC) $(OBJS) *.o *.a
	for i in $(diag_dir_y) ; do make -C $$i clean ; done


export CONFIG_NVRAM_SUPPORT
export CONFIG_LIBOBJ_SUPPORT
export CC INSTALL_ROOT
