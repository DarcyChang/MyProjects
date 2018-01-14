EXEC = button_led
OBJS = button_led.o

CFLAGS += -Wall -I. -I./include -I$(TOPDIR) -I$(LINUX_DIR)/include
LDFLAGS += -L$(TOPDIR)/apps/diagmon -ldiags

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDLIBS)

romfs:
	$(ROMFSINST) /bin/$(EXEC)

clean:
	rm -f $(EXEC) *.o *.a

