/*
 * SENAO simple Control GPIO pins.
 *
 * Copyright (c) 2018 SENAO Inc.
 *
 * Licensed under the GPL-2 or later.
 */

/*
GPIO
#define ChipcommonG_GP_DATA_IN  0x1800a000
#define ChipcommonG_GP_DATA_OUT 0x1800a004
#define ChipcommonG_GP_OUT_EN   0x1800a008
#define ChipcommonG_GP_TEST_INPUT 0x1800a03c
*/


#include <common.h>
#include <command.h>
#include <errno.h>
#include <dm.h>
#include <asm/gpio.h>
#include <asm/arch/socregs.h>
#include <asm/iproc-common/reg_utils.h>

#define DEBUG 0


int is_high(uint32_t tmp) {

#if defined(DEBUG) && DEBUG
	printf("[DEBUG] tmp 0x%x\n", tmp);
#endif
	if(tmp)
		return 1;
	return 0;
}


int gpio_read(uint32_t pin) {

	uint32_t val_in, val_out, val_enb;

#if defined(DEBUG) && DEBUG
	printf("[DEBUG] str_cmd %s\n", str_cmd);
	printf("[DEBUG] pin 0x%x\n", pin);
#endif

	val_in = reg32_read((volatile uint32_t *)ChipcommonG_GP_DATA_IN);
	val_in &= pin;
	val_out = reg32_read((volatile uint32_t *)ChipcommonG_GP_DATA_OUT);
	val_out &= pin;
	val_enb = reg32_read((volatile uint32_t *)ChipcommonG_GP_OUT_EN);
	val_enb &= pin;

	printf("Input : %d\n", is_high(val_in));
	printf("Output : %d\n", is_high(val_out));
	printf("Enable : %d\n", is_high(val_enb));

	return 0;
}


int gpio_write(char *str_cmd, uint32_t pin, int value) {

	uint32_t val;

#if defined(DEBUG) && DEBUG
	printf("[DEBUG] str_cmd %s\n", str_cmd);
	printf("[DEBUG] pin 0x%x\n", pin);
	printf("[DEBUG] value %d\n", value);
#endif

	if(!strcmp(str_cmd,"in"))
	{
		val = reg32_read((volatile uint32_t *)ChipcommonG_GP_DATA_OUT);
		val &= ~pin	;
#if defined(DEBUG) && DEBUG
		printf("[DEBUG] val 0x%x\n", val);
#endif
		reg32_write((volatile uint32_t *)ChipcommonG_GP_DATA_OUT, val); 

		val = reg32_read((volatile uint32_t *)ChipcommonG_GP_OUT_EN);
		if(value == 1)
			val |= pin;
		else if(value == 0)
			val &= ~pin;

#if defined(DEBUG) && DEBUG
		printf("[DEBUG] val 0x%x\n", val);
#endif
		reg32_write((volatile uint32_t *)ChipcommonG_GP_OUT_EN, val); 
	}		
	else if(!strcmp(str_cmd,"out"))
	{
		val = reg32_read((volatile uint32_t *)ChipcommonG_GP_DATA_OUT);
		val |= pin	;
#if defined(DEBUG) && DEBUG
		printf("[DEBUG] val 0x%x\n", val);
#endif
		reg32_write((volatile uint32_t *)ChipcommonG_GP_DATA_OUT, val); 

		val = reg32_read((volatile uint32_t *)ChipcommonG_GP_OUT_EN);
		if(value == 1)
			val |= pin;
		else if(value == 0)
			val &= ~pin;

#if defined(DEBUG) && DEBUG
		printf("[DEBUG] val 0x%x\n", val);
#endif
		reg32_write((volatile uint32_t *)ChipcommonG_GP_OUT_EN, val); 
	}
	else 
		return CMD_RET_USAGE;

	return 0;
}


int my_atoi(char *p) {
    int k = 0;
    while (*p) {
        k = (k<<3)+(k<<1)+(*p)-'0';
        p++;
     }
     return k;
}

static int do_gpioctl(cmd_tbl_t *cmdtp, int flag, int argc, char * const argv[])
{
	const char *str_rw = NULL;
	int str_gpio, value = -1;
	uint32_t pin;

	if(argc < 3) 
		return CMD_RET_USAGE;
	
	str_rw = argv[1];
	str_gpio = my_atoi(argv[2]);
	if(str_gpio < 0 || str_gpio > 15)
		return CMD_RET_USAGE;
	pin = 1 << str_gpio;

#if defined(DEBUG) && DEBUG
	printf("ChipcommonG_GP_DATA_IN 0x%x\n", ChipcommonG_GP_DATA_IN);
	printf("ChipcommonG_GP_DATA_OUT 0x%x\n", ChipcommonG_GP_DATA_IN);
	printf("ChipcommonG_GP_OUT_EN 0x%x\n", ChipcommonG_GP_OUT_EN);
	printf("ChipcommonG_GP_TEST_INPUT 0x%x\n", ChipcommonG_GP_TEST_INPUT);
	printf("[DEBUG] argc %d\n", argc);
	printf("[DEBUG] argv[0] %s\n", argv[0]);
	printf("[DEBUG] argv[1] %s\n", argv[1]);
	printf("[DEBUG] argv[2] %s\n", argv[2]);
	printf("[DEBUG] argv[3] %s\n", argv[3]);
	printf("[DEBUG] argv[4] %s\n", argv[4]);
	printf("[DEBUG] str_rw %s\n", str_rw);
	printf("[DEBUG] str_gpio %d\n", str_gpio);
	printf("[DEBUG] pin = 0x%x\n", pin);
#endif

	if(!strcmp(str_rw, "r"))
	{
#if defined(DEBUG) && DEBUG
		printf("[DEBUG] read\n");
#endif
		gpio_read(pin);
    }	
	else if(!strcmp(str_rw, "w"))
	{
#if defined(DEBUG) && DEBUG
		printf("[DEBUG] write\n");
#endif

		if(argc == 5)
			value = my_atoi(argv[4]);
#if defined(DEBUG) && DEBUG
		printf("[DEBUG] value %d\n", value);
#endif
		gpio_write(argv[3], pin, value);
		gpio_read(pin);
	}
	else
		return CMD_RET_USAGE;

	return 0;
}

U_BOOT_CMD(gpioctl, 5, 0, do_gpioctl,
        "v1.0.0 SENAO control gpio pins",
		"<r|w> <pin number, e.g., 1> <in|out|enb> <value, 0|1>\n"
        "   - read/write the specified gpio in/out/enable and pin number.\n"
        "   - pin number 0 ~ 15\n"
		"   - e.g.  gpioctl w pin_number out <0|1>\n"
		"           gpioctl w pin_number in <0|1>\n"
		"           gpioctl r pin_number");
