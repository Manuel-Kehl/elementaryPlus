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

iconDir = sys.argv[3] + "icons/telegram_desktop/"
home = expanduser("~")
destDir = home + "/.local/share/TelegramDesktop/tdata/ticons/"


def installCustomIndicatorIcons(installMethod):
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    else:
        try:
            shutil.rmtree(destDir)
        except OSError:
            exit(1)
        os.makedirs(destDir)

    if installMethod == "copy":
        try:
            for icon in os.listdir(iconDir):
                shutil.copy(iconDir + icon, destDir + icon)
            symlink(destDir + "ico_22_0.png", destDir + "icomute_22_0.png")
            for i in range(2, 100):
                symlink(destDir + "ico_22_1.png", destDir + "ico_22_" + str(i) + ".png")
            for i in range(1, 100):
                symlink(destDir + "ico_22_1.png", destDir + "icomute_22_" + str(i) + ".png")
        except:
            exit(1)
    elif installMethod == "link":
        try:
            for icon in os.listdir(iconDir):
                symlink(iconDir + icon, destDir + icon)
            symlink(iconDir + "ico_22_0.png", destDir + "icomute_22_0.png")
            for i in range(2, 100):
                symlink(iconDir + "ico_22_1.png", destDir + "ico_22_" + str(i) + ".png")
            for i in range(1, 100):
                symlink(iconDir + "ico_22_1.png", destDir + "icomute_22_" + str(i) + ".png")
        except:
            exit(1)
    else:
        print "Invalid operation!"

    file = open(destDir + "elementaryPlus.installed", "w")
    file.close()


def removeCustomIndicatorIcons():
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir)
        except OSError:
            exit(1)


if sys.argv[1] == "--install":
    installCustomIndicatorIcons(sys.argv[2])
elif sys.argv[1] == "--remove":
    removeCustomIndicatorIcons()
