CFLAGS_suio_gpio.o=-DDEBUG
KDIR="/usr/src/linux-headers-$(shell uname -r)"
PWD=$(shell pwd)

obj-m := gpio-suio.o

all:
	$(MAKE) -C ${KDIR} M=${PWD} modules
clean:
	$(MAKE) -C ${KDIR} M=${PWD} clean
