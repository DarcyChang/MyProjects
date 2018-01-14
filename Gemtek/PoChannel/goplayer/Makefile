#!/bin/sh

# ali mips toolchain dir
ALI_MIPS_TOOLCHAIN_DIR=/opt/mipsel-4.4/bin

# ali mips sdk dir
#ALI_MIPS_SDK_DIR=../../../..
ALI_MIPS_SDK_DIR=/home/darcy/ALi/SDK-20130924/extern/build


CROSS_COMPILE=${ALI_MIPS_TOOLCHAIN_DIR}/mipsel-linux-gnu-

AR=${CROSS_COMPILE}ar
AS=${CROSS_COMPILE}as
LD=${CROSS_COMPILE}ld
NM=${CROSS_COMPILE}nm
CC=${CROSS_COMPILE}gcc
CXX=${CROSS_COMPILE}g++
FC=${CROSS_COMPILE}gfortran
RANLIB=${CROSS_COMPILE}ranlib
STRIP=${CROSS_COMPILE}strip
OBJCOPY=${CROSS_COMPILE}objcopy

CFLAGS=-Os -pipe -O2 -g -mtune=mips32r2 -mabi=32 --sysroot=${ALI_MIPS_SDK_DIR}/staging/ -I${ALI_MIPS_SDK_DIR}/toolchain/linux/include -I${ALI_MIPS_SDK_DIR}/staging/usr/include -I${ALI_MIPS_SDK_DIR}/staging/usr/include/glib-2.0 -I${ALI_MIPS_SDK_DIR}/staging/usr/include/glib-2.0/lib -I${ALI_MIPS_SDK_DIR}/staging/usr/lib/glib-2.0/include -Wall
LDFLAGS=--sysroot=${ALI_MIPS_SDK_DIR}/staging/ -L${ALI_MIPS_SDK_DIR}/staging/lib -L${ALI_MIPS_SDK_DIR}/staging/usr/lib

all: cmdpipe.c goplayer_sample.c
	${CC} ${CFLAGS} ${LDFLAGS} -lpthread cmdpipe.c goplayer_sample.c -o goplayer_sample -lgoplayer -lshared -lgtkxml -lcurl


clean:
	rm -f goplayer_sample *.o

