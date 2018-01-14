/* Please put the common functions here if they are necessary */
#define MEM_FREE 1

DIAG_CODE getSystemMemInfo(int infoType)
{
        int i;
        FILE* fp;
        char info[64];
        char mem[32];

        fp = fopen("/proc/meminfo","r");
        if( fp==NULL ) {
                perror("fopen");
                return 0;
        }

        /* the 1st line describes the info of TOTAL memory capacity */
        /* MemTotal:         509552 kB */
        /* the 2nd line describes the info of FREE  memory capacity */
        /* MemFree:          451388 kB */
        for( i=0 ; i<2 ; i++ ) {
                if( NULL == fgets(info, 64, fp) ) {
                        perror("fgets");
                        return 0;
                }
                if( i == infoType ) {
                        int j=0;
                        int index=0;
                        while( info[j] != '\n' ) {
                                if( isdigit(info[j]) ) {
                                         mem[index++] = info[j++];
                                } else {
                                         j++;
                                }
                        }
                        mem[index]='\0';
                }
        }
        fclose(fp);

        i = atoi(mem);
        return i;
}

DIAG_CODE get_memory_info(IO_DATA *pio_data)
{
	DIAG_CODE ret = 0;
	DBGMSG("get memory test info\n");

	char str[256];
        unsigned int inst=0;
        int freeMem, size=0, buf=0;
        unsigned int element;

        printf("Start address from 0x1200000(18mb) :");
        memset (str , 0 , 256);
        if (!fgets (str, 255, stdin)) {
                printf ("Error in reading line from stdin\n");
                exit (-1);
        }
        sscanf (str , "%x" , &inst);

        if(inst < 0x1200000 || inst > 0x8000000){
                printf("It will be invalid address.\n");
                return -1;
        }

	freeMem = getSystemMemInfo( MEM_FREE )/1024 - 10;

        printf("Input test size[mb] %d :", freeMem);
        memset (str , 0 , 256);
        if (!fgets (str, 255, stdin)) {
                printf ("Error in reading line from stdin\n");
                exit (-1);
        }

        element = sscanf (str , "%d" , &size);
        if(element == 0 || !strcmp(str, "\n")){
                printf("Invalid size\n");
                return -1;
        }

	if(size > freeMem){
		printf("Over size\n");
		return -1;
	}
	buf = size*1024*1024 + inst;
	buf = buf/1024/1024;

	if(buf > 128){
		printf("It is over memory size. It will stop\n");
		return -1;
	}

	pio_data->u.mem.offset = inst;
        pio_data->u.mem.size = size;

	return DONE;
}
