#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# core.py core icon theme custom install script
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

themeDir = os.getcwd() + "/elementaryPlus"
home = expanduser("~")
destDir = home + "/.icons/"
destDir2 = home + "/.local/share/icons/"


def installCoreIconTheme():
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    try:
        shutil.copytree(themeDir, destDir + "elementaryPlus")
    except:
        exit(1)


def removeCoreIconTheme():
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir + "elementaryPlus")
            shutil.rmtree(destDir2 + "elementaryPlus")
        except OSError:
            pass

if sys.argv[1] == "--install":
    installCoreIconTheme()
elif sys.argv[1] == "--remove":
    removeCoreIconTheme()
