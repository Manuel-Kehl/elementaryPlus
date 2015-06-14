#!/usr/bin/env python

from gi.repository import Gtk, Gio, Notify
import os
import sys
import subprocess

if not (Gtk.get_major_version() == 3 and Gtk.get_minor_version() >= 14):
    sys.exit("You need to have GTK 3.14 or newer to run this script")

appName = "elementary+ Configurator"

fromPPA = False

scripts = os.getcwd() + "/scripts/"
schema = "/usr/share/glib-2.0/schemas/apps.elementaryPlusConfigurator.gschema.xml"

if os.path.isfile(schema) is False:
    subprocess.call(["pkexec", scripts + "first_start.sh", scripts])

iconMegaList = [
    [
        "Core icon theme",
        "",
        "The core elementary+ icon theme",
        "preferences-desktop"
    ],
    [
        "flareGet",
        "/usr/bin/flareget",
        "FlareGet is a full featured, multi-threaded download manager and accelerator for Windows, Mac and Linux",
        "flareget"
    ],
    [
        "Google Music Manager",
        "/opt/google/musicmanager/google-musicmanager",
        "With Google Play Music for Chrome or Music Manager, you can add your personal music library to the cloud",
        "google-musicmanager"
    ],
    [
        "MEGAsync",
        "/usr/bin/megasync",
        "MEGAsync is a free online storage service",
        "mega"
    ],
    [
        "OwnCloud",
        "/usr/bin/owncloud",
        "An enterprise file sharing solution for online collaboration and storage",
        "owncloud"
    ],
    [
        "Seafile Client",
        "/usr/bin/seafile-applet",
        "The Seafile desktop client",
        "seafile"
    ],
    [
        "Skype",
        "/usr/bin/skype",
        "Stay in touch with your family and friends for free on Skype",
        "skype"
    ],
    [
        "Spotify",
        "/opt/spotify/spotify-client/spotify",
        "Spotify is a digital music service that gives you access to millions of songs",
        "spotify-client"
    ],
    [
        "Telegram Desktop",
        "%s/.TelegramDesktop/tdata/icon.png" % (os.getenv('HOME')),
        "Telegram is a messaging app with a focus on speed and security, it's super fast, simple and free",
        "telegram"
    ],
    [
        "Tomahawk",
        "/usr/bin/tomahawk",
        "A new kind of music player that invites all your streams, downloads, cloud music storage, playlists, radio stations and friends to the same party. It's about time they all mingle",
        "tomahawk"
    ],
    [
        "WizNote",
        "/usr/bin/WizNote",
        "Wiznote is a cloud based notes solution which helps personal and professional to take notes and collaborate with team members",
        "wiznote"
    ]
]

if fromPPA is True:
    iconMegaList.pop(0)

components = []

iconTheme = Gtk.IconTheme
defaultIconTheme = iconTheme.get_default()

for a in iconMegaList:
    name = a[0]
    codeName = a[0].lower().replace(" ", "_")
    shortDesc = (a[2][:60] + '..') if len(a[2]) > 60 else a[2]
    icon = ("package-x-generic") if iconTheme.has_icon(defaultIconTheme, a[3]) == False else a[3]
    enabled = (True) if os.path.isfile(a[1]) else False
    if codeName == "core_icon_theme":
        components.append([name, "core", shortDesc, icon, True])
    else:
        components.append([name, codeName, shortDesc, icon, enabled])


toInstall = []
toRemove = []

iconThemeName = "elementaryPlus"

settings = Gio.Settings.new("apps.elementaryPlusConfigurator")
installedComponents = settings.get_strv("installed")
patchedSniqt = settings.get_boolean("sniqt-patched")
# settings.reset("installed")
# settings.reset("sniqt-patched")
# settings.reset("previous-icon-theme")

systemSettings = Gio.Settings.new("org.gnome.desktop.interface")

print "Installed components: ", installedComponents
print "Sni-qt %s patched" % (("IS NOT", "IS")[patchedSniqt])


class confirmDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Confirm", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 100)
        self.set_resizable(False)
        self.set_border_width(6)

        toInstallList = ", ".join([x[0] for x in components if x[1] in toInstall])
        toRemoveList = ", ".join([x[0] for x in components if x[1] in toRemove])
        labelToInstall = Gtk.Label("To install: " + toInstallList)
        labelToRemove = Gtk.Label("To remove: " + toRemoveList + "\n")
        labelQuestion = Gtk.Label("Are you sure you want to appply these changes?\n")

        box = self.get_content_area()
        if toInstall != []:
            box.add(labelToInstall)
        if toRemove != []:
            box.add(labelToRemove)
        box.add(labelQuestion)
        self.show_all()


class useThemeDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Switch to elementary+", parent, 0,
                            (Gtk.STOCK_NO, Gtk.ResponseType.NO,
                                Gtk.STOCK_YES, Gtk.ResponseType.YES))

        self.set_default_size(150, 100)
        self.set_resizable(False)
        self.set_border_width(6)

        labelQuestion = Gtk.Label("Would you like to switch to elementary+ now?", xalign=0)
        labelInfo = Gtk.Label("This will replace your current icon theme.\n", xalign=0)
        labelInfo1 = Gtk.Label("You can swith back to your previous icon theme \
            \nby removing the \"Core icon theme\" from the installer \
            \nor by selecting it in elementary Tweaks.")

        box = self.get_content_area()
        box.add(labelQuestion)
        box.add(labelInfo)
        box.add(labelInfo1)
        self.show_all()


class InstallerWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title=appName)
        self.set_border_width(10)
        self.set_size_request(500, 500)
        self.set_icon_name("preferences-desktop")

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "elementary+"
        self.hb.set_subtitle("Configurator")
        self.set_titlebar(self.hb)

        self.installButton = Gtk.Button(label="Apply")
        self.installButton.set_sensitive(False)
        self.installButton.get_style_context().add_class("suggested-action")
        self.installButton.connect("clicked", self.install, "yes")

        self.hb.pack_end(self.installButton)

        Notify.init(appName)

        self.add(self.build_ui())

    def notify(self, messageOne, messageTwo, icon):
        notification = Notify.Notification.new(messageOne, messageTwo, icon)
        notification.show()

    def build_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        availableIcons = self.create_icons_page()
        vbox.pack_start(availableIcons, True, True, 0)

        return vbox

    def create_icons_page(self):
        scroller = Gtk.ScrolledWindow(None, None)
        scroller.set_shadow_type(Gtk.ShadowType.IN)
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        lbox = Gtk.ListBox()
        lbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scroller.add(lbox)

        for i in range(len(components)):
            longDesc = iconMegaList[i][2]
            item = self.create_item(components[i][0], components[i][3], components[i][2], longDesc)

            componentSwitch = Gtk.Switch()
            componentSwitch.props.halign = Gtk.Align.END
            componentSwitch.props.valign = Gtk.Align.CENTER
            componentSwitch.connect("notify::active", self.callback, components[i][1])

            if components[i][1] in installedComponents:
                componentSwitch.set_active(True)

            wrap = Gtk.HBox(0)
            wrap.pack_start(item, True, True, 0)
            wrap.pack_end(componentSwitch, False, False, 2)

            if components[i][4] is False:
                wrap.set_sensitive(False)
                wrap.set_tooltip_text("You must first install this app to select this!")
            else:
                wrap.set_tooltip_text(longDesc)

            lbox.add(wrap)

        return scroller

    def create_item(self, name, iconName, shortDesc, longDesc):
        grid = Gtk.Grid()
        grid.set_border_width(16)
        grid.set_row_spacing(4)
        grid.set_column_spacing(16)

        label = Gtk.Label("<big>%s</big>" % name)
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

    def notsensitive():
        notify("dsa", "dsa", "dasd")

    def callback(self, widget, event, data=None):

        installedComponents = settings.get_strv("installed")

        print "\n%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

        if widget.get_active() == 1:
            if toRemove != [] and data in installedComponents:
                toRemove.remove(data)
            elif data not in installedComponents:
                toInstall.append(data)
        else:
            if data in installedComponents:
                toRemove.append(data)
            else:
                toInstall.remove(data)

        if len(toInstall) != 0 or len(toRemove) != 0:
            self.installButton.set_sensitive(True)
        else:
            self.installButton.set_sensitive(False)

        print "To install: ", toInstall
        print "To remove: ", toRemove

    def install(self, widget, event, data=None):

        if len(toInstall) != 0 or len(toRemove) != 0:
            dialog = confirmDialog(self)
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.OK:
                if len(toInstall) != 0:
                    for data in toInstall[:]:
                        patchedSniqt = settings.get_boolean("sniqt-patched")
                        if data != "core" and data != "telegram_desktop" and patchedSniqt is False:
                            print "Installing patched sni-qt"
                            self.notify('This may take a while', 'Please don\'t close the window', 'gnome-tweak-tool')
                            if subprocess.call(['pkexec', scripts + "sni-qt.sh"]) == 0:
                                settings.set_boolean("sniqt-patched", True)

                        subprocess.call(['bash', scripts + data + "/setup.sh", "--install"])
                        print data + " was installed"

                        if data == "core":
                            dialog = useThemeDialog(self)
                            response = dialog.run()
                            dialog.destroy()

                            if response == Gtk.ResponseType.YES:
                                currentTheme = systemSettings.get_string("icon-theme")
                                settings.set_string("previous-icon-theme", currentTheme)
                                systemSettings.set_string("icon-theme", iconThemeName)
                            elif response == Gtk.ResponseType.NO:
                                print "Theme not changed"

                        installedComponents.append(data)
                    settings.set_strv("installed", installedComponents)

                if len(toRemove) != 0:
                    for data in toRemove[:]:
                        subprocess.call(['bash', scripts + data + "/setup.sh", "--remove"])
                        print data + " was removed"
                        if data == "core":
                            currentTheme = systemSettings.get_string("icon-theme")
                            if currentTheme == iconThemeName:
                                previousIconTheme = settings.get_string("previous-icon-theme")
                                systemSettings.set_string("icon-theme", previousIconTheme)

                        installedComponents.remove(data)
                    settings.set_strv("installed", installedComponents)

                toRemove[:] = []
                toInstall[:] = []

                self.notify('All changes applied', 'Check out your new icons!', 'gnome-tweak-tool')

                self.installButton.set_sensitive(False)

            elif response == Gtk.ResponseType.CANCEL:
                print("The Cancel button was clicked")
                self.installButton.set_sensitive(True)

win = InstallerWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
