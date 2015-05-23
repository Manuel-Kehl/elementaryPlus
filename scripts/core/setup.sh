#!/bin/bash

cd scripts/core/

if [ $1 == "--install" ]
    then
        mkdir ~/.icons
        cp -R ../../elementaryPlus ~/.icons/
elif [ $1 == "--remove" ]
    then
        rm -rf ~/.icons/elementaryPlus
fi
exit