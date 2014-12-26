#!/bin/bash

(( EUID != 0 )) && exec sudo -- "$0" "$@"

read -p "Do you want to replace the default Spotify status icon with the new one [Y/n]?" yn

if [[ $yn =~ ^[Yy]$ ]] || [[ $yn == "" ]]; then

    apt-get install zip

    tmp_dir="/tmp/fsi-$(date +%s)"

    echo "Entering temporary directory"
    mkdir $tmp_dir
    cd $tmp_dir

    echo "Making a copy of resources.zip"
    cp /opt/spotify/spotify-client/Data/resources.zip resources_old.zip
    unzip resources_old.zip -d resources_old/

    echo "Replacing the icon"
    cp spotify_icon.ico resources_old/_linux/spotify_icon.ico

    echo "Packaging resources.zip back up"
    cd resources_old/
    zip -r resources_patched.zip .
    cd ..
    mv resources_old/resources_patched.zip .

    echo "Replacing current resources.zip"
    sudo cp resources_patched.zip /opt/spotify/spotify-client/Data/resources.zip

    echo "Cleaning up"
    rm -rf $tmp_dir

    echo "The Spotify icon has been replaced successfuly! Start Spotify again to check it out."
fi
