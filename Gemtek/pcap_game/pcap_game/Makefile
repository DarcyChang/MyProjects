
#compiler
CC = gcc

#cflags
CFLAGS = -Wall -std=c99 -g -D_BSD_SOURCE -O3

#object
OBJS = pcap_main.o

all: check_pcap

check_pcap: $(OBJS)
	$(CC) $(OBJS) -o $@
	strip -s $@

pcap_main.o: pcap_main.c pcap_main.h
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f *.o
	rm -f check_pcap 
