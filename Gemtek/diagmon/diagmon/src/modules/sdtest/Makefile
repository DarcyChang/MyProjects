EXEC = sdtest
OBJS = sdtest.o
CFLAGS += -I$(ROOTDIR)/$(LINUXDIR) -I$(ROOTDIR)/user/diagmon
LDFLAGS += -L$(TOPDIR)/apps/diagmon -ldiags

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

romfs:
	$(ROMFSINST) /usr/bin/$(EXEC)

clean:
	rm -f $(EXEC) *.o *.a

install:
	install -D -m 755 $(EXEC) $(INSTALL_ROOT)/usr/bin/$(EXEC)
