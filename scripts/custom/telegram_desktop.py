#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# telegram_desktop.py telegram indicator icons custom install script
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
iconDir = os.getcwd() + "/scripts/icons/telegram_desktop/"
destDir = home + "/.TelegramDesktop/tdata/ticons/"

def installCustomIndicatorIcons():
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    else:
        try:
            shutil.rmtree(destDir)
        except:
            return False
        os.makedirs(destDir)

    if installMethod == "copy":
        try:
            for icon in os.listdir(iconDir):
                shutil.copy(iconDir + icon, destDir + icon)
            symlink(destDir + "ico_22_0.png", destDir + "icomute_22_0.png")
            for i in range(2, 100):
                symlink(destDir + "ico_22_1.png", destDir + "ico_22_" + str(i) + ".png")
                symlink(destDir + "ico_22_1.png", destDir + "icomute_22_" + str(i) + ".png")
        except:
            return False
    elif installMethod == "link":
        try:
            for icon in os.listdir(iconDir):
                symlink(iconDir + icon, destDir + icon)
            symlink(destDir + "ico_22_0.png", destDir + "icomute_22_0.png")
            for i in range(2, 100):
                symlink(iconDir + "ico_22_1.png", destDir + "ico_22_" + str(i) + ".png")
                symlink(iconDir + "ico_22_1.png", destDir + "icomute_22_" + str(i) + ".png")
        except:
            return False
    else:
        print "Invalid operation!"

def removeCustomIndicatorIcons():
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir)
        except:
            return False


if sys.argv[1] == "--install":
    installCustomIndicatorIcons()
elif sys.argv[1] == "--remove":
    removeCustomIndicatorIcons()
