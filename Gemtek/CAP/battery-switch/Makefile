LOCAL_DIR := $(shell pwd)
EXEC=battery_switch
SRCS=battery_switch.c 
#SRCS=$(shell pwd)/*.c

LIB_REAL_NAME = libbattery.so
OBJS = battery_switch.o

CFLAGS+=
LDFLAGS+= -lpthread

all: clean binary library romfs
#	$(CC) -o $(EXEC) $(SRCS) $(CFLAGS) $(LDFLAGS) -lpthread 
#	$(CC) -shared -Wl,-soname,$(OBJS) -o $(LIB_REAL_NAME) $(CFLAGS) $(LDFLAGS) -lc $(LIBOBJS) -lpthread

binary : 
	$(CC) -o $(EXEC) $(SRCS) $(CFLAGS) $(LDFLAGS) 

library : 
	$(CC) -shared -Wl,-soname,$(OBJS) -o $(LIB_REAL_NAME) $(CFLAGS) $(LDFLAGS) -lc
#	cp $(LOCAL_DIR)/$(LIB_REAL_NAME) $(OUTPUT_DIR)/lib/ -f
 
clean:
	rm -f *.o
	rm -f $(EXEC)
	rm -f $(LIB_REAL_NAME)

romfs:
	$(ROMFSINST) $(LIB_REAL_NAME) /lib/$(LIB_REAL_NAME)

