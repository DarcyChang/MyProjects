EXEC=mptool
DIR=$(shell pwd)
SRCS=$(shell ls $(DIR)/*.c)
OBJS=$(SRCS:.c=.o)
IOUTIL=io_util.o
LIBIOPORT=libioport.a

CFLAGS=-I$(DIR) -Wall
LDFLAGS=

.PHONY:all $(LIBIOPORT) $(EXEC) clean

all: $(EXEC) $(LIBIOPORT)

$(EXEC): $(OBJS)
	$(CC) -o $@ $(OBJS) $(CFLAGS) $(LDFLAGS)

$(LIBIOPORT):
	$(AR) -cru $(LIBIOPORT) $(IOUTIL)
	mkdir -p $(DIR)/lib
	mv $(LIBIOPORT) $(DIR)/lib

%.o:%.c
	$(CC) $(CFLAGS) $(LDFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)
	rm -f $(EXEC)
	rm -rf $(DIR)/lib

romfs:
	$(ROMFSINST) /usr/bin/$(EXEC)