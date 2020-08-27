/*
 * NCT6779D gpio module
 * */

#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/delay.h>
#include <linux/sysfs.h>
#include <linux/kernel.h>
#include <linux/spinlock.h>
#include <linux/mutex.h>
#include <linux/tty.h>
#include <linux/proc_fs.h>
#include <linux/timer.h>
#include <linux/device.h>
#include <asm/uaccess.h> /*copy_from_user*/
#include <linux/proc_fs.h>
#include <net/net_namespace.h>

#define HH 0x03
#define HL 0x02
#define LH 0x01
#define LL 0x00
#define PROC_ENTRY_NAME	"suio_gpio"


static inline void superio_gpio_init(void)
{
	int Value; 

	outb(0x87,0x2E); // two successive 0x87 to enable exteneded mode
	outb(0x87,0x2E); //

	outb(0x27,0x2E);
	Value = inb(0x2F);
	outb((Value | 0x10) , 0x2F);

	outb(0x7,0x2E); // logical device selection
	outb(0x9,0x2F); // logical device 9

	outb(0x30,0x2E); // Enable GPIO6 group , CR30 Bit6 set 1
	Value = inb(0x2F);
	outb((Value | 0x40) , 0x2F); // GPIO6 is active.

	outb(0x7,0x2E); // logical device selection
	outb(0x7,0x2F); // logical device 7

	outb(0xF4,0x2E);
	Value = inb(0x2F);
	outb(Value & 0x00, 0x2F); // GPIO6 register as an output port.

	outb(0xF8,0x2E);
	Value = inb(0x2F);
	outb(Value & 0xFC, 0x2F); // GPIO6 multi-function select register.
}


static inline void superio_gpio_exit(void)
{
	/* Closed I/O control */
	outb(0x55,0x2E);
	outb(0xAA,0x2E);
}

/* Usage:
 * cat /proc/suio_gpio 
 * The bit 1 is GP61 and the bit 0 is GP60.
 * */
static inline void superio_gpio_read(void)
{
	int Value=0;
	int i, bit;
	superio_gpio_init();
	outb(0xF5,0x2E);
	Value = inb(0x2F);
	printk(KERN_ALERT "[SENAO] 0x%x\n", Value);
	for(i=128, bit=7;i;i>>=1,bit--)
		printk(KERN_ALERT "[SENAO] bit %d = %s\n", bit, i&Value?"1":"0");

	superio_gpio_exit();
	return;
}

/* Usage:
 * echo "00" /proc/suio_gpio 
 *
 * */

static inline void superio_gpio_write(int gpio_value)
{
	int Value=0;
	superio_gpio_init();
	outb(0xF5,0x2E);
	Value = inb(0x2F);
//	printk(KERN_ALERT "[SENAO] 0x%x\n", Value);
	Value &= 0xfc; // origin value.
	Value |= gpio_value;
	outb(Value,0x2F);

	superio_gpio_exit();
	return;
}

static ssize_t suio_gpio_proc_read(struct file *filp, char *buffer, size_t count, loff_t *offp)
{
	superio_gpio_read();
	return 0;
}

static ssize_t suio_gpio_proc_write(struct file *filp, const char *buffer, size_t count, loff_t *offp)
{
	unsigned char input[3];
	memset(input, 0x00, sizeof(input));

	if ((count > 34) || (copy_from_user(input, buffer, count-1) != 0))
		return -EFAULT;

	if (strcmp(input, "00") == 0) 
	{
		printk(KERN_ALERT "[SENAO] write %s\n", input);
		printk(KERN_ALERT "[SENAO] GP61 Low, GP60 Low\n");
		superio_gpio_write(LL);
	} 
	else if (strcmp(input, "01") == 0)
	{
		printk(KERN_ALERT "[SENAO] write %s\n", input);
		printk(KERN_ALERT "[SENAO] GP61 Low, GP60 High\n");
		superio_gpio_write(LH);
	}
	else if (strcmp(input, "10") == 0)
	{
		printk(KERN_ALERT "[SENAO] write %s\n", input);
		printk(KERN_ALERT "[SENAO] GP61 High, GP60 Low\n");
		superio_gpio_write(HL);
	}
	else if (strcmp(input, "11") == 0)
	{
		printk(KERN_ALERT "[SENAO] write %s\n", input);
		printk(KERN_ALERT "[SENAO] GP61 High, GP60 High\n");
		superio_gpio_write(HH);
	}
	else
	{
		printk(KERN_ALERT "[SENAO] ERROR number, only \"00\", \"01\", \"10\", \"11\"\n");
		printk(KERN_ALERT "[SENAO] E.g. echo \"00\" > /proc/%s\n", PROC_ENTRY_NAME);
	}
	return count;
}

static int suio_gpio_init(void)
{
	static const struct file_operations proc_file_fops1 = {
		.read = suio_gpio_proc_read,
		.write = suio_gpio_proc_write,
	};
	printk(KERN_ALERT "[SENAO] suio_gpio driver init.\n");
	proc_create(PROC_ENTRY_NAME, 0, NULL, &proc_file_fops1);
	printk(KERN_DEBUG "[SENAO] Success create /proc/suio_gpio\n");
	return 0;
}
void suio_gpio_exit(void){
	remove_proc_entry(PROC_ENTRY_NAME, NULL);
	printk(KERN_DEBUG "[SENAO] Success remove /proc/suio_gpio\n");
	printk(KERN_ALERT "[SENAO] suio_gpio driver removed.\n");
}

module_init(suio_gpio_init);
module_exit(suio_gpio_exit);

MODULE_LICENSE("GPL") ;
MODULE_AUTHOR("Darcy_Chang <Darcy.Chang@senao.com>");
MODULE_DESCRIPTION("This is suio gpio module.");
