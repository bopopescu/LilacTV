import sys
import os
import re
import time
import xbmc
import xbmcgui
import xbmcaddon
import shutil
import json

IconPath = "/storage/.xbmc/media/tv/au/"
ADDON = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath( ADDON.getAddonInfo('path') )
__lib__ = os.path.join( __cwd__, 'resources')
USERPATH1 = os.path.join('/storage/.xbmc/addons')
USERPATH2 = os.path.join('/storage/.xbmc/userdata/addon_data')


def replace(fName, srcStr, desStr):
  fi=open(fName)
  text=fi.read()
  text=re.subn(srcStr,desStr,text)[0]
  fi.close()

  fo=open(fName,"w")
  fo.write(text)
  fo.close()

def updateICON(targetFile):
  RESOURCES = os.path.join(__lib__,targetFile)
  targetPath = os.path.join(IconPath,targetFile)
  if not (os.path.exists(targetPath)):
    shutil.copy(RESOURCES,IconPath)

def TargetFileUpdate(tFile,tPath):
  Flag = False;
  sPath=os.path.join(__lib__, tFile)
  if os.path.exists(sPath):
    if not os.path.exists(os.path.join(tPath,tFile)):
      #xbmc.executebuiltin("XBMC.InstallAddon(%s)" % tFile)
      os.system("cp -r "+sPath+" "+tPath)
      Flag = True

    os.system("rm -rf "+sPath)

  return Flag

def TargetFileUpdate2(tFile,tPath):
  Flag = False
  sPath=os.path.join(__lib__, tFile)
  if os.path.exists(sPath):  
    if not os.path.exists(os.path.join(tPath,tFile)):
      #xbmc.executebuiltin("XBMC.UpdateAddonRepos()")
      #time.sleep(2)
      #xbmc.executebuiltin("XBMC.InstallAddon(%s)" % tFile)
      os.system("cp -r "+sPath+" "+tPath)
      Flag = True
    
    os.system("rm -rf "+sPath)    

  return Flag

def TargetFileRemove(tFile,tPath):
  sPath=os.path.join(tPath,tFile)
  if os.path.exists(sPath):
    os.system("rm -rf "+sPath)


def dis_or_enable_addon(addon_id, enable="true"):    
    addon = '"%s"' % addon_id
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "true":
        return xbmc.log("### Skipped %s, reason = allready enabled" % addon_id)
    elif not xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "false":
        xbmc.log("### Skipped %s, reason = not installed" % addon_id)
        quit()
    else:
        do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}' % (addon, enable)
        query = xbmc.executeJSONRPC(do_json)
        response = json.loads(query)
        if enable == "true":
            xbmc.log("### Enabled %s, response = %s" % (addon_id, response))
        else:
            xbmc.log("### Disabled %s, response = %s" % (addon_id, response))            
    return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))


if __name__=='__main__':
  updateICON("SBS ONE HD.png")
  updateICON("SBS VICELAND HD.png")
  updateICON("ABC NEWS.png")
  updateICON("ABC COMEDY.png")
  updateICON("7food network.png")
  updateICON("10.png")
  updateICON("10 BOLD.png")
  updateICON("10 Peach.png")
  updateICON("10 HD.png")
  updateICON("Your Money.png")
  updateICON("SBS Food.png")

  #Check the ABCComedy/Kids channel
  srcPath="/storage/.xbmc/userdata/addon_data/service.multimedia.vdr-addon/config/channels.conf"
  if os.path.exists(srcPath):
    replace(srcPath,"ABCComedy/Kids","ABC COMEDY")

  #Add-ons
  RebootFlag = False
  sPath=os.path.join(USERPATH1,"plugin.video.afl-video")
  if os.path.exists(sPath):
    str1="AFL / NRL /Cricket / netball"
 
    dialog = xbmcgui.Dialog()    
    yes = dialog.yesno("Remove add-ons",str1,"These Add-ons will no longer be operating.","Please refer [http://aussieaddons.com]")
    if yes:
      TargetFileRemove("plugin.video.afl-video",USERPATH1)
      TargetFileRemove("plugin.video.cricketaustralia",USERPATH1)
      TargetFileRemove("plugin.video.netball-live",USERPATH1)
      TargetFileRemove("plugin.video.nrl-live",USERPATH1)
      time.sleep(1)
      RebootFlag = True

  sPath=os.path.join(USERPATH1,"plugin.video.covenant")
  if os.path.exists(sPath):
    str1="StreamHub / Survivor / Covenant"
 
    dialog = xbmcgui.Dialog()    
    yes = dialog.yesno("Remove add-ons",str1,"These Add-ons will no longer be operating.")
    if yes:
      TargetFileRemove("plugin.video.streamhub",USERPATH1)
      TargetFileRemove("plugin.video.survivor",USERPATH1)
      TargetFileRemove("plugin.video.covenant",USERPATH1)
      time.sleep(1)
      RebootFlag = True

  sPath=os.path.join(USERPATH1,"plugin.video.neptune")
  if os.path.exists(sPath):
    str1="Neptune Rising" 
    dialog = xbmcgui.Dialog()    
    yes = dialog.yesno("Remove add-ons",str1,"This Add-on will no longer be operating.")
    if yes:
      TargetFileRemove("plugin.video.neptune",USERPATH1)
      TargetFileRemove("script.neptune.artwork",USERPATH1)
      TargetFileRemove("script.neptune.metadata",USERPATH1)
      TargetFileRemove("plugin.video.foodnetwork",USERPATH1)
      TargetFileRemove("plugin.video.footballreplays",USERPATH1)
      time.sleep(1)
      RebootFlag = True

  if TargetFileUpdate2('plugin.video.themagicdragon',USERPATH1):
    TargetFileUpdate('plugin.video.yoda',USERPATH1)
    TargetFileUpdate('script.module.yoda',USERPATH1)
    TargetFileUpdate('script.realdebrid.mod',USERPATH1)
    TargetFileUpdate('script.yoda.artwork',USERPATH1)
    TargetFileUpdate('script.yoda.metadata',USERPATH1)
    TargetFileUpdate('plugin.video.tempest',USERPATH1)
    TargetFileUpdate('script.tempest.artwork',USERPATH1)
    TargetFileUpdate('script.tempest.metadata',USERPATH1)

    str1="[The Magic Dragon] [Yoda] [Tempest]"
    str4="The system will be restarted to enable these add-ons."
    dialog = xbmcgui.Dialog()
    dialog.ok("Update new add-ons for movies",str1,str4)
    time.sleep(1)
    RebootFlag = True

  else:
    str1 = "plugin.video.yoda"
    if TargetFileUpdate2(str1,USERPATH1):
      TargetFileUpdate('script.module.yoda',USERPATH1)
      TargetFileUpdate('script.realdebrid.mod',USERPATH1)
      TargetFileUpdate('script.yoda.artwork',USERPATH1)
      TargetFileUpdate('script.yoda.metadata',USERPATH1)

      str2="[Yoda]"
      str3="The system will be restarted to enable this add-on."
      dialog = xbmcgui.Dialog()
      dialog.ok("Update new add-on for movies TV shows",str2,str3)
      time.sleep(1)      
      RebootFlag = True

    str1 = "plugin.video.tempest"
    if TargetFileUpdate2(str1,USERPATH1):
      TargetFileUpdate('script.tempest.artwork',USERPATH1)
      TargetFileUpdate('script.tempest.metadata',USERPATH1)

      str2="[Tempest]"
      str3="The system will be restarted to enable this add-on."
      dialog = xbmcgui.Dialog()
      dialog.ok("Update new add-on for movies TV shows",str2,str3)
      time.sleep(1)      
      RebootFlag = True

  str1 = "plugin.video.kayo.sports"
  sPath=os.path.join(USERPATH1,str1)
  if not os.path.exists(sPath) and not os.path.exists("/storage/DontAskAgain"):    
    str2="This is an add-on that requires a paid subscription."
    str3="For more information, please visit https://kayosports.com.au"
    str4="Would you like to install it?"
    dialog = xbmcgui.Dialog()
    if dialog.yesno("[Kayo Sports] add-on is available now",str2,str3,str4):
      TargetFileUpdate(str1,USERPATH1)
      TargetFileUpdate('script.module.arrow',USERPATH1)      
      dialog = xbmcgui.Dialog()
      dialog.ok("Update new add-on for Spotrs","Kayo Sports","The system will be restarted to enable this add-on.")
      time.sleep(1)
      RebootFlag = True
    else:
      str2="You can install it at any time."
      str3="Through [On Demand] > [+] menu if you want."
      dialog.ok("[Kayo Sports] add-on is available now",str2,str3)
      os.system("touch /storage/DontAskAgain")

    TargetFileUpdate('inputstream.adaptive',USERPATH1)    

  if RebootFlag:
    os.system("reboot")

  dis_or_enable_addon("pvr.iptvsimple", "true")






