#!/bin/sh

FreeVPN=/storage/.config/freevpn.txt
OpenVPN=/storage/.config/bjfree.ovpn
#OpenVPN1=/storage/.config/bjfree1.ovpn

curl https://www.freeopenvpn.org/en/cf/usa.php > $FreeVPN

temp=`cat $FreeVPN | sed -n '/pservers/p' | awk -F"\"" '{print $4}'`
ovpnFile=`echo $temp | awk -F" " '{print $2}'`
#ovpnFile1=`echo $temp | awk -F" " '{print $4}'`
#echo $ovpnFile

curl $ovpnFile --output $OpenVPN
#curl $ovpnFile1 --output $OpenVPN1

newVPNpass=/storage/freevpn.txt
Passfile=/storage/.kodi/addons/service.vpn.manager/VPNBook.com-OpenVPN-CA1/pass.txt

OldPassword=`cat $Passfile | sed -n '2p'`
curl lilactv.com:8080/BadJin/Favourites/VPN.txt > $newVPNpass
. $newVPNpass
NewPassword=`echo $Password | awk -F" " '{print $1}'`
if [ -n "$NewPassword" ]; then
  if [ "$OldPassword" != "$NewPassword" ]; then
    sed -i "s|$OldPassword|$NewPassword|" $Passfile
  fi
fi
