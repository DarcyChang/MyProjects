KDIR="/usr/src/linux-headers-$(shell uname -r)"
PWD=$(shell pwd)

obj-m := suio_smbus.o

all:
	$(MAKE) -C ${KDIR} M=${PWD} modules
clean:
	$(MAKE) -C ${KDIR} M=${PWD} clean