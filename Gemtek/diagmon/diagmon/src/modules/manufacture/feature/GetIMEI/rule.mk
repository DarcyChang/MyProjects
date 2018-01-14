GetIMEI_ROOT := feature/GetIMEI

# GetIMEI
GetIMEI_SOURCES := $(shell ls $(GetIMEI_ROOT)/*.c 2>/dev/null)
GetIMEI_OBJS := ${GetIMEI_SOURCES:.c=.o}
GetIMEI_HSOURCES := $(shell ls $(GetIMEI_ROOT)/*.h 2>/dev/null)

OBJS += $(GetIMEI_OBJS)

FEATURE_HSOURCES += $(GetIMEI_HSOURCES)
