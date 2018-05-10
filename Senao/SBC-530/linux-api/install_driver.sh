#/bin/bash
# Version: 0.1.0


cp nct6775.ko.senao /lib/modules/$(uname -r)/kernel/drivers/hwmon/
cd /lib/modules/$(uname -r)/kernel/drivers/hwmon/
mv nct6775.ko nct6775.ko.org
ln -s nct6775.ko.senao nct6775.ko
modprobe nct6775
