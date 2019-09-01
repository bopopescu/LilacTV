#!/bin/sh

# Auto detecting a backup.tar.bz2 file when the firmware is installed
if [ -f "/flash/backup.tar.bz2" ] && [ ! -f "/storage/.BadJin.sm" ]; then
  mount -o remount,rw /flash
  if [ ! -d "/storage/packages" ]; then
    mkdir /storage/packages
  fi
  cp -PR /flash/backup.tar.bz2 /storage/backup.tar.bz2
  cp /flash/*.md5 /storage/packages/

  cd /storage
  tar xvf backup.tar.bz2
  rm -rf backup.tar.bz2
  rm -rf /flash/*.md5
  rm -rf /flash/backup.tar.bz2
  touch /storage/.BadJin.sm
  mount -o remount,ro /flash
  cp -r /storage/.kodi/cache/* /storage/.cache/

elif [ -f "/storage/.config/customsetting.py" ] && [ ! -f "/storage/.CustomSettingFlag" ]; then
  python /storage/.config/customsetting.py > /dev/null
  touch /storage/.CustomSettingFlag
fi

#crontab /etc/seebo/Seebo.cron
crontab /storage/Seebo.cron

# if [ -d "/storage/.kodi/addons/plugin.video.exodus" ]; then
#   if [ ! -d "/storage/.kodi/addons/plugin.video.exodus/resources/language/Korean" ]; then
#     cp -r /storage/.kodi/media/Custom/Korean /storage/.kodi/addons/plugin.video.exodus/resources/language
#   fi
# fi

python /storage/.config/CheckSkin.py > /dev/null

if [ -d "/storage/.kodi/addons/service.vpn.manager" ]; then
  /bin/sh -c "exec sh /storage/.config/vpnbook.sh &" > /dev/null
fi

cp /storage/.config/resolv.conf /run/connman/resolv.conf

curl http://172.104.51.248/BadJin/Favourites/System/playlist-lilactvHD.m3u > /storage/.kodi/media/tv/iptv/playlist-lilactvHD.m3u
curl http://172.104.51.248/BadJin/Favourites/System/playlist-lilactvHD1.m3u > /storage/.kodi/media/tv/iptv/playlist-lilactvHD1.m3u
curl http://172.104.51.248/BadJin/Favourites/System/playlist-lilactvHD2.m3u > /storage/.kodi/media/tv/iptv/playlist-lilactvHD2.m3u
curl http://172.104.51.248/BadJin/Favourites/System/playlist-lilactvHD3.m3u > /storage/.kodi/media/tv/iptv/playlist-lilactvHD3.m3u
curl http://172.104.51.248/BadJin/Favourites/System/playlist-lilactvHD4.m3u > /storage/.kodi/media/tv/iptv/playlist-lilactvHD4.m3u

# Adding to see whether the apply backup should be executed before kodi starts
if [ -f "/storage/.seeboBackup/applyBackup" ]; then
  # "Installing kodi theme..."
  cp -rf /storage/target/.kodi  /storage/
  # "Removing temporary data..."
  rm -rf /storage/target
  rm -rf  /storage/.seeboBackup
fi

#Cleared UpdateOngoing flag...
if [ -f "/storage/.kodi/temp/UpdateOngoing" ]; then
  rm /storage/.kodi/temp/UpdateOngoing
fi

if [ -f "/storage/.NeedUpdate.ch" ]; then
  rm /storage/.NeedUpdate.ch
fi

if [ -f "/storage/.NeedReboot.ch" ]; then
  rm /storage/.NeedReboot.ch
fi

if [ ! -d "/storage/subtitles" ]; then
  mkdir /storage/subtitles
fi

#Update Check
#if [ -d "/storage/.kodi/userdata/addon_data/service.libreelec.settings" ]; then
#        /bin/sh -c "exec sh /etc/seebo/CheckUpdateInBoot.sh &" > /dev/null
#fi
