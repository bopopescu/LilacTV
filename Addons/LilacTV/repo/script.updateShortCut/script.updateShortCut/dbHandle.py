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
    if not row:
        dialog = xbmcgui.Dialog()
        dialog.ok("WARNING","등록되지 않은 제품입니다.", " ", "lilactv.com에 문의하여 주세요.")
        os.system("killall kodi.bin")
    else:
        time.sleep(5)
        if (row[7] != 1): #owner_id가 admin이면
            dialog = xbmcgui.Dialog()
            message1 = """

            라일락TV 소프트웨어의 무단사용 및 제공되는 콘텐츠의 트래픽 과부화의 방지를 위하여
            2019년 10월 1일부터 라일락TV는 연간 회원제로 운영됩니다. 따라서 모든 라일락TV 장치의
            Activation(활성화)이 필요합니다.

            활성화된 라일락TV는 그 시점부터 1년간 사용이 가능하며 이후 1년 단위로 연장이 가능합니다.
            구독기간 연장시 AUD$50의 비용이 발생하게 됩니다.
            단, 기존 사용자분들은 2019년 9월 30일까지 장치를 활성화 시킬 경우 10년을 구독기간으로
            설정합니다. 10월 1일 이후에 활성화 할 경우 구독기간이 1년으로 설정되니 꼭 9월 내에
            장치의 활성화를 완료해 주십시요.

            [lilactv.com] -라일락TV 공식웹사이트- 에서 회원가입후 [개인정보]메뉴를 통해 장치
            활성화를 진행하실 수 있습니다. 활성화 진행시 제품의 ID가 필요하며 해당 ID는 라일락TV의
            [설정]의 서브메뉴(왼쪽방향키)의 [제품정보]란에서 확인하실 수 있습니다.

            자세한 사항은 [lilactv.com]의 사용자 가이드 항목에서 관련동영상을 참고하십시요.
            """

            message2 = """
            1. Activation
            라일락TV 소프트웨어의 무단사용 및 제공되는 콘텐츠의 트래픽 과부화의 방지를 위하여
            라일락TV는 연간 회원제로 운영됩니다. 라일락TV 장치의 사용은 Activation(활성화)을
            한 후 가능합니다.

            활성화된 라일락TV는 그 시점부터 1년간 사용이 가능하며 이후 1년 단위로 연장이 가능합니다.
            구독기간 연장시 AUD$50의 비용이 발생하게 됩니다.

            [lilactv.com] -라일락TV 공식웹사이트- 에서 회원가입후 [개인정보]메뉴를 통해 장치
            활성화를 진행하실 수 있습니다. 활성화 진행시 제품의 ID가 필요하며 해당 ID는 라일락TV의
            [설정]의 서브메뉴(왼쪽방향키)의 [제품정보]란에서 확인하실 수 있습니다.

            자세한 사항은 [lilactv.com]의 사용자 가이드 항목에서 관련동영상을 참고하십시요.

            2. WARRANTY
                1) 신제품 교체
                제품 구매 시기가 1개월 이내인 제품 불량 시 필히 아답터 등 부속품 반납 시
                신제품으로 교환.

                2) 부속품 교체
                제품 구매 시기가 1년 이내인 부속품(아답터 / 리모컨) 불량시 해당제품 반납 시
                교환.

                *교환이 불가능한 경우 : 고객과실(외형파손, 분해등), 자연재해(낙뢰, 천둥번개등)
            """


            if (row[6] < 43): #평생무료 버전
                dialog.textviewer("==================== 라일락TV Avtivation 안내 ====================", message2)
            else:
                dialog.textviewer("======================= 라일락TV 안내 ======================", message1)

            dialog = xbmcgui.Dialog()
            if (dialog.ok("System Information", "", "시스템을 종료합니다.", "")):
                os.system("poweroff")

        else:
            stmt_select = "SELECT * FROM subscription WHERE lilac_tv_id = %s"
            cursor.execute(stmt_select, (row[6],))
            sub = cursor.fetchone()
            now = datetime.now()
            restDays = ((sub[2] - now).days)+1
            endDate = sub[2].strftime('%Y-%m-%d')
            if (sub[3] == 3): #subscription의 state가 "Expired"이면
                dialog = xbmcgui.Dialog()
                dialog.ok("사용기간 만료", "구독기간이 만료되어 사용을 중지합니다.", "구독연장은 lilactc.com에서 문의하세요.", "종료일시 : "+endDate)
                time.sleep(10)
                os.system("killall kodi.bin")
            elif (sub[3] == 2): #subscription의 state가 "Activated"이면
                if (restDays < 8): #만료일 7일 전부터 알림
                    dialog = xbmcgui.Dialog()
                    dialog.ok("사용기간이 곧 만료됩니다.", "만료일까지 "+str(restDays)+"일 남았습니다.", "", "종료일시 : "+endDate)
                    if (restDays <= 0): #만료일에 "Expired" 저장
                        cursor.executemany("UPDATE subscription SET status_id = %s WHERE lilac_tv_id = %s", ((3, row[6]),))

                makeAccount4PvrHts(str(row[6]), row[0], row[4])

        stmt_update = "UPDATE items SET ipadd = %s, online = %s WHERE macaddeth0 = %s"
        cursor.executemany(stmt_update, ((ip, 1, row[0]),))

    db.commit()
    cursor.close()
    db.close()
