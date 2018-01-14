
MAIN_HOSTNAMELOOKUPD_ROOT := main/hostnamelookupd

MAIN_LISTS += main_hostnamelookupd

MAIN_HOSTNAMELOOKUPD_SOURCES := $(shell ls $(MAIN_HOSTNAMELOOKUPD_ROOT)/*.c 2>/dev/null)
MAIN_HOSTNAMELOOKUPD_OBJS := ${MAIN_HOSTNAMELOOKUPD_SOURCES:.c=.o}
MAIN_HOSTNAMELOOKUPD_HSOURCES := $(shell ls $(MAIN_HOSTNAMELOOKUPD_ROOT)/*.h 2>/dev/null)

CFLAGS += -I$(ROOTDIR)/lib
LDFLAGS += -L$(ROOTDIR)/lib -lhostname

OBJS += $(MAIN_HOSTNAMELOOKUPD_OBJS)

MAIN_HSOURCES += $(MAIN_HOSTNAMELOOKUPD_HSOURCES)

subdir-romfs += main_hostnamelookupd_romfs

main_hostnamelookupd_romfs:
	$(ROMFSINST) -s /bin/$(EXEC) /usr/bin/hostnamelookupd

main_hostnamelookupd:
	@echo "hostnamelookupd hostnamelookupd_main" >> main_lists.txt

subdir-clean += main_hostnamelookupd_testsuite_clean

# main hostnamelookupd testsuite
MAIN_HOSTNAMELOOKUPD_TESTSUITE_PROG := testsuite_main_hostnamelookupd
MAIN_HOSTNAMELOOKUPD_TESTSUITE_SOURCES := $(shell ls $(MAIN_HOSTNAMELOOKUPD_ROOT)/testsuite/*.c 2>/dev/null)
MAIN_HOSTNAMELOOKUPD_TESTSUITE_OBJS := ${MAIN_HOSTNAMELOOKUPD_TESTSUITE_SOURCES:.c=.o}

ifeq ($(MAIN_HOSTNAMELOOKUPD_ROOT)/testsuite,$(wildcard $(MAIN_HOSTNAMELOOKUPD_ROOT)/testsuite))
ifeq ($(MAIN_HOSTNAMELOOKUPD_ROOT)/testsuite/main.c,$(wildcard $(MAIN_HOSTNAMELOOKUPD_ROOT)/testsuite/main.c))
subdir-testsuite += $(MAIN_HOSTNAMELOOKUPD_TESTSUITE_PROG)
endif
endif

$(MAIN_HOSTNAMELOOKUPD_TESTSUITE_PROG): $(MAIN_HOSTNAMELOOKUPD_TESTSUITE_OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(EXTRA_LIBS)

main_hostnamelookupd_testsuite_clean:
	rm -f $(MAIN_HOSTNAMELOOKUPD_TESTSUITE_PROG) $(MAIN_HOSTNAMELOOKUPD_TESTSUITE_OBJS)
