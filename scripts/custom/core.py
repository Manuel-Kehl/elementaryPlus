#!/usr/bin/env python
import sys
import os
from os import symlink
from os.path import expanduser
import shutil
from whatToUse import *

home = expanduser("~")

themeDir = os.getcwd() + "/elementaryPlus"
destDir = home + "/.icons/"

def installCustomIndicatorIcons():
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    try:
        shutil.copytree(themeDir, destDir + "elementaryPlus")
    except:
        return False

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