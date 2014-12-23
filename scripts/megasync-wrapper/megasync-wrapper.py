#!/usr/bin/env python
import subprocess
import os
import shutil
import stat
import re

mega_env = os.environ.copy()
mega_bin = '/usr/bin/megasync'

def is_running(process):
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    
    for x in s.stdout:
        if re.search(process, x):
            return True

    return False

if __name__ == '__main__':
    icons_map = [
        ('5e6bbab03e062640f0a3c6c540f119a7', 'megasync_start.png'),
        ('a8fb04239cb3d37ca409bd8a55eaa7d8', 'megasync_idle.png'),
        ('58ebdeee7b844ca4da145dcf572f322c', 'megasync_sync.png'),
        ('42214812629c8b59f19722c2b22938d3', 'megasync_pause.png')
    ]
    if is_running(mega_bin):
        print 'MEGAsync already running'
        subprocess.call([mega_bin]);
        exit(1)
        
    pid = subprocess.Popen([mega_bin], env=mega_env).pid
    substr = "sni-qt_megasync_{0}".format(pid)

    finished = False
    folder_name = ""

    while not finished:
        for name in os.listdir("/tmp/"):
            if name.startswith(substr):
                folder_name = name
                finished = True

    icons_folder = "/tmp/" + folder_name + "/icons/hicolor/22x22/apps/"
    os.makedirs(icons_folder)

    subst_icons_folder = os.path.dirname(os.path.realpath(__file__)) + '/icons/'
    
    for (uid, subst_icon) in icons_map:
        mega_icon = icons_folder + 'megasync_{0}_{1}.png'.format(pid, uid)
        shutil.copy(subst_icons_folder + subst_icon, mega_icon)
        os.chmod(mega_icon, stat.S_IRUSR)
    

