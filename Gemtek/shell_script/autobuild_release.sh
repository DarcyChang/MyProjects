#!/bin/bash
# This script is used to build firmware for EasyConnect 1.2.0 branch
# It will build two versions: one with root permission and one without
# The code on svn branch have no root access
BUILD_NONROOT=1
BUILD_ROOT=1

# XXX: update MAIN_VERSION everytime
MAIN_TREE="1.2.0";
MAIN_VERSION="1.2.19";

SCRIPT_PATH="/home/XXX/intel";
SDK_PATH="/home/volker/intel/release/$MAIN_TREE";
SDK_ENABLE_ROOT_FILE_PATH="/home/volker/intel/release/enable_root";
SDK_DISABLE_ROOT_FILE_PATH="/home/volker/intel/release/disable_root";
FIRMWARE_VERSION="$MAIN_VERSION";

SVN_BRANCH_PATH="http://10.5.88.14/EasyConnect/branch/release"/$MAIN_TREE ;
SVN_USER="XXXXX" ;
SVN_PASSWD="XXXXX" ;

AUTO_BUILD_PATH=$SDK_PATH/autobuild
BUILD_LOG=$AUTO_BUILD_PATH/buildLog

PRINT()
{
	echo $1;
	echo "############" $1 >> $BUILD_LOG;
}

PRINT "Step1: svn up"
cd $SDK_PATH
rm -rf $AUTO_BUILD_PATH
mkdir -p $AUTO_BUILD_PATH
svn up  $SDK_PATH  --username $SVN_USER --password $SVN_PASSWD > $BUILD_LOG 2>&1

PRINT "Step2: update version info"
## Modify version and commit to svn
echo $FIRMWARE_VERSION > $SDK_PATH/etc/version
date > $SDK_PATH/etc/buildDate

PRINT "Step3: Create svn link"
#svn ci --username $SVN_USER --password $SVN_PASSWD -m "============ $FIRMWARE_VERSION ==============" $SDK_PATH/etc/version $SDK_PATH/etc/buildDate
#svn copy $SVN_TRUNK_PATH $SVN_CP_PATGH --username $SVN_USER --password  $SVN_PASSWD -m "create $FIRMWARE_VERSION tag"
svn up  $SDK_PATH  --username $SVN_USER --password $SVN_PASSWD >> $BUILD_LOG 2>&1

PRINT "Step4: Create image directory"
mkdir -p /home/ftpuser/$MAIN_TREE/$FIRMWARE_VERSION

PRINT "Step5: Put releaseLog to FTP"
cp $AUTO_BUILD_PATH/releaseLog /home/ftpuser/$MAIN_TREE/$FIRMWARE_VERSION

PRINT "Step6: start make rooted version"
if [ "$BUILD_ROOT" = "1" ]; then
	cp $SDK_ENABLE_ROOT_FILE_PATH/etc/* $SDK_PATH/etc/ -rf 
	echo $FIRMWARE_VERSION-rooted > $SDK_PATH/etc/version
	cd $SDK_PATH
	make clean >> $BUILD_LOG 2>&1;
	make >> $BUILD_LOG 2>&1;
	if [ -e output/package.tgz ]; then
		cp -f output/package.tgz $AUTO_BUILD_PATH/package.tgz
	else
		PRINT "Build ERROR";
		exit 0;
	fi
	if [ -e output/package_release.tgz ]; then
		cp -f output/package_release.tgz $AUTO_BUILD_PATH/package_"$FIRMWARE_VERSION"_rooted.tgz
	else
		PRINT "Build ERROR";
		exit 0;
	fi
fi

PRINT "Step7: start make non rooted version"
if [ "$BUILD_ROOT" = "1" ]; then
	cp $SDK_DISABLE_ROOT_FILE_PATH/etc/* $SDK_PATH/etc/ -rf
	echo $FIRMWARE_VERSION > $SDK_PATH/etc/version
	cd $SDK_PATH
	make clean >> $BUILD_LOG 2>&1;
	make >> $BUILD_LOG 2>&1;
	if [ -e output/package.tgz ]; then
		cp -f output/package.tgz $AUTO_BUILD_PATH/package.tgz
	else
		PRINT "Build ERROR";
		exit 0;
	fi
	if [ -e output/package_release.tgz ]; then
		cp -f output/package_release.tgz $AUTO_BUILD_PATH/package_$FIRMWARE_VERSION.tgz
	else
		PRINT "Build ERROR";
		exit 0;
	fi
fi

PRINT "Step8: copy files to FTP"
cp $AUTO_BUILD_PATH/package_$FIRMWARE_VERSION.tgz /home/ftpuser/$MAIN_TREE/$FIRMWARE_VERSION
cp $AUTO_BUILD_PATH/package_"$FIRMWARE_VERSION"_rooted.tgz /home/ftpuser/$MAIN_TREE/$FIRMWARE_VERSION
cp $AUTO_BUILD_PATH/md5_txt /home/ftpuser/$MAIN_TREE/$FIRMWARE_VERSION
 
