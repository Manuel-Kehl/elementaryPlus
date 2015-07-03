#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "$DIR"

sniqtPrefix="spotify"

source ../whattouse.sh

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
            rm -rf ~/.local/share/sni-qt/icons/$sniqtPrefix
            mkdir -p ~/.local/share/sni-qt/icons/$sniqtPrefix
            if [ $whatToUse == "cp" ]
                then
                    cp ./icons/icon.png ~/.local/share/sni-qt/icons/$sniqtPrefix/$uuid.png
            elif [ $whatToUse == "ln" ]
                then
                    ln -sf $DIR/icons/icon.png ~/.local/share/sni-qt/icons/$sniqtPrefix/$uuid.png
            fi
        else
            echo "Failed"
            notify-send "Failed to install Spotify icons" "Please run Spotify and try again" -i "preferences-desktop"
        fi
elif [ $1 == "--remove" ]
    then
        rm -rf ~/.local/share/sni-qt/icons/$sniqtPrefix
fi
exit
