#/bin/sh

rmmod r8169
insmod /lib/modules/pgdrv.ko

cp 8168G.cfg.mac /tmp/
cat /tmp/8168G.cfg.mac /etc/8168G.cfg > /tmp/8168GEF.cfg

cp -f /usr/bin/rtnicpg-x86_64 /tmp/rtnicpg-x86_64

cd /tmp/
/tmp/rtnicpg-x86_64 /efuse
/usr/bin/rtnicpg-x86_64 /efuse /r > /var/RTL_phy_config
