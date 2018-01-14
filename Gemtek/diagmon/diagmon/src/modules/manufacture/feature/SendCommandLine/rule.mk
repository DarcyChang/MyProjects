SendCommandLine_ROOT := feature/SendCommandLine

# SendCommandLine
SendCommandLine_SOURCES := $(shell ls $(SendCommandLine_ROOT)/*.c 2>/dev/null)
SendCommandLine_OBJS := ${SendCommandLine_SOURCES:.c=.o}
SendCommandLine_HSOURCES := $(shell ls $(SendCommandLine_ROOT)/*.h 2>/dev/null)

OBJS += $(SendCommandLine_OBJS)

FEATURE_HSOURCES += $(SendCommandLine_HSOURCES)
