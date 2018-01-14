/* Please put the common functions here if they are necessary */

DIAG_CODE get_cputest_input(int option, IO_DATA *pio_data)
{
        DIAG_CODE ret = 0;
        DBGMSG("get cpu test input\n");

	char str[256];
	unsigned int sec, pin;
	int value;

	if(option == 0 || option == 1) 	// CPU Full Loading Tool, Show CPU Usage
	{
	        printf("Test duration(seconds) :");
        	memset (str , 0 , 256);
	        if (!fgets (str, 255, stdin)) 
		{
        	        printf ("Error in reading line from stdin\n");
                	exit (-1);
	        }
        	sscanf (str , "%d" , &sec);

		pio_data->u.cpu.time_sec = sec;

		return DONE;
	}
	else if(option == 2) 		// Set GPIO Tool
	{
                printf("GPIO pin number(0~31) :");
                memset (str , 0 , 256);
                if (!fgets (str, 255, stdin))
                {
                        printf ("Error in reading line from stdin\n");
                        exit (-1);
                }
                sscanf (str , "%d" , &pin);

                printf("Setting value(0: LOW, 1: HIGH) :");
                memset (str , 0 , 256);
                if (!fgets (str, 255, stdin))
                {
                        printf ("Error in reading line from stdin\n");
                        exit (-1);
                }
                sscanf (str , "%d" , &value);


                pio_data->u.cpu.pin_index = pin;
                pio_data->u.cpu.value = value;

                return DONE;
	}
	else				// Get GPIO Tool
	{
                printf("GPIO pin number(0~31) :");
                memset (str , 0 , 256);
                if (!fgets (str, 255, stdin))
                {
                        printf ("Error in reading line from stdin\n");
                        exit (-1);
                }
                sscanf (str , "%d" , &pin);

                pio_data->u.cpu.pin_index = pin;

                return DONE;
	}

}

