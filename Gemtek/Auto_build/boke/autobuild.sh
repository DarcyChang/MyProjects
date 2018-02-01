#!/bin/bash
#############################################################################
#
# This autobuild script is used to build your project, upload your firmware
# to ftp, and send email alerts to your developers automatically. Please
# modify the *autobuild.conf* file first. After executing the script, there
# are five files will be produced:
#
# - .autobuild.log       = Save the entire autobuild configuration file and process.
# - .git.log 	         = Save Git related data.
# - .git_last_build_time = record the time of "git pull" of this auto build.
# - .build.log 	         = The compiling messages when you build your project.
# - .build.err 	         = The warning and error messages when you build your project.
# - .messages	         = Your email alert content.
#

# setup the locale
export LANG=en_US.UTF-8
#LANGUAGE=C

cd /home/evans_lai/projects/WRTM-326ACN/autobuild
# include autoconf.conf
. ./autobuild.conf

# remove log files
rm -rf .autobuild.log .build.err .build.log .git.log .messages 
rm -rf releaseLog firmware.img md5sums
rm -rf firmware-wrtr-300acn.img

#############################################################################
#
# function Exec()
#	This function is used to execute the commands used in this script.
#	And save the execution process to related log files or show it on 
#	standard output.
#
Exec()
{
	echo -e "`date +"[%T]"`\t$*" >> $AUTOBUILD_LOG
	echo $*
	if [ $VERBOSE -eq 1 ]; then
		# Execute command
		$*
	else
		# Execute command
		if [ $1 = "git" ]; then
			echo -e "#`date +"[%T]"`\t$*" >> $AUTOBUILD_GITLOG
			$* 2>&1>> $AUTOBUILD_GITLOG 
		elif [ $1 = "make" ]; then
			echo -e "#`date +"[%T]"`\t$*" >> $AUTOBUILD_BUILDLOG
			$* 1>> $AUTOBUILD_BUILDLOG 2>> $AUTOBUILD_BUILDERR
		else
			$* 1>> $AUTOBUILD_LOG
		fi
	fi
	# If error happens..
	if [ $? -ne 0 ]; then
		echo "Error while executing $1"
		echo "    Command: $*"
		exit 1
	fi
}

#############################################################################
#
# Get the firmware version according to the $CUSTOMER_CONFIG.
# 
EXTERNAL_VERSION=`cat $PROJECT_ROOT/$CUSTOMER_CONFIG | grep FIRMWARE_VERSION | cut -f 2 -d'"' | cut -f 1 -d '-'`
INTERNAL_VERSION=`cat $PROJECT_ROOT/$CUSTOMER_CONFIG | grep FIRMWARE_VERSION | cut -f 2 -d'"' `
INTERNAL_LAST_VERSION=`cat $PROJECT_ROOT/$CUSTOMER_CONFIG | grep FIRMWARE_VERSION | cut -f 2 -d'"' | cut -f 2 -d '-'`
INTERNAL_NEXT_VERSION=$EXTERNAL_VERSION"-"`expr $INTERNAL_LAST_VERSION + 1`
RELEASE_VERSION=$INTERNAL_NEXT_VERSION
CHECK_VERSION=$INTERNAL_VERSION



#############################################################################
#
# Start the autobuild
#

##### Save the user's configuration 

cat > "$AUTOBUILD_LOG" << EOF
##### autobuild.sh setting values #####

AUTOBUILD_ROOT=$AUTOBUILD_ROOT
AUTOBUILD_LOG=$AUTOBUILD_LOG
AUTOBUILD_GITLOG=$AUTOBUILD_GITLOG
CUSTOMER_CONFIG=$CUSTOMER_CONFIG
RELEASE_VERSION=$RELEASE_VERSION
CHECK_VERSION=$CHECK_VERSION
--
EXTERNAL_VERSION=$EXTERNAL_VERSION
INTERNAL_VERSION=$INTERNAL_VERSION
INTERNAL_LAST_VERSION=$INTERNAL_LAST_VERSION
INTERNAL_NEXT_VERSION=$INTERNAL_NEXT_VERSION
--
FTP_SERVER=$FTP_SERVER
FTP_USERNAME=$FTP_USERNAME
FTP_PASSWORD=$FTP_PASSWORD
FTP_DIR=$FTP_DIR
--
EMAILALERT_FROM=$EMAILALERT_FROM
EMAILALERT_TO=$EMAILALERT_TO
EMAILALERT_SUBJECT=$EMAILALERT_SUBJECT
--

##### Start the autobuild #####
Start Time >>> `date +"%Y-%m-%d [%T]"`


EOF



##### Get the Git-related information of this project
Exec cd $PROJECT_ROOT
last_version=`cat $AUTOBUILD_ROOT/GIT_LAST_VERSION.txt`
git pull 
Exec echo "====== after pull ======="
this_version=`git log --oneline -n1 | cut -f 1 -d ' '`

if [ x$last_version = x$this_version ]; then
	Exec echo "Don't need to Make since the version are the same"
	exit 0
fi


BUILD_START_TIME=`cat $AUTOBUILD_GIT_LAST_BUILD`
echo -e "`date +%Y-%m-%d-%T`" > $AUTOBUILD_GIT_LAST_BUILD

BUILD_END_TIME=`cat $AUTOBUILD_GIT_LAST_BUILD`
GITPULL_REVISION=`git log --oneline -n1 | cut -f 1 -d ' '`

cat >> "$AUTOBUILD_LOG" << EOF
##### git Revision Information #####

BUILD_START_TIME=$BUILD_START_TIME
BUILD_END_TIME=$BUILD_END_TIME
GITPULL_REVISION=$GITPULL_REVISION
--

EOF


##### Start to build the project 

#
# Based on each project, you may have your own build procedure.
# The following is an example.
#

# WRTM-326ACN
Exec echo "Update the firmware internal version..."
sed -i "s/FIRMWARE_VERSION=\"$INTERNAL_VERSION\"/FIRMWARE_VERSION=\"$INTERNAL_NEXT_VERSION\"/" $CUSTOMER_CONFIG
date > .build
git add $CUSTOMER_CONFIG .build
git commit -m "======== $RELEASE_VERSION =========" 
git push
git log --oneline -n1 | cut -f 1 -d ' ' > $AUTOBUILD_ROOT/GIT_LAST_VERSION.txt 
Exec make clean
Exec echo "Update the default config files..."
Exec make oldconfig
Exec echo "Target: WRTR-300ACN324CN v$INTERNAL_NEXT_VERSION"
Exec echo "Build the firmware..."
Exec make V=s 
echo start=$BUILD_START_TIME, end=$BUILD_END_TIME
git log --stat --after=$BUILD_START_TIME --before=$BUILD_END_TIME > $AUTOBUILD_ROOT/releaseLog
cp -dpf $PROJECT_ROOT/bin/ramips/openwrt-ramips-mt7620a-wrtm-326acn-squashfs-sysupgrade.bin $AUTOBUILD_ROOT/firmware.img
cp -dpf $PROJECT_ROOT/bin/ramips/md5sums $AUTOBUILD_ROOT/

# WRTR-300ACN324CN
#sed -i 's/# CONFIG_TARGET_ramips_mt7620a_WRTR-300ACN is not set/CONFIG_TARGET_ramips_mt7620a_WRTR-300ACN=y/' .config
#sed -i 's/CONFIG_TARGET_ramips_mt7620a_WRTM-326ACN=y/# CONFIG_TARGET_ramips_mt7620a_WRTM-326ACN is not set/' .config
#Exec make clean
#Exec make V=s
#cp -dpf $PROJECT_ROOT/bin/ramips/openwrt-ramips-mt7620a-wrtr-300acn-squashfs-sysupgrade.bin $AUTOBUILD_ROOT/firmware-wrtr-300acn.img
#cp -dpf $PROJECT_ROOT/bin/ramips/md5sums $AUTOBUILD_ROOT/md5sums-wrtr-300acn

cd $AUTOBUILD_ROOT

##### Upload the firmware  

Upload_firmware()
{
	ftp -d -n $FTP_SERVER << EOF
user $FTP_USERNAME $FTP_PASSWORD
bi
ha
cd $FTP_DIR
mkdir $RELEASE_VERSION
cd $RELEASE_VERSION
put releaseLog
put firmware.img
put md5sums
quit
EOF
}

Upload_firmware2()
{
	ftp -d -n $FTP2_SERVER << EOF
user $FTP2_USERNAME $FTP2_PASSWORD
bi
ha
cd $FTP2_DIR
mkdir $RELEASE_VERSION
cd $RELEASE_VERSION
put releaseLog
put firmware.img
put md5sums
quit
EOF
}

if [ $USE_FTP -eq 1 ]; then
	Upload_firmware
	Upload_firmware2
fi



##### Send the email alert

Send_emailalert()
{
	Exec echo "Forming the email alert messages..."
	cat >> "$EMAILALERT_MESSAGES" << EOF
Date: `date +"%a, %e %Y %T %z"`
From: $EMAILALERT_FROM
To: $receiver
Subject: $EMAILALERT_SUBJECT v$RELEASE_VERSION
Mime-Version: 1.0
Content-Type: text/html; charset=gb2312

Hi all<br><br>
Please download it from<br>
<a href="ftp://$FTP_USERNAME:$FTP_PASSWORD@$FTP_SERVER/$FTP_DIR/$RELEASE_VERSION/blkdsr_le-$RELEASE_VERSION.tar.bz2">
ftp://$FTP_USERNAME:$FTP_PASSWORD@$FTP_SERVER/$FTP_DIR/$RELEASE_VERSION/blkdsr_le-$RELEASE_VERSION.tar.bz2
</a><br><br>
<pre>
`git log --stat --after=$BUILD_START_TIME --before=$BUILD_END_TIME`
</pre>
EOF

	Exec echo "Send the email alert..."
	for receiver in $EMAILALERT_TO ; do
		sed -i "s/^To:.*/To: $receiver/g" $EMAILALERT_MESSAGES
		dos2unix $EMAILALERT_MESSAGES &> /dev/null
		cat $EMAILALERT_MESSAGES | /usr/sbin/sendmail -t
	done
}

if [ $USE_EMAIL -eq 1 ]; then
	Send_emailalert
fi


##### End of the autobuild 

Exec cd $AUTOBUILD_ROOT
echo "##### End of the autobuild #####" >> $AUTOBUILD_LOG
echo "End Time <<< `date +"%Y-%m-%d [%T]"`" >> $AUTOBUILD_LOG

