#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# qtStandardInstall.py standard sni-qt indicator icon installer
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
from whatToUse import *

home = expanduser("~")

def installQtIndicatorIcons(appName):
    iconDir = os.getcwd() + "/scripts/icons/" + appName + "/"
    destDir = home + "/.local/share/sni-qt/icons/" + appName + "/"

    if installMethod == "copy":
        if os.path.exists(destDir):
            try:
                shutil.rmtree(destDir)
            except:
                return False
        copy = shutil.copytree(iconDir, destDir)
        return copy
    elif installMethod == "link":
        if not os.path.exists(destDir):
            os.makedirs(destDir)
        else:
            try:
                shutil.rmtree(destDir)
            except:
                return False
            os.makedirs(destDir)
        for icon in os.listdir(iconDir):
            link = symlink(iconDir + icon, destDir + icon)
        return link
    else:
        print "Invalid operation!"

def removeQtIndicatorIcons(appName):
    destDir = home + "/.local/share/sni-qt/icons/" + appName
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir)
        except:
            return False
    else:
        return True