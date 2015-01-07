#!/usr/bin/env python

from gi.repository import Gtk, Gio
import os.path
import os
import sys



installed = "/tmp/elementaryPlus.installed"
sniqt = "/tmp/sni-qt.patch.installed"
toinstall = []
toremove = []
curr = os.path.dirname(os.path.realpath(__file__)) + os.sep

class confirmDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Confirm", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Are you sure you want to appply these changes?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class InstallerWindow(Gtk.Window):

    f = open(installed, 'a')
    f.close()

    def callback(self, widget, event, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

        if widget.get_active() == 1:
            if data not in open(installed).read():
                toinstall.append(data)
            elif toremove != [] and data in open(installed).read():
                toremove.remove(data)
        else:
            if data in open(installed).read():
                toremove.append(data)
            else:
                toinstall.remove(data)

        print "To install: ",toinstall
        print "To remove: ",toremove

    def install(self, widget, event, data=None):

        if toinstall != [] or toremove != []:
            dialog = confirmDialog(self)
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.OK:
                if toinstall != []:
                    for data in toinstall:
                        if data != "core" and os.path.isfile(sniqt) == False:
                            print "Installing patched sni-qt"
                            os.system("bash ./sni-qt.sh")
                            f = open(sniqt, 'a')
                            f.close()

                        os.chdir(curr+data+"/")
                        os.system("bash ./"+data+".sh")
                        f = open(installed,"a")
                        f.write(data+"\n")
                        f.close()
                        print data+" was installed"
                        os.chdir(curr)

                if toremove != []:
                    for data in toremove:
                        os.chdir(curr+data+"/")
                        os.system("bash ./"+data+"_remove.sh")
                        f = open(installed,"r")
                        lines = f.readlines()
                        f.close()
                        f = open(installed,"w")
                        for line in lines:
                            if line!=data+"\n":
                                f.write(line)

                        print data+" was removed"
                        os.chdir(curr)
                del toremove[:]
                del toinstall[:]
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
        options = {
            "Core icon theme":"core",
            "MEGAsync":"megasync",
            "Spotify":"spotify",
            "Skype":"skype",
            "OwnCloud":"owncloud"
        }
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

        lni = len(options.keys())
        table = Gtk.Table(lni, 3, True)
        table.set_row_spacings(15)
        table.set_col_spacings(10)
        self.add(table)

        for i in range(len(options.keys())):

            optionLabel = Gtk.Label(options.keys()[i], xalign=0)

            optionSwitch = Gtk.Switch()
            optionSwitch.props.halign = Gtk.Align.CENTER
            optionSwitch.connect("notify::active", self.callback, options.values()[i])

            if options.values()[i] in open(installed).read():
                optionSwitch.set_active(True)

            table.attach(optionLabel, 0, 2, i, i+1)
            table.attach(optionSwitch, 2, 3, i, i+1)

win = InstallerWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()