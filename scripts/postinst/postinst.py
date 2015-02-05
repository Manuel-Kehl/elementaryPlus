#!/usr/bin/env python

import os
import pwd
import grp
from gi.repository import Gio


def dropPrivileges(uid_name='nobody', gid_name='nogroup'):
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    old_umask = os.umask(077)


def changeComp():
    settings = Gio.Settings.new("apps.elementaryPlusInstaller")
    installedComponents = settings.get_strv("installed")

    if "core" not in installedComponents:
        installedComponents.append("core")
        settings.set_strv("installed", installedComponents)
        print "Core added"


if __name__ == '__main__':
    dropPrivileges()
    changeComp()
