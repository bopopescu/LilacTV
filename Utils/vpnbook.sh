#!/bin/sh

FreeVPN=freevpn.txt
OpenVPN=bjfree.ovpn

curl https://www.freeopenvpn.org/en/cf/usa.php > $FreeVPN

temp=`cat $FreeVPN | sed -n '/pservers/p' | awk -F"\"" '{print $4}'`
ovpnFile=`echo $temp | awk -F" " '{print $2}'`
#echo $ovpnFile

curl $ovpnFile --output $OpenVPN
