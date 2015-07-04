#!/usr/bin/env python
import sys
import os
from os import symlink
from os.path import expanduser
import shutil
from whatToUse import *

home = expanduser("~")

def listfiles(folder):
    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            yield os.path.join(root, filename)

def installCustomIndicatorIcons():
    icon = os.getcwd() + "/scripts/icons/spotify/icon.png"
    destDir = home + "/.local/share/sni-qt/icons/spotify/"

    for filename in listfiles('/tmp/'):
        if "/icons/hicolor/512x512/apps/" in filename:
            uuid = filename.split("/")
            uuid = uuid[-1].split("_")
            uuid = uuid[-1]

    print uuid

    if not os.path.exists(destDir):
        os.makedirs(destDir)
    else:
        try:
            shutil.rmtree(destDir)
        except:
            return False
        os.makedirs(destDir)

    if installMethod == "copy":
        copy = shutil.copy(icon, destDir + uuid)
        return copy
    elif installMethod == "link":
        link = symlink(icon, destDir + uuid)
        return link
    else:
        print "Invalid operation!"

def removeCustomIndicatorIcons():
    destDir = home + "/.local/share/sni-qt/icons/spotify"
    if os.path.exists(destDir):
        try:
            shutil.rmtree(destDir)
        except:
            return False
    else:
        return True

if sys.argv[1] == "--install":
    installCustomIndicatorIcons()
elif sys.argv[1] == "--remove":
    removeCustomIndicatorIcons()