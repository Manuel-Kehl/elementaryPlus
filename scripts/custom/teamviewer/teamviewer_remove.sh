#!/bin/bash
DSTFILE="/opt/teamviewer/tv_bin/RTlib/plugins/systemtrayicon/libsni-qt.so"
DSTFILEBAK="/opt/teamviewer/tv_bin/RTlib/plugins/systemtrayicon/libsni-qt.so.bak"
cp $DSTFILEBAK $DSTFILE
update-desktop-database