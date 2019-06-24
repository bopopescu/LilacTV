# -*- coding: utf-8 -*-
import os
import time
import xbmc
import FileUtil

if __name__=='__main__':

    if os.path.exists("/storage/.kodi/userdata/addon_data/service.libreelec.settings/oe_settings.xml"):
        FileUtil.UpdateCheck4Favourites("예능")
        FileUtil.UpdateCheck4Favourites("YouTube")
        FileUtil.UpdateCheck4YouTubeLive()
        FileUtil.UpdateCheck4LilacTV()

        os.system("/storage/.config/./vpnbook.sh")
        time.sleep(1)      

        xbmc.executebuiltin('ReloadSkin()')


