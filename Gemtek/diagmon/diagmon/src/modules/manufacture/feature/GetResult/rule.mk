GetResult_ROOT := feature/GetResult

# GetResult
GetResult_SOURCES := $(shell ls $(GetResult_ROOT)/*.c 2>/dev/null)
GetResult_OBJS := ${GetResult_SOURCES:.c=.o}
GetResult_HSOURCES := $(shell ls $(GetResult_ROOT)/*.h 2>/dev/null)

OBJS += $(GetResult_OBJS)

FEATURE_HSOURCES += $(GetResult_HSOURCES)
