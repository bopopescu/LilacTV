# -*- coding: utf-8 -*-
import sys
import os
import re
import time
import xbmc
import xbmcgui
import xbmcaddon
import urllib2

__scriptid__ = 'plugin.program.xiptv'
__addon__ = xbmcaddon.Addon(id=__scriptid__)
__targetDIR__ = "/storage/.kodi/media/tv/iptv"


def get_settings_login_info():
  uid = __addon__.getSetting( 'id' )
  pwd = __addon__.getSetting( 'pwd' )
  return (uid, pwd)


def replace(fName, srcStr, desStr):
  fi=open(fName)
  text=fi.read()
  text=re.subn(srcStr,desStr,text)[0]
  fi.close()

  fo=open(fName,"w")
  fo.write(text)
  fo.close()


def GetCODE(iptvfile):  
  fi=open(iptvfile)
  lines=fi.readlines()
  fi.close()

  code="BadJin"  
  for line in lines:
    if "http://client-proiptv.com" in line:
      item=line.split("/")
      code=item[4]+'/'+item[5]
      break
  
  return code


def MakePlaylist(uid, pw):
  #url = 'http://iptvtop.ddns.net:25461/get.php?username='+uid+'&password='+pw+'&type=m3u_plus&output=ts'
  url = 'http://client-proiptv.com:8080/get.php?username='+uid+'&password='+pw+'&type=m3u_plus&output=ts'
  try:
    response = urllib2.urlopen(url)
    data = response.read()
    f = open(os.path.join(__targetDIR__, 'allchannels.m3u'), 'w') 
    f.write(data)
    f.close()
    return True

  except:   
   return False


def SetPlaylist(iptvpath):

  # login process
  (xiptv_id, xiptv_pw) = get_settings_login_info()  

  # check login
  if xiptv_id and xiptv_pw:
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    try:
      if MakePlaylist(xiptv_id, xiptv_pw):
        M3U = "playlist-xiptv.m3u"
        code = GetCODE(iptvpath)
        replace(iptvpath,code,xiptv_id+'/'+xiptv_pw)
   
      xbmc.executebuiltin('Dialog.Close(busydialog)')

    except:
      xbmc.executebuiltin('Dialog.Close(busydialog)')



