#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# elementaryplus-configurator.py elementary+ Installer/Configurator
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
#
# Some code taken from Evolve-SC  (https://github.com/solus-project/evolve-sc)

from gi.repository import Gtk, Gio, Notify
import os
from os.path import expanduser
import json
from InstallerFunctions import Installer
import sys
import subprocess
import threading
import platform

if not (Gtk.get_major_version() == 3 and Gtk.get_minor_version() >= 14):
    sys.exit("You need to have GTK 3.14 or newer to run this script")

app_name = "elementary+ Configurator"
icon_theme_name = "elementaryPlus"

home = expanduser ("~")
configurator_directory = "{}{}".format (os.getcwd(), "/configurator/")
plugins_directory = "{}{}".format (configurator_directory, "plugins/")

architecture = platform.architecture ()[0]

schema = "/usr/share/glib-2.0/schemas/apps.elementaryPlusConfigurator.gschema.xml"

if os.path.isfile(schema) is False:
    subprocess.call(["pkexec", configurator_directory + "first_start.sh", configurator_directory])

system_settings = Gio.Settings.new ("org.gnome.desktop.interface")
default_icon_theme = Gtk.IconTheme.get_default ()

installer = Installer ()

class ConfiguratorWindow (Gtk.Window):
    def __init__ (self):
        Gtk.Window.__init__ (self, title=app_name)
        self.set_size_request (500, 500)
        self.set_icon_name ("preferences-desktop")

        headerbar = Gtk.HeaderBar ()
        headerbar.set_show_close_button (True)
        headerbar.props.title = "elementary+"
        headerbar.props.subtitle = "Configurator"
        self.set_titlebar (headerbar)

        search_icon = Gtk.Image.new_from_icon_name ("edit-find-symbolic", Gtk.IconSize.MENU)
        search_button = Gtk.ToggleButton ()
        search_button.set_image (search_icon)
        search_button.connect ('clicked', self.search_handler)
        self.search_button = search_button
        headerbar.pack_start (search_button)

        if not os.path.isfile ("/etc/xdg/sni-qt-eplus.installed") or \
           not os.path.isfile ("/usr/lib/i386-linux-gnu/qt4/plugins/systemtrayicon/libsni-qt.so") or \
           (not os.path.isfile ("/usr/lib/x86_64-linux-gnu/qt4/plugins/systemtrayicon/libsni-qt.so") and architecture == "64bit"):
            question_dialog = Gtk.MessageDialog (self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Do you want to install out patched sni-qt?")
            question_dialog.format_secondary_text ("Without it you won't be able to install custom indicator icons")
            response = question_dialog.run()

            if response == Gtk.ResponseType.YES:
                self.patch_sni_qt ()

            elif response == Gtk.ResponseType.NO:
                print("QUESTION dialog closed by clicking NO button")

            question_dialog.destroy()

        Notify.init (app_name)

        self.add (self.build_ui ())

    def build_ui (self):
        vbox = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=0)
        search_bar = Gtk.SearchBar ()
        self.search_bar = search_bar
        search_bar.get_style_context ().add_class ("primary-toolbar")
        search_bar.set_halign (Gtk.Align.FILL)
        search_bar.set_show_close_button (True)

        search_entry = Gtk.SearchEntry ()
        search_entry.connect ("search-changed", self.search_changed)
        search_bar.add (search_entry)
        search_bar.connect_entry (search_entry)
        vbox.pack_start (search_bar, False, False, 0)
        self.search_entry = search_entry
        self.connect ("key-press-event", lambda x, y: search_bar.handle_event (y))

        icons_page = self.create_icons_page ()
        vbox.pack_start (icons_page, True, True, 0)

        return vbox

    def create_icons_page (self):
        scroller = Gtk.ScrolledWindow (None, None)
        scroller.set_border_width (10)
        scroller.set_shadow_type (Gtk.ShadowType.IN)
        scroller.set_policy (Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        listbox = Gtk.ListBox ()
        self.listbox = listbox
        listbox.set_selection_mode (Gtk.SelectionMode.NONE)

        placeholder = Gtk.Label ()
        self.placeholder = placeholder
        placeholder.set_use_markup (True)
        placeholder.get_style_context ().add_class ("dim-label")
        listbox.set_placeholder (placeholder)
        placeholder.show_all ()

        scroller.add (listbox)

        plugin_list = self.list_plugins ()
        plugin_list.sort ()

        available_components = []

        for folder in plugin_list:
            data = self.fetch_plugin_info (folder)

            if data['sni-qt-prefix'] != "":
                if not os.path.isfile ("/etc/xdg/sni-qt-eplus.installed") or \
                   not os.path.isfile ("/usr/lib/i386-linux-gnu/qt4/plugins/systemtrayicon/libsni-qt.so") or \
                   (not os.path.isfile ("/usr/lib/x86_64-linux-gnu/qt4/plugins/systemtrayicon/libsni-qt.so") and architecture == "64bit"):
                    continue

            code_name = data['label'].lower ().replace (" ", "_")
            available_components.append (
                [
                    data['icon'], 
                    data['label'], 
                    data['description'], 
                    data['sni-qt-prefix'], 
                    data['install-method'], 
                    data['check-if-installed'], 
                    data['custom-check-location'], 
                    folder,
                    self.check_if_installed (code_name, data['check-if-installed'])
                ]
            )

        available_components.sort (key=lambda x: x[8], reverse=True)

        for component in available_components:
            short_description = (component[2][:60] + '...') if len (component[2]) > 60 else component[2]

            item = self.create_item (component[0], component[1], short_description, component[8])

            code_name = component[1].lower ().replace (" ", "_")

            component_switch = Gtk.Switch ()
            component_switch.set_name (component[1])
            component_switch.props.halign = Gtk.Align.END
            component_switch.props.valign = Gtk.Align.CENTER
            component_switch.connect ("notify::active", self.callback, code_name, component[3], component[4], component[7])

            if self.check_if_enabled (code_name, component[3], component[6]):
                component_switch.set_active (True)

            if code_name == "core_icon_theme":
                current_theme = system_settings.get_string ("icon-theme")
                if current_theme == icon_theme_name:
                    component_switch.set_active (True)

            wrap = Gtk.HBox (0)
            wrap.pack_start (item, True, True, 0)
            wrap.pack_end (component_switch, False, False, 2)

            if self.check_if_installed (code_name, component[5]) is False:
                wrap.set_sensitive (False)

            wrap.set_tooltip_text (component[2])

            listbox.add (wrap)

        return scroller

    def list_plugins (self):
        for root, folders, files in os.walk (plugins_directory):
            return folders

    def fetch_plugin_info (self, plugin):
        with open ('{}{}{}'.format (plugins_directory, plugin, "/metadata.json")) as data_file:    
            return json.load (data_file)

    def check_if_installed (self, app_name, check_locations):
        if app_name == "elementary+_icon_theme":
            return True

        for location in check_locations:
            if location.startswith ("~"):
                location = list (location)
                location[0] = home
                location = "".join (location)
            if os.path.isfile (location):
                return True

        return False

    def check_if_enabled (self, app_name, sni_qt_prefix, custom_check_location):
        if custom_check_location.startswith ("~"):
            custom_check_location = list (custom_check_location)
            custom_check_location[0] = home
            custom_check_location = "".join (custom_check_location)

        if custom_check_location != "":
            if os.path.isfile (custom_check_location):
                return True
            else:
                return False
        elif sni_qt_prefix != "":
            if os.path.isdir ("{}{}{}".format (home, "/.local/share/sni-qt/icons/", sni_qt_prefix)):
                return True
            else:
                return False
        else:
            return False

    def create_item (self, icon_name, app_label, short_description, enabled):
        grid = Gtk.Grid ()
        grid.set_border_width (16)
        grid.set_row_spacing (4)
        grid.set_column_spacing (16)

        if enabled is True:
            label = Gtk.Label ("<big>%s</big>" % app_label)
        else:
            label = Gtk.Label ("<big>%s  (Not installed)</big>" % app_label)
        label.set_use_markup (True)
        label.set_alignment (0.0, 0.5)

        icon = Gtk.Image.new_from_icon_name (icon_name, Gtk.IconSize.DIALOG)

        description = Gtk.Label (short_description)
        description.get_style_context ().add_class ("dim-label")
        description.set_alignment (0.0, 0.5)

        grid.attach (icon, 0, 0, 1, 2)
        grid.attach (label, 1, 0, 1, 1)
        grid.attach (description, 1, 1, 1, 1)

        return grid

    def search_handler (self, widget):
        widget.freeze_notify ()
        self.search_bar.set_search_mode (widget.get_active ())
        widget.thaw_notify ()

    def search_changed (self, widget, data=None):
        text = widget.get_text ().strip ()
        if text == "":
            self.search_bar.set_search_mode (False)

        active = False if text == "" else True

        self.search_button.freeze_notify ()
        self.search_button.set_active (active)
        self.search_button.thaw_notify ()
        self.searching (widget)

    def searching (self, widget, event=None):
        text = widget.get_text ().strip ()
        self.listbox.set_filter_func (self.filter, text)

        result = False

        for child in self.listbox.get_children ():
            if child.get_visible () and child.get_child_visible ():
                result = True
                break

        if not result:
            self.placeholder.set_markup ("<big>No results</big>")

    def filter (self, row, text):
        name = row.get_children ()[0].get_children ()[0].get_children ()[1].get_text ()
        description = row.get_children ()[0].get_tooltip_text ()

        if text.lower () in name.lower () or text.lower () in description.lower ():
            return True
        else:
            return False

    def callback (self, widget, event, data, sni_qt_prefix, install_method, plugin):
        if widget.get_active () == 1:
            if data == "elementary+_icon_theme":
                installer.toggle_theme ("install", plugins_directory)
            else:
                if not self.check_if_enabled (data, sni_qt_prefix, ""):
                    try:
                        installer.install (data, install_method, sni_qt_prefix, configurator_directory, plugins_directory, plugin)
                    except Exception:
                        widget.set_active (False)
        else:
            if data == "elementary+_icon_theme":
                installer.toggle_theme ("remove", plugins_directory)
            else:
                try:
                    installer.remove (data, install_method, sni_qt_prefix, configurator_directory, plugins_directory, plugin)
                except Exception:
                    widget.set_active (False)

    def patch_sni_qt (self):
        print "Installing patched sni-qt (amd64)"
        self.notify (
            'This may take a while', 
            'Please don\'t close the window', 
            'preferences-desktop'
        )
        self.popen_and_call (self.on_exit, ['pkexec', "{}{}".format (configurator_directory, "sni-qt.sh")])
        
        install_dialog = Gtk.MessageDialog (self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.CANCEL, "Installing patched sni-qt")
        install_dialog.format_secondary_text ("This may take a while, please wait.")
        self.install_dialog = install_dialog
        spinner = Gtk.Spinner ()
        spinner.start ()
        box = install_dialog.get_content_area ()
        box.add (spinner)
        install_dialog.show_all ()
        install_dialog.run()
        install_dialog.destroy()

    def popen_and_call (self, on_exit, popen_arguments):
        def run_in_thread(on_exit, popen_arguments):
            proc = subprocess.Popen(popen_arguments)
            proc.wait()
            on_exit ()
            return

        thread = threading.Thread(target=run_in_thread, args=(self.on_exit, popen_arguments))
        thread.start()

        return thread

    def on_exit (self):
        self.install_dialog.close ()

    def notify (self, message_one, message_two, icon):
        try:
            notification = Notify.Notification.new (message_one, message_two, icon)
            notification.set_urgency (1)
            notification.show ()
            del notification
        except:
            pass


win = ConfiguratorWindow ()
win.connect ("delete-event", Gtk.main_quit)
win.show_all ()
Gtk.main ()
