#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

sniqtPrefix="python2.7"

if [ $1 == "--install" ]
    then
        mkdir -p ~/.local/share/sni-qt/icons/$sniqtPrefix
        cp ./icons/* ~/.local/share/sni-qt/icons/$sniqtPrefix
elif [ $1 == "--remove" ]
    then
        rm -rf ~/.local/share/sni-qt/icons/$sniqtPrefix
fi
exit
