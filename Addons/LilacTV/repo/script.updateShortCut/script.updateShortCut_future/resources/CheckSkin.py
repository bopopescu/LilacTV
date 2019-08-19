# -*- coding: utf-8 -*-
import sys
import os
import xml.etree.ElementTree as ET

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
            return True

    return False


__cwd__ = '/storage/.kodi/addons/script.updateShortCut'
__lib__ = os.path.join( __cwd__, 'resources')

if __name__ == '__main__':

    if CheckSkin():
        os.system("cp "+__lib__+"/Addons27.db /storage/.kodi/userdata/Database")
