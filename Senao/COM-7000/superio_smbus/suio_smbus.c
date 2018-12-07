/*
 * Support for smbus byte data on nct6775
 * 
 */
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/delay.h>
#include <linux/i2c.h>

#define SM_DATA 0
#define SM_WRITE_SIZE 1
#define SM_COMMAND 2
#define SM_INDEX 3
#define SM_CONTROL 4
#define SM_ADDRESS 5
#define SM_FERQ 6
#define BS_MASK	(~7)

#define DRIVER_NAME "suio_smbus"
int smbus_clock = 7;
module_param(smbus_clock, int, 0);

static struct platform_device suio_smbus_device = {
	.name = "suio_smbus",
	.id = -1,
};

struct suio_smbus_priv {
	struct i2c_adapter adap;
	struct i2c_msg *msg;
	struct device *dev;
	struct mutex acpi_lock;
	int bs_addr;
};

static inline int
superio_inb(int ioreg, int reg)
{
	outb(reg, ioreg);
	return inb(ioreg + 1);
}

static inline int
superio_enter(int ioreg)
{
	if (!request_muxed_region(ioreg, 2, DRIVER_NAME))
		return -EBUSY;

	outb(0x87, ioreg);
	outb(0x87, ioreg);

	return 0;
}

static inline void
superio_select(int ioreg, int ld)
{
	outb(0x7, ioreg);
	outb(ld, ioreg + 1);
}

static inline void
superio_exit(int ioreg)
{
	outb(0xaa, ioreg);
	outb(0x02, ioreg);
	outb(0x02, ioreg + 1);
	release_region(ioreg, 2);
}

static int suio_init(struct suio_smbus_priv *priv)
{
	int enable_val,ret=0;
	u16 val;
	ret = superio_enter(0x2e);
	if (ret)
		goto error;
	superio_select(0x2e, 0x0b);
	val = (superio_inb(0x2e, 0x62) << 8)
	    | superio_inb(0x2e, 0x63 );
	priv->bs_addr = val & BS_MASK;	
	enable_val = superio_inb(0x2e, 0x30);
	if (!enable_val){
		ret = 1;
		goto error;
	}
	printk(KERN_ALERT "base address:%x.\n", priv->bs_addr);
	superio_exit(0x2e);
	outb_p(smbus_clock, priv->bs_addr + SM_FERQ);
	printk(KERN_ALERT "SMBUS CLK:%x.\n", smbus_clock);
error:
	return ret;
}


static s32 suio_smbus_access(struct i2c_adapter *adap, u16 addr, unsigned short flags, char read_write, u8 command, int size, union i2c_smbus_data *data)
{
	struct suio_smbus_priv *priv = i2c_get_adapdata(adap);
	int ret = 0;
	
	mutex_lock(&priv->acpi_lock);
	switch (size) {
		case I2C_SMBUS_BYTE_DATA:
			outb_p(((addr & 0x7f) << 1), priv->bs_addr + SM_ADDRESS);
			outb_p(command, priv->bs_addr + SM_INDEX);
			if (read_write == I2C_SMBUS_WRITE){
				outb_p(0x8, priv->bs_addr + SM_COMMAND);
				outb_p(data->byte, priv->bs_addr + SM_DATA);
			}else{
				outb_p(0x0, priv->bs_addr + SM_COMMAND);
			}
			msleep(10);
			outb_p(0x80, priv->bs_addr + SM_CONTROL);
			break;
		default:
			dev_err(priv->dev, "Unsupported transaction %d\n",size);
			ret = -EOPNOTSUPP;
		goto out;	
	}
	if (read_write == I2C_SMBUS_WRITE)
		goto out;
	switch (size) {
	case I2C_SMBUS_BYTE_DATA:
		msleep(10);
		data->byte = inb(priv->bs_addr + SM_DATA);
		break;
	}
out:
	mutex_unlock(&priv->acpi_lock);
	return ret;
}

static u32 suio_smbus_func(struct i2c_adapter *adapter)
{
	return I2C_FUNC_SMBUS_BYTE_DATA;
}

static const struct i2c_algorithm smbus_algorithm = {
	.smbus_xfer	= suio_smbus_access,
	.functionality	= suio_smbus_func,
};

static int suio_smbus_probe(struct platform_device *pdev)
{
	struct suio_smbus_priv *priv;
	int ret=0;
	priv = devm_kzalloc(&pdev->dev, sizeof(*priv), GFP_KERNEL);
	if (!priv)
		return -ENOMEM;
	strlcpy(priv->adap.name, "suio_smbus", sizeof(priv->adap.name));
	priv->dev = &pdev->dev;
	priv->adap.owner = THIS_MODULE;
	priv->adap.algo = &smbus_algorithm;
	priv->adap.algo_data = priv;
	priv->adap.dev.parent = &pdev->dev;
	i2c_set_adapdata(&priv->adap, priv);
	platform_set_drvdata(pdev, priv);
	mutex_init(&priv->acpi_lock);
	ret = i2c_add_adapter(&priv->adap);
	if (ret < 0) {
		dev_err(&pdev->dev, "failed to add bus to i2c core\n");
		goto error;
	}
	ret = suio_init(priv);
	
error:
	return ret;
}

static int suio_smbus_remove(struct platform_device *pdev)
{
	struct suio_smbus_priv *priv = platform_get_drvdata(pdev);
	i2c_del_adapter(&priv->adap);
	return 0;
}

static struct platform_driver suio_smbus_driver = {
	.probe		= suio_smbus_probe,
	.remove		= suio_smbus_remove,
	.driver		= {
		.name	= "suio_smbus",
	},
};

static int suio_smbus_init(void)
{
	int ret = 0;
	ret = platform_device_register(&suio_smbus_device);
	if (ret)
		goto error;
	ret = platform_driver_register(&suio_smbus_driver);
	if (ret)
		goto error;
	printk(KERN_ALERT "suio_smbus driver init.\n");
	return 0;
error:
	return 1;
}
void suio_smbus_exit(void){
	platform_device_unregister(&suio_smbus_device);
	platform_driver_unregister(&suio_smbus_driver);
	printk(KERN_ALERT "suio_smbus driver removed.\n");
}

module_init(suio_smbus_init);
module_exit(suio_smbus_exit);

MODULE_LICENSE("GPL") ;
MODULE_AUTHOR("Gino <gino.tien@senao.com>");
MODULE_DESCRIPTION("This is suio smbus module.");
