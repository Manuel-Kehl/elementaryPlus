#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# spotify.py spotify indicator icon custom install script
#
# Copyright (C) 2015  Stefan Ric (cybre)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
import sys
import os
from os import symlink
from os.path import expanduser
import shutil

icon = sys.argv[3] + "icons/spotify/icon.png"
home = expanduser("~")
destDir = home + "/.local/share/sni-qt/icons/spotify/"

def listfiles(folder):
    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            yield os.path.join(root, filename)

def installCustomIndicatorIcons(installMethod):
    for filename in listfiles('/tmp/'):
        if "/icons/hicolor/512x512/apps/" in filename:
            uuid = filename.split("/")
            uuid = uuid[-1].split("_")
            uuid = uuid[-1]

    print uuid

    if not os.path.exists(destDir):
        os.makedirs(destDir)
    else:
        try:
            shutil.rmtree(destDir)
        except:
            return False
        os.makedirs(destDir)

    if installMethod == "copy":
        copy = shutil.copy(icon, destDir + uuid)
        return copy
    elif installMethod == "link":
        link = symlink(icon, destDir + uuid)
        return link
    else:
        print "Invalid operation!"

def removeCustomIndicatorIcons():
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir)
        except:
            return False
    else:
        return True

if sys.argv[1] == "--install":
    installCustomIndicatorIcons(sys.argv[2])
elif sys.argv[1] == "--remove":
    removeCustomIndicatorIcons()