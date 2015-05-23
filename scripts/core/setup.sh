#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

if [ $1 == "--install" ]
    then
        mkdir ~/.icons
        cp -R ../../elementaryPlus ~/.icons/
elif [ $1 == "--remove" ]
    then
        rm -rf ~/.icons/elementaryPlus
fi
exit