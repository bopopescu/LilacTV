# -*- coding: utf-8 -*-
import sys
import os
import time
import xbmc
import xbmcgui
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET

sys.path.append('/storage/.kodi/addons/script.updateShortCut/')
import FileUtil

__m3uPath__ = '/storage/.kodi/media/tv/iptv/playlist-lilactvHD3.m3u'
__m3uFile__ = 'playlist-lilactvHD3.m3u'

def dis_or_enable_addon(addon_id, enable):
    addon = '"%s"' % addon_id
    do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}' % (addon, enable)
    query = xbmc.executeJSONRPC(do_json)
    response = json.loads(query)
    if enable == "true":
        xbmc.log("### Enabled %s, response = %s" % (addon_id, response))
    else:
        xbmc.log("### Disabled %s, response = %s" % (addon_id, response))
    return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))

def restartPVR():
    dis_or_enable_addon("pvr.vdr.vnsi", "true")
    time.sleep(2)
    dis_or_enable_addon("pvr.vdr.vnsi", "false")

def CheckKoreanChannel():
    xml_file = '/storage/.kodi/userdata/addon_data/pvr.iptvsimple/settings.xml'
    if not (os.path.exists(xml_file)):
        return False

    doc = ET.parse(xml_file)
    root = doc.getroot()

    for e in root:
        if e.attrib.get('id') == "m3uPath":
            if not e.attrib.get('value') == __m3uPath__:
                return True

    return False


def RemoveBlankLine(fName):
    clean_lines = []
    with open(fName, "r") as f:
        lines = f.readlines()
        clean_lines = [l.strip() for l in lines if l.strip()]

    with open(fName, "w") as f:
        f.writelines('\n'.join(clean_lines))


def set_settingsxml():
    settings_file = '/storage/.kodi/userdata/addon_data/pvr.iptvsimple/settings.xml'

    config_file = open(settings_file, 'r')
    config_text = config_file.read()
    config_file.close()

    xml_conf = minidom.parseString(config_text)


    for xml_entry in xml_conf.getElementsByTagName('setting'):
        for attr_name, attr_value in xml_entry.attributes.items():
            if attr_name == 'id' and attr_value == 'm3uPath':
                xml_entry.setAttribute("value", __m3uPath__)

    config_file = open(settings_file, 'w')
    config_file.write(xml_conf.toprettyxml())
    config_file.close()
    RemoveBlankLine(settings_file)


if __name__=='__main__':

    if os.path.exists("/storage/.kodi/userdata/addon_data/service.libreelec.settings/oe_settings.xml"):
        #return to homescreen
        xbmc.executebuiltin('ActivateWindow(home)')
        #sleep long enough for the home screen to come up
        time.sleep(1)
        if CheckKoreanChannel():
            os.system("curl http://lilactv.com/BadJin/Favourites/System/"+__m3uFile__+" > "+__m3uPath__)
            set_settingsxml()
            dialog = xbmcgui.Dialog()
            if dialog.ok("TV채널 업데이트 -[Test Version]","고화질[1080p]로 리스트를 구성합니다. -52채널", " ", "***예고없이 방송이 중단될 수 있습니다.***"):
                xbmc.executebuiltin('ActivateWindow(TVChannels)')
                time.sleep(1)
                xbmc.executebuiltin("PlayerControl(Stop)")
                time.sleep(1)
                restartPVR()

        else:
            if FileUtil.UpdateCheck4TVChannels(__m3uFile__):
                dialog = xbmcgui.Dialog()
                if dialog.ok("TV채널 업데이트", " ", "채널의 정보가 업데이트 되었습니다."):
                    xbmc.executebuiltin('ActivateWindow(TVChannels)')
                    time.sleep(1)
                    condition = xbmc.getCondVisibility('Player.HasMedia')
                    if condition:
                        xbmc.executebuiltin("PlayerControl(Stop)")
                        time.sleep(1)
                    restartPVR()
