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

sys.path.append('/storage/.kodi/addons/script.module.myconnpy/lib/')
import mysql.connector

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

    # Drop table if exists, and create it new
    # stmt_drop = "DROP TABLE IF EXISTS names"
    # cursor.execute(stmt_drop)

    # stmt_create = """
    # CREATE TABLE users (
    #     id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    #     name VARCHAR(30) DEFAULT '' NOT NULL,
    #     email VARCHAR(50),
    #     phone VARCHAR(20),
    #     memo TEXT,
    #     PRIMARY KEY (id)
    # )"""
    # cursor.execute(stmt_create)
    #
    # stmt_create = """
    # CREATE TABLE devices (
    #     id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    #     mac_add_eth0 VARCHAR(50) DEFAULT '' NOT NULL,
    #     mac_add_wlan VARCHAR(50) DEFAULT '' NOT NULL,
    #     ip_add VARCHAR(30),
    #     PRIMARY KEY (id)
    # )"""
    # cursor.execute(stmt_create)

    ip_add = check_in()
    mac_add_eth0 = getHwAddr('eth0')
    mac_add_wlan = getHwAddr('wlan0')

    stmt_select = "SELECT * FROM devices WHERE mac_add_eth0 = VALUES (%s)"
    output = cursor.executemany(stmt_select, mac_add_eth0)
    if not output:
        device = ((mac_add_eth0, mac_add_wlan, ip_add),)
        stmt_insert = "INSERT INTO devices (mac_add_eth0, mac_add_wlan, ip_add) VALUES (%s,%s,%s)"
        cursor.executemany(stmt_insert, device)
        db.commit()
    # else:
    #     stmt_select = "SELECT id, mac_add_eth0, mac_add_wlan, ip_add FROM devices ORDER BY id"
    #     cursor.execute(stmt_select)
    # # Read the names again and print them
    # stmt_select = "SELECT id, ip_add, mac_add_eth0, mac_add_wlan FROM user ORDER BY id"
    # cursor.execute(stmt_select)
    #
    # for row in cursor.fetchall():
    #     output.append(row)

    # Cleaning up, dropping the table again
    # cursor.execute(stmt_drop)

    cursor.close()
    db.close()
    #return output
