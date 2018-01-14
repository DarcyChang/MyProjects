EXE = automount
OBJS = automount.o

CFLAGS += -I$(ROOTDIR)/lib/libusb-0.1.12	
CFLAGS += -I$(ROOTDIR)/lib/include
CFLAGS += -I$(ROOTDIR)/lib/gemtek_include
CFLAGS += -I$(ROOTDIR)/lib/libobj
CFLAGS += -I$(ROOTDIR)/lib/scew-0.4.0/scew	
CFLAGS += -I$(ROOTDIR)/user/expat/lib	

LDFLAGS += -L$(ROOTDIR)/lib -lnvram -lobj -lscew -lexpat
	
all: $(OBJS)
	$(CC) $(CFLAGS) -o $(EXE) $(OBJS) $(LDFLAGS)

romfs:
	$(ROMFSINST) /bin/$(EXE)

clean:
	@rm -rf $(EXE)  *.o

