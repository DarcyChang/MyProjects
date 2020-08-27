#!/bin/bash

dd if=/dev/zero of=/mnt/aaa bs=1M count=1K conv=fsync &
dd if=/dev/zero of=/media/cdrom/aaa bs=1M count=1K conv=fsync &

#rm /mnt/aaa
#rm /media/cdrom/aaa
