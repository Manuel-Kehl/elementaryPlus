#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# elementaryplus-installer.py elementary+ Installer/Configurator
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
#
# Some code taken from Evolve-SC (https://github.com/solus-project/evolve-sc)

from gi.repository import Gtk, Gdk, Gio, Notify
import sys
import os
from os import symlink
from os.path import expanduser
import shutil
import subprocess
import apt

if not (Gtk.get_major_version() == 3 and Gtk.get_minor_version() >= 14):
    sys.exit("You need to have GTK 3.14 or newer to run this script")

appName = "elementary+ Configurator"
iconThemeName = "elementaryPlus"

fromPPA = False

if fromPPA is True:
    whatToUse = "link"
else:
    whatToUse = "copy"

scripts = os.getcwd() + "/scripts/"
schema = "/usr/share/glib-2.0/schemas/apps.elementaryPlusConfigurator.gschema.xml"

if os.path.isfile(schema) is False:
    subprocess.call(["pkexec", scripts + "first_start.sh", scripts])

settings = Gio.Settings.new("apps.elementaryPlusConfigurator")
patchedSniqt = settings.get_boolean("sniqt-patched")

systemSettings = Gio.Settings.new("org.gnome.desktop.interface")

home = expanduser("~")

iconMegaList = [
    # [
    #   "Name",
    #   "Sni-qt prefix",
    #   "Binary/Static File", [/path/to/file]
    #   "Description",
    #   "Icon",
    #   "Install Method", ["custom", "standard"]
    # ],
    [
        "Core icon theme",
        "",
        "",
        "The core elementary+ icon theme",
        "preferences-desktop",
        "custom"
    ],
    [
        "Bitcoin",
        "bitcoin-qt",
        "/usr/bin/bitcoin-qt",
        "Bitcoin is a free open source peer-to-peer electronic cash system that is completely decentralized, without the need for a central server or trusted parties",
        "bitcoin128",
        "standard"
    ],
    [
        "flareGet",
        "flareget",
        "/usr/bin/flareget",
        "FlareGet is a full featured, multi-threaded download manager and accelerator for Windows, Mac and Linux",
        "flareget",
        "standard"
    ],
    [
        "Google Music Manager",
        "MusicManager",
        "/opt/google/musicmanager/google-musicmanager",
        "With Google Play Music for Chrome or Music Manager, you can add your personal music library to the cloud",
        "google-musicmanager",
        "standard"
    ],
    [
        "HP Linux Printing and Imaging",
        "python2.7",
        "/usr/bin/hp-systray",
        "The HP Linux Printing and Imaging System provides full support for printing on most HP SFP inkjets and many LaserJets, and for scanning, sending faxes and for photo-card access on most HP MFP printers",
        "HPmenu",
        "standard"
    ],
    [
        "MEGAsync",
        "megasync",
        "/usr/bin/megasync",
        "MEGAsync is a free online storage service",
        "mega",
        "standard"
    ],
    [
        "Mumble",
        "mumble",
        "/usr/bin/mumble",
        "Mumble is a low-latency, high quality voice chat program for gaming",
        "mumble",
        "standard"
    ],
    [
        "OwnCloud",
        "owncloud",
        "/usr/bin/owncloud",
        "An enterprise file sharing solution for online collaboration and storage",
        "owncloud",
        "standard"
    ],
    [
        "ScreenCloud",
        "screencloud",
        "/usr/bin/screencloud",
        "ScreenCloud is a Screenshot sharing tool",
        "screencloud",
        "standard"
    ],
    [
        "Seafile Client",
        "seafile-applet",
        "/usr/bin/seafile-applet",
        "The Seafile desktop client",
        "seafile",
        "standard"
    ],
    [
        "Skype",
        "skype",
        "/usr/bin/skype",
        "Stay in touch with your family and friends for free on Skype",
        "skype",
        "standard"
    ],
    [
        "Spotify",
        "spotify",
        ["/opt/spotify/spotify-client/spotify", "/usr/bin/spotify"],
        "Spotify is a digital music service that gives you access to millions of songs",
        "spotify-client",
        "custom"
    ],
    [
        "Teamviewer",
        "teamviewer",
        "/usr/bin/teamviewer",
        "TeamViewer is a software package for remote control, desktop sharing, online meetings, web conferencing and file transfer between computers",
        "teamviewer",
        "custom"
    ],
    [
        "Telegram Desktop",
        "",
        "%s/.TelegramDesktop/tdata/icon.png" % (home),
        "Telegram is a messaging app with a focus on speed and security, it's super fast, simple and free",
        "telegram",
        "custom"
    ],
    [
        "Tomahawk",
        "tomahawk",
        "/usr/bin/tomahawk",
        "A new kind of music player that invites all your streams, downloads, cloud music storage, playlists, radio stations and friends to the same party. It's about time they all mingle",
        "tomahawk",
        "standard"
    ],
    [
        "WizNote",
        "WizNote",
        "/usr/bin/WizNote",
        "Wiznote is a cloud based notes solution which helps personal and professional to take notes and collaborate with team members",
        "wiznote",
        "standard"
    ]
]

customCheckLocations = [
    [
        "telegram_desktop",
        ["%s/.TelegramDesktop/tdata/ticons/elementaryPlus.installed" % (home)]
    ]
]

installedComponents = []
availableComponents = []

iconTheme = Gtk.IconTheme
defaultIconTheme = iconTheme.get_default()


def checkIfInstalled(appName):
    for customLocation in customCheckLocations:
        if appName in customLocation:
            for location in customLocation[1]:
                if os.path.isfile(location):
                    installedComponents.append(appName)
    if os.path.isdir("%s/.local/share/sni-qt/icons/" % (home) + codeName):
        installedComponents.append(codeName)

for a in iconMegaList:
    name = a[0]
    codeName = a[0].lower().replace(" ", "_")
    shortDesc = (a[3][:60] + '...') if len(a[3]) > 60 else a[3]
    icon = ("package-x-generic") if iconTheme.has_icon(defaultIconTheme, a[4]) == False else a[4]
    installMethod = a[5]
    sniqtPrefix = a[1]
    if isinstance(a[2], list):
        for checkLocation in a[2]:
            print checkLocation
            if os.path.isfile(checkLocation):
                enabled = True
                break
            else:
                enabled = False
    else:
        enabled = (True) if os.path.isfile(a[2]) or codeName == "core_icon_theme" else False

    checkIfInstalled(codeName)
    availableComponents.append([name, codeName, shortDesc, icon, installMethod, sniqtPrefix, enabled])

availableComponents.sort(key=lambda x: x[6], reverse=True)

print "installed", installedComponents


class InstallerWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=appName)
        self.set_size_request(500, 500)
        self.set_icon_name("preferences-desktop")

        self.error = 0

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "elementary+"
        self.hb.set_subtitle("Configurator")
        self.set_titlebar(self.hb)

        searchIcon = Gtk.Image.new_from_icon_name("edit-find-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
        searchButton = Gtk.ToggleButton()
        searchButton.set_image(searchIcon)
        searchButton.connect('clicked', self.search_handler)
        self.searchButton = searchButton
        self.hb.pack_start(searchButton)

        Notify.init(appName)

        self.add(self.build_ui())

        style_provider = Gtk.CssProvider()

        css = """
        .search-bar {
            border-width: 0;
        }
        """

        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def notify(self, messageOne, messageTwo, icon):
        try:
            notification = Notify.Notification.new(messageOne, messageTwo, icon)
            notification.set_urgency(1)
            notification.show()
            del notification
        except:
            pass

    def build_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.searchBar = Gtk.SearchBar()
        self.searchBar.get_style_context().add_class("primary-toolbar")
        self.searchBar.set_halign(Gtk.Align.FILL)
        self.searchBar.set_show_close_button(True)

        entry = Gtk.SearchEntry()
        entry.connect("search-changed", self.search_changed)
        self.searchBar.add(entry)
        self.searchBar.connect_entry(entry)
        vbox.pack_start(self.searchBar, False, False, 0)
        self.searchEntry = entry
        self.connect("key-press-event", lambda x, y: self.searchBar.handle_event(y))

        iconsPage = self.create_icons_page()
        vbox.pack_start(iconsPage, True, True, 0)

        return vbox

    def create_icons_page(self):
        scroller = Gtk.ScrolledWindow(None, None)
        scroller.set_border_width(10)
        scroller.set_shadow_type(Gtk.ShadowType.IN)
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.lbox = Gtk.ListBox()
        self.lbox.set_selection_mode(Gtk.SelectionMode.NONE)

        placeholder = Gtk.Label()
        self.placeholder = placeholder
        placeholder.set_use_markup(True)
        placeholder.get_style_context().add_class("dim-label")
        self.lbox.set_placeholder(placeholder)
        placeholder.show_all()

        scroller.add(self.lbox)
        for i in range(len(availableComponents)):
            for sublist in iconMegaList:
                if sublist[0] == availableComponents[i][0]:
                    longDesc = sublist[3]
            item = self.create_item(availableComponents[i][0], availableComponents[i][3], availableComponents[i][2], availableComponents[i][6])

            componentSwitch = Gtk.Switch()
            componentSwitch.set_name(availableComponents[i][0].lower())
            componentSwitch.props.halign = Gtk.Align.END
            componentSwitch.props.valign = Gtk.Align.CENTER
            componentSwitch.connect("notify::active", self.callback, availableComponents[i][1], availableComponents[i][4], availableComponents[i][5])

            if availableComponents[i][1] in installedComponents:
                componentSwitch.set_active(True)

            if availableComponents[i][1] == "core_icon_theme":
                currentTheme = systemSettings.get_string("icon-theme")
                if currentTheme == iconThemeName:
                    componentSwitch.set_active(True)

            wrap = Gtk.HBox(0)
            wrap.pack_start(item, True, True, 0)
            wrap.pack_end(componentSwitch, False, False, 2)

            if availableComponents[i][6] is False:
                wrap.set_sensitive(False)

            wrap.set_tooltip_text(longDesc)

            self.lbox.add(wrap)

        return scroller

    def create_item(self, name, iconName, shortDesc, enabled):
        grid = Gtk.Grid()
        grid.set_border_width(16)
        grid.set_row_spacing(4)
        grid.set_column_spacing(16)

        if enabled is True:
            label = Gtk.Label("<big>%s</big>" % name)
        else:
            label = Gtk.Label("<big>%s (Not installed)</big>" % name)
        label.set_use_markup(True)
        label.set_alignment(0.0, 0.5)
        icon = Gtk.Image.new_from_icon_name(iconName, Gtk.IconSize.DIALOG)
        desc = Gtk.Label(shortDesc)
        desc.get_style_context().add_class("dim-label")
        desc.set_alignment(0.0, 0.5)
        grid.attach(icon, 0, 0, 1, 2)
        grid.attach(label, 1, 0, 1, 1)
        grid.attach(desc, 1, 1, 1, 1)

        return grid

    def search_handler(self, w):
        w.freeze_notify()
        self.searchBar.set_search_mode(w.get_active())
        w.thaw_notify()

    def search_changed(self, w, data=None):
        text = w.get_text().strip()
        if text == "":
            self.searchBar.set_search_mode(False)

        act = False if text == "" else True
        self.searchButton.freeze_notify()
        self.searchButton.set_active(act)
        self.searchButton.thaw_notify()
        self.searching(w)

    def searching(self, entry, event=None):
        text = entry.get_text().strip()
        self.lbox.set_filter_func(self.filter, text)

        res = False
        for child in self.lbox.get_children():
            if child.get_visible() and child.get_child_visible():
                res = True
                break
        if not res:
            self.placeholder.set_markup("<big>No results</big>")

    def filter(self, row, text):
        name = row.get_children()[0].get_children()[0].get_children()[1].get_text()
        desc = row.get_children()[0].get_tooltip_text()

        if text.lower() in name.lower() or text.lower() in desc.lower():
            return True
        else:
            return False

    def callback(self, widget, event, data, method, sniqtPrefix):
        if widget.get_active() == 1:
            if data == "core_icon_theme":
                self.toggleTheme("install")
            elif data not in installedComponents:
                self.install(data, method, sniqtPrefix)
        else:
            if data == "core_icon_theme":
                self.toggleTheme("remove")
            elif data in installedComponents and self.error == 0:
                self.remove(data, method, sniqtPrefix)

    def install(self, appName, installMethod, sniqtPrefix):
        patchedSniqt = settings.get_boolean("sniqt-patched")
        if appName != "core_icon_theme" and appName != "telegram_desktop" and patchedSniqt is False and fromPPA is False:
            print "Installing patched sni-qt"
            self.notify('This may take a while', 'Please don\'t close the window', 'preferences-desktop')
            if subprocess.call(['pkexec', scripts + "sni-qt.sh"]) == 0:
                cache = apt.Cache()
                version = cache["sni-qt"].candidate.version
                if "0.2.7" in version:
                    print "Succesfully patched sni-qt"
                    settings.set_boolean("sniqt-patched", True)
                else:
                    print "Failed to patch sni-qt"
            else:
                print "Unknown error"

        out = 0
        if installMethod == "standard":
            out = self.installQtIndicatorIcons(appName, sniqtPrefix)
        else:
            out = subprocess.call(['python', scripts + "custom/" + appName + ".py", "--install", whatToUse, scripts])
            print out

        if out == 1:
            self.error = 1
            if appName != "spotify":
                self.notify('elementary+ Configurator', 'Error while installing ' + appName.replace("_", " ").capitalize(), 'error')

        if self.error == 0:
            installedComponents.append(appName)

    def remove(self, appName, installMethod, sniqtPrefix):
        out = 0
        if installMethod == "standard":
            out = self.removeQtIndicatorIcons(sniqtPrefix)
        else:
            out = subprocess.call(['python', scripts + "custom/" + appName + ".py", "--remove", whatToUse, scripts])

        if out == 1:
            self.error = 1
            self.notify('elementary+ Configurator', 'Error while removing ' + appName.replace("_", " ").capitalize(), 'error')

        if self.error == 0:
            installedComponents.remove(appName)

    def installQtIndicatorIcons(self, appName, sniqtPrefix):
        iconDir = scripts + "icons/" + appName + "/"
        destDir = home + "/.local/share/sni-qt/icons/" + sniqtPrefix + "/"

        if whatToUse == "copy":
            if os.path.exists(destDir):
                try:
                    shutil.rmtree(destDir)
                except:
                    return False
            copy = shutil.copytree(iconDir, destDir)
            return copy
        elif whatToUse == "link":
            if not os.path.exists(destDir):
                os.makedirs(destDir)
            else:
                try:
                    shutil.rmtree(destDir)
                except:
                    return False
                os.makedirs(destDir)
            for icon in os.listdir(iconDir):
                link = symlink(iconDir + icon, destDir + icon)
            return link
        else:
            print "Invalid operation!"

    def removeQtIndicatorIcons(self, sniqtPrefix):
        destDir = home + "/.local/share/sni-qt/icons/" + sniqtPrefix
        if os.path.exists(destDir):
            try:
                shutil.rmtree(destDir)
            except:
                return False
        else:
            return True

    def toggleTheme(self, operation):
        currentTheme = systemSettings.get_string("icon-theme")
        previousIconTheme = settings.get_string("previous-icon-theme")

        if os.path.isdir(home + "/.local/share/icons/elementaryPlus"):
            shutil.rmtree(home + "/.local/share/icons/elementaryPlus")

        if os.path.isdir("/usr/share/icons/elementaryPlus"):
            print "/usr/share... exists"
            if operation == "install":
                if fromPPA is True:
                    if os.path.isdir(home + "/.icons/elementaryPlus"):
                        print "Remove from .icons"
                        shutil.rmtree(home + "/.icons/elementaryPlus")
                    if currentTheme != iconThemeName:
                        settings.set_string("previous-icon-theme", currentTheme)
                        systemSettings.set_string("icon-theme", iconThemeName)
                else:
                    out = subprocess.call(['python', scripts + "custom/core_icon_theme.py", "--install", whatToUse, scripts])
                    if currentTheme != iconThemeName:
                        settings.set_string("previous-icon-theme", currentTheme)
                        systemSettings.set_string("icon-theme", iconThemeName)
            else:
                if fromPPA is True:
                    systemSettings.set_string("icon-theme", previousIconTheme)
                else:
                    out = subprocess.call(['python', scripts + "custom/core_icon_theme.py", "--remove", whatToUse, scripts])
                    systemSettings.set_string("icon-theme", previousIconTheme)
        else:
            print "/usr/share... does not exist"
            if operation == "install":
                out = subprocess.call(['python', scripts + "custom/core_icon_theme.py", "--install", whatToUse, scripts])
                settings.set_string("previous-icon-theme", currentTheme)
                systemSettings.set_string("icon-theme", iconThemeName)
            else:
                out = subprocess.call(['python', scripts + "custom/core_icon_theme.py", "--remove", whatToUse, scripts])
                systemSettings.set_string("icon-theme", previousIconTheme)

win = InstallerWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
