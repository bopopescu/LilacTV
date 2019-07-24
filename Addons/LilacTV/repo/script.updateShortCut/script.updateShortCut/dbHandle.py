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

sys.path.append('/storage/.kodi/addons/script.module.myconnpy/lib/')
import mysql.connector
import xml.etree.ElementTree as ET

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

def main(config):
    # output = []
    db = mysql.connector.Connect(**config)
    cursor = db.cursor()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    ip = check_in()
    eth0 = getHwAddr('eth0')
    wlan = getHwAddr('wlan0')

    device = ((eth0, wlan, ip))
    stmt_insert = """
        INSERT INTO items (macaddeth0, macaddwlan, ipadd, online)
        VALUES (%s,%s,%s,1)
        ON DUPLICATE KEY UPDATE
        ipadd = VALUES(ipadd), online = VALUES(online)
    """
    cursor.execute(stmt_insert, device)
    db.commit()

    Path = "/storage/.kodi/userdata/addon_data/pvr.hts/settings.xml"
    if not os.path.exists(Path):
        os.system("cp -r /storage/.kodi/addons/script.updateShortCut/pvr.hts /storage/.kodi/userdata/addon_data")

    if os.path.exists(Path):
        stmt_select = "SELECT * FROM items WHERE macaddeth0 = %s"
        cursor.execute(stmt_select, (eth0))
        row = cursor.fetchone()
        cursor.close()
        db.close()
        ChangeData_XML(Path, "lilactv.com", str(row[6]), row[0])
        if (row[4] == True):
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
