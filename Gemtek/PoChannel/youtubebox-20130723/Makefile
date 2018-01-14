###############################################################################
#
# 	Makefile for youtubebox
#

ROOTDIR = $(shell pwd)
HEADERDIR = $(ROOTDIR)/include
LIBDIR = $(ROOTDIR)/utube

MIPS_TOOLCHAIN_DIR = ${BR2_TOOLCHAIN_EXTERNAL_PATH}/bin
#CROSS_COMPILE = ${MIPS_TOOLCHAIN_DIR}/${BR2_TOOLCHAIN_EXTERNAL_PREFIX}-
CROSS_COMPILE = /opt/mipsel-4.4/bin/mipsel-linux-gnu-
#MIPS_SDK_DIR = $(TOPDIR)/build/staging
MIPS_SDK_DIR = /home/darcy/ALi/SDK-20130813/extern/build/staging
CC = ${CROSS_COMPILE}gcc

CFLAGS = -g -Wall --sysroot=${MIPS_SDK_DIR} -I${MIPS_SDK_DIR}/usr/include -I${MIPS_SDK_DIR}/usr/include/libxml2 -I${HEADERDIR}
LDFLAGS = --sysroot=${MIPS_SDK_DIR} -L$(MIPS_SDK_DIR)/usr/lib -lxml2 -L$(LIBDIR) -lutube -lconfig -ljson

export ROOTDIR HEADERDIR LIBDIR MIPS_TOOLCHAIN_DIR CROSS_COMPILE MIPS_SDK_DIR CC


.PHONY: all youtube utube clean

all: youtube install

youtube: main.o
	make -C utube
	$(CC) -o $@ $^ $(LDFLAGS)

install:
	cp include/youtubeAPI.h ${MIPS_SDK_DIR}/usr/include/GTK_gui/page_gui

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	make -C utube clean
	rm -f youtube *.o

