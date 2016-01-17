#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# InstallerFunctions.py elementary+ Configurator Installer Functions
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

import os
import shutil
from os import symlink
from gi.repository import Gio, Notify
from os.path import expanduser
import subprocess

home = expanduser ("~")
system_settings = Gio.Settings.new ("org.gnome.desktop.interface")
elementaryplus_settings = Gio.Settings.new ("apps.elementaryPlusConfigurator")

app_name = "elementary+ Configurator"
icon_theme_name = "elementaryPlus"

from_PPA = False

if from_PPA:
    what_to_use = "link"
else:
    what_to_use = "copy"

class Installer ():
    def __init__ (self):
        Notify.init (app_name)

    def install (self, app_name, install_method, sni_qt_prefix, configurator_directory, plugins_directory, plugin):
        if install_method == "standard":
            try:
                self.install_qt_indicator_icons (app_name, sni_qt_prefix, plugins_directory)
            except Exception:
                self.notify (
                    'elementary+ Configurator', 
                    '{} {}'.format ('Error while installing', app_name.replace ("_", " ").capitalize ()), 
                    'error'
                )
                raise Exception ("Error while installing")
        else:
            try:
                subprocess.check_output (
                    [
                        'python', 
                        '{}{}{}'.format (plugins_directory, plugin, "/configure.py"), 
                        "--install", 
                        what_to_use, 
                        plugins_directory
                    ]
                )
            except subprocess.CalledProcessError as e:
                self.notify (
                    'elementary+ Configurator', 
                    e.output,
                    'error'
                )
                raise Exception ("Error while installing (custom)")

        return True

    def remove (self, app_name, install_method, sni_qt_prefix, configurator_directory, plugins_directory, plugin):
        try:
            if install_method == "standard":
                try:
                    self.remove_qt_indicator_icons (sni_qt_prefix)
                except:
                    raise Exception ("Error while removing")
            else:
                try:
                    subprocess.call (
                        [
                            'python', 
                            '{}{}{}'.format (plugins_directory, plugin, "/configure.py"), 
                            "--remove", 
                            what_to_use, 
                            plugins_directory
                        ]
                    )
                except subprocess.CalledProcessError as e:
                    self.notify (
                        'elementary+ Configurator', 
                        e.output,
                        'error'
                    )
                    raise Exception ("Error while removing (custom)")
        except:
            self.notify (
                'elementary+ Configurator', 
                '{} {}'.format ('Error while removing', app_name.replace ("_", " ").capitalize ()), 
                'error'
            )
            return False

        return True

    def install_qt_indicator_icons (self, app_name, sni_qt_prefix, plugins_directory):
        icon_directory = "{}{}{}".format (plugins_directory, app_name, "/icons/")
        destination_directory = "{}{}{}{}".format (home, "/.local/share/sni-qt/icons/", sni_qt_prefix, "/")

        if what_to_use == "copy":
            if os.path.exists (destination_directory):
                try:
                    shutil.rmtree (destination_directory)
                except:
                    raise Exception ("Error while removing destination_directory (copy)")

            try:
                shutil.copytree (icon_directory, destination_directory)
            except:
                raise Exception ("Error while installing (link)")

            return True
        elif what_to_use == "link":
            if not os.path.exists (destination_directory):
                os.makedirs (destination_directory)
            else:
                try:
                    shutil.rmtree (destination_directory)
                except:
                    raise Exception ("Error while removing destination_directory (link)")
                os.makedirs (destination_directory)
            for icon in os.listdir (icon_directory):
                try:
                    symlink (icon_directory + icon, destination_directory + icon)
                except:
                    raise Exception ("Error while installing (link)")
            
            return True
        else:
            print "Invalid operation!"

    def remove_qt_indicator_icons (self, sni_qt_prefix):
        destination_directory = home + "/.local/share/sni-qt/icons/" + sni_qt_prefix
        if os.path.exists (destination_directory):
            try:
                shutil.rmtree (destination_directory)
            except:
                raise Exception ("Error while removing destination_directory")

        return True

    def toggle_theme (self, operation, plugins_directory):
        current_theme = system_settings.get_string ("icon-theme")
        previous_icon_theme = elementaryplus_settings.get_string ("previous-icon-theme")

        if os.path.isdir (home + "/.local/share/icons/elementaryPlus"):
            shutil.rmtree (home + "/.local/share/icons/elementaryPlus")

        try:
            if os.path.isdir ("/usr/share/icons/elementaryPlus"):
                print "/usr/share... exists"
                if operation == "install":
                    if from_PPA:
                        if os.path.isdir (home + "/.icons/elementaryPlus"):
                            print "Remove from .icons"
                            shutil.rmtree (home + "/.icons/elementaryPlus")
                        if current_theme != icon_theme_name:
                            elementaryplus_settings.set_string ("previous-icon-theme", current_theme)
                            system_settings.set_string ("icon-theme", icon_theme_name)
                    else:
                        subprocess.call (
                            [
                                'python', 
                                '{}{}'.format (plugins_directory, "core/configure.py"), 
                                "--install", 
                                what_to_use, 
                                plugins_directory
                            ]
                        )
                        if current_theme != icon_theme_name:
                            elementaryplus_settings.set_string ("previous-icon-theme", current_theme)
                            system_settings.set_string ("icon-theme", icon_theme_name)
                else:
                    if from_PPA:
                        system_settings.set_string ("icon-theme", previous_icon_theme)
                    else:
                        subprocess.call(
                            [
                                'python', 
                                '{}{}'.format (plugins_directory, "core/configure.py"), 
                                "--remove", 
                                what_to_use, 
                                plugins_directory
                            ]
                        )
                        system_settings.set_string ("icon-theme", previous_icon_theme)
            else:
                print "/usr/share... does not exist"
                if operation == "install":
                    subprocess.call (
                        [
                            'python', 
                            '{}{}'.format (plugins_directory, "core/configure.py"), 
                            "--install", 
                            what_to_use, 
                            plugins_directory
                        ]
                    )
                    elementaryplus_settings.set_string ("previous-icon-theme", current_theme)
                    system_settings.set_string ("icon-theme", icon_theme_name)
                else:
                    subprocess.call(
                        [
                            'python', 
                            '{}{}'.format (plugins_directory, "core/configure.py"), 
                            "--remove", 
                            what_to_use, 
                            plugins_directory
                        ]
                    )
                    system_settings.set_string("icon-theme", previous_icon_theme)
        except:
            return False

        return True

    def notify (self, message_one, message_two, icon):
        try:
            notification = Notify.Notification.new (message_one, message_two, icon)
            notification.set_urgency (1)
            notification.show ()
            del notification
        except:
            pass