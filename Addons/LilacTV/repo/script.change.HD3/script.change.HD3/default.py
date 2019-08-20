# -*- coding: utf-8 -*-
import sys
import os
import time
import xbmc
import xbmcgui
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re

sys.path.append('/storage/.kodi/addons/script.updateShortCut/')
import FileUtil

__m3uPath__ = '/storage/.kodi/media/tv/iptv/'
__m3uFile__ = 'playlist-tvheadend'
# __m3uFile__ = 'playlist-lilactvHD'

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


def restartPVR():
    dis_or_enable_addon("pvr.hts", "true")
    time.sleep(2)
    dis_or_enable_addon("pvr.hts", "false")


def GetFileName(no):
    return __m3uFile__+str(no)+".m3u"

def GetPath(no):
    return os.path.join(__m3uPath__,__m3uFile__)+str(no)+".m3u"


def GetCurrentListNo():
    xml_file = '/storage/.kodi/userdata/addon_data/pvr.iptvsimple/settings.xml'
    doc = ET.parse(xml_file)
    root = doc.getroot()

    for e in root:
        if e.attrib.get('id') == "m3uPath":
            path = e.attrib.get('value')
            break

    no = int(re.findall("\d+",path)[0]) - 1
    return no

def isSameList(no):
    xml_file = '/storage/.kodi/userdata/addon_data/pvr.iptvsimple/settings.xml'
    if not (os.path.exists(xml_file)):
        return True

    doc = ET.parse(xml_file)
    root = doc.getroot()

    for e in root:
        if e.attrib.get('id') == "m3uPath":
            if not e.attrib.get('value') == GetPath(no):
                return False

    return True


def RemoveBlankLine(fName):
    clean_lines = []
    with open(fName, "r") as f:
        lines = f.readlines()
        clean_lines = [l.strip() for l in lines if l.strip()]

    with open(fName, "w") as f:
        f.writelines('\n'.join(clean_lines))


def set_settingsxml(no):
    settings_file = '/storage/.kodi/userdata/addon_data/pvr.iptvsimple/settings.xml'

    config_file = open(settings_file, 'r')
    config_text = config_file.read()
    config_file.close()

    xml_conf = minidom.parseString(config_text)

    for xml_entry in xml_conf.getElementsByTagName('setting'):
        for attr_name, attr_value in xml_entry.attributes.items():
            if attr_name == 'id' and attr_value == 'm3uPath':
                xml_entry.setAttribute("value", GetPath(no))

    config_file = open(settings_file, 'w')
    config_file.write(xml_conf.toprettyxml())
    config_file.close()
    RemoveBlankLine(settings_file)


def ChangeList(no):
    dialog = xbmcgui.Dialog()
    if isSameList(no):
        if FileUtil.UpdateCheck4TVChannels(GetFileName(no)):
            if dialog.ok("TV채널 업데이트", " ", "채널의 정보가 업데이트 되었습니다."):
                xbmc.executebuiltin('ActivateWindow(TVChannels)')
                time.sleep(1)
                xbmc.executebuiltin("PlayerControl(Stop)")
                time.sleep(1)
                restartPVR()

    else:
        os.system("curl http://lilactv.com/BadJin/Favourites/System/"+GetFileName(no)+" > "+GetPath(no))
        set_settingsxml(no)
        if dialog.ok("TV채널 업데이트 -[Test Version]","고화질[1080p]로 리스트를 구성합니다. -56채널", " ", "***각 채널의 동작을 보장하지 않습니다.***"):
            xbmc.executebuiltin('ActivateWindow(TVChannels)')
            time.sleep(1)
            xbmc.executebuiltin("PlayerControl(Stop)")
            time.sleep(1)
            restartPVR()

if __name__=='__main__':

    if os.path.exists("/storage/.kodi/userdata/addon_data/service.libreelec.settings/oe_settings.xml"):
        #return to homescreen
        xbmc.executebuiltin('ActivateWindow(home)')
        #sleep long enough for the home screen to come up
        time.sleep(1)

        dialog = xbmcgui.Dialog()
        List = []
        for n in range(1,11):
            List.append("Channel List %s" %str(n))

        selectedList = dialog.select("리스트를 선택하세요", List, preselect = GetCurrentListNo())
        ChangeList(selectedList+1)
