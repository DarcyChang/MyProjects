#! /bin/bash

sudo apt-get install -y python-software-properties
sudo apt-get install -y software-properties-common

# update
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install -y gnome-session-fallback

# Install python
sudo apt-get install -y python3.6
sudo apt-get install -y python
sudo apt-get install -y python-pip
sudo apt-get install -y idle
sudo apt-get install -y python3-pip
sudo apt-get install -y python-dev
sudo apt-get install -y python3.6-dev
sudo apt-get install -y python3-all
sudo pip3 install pyinstaller
sudo pip3 install pyserial
sudo pip3 install html-testRunner

# Install vim and python plugin
sudo apt-get install -y vim

# For Python code.
# https://github.com/fisadev/fisa-vim-config
curl -O https://raw.githubusercontent.com/vince67/v7_config/master/vim.sh
bash vim.sh
sudo apt-get install -y ctags
sudo apt-get install -y ack-grep

# Install SSH
sudo apt-get install -y openssh-server
sudo /etc/init.d/ssh restart

# Install Git
sudo apt-get install -y git git-review 
sudo apt-get install -y git-core
sudo apt-get install -y subversion

# Install filezilla, PuTTY, 
sudo apt-get install -y filezilla
sudo apt-get install -y putty

# Install tftp
sudo apt-get install -y xinetd tftpd tftp
sudo apt-get install -y tftp-hpa
sudo cp tftp /etc/xinetd.d/
mkdir ~/tftpboot
chmod -R 777 ~/tftpboot
sudo service xinetd restart

# Install samba
#https://wiki.ubuntu.com/Ubuntu_14.04_LTS
sudo apt-get install -y samba samba-common
sudo apt-get install -y python-glade2 system-config-samba
sudo cp /etc/samba/smb.conf ~/tftpboot/
sudo cp smb.conf /etc/samba/smb.conf
#sudo smbpasswd -a darcy
#sudo service smbd restart

#PC端的 windows 要連進來
#\\192.168.75.103
#\\192.168.75.103\darcy

# Some environment settings 
sudo apt-get install -y build-essential
sudo apt-get install -y manpages manpages-posix manpages-posix-dev manpages-dev
sudo apt-get install -y tree
sudo apt-get install -y ncurses-dev #(About make menuconfig)
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y gawk
sudo apt-get install -y libncurses5-dev
sudo apt-get install -y flex
sudo apt-get install -y patch
sudo apt-get install -y g++
sudo apt-get install -y bison
sudo apt-get install -y automake
sudo apt-get install -y kpartx gdisk
sudo apt-get install -y curl
sudo apt-get install -y libjpeg62
sudo apt-get install -y zip

# Install  wireshark
sudo apt-get install -y wireshark

# 透過 Terminal Connecting To The Serial Console
#http://www.cyberciti.biz/hardware/5-linux-unix-commands-for-connecting-to-the-serial-console/

sudo apt-get install -y cu

# Install minicom
sudo apt-get install -y minicom

#upgrade firefix
sudo apt-get install firefox

# nodejs
# https://github.com/nodesource/distributions
# indicate version

# nodejs 8 have a bug.
#curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
# nodejs 6 is LTS version.
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs

# Installing Java
echo "================== Install Java ==========================="
echo "================== Must accept License ==========================="
echo ""
sudo apt-get install -y oracle-java8-installer
sudo apt-get install -y oracle-java8-set-default

# Install Jenkins
wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install -y jenkins
sudo service jenkins restart

# Install appium
echo "================== Install Appium ==========================="
echo ""
sudo cp ia32-libs-raring.list /etc/apt/sources.list.d/
sudo apt-get update
sudo apt-get install -y ia32-libs

sudo npm install -g appium
sudo npm install -g appium-doctor

pip3 install Appium-Python-Client
pip3 install selenium==3.3.1

# Install robot framework
echo "================== Install robotframework ==========================="
echo ""
pip3 install robotframework
pip3 install robotframework-appiumlibrary

# copy .bashrc
echo "================== Copy bashrc ==========================="
echo ""
cp .bashrc ~/.bashrc

echo "================== Copy 51-android.rules ==========================="
echo ""
sudo cp 51-android.rules /etc/udev/rules.d/51-android.rules
sudo chmod a+r /etc/udev/rules.d/51-android.rules

# Install android studio 
echo "================== Downaload and Install Android studio ==========================="
echo ""
wget -t 5 -O android_studio.zip https://dl.google.com/dl/android/studio/ide-zips/2.3.3.0/android-studio-ide-162.4069837-linux.zip
sudo unzip android_studio.zip -d /opt
cd /opt/android-studio/bin
./studio.sh
