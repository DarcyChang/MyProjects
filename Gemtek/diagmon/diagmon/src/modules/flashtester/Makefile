
PROGRAM_NAME:= flashtester
PROGRAM_NAME2:= norflash_tool
PROGRAM_NAME3:= check_badblocks

SOURCE_FILES:= flashtester.o crc32.o
SOURCE_FILES2:= norflash_tool.o
SOURCE_FILES3:= check_badblocks.o

CFLAGS =-s -Os -fomit-frame-pointer -I$(INC_BRCMDRIVER_PUB_PATH)/$(BRCM_BOARD) -I$(INC_BRCMDRIVER_PRIV_PATH)/$(BRCM_BOARD) -I$(INC_BRCMSHARED_PUB_PATH)/$(BRCM_BOARD) -I$(INC_BRCMSHARED_PRIV_PATH)/$(BRCM_BOARD)

CFLAGS += -I$(TOOLCHAIN)/include

INC_ETHERNET_DRIVER_PATH=$(BRCMDRIVERS_DIR)/broadcom/net/enet/bcm9$(BRCM_CHIP)/include

#INC_KERNEL_INC_PATH=$(KERNEL_DIR)/include
INC_KERNEL_INC_PATH=$(ROOTDIR)/$(LINUXDIR)/include 

CFLAGS += -Wall -I$(INC_ETHERNET_DRIVER_PATH) -I$(INC_KERNEL_INC_PATH) -I$(INC_BRCMBOARDPARMS_PATH)/bcm963xx

CFLAGS += $(BRCM_WERROR_CFLAGS)

ifeq ($(strip $(BUILD_WLCTL)), static)
CFLAGS += -DBUILD_STATIC
endif

CFLAGS += -DCONFIG_BCM9$(BRCM_CHIP)

EXTRA_CFLAGS   += -I$(ROOTDIR)/lib/libflash/include
EXTRA_LIBS := -L$(ROOTDIR)/lib/libflash/lib -lflash

#CFLAGS += -I../errlog
#LIBS += ../errlog/errUtils.a

%.o: %.c
	$(CC) -c $(CFLAGS) $(EXTRA_CFLAGS) $(EXTRA_LIBS) -o $@ $< $(LIBS)

TARGETS     = *.o compile load auto-ccld.sh find-systype make-compile make-load systype extra-libs

all: $(PROGRAM_NAME) $(PROGRAM_NAME2) $(PROGRAM_NAME3)

romfs:
	$(ROMFSINST) $(PROGRAM_NAME) /bin/$(PROGRAM_NAME)
	$(ROMFSINST) $(PROGRAM_NAME2) /bin/$(PROGRAM_NAME2)
	$(ROMFSINST) $(PROGRAM_NAME3) /bin/$(PROGRAM_NAME3)

dynamic: $(PROGRAM_NAME) $(PROGRAM_NAME2) $(PROGRAM_NAME3) install

static: $(PROGRAM_NAME).a

$(PROGRAM_NAME): $(SOURCE_FILES)
	$(CC) $(CFLAGS) $(EXTRA_CFLAGS) $(EXTRA_LIBS) -lm -Wl,--allow-shlib-undefined -o $@ $^ $(LIBS)
  
$(PROGRAM_NAME2): $(SOURCE_FILES2)
	$(CC) $(CFLAGS) $(EXTRA_CFLAGS) $(EXTRA_LIBS) -lm -Wl,--allow-shlib-undefined -o $@ $^ $(LIBS)

$(PROGRAM_NAME3): $(SOURCE_FILES3)
	$(CC) $(CFLAGS) $(EXTRA_CFLAGS) $(EXTRA_LIBS) -lm -Wl,--allow-shlib-undefined -o $@ $^ $(LIBS)

$(PROGRAM_NAME).a: $(SOURCE_FILES)
	$(AR) rcs $(PROGRAM_NAME).a $^

clean:
	-rm -f $(PROGRAM_NAME) $(TARGETS) *.o *.a $(PROGRAM_NAME2) $(PROGRAM_NAME3)


