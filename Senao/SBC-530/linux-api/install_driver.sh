#/bin/bash
# Version: 0.1.2

cp nct6775.ko.new /lib/modules/$(uname -r)/kernel/drivers/hwmon/
cp sensors3.conf /etc/
cd /lib/modules/$(uname -r)/kernel/drivers/hwmon/
mv nct6775.ko nct6775.ko.org
ln -s nct6775.ko.new nct6775.ko
modprobe nct6775
