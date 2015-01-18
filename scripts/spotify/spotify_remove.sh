#!/bin/bash
dire=`find /tmp/ -name 'sni-qt_spotify*'`
cd $dire
subdire="icons/hicolor/16x16/apps/"
cd $subdire
filename=`find . -name 'spotify_*'`
filename="${filename%.*}"
uuid=`cut -d '_' -f3 <<< $filename`
rm ~/.local/share/sni-qt/icons/$uuid.png
