#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# configure.py spotify indicator icon custom install script
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

icon = sys.argv[3] + "spotify/icons/icon.png"
home = expanduser ("~")
destination_directory = home + "/.local/share/sni-qt/icons/spotify/"

def list_files (folder):
    for root, folders, files in os.walk (folder):
        for filename in folders + files:
            yield os.path.join (root, filename)

def install_custom_indicator_icons (what_to_use):
    uuid = ""
    for filename in list_files ('/tmp/'):
        if "/icons/hicolor/512x512/apps/" in filename:
            uuid = filename.split ("/")
            uuid = uuid[-1].split ("_")
            uuid = uuid[-1]

    if uuid != "":
        if not os.path.exists (destination_directory):
            os.makedirs (destination_directory)
        else:
            shutil.rmtree (destination_directory)
            os.makedirs (destination_directory)

        if what_to_use == "copy":
            shutil.copy (icon, destination_directory + uuid)
        elif what_to_use == "link":
            symlink (icon, destination_directory + uuid)
        else:
            print "Invalid operation!"
    else:
        print "Failed to install Spotify\nPlease run Spotify and try again!"
        raise Exception ("Error while installing spotify")

def remove_custom_indicator_icons ():
    if os.path.exists (destination_directory):
        try:
            shutil.rmtree (destination_directory)
        except:
            print "Failed to remove Spotify"
            raise Exception ("Error while removing spotify")


if sys.argv[1] == "--install":
    install_custom_indicator_icons (sys.argv[2])
elif sys.argv[1] == "--remove":
    remove_custom_indicator_icons ()
