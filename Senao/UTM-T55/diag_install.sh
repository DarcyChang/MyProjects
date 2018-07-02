#!/bin/ash 

tar -xzvf diag.tar.gz

cp -rf automation /root/automation
ln -s /root/automation/T55_MFG/stress_8.sh /root/automation/T55_MFG/stress.sh
ln -s /root/automation/T55_MFG/mfg_version.bak /root/automation/T55_MFG/mfg_version

cp -rf diag_tools/ssh/* /root/.ssh/
cp -rf diag_tools/bin /
cp -rf diag_tools/etc /
cp -rf diag_tools/lib /
cp -rf diag_tools/usr /
cp -rf diag_tools/lib64/* /lib64/

ln -s /usr/share/perl/5.22.1 /usr/share/perl/5.22
rm /lib64/libstdc++.so
ln -s /lib64/libstdc++.so.6.0.21 /lib64/libstdc++.so
ln -s /lib64/libaio.so.1.0.1 /lib64/libaio.so.1
