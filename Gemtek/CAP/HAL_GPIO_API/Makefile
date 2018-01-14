
LOCAL_DIR := $(shell pwd)
KERNELDIR := $(OUTPUT_DIR)/kernel-build

obj-m := hal_gpio_api.o

all:
	$(MAKE) -C $(KERNELDIR) M=$(LOCAL_DIR) modules
	cp $(LOCAL_DIR)/hal_gpio_api.ko $(OUTPUT_DIR)/lib/modules/ -f 

clean:
	-rm -f $(LOCAL_DIR)/hal_gpio_api.o
	-rm -f $(LOCAL_DIR)/hal_gpio_api.cmd
	-rm -f $(LOCAL_DIR)/hal_gpio_api.ko
	-rm -f $(LOCAL_DIR)/.hal_gpio_api.*
	-rm -f $(LOCAL_DIR)/hal_gpio_api.mod.*
	-rm -f $(LOCAL_DIR)/modules.order
	-rm -f $(LOCAL_DIR)/Module.symvers
	-rm -f $(OUTPUT_DIR)/lib/modules/hal_gpio_api.ko
	-rm -rf $(LOCAL_DIR)/.tmp_versions

