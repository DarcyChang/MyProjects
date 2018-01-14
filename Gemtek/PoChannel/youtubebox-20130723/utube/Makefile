#CROSS_COMPILE = arm-linux-uclibc

CC = $(CROSS_COMPILE)gcc

OBJS = libutube.so 
SRCS = youtubeAPI.c

CFLAGS := -g -Wall --sysroot=${MIPS_SDK_DIR} -I${MIPS_SDK_DIR}/usr/include -I${MIPS_SDK_DIR}/usr/include/libxml2 -I${HEADERDIR} 
LDFLAGS := --sysroot=${MIPS_SDK_DIR} -L$(MIPS_SDK_DIR)/usr/lib -lxml2 -ljson -lconfig

all: urldecoder $(OBJS) install

$(OBJS): libutube.o
	$(CC) -shared -o $(OBJS) youtubeAPI.o

install:
	cp libutube.so $(MIPS_SDK_DIR)/usr/lib/

libutube.o: $(SRCS) 
	$(CC) $(LDFLAGS) $(CFLAGS) -c -Wall -Werror -fpic $(SRCS)

urldecoder: urldecoder.c
	$(CC) -Wall -o urldecoder urldecoder.c

clean:
	rm -rf *.o libutube.so urldecoder
	
