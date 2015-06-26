#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

sniqtPrefix="spotify"

if [ $1 == "--install" ]
    then
        curr=`pwd`
        dire=`find /tmp/ -name 'sni-qt_spotify*'`
        if [[ -n $dire ]]; then
            cd $dire
            subdire="icons/hicolor/512x512/apps/"
            cd $subdire
            filename=`find . -name 'spotify_*'`
            filename="${filename%.*}"
            uuid=`cut -d '_' -f3 <<< $filename`
            cd $curr
            mkdir -p ~/.local/share/sni-qt/icons/$sniqtPrefix
            cp ./icons/icon.png ~/.local/share/sni-qt/icons/$sniqtPrefix/$uuid.png
        else
            echo "Failed"
            notify-send "Failed to install Spotify icons" "Please run Spotify and try again" -i "preferences-desktop"
        fi
elif [ $1 == "--remove" ]
    then
        rm -rf ~/.local/share/sni-qt/icons/$sniqtPrefix
fi
exit
