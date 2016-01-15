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
import subprocess


iconDir = sys.argv[3] + "icons/teamviewer/"
home = expanduser("~")
destDir = home + "/.local/share/sni-qt/icons/teamviewer/"
destDir1 = home + "/.local/share/sni-qt/icons/TVGuiDelegate/"


def installCustomIndicatorIcons(installMethod):
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    else:
        try:
            shutil.rmtree(destDir)
        except OSError:
            exit(1)
        os.makedirs(destDir)

    if not os.path.exists(destDir1):
        os.makedirs(destDir1)
    else:
        try:
            shutil.rmtree(destDir1)
        except OSError:
            exit(1)
        os.makedirs(destDir1)

    if installMethod == "copy":
        try:
            for icon in os.listdir(iconDir):
                shutil.copy(iconDir + icon, destDir + icon)
                shutil.copy(iconDir + icon, destDir1 + icon)
        except:
            exit(1)
    elif installMethod == "link":
        try:
            for icon in os.listdir(iconDir):
                symlink(iconDir + icon, destDir + icon)
                symlink(iconDir + icon, destDir1 + icon)
        except:
            exit(1)
    else:
        print "Invalid operation!"

    if os.path.exists(home + "/.local/share/applications/teamviewer-teamviewer11.desktop"):
        shutil.copy(home + "/.local/share/applications/teamviewer-teamviewer11.desktop", home + "/.local/share/applications/teamviewer-teamviewer11.desktop.bak")
    shutil.copy(sys.argv[3] + "custom/teamviewer/teamviewer-teamviewer11.desktop", home + "/.local/share/applications/teamviewer-teamviewer11.desktop")

    subprocess.call(["pkexec", sys.argv[3] + "custom/teamviewer/teamviewer.sh"])


def removeCustomIndicatorIcons():
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir)
        except OSError:
            exit(1)

    if os.path.exists(destDir1):
        try:
            shutil.rmtree(destDir1)
        except OSError:
            exit(1)

    if os.path.exists(home + "/.local/share/applications/teamviewer-teamviewer11.desktop"):
        try:
            os.remove(home + "/.local/share/applications/teamviewer-teamviewer11.desktop")
        except OSError:
            exit(1)

    subprocess.call(["pkexec", sys.argv[3] + "custom/teamviewer/teamviewer_remove.sh"])


if sys.argv[1] == "--install":
    installCustomIndicatorIcons(sys.argv[2])
elif sys.argv[1] == "--remove":
    removeCustomIndicatorIcons()
