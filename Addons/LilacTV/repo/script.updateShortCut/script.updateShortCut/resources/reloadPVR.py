# -*- coding: utf-8 -*-
import sys
import os
import time
import xbmc
import xml.etree.ElementTree as ET

sys.path.append('/storage/.kodi/addons/script.updateShortCut/')
import FileUtil

def CheckKoreanChannel():
    xml_file = '/storage/.kodi/userdata/addon_data/pvr.iptvsimple/settings.xml'
    if not (os.path.exists(xml_file)):
        return False

    doc = ET.parse(xml_file)
    root = doc.getroot()
    
    for e in root:
        if e.attrib.get('id') == "m3uPath":            
            path = e.attrib.get('value').split("/")
            return path[6]

    return False


if __name__=='__main__':

    m3u = CheckKoreanChannel()
    if FileUtil.UpdateCheck4TVChannels(m3u):
        #xbmc.executebuiltin( "XBMC.Notification(TV채널 업데이트,TV채널의 정보가 업데이트 되었습니다.,20000)" )
        pass

