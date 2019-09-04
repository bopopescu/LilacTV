#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2009, 2013, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from __future__ import print_function

import sys, os, time
import urllib, re
import fcntl, socket, struct
from datetime import datetime
import xbmc, xbmcgui
import json
from datetime import datetime, timedelta
import sfile

sys.path.append('/storage/.kodi/addons/script.module.myconnpy/lib/')
import mysql.connector
import xml.etree.ElementTree as ET

__cwd__ = '/storage/.kodi/addons/script.updateShortCut'


def ChangeData_XML(xml_file, value1, value2, value3):
    doc = ET.parse(xml_file)
    root = doc.getroot()
    removeFlag = False

    for e in root.findall("setting"):
        if e.get("id") == "host":
            e.set("value", value1)
            removeFlag = True
        if e.get("id") == "user":
            e.set("value", "user"+value2)
            removeFlag = True
        if e.get("id") == "pass":
            e.set("value", value3)
            removeFlag = True

    if removeFlag:
        doc.write(xml_file, encoding="utf-8", xml_declaration=True)

def check_in():
    wan = re.search(re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),urllib.urlopen('http://checkip.dyndns.org').read()).group()
    return "%s"%wan

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    str = ':'.join(['%02x' % ord(char) for char in info[18:24]])
    return str

def IsPvrEnable(addon_id):
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id):
        return True
    else:
        return False

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

def makeAccount4PvrHts(id, mac, tvheadend):
# For the future
#===================================================================================================
    Path = "/storage/.kodi/userdata/addon_data/pvr.hts/settings.xml"
    if not os.path.exists(Path):
        os.system("cp -r /storage/.kodi/addons/script.updateShortCut/pvr.hts /storage/.kodi/userdata/addon_data")
        time(2)

    if os.path.exists(Path):
        ChangeData_XML(Path, "lilactv.com", id, mac)
        if (tvheadend == True):
            time.sleep(4)
            # xbmc.executebuiltin( "ActivateWindow(busydialog)" )
            dialog = xbmcgui.Dialog()
            if not IsPvrEnable("pvr.hts"):
                if IsPvrEnable("pvr.iptvsimple"):
                    dialog.ok("현재의 TV 서비스 끄기","1. [애드온] > [내 애드온] > [PVR 클라이언트]", "2. 첫번째 [PVR IPTV Simple Client] 선택", "3. [사용안함] 선택후 재시작 합니다.")

                elif dialog.ok("새로운 TV 서비스 시작","Tvheadend 클라이언트를 시작합니다."):
                    dis_or_enable_addon("pvr.hts", "true")
                    time.sleep(3)
            else:
                if IsPvrEnable("pvr.iptvsimple"):
                    dialog.ok("기존의 TV 서비스 끄기","1. [애드온] > [내 애드온] > [PVR 클라이언트]", "2. 첫번째 [PVR iptvsimple] 선택", "3. [사용안함] 선택후 재시작 합니다.")
            # xbmc.executebuiltin( "Dialog.Close(busydialog)" )


def setCrontab(enable = True):
    path = "/storage/Seebo.cron"
    cronCurrent = "*/30 * * * * kodi-send --action='RunScript(/storage/.kodi/addons/script.updateShortCut/dbHandle.py)'"

    fi=open(path)
    lines=fi.readlines()
    fi.close()

    newList = []
    for line in lines:
        if not cronCurrent in line:
            newList.append(line)

    if (enable):
        newList.append(cronCurrent)

    ofp = open("/storage/Seebo.cron", "w")
    for line in newList:
        ofp.write(line)
    ofp.close()

    os.system("crontab /storage/Seebo.cron")


def showText(heading, text, waitForClose=False):
    id = 10147

    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)

    win = xbmcgui.Window(id)

    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            retry = 0
        except:
            retry -= 1

    if waitForClose:
        while xbmc.getCondVisibility('Window.IsVisible(%d)' % id) == 1:
            xbmc.sleep(50)


def showMyMessage(num,id):

    title = "======================= 라일락TV  안내 ======================="
    path  = os.path.join(__cwd__, 'message%d.txt' % num)

    fp = open(path)
    text = fp.read()
    fp.close()
    lines = text.split('\n')

    newMessage = []
    count = 0
    for line in lines:
        newMessage.append(line)
        count += 1
        if "진행하실 수 있습니다" in line:
            newMessage.append("")
            newMessage.append("                                                                  "+id)
            count += 2

    ofp = open(__cwd__+"/message.txt", "w")
    for line in newMessage:
        ofp.write(line+'\n')
    ofp.close()

    path1  = os.path.join(__cwd__, 'message.txt')
    at  = sfile.read(path1)
    showText(title, at, True)


def main(config):
    if os.path.exists(os.path.join(__cwd__, 'FileUtil.py')):
        os.system("rm "+__cwd__+"/FileUtil.py")

    db = mysql.connector.Connect(**config)
    cursor = db.cursor()

    ip = check_in()
    eth0 = getHwAddr('eth0')
    wlan = getHwAddr('wlan0')

    stmt_select = "SELECT * FROM items WHERE macaddeth0 = %s"
    cursor.execute(stmt_select, (eth0,))
    row = cursor.fetchone()

    dialog = xbmcgui.Dialog()

    if not row:
        if (ip == "194.193.60.92"):
            device = ((eth0, wlan, ip, 1),)
            stmt_insert = "INSERT INTO items (macaddeth0, macaddwlan, ipadd, online) VALUES (%s,%s,%s,%s)"
            cursor.executemany(stmt_insert, device)
        else:
            time.sleep(5)
            if (dialog.ok("WARNING","등록되지 않은 제품입니다.", " ", "lilactv.com에 문의하여 주세요.")):
                os.system("poweroff")
            else:
                os.system("poweroff")
    else:
        time.sleep(10)
        if (row[7] == 1): #owner_id가 admin이면
            setCrontab()
            # userid = row[0].replace(':','')+str("%02x" % row[6]) #255까
            userid = row[0].replace(':','')+str("%04x" % row[6])
            if (row[6] < 50): #평생무료 버전
                showMyMessage(1, userid)
            else:
                showMyMessage(2, userid)

        else:
            setCrontab(False)
            stmt_select = "SELECT * FROM subscription WHERE lilac_tv_id = %s"
            cursor.execute(stmt_select, (row[6],))
            sub = cursor.fetchone()
            now = datetime.now()
            restDays = ((sub[2] - now).days)+1
            endDate = sub[2].strftime('%Y-%m-%d')
            if (sub[3] == 3): #subscription의 state가 "Expired"이면
                if (dialog.ok("사용기간 만료", "구독기간이 만료되어 사용을 중지합니다.", "구독연장은 lilactc.com에서 문의하세요.", "종료일시 : "+endDate)):
                    os.system("poweroff")
                else:
                    os.system("poweroff")
            elif (sub[3] == 2): #subscription의 state가 "Activated"이면
                if (restDays < 8): #만료일 7일 전부터 알림
                    dialog.ok("사용기간이 곧 만료됩니다.", "만료일까지 "+str(restDays)+"일 남았습니다.", "", "종료일시 : "+endDate)
                    if (restDays <= 0): #만료일에 "Expired" 저장
                        cursor.executemany("UPDATE subscription SET status_id = %s WHERE lilac_tv_id = %s", ((3, row[6]),))

                makeAccount4PvrHts(str(row[6]), row[0], row[4])

        stmt_update = "UPDATE items SET ipadd = %s, online = %s WHERE macaddeth0 = %s"
        cursor.executemany(stmt_update, ((ip, 1, row[0]),))

    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    #
    # Configure MySQL login and database to use in config.py
    #
    from config import Config
    config = Config.dbinfo().copy()
    main(config)
