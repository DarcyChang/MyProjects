USBTest_ROOT := feature/USBTest

# USBTest
USBTest_SOURCES := $(shell ls $(USBTest_ROOT)/*.c 2>/dev/null)
USBTest_OBJS := ${USBTest_SOURCES:.c=.o}
USBTest_HSOURCES := $(shell ls $(USBTest_ROOT)/*.h 2>/dev/null)

OBJS += $(USBTest_OBJS)

FEATURE_HSOURCES += $(USBTest_HSOURCES)
