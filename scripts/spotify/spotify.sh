#!/bin/bash

apt-get install zip
tmp_dir="/tmp/elementaryPlus/spotify"
mkdir -p $tmp_dir
cp icons/spotify_icon.ico $tmp_dir
cd $tmp_dir
cp /opt/spotify/spotify-client/Data/resources.zip resources_old.zip
unzip resources_old.zip -d resources_old/
mv spotify_icon.ico resources_old/_linux/spotify_icon.ico
cd resources_old/
zip -r resources_patched.zip .
cd ..
mv resources_old/resources_patched.zip .
cp resources_patched.zip /opt/spotify/spotify-client/Data/resources.zip
exit
