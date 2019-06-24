#!/bin/sh
# This is the script to check and instal ubuntu system.
# written:	carywu@amlogic.com
# Update:		2014-8-18
# Version:	1.0
#
#
#########################
# === global config === #
#########################
WORKDIR=`dirname $(readlink -f $0)`

LOGFILE="$WORKDIR/install.log"

DOWNLOAD_URL="http://openlinux.amlogic.com:8000/deploy"

OS_MACHINE=`uname -m`

OS_NUMBER=`cat /etc/lsb-release  |grep RELEASE |awk -F "=" '{print $2}' |awk -F "." '{print $1}'`

#########################
#   === function ===    #
#########################



check_root()
{
	if [ "$(id -u)" != "0" ]; then
	echo " "
	echo "
!! This script must be run as root !!!
Script will exit, you need run it again" 1>&2
	echo " "
	exit 1
	fi
}


check_OS_version()
{
	if [ "$OS_MACHINE" != "x86_64" ]; then
	echo " "
	echo "
Sorry, Please use 64bit Ubuntu!!
will exit, sorry~~ "
	echo " "
	exit 1
	fi

	if [ "$OS_NUMBER" != "12" || "$OS_NUMBER" != "14"]; then
	echo "
Sorry, Here we suggest the Ubuntu 12.04 or 14.04 version !!
Will exiit !! "
	exit 1
	fi

}

check_openlinux()
{
      ping -c 2 -i 0.2 -W 3 openlinux.amlogic.com &> /dev/null
      if [ $? -eq 0 ];then
      echo "Network is good"
      else
      echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
      echo "Sorry, looks like your PC can't access to openlinux, check your network!"
      echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
      exit 1
     fi
}

install_12()
{
	apt-get install -y gcc-4.4 g++-4.4 gcc-4.4-multilib build-essential
	apt-get install -y cryptsetup cryptsetup-bin libcryptsetup-dev uuid-dev libdevmapper-dev libpopt-dev
	apt-get install -y lzop
}

install_14()
{
	apt-get install -y lzop
        ### install the library
           apt-get install -y git-core gnupg flex gperf build-essential \
           zip curl libc6-dev libncurses5-dev:i386 x11proto-core-dev \
           libx11-dev:i386 libreadline6-dev:i386 libgl1-mesa-dev:i386 \
           g++-multilib mingw32 tofrodos python-markdown libxml2-utils xsltproc zlib1g-dev:i386
}

install_16()
{
      apt-get update
      apt-get install -y openjdk-8-jdk
}

install_software()
{
	echo "We are going to do apt-get update..... please wait......"
	add-apt-repository -y ppa:rayanayar/cryptsetup
	apt-get update
	echo "############################################################"
	echo "#####       going to install samba,nfs,vim             #####"
	echo "############################################################"
	apt-get install -y automake make perl gcc g++
	apt-get install -y bison git gperf libxml2-utils zip unixodbc dos2unix java-common vim autofs

	if [ "$OS_NUMBER" = "12" ];then
	install_12
	else if [ "$OS_NUMBER" = "14" ];then
	install_14
	else
        install_16
        fi
        fi

}
Install_tools()
{


	echo "############################################################"
	echo "#####       going to install gnutools, arm gcc         #####"
	echo "############################################################"
	if [ -f /usr/bin/wget ];then
	if [ -d /opt/CodeSourcery ];then
	echo "ERROR 1:
Hello, there is folder CodeSourcery under /opt, System will not download files from $DOWNLOAD_URL
if you still need download it, please download from $DOWNLOAD_URL/CodeSourcery.tar.gz" >> $LOGFILE
	else
	wget --continue $DOWNLOAD_URL/CodeSourcery.tar.gz -P /tmp/
	tar -zxvf /tmp/CodeSourcery.tar.gz -C /opt
	fi

	if [ -d /opt/gcc-linaro-aarch64-linux-gnu-4.9-2014.09_linux ];then
	echo "ERROR 1:
Hello,System will not download files from $DOWNLOAD_URL
if you still need download it, please download from $DOWNLOAD_URL/gcc-linaro-aarch64-linux-gnu-4.9-2014.09_linux.tar" >> $LOGFILE
	else
	wget --continue $DOWNLOAD_URL/gcc-linaro-aarch64-linux-gnu-4.9-2014.09_linux.tar -P /tmp/
	tar -xvf /tmp/gcc-linaro-aarch64-linux-gnu-4.9-2014.09_linux.tar -C /opt
	fi

	if [ -d /opt/gcc-linaro-aarch64-none-elf-4.8-2013.11_linux ];then
	echo "ERROR 1:
Hello,System will not download files from $DOWNLOAD_URL
if you still need download it, please download from $DOWNLOAD_URL/gcc-linaro-aarch64-none-elf-4.8-2013.11_linux.tar" >> $LOGFILE
	else
	wget --continue $DOWNLOAD_URL/gcc-linaro-aarch64-none-elf-4.8-2013.11_linux.tar -P /tmp/
	tar -xvf /tmp/gcc-linaro-aarch64-none-elf-4.8-2013.11_linux.tar -C /opt
	fi

	if [ -d /opt/gcc-linaro-arm-linux-gnueabihf ];then
	echo "
ERROR 2:
Hello, there is folder gcc-linaro-arm-linux-gnueabihf under /opt, System will not download files from $DOWNLOAD_URL
if you still need download it, please download from $DOWNLOAD_URL/gcc-linaro-arm-linux-gnueabihf.tar.gz" >> $LOGFILE
	else
	wget --continue $DOWNLOAD_URL/gcc-linaro-arm-linux-gnueabihf.tar.gz -P /tmp/
	tar -zxvf /tmp/gcc-linaro-arm-linux-gnueabihf.tar.gz -C /opt
	fi
	if [ -d /opt/gnutools ];then
	echo "
ERROR 3:
Hello, there is folder gcc-linaro-arm-linux-gnueabihf under /opt, System will not download files from $DOWNLOAD_URL
if you still need download it, please download from $DOWNLOAD_URL/gcc-linaro-arm-linux-gnueabihf.tar.gz" >> $LOGFILE
	else

	wget --continue $DOWNLOAD_URL/gnutools.tar.gz -P /tmp
	tar -zxvf /tmp/gnutools.tar.gz -C /opt
	fi
	if [ -d /opt/arc-4.8-amlogic-20130924-r2 ];then
	echo "
ERROR 4:
Hello, there is folder arc-4.8-amlogic-20130904-r2 under /opt, System will not download files from $DOWNLOAD_URL
if you still need download it, please download from $DOWNLOAD_URL/arc-4.8-amlogic-20130904-r2.tar.gz" >> $LOGFILE
	else
	wget --continue $DOWNLOAD_URL/arc-4.8-amlogic-20130904-r2.tar.gz -P /tmp
	tar -zxvf /tmp/arc-4.8-amlogic-20130904-r2.tar.gz -C /opt
	fi
	if [ ! -f /etc/profile.d/TOOLSENV.sh ];then
	wget $DOWNLOAD_URL/TOOLSENV.sh -P /etc/profile.d
	fi

	wget $DOWNLOAD_URL/repo -P /usr/bin

	chmod +x /usr/bin/repo
	chmod +x /etc/profile.d/*.sh

	else
        echo "I can't fint wget --continue command, script need this tool to download tools, please use apt-get install wget --continue firstly"
	exit
	fi

}

install_java()
{
	echo "############################################################"
	echo "#####       going to install sun-java6 and library     #####"
	echo "############################################################"
#	apt-get install -y unixodbc java-common
#	   ln -s /usr/lib/i386-linux-gnu/mesa/libGL.so.1 /usr/lib/i386-linux-gnu/libGL.so

	## Going to download sun-java6 26 version...
	echo "Downloading all java version to /opt..."
	#wget --continue http://openlinux.amlogic.com:8000/deploy/jdk1.6.0_29.tar.gz -P /tmp/
	wget --continue http://openlinux.amlogic.com:8000/deploy/jdk1.7.0_65.tar.gz -P /tmp/
	wget --continue http://openlinux.amlogic.com:8000/deploy/openjdk-1.8.tar.gz -P /tmp/

	#tar -zxvf /tmp/jdk1.6.0_29.tar.gz -C /opt
	tar -zxvf /tmp/jdk1.7.0_65.tar.gz -C /opt
	tar -zxvf /tmp/openjdk-1.8.tar.gz -C /opt
}

install_x_desktop()
{
	echo "############################################################"
	echo "#####       going to install ubuntu desktop software   #####"
	echo "############################################################"

	apt-get install -y ubuntu-desktop

}

timing()
{
	echo  "\aJust please wait for 30 seconds....\r"

	for i in $(seq 30|tac);do
           echo -n "${i}."
           sleep 1
	done

}

###TODO####
### NOT START BY NOW ####
check_software()
{
	if [ ! -f /tmp/software.list ]
	then
	wget --continue http://openlinux.amlogic.com:8000/deploy/software.list -P /tmp
	fi

	SOFTLIST=/tmp/software.list
	SOFT=`cat $SOFTLIST`
	for soft in $SOFT
	do
	apt-get install -y $soft
	done

}

exit_script()
{
	echo "Installation finished...will exit"
	exit 1

}

echo "
####################################################################################################
# writer: cary.wu@amlogic.com
# Owner:  Amlogic IT group
# Date:	  2012-10-11
#
# README:
# This is a simple script help setup the Android build environment automatically..after done
# your ubuntu will have the same tools and library as Amlogic servers...
# This script will only support Ubuntu 12.04 OS and no other choose now..please make sure
# your OS version is 12.04 Ubuntu 64bit, Thank you!
#
# script will download tools and save them to /opt directory...
# script will create new shell script to /etc/profile.d/ directory...
#
#
# !!ATTENTION!!
# please make sure you have root permission, script need root permission and do some system
# change...
# Please dont use this script on a running important server, although it will not delete any data
# but I dont suggest you use it..
#
# USAGE:
# very simple! just use "sh deploy_ubuntu_12.04.sh" or "./deploy_ubuntu_12.04.sh" YEAH!!
#
###################################################################################################
 "

while read -p "Please type yes if you will go ahead[yes|no]:  " ANSWER
do
  if [ -z $ANSWER ];then
  continue
  fi

  case $ANSWER in
  yes|YES|y)
	check_root
#	check_OS_version
	check_openlinux
	install_software
	Install_tools
	install_java
#	install_x_desktop

##	Check software take too much time, so by default, I will not run it, if you like, please uncommont it
	#check_software

	exit_script
   ;;
  no|NO|n)
     echo "I will quit...Thank you!!"
      break;;
  *)
      continue
      ;;
  esac

done
