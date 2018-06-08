#!/bin/bash 
#
# usage:
# ./exec_shc.sh (default directory name is automation)
# or
# ./exec_shc.sh your_dir_name
#
# version 1.0.1

files[0]=autotest.sh
files[1]=menu.sh 
#files[2]=
files[3]=Library/path.sh
files[4]=T55_MFG/bom_check.sh 
files[5]=T55_MFG/burn_in_test_golden.sh
files[6]=T55_MFG/burn_in_test.sh
files[7]=T55_MFG/button_test.sh
files[8]=T55_MFG/checkhw.sh
files[9]=T55_MFG/do_upg
files[10]=T55_MFG/EEPROM_ID_Test.sh
files[11]=T55_MFG/golden_networking.sh
#files[12]=T55_MFG/hwconfig
files[13]=T55_MFG/hwinfo.sh
files[14]=T55_MFG/img_copy
files[15]=T55_MFG/iperf_test.sh
files[16]=T55_MFG/LanLEDTest.sh
files[17]=T55_MFG/memory_test.sh
files[18]=T55_MFG/mem_size_check.sh
#files[19]=T55_MFG/
files[20]=T55_MFG/msata_fw_check.sh
files[21]=T55_MFG/network_test_golden_tcp.sh
files[22]=T55_MFG/network_test_golden_udp_high.sh
files[23]=T55_MFG/network_test_golden_udp_low.sh
files[24]=T55_MFG/network_test.sh
files[25]=T55_MFG/PLoadCheck.sh
files[26]=T55_MFG/rtc_battery_test.sh
files[27]=T55_MFG/rtc_test.sh
files[28]=T55_MFG/sethostname.sh
files[29]=T55_MFG/set_ip.sh
files[30]=T55_MFG/SmartPoE.sh
files[31]=T55_MFG/smart_poe_test.sh
files[32]=T55_MFG/sn_mac_check.sh
files[33]=T55_MFG/stress.sh
files[34]=T55_MFG/superIO.sh
files[35]=T55_MFG/SysLEDTest.sh
files[36]=T55_MFG/test_all.sh
files[37]=T55_MFG/test_lan.sh
files[38]=T55_MFG/test_poe.sh
files[39]=T55_MFG/testRtc.sh
files[40]=T55_MFG/tpm_test.sh
files[41]=T55_MFG/upg_img_from_usb.sh
files[42]=T55_MFG/upg_img.sh
files[43]=T55_MFG/usb_format.sh
files[44]=T55_MFG/wlanSet.sh
files[45]=T55_MFG/wlan_test.sh
files[46]=T55_MFG/stress_1.sh
files[47]=T55_MFG/stress_2.sh
files[48]=T55_MFG/stress_8.sh

if [ -z "$1" ] ; then
	dir_name=automation
else
	dir_name=$1	
fi
echo "[DEBUG] Target directory name = $dir_name"

if [ -d $dir_name ]; then
	echo "[DEBUG] Target directory $dir_name exist, delete it."
	rm -rf $dir_name
fi

cp -rf wg $dir_name

for name in ${files[@]}
do
	echo "[DEBUG] $name"
	shc -r -f $dir_name/$name
	rm $dir_name/$name 
	rm $dir_name/$name.x.c
	mv $dir_name/$name.x $dir_name/$name
done
 
tar -czvf diag.tar.gz automation diag_tools

cp diag_install.sh /media/darcy/16G/
cp diag.tar.gz /media/darcy/16G/
rm -rf /media/darcy/16G/automation
rm -rf /media/darcy/16G/automation_WG_v2.4.0/wg
cp -rf automation /media/darcy/16G/
cp -rf wg /media/darcy/16G/automation_WG_v2.4.0/
cp diag_install_bak.sh diag_install.sh
