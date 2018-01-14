#include <linux/version.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/stddef.h>
#include <linux/kernel.h>
#include <linux/ioport.h>
#include <linux/ctype.h>
#include <linux/gpio.h>

#define HAL_GPIO_API_VERSION "1.0"

static int hal_gpio_request(unsigned gpio, const char *label)
{
	return gpio_request(gpio, label);
}
EXPORT_SYMBOL(hal_gpio_request);

static int hal_gpio_get_value(unsigned int gpio)
{
    return gpio_get_value(gpio);
}
EXPORT_SYMBOL(hal_gpio_get_value);

static void hal_gpio_set_value(unsigned int gpio, int value)
{
    gpio_set_value(gpio, value);
}
EXPORT_SYMBOL(hal_gpio_set_value);

static int hal_gpio_direction_input(unsigned gpio)
{
	gpio_direction_input(gpio);
	return 0;
}
EXPORT_SYMBOL(hal_gpio_direction_input);

static int hal_gpio_direction_output(unsigned gpio, int value)
{
	gpio_direction_output(gpio, value);
	return 0;
}
EXPORT_SYMBOL(hal_gpio_direction_output);


static int __init hal_gpio_api_init( void )
{
	printk( "HAL_GPIO_API: hal_gpio_api_init entry\n" );
	return 0;
}

static void __exit hal_gpio_api_cleanup( void )
{
	printk( "HAL_GPIO_API: hal_gpio_api_cleanup entry\n" );	
}

module_init(hal_gpio_api_init);
module_exit(hal_gpio_api_cleanup);

MODULE_DESCRIPTION("Export Symbol for GPIOs in Intel ClassConnect");
MODULE_LICENSE("GPL");
MODULE_VERSION(HAL_GPIO_API_VERSION);
