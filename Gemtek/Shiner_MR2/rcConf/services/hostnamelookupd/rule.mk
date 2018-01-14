
SERV_HOSTNAMELOOKUPD_ROOT := services/hostnamelookupd

# hostnamelookupd
SERV_HOSTNAMELOOKUPD_SOURCES := $(shell ls $(SERV_HOSTNAMELOOKUPD_ROOT)/*.c 2>/dev/null)
SERV_HOSTNAMELOOKUPD_OBJS := ${SERV_HOSTNAMELOOKUPD_SOURCES:.c=.o}
SERV_HOSTNAMELOOKUPD_HSOURCES := $(shell ls $(SERV_HOSTNAMELOOKUPD_ROOT)/*.h 2>/dev/null)

OBJS += $(SERV_HOSTNAMELOOKUPD_OBJS)

SERVICES_HSOURCES += $(SERV_HOSTNAMELOOKUPD_HSOURCES)

subdir-romfs += hostnamelookupd_romfs

hostnamelookupd_romfs:

subdir-clean += service_hostnamelookupd_testsuite_clean

# hostnamelookupd testsuite
SERV_HOSTNAMELOOKUPD_TESTSUITE_PROG := testsuite_service_hostnamelookupd
SERV_HOSTNAMELOOKUPD_TESTSUITE_SOURCES := $(shell ls $(SERV_HOSTNAMELOOKUPD_ROOT)/testsuite/*.c 2>/dev/null)
SERV_HOSTNAMELOOKUPD_TESTSUITE_OBJS := ${SERV_HOSTNAMELOOKUPD_TESTSUITE_SOURCES:.c=.o}

ifeq ($(SERV_HOSTNAMELOOKUPD_ROOT)/testsuite,$(wildcard $(SERV_HOSTNAMELOOKUPD_ROOT)/testsuite))
ifeq ($(SERV_HOSTNAMELOOKUPD_ROOT)/testsuite/main.c,$(wildcard $(SERV_HOSTNAMELOOKUPD_ROOT)/testsuite/main.c))
subdir-testsuite += $(SERV_HOSTNAMELOOKUPD_TESTSUITE_PROG)
endif
endif

$(SERV_HOSTNAMELOOKUPD_TESTSUITE_PROG): $(SERV_HOSTNAMELOOKUPD_TESTSUITE_OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(EXTRA_LIBS)

service_hostnamelookupd_testsuite_clean:
	rm -f $(SERV_HOSTNAMELOOKUPD_TESTSUITE_PROG) $(SERV_HOSTNAMELOOKUPD_TESTSUITE_OBJS)
