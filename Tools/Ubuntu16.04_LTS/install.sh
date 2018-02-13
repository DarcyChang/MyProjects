#! /bin/bash

sudo apt-get install -y python-software-properties
sudo apt-get install -y software-properties-common

sudo add-apt-repository ppa:notepadqq-team/notepadqq
sudo add-apt-repository ppa:jonathonf/python-3.6

sudo apt-get update

sudo apt-get install -y gnome-session-fallback

#1. Install synergy
sudo apt-get install -y quicksynergy synergy

#2. Install vim and notepadqq
sudo apt-get install -y vim
sudo apt-get install -y notepadqq

#18. python
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

cp .bashrc ~/.bashrc
# For Python code.
# https://github.com/fisadev/fisa-vim-config
curl -O https://raw.githubusercontent.com/vince67/v7_config/master/vim.sh
bash vim.sh
sudo apt-get install -y ctags
sudo apt-get install -y ack-grep

# For C code.
#cp .vimrc ~/ 
#cp -r .vim ~/ 
#sudo apt-get install -y ctags
#sudo apt-get install -y screen
#sudo apt-get install -y cscope

#3. Install SSH
sudo apt-get install -y openssh-server
sudo /etc/init.d/ssh restart

#4. Install Git
sudo apt-get install -y git git-review 
sudo apt-get install -y git-core
sudo apt-get install -y subversion

#5. Install filezilla, PuTTY, 
sudo apt-get install -y filezilla
sudo apt-get install -y putty

#6. Install tftp
sudo apt-get install -y xinetd tftpd tftp
sudo apt-get install -y tftp-hpa
sudo cp tftp /etc/xinetd.d/
mkdir ~/tftpboot
chmod -R 777 ~/tftpboot
sudo service xinetd restart

#7. Install samba
#https://wiki.ubuntu.com/Ubuntu_14.04_LTS
sudo apt-get install -y samba samba-common
sudo apt-get install -y python-glade2 system-config-samba
sudo cp /etc/samba/smb.conf ~/tftpboot/
sudo cp smb.conf /etc/samba/smb.conf
sudo smbpasswd -a darcy
sudo service smbd restart

#PC端的 windows 要連進來
#\\192.168.75.103
#\\192.168.75.103\darcy

#8. Ubuntu 底下讓終端機使用彩色提示
#sudo vi ~/.bashrc
#搜尋「#force_color_prompt=yes」這一行字，找到之後將這一行開頭的 # 字號刪除。
#存檔，關閉終端機後重開。

# 9. 
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

#10. 安裝 Team Viewer 10
#https://www.teamviewer.com/zhtw/download/linux.aspx
#https://www.teamviewer.com/zhtw/help/363-How-do-I-install-TeamViewer-on-my-Linux-distribution.aspx
#下載 deb 檔 (預設會放進家目錄的 下載)
#darcy@darcy-System-Product-Name:~$ cd 下載
#darcy@darcy-System-Product-Name:~/下載$ ls
#teamviewer_10.0.46203_i386.deb
#darcy@darcy-System-Product-Name:~/下載$ sudo dpkg -i teamviewer_10.0.46203_i386.deb
#[sudo] password for darcy:
#選取了原先未選的套件 teamviewer。
#（讀取資料庫 ... 目前共安裝了 206735 個檔案和目錄。）
#準備解開 teamviewer_10.0.46203_i386.deb ...
#解開 teamviewer (10.0.46203) 中...
#dpkg: 因相依問題，無法設定 teamviewer：
#teamviewer 相依於 libjpeg62﹔然而：
#  套件 libjpeg62 未安裝。

#dpkg: error processing package teamviewer (--install):
#相依問題 - 保留未設定
#處理時發生錯誤：
#teamviewer

sudo apt-get install -f libjpeg62
#sudo dpkg -i teamviewer_10.0.46203_i386.deb

#11. 安裝 wireshark
sudo apt-get install -y wireshark

#13. RS232
#http://blog.unlink.link/Linux/connect_to_usb2rs232_by_putty_under_ubuntu.html

#一般來講，有 ~/dev/ttyUSBx 的話應該都可以用吧 這已經表示有抓到了

#使用指令:
#$ ll /dev/ttyUSB0

#預設是給root、dialout這兩個群組

#確認自己的帳號是否有在這兩個群組中
#$ id -Gn

#如果沒有就自行新增(****請輸入你的帳號)
#$ sudo adduser **** dialout

#新增完成後，重開機或者是登出再登入之後，可以看到自己的帳號已經加入了這個群組
#這樣就可以正常使用了!!

#14. 透過 Terminal Connecting To The Serial Console
#http://www.cyberciti.biz/hardware/5-linux-unix-commands-for-connecting-to-the-serial-console/

sudo apt-get install -y cu
#darcy@darcy-System-Product-Name:~$ cu -l /dev/ttyUSB0 -s 57600 (cu -l /dev/device -s baud-rate-speed)
#darcy@darcy-System-Product-Name:~$ ~. (離開 Serial Console)

#15. Install Evernote Web APP
#http://www.ubuntu-tw.org/modules/newbb/viewtopic.php?topic_id=93544

#by firefox
#https://marketplace.firefox.com/search?q=evernote

#16. Install Gparted (或從軟體中心內搜尋 Gparted)
sudo apt-get install -y gparted

#17. Install minicom
sudo apt-get install -y minicom

#18. upgrade firefix
sudo apt-get install firefox

#19. nodejs
# https://github.com/nodesource/distributions
# indicate version
# nodejs 6.x is LTS
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
