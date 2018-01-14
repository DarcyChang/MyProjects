GetRSSIStatus_ROOT := feature/GetRSSIStatus

# GetRSSIStatus
GetRSSIStatus_SOURCES := $(shell ls $(GetRSSIStatus_ROOT)/*.c 2>/dev/null)
GetRSSIStatus_OBJS := ${GetRSSIStatus_SOURCES:.c=.o}
GetRSSIStatus_HSOURCES := $(shell ls $(GetRSSIStatus_ROOT)/*.h 2>/dev/null)

OBJS += $(GetRSSIStatus_OBJS)

FEATURE_HSOURCES += $(GetRSSIStatus_HSOURCES)
