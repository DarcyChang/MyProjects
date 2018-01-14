#
# rcConf Makefile
#
# Copyright 2006-2009, Gemtek Corporation
# All Rights Reserved.
# 
# $Id$
#

# USE_PTHREAD=1

EXEC = rcConf
SOURCES := $(shell ls *.c 2>/dev/null)
OBJS := ${SOURCES:.c=.o}

RCCONF_TOPDIR := $(shell pwd)

subdir-create :=
subdir-clean :=
subdir-romfs :=
subdir-testsuite :=

EXTRA_INCLUDE := -I. -Iinclude/ 
EXTRA_INCLUDE += -I$(ROOTDIR)/nvram/include -I$(ROOTDIR)/lib/libshared 
EXTRA_INCLUDE += -I$(ROOTDIR)/include -I$(ROOTDIR)/lib/libapi
EXTRA_INCLUDE += -I$(ROOTDIR)/lib/libobj
EXTRA_INCLUDE += -I$(ROOTDIR)/lib/scew-0.4.0/scew
EXTRA_LIBS := -L$(ROOTDIR)/lib/libnvram -lnvram
EXTRA_LIBS += -L$(ROOTDIR)/lib/libshared -lshared
EXTRA_LIBS += -L$(ROOTDIR)/lib/libapi -lapi
EXTRA_LIBS += -L$(ROOTDIR)/lib/libobj -lobj
EXTRA_LIBS += -L$(ROOTDIR)/lib/scew-0.4.0/scew -lscew
EXTRA_LIBS += -L$(ROOTDIR)/lib -lsqlite3
EXTRA_LIBS += -L$(ROOTDIR)/lib/libipv6util -lipv6util
ifeq ($(CONFIG_USER_RCCONF_IDA_CLIENT_SUPPORT),y)
EXTRA_LIBS += -L$(ROOTDIR)/lib/libssl -lcrypto -lssl -L$(ROOTDIR)/lib -lidaClient -lcurl -lexpat
endif
EXTRA_LIBS += -L$(ROOTDIR)/lib/hostnamelookup -lhostname

ifdef USE_PTHREAD
EXTRA_LIBS += -lpthread
endif

CFLAGS += $(EXTRA_INCLUDE)
CFLAGS += -DKERNEL26

ifeq ($(ROOTDIR)/.release,$(wildcard $(ROOTDIR)/.release))
CFLAGS += -DREDIRECT_NULL_DEVICE
else
CFLAGS += -DDEBUG
endif

CFLAGS += -Werror -Wall -fno-strict-aliasing

ifdef USE_PTHREAD
CFLAGS += -DUSE_PTHREAD
endif

ifeq ($(CONFIG_USER_RCCONF_SNMP_SPECIFIC_TRAP_SUPPORT),y)
CFLAGS += -DSNMP_SPECIFIC_TRAP_SUPPORT
endif

ifeq ($(CONFIG_USER_RCCONF_CT_LOGO_SUPPORT),y)
CFLAGS += -DCT_LOGO_SUPPORT
endif

ifeq ($(CONFIG_USER_RCCONF_RALINK_DISABLE_PER_SSID),y)
CFLAGS += -DRALINK_DISABLE_SSID
endif

ifeq ($(CONFIG_USER_RCCONF_IPV6_SUPPORT),y)
CFLAGS += -DIPV6_SUPPORT
endif

-include $(TOOLSDIR)/mkimage/Rule.make
CFLAGS += -D$(IMG_PID) -D$(IMG_VID) -D$(IMG_MID) -D$(IMG_CID)

default: all

-include defaults/Makefile
-include firewall/Makefile
-include main/Makefile
-include services/Makefile
-include systems/Makefile
#-include reconf/Makefile
-include testsuite/Makefile

all: tools subdir-prepare .depend $(EXEC) testsuite

$(EXEC): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(EXTRA_LIBS)

subdir-prepare: $(subdir-create)

testsuite: $(subdir-testsuite)

romfs: all $(subdir-romfs)
	$(ROMFSINST) $(EXEC) /bin/$(EXEC)
	$(ROMFSINST) scripts/nvram-restore-done /etc/nvram-restore-done
	$(ROMFSINST) scripts/mount_shiner.sh /etc/mount_shiner.sh
	$(ROMFSINST) scripts/mount_log.sh /etc/mount_log.sh
	$(ROMFSINST) scripts/mount_nf.sh /etc/mount_nf.sh
	$(ROMFSINST) scripts/firewall/iptables-save-basic-firewall.ej /etc/iptables-save-basic-firewall.ej
	$(ROMFSINST) scripts/firewall/run-basic-firewall.sh /etc/run-basic-firewall.sh
	$(ROMFSINST) scripts/netflow/netflow_database.sh /sbin/netflow_database.sh
	$(ROMFSINST) scripts/netflow/netflow_ip_top.sh /sbin/netflow_ip_top.sh
	$(ROMFSINST) scripts/netflow/netflow_service_top.sh /sbin/netflow_service_top.sh
	$(ROMFSINST) scripts/netflow/netflow_web_top.sh /sbin/netflow_web_top.sh
	$(ROMFSINST) scripts/netflow/netflow_app_top.sh /sbin/netflow_app_top.sh
	$(ROMFSINST) scripts/netflow/netflow_data_backup.sh /sbin/netflow_data_backup.sh
	$(ROMFSINST) scripts/netflow/netflow_time_maintain.sh /sbin/netflow_time_maintain.sh
	$(ROMFSINST) scripts/netflow/send_report_mail.sh /sbin/send_report_mail.sh
	$(ROMFSINST) services/netflow/reserve_lanip  /bin/reserve_lanip
	$(ROMFSINST) services/netflow/sys_up_time  /bin/sys_up_time
	$(ROMFSINST) services/netflow/reduce_nf_conntrack_destroy  /bin/reduce_nf_conntrack_destroy
	$(ROMFSINST) services/netflow/netflow_chk_update  /bin/netflow_chk_update
	$(ROMFSINST) services/netflow/nf_query_hostname  /bin/nf_query_hostname
	$(ROMFSINST) services/security_service/update_table /bin/update_table
	$(ROMFSINST) scripts/force_factory_default.sh /sbin/force_factory_default.sh
	$(ROMFSINST) scripts/security_service/security_service_db_stat.sh /sbin/security_service_db_stat.sh
	$(ROMFSINST) scripts/security_service/security_service_db_backup.sh /sbin/security_service_db_backup.sh
	$(ROMFSINST) scripts/security_service/security_dummy_data.sh /sbin/security_dummy_data.sh
	$(ROMFSINST) scripts/security_service/security_service_send_report.sh /sbin/security_service_send_report.sh
	$(ROMFSINST) scripts/security_service/security_service_export_report.sh /sbin/security_service_export_report.sh
	$(ROMFSINST) scripts/wireless/wireless_htExtCha.sh /sbin/wireless_htExtCha.sh

clean: $(subdir-clean) tools_clean
	rm -f *.o $(EXEC) $(OBJS)
	@find . -name "*.o" | xargs rm -rf
	@rm -f  testsuite_*
	@rm -f .depend

tools:
	${MAKE} -C tools || exit $$?

tools_clean:
	${MAKE} -C tools clean || exit $$?
	
.depend:
	$(CC) $(CFLAGS) -M $(OBJS:.o=.c) > $@.old
	tools/fixupdep/fixupdep $@.old > $@
	rm -f $@.old

ifeq (.depend,$(wildcard .depend))	
include .depend
endif

codeStyle:
	find . -name "*.[ch]" -exec dos2unix {} \;
	find . -name "*.cc" -exec dos2unix {} \;
	find . -name "*.[ch]" -exec indent -bls -ts4 -cdw -bad -bap -bbo -nbc -br -brs -c33 -cd33 -ncdb -ce -ci4 -cli4 -cp33 -cs -d0 -di1 -nfc1 -nfca -nhnl -i4 -ip0 -l110 -nlp -npcs -nprs -npsl -nsaf -nsai -nsaw -nsc -nsob -nss {} \;
	find . -name "*.cc" -exec indent -bls -ts4 -cdw -bad -bap -bbo -nbc -br -brs -c33 -cd33 -ncdb -ce -ci4 -cli4 -cp33 -cs -d0 -di1 -nfc1 -nfca -nhnl -i4 -ip0 -l110 -nlp -npcs -nprs -npsl -nsaf -nsai -nsaw -nsc -nsob -nss {} \;
	find . -name "*.[ch]~" -exec rm -f {} \;
	find . -name "*.cc~" -exec rm -f {} \;


.PHONY: all clean romfs tools testsuite
