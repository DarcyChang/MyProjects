EXEC = cpu
OBJS = cpu.o
CFLAGS += -I$(ROOTDIR)/$(LINUXDIR) -I$(ROOTDIR)/user/diagmon
LDFLAGS += -L$(TOPDIR)/apps/diagmon -ldiags

all: $(EXEC)

.c.o:
	$(CC) -c $(CFLAGS) $<

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

romfs:
	$(ROMFSINST) /bin/cpu

clean:
	-rm -f $(EXEC) *.elf *.o

