
TOP		:= $(shell pwd)
#DRIVER_DIR1	:= $(TOP)/RTL81XX_Driver_Package_Release_v3_2_20140402/DriverSrcPkg/driver/rtl8192cd/
#SCRIPT_DIR1	:= $(TOP)/RTL81XX_Driver_Package_Release_v3_2_20140402/ScriptFiles/script/
#AP_TOOL_DIR1	:= $(TOP)/RTL81XX_Driver_Package_Release_v3_2_20140402/DriverSrcPkg/users/
DRIVER_DIR1	:= $(TOP)/RTL81XX_Driver_Package_Release_v3_3_20150511/DriverSrcPkg/driver/rtl8192cd/
SCRIPT_DIR1	:= $(TOP)/RTL81XX_Driver_Package_Release_v3_3_20150511/ScriptFiles/script/
AP_TOOL_DIR1	:= $(TOP)/RTL81XX_Driver_Package_Release_v3_3_20150511/DriverSrcPkg/user/
SMBUS_DIR	:= $(TOP)/smbus_over_gpio_driver 
HAL_DIR	:= $(TOP)/HAL_GPIO_API 
PGTOOL_DIR 	:= $(TOP)/pgtool
ETH_DRIVER_DIR	:= $(TOP)/Realtek_r816x_ethernet
OUTPUT_DIR	:= $(TOP)/../output


export OUTPUT_DIR

.PHONY: all realtek_driver realtek_ap_daemon realtek_eth_driver pgtool smbus hal_gpio_api
#.PHONY: all realtek_eth_driver pgtool smbus hal_gpio_api

all:realtek_driver realtek_ap_daemon realtek_eth_driver pgtool smbus hal_gpio_api

realtek_driver:
#	make -C $(DRIVER_DIR)
#	cp $(DRIVER_DIR)/rtl8192cd.ko $(OUTPUT_DIR)/
	make -C $(DRIVER_DIR1)
	cp $(DRIVER_DIR1)/rtl8192cd.ko $(OUTPUT_DIR)/lib/modules
	cp -rf $(SCRIPT_DIR1)/* $(OUTPUT_DIR)/usr/bin

realtek_ap_daemon:
#	make -C $(AP_TOOL_DIR) CC="gcc -m32"
#	cp $(AP_TOOL_DIR)/bin/ $(OUTPUT_DIR)/ap_tools/ -fr
	make -C $(AP_TOOL_DIR1)
	cp -rf $(AP_TOOL_DIR1)/bin/* $(OUTPUT_DIR)/usr/bin/

pgtool:
	make -C $(PGTOOL_DIR)

smbus:
	make -C $(SMBUS_DIR)

hal_gpio_api:
	make -C $(HAL_DIR)

realtek_eth_driver:
	make -C $(ETH_DRIVER_DIR)

clean:
	make -C $(DRIVER_DIR1) clean
	make -C $(AP_TOOL_DIR1) clean
	make -C $(PGTOOL_DIR) clean
	make -C $(SMBUS_DIR) clean
	make -C $(HAL_DIR) clean
	make -C $(ETH_DRIVER_DIR) clean
#	-rm $(OUTPUT_DIR)/lib/modules/rtl8192cd.ko
#	-rm $(OUTPUT_DIR)/usr/bin/1x-*.sh
#	-rm $(OUTPUT_DIR)/usr/bin/bridge.sh
#	-rm $(OUTPUT_DIR)/usr/bin/client_init.sh
#	-rm $(OUTPUT_DIR)/usr/bin/default_setting*.sh
#	-rm $(OUTPUT_DIR)/usr/bin/init.sh
#	-rm $(OUTPUT_DIR)/usr/bin/mywlan_8192c.sh
#	-rm $(OUTPUT_DIR)/usr/bin/wep-*.sh
#	-rm $(OUTPUT_DIR)/usr/bin/wlan*.sh
#	-rm $(OUTPUT_DIR)/usr/bin/wpa*.sh
#	-rm $(OUTPUT_DIR)/ap_tools/ -fr
