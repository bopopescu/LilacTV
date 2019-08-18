# -*- coding: utf-8 -*-
import sys
import os
import time
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xbmc
import xbmcgui

import iptv
import FileUtil
import dbHandle

import xbmcaddon

__cwd__ = '/storage/.kodi/addons/script.updateShortCut'
__UpdateFlag__ = os.path.join( __cwd__, 'resources', "script.skinshortcuts" )
__lib__ = os.path.join( __cwd__, 'resources')
__AddonPath__ = '/storage/.kodi/addons'
__favouritepath__ = '/storage/.kodi/userdata/addon_data/plugin.program.super.favourites/Super Favourites'


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


def AddonEnable():
    fi=open(os.path.join(__UpdateFlag__, 'mainmenu.DATA.xml'))
    lines=fi.readlines()
    fi.close()

    for line in lines:
        if 'plugin://' in line:
            item=line.split('"')[1]
            addon=item.split('/')[2]
            dis_or_enable_addon(addon)


def AddNewRepo(repo):
    sPath=os.path.join(__lib__, repo)
    if os.path.exists(sPath):
        if not os.path.exists(os.path.join(__AddonPath__,repo)):
            os.system("cp -r "+sPath+" "+ __AddonPath__)
            time.sleep(0.5)
            #xbmc.executebuiltin('UpdateLocalAddons')
            #time.sleep(2)

        os.system("rm -rf "+sPath)
    dis_or_enable_addon(repo)


def AddNewAddon(repo, addon):
    Flag = False
    #Check addon
    AddonPath = os.path.join(__AddonPath__, addon)
    if not os.path.exists(AddonPath):
        #Add-ons
        AddNewRepo(repo)
        time.sleep(2)
        xbmc.executebuiltin('InstallAddon(%s)' % addon)
        Flag = True

    time.sleep(2)
    dis_or_enable_addon(addon)

    #Custom file
    UsrDataPath = os.path.join(__lib__, 'usr', addon)
    if os.path.exists(UsrDataPath):
        FileUtil.TargetFileUpdate('usr/'+addon, '/storage/.kodi/userdata/addon_data', isFolder = True)

    return Flag


def CheckValue_XML(xml_file,PTag,STag,value):
    if not (os.path.exists(xml_file)):
        return False

    doc = ET.parse(xml_file)
    root = doc.getroot()

    for e in root.iter(PTag):
        if e.findtext(STag) == value:
            return True

    return False


def CheckSkin():
    settings_file = '/storage/.kodi/userdata/guisettings.xml'
    #Change skin
    ParentTag = 'lookandfeel'
    SubTag = 'skin'

    if os.path.exists("/storage/.kodi/userdata/addon_data/service.libreelec.settings"):
        if not CheckValue_XML(settings_file, ParentTag, SubTag, 'skin.arctic.zephyr.plus'):
            dialog = xbmcgui.Dialog()
            yes = dialog.yesno("Skin Error", "LilacTV doesn't support this skin.", "You may need to re-install to go back LilacTV.","Do you want to re-install now?")
            if yes:
                xbmc.executebuiltin("RunScript(/etc/seebo/python_updater.py, Kor, true, true)")
                sys.exit()


def GetVPNCheck():
    fi=open("/storage/.config/vpnbook.sh")
    lines=fi.readlines()
    fi.close()

    for line in lines:
        if '#curl' in line:
            return True
        else:
            pass

    return False


def CheckUpdate():
    if os.path.exists("/storage/.config/CheckUpdate.sh"):
        os.system("/storage/.config/./CheckUpdate.sh")


def UpgradeDependency(addon_id, currentVersion):
    if os.path.exists(os.path.join(__lib__, addon_id)):
        if os.path.exists(os.path.join(__AddonPath__, addon_id)):
            version = xbmcaddon.Addon(addon_id).getAddonInfo('version')
            if not version == currentVersion:
                FileUtil.TargetFileUpdate(addon_id, __AddonPath__, isFolder = True)
        else:
            FileUtil.TargetFileUpdate(addon_id, __AddonPath__, isFolder = True)


def DBsetting():
    from config import Config
    UsrDataPath = os.path.join(__lib__, 'usr', "pvr.hts")
    Path = "/storage/.kodi/userdata/addon_data/pvr.hts/settings.xml"
    if os.path.exists(UsrDataPath):
        if not os.path.exists(Path):
            FileUtil.TargetFileUpdate('usr/pvr.hts', '/storage/.kodi/userdata/addon_data', isFolder = True)
    config = Config.dbinfo().copy()
    dbHandle.main(config)

if __name__=='__main__':

    if os.path.exists("/storage/.kodi/userdata/addon_data/service.libreelec.settings/oe_settings.xml"):

        if not os.path.exists(__UpdateFlag__):
            DBsetting()

        if os.path.exists("/storage/.kodi/patches"):
            os.system("python /storage/.kodi/patches/patch.py")
            os.system("rm -rf /storage/.kodi/patches")

        if not os.path.exists(__UpdateFlag__):
            if not os.path.exists("/storage/.NeedUpdate.ch"):
                CheckUpdate()

        Flag = False
        if FileUtil.UpdateCheck4Favourites("즐겨찾기"):
            Flag = True
        if FileUtil.UpdateCheck4Favourites("애드온"):
            Flag = True
        if FileUtil.UpdateCheck4Favourites("YouTube"):
            Flag = True
        if FileUtil.UpdateCheck4YouTubeLive():
            Flag = True
        if FileUtil.UpdateCheck4Drama():
            Flag = True
        if FileUtil.UpdateCheck4Movie():
            Flag = True

        if os.path.exists(__UpdateFlag__):

            if os.path.exists(os.path.join(__lib__, 'Seebo.cron')):
                FileUtil.TargetFileUpdate('autostart.sh', '/storage/.config', isFolder = False)
                FileUtil.TargetFileUpdate('resolv.conf', '/storage/.config', isFolder = False)
                FileUtil.TargetFileUpdate('Seebo.cron', '/storage', isFolder = False)
                FileUtil.TargetFileUpdate('vpnbook.sh', '/storage/.config', isFolder = False)
                FileUtil.TargetFileUpdate('playlist-lilactvSD.m3u', '/storage/.kodi/media/tv/iptv', isFolder = False)
                FileUtil.TargetFileUpdate('settings.xml', '/storage/.kodi/userdata/addon_data/pvr.iptvsimple', isFolder = False)
                time.sleep(0.2)
                os.system("chmod -R 777 /storage/.config/autostart.sh")
                os.system("chmod -R 777 /storage/.config/resolv.conf")
                os.system("chmod -R 777 /storage/.config/vpnbook.sh")
                os.system("chmod -R 777 /storage/reloadPVR.py")
                os.system("chmod -R 777 /storage/Seebo.cron")
                os.system("crontab /storage/Seebo.cron")
                os.system("/storage/.config/./vpnbook.sh")
                time.sleep(0.5)

                if not os.path.exists(os.path.join(__favouritepath__, '즐겨찾기')):
                    FileUtil.TargetFileUpdate("즐겨찾기", __favouritepath__, isFolder = True)

            #Remove not working addons
            if os.path.exists(os.path.join(__lib__, 'Addons27.db')):
                FileUtil.TargetFileUpdate('Addons27.db', '/storage/.kodi/userdata/Database', isFolder = False)
                FileUtil.TargetFileDelete("plugin.video.exodus", "/storage/.kodi/addons")
                FileUtil.TargetFileDelete("plugin.video.mc1080p", "/storage/.kodi/addons")
                FileUtil.TargetFileDelete("plugin.video.veetle", "/storage/.kodi/addons")
                FileUtil.TargetFileDelete("plugin.program.indigo", "/storage/.kodi/addons")
                FileUtil.TargetFileDelete("plugin.video.placenta", "/storage/.kodi/addons")

            if os.path.exists(os.path.join(__lib__, 'customsetting.py')):
                FileUtil.TargetFileUpdate('customsetting.py', '/storage/.config', isFolder = False)
                os.system("rm /storage/.CustomSettingFlag")

            if FileUtil.UpdateCheck4Skin():
                Flag = True

            os.system("rm -rf /storage/.kodi/addons/script.updateShortCut/resources/plugin.*")
            os.system("rm -rf /storage/.kodi/addons/script.updateShortCut/resources/service.*")

        else:
            CheckSkin()

        favPath = os.path.join(__favouritepath__, '즐겨찾기')
        if not os.path.exists(favPath):
            os.system("mkdir "+favPath)

        if Flag and not os.path.exists("/storage/.NeedUpdate.ch"):
            xbmc.executebuiltin('ReloadSkin()')

        AddNewAddon('repository.tempest', 'plugin.video.tempest')
        AddNewAddon('repository.supremacy', 'plugin.video.yoda')
        AddNewAddon('repository.lilac', 'plugin.video.kayo.sports')
        AddNewAddon('repository.matthuisman', 'plugin.video.au.freeview')
        AddNewRepo('repository.EzzerMacsWizard')
        #api update to devs one as 5
        AddNewAddon('repository.lilac', 'plugin.video.youtube')


        dis_or_enable_addon("pvr.vdr.vnsi", "false")
