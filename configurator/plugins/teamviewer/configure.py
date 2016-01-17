#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# telegram_desktop.py telegram indicator icons custom install script
#
# Copyright  (C) 2015  Stefan Ric (cybre)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
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


icon_directory = sys.argv[3] + "teamviewer/icons/"
home = expanduser ("~")
destination_directory = home + "/.local/share/sni-qt/icons/teamviewer/"
destination_directory1 = home + "/.local/share/sni-qt/icons/TVGuiDelegate/"

def install_custom_indicator_icons (what_to_use):
    if not os.path.exists (destination_directory):
        os.makedirs (destination_directory)
    else:
        try:
            shutil.rmtree (destination_directory)
        except OSError:
            raise Exception ("Error removing destination_directory (teamviewer)")
        os.makedirs (destination_directory)

    if not os.path.exists (destination_directory1):
        os.makedirs (destination_directory1)
    else:
        try:
            shutil.rmtree (destination_directory1)
        except OSError:
            print "Error while installing TeamViewer"
            raise Exception ("Error removing destination_directory1 (teamviewer)")
        os.makedirs (destination_directory1)

    if what_to_use == "copy":
        try:
            for icon in os.listdir (icon_directory):
                shutil.copy (icon_directory + icon, destination_directory + icon)
                shutil.copy (icon_directory + icon, destination_directory1 + icon)
        except:
            print "Error while installing TeamViewer"
            raise Exception ("Error installing teamviewer (copy)")
    elif what_to_use == "link":
        try:
            for icon in os.listdir (icon_directory):
                symlink (icon_directory + icon, destination_directory + icon)
                symlink (icon_directory + icon, destination_directory1 + icon)
        except:
            print "Error while installing TeamViewer"
            raise Exception ("Error installing teamviewer (link)")
    else:
        print "Invalid operation!"

    if os.path.exists (home + "/.local/share/applications/teamviewer-teamviewer11.desktop"):
        shutil.copy (home + "/.local/share/applications/teamviewer-teamviewer11.desktop", home + "/.local/share/applications/teamviewer-teamviewer11.desktop.bak")
    shutil.copy (sys.argv[3] + "teamviewer/teamviewer/teamviewer-teamviewer11.desktop", home + "/.local/share/applications/teamviewer-teamviewer11.desktop")

    subprocess.call (["pkexec", sys.argv[3] + "teamviewer/teamviewer/teamviewer.sh"])

def remove_custom_indicator_icons ():
    if os.path.exists (destination_directory):
        try:
            shutil.rmtree (destination_directory)
        except OSError:
            print "Error while removing TeamViewer"
            raise Exception ("Error removing destination_directory (teamviewer)")

    if os.path.exists (destination_directory1):
        try:
            shutil.rmtree (destination_directory1)
        except OSError:
            print "Error while removing TeamViewer"
            raise Exception ("Error removing destination_directory1 (teamviewer)")

    if os.path.exists (home + "/.local/share/applications/teamviewer-teamviewer11.desktop"):
        try:
            os.remove (home + "/.local/share/applications/teamviewer-teamviewer11.desktop")
        except OSError:
            print "Error while removing TeamViewer"
            raise Exception ("Error removing .local desktop file (teamviewer)")

    subprocess.call (["pkexec", sys.argv[3] + "teamviewer/teamviewer/teamviewer_remove.sh"])


if sys.argv[1] == "--install":
    install_custom_indicator_icons (sys.argv[2])
elif sys.argv[1] == "--remove":
    remove_custom_indicator_icons ()
