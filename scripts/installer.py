#!/usr/bin/env python

from gi.repository import Gtk, Gio
import os.path
import os
import sys
import shutil

curr = os.path.dirname(os.path.realpath(__file__)) + os.sep

if os.path.isfile("/usr/share/glib-2.0/schemas/apps.elementaryPlusInstaller.gschema.xml") == False:
    srcfile = curr+"apps.elementaryPlusInstaller.gschema.xml"
    dstdir = "/usr/share/glib-2.0/schemas/"
    shutil.copy(srcfile, dstdir)
    os.system("glib-compile-schemas /usr/share/glib-2.0/schemas/")
    print "schemas copied"


components = {
    "Core icon theme":"core",
    "MEGAsync":"megasync",
    "Spotify":"spotify",
    "Skype":"skype",
    "OwnCloud":"owncloud"
}

toInstall = []
toRemove = []

settings = Gio.Settings.new("apps.elementaryPlusInstaller")
installedComponents = settings.get_strv("installed")
patchedSniqt = settings.get_boolean("sniqt-patched")
#settings.reset("installed")
#settings.reset("sniqt-patched")

print "Installed components: ", installedComponents
print "Sni-qt %s patched" % (("IS NOT", "IS")[patchedSniqt])

class confirmDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Confirm", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 100)

        toInstallList = ", ".join([x[0] for x in components.items() if x[1] in toInstall])
        toRemoveList = ", ".join([x[0] for x in components.items() if x[1] in toRemove])
        labelToInstall = Gtk.Label("To install: "+toInstallList)
        labelToRemove = Gtk.Label("To remove: "+toRemoveList)
        labelSeparator = Gtk.Label(" ")
        label = Gtk.Label("Are you sure you want to appply these changes?")

        box = self.get_content_area()
        if toInstall != []:
            box.add(labelToInstall)
        if toRemove != []:
            box.add(labelToRemove)
        box.add(labelSeparator)
        box.add(label)
        self.show_all()

class InstallerWindow(Gtk.Window):

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

        print "To install: ",toInstall
        print "To remove: ",toRemove

    def install(self, widget, event, data=None):

        if toInstall != [] or toRemove != []:
            dialog = confirmDialog(self)
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.OK:
                if toInstall != []:
                    for data in toInstall[:]:
                        patchedSniqt = settings.get_boolean("sniqt-patched")
                        if data != "core" and patchedSniqt == False:
                            print "Installing patched sni-qt"
                            os.system("bash ./sni-qt.sh")
                            settings.set_boolean("sniqt-patched", True)

                        os.chdir(curr+data+"/")
                        os.system("bash ./"+data+".sh")
                        print data+" was installed"
                        os.chdir(curr)
                    mergedInstalledComponents = installedComponents + toInstall
                    settings.set_strv("installed", mergedInstalledComponents)                      
                            
                if toRemove != []:
                    for data in toRemove[:]:
                        os.chdir(curr+data+"/")
                        os.system("bash ./"+data+"_remove.sh")
                        print data+" was removed"
                        os.chdir(curr)
                    installedComponents[:] = [ item for item in installedComponents if item != data ]
                    settings.set_strv("installed", installedComponents)

                toInstall[:] = []
                toRemove[:] = []

                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "All changes applied")
                dialog.format_secondary_text("Check out your new icons!")
                dialog.run()
                dialog.destroy()
            elif response == Gtk.ResponseType.CANCEL:
                print("The Cancel button was clicked")


        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "There is nothing to apply")
            dialog.format_secondary_text("You must change an option before applying")
            dialog.run()
            dialog.destroy()



    def __init__(self):
        Gtk.Window.__init__(self, title="elementaryPlus Installer")
        self.set_border_width(10)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "elementaryPlus"
        self.set_titlebar(hb)
        hb.set_subtitle("Installer")

        installButton = Gtk.Button(label="Apply")
        installButton.connect("clicked", self.install, "yes")   
        hb.pack_end(installButton)

        lni = len(components.keys())
        table = Gtk.Table(lni, 3, True)
        table.set_row_spacings(15)
        table.set_col_spacings(10)
        self.add(table)

        for i in range(len(components.keys())):

            componentLabel = Gtk.Label(components.keys()[i], xalign=0)

            componentSwitch = Gtk.Switch()
            componentSwitch.props.halign = Gtk.Align.CENTER
            componentSwitch.connect("notify::active", self.callback, components.values()[i])

            if components.values()[i] in installedComponents:
                componentSwitch.set_active(True)

            table.attach(componentLabel, 0, 2, i, i+1)
            table.attach(componentSwitch, 2, 3, i, i+1)

win = InstallerWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()