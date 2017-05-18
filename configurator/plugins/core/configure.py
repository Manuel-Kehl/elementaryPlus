#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# core.py core icon theme custom install script
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
from os.path import expanduser
import shutil

theme_directory = os.getcwd () + "/elementaryPlus"
home = expanduser ("~")
destination_directory = home + "/.icons/"
destination_directory2 = home + "/.local/share/icons/"

def install_core_icon_theme ():
    if not os.path.exists (destination_directory):
        os.makedirs (destination_directory)
    try:
        shutil.copytree (theme_directory, destination_directory + "elementaryPlus")
    except:
        raise Exception ("Error while creating destination_directory (core)")

def remove_core_icon_theme ():
    if os.path.exists (destination_directory):
        try:
            shutil.rmtree (destination_directory + "elementaryPlus")
            shutil.rmtree (destination_directory2 + "elementaryPlus")
        except OSError:
            pass

if sys.argv[1] == "--install":
    install_core_icon_theme ()
elif sys.argv[1] == "--remove":
    remove_core_icon_theme ()
