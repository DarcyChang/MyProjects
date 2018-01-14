SDCardTest_ROOT := feature/SDCardTest

# SDCardTest
SDCardTest_SOURCES := $(shell ls $(SDCardTest_ROOT)/*.c 2>/dev/null)
SDCardTest_OBJS := ${SDCardTest_SOURCES:.c=.o}
SDCardTest_HSOURCES := $(shell ls $(SDCardTest_ROOT)/*.h 2>/dev/null)

OBJS += $(SDCardTest_OBJS)

FEATURE_HSOURCES += $(SDCardTest_HSOURCES)
