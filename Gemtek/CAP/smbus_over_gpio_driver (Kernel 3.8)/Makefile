
LOCAL_DIR := $(shell pwd)
KERNELDIR := $(OUTPUT_DIR)/kernel-build
KBUILD_EXTRA_SYMBOLS := $(TOP)/HAL_GPIO_API/Module.symvers
export KBUILD_EXTRA_SYMBOLS

obj-m := smbus_over_gpio.o

all:
	$(MAKE) -C $(KERNELDIR) M=$(LOCAL_DIR) modules
	cp $(LOCAL_DIR)/smbus_over_gpio.ko $(OUTPUT_DIR)/lib/modules/ -f 

clean:
	-rm -f $(LOCAL_DIR)/smbus_over_gpio.o
	-rm -f $(LOCAL_DIR)/smbus_over_gpio.o.cmd
	-rm -f $(LOCAL_DIR)/smbus_over_gpio.ko
	-rm -f $(LOCAL_DIR)/.smbus_over_gpio.*
	-rm -f $(LOCAL_DIR)/smbus_over_gpio.mod.*
	-rm -f $(LOCAL_DIR)/modules.order
	-rm -f $(LOCAL_DIR)/Module.symvers
	-rm -f $(OUTPUT_DIR)/lib/modules/smbus_over_gpio.ko
	-rm -rf $(LOCAL_DIR)/.tmp_versions

