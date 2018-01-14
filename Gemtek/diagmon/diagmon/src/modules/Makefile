#modules_dir_y	+= module_sample
#modules_dir_y	+= memtester
#modules_dir_y	+= flashtester
modules_dir_y   += manufacture
modules_dir_y   += cpu
modules_dir_y   += usbtest
modules_dir_y   += sdtest
#modules_dir_y	+= io_control
modules_dir_y	+= button_led

all romfs install:
	for i in $(modules_dir_y) ; do make -C $$i $@ || exit $?; done

clean:
	for i in $(modules_dir_y) ; do make -C $$i clean ; done

