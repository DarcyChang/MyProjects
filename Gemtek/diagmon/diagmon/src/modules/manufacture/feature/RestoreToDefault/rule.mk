RestoreToDefault_ROOT := feature/RestoreToDefault

# RestoreToDefault
RestoreToDefault_SOURCES := $(shell ls $(RestoreToDefault_ROOT)/*.c 2>/dev/null)
RestoreToDefault_OBJS := ${RestoreToDefault_SOURCES:.c=.o}
RestoreToDefault_HSOURCES := $(shell ls $(RestoreToDefault_ROOT)/*.h 2>/dev/null)

OBJS += $(RestoreToDefault_OBJS)

FEATURE_HSOURCES += $(RestoreToDefault_HSOURCES)
