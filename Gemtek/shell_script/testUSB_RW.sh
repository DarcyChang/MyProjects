#!/bin/sh

FILENAME="LARGETESTFILE"
WAITTIME=10
RWWAITTIME=5
BSSIZE=1M

FOLDERNAME=""
FOLDERNAME=`lsblk | grep sdb1 | cut -d '/' -f 3`
if [ -z "$FOLDERNAME" ]; then
	echo "Do not get USB test path!!!";
	exit 0;
fi

TESTPATH="/media/$FOLDERNAME"
echo "Test path $TESTPATH/$FILENAME"

while true;
do
	echo ======= Write ========;
	dd if=/dev/zero of=$TESTPATH/$FILENAME bs=$BSSIZE count=1k;
	
	echo ======= Clean Cache ========;
	sync; echo 3 > /proc/sys/vm/drop_caches;
	echo ======= Wait $RWWAITTIME to read ========;
	sleep $RWWAITTIME
	
	echo ======= Read ========;
	dd if=$TESTPATH/$FILENAME bs=$BSSIZE of=/dev/null bs=$BSSIZE;
	
	echo ======= Remove $TESTPATH/$FILENAME ========;
	rm $TESTPATH/$FILENAME
	
	echo ======= Clean Cache ========;
	sync; echo 3 > /proc/sys/vm/drop_caches;
	echo ======= Wait $WAITTIME for next run========;
	sleep $WAITTIME
done

