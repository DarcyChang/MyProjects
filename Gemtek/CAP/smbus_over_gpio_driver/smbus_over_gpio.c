
/* Includes. */
#include <linux/version.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/stddef.h>
#include <linux/kernel.h>
#include <linux/ioport.h>
#include <linux/delay.h>
#include <linux/ctype.h>
#include <linux/gpio.h>
#include <linux/time.h>
#include <linux/i2c.h>
#include <linux/i2c-algo-bit.h>

#include <asm/uaccess.h> /*copy_from_user*/
#include <linux/proc_fs.h>

#if LINUX_VERSION_CODE >= KERNEL_VERSION(3,8,0)
#include <net/net_namespace.h>
#endif

/* Defines. */
#define GPIO2SMBUS_VERSION                     "1.0"

/* Typedefs. */
/*
 * definitions for writing to SMBUS
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

#define DVT_03

#ifdef DVT_03
#define GPIO_PIN_SCL_SMBUS	88 // GPIO_S5[06]
#define GPIO_PIN_SDA_SMBUS	89 // GPIO_S5[07]
#else
#define GPIO_PIN_SCL_SMBUS	87 // GPIO_S5[05]
#define GPIO_PIN_SDA_SMBUS	82 // GPIO_S5[00]
#endif

#define TRUE 1
#define FALSE 0

#define DEV_ADDR_BATTERY	0x0B //Inter ClassConnect Battery address

#define PROC_ENTRY_NAME	"bb_smbus_reg"
//#define CLASS_DEVICE_NAME	"smbus_sys_dir"
#define READ_DATA_SIZE	520

#define MAX_SMBUS_DATA_SIZE	32

typedef unsigned char	uchar;
typedef unsigned char	uint8; 
typedef void (*smbusbb_fn_t) (void *obj); 
typedef uchar (*smbusbb_read_fn_t) (void *obj); 
typedef uchar (*smbusbb_read_parm_fn_t) (void *obj, uchar byte); 
typedef void (*smbusbb_write_fn_t) (void *obj, uchar byte); 

/* Prototypes. */
static int __init gpio2smbus_init( void );
static void __exit gpio2smbus_cleanup( void );
static ssize_t bb_smbus_proc_write(struct file *file, const char *buffer, unsigned long count, void *data);
int word_data_byte_highlow_transfer(int* , uint8, uint8);
extern int hal_gpio_get_value(unsigned int gpio);
extern void hal_gpio_set_value(unsigned int gpio, int value);
extern int hal_gpio_direction_input(unsigned gpio);
extern int hal_gpio_direction_output(unsigned gpio, int value);

/* Globals. */
uint8 buffer_data[READ_DATA_SIZE];
//int Charge_Current = 0x0000;
int Charge_Current = 0xFFFF;

//#define SMBUS_DELAY  10   /* 10 usec i.e. 100k Cycle */
//#define SMBUS_DELAY  1050   /* 1050 nano sec */
#define SMBUS_DELAY  1050   /* 1050 nano sec */
#define	usecdelay(x)	udelay(x)
#define	nanodelay(x)	ndelay(x)

enum bb_state_t {
   BB_START,
   BB_STOP
};

static int DEBUG_ME=0;
/* Bit bang bus controller */

typedef struct smbusbb_
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
    smbusbb_fn_t       start;          
    smbusbb_fn_t       stop;           
    smbusbb_fn_t       write_ack;            
    smbusbb_fn_t       write_nack;            

    /* signal control */
    smbusbb_fn_t       scl_high;       
    smbusbb_fn_t       scl_low;        
    smbusbb_fn_t       scl_input;      
    smbusbb_fn_t       scl_output;     
    smbusbb_read_fn_t  scl_get;       

    smbusbb_fn_t       sda_high;       
    smbusbb_fn_t       sda_low;        
    smbusbb_fn_t       sda_input;      
    smbusbb_fn_t       sda_output;     
    smbusbb_read_fn_t  sda_get;       

    smbusbb_read_fn_t      read_ack;       
    smbusbb_read_fn_t      read_data_bit;  
    smbusbb_write_fn_t     write_data_bit; 
    smbusbb_read_parm_fn_t device_ready;   

    /* high level function */
    smbusbb_read_fn_t  read_data_byte;  
    smbusbb_write_fn_t write_data_byte; 
    smbusbb_read_fn_t  bus_busy;        
} smbusbb_t;

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

smbusbb_t bcm6300_bb_smbus[TOTAL_BB_I2C_BUS]; 


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
static inline void gpio_line_set (int bus_no, int gpio, bool highlow)
{
    /* Set GPIO to HIGH = 1 or LOW = 0*/
    if(highlow == HIGH)
        hal_gpio_set_value(gpio, HIGH);
    else
        hal_gpio_set_value(gpio, LOW);
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
    /* Set GPIO mode is OUTPUT or INPUT */
    if(inout == OUTPUT)
        hal_gpio_direction_output(gpio, 1); // Don't care output is high, just default.
    else
        hal_gpio_direction_input(gpio);
}


/*
 * Description:
 *   set the sda line to output mode with high 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */

static void smbus_sda_output (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_mode_set(obj->bus_no, obj->gpio_pin_sda, OUTPUT);
}
/*
 * Description:
 *   set the sda line to output mode with low.
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_sda_output_with_low (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

	hal_gpio_direction_output(obj->gpio_pin_sda, 0);
   
}

/*
 * Description:
 *   set the scl clock line to low
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_scl_low (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_line_set(obj->bus_no, obj->gpio_pin_scl, LOW);

	nanodelay(obj->delay);

}

/*
 * Description:
 *   set the scl clock line to low without delay time.
 *   Some special case used it.
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_scl_low_without_delay (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;
   	gpio_line_set(obj->bus_no, obj->gpio_pin_scl, LOW);
}


/*
 * Description:
 *   set the sda line to high
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_sda_high (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_line_set(obj->bus_no, obj->gpio_pin_sda, HIGH);
	nanodelay(obj->delay);
}


/*
 * Description:
 *   set the sda line to low
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
 
static void smbus_sda_low (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_line_set(obj->bus_no, obj->gpio_pin_sda, LOW);
	nanodelay(obj->delay);
}

/*
 * Description:
 *   set the scl clock line to high
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_scl_high (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_line_set(obj->bus_no, obj->gpio_pin_scl, HIGH);
	nanodelay(obj->delay);
}
/*
 * Description:
 *   set the scl clock line to high without delay.
 *   Some special case used it. 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_scl_high_without_delay (void *smbusbb)
{
	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_line_set(obj->bus_no, obj->gpio_pin_scl, HIGH);
}

/*
 * Description:
 *   set the scl line to output mode 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
 
static void smbus_scl_output (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	gpio_mode_set(obj->bus_no, obj->gpio_pin_scl, OUTPUT);
}


/*
 * Description:
 *   Write one bit to SDA 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_write_data_bit (void *smbusbb, uchar bit)
{
//   smbusbb_t *obj = (smbusbb_t *) smbusbb;
    /* clock low */
    smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);    
    if (bit & 0x1) {
        smbus_sda_high(smbusbb);	//obj->sda_high(smbusbb);
    } else {
       smbus_sda_low(smbusbb); //obj->sda_low(smbusbb);
    }
   
	 /* data ready, signal */
    smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb);   

    smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb);   
    /* if support clock stretching, need: 
     * while obj->scl_get(smbusbb) == LOW);
     * obj->delay(smbusbb); */
	
    /* data done */
}

/*
 * Description:
 *   Write one bit to SDA for SMBus protocol word write.
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void word_data_write_data_bit (void *smbusbb, uchar bit)
{
//   smbusbb_t *obj = (smbusbb_t *) smbusbb;
    /* clock low */
    smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);    
    if (bit & 0x1) {
        smbus_sda_high(smbusbb);	//obj->sda_high(smbusbb);
    } else {
       smbus_sda_low(smbusbb); //obj->sda_low(smbusbb);
    }
   
	 /* data ready, signal */
    smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb);   
    smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb);   

    /* if support clock stretching, need: 
     * while obj->scl_get(smbusbb) == LOW);
     * obj->delay(smbusbb); */
	
    /* data done */
    smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);    
}


/*
 * Description:
 *   write an ack to the bus 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_write_ack (void *smbusbb)
{
//    smbusbb_t *obj = (smbusbb_t *) smbusbb;

    smbus_sda_output(smbusbb);	//obj->sda_output(smbusbb);
    
	word_data_write_data_bit(smbusbb, LOW);
}


/*
 * Description:
 *   write an nack to the bus 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_write_nack (void *smbusbb)
{
//    smbusbb_t *obj = (smbusbb_t *) smbusbb;

    smbus_sda_output(smbusbb);	//obj->sda_output(smbusbb);
    
    smbus_write_data_bit(smbusbb, HIGH);	//obj->write_data_bit(smbusbb, HIGH);  /* nack is high*/
}


/*
 * Description:
 *   set the sda line to input mode 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_sda_input (void *smbusbb)
{
   smbusbb_t *obj = (smbusbb_t *) smbusbb;

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
	return hal_gpio_get_value(gpio);
}

/*
 * Description:
 *   read the sda signal 
 *
 */
static uchar smbus_sda_get (void *smbusbb)
{
   smbusbb_t *obj = (smbusbb_t *) smbusbb;

   /* return sda gpio state, 1 = high, 0 = low */
   return gpio_line_get(obj->bus_no, obj->gpio_pin_sda);
}


/*
 * Description:
 *   Read 1 bit from SDA line
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 * Return:
 *    1 or 0  (represent the bit)
 */

static uchar smbus_read_data_bit (void *smbusbb)
{
//   smbusbb_t *obj = (smbusbb_t *) smbusbb;
	int bit;
	smbus_scl_low(smbusbb);
	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb); 
   /* if support clock clock stretching should wait for 
    * slave to pull high instead of polling high by master 
    * while (obj->scl_get(smbusbb) == LOW ); */
   
   /* now scl is high, data ready */
	nanodelay(1000);
   	bit = smbus_sda_get(smbusbb);	//obj->sda_get(smbusbb);
	nanodelay(1000);
//	nanodelay(2000);
	smbus_sda_output_with_low(smbusbb);
	smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);     /* scl low, bit read */
	
	return (bit);
}

/*
 * Description:
 *   Read 1 bit from SDA line for SMBus protocol word read.
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 * Return:
 */
static uchar word_read_data_bit (void *smbusbb)
{
//   smbusbb_t *obj = (smbusbb_t *) smbusbb;
	int bit;
	smbus_scl_low(smbusbb);
	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb); 
   	/* if support clock clock stretching should wait for 
     * slave to pull high instead of polling high by master 
     * while (obj->scl_get(smbusbb) == LOW ); */
   
   	/* now scl is high, data ready */
   	bit = smbus_sda_get(smbusbb);	//obj->sda_get(smbusbb);
	nanodelay(2000);
	smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);     /* scl low, bit read */
	
	return (bit);
}
static uchar TEST_word_read_data_bit (void *smbusbb)
{
//   smbusbb_t *obj = (smbusbb_t *) smbusbb;
	int bit;
	smbus_scl_low(smbusbb);
	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb); 
	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb); 
	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb); 
	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb); 
   	/* if support clock clock stretching should wait for 
     * slave to pull high instead of polling high by master 
     * while (obj->scl_get(smbusbb) == LOW ); */
   
   	/* now scl is high, data ready */
   	bit = smbus_sda_get(smbusbb);	//obj->sda_get(smbusbb);
	nanodelay(2000);
	smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);     /* scl low, bit read */
	
	return (bit);
}


/*
 * Description:
 *   read ack from the bus 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static uchar smbus_read_ack (void *smbusbb)
{
//    smbusbb_t *obj = (smbusbb_t *) smbusbb;
    int ack;
	smbus_scl_low(smbusbb);
    smbus_sda_input(smbusbb);	//obj->sda_input(smbusbb);
    //ack = !(obj->read_data_bit(smbusbb)); /* we expect a 0 as the ACK */
    ack = !(smbus_read_data_bit(smbusbb));
    return (ack);
}
/*
 * Description:
 *   read ack from the bus with delay time.
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */

static uchar smbus_read_ack_with_delay (void *smbusbb)
{
    int ack;
	smbus_scl_low(smbusbb);
	usecdelay(32);
    smbus_sda_input(smbusbb);	//obj->sda_input(smbusbb);
    ack = !(smbus_read_data_bit(smbusbb));
    return (ack);
}

/*
 * Description:
 *   Write 1 byte to SDA line
 * 
 * Parm:
 *    smbusbb: bitband control block
 *    sent_byte: data byte
 *
 */
static void smbus_write_data_byte (void *smbusbb, uchar sent_byte)
{
//   smbusbb_t *obj = (smbusbb_t *) smbusbb // darcy : need mark??
   uchar bits_to_shift = 7;
   uchar bit_to_send = 0x80;

    //obj->sda_output(smbusbb);
	smbus_sda_output_with_low(smbusbb);

    while (bit_to_send) {
        smbus_write_data_bit(smbusbb, (sent_byte & bit_to_send) >> bits_to_shift);	//obj->write_data_bit(smbusbb, (sent_byte & bit_to_send) >> bits_to_shift);
        bit_to_send >>= 1;
        bits_to_shift--;
    }
}


/*
 * Description:
 *   Sent a start condition
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */

static void smbus_start (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;
   /* enable sda output mode */
   	smbus_scl_output(smbusbb);
   	smbus_sda_output(smbusbb);

   /*
    * a start condition is a high-to-low transition of SDA with SCL high
    */
   	smbus_sda_high(smbusbb);	//obj->sda_high(smbusbb); /* change sda bit */

   /*
    * put scl high, so the negative edge of sda bit will indicate a
    * start condition
    */
   	smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb);    
   /* if support clock streching */
   /* need: while (obj->scl_get() == low); */

   /* both are high now */
   //obj->sda_low(smbusbb);    
   	smbus_sda_low(smbusbb);
	nanodelay(2000);
   /* obj->scl_low(smbusbb); */
   	obj->state = BB_START;

}

/*
 * Description:
 *   Sent a stop condition 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */
static void smbus_stop (void *smbusbb)
{
   	smbusbb_t *obj = (smbusbb_t *) smbusbb;

   	smbus_sda_output(smbusbb);	//obj->sda_output(smbusbb);

   /*
    * a stop condition is a low-to-high transition of SDA with SCL high
    */
   	smbus_scl_low(smbusbb);	//obj->scl_low(smbusbb);    /* make scl low to prepare to change sda bit */
	/* make SCL delay time.*/
   	smbus_scl_low(smbusbb);	
   	smbus_scl_low(smbusbb);	
   	smbus_scl_low(smbusbb);	

   	smbus_sda_low(smbusbb);	//obj->sda_low(smbusbb);    /* change sda bit */
	/* make SDA delay time.*/
   	smbus_sda_low(smbusbb);	
   	smbus_sda_low(smbusbb);	
	
    /*
     * put scl high, so the positive edge of sda bit will indicate a
     * start condition
     */
    smbus_scl_high(smbusbb);	//obj->scl_high(smbusbb);
	/* make SDA delay time.*/
    smbus_scl_high(smbusbb);	
    smbus_scl_high(smbusbb);
    smbus_scl_high(smbusbb);

    /* pull sda from low to high */ 
    smbus_sda_high(smbusbb);	//obj->sda_high(smbusbb);     /* sda bit transition */
    
    smbus_sda_input(smbusbb);	//obj->sda_input(smbusbb);    /* make sda an input */

    obj->state = BB_STOP;
}

/*
 * Description:
 *   Read 1 byte from the bus
 * 
 * Parm:
 *    smbusbb: bitband control block
 * Return:
 *    one byte
 */
static uchar smbus_read_data_byte (void *smbusbb)
{
//    smbusbb_t *obj = (smbusbb_t *) smbusbb;
    uchar result = 0;
    int i;

    smbus_sda_input(smbusbb);	//obj->sda_input(smbusbb);
    for (i=0; i < 8; i++) {
        result <<= 1;
        result |= smbus_read_data_bit(smbusbb);	//obj->read_data_bit(smbusbb);
    }

    return (result);
}

/*
 * Description:
 *   Read 1 byte from the bus for SMBus protocol word read.
 * 
 * Parm:
 *    smbusbb: bitband control block
 * Return:
 *    one byte
 */
static uchar word_read_data_byte (void *smbusbb)
{
//    smbusbb_t *obj = (smbusbb_t *) smbusbb;
    uchar result = 0;
    int i;

    smbus_sda_input(smbusbb);	//obj->sda_input(smbusbb);
    for (i=0; i < 8; i++) {
		if(i==0){
			result <<= 1;
        	result |= TEST_word_read_data_bit(smbusbb);	//obj->read_data_bit(smbusbb);
		}else{
        	result <<= 1;
        	result |= word_read_data_bit(smbusbb);	//obj->read_data_bit(smbusbb);
		}
    }
    return (result);
}


/*
 * Description:
 *   initialize the bus and set up vector functions 
 * 
 * Parm:
 *    smbusbb: bitband control block
 *
 */

static void smbus_bitbang_init_bus1 (void)
{
   smbusbb_t *bb_smbus = &bcm6300_bb_smbus[BB_I2C_BUS_1];

   /* copy the vector data over */
   //bcopy(&bcm6300_bb_smbus[BB_I2C_BUS_0], bb_smbus, sizeof(smbusbb_t));
   //no use!!! memcpy(&bcm6300_bb_smbus[BB_I2C_BUS_0], bb_smbus, sizeof(smbusbb_t));

   /* set up bus one attribute */ 
    bb_smbus->bus_no       = BB_I2C_BUS_1;   
    bb_smbus->delay        = SMBUS_DELAY;    
    bb_smbus->state        = BB_STOP;      
    bb_smbus->enabled      = TRUE;         
    bb_smbus->lock         = FALSE;      

    bb_smbus->gpio_pin_scl = GPIO_PIN_SCL_SMBUS;
    bb_smbus->gpio_pin_sda = GPIO_PIN_SDA_SMBUS;
}


/************ user callable function ***************/

/*
 * Description:
 *   transmit data to the slave 
 *
 * Parameters:
 *   smbusNum    - bus number
 *   dev_addr  - slave address
 *   data      - data bytes array
 *   send_stop - boolean, sent stop at the end of transaction?
 *
 * Returns:
 *   data byte written. 
 */

int bb_smbus_write (int smbusNum, uchar dev_addr, char *data, int msg_size, int send_stop)
{

	local_irq_disable(); // Disable CPU irq.

    smbusbb_t *obj;
    void  *smbusbb; 
    int   sent   = 0;
 	int count = 0; // for retry
    uchar smbus_addr_and_rw;
    if (smbusNum >= TOTAL_BB_I2C_BUS) {
		local_irq_enable();	// Enable CPU irq.
       	return (FALSE);
    }

    obj = &bcm6300_bb_smbus[smbusNum];
    smbusbb = (void *) obj;
retry:
	if(count >= 3){
		local_irq_enable();
		printk("%s : Try %d fail!\n", __func__, count);
		return 0;
	}
	count++;
    /*
     * Send start signal 
     */
    smbus_start(smbusbb);	//obj->start(smbusbb); 

    /*
     * Send SMBUS slave address + read/write flag
     */
    smbus_addr_and_rw = dev_addr << 1 | SELECT_WRITE;
//	printk("smbus_addr_and_rw = 0x%02x\n", smbus_addr_and_rw);
    smbus_write_data_byte(smbusbb, smbus_addr_and_rw);	//obj->write_data_byte(smbusbb, smbus_addr_and_rw);


    /* 
     * Check for the ACK from Slave
     */
    if(!smbus_read_ack(smbusbb)) { 	//if (!obj->read_ack(smbusbb)) {
        smbus_stop(smbusbb);	//obj->stop(smbusbb); /* abort protocol */
        bcm6300_bb_info[obj->bus_no].nack_count++; 
        bcm6300_bb_info[obj->bus_no].read_fail_count++;
		printk("%s : %d : sent = %d\n", __func__, __LINE__, sent);
        goto retry;
    }

	smbus_sda_output_with_low(smbusbb);
	usecdelay(35);	
    /*
     * Send the actual data
     */
    for (sent = 0; sent < msg_size; sent++) {
        smbus_write_data_byte(smbusbb, *data++);	//obj->write_data_byte(smbusbb, *data++); 

        /* 
         * Check for the ACK from Slave
         */
        if(!smbus_read_ack_with_delay(smbusbb)) { 	//if (!obj->read_ack(smbusbb)) {
            smbus_stop(smbusbb);	//obj->stop(smbusbb); 
            bcm6300_bb_info[obj->bus_no].tx_bytes += sent;
            bcm6300_bb_info[obj->bus_no].nack_count++; 
            bcm6300_bb_info[obj->bus_no].read_fail_count++;
			printk("%s : %d : sent = %d : tx_bytes = %d\n", __func__, __LINE__, sent, bcm6300_bb_info[obj->bus_no].tx_bytes);
        	goto retry;
        } 
    }
	udelay(35);	

    /* Everything is done */ 
    if (send_stop) {
        smbus_stop(smbusbb);	//obj->stop(smbusbb);
    }

    if (sent == msg_size) {
       bcm6300_bb_info[obj->bus_no].write_ok_count++;
    } else {
       bcm6300_bb_info[obj->bus_no].write_fail_count++;
    }

    bcm6300_bb_info[obj->bus_no].tx_bytes += sent;
	printk("%s : %d : sent = %d\n", __func__, __LINE__, sent);
	local_irq_enable();	//Enable CPU irq.
    return sent;
}

/*
 * Description:
 *   receive data from the slave
 *
 * Parameters:
 *   smbusNum    - bus number
 *   dev_addr  - slave address
 *   read_buffer - data bytes array read
 *
 * Returns:
 *   count of data bytes read. 
 */

int bb_smbus_read (int smbusNum, uchar dev_addr, ulong size, uchar *read_buffer)
{
	local_irq_disable(); //Disable CPU irq.

    smbusbb_t *obj;
    void   *smbusbb = (void *) obj; 
    uchar  smbus_addr_and_rw;
    int    read = 0;
 	int count = 0; // for retry
    uchar  val;

    if (smbusNum >= TOTAL_BB_I2C_BUS) {
		local_irq_enable();	// Enable CPU irq.
       	return (FALSE);
    }

    obj = &bcm6300_bb_smbus[smbusNum];
    smbusbb = (void *) obj;

retry: 
	if(count >= 3){
		local_irq_enable();
		printk("%s : Try %d fail!\n", __func__, count);
		return 0;
	}
	count++;
    /*
     * Start Bits 
     */
    smbus_start(smbusbb);	//obj->start(smbusbb); /* on the IIC bus */

    /*
     * Format SMBUS-Address + Write-Select
     */
    smbus_addr_and_rw = dev_addr << 1 | SELECT_READ;
    smbus_write_data_byte(smbusbb, smbus_addr_and_rw);		//obj->write_data_byte(smbusbb, smbus_addr_and_rw);

    /* 
     * Check for the ACK from Slave
     */
    if(!smbus_read_ack(smbusbb)) { 	//if (!obj->read_ack(smbusbb)) {
				/* no response */
        smbus_stop(smbusbb);	//obj->stop(smbusbb);
        bcm6300_bb_info[obj->bus_no].nack_count++; 
        bcm6300_bb_info[obj->bus_no].read_ok_count++;
		printk("%s : %d : read = %d\n", __func__, __LINE__, read);
		goto retry;
    } 
    smbus_sda_input(smbusbb);	//obj->sda_input(smbusbb);
	usecdelay(105);

    /*
     * Read data from Slave
     */
	for (read = 0; read < size; read++) {
    	val = word_read_data_byte(smbusbb);	//val = obj->read_data_byte(smbusbb);
		usecdelay(50);
        /* 
         *  Send ACK to Slave
         */
        if (read < (size - 1)) {
        	smbus_write_ack(smbusbb);	//obj->write_ack(smbusbb);
			smbus_sda_input(smbusbb);
			usecdelay(10);
        }       
//		printk("%s : val = 0x%x\n", __func__, val); //darcy : For debug
        *read_buffer++ = val;
		usecdelay(8); 
	}
    smbus_write_nack(smbusbb);	//obj->write_nack(smbusbb);
    smbus_stop(smbusbb);	//obj->stop(smbusbb);

    bcm6300_bb_info[obj->bus_no].rx_bytes += read;

    if (read == size) {
       bcm6300_bb_info[obj->bus_no].read_ok_count++;
    } else {
       bcm6300_bb_info[obj->bus_no].read_fail_count++;
    }

	local_irq_enable();	// Enable CPU irq.
    return (read);
}

/* Read Function of PROCFS attribute */
static ssize_t bb_smbus_proc_read(char *buffer, char **buffer_location,
                                       off_t offset, int buffer_length, int *eof, void *data)
{

	int ret = 0;
    ret = sprintf(buffer,"%d\n", Charge_Current);
	return ret;
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
static ssize_t bb_smbus_proc_write(struct file *file, const char *buffer, 
                                        unsigned long count, void *data)
{

	//	int procfs_buffer_size;
	uchar reg_addr;
	int read, write, size;
	int *dataptr;
	uint8 send_data[MAX_SMBUS_DATA_SIZE] = { 0 };
	int jj;
	char wr_type;
	int read_command;
	int write_command;
	char tmp[128];
	int write_data;

	memset( buffer_data, 0x00, READ_DATA_SIZE);

	uchar input[40];
	memset(input, 0x00, sizeof(input));

	int i = 0;
	int r = count;

	if ((count > 34) || (copy_from_user(input, buffer, count-1) != 0))
		return -EFAULT;

	if (input[0] == 'r') {
		sscanf(input, "%c 0x%x %s", &wr_type, &read_command, tmp);
		printk("read : 0x%2x\n",read_command);
		send_data[0] = (uint8)read_command;

		int count_proc = 0;
		unsigned int sleep_time = 2000;
//		Charge_Current = 0x0000;
		Charge_Current = 0xFFFF;
retry_proc:
		if(count_proc > 0){
			printk("%s : %d : sleep %d\n", __func__, count_proc, sleep_time);	
			udelay(sleep_time);
		}			
		if(count_proc >= 3){
			printk("%s : Try %d fail!\n", __func__, count_proc);
			return count;
		}
		count_proc++;
		size = 1;
	
		if (bb_smbus_write(BB_I2C_BUS_1, DEV_ADDR_BATTERY, send_data, size, FALSE) != size){
			printk("Fail to write register address\n");
			goto retry_proc;
		}
		size = 3;	
		uint8 datatemp[size];
		read = bb_smbus_read(BB_I2C_BUS_1, DEV_ADDR_BATTERY, size, datatemp);

		if (read != size) {
			printk("Partial read. Total: %d read: %d\n", size, read);
		}
		if(input[5] == 'd')
			datatemp[1]=0x00;	
			
		printk("%s : Data Byte Low : 0x%02X  %d\n", __func__, datatemp[0], datatemp[0]); // data byte low
		printk("%s : Data Byte High : 0x%02X  %d\n", __func__, datatemp[1], datatemp[1]); // data byte high
		printk("%s : PEC : 0x%02X\n", __func__, datatemp[2]); // PEC

		/* Change data byte high and low and transfer Decimal*/
		Charge_Current = 0xFFFF;
		word_data_byte_highlow_transfer(&Charge_Current, datatemp[0], datatemp[1]);

//		if(input[5] == 'd' && (Charge_Current <= 0 || Charge_Current > 100)){
		if(input[5] == 'd' && (Charge_Current < 0 || Charge_Current > 100)){
			printk("goto retry_proc %d and Charge_Current %d\n", count_proc ,Charge_Current);
			goto retry_proc;
		}else if(input[5] == 'a' && (Charge_Current < -2000 || Charge_Current > 2000 || Charge_Current == 0 )){
			printk("goto retry_proc %d and Charge_Current %d\n", count_proc ,Charge_Current);
			goto retry_proc;
		}
		printk("%s : 0x%02X : %d\n", __func__, Charge_Current, Charge_Current); // Darcy : Battery real charge or charge current.
		
	}else if (input[0] == 'w') {

		sscanf(input, "%c 0x%x 0x%x %s", &wr_type, &write_command, &write_data, tmp);

//		printk("write : 0x%2x 0x%2x\n",write_command,write_data);

		send_data[0] = (uint8)write_command;
		send_data[1] = (uint8)write_data;
		size = 2;

		if ((write = bb_smbus_write(BB_I2C_BUS_1, DEV_ADDR_BATTERY, send_data, size, TRUE)) != size) {
			printk("Partial write. Total (+reg): %d write: %d\n", size, write);
			return -EFAULT;
		}
	}else {
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
		if ((write = bb_smbus_write(BB_I2C_BUS_1, DEV_ADDR_BATTERY, send_data, size, TRUE)) != size) {
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

/***************************************************************************
 * Function Name: word_data_byte_highlow_transfer
 * Description  : Change data_byte_high and data_byte_low in SMBus protocol word.
 * Returns      : None.
 ***************************************************************************/
int word_data_byte_highlow_transfer(int *result, uint8 data_byte_low, uint8 data_byte_high)
{
	*result &= ((data_byte_high << 8) | 0xff) ;
	*result &= data_byte_low | 0xff00;
	if(data_byte_high & 0x80)
		*result = *result - 65535;

	return 0;
}

/***************************************************************************
 * Function Name: gpio2smbus_init
 * Description  : Initial function that is called at system startup that
 *                registers this device.
 * Returns      : None.
 ***************************************************************************/
static int __init gpio2smbus_init( void )
{
  	struct proc_dir_entry *p;

	printk( "gpio2smbus: gpio2smbus_init entry\n" );	

  	p = create_proc_entry(PROC_ENTRY_NAME, 0, 0);
  	if (!p) {
		printk("[ERROR] Cannot create /proc/bb_smbus_reg!!!\n");
  	}else{
		p->read_proc = bb_smbus_proc_read;
        p->write_proc = bb_smbus_proc_write;
		
		printk("[Create] Success create /proc/bb_smbus_reg!!!\n");
  	}

	memset( buffer_data, 0x00, READ_DATA_SIZE);
  
  	smbus_bitbang_init_bus1();
	return 0;
} /* gpio2smbus_init */


/***************************************************************************
 * Function Name: gpio2smbus_cleanup
 * Description  : Final function that is called when the module is unloaded.
 * Returns      : None.
 ***************************************************************************/
static void __exit gpio2smbus_cleanup( void )
{
		printk( "gpio2smbus: gpio2smbus_cleanup entry\n" );

		remove_proc_entry(PROC_ENTRY_NAME, NULL);
		printk("[Remove] Success remove /proc/bb_smbus_reg !!!\n");

} /* gpio2smbus_cleanup */


module_init(gpio2smbus_init);
module_exit(gpio2smbus_cleanup);

MODULE_DESCRIPTION("SMBus-Bus adapter routines for GPIOs in Intel ClassConnect");
MODULE_LICENSE("Proprietary");
MODULE_VERSION(GPIO2SMBUS_VERSION);


