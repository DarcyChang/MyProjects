{"BackdoorPacketRetrieveInformation_Req", Information }, 	//1. retrieve the information of firmware version
//{"BackdoorPacketRetrieveMACs_Req", GetMAC},					//2. search the target & retrieve the all of MAC information
//{"BackdoorPacketLoadMACs_Req", LoadMAC},					//3. load MAC
{"BackdoorPacketRestoreToDefault_Req", RestoreToDefault},	//4. restore to default
//{"BackdoorPacketRetrieveSerialNum_Req", GetSN},			//5. retrieve S/N(PIN)
//{"BackdoorPacketLoadSerialNum_Req", SetSN},				//6. load S/N(PIN)
//{"BackdoorPacketSetToButtonLedTest_Req", ButtonLed},	//7. Set to Button & LED Test Mode
//{"BackdoorPacketSetBandto11G_Req", SetBandto11G},			//8. Set to 11g mode
//{"BackdoorPacketSetBandto11A_Req", SetBandto11A},			//9. Set to 11a mode
//{"BackdoorPacketRetrieveSSIDChannel_Req", RetrieveSSIDChannel},		//18. Retrieve the information of SSID & Channel
//{"BackdoorPacketSetSSIDChannel_Req", SetSSIDChannel},		//19. Set SSID & Channel
{"BackdoorPacketUSBTest_Req", USBTest},						//33. USB Test
{"BackdoorPacketSDCardTest_Req", SDCardTest},				//45. SD CArd Test
//{"BackdoorPacketSetLEDOn_Req", LEDon},						//47. Set LED ON Mode
//{"BackdoorPacketSetLEDOff_Req", LEDoff},					//47. Set LED OFF Mode
{"BackdoorPacketCmdLine_Req", SendCommandLine},				//48. Send Command Line(Critical)
//{"BackdoorPacketSetSystemTime_Req", SetSystemTime},			//59. Set System Time
//{"BackdoorPacketGetSystemTime_Req", GetSystemTime},			//60. Get System Time
{"BackdoorPacketGetIMEI_Req", GetIMEI},						//101. Get IMEI
{"BackdoorPacketGetRSSIStatus_Req", GetRSSIStatus},			//105. Get RSSI Status
//{"BackdoorPacketGetProductInfo_Req", GetProductInfo},		//135. Get Product Info
//{"BackdoorPacketSetProductInfo_Req", SetProductInfo},		//136. Get Product Info
//{"BackdoorPacketRetrieveResultGetting_Req", GetResult},	//undefined
//{"BackdoorPacketBackToShippingMode_Req", ApplyShippingMode},
//{"BackdoorPacketBackToTestingMode_Req", ApplyTestingMode},
