# -*- coding: utf-8 -*-
import os
import time
import xbmc
import FileUtil

if __name__=='__main__':

    if os.path.exists("/storage/.kodi/userdata/addon_data/service.libreelec.settings/oe_settings.xml"):
        Flag = False
        if FileUtil.UpdateCheck4YouTubeLive():
            Flag = True
        if FileUtil.UpdateCheck4Drama():
            Flag = True
        if FileUtil.UpdateCheck4Movie():
            Flag = True

        if Flag:
            xbmc.executebuiltin('ReloadSkin()')
