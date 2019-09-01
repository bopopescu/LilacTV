# -*- coding: utf-8 -*-
import sys
import os
import re
import urllib
import time
import hashlib

import dbHandle
#import xbmcgui

__cwd__ = '/storage/.kodi/addons/script.updateShortCut'
__userpath__ = '/storage/.kodi/userdata/addon_data'
__favouritepath__ = '/storage/.kodi/userdata/addon_data/plugin.program.super.favourites/Super Favourites'
__resources__ = '/storage/.kodi/addons/script.updateShortCut/resources'
ServerURL='http://lilactv.com/BadJin/'
temp='/storage/.kodi/addons/script.updateShortCut/resources/favourites.xml'

__iptv__ = '/storage/.kodi/media/tv/iptv'
__serveriptv__ = '/storage/.kodi/temp'

'''
def DebugDialog(str1,str2):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok("Debug Window",str1,str2)
'''

def DebugFile(text):
    fo=open("/storage/DebubyBJ.txt","a+")
    fo.write(text+'\n')
    fo.close()

def CpSource(source, target):
    s1 = source
    t1 = target
    if ' ' in source:
        s1=re.subn(' ','\ ',source)[0]
    if ' ' in target:
        t1=re.subn(' ','\ ',target)[0]

    os.system("cp "+s1+" "+t1)

def RmSource(source):
    s1 = source
    if ' ' in source:
        s1=re.subn(' ','\ ',source)[0]

    os.system("rm -rf "+s1)

#------------------------------------------------------------------------------

class FileCheck:
    status = False
    md5 = 'BadJin'
    source = 'BadJin'

    def md5sum(self, sPath, blocksize=65536):
        hash = hashlib.md5()
        with open(sPath, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
        return hash.hexdigest()

    def Remove(self):
        if os.path.exists(self.source):
            RmSource(self.source)

    def Update(self, other):
        if self.status:
            if os.path.exists(other.source):
                RmSource(other.source)
            CpSource(self.source, other.source)

    def IsDifferent(self, other):
        if not self.md5 == other.md5:
            return True
        else:
            return False

    def __init__(self, sPath):
        self.source = sPath
        if os.path.exists(self.source):
            if os.path.isfile(self.source) and os.path.getsize(self.source) > 0:
                self.status = True
                self.md5 = self.md5sum(self.source)


class CheckFavourite():
    def __init__(self, Category, IsSystem=False):
        self.Category = Category
        self.ReloadSkin = False
        temp='/storage/.kodi/addons/script.updateShortCut/'+Category+'.xml'
        if IsSystem:
            self.Current = FileCheck(os.path.join(__favouritepath__,"System",Category,"favourites.xml"))
            if Category == "최신드라마":
                WeekDay=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
                DAYofWEEK = time.localtime().tm_wday
                Path = WeekDay[DAYofWEEK]
            else:
                Path = Category
            url=ServerURL+"/Favourites/System/"+Path+"/favourites.xml"
        else:
            self.Current = FileCheck(os.path.join(__favouritepath__, Category, "favourites.xml"))
            url=ServerURL+"/Favourites/"+Category+"/favourites.xml"

        #if os.path.exists(temp):
        #  os.system("rm "+temp)

        try:
            a,b=urllib.urlretrieve(url, temp)
            time.sleep(1)
            if b.getheader('Content-length'):
                self.New = FileCheck(temp)

        except:
            a,b=urllib.urlretrieve(url, temp)
            time.sleep(1)
            if b.getheader('Content-length'):
                self.New = FileCheck(temp)


    def GetItemList(self):
        self.lists = []
        temp='/storage/.kodi/addons/script.updateShortCut/'+self.Category+'.list'
        url=ServerURL+'/Favourites/'+self.Category+'.list'

        #if os.path.exists(temp):
        #  os.system("rm "+temp)

        try:
            a,b=urllib.urlretrieve(url, temp)
            time.sleep(1)

        except:
            a,b=urllib.urlretrieve(url, temp)
            time.sleep(1)

        if b.getheader('Content-length'):
            fi=open(temp)
            lines=fi.readlines()
            fi.close()
            for line in lines:
                if "name=" in line:
                    item=line.split("thumb=")
                    code=item[0].split("=")
                    self.lists.append(code[1])


    def Update(self):
        if self.New.status and self.Current.IsDifferent(self.New):
            CpSource(self.New.source, self.Current.source)
            return True
        else:
            return False


    def Replace(self, srcStr, desStr):
        fi=open(self.Current.source)
        text=fi.read()
        text=re.subn(srcStr,desStr,text)[0]
        fi.close()

        fo=open(self.Current.source,"w")
        fo.write(text)
        fo.close()


    def IsItemIn(self, source, item):
        fi=open(source)
        lines=fi.readlines()
        fi.close()

        for line in lines:
            if item in line:
                return True

        return False


    def GetCODE(self, source, Channel):
        fi=open(source)
        lines=fi.readlines()
        fi.close()

        code="BadJin"
        for line in lines:
            if Channel in line:
                if "&amp" in line:
                    item=line.split("&amp")
                    code=item[0].split("=")
                    return code[3]

        return code


    def Add(self, Channel):
        fi=open(self.New.source)
        lines=fi.readlines()
        TargetItem = "BadJin"
        for line in lines:
            if Channel in line:
                TargetItem = line
                break
        fi.close()

        if not TargetItem == "BadJin":
            Flag = False
            fi=open(self.Current.source)
            Targetlines=fi.readlines()
            for line in Targetlines:
                if Channel in line:
                    Flag = True
                    break
            fi.close()

            if not Flag:
                fo=open(self.Current.source,"w")
                i = 0
                for line in Targetlines:
                    if i == 1:
                        fo.write(TargetItem)
                    fo.write(line)
                    i = i + 1
                fo.close()
                self.ReloadSkin = True


    def Remove(self, Channel):
        Flag = False
        if self.Current.status:
            fi=open(self.Current.source)
            lines=fi.readlines()
            for line in lines:
                if Channel in line:
                    Flag = True
                    break
            fi.close()

            if Flag:
                fo=open(self.Current.source,"w")
                for line in lines:
                    if not Channel in line:
                        fo.write(line)
                fo.close()
                self.ReloadSkin = True
        else:
            CpSource(self.New.source, self.Current.source)
            self.ReloadSkin = True


    def UpdateCodes(self, Channel):
        oldCode = self.GetCODE(self.Current.source, Channel)
        newCode = self.GetCODE(self.New.source, Channel)

        if not oldCode == "BadJin":
            if not newCode == "BadJin":
                if not oldCode == newCode:
                    self.Replace(oldCode, newCode)
                    self.ReloadSkin = True
            else:
                self.Remove(Channel)
        else:
            self.Add(Channel)


    def UpdateItem(self, Item):
        if not self.Current.status:
            self.Current = FileCheck(self.Current.source)
        if not self.New.status:
            self.Current = FileCheck(self.New.source)

        if self.IsItemIn(self.Current.source, Item):
            if not self.IsItemIn(self.New.source, Item):
                self.Remove(Item)
        else:
            self.Add(Item)

#------------------------------------------------------------------------------

def TargetFileUpdate(source, tPath, isFolder = False):
    if isFolder:
        sFolder = os.path.join(__resources__, source)
        tFolder = os.path.join(tPath, source)

        #if os.path.exists(tFolder):
            #RmSource(tFolder)

        if ' ' in tPath:
            t1=re.subn(' ','\ ',tPath)[0]
            time.sleep(0.5)
            os.system("cp -r "+sFolder+" "+t1)

        else:
            os.system("cp -r "+sFolder+" "+tPath)
            os.system("rm -rf "+sFolder)
        # RmSource(sFolder)

    else:
        sFile = FileCheck(os.path.join(__resources__, source))
        tFile = FileCheck(os.path.join(tPath, source))
        sFile.Update(tFile)
        sFile.Remove()


def TargetFileDelete(source, tPath):
    sFile = FileCheck(os.path.join(tPath, source))
    sFile.Remove()


def DellItem(Category, Item):
    Favourite = CheckFavourite(Category)
    Favourite.Remove(Item)
    return Favourite.ReloadSkin


def AddItem(Category, Item):
    Favourite = CheckFavourite(Category)
    Favourite.Add(Item)
    return Favourite.ReloadSkin


def UpdateCheck4Drama():
    Drama = CheckFavourite("최신드라마", IsSystem=True)
    return Drama.Update()

def UpdateCheck4Movie():
    Movie = CheckFavourite("LilacTV", IsSystem=True)
    return Movie.Update()


def UpdateCheck4YouTubeLive():
    YouTube = CheckFavourite("YouTube")
    if YouTube.Current.status:
        YouTube.GetItemList()
        for channel in YouTube.lists:
            YouTube.UpdateCodes(channel)
    else:
        CpSource(YouTube.New.source, YouTube.Current.source)
        return True

    return YouTube.ReloadSkin


def UpdateCheck4Favourites(Category):
    Favourite = CheckFavourite(Category)
    if Favourite.Current.status:
        Favourite.GetItemList()
        for item in Favourite.lists:
            Favourite.UpdateItem(item)
    else:
        CpSource(Favourite.New.source, Favourite.Current.source)
        return True

    return Favourite.ReloadSkin


def UpdateCheck4Skin():
    Flag = False
    sFile = FileCheck(os.path.join(__resources__, "script.skinshortcuts", "skin.arctic.zephyr.plus.hash"))
    tFile = FileCheck(os.path.join(__userpath__, "script.skinshortcuts", "skin.arctic.zephyr.plus.hash"))

    if sFile.IsDifferent(tFile):
        #if tFile.status:
        #    RmSource(os.path.join(__userpath__, "script.skinshortcuts"))
        os.system("cp -r "+os.path.join(__resources__, "script.skinshortcuts")+" "+__userpath__)
        Flag = True
    else:
        os.system("rm -rf "+__resources__+"/script.skinshortcuts")

    return Flag

def UpdateCheck4TVChannels(m3uFile):
    Flag = False
    tFile = FileCheck(os.path.join(__iptv__, m3uFile))
    if tFile.status:
        path = os.path.join(__serveriptv__, m3uFile)
        url = ServerURL+"/Favourites/System/" + m3uFile
        a,b=urllib.urlretrieve(url, path)
        time.sleep(1)
        if b.getheader('Content-length'):
            sFile = FileCheck(path)
            if sFile.IsDifferent(tFile):
               os.system("cp -r "+sFile.source+" "+tFile.source)
               Flag = True

    return Flag

def DBsetting():
    from config import Config
    UsrDataPath = os.path.join(__resources__, 'usr', "pvr.hts")
    Path = "/storage/.kodi/userdata/addon_data/pvr.hts/settings.xml"
    if os.path.exists(UsrDataPath):
        if not os.path.exists(Path):
            TargetFileUpdate('usr/pvr.hts', '/storage/.kodi/userdata/addon_data', isFolder = True)
    config = Config.dbinfo().copy()
    dbHandle.main(config)
    if os.path.exists(os.path.join(__cwd__, 'config.py')):
        os.system("rm "+__cwd__+"/config.py")
    # if os.path.exists(os.path.join(__cwd__, 'dbHandle.py')):
    #     os.system("rm "+__cwd__+"/dbHandle.py")
