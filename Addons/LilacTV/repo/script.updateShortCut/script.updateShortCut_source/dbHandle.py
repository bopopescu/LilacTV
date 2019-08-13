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

    # now = datetime.now()
    # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    ip = check_in()
    eth0 = getHwAddr('eth0')
    wlan = getHwAddr('wlan0')

    # device = ((eth0, wlan, ip))
    # stmt_insert = """
    #     INSERT INTO items (macaddeth0, macaddwlan, ipadd, online)
    #     VALUES (%s,%s,%s,1)
    #     ON DUPLICATE KEY UPDATE
    #     ipadd = VALUES(ipadd), online = VALUES(online)
    # """
    # cursor.execute(stmt_insert, device)
    # db.commit()

    stmt_select = "SELECT * FROM items WHERE macaddeth0 = %s"
    cursor.execute(stmt_select, (eth0,))
    row = cursor.fetchone()
    if not row:
        # device = ((eth0, wlan, ip, 1),)
        # stmt_insert = "INSERT INTO items (macaddeth0, macaddwlan, ipadd, online) VALUES (%s,%s,%s,%s)"
        # cursor.executemany(stmt_insert, device)
        dialog = xbmcgui.Dialog()
        dialog.ok("Error", "등록되지 않은 라일락TV 소프트웨어 입니다.")
        os.system("killall kodi.bin")
    else:
        if (row[7] == 1): #owner_id가 admin이면
            dialog = xbmcgui.Dialog()
            message = """

            라일락TV 소프트웨어의 무단사용 및 제공되는 콘텐츠의 트래픽 과부화의 방지를 위하여
            2019년 9월 2일부터 라일락TV는 연간 회원제로 운영됩니다. 따라서 모든 라일락TV 장치의
            Activation(활성화)가 필요합니다.

            활성화된 라일락TV는 그 시점부터 1년간 사용이 가능하며 이후 1년 단위로 연장이 가능합니다.
            연장시 AUD$50 의 구독료가 발생합니다. 이용에 참고하십시요.

            [lilactv.com] -라일락TV 공식웹사이트- 에서 회원가입후 [개인정보]메뉴를 통해 장치 활성화를
            진행하실 수 있습니다.
            활성화 진행시 제품의 ID가 필요하며 해당 ID는 라일락TV의 [설정]의 서브메뉴(왼쪽방향키)의
            [제품정보]란에서 확인하실 수 있습니다.

            자세한 사항은 [lilactv.com]의 사용자 가이드 항목에서 관련동영상을 참고하십시요.
            """
            dialog.textviewer("==================== 라일락TV Avtivation 안내 ====================", message)
            # os.system("killall kodi.bin")
        else:
            stmt_select = "SELECT * FROM subscription WHERE lilac_tv_id = %s"
            cursor.execute(stmt_select, (row[6],))
            sub = cursor.fetchone()
            now = datetime.now()
            restDays = (sub[2] - datetime.now()).days
            endDate = sub[2].strftime('%Y-%m-%d')
            if (sub[3] == 3): #subscription의 state가 "Expired"이면
                dialog = xbmcgui.Dialog()
                dialog.ok("사용기간 만료", "구독기간이 만료되어 사용을 중지합니다.", "구독연장은 lilactc.com에서 문의하세요.", "종료일시 : "+endDate)
                os.system("killall kodi.bin")
            elif (sub[3] == 2): #subscription의 state가 "Activated"이면
                if (restDays < 8): #만료일 7일 전부터 알림
                    dialog = xbmcgui.Dialog()
                    dialog.ok("사용기간이 곧 만료됩니다.", "만료일까지 "+str(restDays)+"일 남았습니다.", "종료일시 : "+endDate)
                    if (restDays == 0): #만료일에 "Expired" 저장
                        cursor.execute("UPDATE subscription SET status_id = %s WHERE lilac_tv_id = %s", (3,row[6],))


        stmt_update = "UPDATE items SET ipadd = %s, online = %s WHERE macaddeth0 = %s"
        cursor.executemany(stmt_update, ((ip, 1, row[0]),))

    db.commit()

    Path = "/storage/.kodi/userdata/addon_data/pvr.hts/settings.xml"
    if not os.path.exists(Path):
        os.system("cp -r /storage/.kodi/addons/script.updateShortCut/pvr.hts /storage/.kodi/userdata/addon_data")

    if os.path.exists(Path):
        stmt_select = "SELECT * FROM items WHERE macaddeth0 = %s"
        cursor.execute(stmt_select, (eth0,))
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
