#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "$DIR"

sniqtPrefix="owncloud"

source ../whattouse.sh

if [ $1 == "--install" ]
    then
        rm -rf ~/.local/share/sni-qt/icons/$sniqtPrefix
        mkdir -p ~/.local/share/sni-qt/icons/$sniqtPrefix
        if [ $whatToUse == "cp" ]
            then
                cp ./icons/* ~/.local/share/sni-qt/icons/$sniqtPrefix
        elif [ $whatToUse == "ln" ]
            then
                ln -sf $DIR/icons/* ~/.local/share/sni-qt/icons/$sniqtPrefix
        fi
elif [ $1 == "--remove" ]
    then
        rm -rf ~/.local/share/sni-qt/icons/$sniqtPrefix
fi
exit