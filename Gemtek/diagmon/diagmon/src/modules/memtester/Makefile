
PROGRAM_NAME:= memtester

SOURCE_FILES:= tests.o memtester.o crc32.o

%.o: %.c
	$(CC) -c -o $@ $< $(LIBS)

TARGETS     = *.o compile load auto-ccld.sh find-systype make-compile make-load systype extra-libs

all: $(PROGRAM_NAME)

$(PROGRAM_NAME): $(SOURCE_FILES)
	$(CC) -lm -Wl,--allow-shlib-undefined -o $@ $^ ${LIBS}
  
clean:
	-rm -f $(PROGRAM_NAME) $(TARGETS) *.o *.a

romfs:
	$(ROMFSINST) memtester /bin/memtester
