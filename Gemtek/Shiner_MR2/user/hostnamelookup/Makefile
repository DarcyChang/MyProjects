
LIB_SRC_DIR=.
LIB_DST_DIR=/lib
BIN_DST_DIR=/usr/bin

EXEC = hostnamelookup
SRCS = hostnamelookup.c
OBJS = $(SRCS:.c=.o)

LIB_REAL_NAME = libhostname.so
LIBOBJS = hostnamelookup.o


CFLAGS += -I$(ROOTDIR)/lib  \
		-I$(ROOTDIR)/lib/libshared \
		-I$(ROOTDIR)/lib/sqlite-3.6.22
LDFLAGS += -L$(ROOTDIR)/lib -lsqlite3 \
		-L$(ROOTDIR)/lib/libshared -lshared


all: $(LIB_REAL_NAME)  $(EXEC)

$(LIB_REAL_NAME) : $(LIBOBJS)
	$(CC) -shared -Wl,-soname,$(LIB_REAL_NAME) -o $(LIB_REAL_NAME) $(CFLAGS) $(LDFLAGS) -lc $(LIBOBJS)


#dnsquery: hostnamelookup.o
#	$(CC) $(LDFLAGS) -o $@ hostnamelookup.o $(LDLIBS$(LDLIBS_$@))

clean:
	-rm -f $(EXEC) *.elf *.gdb *.o *.so

#romfs:
#	$(ROMFSINST) $(EXEC) /bin/hostnamelookup

#.PHONY : clean
#clean :
#	-rm -f $(LIB_REAL_NAME) $(LIBOBJS)
#	-rm -f $(EXEC) $(OBJS)

romfs:
	$(ROMFSINST) $(LIB_SRC_DIR)/$(LIB_REAL_NAME)  $(LIB_DST_DIR)/$(LIB_REAL_NAME)
	$(ROMFSINST) $(LIB_SRC_DIR)/$(EXEC)           $(BIN_DST_DIR)/$(EXEC)

