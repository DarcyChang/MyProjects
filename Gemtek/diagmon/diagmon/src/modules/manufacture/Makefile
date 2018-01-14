# Makefile

CURRENT_TOPDIR := $(shell pwd)

CFLAGS += -Wall -I. -I./include -I$(TOPDIR)
LDFLAGS += -L$(TOPDIR)/apps/diagmon -ldiags


SOURCES := $(shell ls *.c 2>/dev/null)
OBJS := ${SOURCES:.c=.o}

EXEC = wizard

OBJS := wizard.o 

-include feature/rule.mk

all: create_feature_h $(EXEC)

create_feature_h:
	@rm -f include/feature.h
	@rm -f include/feature.txt
	@echo $(FEATURE_HSOURCES) > include/feature.txt
	@sed < include/feature.txt > include/feature.h \
        -e 's/[ ][ ]*/> </g' \
        -e 's/[ ][ ]*/\n#include /g' \
        -e 's/^/#include </' \
        -e 's/$$/>/'

$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

clean:
	rm -f *.o $(EXEC)
	rm -f include/feature.h include/feature.txt
	rm -f $(OBJS)

romfs:
	$(ROMFSINST) /usr/bin/$(EXEC)

install:
	install -D -m 755 $(EXEC) $(INSTALL_ROOT)/usr/bin/$(EXEC)
