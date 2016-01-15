#!/bin/bash
SRCFILE="/usr/lib/i386-linux-gnu/qt4/plugins/systemtrayicon/libsni-qt.so"
DSTFILE="/opt/teamviewer/tv_bin/RTlib/plugins/systemtrayicon/libsni-qt.so"
DSTFILEBAK="/opt/teamviewer/tv_bin/RTlib/plugins/systemtrayicon/libsni-qt.so.bak"
cp $DSTFILE $DSTFILEBAK
cp $SRCFILE $DSTFILE
update-desktop-database