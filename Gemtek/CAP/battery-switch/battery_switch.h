#include <pthread.h>
#include <errno.h>

#define DBGMSG(fmt, args...)
#define GPIO_PIN_BATTERY_SWITCH  213 // GPIO_S0_SC[059]

extern int Detect_Battery_Type(void);
extern int SMBus_Battery_Status(void);
extern int IIC_Battery_Status(void);
extern int SMBus_Battery_Charge_Status(void);
extern int IIC_Battery_Charge_Status(void);
extern int GPIO_Status(void);
extern int BatteryStatus(void);
extern int BatteryChargeStatus(void);
