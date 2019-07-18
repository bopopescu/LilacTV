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

import sys, os
import urllib, re
import fcntl, socket, struct
from datetime import datetime
#sys.path.append('/storage/.kodi/addons/script.module.myconnpy/lib/')
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

def main(config):
    output = []
    db = mysql.connector.Connect(**config)
    cursor = db.cursor()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    # stmt_drop = "DROP TABLE IF EXISTS devices"
    # cursor.execute(stmt_drop)
    #
    # stmt_create = """
    # CREATE TABLE devices (
    #   id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    #   mac_add_eth0 VARCHAR(30) DEFAULT '' NOT NULL,
    #   mac_add_wlan VARCHAR(30) DEFAULT '' NOT NULL,
    #   ip_add VARCHAR(30) DEFAULT '' NOT NULL,
    #   registered VARCHAR(30) DEFAULT '' NOT NULL,
    #   active BOOLEAN,
    #   PRIMARY KEY (id)
    # )"""
    # cursor.execute(stmt_create)

    ip = check_in()
    eth0 = getHwAddr('enp0s25')
    wlan = getHwAddr('enp0s25')

    stmt_select = "SELECT mac_add_eth0 FROM devices WHERE mac_add_eth0 = %s"
    cursor.execute(stmt_select, (eth0,))
    row = cursor.fetchone()
    if not row:
        device = ((eth0, wlan, ip, formatted_date, 1, 0),)
        stmt_insert = "INSERT INTO devices (mac_add_eth0, mac_add_wlan, ip_add, registered, active, enable) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.executemany(stmt_insert, device)
        db.commit()
        output.append("Insert Data %s, %s, %s\n%s active %s" % (eth0, wlan, ip, formatted_date, 1))
    else:
        # stmt_update = "UPDATE devices SET ip_add = %s, active = %s WHERE mac_add_eth0 = %s"
        stmt_update = "UPDATE devices SET enable = %s WHERE id in (2,3)"
        cursor.execute(stmt_update, (1, ))
        db.commit()

    # Path = "/WorkDisk/LilacTV/Study/python/MySQL/mysql/pvr.hts/settings.xml"
    # if not os.path.exists(Path):
    #     os.system("cp -r pvr.hts /WorkDisk/LilacTV/Study/python/MySQL/mysql")
    #     print("asdasd")
    #
    # if os.path.exists(Path):
    #     stmt_select = "SELECT * FROM devices WHERE mac_add_eth0 = %s"
    #     cursor.execute(stmt_select, (eth0,))
    #     row = cursor.fetchone()
    #     ChangeData_XML(Path, "lilactv.com", str(row[0]), row[1])
    #     userid = row[1].replace(':','')+str("%02x" % row[0])
    #     output.append("UserID is %s" % userid)

    # stmt_update = "UPDATE devices SET active = REPLACE( active, 1, 0 )"
    # cursor.execute(stmt_update)
    # db.commit()

    cursor.close()
    db.close()
    return output


if __name__ == '__main__':
    #
    # Configure MySQL login and database to use in config.py
    #
    from config import Config
    config = Config.dbinfo().copy()
    out = main(config)
    print('\n'.join(out))
