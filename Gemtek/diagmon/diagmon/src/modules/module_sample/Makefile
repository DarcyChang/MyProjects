EXEC = module_sample
OBJS = module_sample.o
CFLAGS += -I$(ROOTDIR)/$(LINUXDIR) -I$(ROOTDIR)/user/diagmon
LDLIBS += -L$(ROOTDIR)/user/diagmon -ldiags

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDLIBS)

romfs:
	$(ROMFSINST) /bin/$(EXEC)

clean:
	rm -f $(EXEC) *.o *.a

