
Information_ROOT := feature/Information

# information
Information_SOURCES := $(shell ls $(Information_ROOT)/*.c 2>/dev/null)
Information_OBJS := ${Information_SOURCES:.c=.o}
Information_HSOURCES := $(shell ls $(Information_ROOT)/*.h 2>/dev/null)

OBJS += $(Information_OBJS)

FEATURE_HSOURCES += $(Information_HSOURCES)


