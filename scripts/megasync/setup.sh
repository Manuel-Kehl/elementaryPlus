#!/bin/bash

cd scripts/megasync/

if [ $1 == "--install" ]
    then
        mkdir -p ~/.local/share/sni-qt/icons
        cp ./icons/* ~/.local/share/sni-qt/icons/
elif [ $1 == "--remove" ]
    then
        for entry in icons/*
            do
                echo "$entry"
                rm ~/.local/share/sni-qt/$entry
            done
fi
exit