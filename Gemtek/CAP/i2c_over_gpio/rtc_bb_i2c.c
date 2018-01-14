
/* Includes. */
#include <linux/version.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/stddef.h>
#include <linux/kernel.h>
#include <linux/ioport.h>
#include <linux/delay.h>
#include <linux/ctype.h>

#include <linux/i2c.h>
#include <linux/i2c-algo-bit.h>

#include <asm/uaccess.h> /*copy_from_user*/
#include <linux/proc_fs.h>

#include <bcm_map_part.h>

#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,29)
#include <net/net_namespace.h>
#endif

/* Defines. */
#define GPIO2IIC_VERSION                     "1.0"

/* Typedefs. */
/*
 * definitions for writing to I2C
 */
#define SELECT_READ  1 
#define SELECT_WRITE 0 
#define HIGH         1 
#define LOW          0 
#define OUTPUT       1 
#define INPUT        0 

#define BB_I2C_BUS_0   0    
#define BB_I2C_BUS_1   1    

#define TOTAL_BB_I2C_BUS     2

#if defined(GTK_WVDB_128N_V01)
#define GPIO_PIN_SCL_RTC	14
#define GPIO_PIN_SDA_RTC	15
#define GPIO_PIN_INIT_RTC 	35
#elif defined(GTK_WVDB_128N_V02)
#define GPIO_PIN_SCL_RTC	13
#define GPIO_PIN_SDA_RTC	15
#define GPIO_PIN_INIT_RTC 	35
#else // GTK_WVDB_128N_V02_B GTK_WVDB_128N_V03 GTK_WVDB_128N_V04
#define GPIO_PIN_SCL_RTC        9
#define GPIO_PIN_SDA_RTC        15
#define GPIO_PIN_INIT_RTC       35 
#endif



#define DEV_ADDR_RTC	0x68 //P2 RTC address

#define PROC_ENTRY_NAME	"bb_rtc_reg"
#define READ_DATA_SIZE	520
#define	DEFAULT_PART_NUMBER	"04FFC30600112A334B50C18B464848313233303030474A40074241010009BC824A21AF0142303188000000000201030081000000000400430008C28B4648483132333150303630CB92434953434F838365641458956303120D90340C1C2C68A54424420202020202020FF"

#define MAX_BB_I2C_DATA_SIZE 64    /* Data size engineering limit */
#define MAX_RTC_DATA_SIZE	32
#define RTC_READ_DATA_SIZE	6

typedef unsigned char	uchar;
typedef void (*i2cbb_fn_t) (void *obj); 
typedef uchar (*i2cbb_read_fn_t) (void *obj); 
typedef uchar (*i2cbb_read_parm_fn_t) (void *obj, uchar byte); 
typedef void (*i2cbb_write_fn_t) (void *obj, uchar byte); 

/* Prototypes. */
static int __init gpio2iic_init( void );
static void __exit gpio2iic_cleanup( void );
static int i2c_bb_bitgpio_init( void );
static ssize_t bb_rtc_proc_write(struct file *file, const char *buffer, unsigned long count, void *data);

/* Globals. */
int bcm_gpio_active_is_high = 1; /* scl: 25, sda: 26 gpio: active high */
uint8 buffer_data[READ_DATA_SIZE];
uint8 dataInReg;

#define GPIO_NUM_MASK 0x00FF
//#define BCM_GPIO_NUM_TO_MASK(X)  ((((X) & GPIO_NUM_MASK) < GPIO_NUM_MAX) ? ((uint64)1 << ((X) & GPIO_NUM_MASK)) : (0))
#define BCM_GPIO_NUM_TO_MASK(X)  ((((X) & GPIO_NUM_MASK) < GPIO_NUM_MAX) ? (1 << ((X) & GPIO_NUM_MASK)) : (0))
#define I2C_DELAY  10   /* 10 usec i.e. 100k Cycle */
#define	usecdelay(x)	udelay(x)

/* this belongs in i2c-id.h */
#define I2C_HW_B_BCM5365	0x010021 /* Broadcom BCM5365 gpio */

enum bb_state_t {
   BB_START,
   BB_STOP 
};

static int DEBUG_ME=0;
/* Bit bang bus controller */

typedef struct i2cbb_
{ 
    /* internal attributes */
    int bus_no;
    int delay;     /* must be half cycle of the clock */
    int lock;
    int state; 
    int enabled;
    int gpio_pin_scl;
    int gpio_pin_sda;
   
    /* internal methods */
    i2cbb_fn_t       start;          
    i2cbb_fn_t       stop;           
    i2cbb_fn_t       write_ack;            
    i2cbb_fn_t       write_nack;            

    /* signal control */
    i2cbb_fn_t       scl_high;       
    i2cbb_fn_t       scl_low;        
    i2cbb_fn_t       scl_input;      
    i2cbb_fn_t       scl_output;     
    i2cbb_read_fn_t  scl_get;       

    i2cbb_fn_t       sda_high;       
    i2cbb_fn_t       sda_low;        
    i2cbb_fn_t       sda_input;      
    i2cbb_fn_t       sda_output;     
    i2cbb_read_fn_t  sda_get;       

    i2cbb_read_fn_t      read_ack;       
    i2cbb_read_fn_t      read_data_bit;  
    i2cbb_write_fn_t     write_data_bit; 
    i2cbb_read_parm_fn_t device_ready;   

    /* high level function */
    i2cbb_read_fn_t  read_data_byte;  
    i2cbb_write_fn_t write_data_byte; 
    i2cbb_read_fn_t  bus_busy;        
} i2cbb_t;


/* stats for bit bang */
typedef struct bcm6300_bb_info_ {
    ulong tx_bytes; 
    ulong rx_bytes; 
    ulong read_ok_count; 
    ulong read_fail_count; 
    ulong write_ok_count; 
    ulong write_fail_count; 
    ulong nack_count; 
} bcm6300_bb_info_t;

static bcm6300_bb_info_t bcm6300_bb_info[TOTAL_BB_I2C_BUS];  

i2cbb_t bcm6300_bb_i2c[TOTAL_BB_I2C_BUS]; 

/* testing */
#if 0
static int bcm6300_bb_gpio_test = FALSE;
#endif

/*
 * Description:
 *   set the gpio signal
 *
 * Parm:
 *   bus_no: bus number
 *   gpio  : gpio pin number 
 *
 * Returns:
 */
static void set_gpio(int bus_no, int gpio, int active)
{
    if (active == TRUE) {  
        GPIO->GPIOio |= BCM_GPIO_NUM_TO_MASK(gpio);
    } else {
        GPIO->GPIOio &= ~BCM_GPIO_NUM_TO_MASK(gpio);
    }
}


/*
 * Description:
 *   set the gpio signal 
 *
 * Parm:
 *   bus_no: bus number
 *
 */
static inline void gpio_line_set (int bus_no, int gpio, bool highlow)
{

    /* notes: active is low, default is high */
    if (bcm_gpio_active_is_high) {
        /* active is high */
        if (highlow == HIGH) {
            set_gpio(bus_no, gpio, TRUE);
        } else {
            set_gpio(bus_no, gpio, FALSE);
        }
    } else {
        if (highlow == HIGH) {
            set_gpio(bus_no, gpio, FALSE);
        } else {
            set_gpio(bus_no, gpio, TRUE);
        }
    }
}

/*
 * Description:
 *   set the gpio signal mode (input or output)
 *
 * Parm:
 *   bus_no: bus number
 *
 */
static inline void gpio_mode_set (int bus_no, int gpio, bool inout)
{
   if (inout == OUTPUT) {
       GPIO->GPIODir |= BCM_GPIO_NUM_TO_MASK(gpio);
   } else {
       GPIO->GPIODir &= ~BCM_GPIO_NUM_TO_MASK(gpio);
   }
}


/*
 * Description:
 *   set the sda line to output mode 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */

static void i2c_sda_output (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_mode_set(obj->bus_no, obj->gpio_pin_sda, OUTPUT);
}


/*
 * Description:
 *   set the scl clock line to low
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_scl_low (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_line_set(obj->bus_no, obj->gpio_pin_scl, LOW);
   usecdelay(obj->delay);

}


/*
 * Description:
 *   set the sda line to high
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */

static void i2c_sda_high (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_line_set(obj->bus_no, obj->gpio_pin_sda, HIGH);
   usecdelay(obj->delay);
}


/*
 * Description:
 *   set the sda line to low
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
 
static void i2c_sda_low (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_line_set(obj->bus_no, obj->gpio_pin_sda, LOW);
   usecdelay(obj->delay);
}

/*
 * Description:
 *   set the scl clock line to high
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_scl_high (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_line_set(obj->bus_no, obj->gpio_pin_scl, HIGH);
   usecdelay(obj->delay);
}




/*
 * Description:
 *   set the scl line to output mode 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
 
static void i2c_scl_output (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_mode_set(obj->bus_no, obj->gpio_pin_scl, OUTPUT);
}


/*
 * Description:
 *   Write one bit to SDA 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_write_data_bit (void *i2cbb, uchar bit)
{
//   i2cbb_t *obj = (i2cbb_t *) i2cbb;

    /* clock low */
    i2c_scl_low(i2cbb);	//obj->scl_low(i2cbb);    

    if (bit & 0x1) {
        i2c_sda_high(i2cbb);	//obj->sda_high(i2cbb);
    } else {
       i2c_sda_low(i2cbb); //obj->sda_low(i2cbb);
    }

    /* data ready, signal */
    i2c_scl_high(i2cbb);	//obj->scl_high(i2cbb);   

    /* if support clock stretching, need: 
     * while obj->scl_get(i2cbb) == LOW);
     * obj->delay(i2cbb); */

    /* data done */
    i2c_scl_low(i2cbb);	//obj->scl_low(i2cbb);    
}


/*
 * Description:
 *   write an ack to the bus 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_write_ack (void *i2cbb)
{
//    i2cbb_t *obj = (i2cbb_t *) i2cbb;

    i2c_sda_output(i2cbb);	//obj->sda_output(i2cbb);
    
    i2c_write_data_bit(i2cbb, LOW);	//obj->write_data_bit(i2cbb, LOW);  /* ack is low */

}


/*
 * Description:
 *   write an nack to the bus 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_write_nack (void *i2cbb)
{
//    i2cbb_t *obj = (i2cbb_t *) i2cbb;

    i2c_sda_output(i2cbb);	//obj->sda_output(i2cbb);
    
    i2c_write_data_bit(i2cbb, HIGH);	//obj->write_data_bit(i2cbb, HIGH);  /* nack is high*/
}


/*
 * Description:
 *   set the sda line to input mode 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_sda_input (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   gpio_mode_set(obj->bus_no, obj->gpio_pin_sda, INPUT);
}



/*
 * Description:
 *   read the gpio signal
 *
 * Parm:
 *   bus_no: bus number
 *
 * Returns:
 *    HIGH (1) LOW(0)
 */
static inline uchar gpio_line_get (int bus_no, int gpio)
{
    if (bcm_gpio_active_is_high) {
        /* notes: active is high */
        if ((GPIO->GPIOio & BCM_GPIO_NUM_TO_MASK(gpio)) == 0) {
           /* inactive */
           return (LOW); 
        } else {
           /* active */
           return (HIGH); 
        }
    } else {
        /* notes: active is low */
        if ((GPIO->GPIOio & BCM_GPIO_NUM_TO_MASK(gpio)) == 0) {
           /* inactive */
           return (HIGH); 
        } else {
           /* active */
           return (LOW); 
        }
    }
}


/*
 * Description:
 *   read the sda signal 
 *
 */
static uchar i2c_sda_get (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   /* return sda gpio state, 1 = high, 0 = low */
   return gpio_line_get(obj->bus_no, obj->gpio_pin_sda);
}


/*
 * Description:
 *   Read 1 bit from SDA line
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 * Return:
 *    1 or 0  (represent the bit)
 */

static uchar i2c_read_data_bit (void *i2cbb)
{
//   i2cbb_t *obj = (i2cbb_t *) i2cbb;
   int bit;

   i2c_sda_input(i2cbb);	//obj->sda_input(i2cbb); 
   i2c_scl_high(i2cbb);	//obj->scl_high(i2cbb); 
   /* if support clock clock stretching should wait for 
    * slave to pull high instead of polling high by master 
    * while (obj->scl_get(i2cbb) == LOW ); */
   
   /* now scl is high, data ready */
   bit = i2c_sda_get(i2cbb);	//obj->sda_get(i2cbb);
   i2c_scl_low(i2cbb);	//obj->scl_low(i2cbb);     /* scl low, bit read */

   return (bit);
}



/*
 * Description:
 *   read ack from the bus 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static uchar i2c_read_ack (void *i2cbb)
{
//    i2cbb_t *obj = (i2cbb_t *) i2cbb;
    int ack;

    i2c_sda_input(i2cbb);	//obj->sda_input(i2cbb);
    //ack = !(obj->read_data_bit(i2cbb)); /* we expect a 0 as the ACK */
    ack = !(i2c_read_data_bit(i2cbb));

    return (ack);
}





/*
 * Description:
 *   Write 1 byte to SDA line
 * 
 * Parm:
 *    i2cbb: bitband control block
 *    sent_byte: data byte
 *
 */
static void i2c_write_data_byte (void *i2cbb, uchar sent_byte)
{
//   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   uchar bits_to_shift = 7;
   uchar bit_to_send = 0x80;

    //obj->sda_output(i2cbb);
    i2c_sda_output(i2cbb);

    while (bit_to_send) {
        i2c_write_data_bit(i2cbb, (sent_byte & bit_to_send) >> bits_to_shift);	//obj->write_data_bit(i2cbb, (sent_byte & bit_to_send) >> bits_to_shift);
        bit_to_send >>= 1;
        bits_to_shift--;
    }
}


/*
 * Description:
 *   Sent a start condition
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */

static void i2c_start (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   /* enable sda output mode */
   //obj->scl_output(i2cbb);
   i2c_scl_output(i2cbb);
   //obj->sda_output(i2cbb);
   i2c_sda_output(i2cbb);

   /*
    * a start condition is a high-to-low transition of SDA with SCL high
    */
   i2c_scl_low(i2cbb);	//obj->scl_low(i2cbb);  /* make scl low to prepare to change sda bit */
   i2c_sda_high(i2cbb);	//obj->sda_high(i2cbb); /* change sda bit */


   /*
    * put scl high, so the negative edge of sda bit will indicate a
    * start condition
    */
   i2c_scl_high(i2cbb);	//obj->scl_high(i2cbb);    
   /* if support clock streching */
   /* need: while (obj->scl_get() == low); */

   /* both are high now */
   //obj->sda_low(i2cbb);    
   i2c_sda_low(i2cbb);
   /* obj->scl_low(i2cbb); */
   obj->state = BB_START;

}


/*
 * Description:
 *   Sent a stop condition 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */
static void i2c_stop (void *i2cbb)
{
   i2cbb_t *obj = (i2cbb_t *) i2cbb;

   i2c_sda_output(i2cbb);	//obj->sda_output(i2cbb);

   /*
    * a stop condition is a low-to-high transition of SDA with SCL high
    */
   i2c_scl_low(i2cbb);	//obj->scl_low(i2cbb);    /* make scl low to prepare to change sda bit */
   i2c_sda_low(i2cbb);	//obj->sda_low(i2cbb);    /* change sda bit */

    /*
     * put scl high, so the positive edge of sda bit will indicate a
     * start condition
     */
    i2c_scl_high(i2cbb);	//obj->scl_high(i2cbb);
    /* pull sda from low to high */ 
    i2c_sda_high(i2cbb);	//obj->sda_high(i2cbb);     /* sda bit transition */
    
    i2c_sda_input(i2cbb);	//obj->sda_input(i2cbb);    /* make sda an input */

    obj->state = BB_STOP;
}


/*
 * Description:
 *   Is the slave device on the bus 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *    dev_addr: i2c slave device address
 *
 * Return:
 *    0 (not found), 1 (found and ready)
 */

static uchar i2c_ready(void *i2cbb, uchar dev_addr)
{
//    i2cbb_t *obj = (i2cbb_t *) i2cbb;
    uchar  i2c_addr_and_rw;
    int ready = FALSE;  

    /*
     * Send start signal 
     */
    i2c_start(i2cbb);	//obj->start(i2cbb); 

    /*
     * Send I2C slave address + read/write flag
     */
    i2c_addr_and_rw = dev_addr << 1 | SELECT_WRITE;
    i2c_write_data_byte(i2cbb, i2c_addr_and_rw);	//obj->write_data_byte(i2cbb, i2c_addr_and_rw);

    /* 
     * Check for the ACK from Slave
     */
    if(!i2c_read_ack(i2cbb)) { //if (!obj->read_ack(i2cbb)) {
        /* no response */
        ready = FALSE; 
    } else {
        ready = TRUE; 
    }

    i2c_stop(i2cbb);	//obj->stop(i2cbb); 

    return (ready);
}


/*
 * Description:
 *   Read 1 byte from the bus
 * 
 * Parm:
 *    i2cbb: bitband control block
 * Return:
 *    one byte
 */
static uchar i2c_read_data_byte (void *i2cbb)
{
//    i2cbb_t *obj = (i2cbb_t *) i2cbb;
    uchar result = 0;
    int i;

    i2c_sda_input(i2cbb);	//obj->sda_input(i2cbb);
    for (i=0; i < 8; i++) {
        result <<= 1;
        result |= i2c_read_data_bit(i2cbb);	//obj->read_data_bit(i2cbb);
    }

    return (result);
}


/*
 * Description:
 *   initialize the bus and set up vector functions 
 * 
 * Parm:
 *    i2cbb: bitband control block
 *
 */

static void i2c_bitbang_init_bus1 (void)
{
   i2cbb_t *bb_i2c = &bcm6300_bb_i2c[BB_I2C_BUS_1];

   /* copy the vector data over */
   //bcopy(&bcm6300_bb_i2c[BB_I2C_BUS_0], bb_i2c, sizeof(i2cbb_t));
   //no use!!! memcpy(&bcm6300_bb_i2c[BB_I2C_BUS_0], bb_i2c, sizeof(i2cbb_t));

   /* set up bus one attribute */ 
    bb_i2c->bus_no       = BB_I2C_BUS_1;   
    bb_i2c->delay        = I2C_DELAY;    
    bb_i2c->state        = BB_STOP;      
    bb_i2c->enabled      = TRUE;         
    bb_i2c->lock         = FALSE;      

    bb_i2c->gpio_pin_scl = GPIO_PIN_SCL_RTC;
    bb_i2c->gpio_pin_sda = GPIO_PIN_SDA_RTC;

}

#if 0

static void test_gpio_signal(int gpio)
{
    printk("\n=== pin: %d ===", gpio);
    /* read current gpio signal */
    if (bcm6300_bb_gpio_test == FALSE) { 
        gpio_mode_set (0, gpio, OUTPUT);
        printk("\nOutput mode:  GPIO is %s", 
            gpio_line_get(0, gpio)?"HIGH":"LOW");

        gpio_mode_set (0, gpio, INPUT);
        printk("\nInput mode :  GPIO is %s", 
            gpio_line_get(0, gpio)?"HIGH":"LOW");
    } else {
        /* low test */
        printk("\n=== set  GPIO to LOW");
        gpio_mode_set (0, gpio, OUTPUT);
        gpio_line_set(0, gpio, LOW);
        printk("\noutput:  GPIO is %s", 
            gpio_line_get(0, gpio)?"HIGH":"LOW");

        /* switch mode test */
        usecdelay(100);
        gpio_mode_set (0, gpio, INPUT);
        usecdelay(100);
        gpio_mode_set (0, gpio, OUTPUT);
        usecdelay(100);
        printk("\noutput: double switch back:  GPIO is %s", 
            gpio_line_get(0, gpio)?"HIGH":"LOW");

        /* high test */
        printk("\n=== set  GPIO to HIGH");
        gpio_mode_set (0, gpio, OUTPUT);
        usecdelay(100);
        gpio_line_set(0, gpio, HIGH);
        printk("\noutput:  GPIO is %s", 
            gpio_line_get(0, gpio)?"HIGH":"LOW");

        /* low test */
        printk("\n=== set  GPIO to LOW");
        gpio_mode_set (0, gpio, OUTPUT);
        gpio_line_set(0, gpio, LOW);
        printk("\noutput:  GPIO is %s", 
            gpio_line_get(0, gpio)?"HIGH":"LOW");
    }
    printk("\n");
}

void bb_i2c_scanbus (int i2cNum)
{
    i2cbb_t *obj;
    void   *i2cbb = (void *) obj; 
    int    total = 0;
    int    jj;

    if (i2cNum >= TOTAL_BB_I2C_BUS) {
       printk("\n bb_i2c_scanbus(): error - Invalid bus number %d", i2cNum);
       return;
    }

    obj = &bcm6300_bb_i2c[i2cNum];
    i2cbb = (void *) obj;

    /* scan the range of i2c slave device */
    for (jj = 0x1; jj < 0x7f; jj++) {
			if( i2c_ready(i2cbb, jj) == TRUE )
//        if (obj->device_ready(i2cbb, jj) == TRUE)
        {
            printk("\n  I2C: Found device at address 0x%02x\n",jj);
            total++;
        }
    }

    if (total == 0) {
        printk("\n  I2C: No device found");
    }
}


/*
 * Description:
 *   Dump internal diagnostic and stats
 *
 * Parameters:
 *   i2cNum    - bus number
 *
 * Returns:
 */

static void bb_i2c_dump_info (int bus_no)
{
#define BBDUMP(x) printk(" %45s : 0x%02X\n", "" # x, x)
	i2cbb_t *bb_i2c = &bcm6300_bb_i2c[bus_no];

    printk("\n= bitband bus no: %d ==\n", bus_no);

    printk("\n== Bitbang diag stats ==\n");
    BBDUMP(bcm6300_bb_info[bus_no].tx_bytes);
    BBDUMP(bcm6300_bb_info[bus_no].rx_bytes);
    BBDUMP(bcm6300_bb_info[bus_no].read_ok_count);
    BBDUMP(bcm6300_bb_info[bus_no].write_ok_count);
    BBDUMP(bcm6300_bb_info[bus_no].read_fail_count);
    BBDUMP(bcm6300_bb_info[bus_no].write_fail_count);
    BBDUMP(bcm6300_bb_info[bus_no].nack_count);

    printk("\n== SDA ==");
//    test_gpio_signal(GPIO_PIN_SDA_QUACK);
		test_gpio_signal(bb_i2c->gpio_pin_sda);

    printk("\n== SCL ==");
//    test_gpio_signal(GPIO_PIN_SCL_QUACK);
		test_gpio_signal(bb_i2c->gpio_pin_scl);

}

#endif

//void test_bb_i2c_scanbus_command (parseinfo *csb)
static int i2c_bb_bitgpio_init()
{
    i2cbb_t *obj = &bcm6300_bb_i2c[BB_I2C_BUS_1]; 
    void   *i2cbb = (void *) obj; 
    uint8 jj    = 0;
    int   count = 0;

    i2c_bitbang_init_bus1();

    printk("Scan start ...bus 1\n"); 
    for (jj = 1; jj < 128; jj++) { 
    	if( i2c_ready(i2cbb, jj) == TRUE ) {
            printk("%02X(%02X) ", jj, jj<<1);
            count++;
        } 

        usecdelay(1000);
    }

    printk("\n[RTC] Number of smbus/i2c slave devices found %d\n" , count); 
}


/************ user callable function ***************/

/*
 * Description:
 *   transmit data to the slave 
 *
 * Parameters:
 *   i2cNum    - bus number
 *   dev_addr  - slave address
 *   data      - data bytes array
 *   send_stop - boolean, sent stop at the end of transaction?
 *
 * Returns:
 *   data byte written. 
 */

int bb_i2c_write_exe (int i2cNum, uchar dev_addr, char *data, int msg_size, int send_stop)
{
    i2cbb_t *obj;
    void  *i2cbb; 
    int   sent   = 0;
    uchar i2c_addr_and_rw;

    if (i2cNum >= TOTAL_BB_I2C_BUS) {
       return (FALSE);
    }

    obj = &bcm6300_bb_i2c[i2cNum];
    i2cbb = (void *) obj;

    /*
     * Send start signal 
     */
    i2c_start(i2cbb);	//obj->start(i2cbb); 

    /*
     * Send I2C slave address + read/write flag
     */
    i2c_addr_and_rw = dev_addr << 1 | SELECT_WRITE;
    i2c_write_data_byte(i2cbb, i2c_addr_and_rw);	//obj->write_data_byte(i2cbb, i2c_addr_and_rw);


    /* 
     * Check for the ACK from Slave
     */
    if(!i2c_read_ack(i2cbb)) { 	//if (!obj->read_ack(i2cbb)) {
        i2c_stop(i2cbb);	//obj->stop(i2cbb); /* abort protocol */
        bcm6300_bb_info[obj->bus_no].nack_count++; 
        bcm6300_bb_info[obj->bus_no].read_fail_count++;
        return (0);
    }

    /*
     * Send the actual data
     */
    for (sent = 0; sent < msg_size; sent++) {
        i2c_write_data_byte(i2cbb, *data++);	//obj->write_data_byte(i2cbb, *data++); 

        /* 
         * Check for the ACK from Slave
         */
        if(!i2c_read_ack(i2cbb)) { 	//if (!obj->read_ack(i2cbb)) {
            i2c_stop(i2cbb);	//obj->stop(i2cbb); 
            bcm6300_bb_info[obj->bus_no].tx_bytes += sent;
            bcm6300_bb_info[obj->bus_no].nack_count++; 
            bcm6300_bb_info[obj->bus_no].read_fail_count++;
            return sent;
        } 
    }

    /* Everything is done */ 
    if (send_stop) {
        i2c_stop(i2cbb);	//obj->stop(i2cbb);
    }

    if (sent == msg_size) {
       bcm6300_bb_info[obj->bus_no].write_ok_count++;
    } else {
       bcm6300_bb_info[obj->bus_no].write_fail_count++;
    }

    bcm6300_bb_info[obj->bus_no].tx_bytes += sent;

    return sent;
}

/*
 * Description:
 *   transmit data to the slave
 *
 * Parameters:
 *   i2cNum    - bus number
 *   dev_addr  - slave address
 *   data      - data bytes array
 *
 * Returns:
 *   count of data byte written. 
 */

inline int bb_i2c_write (int i2cNum, uchar dev_addr, char *data, int msg_size)
{
    return bb_i2c_write_exe(i2cNum, dev_addr, data, msg_size, TRUE); 
}

/*
 * Description:
 *   receive data from the slave
 *
 * Parameters:
 *   i2cNum    - bus number
 *   dev_addr  - slave address
 *   read_buffer - data bytes array read
 *
 * Returns:
 *   count of data bytes read. 
 */

int bb_i2c_read (int i2cNum, uchar dev_addr, ulong size, uchar *read_buffer)
{
    i2cbb_t *obj;
    void   *i2cbb = (void *) obj; 
    uchar  i2c_addr_and_rw;
    int    read = 0;
    uchar  val;

    if (i2cNum >= TOTAL_BB_I2C_BUS) {
       return (FALSE);
    }

    obj = &bcm6300_bb_i2c[i2cNum];
    i2cbb = (void *) obj;

    /*
     * Start Bits 
     */
    i2c_start(i2cbb);	//obj->start(i2cbb); /* on the IIC bus */

    /*
     * Format I2C-Address + Write-Select
     */
    i2c_addr_and_rw = dev_addr << 1 | SELECT_READ;
    i2c_write_data_byte(i2cbb, i2c_addr_and_rw);		//obj->write_data_byte(i2cbb, i2c_addr_and_rw);

    /* 
     * Check for the ACK from Slave
     */
    if(!i2c_read_ack(i2cbb)) { 	//if (!obj->read_ack(i2cbb)) {
				/* no response */
        i2c_stop(i2cbb);	//obj->stop(i2cbb);
        bcm6300_bb_info[obj->bus_no].nack_count++; 
        bcm6300_bb_info[obj->bus_no].read_ok_count++;
        return read;
    } 

    /*
     * Read data from Slave
     */
    for (read = 0; read < size; read++) {
        val = i2c_read_data_byte(i2cbb);	//val = obj->read_data_byte(i2cbb);
        /* 
         *  Send ACK to Slave
         */
         if (read < (size - 1)) {
             i2c_write_ack(i2cbb);	//obj->write_ack(i2cbb);
         }       
          *read_buffer++ = val;
    }
     
    i2c_write_nack(i2cbb);	//obj->write_nack(i2cbb);
    i2c_stop(i2cbb);	//obj->stop(i2cbb);

    bcm6300_bb_info[obj->bus_no].rx_bytes += read;

    if (read == size) {
       bcm6300_bb_info[obj->bus_no].read_ok_count++;
    } else {
       bcm6300_bb_info[obj->bus_no].read_fail_count++;
    }

    return (read);
}

/* Read Function of PROCFS attribute */
static ssize_t bb_rtc_proc_read(char *buffer, char **buffer_location,
                                       off_t offset, int buffer_length, int *eof, void *data)
{

	int ret = 0;
 
        ret = sprintf(buffer,"%02X\n", dataInReg);

	return ret;


 /*  uint8 testdata[MAX_RTC_DATA_SIZE] = { 0 };
    uchar reg_addr;
    uchar test_byte[10];
    int read, size, jj;

		reg_addr = 0x00;
		size = 16;

		memset( buffer_data, 0x00, READ_DATA_SIZE);
	
    // write the register address 
    if (bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, testdata, 1, FALSE) != 1) {
       printk("Fail to write register address\n");
       return;
    }

  	read = bb_i2c_read(BB_I2C_BUS_1, DEV_ADDR_RTC, size, testdata);

    if (read != size) {
       printk("Partial read. Total: %d read: %d\n", size, read);
    } 
    
		if (DEBUG_ME)
    	printk("dev: %X reg: %X size: %d read: %d \n", DEV_ADDR_RTC, reg_addr, size, read);
 
    // Dump out data read 
    for (jj = 0; jj < read; jj++) {

    	printk("%02X: %02X\n", jj, testdata[jj]);
	sprintf( test_byte, "%02X", testdata[jj]);
        strcat( buffer_data, test_byte );

    }
    printk("\n");

	if (DEBUG_ME)
			printk("Retrun Buffer: ==%s==\n", buffer_data);

		if ( copy_to_user( buffer_location, buffer_data, (read*2) ) ) {
			return -EFAULT;
		}

		//printk("\nFOR DEBUG:\n%s\n", buffer_location);

	ret = sprintf(buffer,"%02X\n", dataInReg);

		return ret;
*/

}

static void str_to_num(char* in, char* out, int len)
{
    int i;
    memset(out, 0, len);

    for (i = 0; i < len * 2; i ++)
    {
        if ((*in >= '0') && (*in <= '9'))
            *out += (*in - '0');
        else if ((*in >= 'a') && (*in <= 'f'))
            *out += (*in - 'a') + 10;
        else if ((*in >= 'A') && (*in <= 'F'))
            *out += (*in - 'A') + 10;
        else
            *out += 0;

        if ((i % 2) == 0)
            *out *= 16;
        else
            out ++;

        in ++;
    }
    return;
}

/* Write Function of PROCFS attribute */
static ssize_t bb_rtc_proc_write(struct file *file, const char *buffer, 
                                        unsigned long count, void *data)
{

	//	int procfs_buffer_size;
	uchar reg_addr;
	int read, write, size;
	int *dataptr;
	uint8 send_data[MAX_RTC_DATA_SIZE] = { 0 };
	int jj, ret = 0;
	char wr_type;
	int read_command;
	int write_command;
	char tmp[128];
	int write_data;
	uint8 datatemp;

	memset( buffer_data, 0x00, READ_DATA_SIZE);

	uchar input[40];
	memset(input, 0x00, sizeof(input));

	int i = 0;
	int r = count;
	// int length  = ((int *)data)[1];

	if ((count > 34) || (copy_from_user(input, buffer, count-1) != 0))
		return -EFAULT;

	if(strstr(input, "debug")) {
		DEBUG_ME = 1;
		printk("RTC Debug is enabled.\n");
		return;
	} else if (strstr(input, "no debug")) {
		DEBUG_ME = 0;
		printk("RTC Debug is disabled.\n");
		return;
	}
#if 0

	if(strstr(input, "reset")) {
		printk("RTC reset: 06160001010100000000010000011800\n");
		sprintf(input, "06160001010100000000010000011800");	
		size = 16; //write 16 words to rtc
		r = size;
	} else {
		size = 7; //write 7 words to rtc, this is from menu diagmon
	}
#else
	if(strstr(input, "reset")) {
		printk("RTC reset: 06160001010100000000010000011800\n");
		sprintf(input, "06160001010100000000010000011800");	
		size = 16; //write 16 words to rtc
		r = size;
	}
#endif


	if (input[0] == 'r') {


		sscanf(input, "%c 0x%x %s", &wr_type, &read_command, tmp);

		//              printk("read : 0x%2x\n",read_command);

		send_data[0] = (uint8)read_command;

		size = 1;


		if (bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, send_data, size, FALSE) != size) {

			printk("Fail to write register address\n");

			return;
		}

		read = bb_i2c_read(BB_I2C_BUS_1, DEV_ADDR_RTC, size, &datatemp);

		if (read != size) {

			printk("Partial read. Total: %d read: %d\n", size, read);

		}


		dataInReg = datatemp;

//		printk("0x%02X  %d\n",dataInReg,dataInReg);

	}

	else if (input[0] == 'w') {

		sscanf(input, "%c 0x%x 0x%x %s", &wr_type, &write_command, &write_data, tmp);

		//              printk("write : 0x%2x 0x%2x\n",write_command,write_data);

		sscanf(input, "%c 0x%x 0x%x %s", &wr_type, &write_command, &write_data, tmp);

		send_data[0] = (uint8)write_command;
		send_data[1] = (uint8)write_data;

		size = 2;

		if ((write = bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, send_data, size, TRUE)) != size) {
			printk("Partial write. Total (+reg): %d write: %d\n", size, write);
			return -EFAULT;
		}






	}

	else {


		//remove space here.
		for (i = 0; i < r; i ++)
		{
			if (!isxdigit(input[i]))
			{
				memmove(&input[i], &input[i + 1], r - i - 1);
				r --;
				i --;
			}
		}

		//make string to digi
		str_to_num(input, buffer_data, size);

		if (DEBUG_ME) {
			for (jj = 0; jj < 16; jj++) {
				printk("%02X: %02X\n", jj, buffer_data[jj]);
			}
		}


		printk("\n"); 

		reg_addr = 0x0;

		send_data[0] = reg_addr;

		dataptr = (int *) &send_data[1];
		memcpy((uchar *) &send_data[1], buffer_data, size);

		size++;

		/* write the register address */
		if ((write = bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, send_data, size, TRUE)) != size) {
			printk("Partial write. Total (+reg): %d write: %d\n", size, write);
			return 0;
		}
		if (DEBUG_ME)
			printk("Write okay (%d bytes).\n", write-1); 

		if (DEBUG_ME)
			printk("Retrun Buffer: ==%s==\n", input);

	}
	return count;
}


static struct file_operations bb_rtc_proc_fops = {
  read:	bb_rtc_proc_read,
  write: bb_rtc_proc_write
};


/*
 * Description:
 *   Testing function for the i2c write
 *
 * Parameters:
 *   csb - parser control block 
 *
 * Returns:
 */

void i2c_write_command ( void )
{
    uchar dev_addr, reg_addr;
    uint8 data[MAX_BB_I2C_DATA_SIZE] = { 0x1, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88};
    int write, size, bytes_data;
    int *dataptr;

#if 1
		dev_addr = DEV_ADDR_RTC;
		reg_addr = 0x0;
		size = 4;
		bytes_data = 10;
#else
    dev_addr  = (uchar) GETOBJ(int,1);
    reg_addr  = (uchar) GETOBJ(int,2);
    size      = (ulong) GETOBJ(int,3);
    bytes_data = (ulong) GETOBJ(int,4);
#endif

    if (size > 4) {
        printk("Size too big to test\n");
        return; 
    }

    data[0] = reg_addr;

    dataptr = (int *) &data[1];
    memcpy((uchar *) &bytes_data, &data[1], sizeof(int)); 

    size++;
    
    /* write the register address */
    if ((write = bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, data, size, TRUE)) != size) {
       printk("Partial write. Total (+reg): %d write: %d\n", size, write);
       return;
    }

    printk("Write okay.\n"); 
}


/*
 * Description:
 *   Testing function for the i2c read 
 *
 * Parameters:
 *   csb - parser control block 
 *
 * Returns:
 */
void i2c_read_command ( void )
{
    uchar reg_addr;
    uint8 data[MAX_BB_I2C_DATA_SIZE] = { 0 };
    int read, size, jj;

		reg_addr = 0x00;
		size = 20;

    /* write the register address */
    if (bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, data, 1, FALSE) != 1) {
       printk("Fail to write register address\n");
       return;
    }

		read = bb_i2c_read(BB_I2C_BUS_1, DEV_ADDR_RTC, size, data);
    
    if (read != size) {
       printk("Partial read. Total: %d read: %d\n", size, read);
    } 

    printk("dev: %X reg: %X size: %d read: %d data:\n", DEV_ADDR_RTC, reg_addr, size, read);
    /* Dump out data read */

#if 0
    for (jj = 0; jj < read; jj++) {
        printk("%X ", data[jj]);
        if ((jj % 10) == 9) {
            printk("\n"); 
        }
    }

    if (read > 0) {
        printk("\n"); 
    }
#endif

}


/*
 * Description:
 *   Reset RTC alarm 1/2 flag to logic 0 at initial phase.
 *
 * Parameters:
 *
 * Returns:
 */
void reset_alarm_flag(void)
{
	int size, read, write;
	uint8 read_data;
	uint8 send_data[2];
	memset(send_data, 0x0, sizeof(send_data));
	
	send_data[0] = 0x0f;
	
	size = 1;
	
	//data read from 0x0f
	if (bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, send_data, size, FALSE) != size) {
		printk("[RTC] Write RTC Alarm Flag Address Error.\n");
	}

	if (read = bb_i2c_read(BB_I2C_BUS_1, DEV_ADDR_RTC, size, &read_data) != size) {
		printk("[RTC] Read RTC Alarm Flag Value Error.\n");
		printk("Partial read. Total: %d read: %d\n", size, read);
	}
	printk("[RTC] Status Value: 0x%02X\n", read_data);
	
	//reset A1F and A2F
	send_data[0] = 0x0f;
	send_data[1] = (read_data & 0xF0);
	
	size = 2;
	
	if ((write = bb_i2c_write_exe(BB_I2C_BUS_1, DEV_ADDR_RTC, send_data, size, TRUE)) != size) {
		printk("[RTC] Reset RTC Alarm Flag Error.\n");
		printk("Partial write. Total (+reg): %d write: %d\n", size, write);
	}
	else {
		printk("[RTC] Reset RTC Alarm Flag.\n");
	}
}

/***************************************************************************
 * Function Name: gpio2iic_init
 * Description  : Initial function that is called at system startup that
 *                registers this device.
 * Returns      : None.
 ***************************************************************************/
static int __init gpio2iic_init( void )
{
  struct proc_dir_entry *p;

	printk( "gpio2iic: gpio2iic_init entry\n" );	

  p = create_proc_entry(PROC_ENTRY_NAME, 0, 0);
  if (!p) {
     printk("[ERROR] Cannot create /proc/bb_rtc_reg!!!\n");
  }	else	{
//     p->proc_fops = &bb_rtc_proc_fops;
        p->read_proc = bb_rtc_proc_read;
        p->write_proc = bb_rtc_proc_write;

     printk("[Create] Success create /proc/bb_rtc_reg!!!\n");
  }

	memset( buffer_data, 0x00, READ_DATA_SIZE);
	
	i2c_bb_bitgpio_init();

	i2c_read_command();

	reset_alarm_flag();
	
	return 0;
} /* gpio2iic_init */


/***************************************************************************
 * Function Name: gpio2iic_cleanup
 * Description  : Final function that is called when the module is unloaded.
 * Returns      : None.
 ***************************************************************************/
static void __exit gpio2iic_cleanup( void )
{
		printk( "gpio2iic: gpio2iic_cleanup entry\n" );

		remove_proc_entry(PROC_ENTRY_NAME, NULL);
		printk("[Remove] Success remove /proc/bb_rtc_reg!!!\n");

} /* gpio2iic_cleanup */


module_init(gpio2iic_init);
module_exit(gpio2iic_cleanup);

MODULE_DESCRIPTION("I2C-Bus adapter routines for GPIOs in ponderoso");
MODULE_LICENSE("Proprietary");
MODULE_VERSION(GPIO2IIC_VERSION);


