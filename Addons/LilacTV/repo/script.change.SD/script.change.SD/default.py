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
import xbmc
import xbmcgui

sys.path.append('/storage/.kodi/addons/script.module.myconnpy/lib/')
import mysql.connector

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    str = ':'.join(['%02x' % ord(char) for char in info[18:24]])
    return str

def main(config):
    # output = []
    db = mysql.connector.Connect(**config)
    cursor = db.cursor()

    eth0 = getHwAddr('eth0')

    stmt_select = "SELECT * FROM devices WHERE mac_add_eth0 = %s"
    cursor.execute(stmt_select, (eth0,))
    row = cursor.fetchone()

    #return to homescreen
    xbmc.executebuiltin('ActivateWindow(home)')
    #sleep long enough for the home screen to come up
    time.sleep(1)
    dialog = xbmcgui.Dialog()
    if not row:
        dialog.ok("WARNING","등록되지 않은 제품입니다.", " ", "lilactv.com에 문의하여 주세요.")
    else:
        userid = row[1].replace(':','')+str("%02x" % row[0])
        dialog.ok("제품정보", "Version : Kor-1.0.6", "IP ADD : "+row[3], "ID : "+userid,)

    cursor.close()
    db.close()
    #return output

if __name__ == '__main__':
    #
    # Configure MySQL login and database to use in config.py
    #
    from config import Config
    config = Config.dbinfo().copy()
    main(config)
