#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# telegram_desktop.py telegram indicator icons custom install script
#
# Copyright  (C) 2015  Stefan Ric  (cybre)
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

icon_directory = sys.argv[3] + "telegram_desktop/icons/"
home = expanduser ("~")
destination_directory = home + "/.TelegramDesktop/tdata/ticons/"

def install_custom_indicator_icons (what_to_use):
    if not os.path.exists (destination_directory):
        os.makedirs (destination_directory)
    else:
        try:
            shutil.rmtree (destination_directory)
        except OSError:
            print "Error while installing Telegram"
            raise Exception ("Error while removing destination_directory (telegram)")
        os.makedirs (destination_directory)

    if what_to_use == "copy":
        try:
            for icon in os.listdir (icon_directory):
                shutil.copy (icon_directory + icon, destination_directory + icon)
            symlink (destination_directory + "ico_22_0.png", destination_directory + "icomute_22_0.png")
            for i in range (2, 100):
                symlink (destination_directory + "ico_22_1.png", destination_directory + "ico_22_" + str (i) + ".png")
            for i in range (1, 100):
                symlink (destination_directory + "ico_22_1.png", destination_directory + "icomute_22_" + str (i) + ".png")
        except:
            print "Error while installing Telegram"
            raise Exception ("Error while installing Telegram (copy)")
    elif what_to_use == "link":
        try:
            for icon in os.listdir (icon_directory):
                symlink (icon_directory + icon, destination_directory + icon)
            symlink (icon_directory + "ico_22_0.png", destination_directory + "icomute_22_0.png")
            for i in range (2, 100):
                symlink (icon_directory + "ico_22_1.png", destination_directory + "ico_22_" + str (i) + ".png")
            for i in range (1, 100):
                symlink (icon_directory + "ico_22_1.png", destination_directory + "icomute_22_" + str (i) + ".png")
        except:
            print "Error while installing Telegram"
            raise Exception ("Error while installing Telegram (link)")
    else:
        print "Invalid operation!"

    file = open (destination_directory + "elementaryPlus.installed", "w")
    file.close ()

def remove_custom_indicator_icons ():
    if os.path.exists (destination_directory):
        try:
            shutil.rmtree (destination_directory)
        except OSError:
            print "Error while removing Telegram"
            raise Exception ("Error while removing Telegram")


if sys.argv[1] == "--install":
    install_custom_indicator_icons (sys.argv[2])
elif sys.argv[1] == "--remove":
    remove_custom_indicator_icons ()
