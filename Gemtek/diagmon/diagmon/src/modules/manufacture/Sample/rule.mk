Sample_ROOT := feature/Sample

# Sample
Sample_SOURCES := $(shell ls $(Sample_ROOT)/*.c 2>/dev/null)
Sample_OBJS := ${Sample_SOURCES:.c=.o}
Sample_HSOURCES := $(shell ls $(Sample_ROOT)/*.h 2>/dev/null)

OBJS += $(Sample_OBJS)

FEATURE_HSOURCES += $(Sample_HSOURCES)
