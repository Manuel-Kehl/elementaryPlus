#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

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
            mkdir -p ~/.local/share/sni-qt/icons
            cp ./icons/icon.png ~/.local/share/sni-qt/icons/$uuid.png
        else
            echo "Running spotify."
            timeout 1 /opt/spotify/spotify-client/spotify
            bash setup.sh --install
        fi
elif [ $1 == "--remove" ]
    then
        dire=`find /tmp/ -name 'sni-qt_spotify*'`
        if [[ -n $dire ]]; then
            cd $dire
            subdire="icons/hicolor/512x512/apps/"
            cd $subdire
            filename=`find . -name 'spotify_*'`
            filename="${filename%.*}"
            uuid=`cut -d '_' -f3 <<< $filename`
            rm ~/.local/share/sni-qt/icons/$uuid.png
        else
            timeout 1 /opt/spotify/spotify-client/spotify
            bash setup.sh --remove
        fi
fi
exit
